"use strict";

const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const words = {
  zh: {
    brand:"声迹",workspace:"工作空间",workbench:"转换工作台",history:"转换记录",help:"使用帮助",localTitle:"你的文件，留在本机",localBody:"转换在这台电脑上完成，无需上传到云端。",localMode:"本地运行模式",connecting:"正在连接引擎",engineReady:"转换引擎已就绪",engineMissing:"转换引擎不可用",pageTitle:"让视频里的声音，独立出来。",pageSubtitle:"拖入视频，选择格式。剩下的交给声迹。",outputFolder:"输出文件夹",dropTitle:"把视频拖到这里",dropSubtitle:"支持多个文件，也可以直接添加整个文件夹",chooseFiles:"选择文件",chooseDirectory:"添加文件夹",moreFormats:"及更多格式",nativePick:"大文件？直接选取本机文件，免复制",queue:"转换队列",cancelAll:"取消剩余",clearFinished:"清除已结束",emptyTitle:"等待你的第一个文件",emptyBody:"添加视频后，音轨信息和转换进度会显示在这里。",queueEmpty:"还没有添加文件",downloadAll:"打包下载",privacyLine:"本机处理 · 保留原文件 · 支持视频与音频输入",settings:"输出设置",reset:"重置",outputFormat:"输出格式",originalAudio:"原始音轨",lossless:"无损格式",lossy:"有损压缩",directCopy:"直接复制",wavDescription:"未压缩音频，适合剪辑和后期制作。",sampleRate:"采样率",keepOriginal:"保持原始",channels:"声道",bitDepth:"位深",bitrate:"码率",fixedQuality:"格式固定",volume:"音量",originalVolume:"原始音量 100%",preferCopy:"参数一致时优先无损复制",copyTitle:"保留原始音质",copyBody:"直接提取音轨，不重新编码。输出扩展名根据原音频编码自动选择。",copyNote:"采样率、声道和音量保持原始。",saveTo:"保存到",change:"更改",autoStart:"添加后自动转换",noFiles:"未添加文件",start:"开始转换",duplicateNote:"同名文件自动编号，已有音频不会被覆盖。",historyDescription:"已结束的转换会保存在这里，关闭浏览器后也能找回。",help1Title:"添加文件，选择格式",help1Body:"将一个或多个视频拖入工作台，或点击“选择文件”。文件夹会批量读取其中的媒体文件。大文件建议使用“直接选取本机文件”，不产生源文件副本。",help2Title:"无损格式与无损复制",help2Body:"WAV、FLAC 等格式保存解码后的声音。“原始音轨”直接复制原编码数据，避免再次压缩。将有损音轨转换为 WAV 不会恢复已经丢失的信息。",help3Title:"批量转换，随时取消",help3Body:"选择采样率、声道、位深或码率与音量后点击“开始转换”。队列依次处理，可单独取消或重试。有多个音轨时，可以在文件行中选择语言或轨道。",help4Title:"试听与输出文件",help4Body:"音频直接保存到输出文件夹，也可下载或打包下载。旧式格式会生成最多 60 秒的试听版本。原始 PCM 同时生成 JSON 参数说明，帮助其他软件正确读取。",aboutTitle:"声迹 AudioDrop",aboutBody:"以 Moo0 的音频提取功能为参考打造的独立本机应用。33 种输出格式，加上自动无损提取；使用 FFmpeg 完成实际转换。",miniHelp:"Chrome / Edge 可使用右上角的迷你悬浮窗；其他浏览器会切换到紧凑视图。",preview:"音频试听",footer:"只留下声音，保留每一个细节。",connectionLost:"无法连接本机服务，请保持启动窗口运行。正在尝试重新连接…",mono:"单声道",stereo:"立体声",surround6:"5.1 声道",surround8:"7.1 声道",ready:"待转换",uploading:"正在读取",probing:"分析音轨",queued:"排队中",processing:"转换中",completed:"已完成",failed:"转换失败",cancelled:"已取消",download:"下载音频",play:"试听",cancel:"取消",remove:"移除",retry:"重试",again:"再次转换",metadata:"下载 PCM 参数",track:"音轨",defaultTrack:"默认",filesUnit:"个文件",pending:"待转换",finished:"已完成",total:"共",working:"处理中",noHistory:"还没有转换记录",noHistoryBody:"完成第一次转换后，音频会出现在这里。",copied:"无损复制",encoded:"重新编码",unavailable:"当前引擎不支持",commonGroup:"常用格式",losslessGroup:"无损格式",legacyGroup:"更多与旧式格式",copyOption:"无损复制 · 自动格式",mp3Description:"兼容性广、体积小，适合日常收听。",flacDescription:"无损压缩，比 WAV 更节省空间。",m4aDescription:"高效压缩音频，适合手机与日常播放。",alacDescription:"Apple 无损音频，适合苹果设备与音频归档。",genericDescription:"提取所选音轨，保存为指定音频格式。",pcmDescription:"原始音频无文件头，同时生成 JSON 参数说明。",filesAdded:"文件已加入队列",batchStarted:"已开始批量转换",noEngine:"请安装 FFmpeg 或检查 bin 文件夹后重新启动。",selectingNative:"本机选取窗口已打开，请选择文件。",selectingOutput:"文件夹选取窗口已打开。",recordsCleared:"已清除记录和临时源文件，输出音频仍保留。",noResults:"还没有可下载的音频。",previewError:"无法播放此格式，请下载后打开。",skipped:"已跳过文件夹中的非媒体文件",duplicateSkipped:"已跳过重复添加的文件",miniTitle:"声迹 · 迷你窗口",backToApp:"返回工作台",miniIdle:"等待转换任务",miniProgress:"批量转换进度",miniUnsupported:"已切换到紧凑视图。悬浮窗需要 Chrome / Edge 支持。",conversionComplete:"转换完成",seconds:"秒",formatCount:"种输出格式",readFailed:"文件读取失败",browserOnly:"当前浏览器不支持文件夹选取，请使用直接选取本机文件。"
  },
  en: {
    brand:"AudioDrop",workspace:"Workspace",workbench:"Converter",history:"History",help:"Help",localTitle:"Your files stay here",localBody:"Conversion happens on this computer. No cloud uploads.",localMode:"LOCAL MODE",connecting:"Connecting to engine",engineReady:"Engine ready",engineMissing:"Engine unavailable",pageTitle:"Give your video's sound a life of its own.",pageSubtitle:"Drop a video. Choose a format. Let AudioDrop do the rest.",outputFolder:"Output folder",dropTitle:"Drop your videos here",dropSubtitle:"Add multiple files, or select an entire folder",chooseFiles:"Choose files",chooseDirectory:"Add folder",moreFormats:"and more",nativePick:"Large files? Select locally, without making copies",queue:"Conversion queue",cancelAll:"Cancel remaining",clearFinished:"Clear finished",emptyTitle:"Ready for your first file",emptyBody:"Add a video to see its audio tracks and conversion progress.",queueEmpty:"No files added yet",downloadAll:"Download ZIP",privacyLine:"Local processing · Originals preserved · Video & audio input",settings:"Output settings",reset:"Reset",outputFormat:"Output format",originalAudio:"Original",lossless:"Lossless",lossy:"Lossy",directCopy:"Stream copy",wavDescription:"Uncompressed audio, ideal for editing and production.",sampleRate:"Sample rate",keepOriginal:"Keep original",channels:"Channels",bitDepth:"Bit depth",bitrate:"Bitrate",fixedQuality:"Fixed by format",volume:"Volume",originalVolume:"Original: 100%",preferCopy:"Copy when all parameters match",copyTitle:"Keep the original quality",copyBody:"Extract the audio stream without re-encoding. The file extension is selected automatically.",copyNote:"Sample rate, channels and volume stay unchanged.",saveTo:"Save to",change:"Change",autoStart:"Convert files as they are added",noFiles:"No files added",start:"Start conversion",duplicateNote:"Existing files are preserved; duplicate names get a number.",historyDescription:"Finished conversions are saved here, even after you close the browser.",help1Title:"Add files. Choose a format.",help1Body:"Drop one or more videos into the workspace, or choose files. Add folder reads its media files in a batch. For large files, select them directly on this computer to avoid copying the source.",help2Title:"Lossless format vs. stream copy",help2Body:"WAV and FLAC store decoded audio. Original extracts the encoded stream directly, avoiding another compression step. Converting a lossy track to WAV cannot restore lost information.",help3Title:"Batch processing, with control",help3Body:"Set sample rate, channels, bit depth or bitrate, and volume, then start. Files are processed in order and can be cancelled or retried. For multiple tracks, select a language or track in the file row.",help4Title:"Listen and save",help4Body:"Audio is saved directly to your output folder. Download files individually or as a ZIP. Legacy formats get a preview of up to 60 seconds. Raw PCM includes a JSON file with the parameters needed for playback.",aboutTitle:"AudioDrop",aboutBody:"An independent local application inspired by Moo0 audio extraction. 33 output profiles plus automatic stream copy, powered by FFmpeg.",miniHelp:"Chrome / Edge support the floating mini window. Other browsers use a compact layout.",preview:"Audio preview",footer:"Keep the sound. Preserve every detail.",connectionLost:"Cannot reach the local service. Keep the launcher running. Reconnecting…",mono:"Mono",stereo:"Stereo",surround6:"5.1 channels",surround8:"7.1 channels",ready:"Ready",uploading:"Reading",probing:"Analyzing audio",queued:"Queued",processing:"Converting",completed:"Done",failed:"Failed",cancelled:"Cancelled",download:"Download audio",play:"Listen",cancel:"Cancel",remove:"Remove",retry:"Retry",again:"Convert again",metadata:"Download PCM metadata",track:"Track",defaultTrack:"Default",filesUnit:"files",pending:"ready",finished:"done",total:"Total",working:"processing",noHistory:"No conversions yet",noHistoryBody:"Your finished audio will appear here after your first conversion.",copied:"Stream copy",encoded:"Re-encoded",unavailable:"Unavailable in this engine",commonGroup:"Popular formats",losslessGroup:"Lossless formats",legacyGroup:"More & legacy formats",copyOption:"Lossless copy · Automatic format",mp3Description:"Widely compatible and compact, great for everyday listening.",flacDescription:"Lossless compression, with smaller files than WAV.",m4aDescription:"Efficient audio compression for phones and everyday playback.",alacDescription:"Apple Lossless audio for Apple devices and archiving.",genericDescription:"Extract the selected track into this audio format.",pcmDescription:"Headerless audio. A JSON file with playback parameters is included.",filesAdded:"Files added to the queue",batchStarted:"Batch conversion started",noEngine:"Install FFmpeg or check the bin folder, then restart.",selectingNative:"The local file picker is open. Choose your files.",selectingOutput:"The folder picker is open.",recordsCleared:"History and temporary sources cleared. Output audio is preserved.",noResults:"No converted audio to download yet.",previewError:"Cannot play this format here. Download it to open in a player.",skipped:"Non-media files in the folder were skipped",duplicateSkipped:"Duplicate files were skipped",miniTitle:"AudioDrop · Mini window",backToApp:"Back to workspace",miniIdle:"Waiting for files",miniProgress:"Batch conversion progress",miniUnsupported:"Compact layout enabled. A floating window requires Chrome / Edge.",conversionComplete:"Conversion complete",seconds:"s",formatCount:"output formats",readFailed:"Could not read this file",browserOnly:"Folder selection is not supported. Use the local file picker."
  }
};

