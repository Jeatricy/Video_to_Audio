# FFmpeg 引擎安装

声迹使用本机的 `ffmpeg` 和 `ffprobe`，可执行程序保留在本机，不随 Git 仓库提交。

## Windows

1. 安装 Python 3.10 或更高版本，并确保 `python` 或 `py` 可以在终端运行。
2. 打开 [FFmpeg 官方下载页面](https://ffmpeg.org/download.html)，选择 Windows 编译版本，例如 [Gyan Windows Builds](https://www.gyan.dev/ffmpeg/builds/)。
3. 下载 **Full Build** 并解压。Full Build 提供 AMR、GSM 等旧式格式所需的额外编码器。
4. 把解压包中的 `bin/ffmpeg.exe` 与 `bin/ffprobe.exe` 复制到本文件所在目录。
5. 返回项目根目录，双击 `start.bat`。

目录应包含：

```text
bin/
  README.md
  ffmpeg.exe
  ffprobe.exe
```

已安装并加入 PATH 的 FFmpeg 也能自动检测。如果要指定其他位置，可以设置 `FFMPEG_PATH` 与 `FFPROBE_PATH` 环境变量，值为对应可执行程序的完整路径。

## macOS / Linux

安装 Python 3.10 或更高版本，以及包含需要的编码器的 FFmpeg，然后在项目根目录运行 `python3 server.py`。Windows 的双击启动脚本仅适用于 Windows。

程序会根据本机 FFmpeg 实际提供的编码器与封装器显示可用格式。
