"""Moo0-compatible audio profiles and strictly validated FFmpeg arguments."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

AAC_RATES = (8000, 11025, 12000, 16000, 22050, 24000, 32000, 44100, 48000, 88200, 96000)


@dataclass(frozen=True)
class Profile:
    id: str
    label: str
    extension: str
    muxer: str
    encoder: str
    group: str
    lossless: bool = False
    bit_depths: tuple[str, ...] = ()
    rates: tuple[int, ...] = ()
    max_channels: int = 2
    bitrate: int = 0
    fixed_rate: int = 0
    fixed_channels: int = 0
    note: str = ""


PROFILES = [
    Profile("3gp", "3GP · AMR", "3gp", "3gp", "libopencore_amrnb", "legacy", fixed_rate=8000, fixed_channels=1, bitrate=12, note="AMR-NB：8 kHz、单声道、12.2 kbps"),
    Profile("3gp_aac", "3GP · AAC", "3gp", "3gp", "aac", "legacy", bitrate=192, rates=AAC_RATES),
    Profile("3g2", "3G2 · AMR", "3g2", "3g2", "libopencore_amrnb", "legacy", fixed_rate=8000, fixed_channels=1, bitrate=12, note="AMR-NB：8 kHz、单声道、12.2 kbps"),
    Profile("3g2_aac", "3G2 · AAC", "3g2", "3g2", "aac", "legacy", bitrate=192, rates=AAC_RATES),
    Profile("aac", "AAC", "aac", "adts", "aac", "common", bitrate=192, rates=AAC_RATES),
    Profile("ac3", "AC3", "ac3", "ac3", "ac3", "legacy", bitrate=192, rates=(32000, 44100, 48000), max_channels=6),
    Profile("aiff", "AIFF", "aiff", "aiff", "pcm_s16be", "lossless", True, ("16", "24", "32"), max_channels=8),
    Profile("amr", "AMR", "amr", "amr", "libopencore_amrnb", "legacy", fixed_rate=8000, fixed_channels=1, bitrate=12, note="AMR-NB：8 kHz、单声道、12.2 kbps"),
    Profile("au", "AU · PCM", "au", "au", "pcm_s16be", "legacy", True, ("16", "24", "32"), max_channels=8),
    Profile("au_alaw", "AU · A-law", "au", "au", "pcm_alaw", "legacy"),
    Profile("au_mulaw", "AU · μ-law", "au", "au", "pcm_mulaw", "legacy"),
    Profile("flac", "FLAC", "flac", "flac", "flac", "lossless", True, ("16", "24"), max_channels=8),
    Profile("m4a", "M4A · AAC", "m4a", "ipod", "aac", "common", bitrate=192, rates=AAC_RATES),
    Profile("m4a_alac", "M4A · Apple Lossless", "m4a", "ipod", "alac", "lossless", True, ("16", "24"), max_channels=8),
    Profile("mmf", "MMF · Yamaha SMAF", "mmf", "mmf", "adpcm_yamaha", "legacy", rates=(4000, 8000, 11025, 22050, 44100), fixed_channels=1, note="SMAF 铃声格式，输出为单声道"),
    Profile("mov", "MOV · AAC", "mov", "mov", "aac", "legacy", bitrate=192, rates=AAC_RATES),
    Profile("mp2", "MP2", "mp2", "mp2", "mp2", "legacy", bitrate=192, rates=(16000, 22050, 24000, 32000, 44100, 48000)),
    Profile("mp3", "MP3", "mp3", "mp3", "libmp3lame", "common", bitrate=192, rates=(8000, 11025, 12000, 16000, 22050, 24000, 32000, 44100, 48000)),
    Profile("mp4", "MP4 · AAC 音频", "mp4", "mp4", "aac", "legacy", bitrate=192, rates=AAC_RATES),
    Profile("ogg", "OGG · Vorbis", "ogg", "ogg", "libvorbis", "common", bitrate=192),
    Profile("ogg_flac", "OGG · FLAC", "ogg", "ogg", "flac", "lossless", True, ("16", "24"), max_channels=8),
    Profile("ra", "RA · RealAudio", "ra", "rm", "real_144", "legacy", fixed_rate=8000, fixed_channels=1, note="RealAudio 1.0：8 kHz、单声道、14.4 kbps"),
    Profile("rm", "RM · RealAudio", "rm", "rm", "real_144", "legacy", fixed_rate=8000, fixed_channels=1, note="RealAudio 1.0：8 kHz、单声道、14.4 kbps"),
    Profile("wav", "WAV · PCM", "wav", "wav", "pcm_s16le", "lossless", True, ("16", "24", "32", "32f"), max_channels=8),
    Profile("wav_ima", "WAV · ADPCM IMA", "wav", "wav", "adpcm_ima_wav", "legacy"),
    Profile("wav_ms", "WAV · ADPCM Microsoft", "wav", "wav", "adpcm_ms", "legacy"),
    Profile("wav_yamaha", "WAV · ADPCM Yamaha", "wav", "wav", "adpcm_yamaha", "legacy"),
    Profile("wav_gsm", "WAV · GSM", "wav", "wav", "libgsm_ms", "legacy", fixed_rate=8000, fixed_channels=1, note="GSM：8 kHz、单声道"),
    Profile("wma", "WMA", "wma", "asf", "wmav2", "legacy", bitrate=192, rates=(22050, 32000, 44100, 48000)),
    Profile("pcm_le", "PCM · Little-Endian", "pcm", "s16le", "pcm_s16le", "legacy", True, ("16", "24", "32", "32f"), max_channels=8, note="原始音频无文件头；同时生成参数说明 JSON"),
    Profile("pcm_be", "PCM · Big-Endian", "pcm", "s16be", "pcm_s16be", "legacy", True, ("16", "24", "32", "32f"), max_channels=8, note="原始音频无文件头；同时生成参数说明 JSON"),
    Profile("pcm_alaw", "PCM · A-law", "alaw", "alaw", "pcm_alaw", "legacy", note="原始音频无文件头；同时生成参数说明 JSON"),
    Profile("pcm_mulaw", "PCM · μ-law", "mulaw", "mulaw", "pcm_mulaw", "legacy", note="原始音频无文件头；同时生成参数说明 JSON"),
]
PROFILE_MAP = {p.id: p for p in PROFILES}
RATES = (4000, 8000, 11025, 12000, 16000, 22050, 24000, 32000, 44100, 48000, 88200, 96000, 176400, 192000)
BITRATES = (32, 48, 64, 96, 128, 160, 192, 224, 256, 320)


class ValidationError(ValueError):
    pass


def normalized_settings(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValidationError("转换参数必须是 JSON 对象。")
    profile_id = str(data.get("format", "wav"))
    if profile_id != "copy" and profile_id not in PROFILE_MAP:
        raise ValidationError("不支持这个输出格式。")
    try:
        rate = int(data.get("sample_rate", 0))
        channels = int(data.get("channels", 0))
        bitrate = int(data.get("bitrate", 192))
        volume = float(data.get("volume", 100))
    except (TypeError, ValueError):
        raise ValidationError("音频参数不是有效数字。") from None
    depth = str(data.get("bit_depth", "16"))
    if rate not in (0, *RATES) or channels not in (0, 1, 2, 6, 8):
        raise ValidationError("采样率或声道数无效。")
    if depth not in ("16", "24", "32", "32f") or bitrate not in BITRATES:
        raise ValidationError("位深或码率无效。")
    if not 0 <= volume <= 300 or volume != volume:
        raise ValidationError("音量必须在 0% 到 300% 之间。")
    if profile_id == "copy":
        # Copying cannot silently alter audio parameters.
        if rate or channels or volume != 100:
            raise ValidationError("无损复制需要保持原采样率、原声道和 100% 音量。")
    else:
        p = PROFILE_MAP[profile_id]
        if p.fixed_rate and rate not in (0, p.fixed_rate):
            raise ValidationError(f"{p.label} 只支持 {p.fixed_rate} Hz。")
        if p.rates and rate and rate not in p.rates:
            raise ValidationError(f"{p.label} 不支持这个采样率。")
        if p.fixed_channels and channels not in (0, p.fixed_channels):
            raise ValidationError(f"{p.label} 只支持单声道。")
        if channels > p.max_channels:
            raise ValidationError(f"{p.label} 最多支持 {p.max_channels} 个声道。")
        if p.bit_depths and depth not in p.bit_depths:
            raise ValidationError(f"{p.label} 不支持这个位深。")
    return {"format": profile_id, "sample_rate": rate, "channels": channels,
            "bit_depth": depth, "bitrate": bitrate, "volume": volume,
            "prefer_copy": bool(data.get("prefer_copy", True))}


def copy_target(codec: str) -> tuple[str, str]:
    targets = {
        "aac": ("m4a", "ipod"), "alac": ("m4a", "ipod"),
        "mp3": ("mp3", "mp3"), "mp2": ("mp2", "mp2"),
        "flac": ("flac", "flac"), "vorbis": ("ogg", "ogg"),
        "opus": ("opus", "opus"), "ac3": ("ac3", "ac3"),
        "eac3": ("eac3", "eac3"), "wmav1": ("wma", "asf"), "wmav2": ("wma", "asf"),
        "amr_nb": ("amr", "amr"), "amr_wb": ("amr", "amr"),
    }
    if codec.startswith("pcm_") or codec in {"adpcm_ima_wav", "adpcm_ms", "adpcm_yamaha", "gsm_ms"}:
        return "wav", "wav"
    # Matroska carries many codecs that have no dedicated audio-only container.
    return targets.get(codec, ("mka", "matroska"))


def build_plan(settings: dict[str, Any], stream: dict[str, Any]) -> dict[str, Any]:
    s = normalized_settings(settings)
    source_codec = stream["codec"]
    source_rate = int(stream.get("sample_rate") or 48000)
    source_channels = int(stream.get("channels") or 2)
    if s["format"] == "copy":
        extension, muxer = copy_target(source_codec)
        return {"extension": extension, "muxer": muxer, "codec": source_codec,
                "args": ["-c:a", "copy"], "copy": True,
                "sample_rate": source_rate, "channels": source_channels, "note": "原音轨无损复制"}

    p = PROFILE_MAP[s["format"]]
    rate = s["sample_rate"] or p.fixed_rate or source_rate
    if p.rates and rate not in p.rates:
        rate = min(p.rates, key=lambda candidate: abs(candidate - rate))
    if p.encoder == "aac" and rate > 96000:
        rate = 96000
    channels = s["channels"] or p.fixed_channels or min(source_channels, p.max_channels)
    codec, muxer = p.encoder, p.muxer
    depth = s["bit_depth"]
    if p.id in ("wav", "aiff", "au", "pcm_le", "pcm_be"):
        endian = "be" if p.id in ("aiff", "au", "pcm_be") else "le"
        sample_fmt = "f32" if depth == "32f" else f"s{depth}"
        codec = f"pcm_{sample_fmt}{endian}"
        if p.id.startswith("pcm_"):
            muxer = f"{sample_fmt}{endian}"
    expected_codec = {"libmp3lame": "mp3", "libvorbis": "vorbis", "libgsm_ms": "gsm_ms",
                      "libopencore_amrnb": "amr_nb", "real_144": "ra_144"}.get(codec, codec)
    can_copy = (s["prefer_copy"] and p.id not in {"pcm_le", "pcm_be", "pcm_alaw", "pcm_mulaw"}
                and source_codec == expected_codec and not s["sample_rate"]
                and not s["channels"] and s["volume"] == 100
                and rate == source_rate and channels == source_channels
                and (not p.bitrate or int(stream.get("bitrate", 0)) == s["bitrate"] * 1000)
                and (not p.bit_depths or depth == str(stream.get("bit_depth", ""))))
    args = ["-c:a", "copy"] if can_copy else ["-c:a", codec, "-ar", str(rate), "-ac", str(channels)]
    if not can_copy:
        if p.encoder == "libopencore_amrnb":
            args += ["-b:a", "12.2k"]
        elif p.bitrate:
            bitrate = s["bitrate"]
            # MPEG Layer III at < 32 kHz has a lower allowed bitrate ceiling.
            if p.id == "mp3" and rate < 32000:
                bitrate = min(bitrate, 160 if rate >= 16000 else 64)
            if p.id == "mp2" and rate < 32000:
                bitrate = min(bitrate, 160)
            args += ["-b:a", f"{bitrate}k"]
        if p.encoder in {"flac", "alac"}:
            sample_format = "s16" if depth == "16" else "s32"
            if p.encoder == "alac":
                sample_format += "p"
            args += ["-sample_fmt", sample_format]
            if p.encoder == "flac" and depth == "24":
                args += ["-bits_per_raw_sample", "24"]
        if s["volume"] != 100:
            args += ["-af", f"volume={s['volume'] / 100:.6f}"]
    if muxer == "wav":
        args += ["-rf64", "auto"]
    if muxer in {"ipod", "mp4", "mov", "3gp", "3g2"}:
        args += ["-movflags", "+faststart"]
    notes = [p.note] if p.note else []
    if rate != source_rate and not s["sample_rate"]:
        notes.append(f"格式要求：采样率自动适配为 {rate} Hz")
    if channels != source_channels and not s["channels"]:
        notes.append(f"格式要求：声道自动适配为 {channels}")
    return {"extension": p.extension, "muxer": muxer, "codec": expected_codec,
            "args": args, "copy": can_copy, "sample_rate": rate, "channels": channels,
            "note": "；".join(notes), "raw": p.id.startswith("pcm_")}


def public_profiles(encoders: set[str], muxers: set[str]) -> list[dict[str, Any]]:
    result = []
    for p in PROFILES:
        entry = asdict(p)
        entry["available"] = p.encoder in encoders and p.muxer in muxers
        entry["rates"] = [p.fixed_rate] if p.fixed_rate else list(p.rates or RATES)
        entry["channel_options"] = ([p.fixed_channels] if p.fixed_channels
                                    else [c for c in (1, 2, 6, 8) if c <= p.max_channels])
        result.append(entry)
    return result