function stored(key, fallback) { try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch { return fallback; } }
function remember(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); } catch {} }
let language = stored("audiodrop.language", "zh") === "en" ? "en" : "zh";
const t = key => words[language][key] || words.zh[key] || key;
const defaultSettings = {format:"wav", sample_rate:0, channels:0, bit_depth:"16", bitrate:192, volume:100, prefer_copy:true};
let settings = {...defaultSettings, ...stored("audiodrop.settings", {})};
let batchTail = Promise.resolve();
const state = {token:"", engine:{ready:false}, profiles:[], files:[], jobs:[], output:"", view:"workspace", uploads:new Map(), tracks:new Map(), seen:new Set(), submitting:false, connected:false, mini:null};

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}
function icon(name) {
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("class", "icon"); svg.setAttribute("aria-hidden", "true");
  const use = document.createElementNS(svg.namespaceURI, "use");
  use.setAttribute("href", `#i-${name}`); svg.append(use); return svg;
}
function iconButton(name, label, action) {
  const button = element("button", "icon-button");
  button.type = "button"; button.title = label; button.setAttribute("aria-label", label); button.append(icon(name));
  button.addEventListener("click", () => Promise.resolve(action()).catch(error => toast(error.message, true)));
  return button;
}
function toast(message, error = false) {
  const node = element("div", `toast${error ? " error" : ""}`, message);
  $("#toast-container").append(node);
  setTimeout(() => node.remove(), error ? 8500 : 4500);
}
async function api(path, {method = "GET", data} = {}) {
  const response = await fetch(path, {method, headers:{"Content-Type":"application/json", "X-App-Token":state.token}, ...(data !== undefined ? {body:JSON.stringify(data)} : {})});
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || `HTTP ${response.status}`);
  return result;
}
function humanSize(size = 0) {
  if (size < 1024) return `${size} B`;
  const units = ["KB", "MB", "GB", "TB"]; let index = -1;
  do { size /= 1024; index++; } while (size >= 1024 && index < units.length - 1);
  return `${size >= 100 ? size.toFixed(0) : size.toFixed(1)} ${units[index]}`;
}
function duration(seconds = 0) {
  const value = Math.round(seconds), h = Math.floor(value / 3600), m = Math.floor(value % 3600 / 60), s = value % 60;
  return h ? `${h}:${String(m).padStart(2,"0")}:${String(s).padStart(2,"0")}` : `${String(m).padStart(2,"0")}:${String(s).padStart(2,"0")}`;
}
function channelName(count) { return ({1:t("mono"),2:t("stereo"),6:t("surround6"),8:t("surround8")})[count] || `${count} ch`; }
function chosenTrack(file) { return file.streams.find(s => s.index === state.tracks.get(file.id)) || file.streams.find(s => s.default) || file.streams[0]; }
function readyFiles() { const used = new Set(state.jobs.map(job => job.file_id)); return state.files.filter(file => !used.has(file.id)); }
function activeJobs() { return state.jobs.filter(job => ["queued","processing"].includes(job.status)); }
function doneJobs() { return state.jobs.filter(job => job.status === "completed"); }
function profile() { return state.profiles.find(p => p.id === settings.format); }

