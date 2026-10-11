"""Local-only audio extraction service. Python standard library, no pip dependencies."""

from __future__ import annotations

import argparse
import collections
import json
import mimetypes
import os
import queue
import re
import secrets
import shutil
import socket
import subprocess
import threading
import time
import uuid
import webbrowser
import zipfile
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse

from formats import ValidationError, build_plan, normalized_settings, public_profiles

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "web"
TERMINAL = {"completed", "failed", "cancelled"}
MAX_UPLOAD = 100 * 1024 ** 3
NO_WINDOW = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0


def run_process(args, **kwargs):
    return subprocess.run(args, creationflags=NO_WINDOW, **kwargs)


def resolve_binary(name):
    executable = name + (".exe" if os.name == "nt" else "")
    candidates = [os.environ.get(name.upper() + "_PATH"), str(ROOT / "bin" / executable), shutil.which(name)]
    for candidate in candidates:
        if not candidate:
            continue
        try:
            result = run_process([candidate, "-version"], capture_output=True, timeout=10)
            if result.returncode == 0:
                return str(Path(candidate).resolve())
        except (OSError, subprocess.SubprocessError):
            continue
    return None


def safe_name(name):
    name = str(name).replace("\\", "/").rsplit("/", 1)[-1]
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name).strip(" .")[:180]
    if not name:
        return "audio"
    if name.split(".")[0].upper() in {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}:
        name = "_" + name
    return name


