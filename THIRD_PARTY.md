# 第三方组件

本应用的网页和 Python 服务是独立实现，没有使用 Moo0 的程序代码或资源。Moo0 名称仅用于功能对照。

音频处理依赖 FFmpeg / FFprobe，Git 仓库没有分发这些第三方可执行程序。程序可以从本机 `bin`、PATH 或指定环境变量中读取引擎，安装步骤见 [bin/README.md](bin/README.md)。

开发时使用了本机通过 WinGet 安装的 Gyan FFmpeg Full Build，版本标识：

```
ffmpeg version 9.0-full_build-www.gyan.dev
Copyright (c) 2000-2026 the FFmpeg developers
configuration includes: --enable-gpl --enable-version3 --enable-static
```

- [FFmpeg 官方网站](https://ffmpeg.org/)
- [FFmpeg 下载入口及编译版本来源](https://ffmpeg.org/download.html)
- [Gyan Windows 编译版本及源码信息](https://www.gyan.dev/ffmpeg/builds/)
- [FFmpeg 许可与版权说明](https://ffmpeg.org/legal.html)
- [FFmpeg 转换、音轨选择与 Streamcopy 文档](https://ffmpeg.org/ffmpeg.html)
- [FFmpeg 音频编码器文档](https://ffmpeg.org/ffmpeg-codecs.html)

FFmpeg 的版权及许可属于其原作者。前端与服务不需要向外部发送任何视频或音频。