function translate() {
  document.documentElement.lang = language === "zh" ? "zh-CN" : "en";
  document.title = language === "zh" ? "声迹 · 视频转音频" : "AudioDrop · Video to Audio";
  $$('[data-i18n]').forEach(node => node.textContent = t(node.dataset.i18n));
  $("#mini-button").title = t("miniTitle"); $("#mini-button").setAttribute("aria-label", t("miniTitle"));
  buildFormatSelect(); renderSettings(); switchView(state.view); render();
}
function option(value, label) { const item = element("option", "", label); item.value = value; return item; }
function buildFormatSelect() {
  const select = $("#format-select"); select.replaceChildren(option("copy", t("copyOption")));
  for (const [group, key] of [["common","commonGroup"],["lossless","losslessGroup"],["legacy","legacyGroup"]]) {
    const optgroup = element("optgroup"); optgroup.label = t(key);
    for (const p of state.profiles.filter(p => p.group === group)) {
      const item = option(p.id, p.label.replace("音频", language === "en" ? "audio" : "音频") + (p.available ? "" : ` (${t("unavailable")})`));
      item.disabled = !p.available; optgroup.append(item);
    }
    if (optgroup.children.length) select.append(optgroup);
  }
  if (settings.format !== "copy" && !profile()) settings.format = "wav";
  select.value = settings.format;
}
function replaceOptions(select, entries, value) {
  select.replaceChildren(...entries.map(([value, label]) => option(value, label)));
  select.value = String(value);
  if (select.selectedIndex < 0) select.selectedIndex = 0;
  return select.value;
}
function renderSettings() {
  const p = profile(), copy = settings.format === "copy";
  $("#format-select").value = settings.format;
  $$("[data-preset]").forEach(node => node.classList.toggle("active", node.dataset.preset === settings.format));
  $("#encoding-fields").hidden = copy; $("#copy-notice").hidden = !copy;
  const badge = $("#format-badge"); badge.textContent = t(copy ? "directCopy" : p?.lossless ? "lossless" : "lossy"); badge.classList.toggle("lossy", !copy && !p?.lossless);
  $("#codec-name").textContent = copy ? "AUTO" : (p?.encoder || "PCM").replace("lib", "").replace("pcm_s16le", "PCM").replace("pcm_s16be", "PCM").toUpperCase();
  const descriptions = {wav:"wavDescription",mp3:"mp3Description",flac:"flacDescription",ogg_flac:"flacDescription",m4a:"m4aDescription",m4a_alac:"alacDescription"};
  $("#format-description").textContent = copy ? t("copyNote") : p?.note && language === "zh" ? p.note : t(settings.format.startsWith("pcm_") ? "pcmDescription" : descriptions[settings.format] || "genericDescription");
  if (p && !copy) {
    const rates = p.rates.map(rate => [rate, `${rate.toLocaleString(language === "zh" ? "zh-CN" : "en-US")} Hz`]);
    settings.sample_rate = Number(replaceOptions($("#rate-select"), p.fixed_rate ? rates : [[0,t("keepOriginal")],...rates], settings.sample_rate));
    $("#rate-select").disabled = Boolean(p.fixed_rate);
    const channels = p.channel_options.map(channel => [channel,channelName(channel)]);
    settings.channels = Number(replaceOptions($("#channels-select"), p.fixed_channels ? channels : [[0,t("keepOriginal")],...channels], settings.channels));
    $("#channels-select").disabled = Boolean(p.fixed_channels);
    const quality = $("#quality-select");
    if (p.bit_depths.length) {
      $("#quality-label").textContent = t("bitDepth");
      settings.bit_depth = replaceOptions(quality,p.bit_depths.map(depth => [depth,depth === "32f" ? "32 bit float" : `${depth} bit`]),settings.bit_depth);
      quality.disabled = false;
    } else if (p.bitrate && !p.fixed_rate) {
      $("#quality-label").textContent = t("bitrate");
      settings.bitrate = Number(replaceOptions(quality,[32,48,64,96,128,160,192,224,256,320].map(rate => [rate,`${rate} kbps`]),settings.bitrate));
      quality.disabled = false;
    } else {
      $("#quality-label").textContent = t("bitrate"); replaceOptions(quality,[["fixed",p.fixed_rate && p.bitrate ? "12.2 kbps" : t("fixedQuality")]],"fixed"); quality.disabled = true;
    }
  }
  $("#volume-range").value = settings.volume; updateVolume();
  $("#prefer-copy").checked = settings.prefer_copy;
  let summary = copy ? t("copyOption") : p?.label || "WAV · PCM";
  if (p?.bit_depths.length) summary += ` · ${settings.bit_depth === "32f" ? "32f" : settings.bit_depth} bit`;
  else if (p?.bitrate && !p.fixed_rate) summary += ` · ${settings.bitrate}k`;
  $("#selected-summary").textContent = summary;
  remember("audiodrop.settings", settings);
}
function updateVolume() {
  $("#volume-reset").replaceChildren(document.createTextNode(settings.volume),element("span","","%"));
  const percent = Number(settings.volume) / 3;
  $("#volume-range").style.background = `linear-gradient(to right, #6ba282 0%, #6ba282 ${percent}%, #e7eee4 ${percent}%, #e7eee4 100%)`;
}
function readSettings() {
  const p = profile();
  if (settings.format === "copy") return {...settings,sample_rate:0,channels:0,volume:100};
  settings.sample_rate = Number($("#rate-select").value); settings.channels = Number($("#channels-select").value);
  if (p?.bit_depths.length) settings.bit_depth = $("#quality-select").value;
  else if (p?.bitrate && !p.fixed_rate) settings.bitrate = Number($("#quality-select").value);
  settings.volume = Number($("#volume-range").value); settings.prefer_copy = $("#prefer-copy").checked;
  remember("audiodrop.settings",settings); return {...settings};
}