class Application:
    def __init__(self, data_dir=None, output_dir=None):
        self.data_dir = Path(data_dir or ROOT / ".runtime").resolve()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.uploads = self.data_dir / "uploads"
        self.previews = self.data_dir / "previews"
        self.uploads.mkdir(exist_ok=True)
        self.previews.mkdir(exist_ok=True)
        self.lock = threading.RLock()
        self.dialog_lock = threading.Lock()
        self.preview_lock = threading.Lock()
        self.token = secrets.token_urlsafe(32)
        self.ffmpeg = resolve_binary("ffmpeg")
        self.ffprobe = resolve_binary("ffprobe")
        self.encoders, self.muxers = set(), set()
        self.version = ""
        if self.ffmpeg:
            self.version = run_process([self.ffmpeg, "-version"], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.splitlines()[0]
            text = run_process([self.ffmpeg, "-hide_banner", "-encoders"], capture_output=True, text=True).stdout
            self.encoders = set(re.findall(r"^ A[.A-Z]{5}\s+(\S+)", text, re.M))
            text = run_process([self.ffmpeg, "-hide_banner", "-muxers"], capture_output=True, text=True).stdout
            self.muxers = set(re.findall(r"^\s*E\s+(\S+)", text, re.M))
        self.state_path = self.data_dir / "state.json"
        self.files, self.jobs, self.settings = {}, {}, {"output_dir": str(Path(output_dir or ROOT / "output").resolve())}
        if self.state_path.exists():
            try:
                saved = json.loads(self.state_path.read_text("utf-8"))
                self.files, self.jobs = saved.get("files", {}), saved.get("jobs", {})
                self.settings.update(saved.get("settings", {}))
            except (OSError, ValueError):
                pass
        if output_dir:
            self.settings["output_dir"] = str(Path(output_dir).resolve())
        for job in self.jobs.values():
            if job["status"] not in TERMINAL:
                job.update(status="cancelled", error="服务已重新启动，请点击重试。", finished_at=time.time())
                for key in ("temp_path", "reserved_path"):
                    if job.get(key):
                        Path(job[key]).unlink(missing_ok=True)
        for path in self.uploads.glob("*.part"):
            path.unlink(missing_ok=True)
        self.processes = {}
        self.work = queue.Queue()
        self.stop_event = threading.Event()
        self.worker = threading.Thread(target=self.worker_loop, daemon=True, name="audio-worker")
        self.worker.start()
        self.save()

    def save(self):
        with self.lock:
            temp = self.state_path.with_suffix(".tmp")
            temp.write_text(json.dumps({"files": self.files, "jobs": self.jobs, "settings": self.settings}, ensure_ascii=False, indent=2), encoding="utf-8")
            temp.replace(self.state_path)

    def require_engine(self):
        if not self.ffmpeg or not self.ffprobe:
            raise ValidationError("找不到 FFmpeg / FFprobe。请把两个程序放进 bin 文件夹，或安装并加入 PATH 后重新启动。")

    def probe(self, path):
        self.require_engine()
        try:
            result = run_process([self.ffprobe, "-v", "error", "-protocol_whitelist", "file,pipe", "-show_format", "-show_streams", "-of", "json", str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
        except subprocess.TimeoutExpired:
            raise ValidationError("读取文件超时，请检查视频文件是否完整。") from None
        if result.returncode:
            raise ValidationError("无法读取此文件。它可能已损坏，或不是受支持的音视频文件。")
        info = json.loads(result.stdout)
        streams = []
        duration = float(info.get("format", {}).get("duration", 0) or 0)
        for stream in info.get("streams", []):
            if stream.get("codec_type") != "audio":
                continue
            raw_bits = stream.get("bits_per_raw_sample") or stream.get("bits_per_sample") or 0
            try:
                bits = int(raw_bits)
            except (TypeError, ValueError):
                bits = 0
            stream_duration = float(stream.get("duration", 0) or 0)
            duration = max(duration, stream_duration)
            streams.append({"index": stream["index"], "codec": stream.get("codec_name", "unknown"),
                            "sample_rate": int(stream.get("sample_rate", 0) or 0),
                            "channels": int(stream.get("channels", 0) or 0), "bit_depth": bits,
                            "bitrate": int(stream.get("bit_rate", 0) or 0),
                            "language": stream.get("tags", {}).get("language", ""),
                            "title": stream.get("tags", {}).get("title", ""),
                            "default": bool(stream.get("disposition", {}).get("default", 0))})
        if not streams:
            raise ValidationError("这个文件没有音轨，无法提取音频。")
        return {"duration": round(duration, 3), "streams": streams,
                "container": info.get("format", {}).get("format_name", "")}

    def add_file(self, path, name=None, managed=False, identifier=None):
        path = Path(path).resolve()
        info = self.probe(path)
        identifier = identifier or uuid.uuid4().hex
        item = {"id": identifier, "name": safe_name(name or path.name), "path": str(path),
                "managed": managed, "size": path.stat().st_size, "created_at": time.time(), **info}
        with self.lock:
            self.files[identifier] = item
            self.save()
        return self.public_file(item)

    @staticmethod
    def public_file(item):
        return {k: v for k, v in item.items() if k not in {"path", "managed"}}

    @staticmethod
    def public_job(job):
        return {k: v for k, v in job.items() if k not in {"output_path", "temp_path", "reserved_path", "sidecar_path", "plan"}}

    def bootstrap(self):
        with self.lock:
            return {"app_id": "audiodrop", "token": self.token, "engine": {"ready": bool(self.ffmpeg and self.ffprobe), "version": self.version},
                    "profiles": public_profiles(self.encoders, self.muxers), "settings": dict(self.settings),
                    "files": [self.public_file(f) for f in self.files.values()],
                    "jobs": [self.public_job(j) for j in self.jobs.values()]}

    def snapshot(self):
        with self.lock:
            return {"jobs": [self.public_job(j) for j in self.jobs.values()], "settings": dict(self.settings)}

    def create_jobs(self, items, settings):
        self.require_engine()
        settings = normalized_settings(settings)
        profiles = {p["id"]: p for p in public_profiles(self.encoders, self.muxers)}
        if settings["format"] != "copy" and not profiles[settings["format"]]["available"]:
            raise ValidationError("当前 FFmpeg 缺少此格式的编码器。")
        if not isinstance(items, list) or not 1 <= len(items) <= 500:
            raise ValidationError("请选择 1 到 500 个文件。")
        prepared = []
        with self.lock:
            # Validate the entire batch before adding any jobs.
            for item in items:
                if not isinstance(item, dict):
                    raise ValidationError("文件参数无效。")
                source = self.files.get(item.get("file_id"))
                if not source or not Path(source["path"]).is_file():
                    raise ValidationError("源文件已不存在，请重新添加。")
                default = next((s for s in source["streams"] if s["default"]), source["streams"][0])
                index = item.get("stream_index", default["index"])
                stream = next((s for s in source["streams"] if s["index"] == index), None)
                if stream is None:
                    raise ValidationError("所选音轨不存在。")
                identifier = uuid.uuid4().hex
                plan = build_plan(settings, stream)
                prepared.append({"id": identifier, "file_id": source["id"], "name": source["name"],
                                 "source_size": source["size"], "duration": source["duration"],
                                 "stream": stream, "settings": dict(settings), "plan": plan,
                                 "status": "queued", "progress": 0, "speed": "", "error": "",
                                 "mode": "copy" if plan["copy"] else "encode", "note": plan["note"],
                                 "output_name": "", "output_size": 0, "created_at": time.time(),
                                 "output_dir": self.settings["output_dir"]})
            for job in prepared:
                self.jobs[job["id"]] = job
            self.save()
            for job in prepared:
                self.work.put(job["id"])
            return [self.public_job(j) for j in prepared]

    def cancel(self, identifier):
        with self.lock:
            job = self.jobs.get(identifier)
            if not job:
                raise ValidationError("找不到此任务。")
            if job["status"] not in TERMINAL:
                job.update(status="cancelled", finished_at=time.time(), error="")
                process = self.processes.get(identifier)
                if process and process.poll() is None:
                    process.terminate()
                self.save()
            return self.public_job(job)

    def delete_file(self, identifier):
        with self.lock:
            if any(j["file_id"] == identifier for j in self.jobs.values()):
                raise ValidationError("此文件仍关联转换记录，请先清除对应记录。")
            item = self.files.pop(identifier, None)
            if item and item["managed"]:
                Path(item["path"]).unlink(missing_ok=True)
            self.save()

    def clear_finished(self):
        with self.lock:
            removed = [identifier for identifier, job in self.jobs.items() if job["status"] in TERMINAL]
            source_ids = {self.jobs[i]["file_id"] for i in removed}
            for identifier in removed:
                del self.jobs[identifier]
                (self.previews / f"{identifier}.mp3").unlink(missing_ok=True)
            for source_id in source_ids:
                if not any(j["file_id"] == source_id for j in self.jobs.values()):
                    source = self.files.pop(source_id, None)
                    if source and source["managed"]:
                        Path(source["path"]).unlink(missing_ok=True)
            self.save()
            return {"removed": removed}

    def worker_loop(self):
        while not self.stop_event.is_set():
            try:
                identifier = self.work.get(timeout=0.5)
            except queue.Empty:
                continue
            try:
                self.convert(identifier)
            except Exception as exc:
                with self.lock:
                    job = self.jobs.get(identifier)
                    if job and job["status"] != "cancelled":
                        job.update(status="failed", error=str(exc), finished_at=time.time())
                        self.save()
            finally:
                self.work.task_done()

    def reserve_output(self, job, extension):
        directory = Path(job["output_dir"])
        directory.mkdir(parents=True, exist_ok=True)
        stem = safe_name(Path(job["name"]).stem)[:140]
        with self.lock:
            for number in range(1, 100000):
                name = f"{stem}{'' if number == 1 else f' ({number})'}.{extension}"
                target = directory / name
                try:
                    with target.open("xb"):
                        pass
                    return target
                except FileExistsError:
                    continue
        raise ValidationError("输出目录内同名文件过多。")

    def execute_conversion(self, job, source, plan, temp):
        log_path = self.data_dir / f"{job['id']}.log"
        args = [self.ffmpeg, "-hide_banner", "-nostdin", "-y", "-loglevel", "warning",
                "-stats_period", "0.25", "-progress", "pipe:1", "-protocol_whitelist", "file,pipe",
                "-i", source["path"], "-map", f"0:{job['stream']['index']}", "-vn", "-sn", "-dn",
                "-map_metadata", "0", *plan["args"], "-f", plan["muxer"], str(temp)]
        try:
            with log_path.open("w", encoding="utf-8") as log:
                process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=log, text=True,
                                           encoding="utf-8", errors="replace", creationflags=NO_WINDOW)
                with self.lock:
                    self.processes[job["id"]] = process
                    if job["status"] == "cancelled":
                        process.terminate()
                for line in process.stdout:
                    key, _, value = line.strip().partition("=")
                    with self.lock:
                        if key == "out_time_us" and job["duration"] > 0:
                            try:
                                job["progress"] = min(99, max(0, round(int(value) / 1_000_000 / job["duration"] * 100, 1)))
                            except ValueError:
                                pass
                        elif key == "speed":
                            job["speed"] = value if value != "N/A" else ""
                process.stdout.close()
                code = process.wait()
            return code, log_path.read_text("utf-8", errors="replace")[-3000:]
        finally:
            with self.lock:
                self.processes.pop(job["id"], None)
            log_path.unlink(missing_ok=True)

    def convert(self, identifier):
        with self.lock:
            job = self.jobs.get(identifier)
            if not job or job["status"] != "queued":
                return
            source = self.files[job["file_id"]]
            job.update(status="processing", started_at=time.time())
            self.save()
        plan = job["plan"]
        target = self.reserve_output(job, plan["extension"])
        temp = target.parent / f".audio-{identifier}.{plan['extension']}"
        with self.lock:
            job.update(temp_path=str(temp), reserved_path=str(target))
            self.save()
        success = False
        try:
            code, error = self.execute_conversion(job, source, plan, temp)
            if code and plan["copy"] and job["status"] != "cancelled":
                if job["settings"]["format"] == "copy":
                    # Preserve packet data even when a specialised container rejects it.
                    target.unlink(missing_ok=True)
                    temp.unlink(missing_ok=True)
                    plan = {**plan, "extension": "mka", "muxer": "matroska", "args": ["-c:a", "copy"]}
                    target = self.reserve_output(job, "mka")
                    temp = target.parent / f".audio-{identifier}.mka"
                else:
                    plan = build_plan({**job["settings"], "prefer_copy": False}, job["stream"])
                with self.lock:
                    job.update(plan=plan, mode="copy" if plan["copy"] else "encode", temp_path=str(temp), reserved_path=str(target))
                    self.save()
                code, error = self.execute_conversion(job, source, plan, temp)
            with self.lock:
                if job["status"] == "cancelled":
                    return
                if code or not temp.is_file() or temp.stat().st_size == 0:
                    job.update(status="failed", error="转换失败。" + ("\n" + error.strip() if error else "请检查文件及参数。"), finished_at=time.time())
                    self.save()
                    return
                temp.replace(target)
                job.update(status="completed", progress=100, output_path=str(target), output_name=target.name,
                           output_size=target.stat().st_size, finished_at=time.time(), result_codec=plan["codec"],
                           result_sample_rate=plan["sample_rate"], result_channels=plan["channels"], note=plan["note"])
                if plan.get("raw"):
                    sidecar = target.with_name(target.name + ".json")
                    sidecar.write_text(json.dumps({"codec": plan["codec"], "format": plan["muxer"],
                                                   "sample_rate": plan["sample_rate"], "channels": plan["channels"],
                                                   "duration": job["duration"]}, ensure_ascii=False, indent=2), "utf-8")
                    job["sidecar_path"] = str(sidecar)
                success = True
                self.save()
        finally:
            temp.unlink(missing_ok=True)
            if not success:
                target.unlink(missing_ok=True)

    def result_path(self, identifier):
        with self.lock:
            job = self.jobs.get(identifier)
            if not job or job["status"] != "completed":
                raise ValidationError("文件尚未转换完成。")
            path = Path(job["output_path"])
            if not path.is_file():
                raise ValidationError("输出文件已被移动或删除。")
            return path, dict(job)

    def preview(self, identifier):
        target, job = self.result_path(identifier)
        codec = job.get("result_codec", "")
        if (target.suffix.lower() in {".mp3", ".flac"}
            or target.suffix.lower() in {".m4a", ".mp4", ".aac"} and codec == "aac"
            or target.suffix.lower() == ".wav" and codec in {"pcm_s16le", "pcm_s24le", "pcm_s32le", "pcm_f32le"}):
            return target
        cached = self.previews / f"{identifier}.mp3"
        with self.preview_lock:
            if cached.exists():
                return cached
            input_args = []
            if job["plan"].get("raw"):
                input_args = ["-f", job["plan"]["muxer"], "-ar", str(job["result_sample_rate"]), "-ac", str(job["result_channels"])]
            result = run_process([self.ffmpeg, "-v", "error", "-nostdin", "-y", "-protocol_whitelist", "file,pipe", *input_args,
                                  "-i", str(target), "-t", "60", "-c:a", "libmp3lame", "-b:a", "128k", "-ar", "44100", "-ac", "2", str(cached)], capture_output=True, timeout=120)
            if result.returncode:
                cached.unlink(missing_ok=True)
                raise ValidationError("该格式暂时无法试听，可下载后用音频播放器打开。")
        return cached

    def choose_files(self):
        with self.dialog_lock:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            try:
                paths = filedialog.askopenfilenames(parent=root, title="选择视频或音频文件", filetypes=[("视频和音频", "*.mp4 *.mkv *.avi *.mov *.flv *.wmv *.webm *.ts *.mpg *.mpeg *.vob *.rmvb *.mp3 *.wav *.flac *.m4a *.ogg *.aac"), ("所有文件", "*.*")])
            finally:
                root.destroy()
        files, errors = [], []
        for path in paths:
            try:
                files.append(self.add_file(path))
            except ValidationError as exc:
                errors.append({"name": Path(path).name, "error": str(exc)})
        return {"files": files, "errors": errors}

    def choose_output(self):
        with self.dialog_lock:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            try:
                directory = filedialog.askdirectory(parent=root, title="选择音频输出文件夹", initialdir=self.settings["output_dir"])
            finally:
                root.destroy()
        if directory:
            directory = Path(directory).resolve()
            with self.lock:
                self.settings["output_dir"] = str(directory)
                self.save()
        return dict(self.settings)

    def close(self):
        self.stop_event.set()
        with self.lock:
            active = [i for i, job in self.jobs.items() if job["status"] not in TERMINAL]
        for identifier in active:
            self.cancel(identifier)
        self.worker.join(timeout=5)


class Handler(BaseHTTPRequestHandler):
    server_version = "AudioDrop/1.0"
    protocol_version = "HTTP/1.1"

    def handle(self):
        try:
            super().handle()
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            # Browsers routinely close keep-alive sockets while navigating.
            self.close_connection = True

    @property
    def app(self):
        return self.server.app

    def log_message(self, fmt, *args):
        if len(args) >= 2 and str(args[1]).startswith(("4", "5")):
            print(f"[{time.strftime('%H:%M:%S')}] {fmt % args}", flush=True)

    def secure_request(self, mutation=False):
        host = self.headers.get("Host", "")
        allowed = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
        if host not in allowed:
            raise PermissionError("只接受本机访问。")
        origin = self.headers.get("Origin")
        if origin and origin not in {f"http://{h}" for h in allowed}:
            raise PermissionError("拒绝跨站请求。")
        if self.headers.get("Sec-Fetch-Site") == "cross-site":
            raise PermissionError("拒绝跨站请求。")
        if mutation and not secrets.compare_digest(self.headers.get("X-App-Token", ""), self.app.token):
            raise PermissionError("会话已过期，请刷新页面。")

    def headers_for(self, status, content_type, length=None):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "same-origin")
        self.send_header("Cache-Control", "no-store")
        if length is not None:
            self.send_header("Content-Length", str(length))

    def json_response(self, data, status=200):
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.headers_for(status, "application/json; charset=utf-8", len(payload))
        self.end_headers()
        self.wfile.write(payload)

    def body(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
        except ValueError:
            raise ValidationError("请求长度无效。") from None
        if length < 0 or length > 1024 ** 2:
            raise ValidationError("请求过大。")
        try:
            return json.loads(self.rfile.read(length) or b"{}")
        except ValueError:
            raise ValidationError("JSON 格式无效。") from None

    def file_response(self, path, attachment=False, force_type=None):
        size = path.stat().st_size
        start, end, partial = 0, max(0, size - 1), False
        range_header = self.headers.get("Range", "")
        if range_header:
            match = re.fullmatch(r"bytes=(\d*)-(\d*)", range_header)
            if not match or not size:
                self.headers_for(416, "application/octet-stream", 0)
                self.send_header("Content-Range", f"bytes */{size}")
                self.end_headers()
                return
            left, right = match.groups()
            if not left and not right:
                self.json_response({"error": "无效的 Range。"}, 416)
                return
            if left:
                start = int(left)
                end = min(end, int(right)) if right else end
            else:
                start = max(0, size - int(right))
            if start >= size or start > end:
                self.headers_for(416, "application/octet-stream", 0)
                self.send_header("Content-Range", f"bytes */{size}")
                self.end_headers()
                return
            partial = True
        mime = force_type or mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        count = end - start + 1 if size else 0
        self.headers_for(206 if partial else 200, mime, count)
        self.send_header("Accept-Ranges", "bytes")
        if partial:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        if attachment:
            self.send_header("Content-Disposition", f"attachment; filename=audio{path.suffix}; filename*=UTF-8''{quote(path.name)}")
        if path.suffix in {".html", ".js", ".css"}:
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; media-src 'self' blob:; connect-src 'self'; frame-ancestors 'none'; object-src 'none'; base-uri 'self'")
        self.end_headers()
        with path.open("rb") as source:
            source.seek(start)
            while count:
                chunk = source.read(min(count, 1024 ** 2))
                if not chunk:
                    break
                self.wfile.write(chunk)
                count -= len(chunk)

    def handle_error(self, exc):
        self.close_connection = True
        status = 403 if isinstance(exc, PermissionError) else 400 if isinstance(exc, (ValidationError, ValueError, KeyError)) else 500
        try:
            self.json_response({"error": str(exc) if status < 500 else "操作失败：" + str(exc)}, status)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass

    def do_GET(self):
        try:
            self.secure_request()
            parsed = urlparse(self.path)
            path = parsed.path
            if path == "/api/bootstrap":
                return self.json_response(self.app.bootstrap())
            if path == "/api/jobs":
                return self.json_response(self.app.snapshot())
            if path == "/api/download-all":
                ids = parse_qs(parsed.query).get("ids", [""])[0].split(",")
                if not ids or len(ids) > 500:
                    raise ValidationError("下载任务无效。")
                results = [self.app.result_path(identifier) for identifier in ids]
                archive_path = self.app.data_dir / f"声迹音频-{uuid.uuid4().hex[:8]}.zip"
                try:
                    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_STORED, allowZip64=True) as archive:
                        seen = collections.Counter()
                        for result, job in results:
                            seen[result.name] += 1
                            arcname = result.name if seen[result.name] == 1 else f"{result.stem} ({seen[result.name]}){result.suffix}"
                            archive.write(result, arcname)
                            if job.get("sidecar_path") and Path(job["sidecar_path"]).exists():
                                archive.write(job["sidecar_path"], arcname + ".json")
                    return self.file_response(archive_path, attachment=True)
                finally:
                    archive_path.unlink(missing_ok=True)
            match = re.fullmatch(r"/api/jobs/([a-f0-9]{32})/(download|preview|metadata)", path)
            if match:
                identifier, action = match.groups()
                if action == "preview":
                    return self.file_response(self.app.preview(identifier))
                target, job = self.app.result_path(identifier)
                if action == "metadata":
                    if not job.get("sidecar_path"):
                        raise ValidationError("此格式不需要参数说明。")
                    target = Path(job["sidecar_path"])
                return self.file_response(target, attachment=True)
            if path == "/favicon.ico":
                self.headers_for(204, "image/x-icon", 0)
                self.end_headers()
                return
            target = (STATIC / ("index.html" if path == "/" else unquote(path).lstrip("/"))).resolve()
            if not target.is_relative_to(STATIC) or not target.is_file():
                return self.json_response({"error": "页面不存在。"}, 404)
            return self.file_response(target)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass
        except Exception as exc:
            self.handle_error(exc)

    def do_POST(self):
        try:
            self.secure_request(mutation=True)
            parsed = urlparse(self.path)
            if parsed.path == "/api/files":
                self.app.require_engine()
                try:
                    length = int(self.headers.get("Content-Length", 0))
                except ValueError:
                    raise ValidationError("文件大小无效。") from None
                if not 0 < length <= MAX_UPLOAD:
                    raise ValidationError("文件为空，或超过 100 GB。")
                if shutil.disk_usage(self.app.uploads).free < length + 100 * 1024 ** 2:
                    raise ValidationError("本机剩余空间不足，请使用“直接选取本机文件”，避免复制源文件。")
                name = safe_name(parse_qs(parsed.query).get("name", ["video"])[0])
                identifier = uuid.uuid4().hex
                target = self.app.uploads / f"{identifier}{Path(name).suffix[:12]}"
                partial = self.app.uploads / f"{identifier}.part"
                try:
                    remaining = length
                    self.connection.settimeout(120)
                    with partial.open("wb") as file:
                        while remaining:
                            chunk = self.rfile.read(min(remaining, 1024 ** 2))
                            if not chunk:
                                raise ValidationError("文件读取已中断。")
                            file.write(chunk)
                            remaining -= len(chunk)
                    partial.replace(target)
                    item = self.app.add_file(target, name=name, managed=True, identifier=identifier)
                    return self.json_response(item, 201)
                except Exception:
                    target.unlink(missing_ok=True)
                    raise
                finally:
                    partial.unlink(missing_ok=True)
            data = self.body()
            if not isinstance(data, dict):
                raise ValidationError("请求必须是 JSON 对象。")
            if parsed.path == "/api/jobs":
                return self.json_response({"jobs": self.app.create_jobs(data.get("files"), data.get("settings", {}))}, 201)
            if parsed.path == "/api/pick-files":
                return self.json_response(self.app.choose_files())
            if parsed.path == "/api/pick-output":
                return self.json_response(self.app.choose_output())
            if parsed.path == "/api/open-folder":
                if data.get("job_id"):
                    target, _ = self.app.result_path(data["job_id"])
                    directory = target.parent
                else:
                    directory = Path(self.app.settings["output_dir"])
                    directory.mkdir(parents=True, exist_ok=True)
                if os.name == "nt":
                    os.startfile(str(directory))
                else:
                    subprocess.Popen(["open" if os.sys.platform == "darwin" else "xdg-open", str(directory)])
                return self.json_response({"ok": True})
            if parsed.path == "/api/clear-finished":
                return self.json_response(self.app.clear_finished())
            if parsed.path == "/api/shutdown":
                self.json_response({"ok": True})
                threading.Thread(target=self.server.shutdown, daemon=True).start()
                return
            match = re.fullmatch(r"/api/jobs/([a-f0-9]{32})/cancel", parsed.path)
            if match:
                return self.json_response(self.app.cancel(match.group(1)))
            return self.json_response({"error": "接口不存在。"}, 404)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            self.close_connection = True
        except Exception as exc:
            self.handle_error(exc)

    def do_DELETE(self):
        try:
            self.secure_request(mutation=True)
            match = re.fullmatch(r"/api/files/([a-f0-9]{32})", urlparse(self.path).path)
            if not match:
                return self.json_response({"error": "接口不存在。"}, 404)
            self.app.delete_file(match.group(1))
            return self.json_response({"ok": True})
        except Exception as exc:
            self.handle_error(exc)


def make_server(app, port=8765):
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.daemon_threads = True
    server.app = app
    return server


def main():
    parser = argparse.ArgumentParser(description="声迹 — 本机视频转音频")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--data-dir")
    parser.add_argument("--output-dir")
    args = parser.parse_args()
    app = Application(args.data_dir, args.output_dir)
    server = None
    for port in range(args.port, args.port + 20):
        try:
            server = make_server(app, port)
            break
        except OSError:
            continue
    if server is None:
        app.close()
        raise SystemExit("端口被占用，请使用 --port 指定其他端口。")
    url = f"http://127.0.0.1:{server.server_port}"
    instance_path = app.data_dir / "server.json"
    instance_path.write_text(json.dumps({"pid": os.getpid(), "url": url}), "utf-8")
    print(f"声迹 AudioDrop\nLocal: {url}\nOutput: {app.settings['output_dir']}\nEngine: {app.version or '未找到 FFmpeg'}\n按 Ctrl+C 停止服务。", flush=True)
    if not args.no_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever(poll_interval=0.3)
    except KeyboardInterrupt:
        pass
    finally:
        app.close()
        server.server_close()
        instance_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