function buildRow(item, type) {
  const row = element("div", `file-row ${item.status || "ready"}`);
  const isJob = type === "job", isUpload = type === "upload";
  const art = element("div", "file-art"); art.append(icon(item.status === "completed" ? "music" : "video")); row.append(art);
  const main = element("div", "file-main"), name = element("div", "file-name",item.output_name || item.name); name.title = name.textContent; main.append(name);
  const meta = element("div", "file-meta");
  let metadata = [];
  if (isJob) {
    metadata = [duration(item.duration), humanSize(item.output_size || item.source_size), item.status === "completed" ? (item.result_codec || "").toUpperCase() : item.stream.codec.toUpperCase()];
    if (item.status === "completed") metadata.push(t(item.mode === "copy" ? "copied" : "encoded"));
  } else if (isUpload) metadata = [humanSize(item.size),t(item.status === "probing" ? "probing" : item.status === "failed" ? "readFailed" : "uploading")];
  else {
    const stream = chosenTrack(item);
    metadata = [duration(item.duration),humanSize(item.size),stream.codec.toUpperCase(),`${stream.sample_rate / 1000} kHz`,channelName(stream.channels)];
  }
  metadata.filter(Boolean).forEach((text, index) => { if (index) meta.append(element("span","dot-separator")); meta.append(element("span","",text)); });
  main.append(meta);
  if (!isJob && !isUpload && item.streams.length > 1) {
    const select = element("select", "stream-select"); select.setAttribute("aria-label",`${item.name} ${t("track")}`);
    for (const [index,stream] of item.streams.entries()) select.append(option(stream.index,`${t("track")} ${index + 1} · ${stream.codec.toUpperCase()}${stream.language ? ` · ${stream.language}` : ""}${stream.title ? ` · ${stream.title}` : ""}${stream.default ? ` (${t("defaultTrack")})` : ""}`));
    select.value = chosenTrack(item).index; select.addEventListener("change", () => {state.tracks.set(item.id,Number(select.value)); render();}); main.append(select);
  }
  row.append(main);
  const actions = element("div", "file-actions");
  if (!isJob && !isUpload) {
    actions.append(element("span","file-status",t("ready")),iconButton("close",t("remove"),async () => {await api(`/api/files/${item.id}`,{method:"DELETE"}); state.files = state.files.filter(file => file.id !== item.id); state.seen.delete(item.fingerprint); render();}));
  } else if (isUpload) {
    if (item.status === "failed") actions.append(iconButton("retry",t("retry"),() => {state.uploads.delete(item.id); state.seen.delete(item.fingerprint); return addFiles([item.file]);}));
    actions.append(iconButton("close",t("remove"),() => {item.cancelled = true; item.xhr?.abort(); state.uploads.delete(item.id); state.seen.delete(item.fingerprint); render();}));
  } else {
    const status = element("span", `file-status ${item.status}`,t(item.status));
    if (item.status === "completed") status.prepend(icon("check"));
    actions.append(status);
    if (["queued","processing"].includes(item.status)) actions.append(iconButton("close",t("cancel"),() => cancelJob(item.id)));
    else if (item.status === "completed") {
      actions.append(iconButton("play",t("play"),() => playJob(item)),iconButton("download",t("download"),() => download(`/api/jobs/${item.id}/download`)),iconButton("retry",t("again"),() => retryJob(item)));
    } else actions.append(iconButton("retry",t("retry"),() => retryJob(item)));
  }
  row.append(actions);
  if (item.status === "processing" || (isUpload && ["uploading","probing"].includes(item.status))) {
    const progress = element("div","row-progress"), track = element("div","progress-track"), fill = element("div","progress-fill"); fill.style.width = `${item.progress || 0}%`; track.append(fill);
    progress.append(track,element("span","progress-value",`${Math.round(item.progress || 0)}%`)); row.append(progress);
  }
  if (item.error) row.append(element("div","row-error",item.error));
  if (isJob && item.note && language === "zh") row.append(element("div","row-note",item.note));
  if (isJob && item.status === "completed" && item.settings.format.startsWith("pcm_")) {
    const note = element("div","row-note"), link = element("button","text-button",t("metadata")); link.addEventListener("click",() => download(`/api/jobs/${item.id}/metadata`)); note.append(link); row.append(note);
  }
  return row;
}
function emptyState(history = false) {
  const empty = element("div","empty-state"), art = element("span","empty-icon"); art.append(icon(history ? "clock" : "music"));
  empty.append(art,element("strong","",t(history ? "noHistory" : "emptyTitle")),element("p","",t(history ? "noHistoryBody" : "emptyBody"))); return empty;
}
function reconcileRows(container, items, history = false) {
  if (!items.length) { if (container.dataset.emptyLanguage !== language) container.replaceChildren(emptyState(history)); container.dataset.emptyLanguage = language; return; }
  if (container.dataset.emptyLanguage) {container.replaceChildren(); delete container.dataset.emptyLanguage;}
  const oldRows = new Map([...container.children].map(row => [row.dataset.key,row]));
  const keys = new Set();
  items.forEach(({item,type},index) => {
    const key = `${type}-${item.id}`; keys.add(key);
    const signature = JSON.stringify([language,type,item.status,item.progress,item.output_name,item.output_size,item.note,item.error,state.tracks.get(item.id)]);
    let row = oldRows.get(key);
    if (!row || row.dataset.signature !== signature) {
      const replacement = buildRow(item,type); replacement.dataset.key = key; replacement.dataset.signature = signature;
      if (row) row.replaceWith(replacement); row = replacement;
    }
    if (container.children[index] !== row) container.insertBefore(row,container.children[index] || null);
  });
  [...container.children].forEach(row => {if (!keys.has(row.dataset.key)) row.remove();});
}
function render() {
  const ready = readyFiles(), active = activeJobs(), done = doneJobs();
  const queueItems = [...ready.map(item => ({item,type:"file"})),...[...state.uploads.values()].map(item => ({item,type:"upload"})),...state.jobs.map(item => ({item,type:"job"}))];
  queueItems.sort((a,b) => (a.item.created_at || 0) - (b.item.created_at || 0));
  reconcileRows($("#queue-list"),queueItems);
  const history = state.jobs.filter(job => ["completed","failed","cancelled"].includes(job.status)).sort((a,b) => b.created_at - a.created_at);
  reconcileRows($("#history-list"),history.map(item => ({item,type:"job"})),true);
  $("#queue-count").textContent = queueItems.length; $("#history-badge").textContent = history.length;
  $("#queue-summary").textContent = queueItems.length ? `${t("total")} ${queueItems.length} ${t("filesUnit")} · ${done.length} ${t("finished")}${active.length ? ` · ${active.length} ${t("working")}` : ""}` : t("queueEmpty");
  $("#start-count").textContent = ready.length ? `${ready.length} ${t("filesUnit")} ${t("pending")}` : t("noFiles");
  $("#start-conversion").disabled = !ready.length || !state.engine.ready || !state.connected || state.submitting;
  $("#cancel-all").hidden = !active.length;
  $("#download-all").disabled = !done.length; $("#history-download").disabled = !done.length;
  $("#clear-finished").disabled = !history.length;
  $("#output-path").textContent = state.output || "output"; $("#output-path").parentElement.title = state.output;
  const engine = $("#engine-status"); engine.replaceChildren(element("span",`status-dot${!state.connected ? " checking" : state.engine.ready ? "" : " error"}`),element("span","",t(!state.connected ? "connecting" : state.engine.ready ? "engineReady" : "engineMissing")));
  $("#about-engine").textContent = state.engine.version || t("noEngine");
  const available = state.profiles.filter(p => p.available).length; $("#supported-count").textContent = `${available || 33} AUDIO FORMATS`;
  updateMini();
}

const mediaExtension = /\.(mp4|m4v|mkv|avi|mov|flv|wmv|webm|ts|mts|m2ts|tp|mpg|mpeg|vob|asf|ogv|3gp|3g2|rm|rmvb|mp3|mp2|wav|wave|flac|m4a|aac|ogg|oga|opus|aiff|aif|amr|au|wma|ac3|eac3|mka)$/i;
async function addFiles(files, fromDirectory = false) {
  if (!state.engine.ready) {toast(t("noEngine"),true); return;}
  switchView("workspace");
  const filtered = fromDirectory ? files.filter(file => mediaExtension.test(file.name)) : files;
  if (filtered.length < files.length) toast(`${t("skipped")} (${files.length - filtered.length})`);
  const pending = [];
  for (const file of filtered) {
    const fingerprint = `${file.name}:${file.size}:${file.lastModified}`;
    if (state.seen.has(fingerprint)) continue;
    state.seen.add(fingerprint);
    const upload = {id:crypto.randomUUID(),name:file.name,size:file.size,file,fingerprint,status:"uploading",progress:0,created_at:Date.now()/1000,cancelled:false};
    state.uploads.set(upload.id,upload); pending.push(upload);
  }
  if (!pending.length && filtered.length) {toast(t("duplicateSkipped")); return;}
  render();
  let next = 0;
  const worker = async () => { while (next < pending.length) {const upload = pending[next++]; if (!upload.cancelled) await uploadFile(upload);} };
  await Promise.all([worker(),worker()]);
}
function uploadFile(upload) {
  return new Promise(resolve => {
    const xhr = new XMLHttpRequest(); upload.xhr = xhr;
    xhr.open("POST",`/api/files?name=${encodeURIComponent(upload.name)}`); xhr.setRequestHeader("X-App-Token",state.token); xhr.setRequestHeader("Content-Type","application/octet-stream");
    xhr.upload.onprogress = event => {if (event.lengthComputable) {upload.progress = Math.round(event.loaded/event.total*100); if (upload.progress === 100) upload.status = "probing"; render();}};
    xhr.onload = async () => {
      try {
        const result = JSON.parse(xhr.responseText);
        if (xhr.status >= 400) throw new Error(result.error || t("readFailed"));
        if (upload.cancelled) {await api(`/api/files/${result.id}`,{method:"DELETE"}); resolve(); return;}
        result.fingerprint = upload.fingerprint; state.files.push(result); state.uploads.delete(upload.id);
        if ($("#auto-start").checked) await startBatch([result],false);
      } catch (error) { upload.status = "failed"; upload.error = error.message; }
      render(); resolve();
    };
    xhr.onerror = () => {upload.status="failed";upload.error=t("connectionLost");render();resolve();};
    xhr.onabort = () => resolve();
    xhr.send(upload.file);
  });
}
function startBatch(files = readyFiles(), notify = true) {
  batchTail = batchTail.catch(() => {}).then(() => submitBatch(files, notify));
  return batchTail;
}
async function submitBatch(files, notify) {
  if (!files.length) return;
  state.submitting = true; render();
  try {
    const result = await api("/api/jobs",{method:"POST",data:{files:files.map(file => ({file_id:file.id,stream_index:chosenTrack(file).index})),settings:readSettings()}});
    state.jobs.push(...result.jobs); if (notify) toast(`${t("batchStarted")} (${result.jobs.length})`);
  } catch (error) {toast(error.message,true);}
  finally {state.submitting=false;render();}
}
async function retryJob(job) {
  const result = await api("/api/jobs",{method:"POST",data:{files:[{file_id:job.file_id,stream_index:job.stream.index}],settings:readSettings()}});
  state.jobs.push(...result.jobs); switchView("workspace"); render();
}
async function cancelJob(id) {
  const result = await api(`/api/jobs/${id}/cancel`,{method:"POST",data:{}});
  state.jobs = state.jobs.map(job => job.id === id ? result : job); render();
}
function download(path) { const link = element("a"); link.href=path; link.download=""; document.body.append(link); link.click(); link.remove(); }
function downloadAll() {const ids=doneJobs().map(job=>job.id);if (!ids.length) {toast(t("noResults"));return;}download(`/api/download-all?ids=${ids.join(",")}`);}
function playJob(job) {
  $("#player-name").textContent = job.output_name; $("#player").hidden = false;
  const audio = $("#audio-element"); audio.src = `/api/jobs/${job.id}/preview`;
  audio.play().catch(error => {if(error.name !== "AbortError") toast(t("previewError"),true);});
}
function switchView(view) {
  state.view = view;
  for (const id of ["workspace","history","help"]) $(`#${id}-view`).hidden = id !== view;
  $$("[data-view]").forEach(node => {node.classList.toggle("active",node.dataset.view === view);node.setAttribute("aria-label",t(node.dataset.view === "workspace" ? "workbench" : node.dataset.view));});
  $("#view-title").textContent = t(view === "workspace" ? "workbench" : view);
  $("#page-title").textContent = t(view === "workspace" ? "pageTitle" : view);
  $("#page-subtitle").textContent = view === "workspace" ? t("pageSubtitle") : view === "history" ? t("historyDescription") : t("aboutTitle");
}
async function refresh(initial = false) {
  try {
    const data = await api(initial || !state.token ? "/api/bootstrap" : "/api/jobs");
    const previous = new Map(state.jobs.map(job => [job.id,job.status]));
    if (data.token) {
      state.token=data.token;state.engine=data.engine;state.profiles=data.profiles;state.files=data.files;
      buildFormatSelect(); renderSettings();
    }
    state.jobs=data.jobs;state.output=data.settings.output_dir;state.connected=true;$("#connection-banner").hidden=true;
    const completed = state.jobs.filter(job => job.status === "completed" && previous.has(job.id) && previous.get(job.id) !== "completed");
    if (completed.length) toast(`${t("conversionComplete")} · ${completed.length === 1 ? completed[0].output_name : `${completed.length} ${t("filesUnit")}`}`);
    render();
  } catch {state.connected=false;$("#connection-banner").hidden=false;render();}
}
async function poll() {await refresh(); setTimeout(poll,activeJobs().length || state.uploads.size ? 700 : 1800);}
async function miniWindow() {
  if (state.mini && !state.mini.closed) {state.mini.close();state.mini=null;return;}
  if (!("documentPictureInPicture" in window)) {document.body.classList.toggle("compact");toast(t("miniUnsupported"));return;}
  let mini;
  try {mini = await window.documentPictureInPicture.requestWindow({width:360,height:260});}
  catch {document.body.classList.toggle("compact");toast(t("miniUnsupported"));return;}
  state.mini=mini;
  mini.document.title=t("miniTitle");
  const style = mini.document.createElement("style"); style.textContent="*{box-sizing:border-box}body{font-family:'Segoe UI','Microsoft YaHei',sans-serif;margin:0;padding:22px;background:#f7faf6;color:#345641}h1{font-size:16px;margin:0 0 22px}p{font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}small{font-size:10px;color:#94a88c}.track{height:5px;border-radius:4px;background:#e0e9db;margin:15px 0}.fill{height:100%;background:#17836b;border-radius:4px}button{background:#17836b;color:#fff;border:0;border-radius:7px;padding:10px 14px;font-size:11px;cursor:pointer}.buttons{display:flex;gap:9px;margin-top:20px}.cancel{background:#e6eede;color:#809071}";
  mini.document.head.append(style);
  const heading=mini.document.createElement("h1");heading.textContent=t("miniTitle");
  const name=mini.document.createElement("p");name.id="mini-name";
  const subtitle=mini.document.createElement("small");subtitle.id="mini-subtitle";
  const track=mini.document.createElement("div");track.className="track";const fill=mini.document.createElement("div");fill.className="fill";fill.id="mini-fill";track.append(fill);
  const buttons=mini.document.createElement("div");buttons.className="buttons";
  const back=mini.document.createElement("button");back.textContent=t("backToApp");back.addEventListener("click",()=>{window.focus();mini.close();});
  const cancel=mini.document.createElement("button");cancel.textContent=t("cancel");cancel.className="cancel";cancel.id="mini-cancel";cancel.addEventListener("click",()=>{const job=state.jobs.find(job=>job.status==="processing");if(job) cancelJob(job.id).catch(error=>toast(error.message,true));});
  buttons.append(back,cancel);mini.document.body.append(heading,name,subtitle,track,buttons);mini.addEventListener("pagehide",()=>{state.mini=null;});updateMini();
}
function updateMini() {
  if (!state.mini || state.mini.closed) return;
  const doc=state.mini.document,current=state.jobs.find(job=>job.status==="processing"),active=activeJobs();
  doc.getElementById("mini-name").textContent=current?.name || t("miniIdle");
  doc.getElementById("mini-subtitle").textContent=current ? `${Math.round(current.progress)}% · ${active.length} ${t("filesUnit")} ${t("working")}` : `${doneJobs().length} ${t("finished")}`;
  doc.getElementById("mini-fill").style.width=`${current?.progress || 0}%`;doc.getElementById("mini-cancel").disabled=!current;
}

$$("[data-view]").forEach(node=>node.addEventListener("click",()=>switchView(node.dataset.view)));
$("#language-button").addEventListener("click",()=>{language=language==="zh"?"en":"zh";remember("audiodrop.language",language);translate();});
$("#format-select").addEventListener("change",()=>{settings.format=$("#format-select").value;settings.sample_rate=0;settings.channels=0;settings.bit_depth="16";renderSettings();render();});
$$("[data-preset]").forEach(node=>node.addEventListener("click",()=>{settings.format=node.dataset.preset;settings.sample_rate=0;settings.channels=0;settings.bit_depth="16";renderSettings();render();}));
for(const selector of ["#rate-select","#channels-select","#quality-select","#prefer-copy"]) $(selector).addEventListener("change",()=>{readSettings();renderSettings();});
$("#volume-range").addEventListener("input",()=>{settings.volume=Number($("#volume-range").value);updateVolume();remember("audiodrop.settings",settings);});
$("#volume-reset").addEventListener("click",()=>{settings.volume=100;$("#volume-range").value=100;updateVolume();remember("audiodrop.settings",settings);});
$("#reset-settings").addEventListener("click",()=>{settings={...defaultSettings};renderSettings();});
$("#auto-start").checked=stored("audiodrop.autoStart",false);
$("#auto-start").addEventListener("change",()=>{remember("audiodrop.autoStart",$("#auto-start").checked);if($("#auto-start").checked) startBatch();});
$("#pick-files").addEventListener("click",event=>{event.stopPropagation();$("#file-input").click();});
$("#pick-directory").addEventListener("click",event=>{event.stopPropagation();$("#directory-input").click();});
$("#file-input").addEventListener("change",event=>{addFiles([...event.target.files]);event.target.value="";});
$("#directory-input").addEventListener("change",event=>{addFiles([...event.target.files],true);event.target.value="";});
$("#native-pick").addEventListener("click",async event=>{
  event.stopPropagation();const button=event.currentTarget;button.disabled=true;toast(t("selectingNative"));
  try {const result=await api("/api/pick-files",{method:"POST",data:{}});state.files.push(...result.files);switchView("workspace");render();for(const error of result.errors) toast(`${error.name}: ${error.error}`,true);if(result.files.length&&$("#auto-start").checked) await startBatch(result.files);}
  catch(error){toast(error.message,true);}finally{button.disabled=false;}
});
const dropZone=$("#drop-zone");
dropZone.addEventListener("click",event=>{if(!event.target.closest("button,input")) $("#file-input").click();});
dropZone.addEventListener("keydown",event=>{if(event.target===dropZone&&["Enter"," "].includes(event.key)){event.preventDefault();$("#file-input").click();}});
let dragDepth=0;
document.addEventListener("dragenter",event=>{if(event.dataTransfer?.types.includes("Files")){event.preventDefault();dragDepth++;dropZone.classList.add("dragging");}});
document.addEventListener("dragover",event=>{if(event.dataTransfer?.types.includes("Files")){event.preventDefault();event.dataTransfer.dropEffect="copy";}});
document.addEventListener("dragleave",event=>{event.preventDefault();dragDepth=Math.max(0,dragDepth-1);if(!dragDepth) dropZone.classList.remove("dragging");});
async function readDirectoryEntry(entry) {
  if(entry.isFile) return new Promise(resolve=>entry.file(file=>resolve([file]),()=>resolve([])));
  if(!entry.isDirectory) return [];
  const reader=entry.createReader(),entries=[];
  while(true){const chunk=await new Promise(resolve=>reader.readEntries(resolve,()=>resolve([])));if(!chunk.length) break;entries.push(...chunk);}
  const result=[];for(const child of entries) result.push(...await readDirectoryEntry(child));return result;
}
document.addEventListener("drop",async event=>{
  event.preventDefault();dragDepth=0;dropZone.classList.remove("dragging");
  const entries=[...event.dataTransfer.items].map(item=>item.webkitGetAsEntry?.()).filter(Boolean);
  if(entries.some(entry=>entry.isDirectory)){const files=[];for(const entry of entries) files.push(...await readDirectoryEntry(entry));await addFiles(files,true);}
  else await addFiles([...event.dataTransfer.files]);
});
$("#start-conversion").addEventListener("click",()=>startBatch());
$("#cancel-all").addEventListener("click",async()=>{try{for(const job of activeJobs()) await cancelJob(job.id);}catch(error){toast(error.message,true);}});
$("#clear-finished").addEventListener("click",async()=>{
  try{const result=await api("/api/clear-finished",{method:"POST",data:{}});const removed=new Set(result.removed);state.jobs=state.jobs.filter(job=>!removed.has(job.id));await refresh(true);state.seen.clear();for(const item of state.uploads.values())state.seen.add(item.fingerprint);toast(t("recordsCleared"));}catch(error){toast(error.message,true);}
});
$("#download-all").addEventListener("click",downloadAll);$("#history-download").addEventListener("click",downloadAll);
$("#open-output").addEventListener("click",()=>api("/api/open-folder",{method:"POST",data:{}}).catch(error=>toast(error.message,true)));
$("#change-output").addEventListener("click",async()=>{
  const button=$("#change-output");button.disabled=true;toast(t("selectingOutput"));
  try{const result=await api("/api/pick-output",{method:"POST",data:{}});state.output=result.output_dir;render();}catch(error){toast(error.message,true);}finally{button.disabled=false;}
});
$("#mini-button").addEventListener("click",()=>miniWindow().catch(error=>toast(error.message,true)));
$("#close-player").addEventListener("click",()=>{$("#audio-element").pause();$("#audio-element").removeAttribute("src");$("#player").hidden=true;});
$("#audio-element").addEventListener("error",()=>{if($("#audio-element").getAttribute("src")) toast(t("previewError"),true);});
translate();
refresh(true).finally(()=>setTimeout(poll,1800));
