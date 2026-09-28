# 预览与部署

当前主页使用 AcadHomepage 的 Hugo 移植版。无需 Jekyll、Node.js 或远程字体。

本地预览：

```sh
hugo server --bind 127.0.0.1 --port 1313
```

访问 http://localhost:1313/。构建命令为 `hugo --cleanDestinationDir`，输出目录为 `public/`。

发布仓库为 `https://github.com/CLIVERCHEN/CLIVERCHEN.github.io`，线上地址为 `https://cliverchen.github.io/`。推送到 `main` 后，`.github/workflows/hugo.yaml` 使用 Hugo Extended 0.154.5 构建并发布到 GitHub Pages。构建产物 `public/` 无需提交。

本地工作目录没有 `.git`；发布时将有效源码同步到仓库工作副本，检查差异后提交并推送。不要将整个目录直接上传，也不要启用旧模板的 Jekyll 流程。

照片更新：将原图放入 `static/img/photography/`，精选照片放入其 `selected/` 子目录并在 `scripts/prepare_photos.py` 中登记。运行 `python3 scripts/prepare_photos.py` 后，提交 `data/photos.json`、`static/media/` 和脚本的变动。本次 `src/photography/` 中的新增照片已同步；以后仅更新 `src/` 不会自动进入网页。

需要保留的源码为 `hugo.toml`、`content/`、`data/`、`layouts/`、`assets/`、`themes/acad-homepage/`、`static/media/`、`static/CV.pdf`、`static/favicon.svg`。`scripts/prepare_photos.py` 用于更新照片；生成好的网页照片已包含在 `static/media/`，普通构建不需要 Python。

原始摄影文件、`src/`、`.legacy-hugo-20260928/`、旧 `themes/barks/`、`resources/` 和旧预览文件不必上传。`hugo.toml` 已排除相机原图，不会把 1.3 GB 的原图复制到发布目录。

论文和 news 的信息来源见 `docs/CONTENT_SOURCES.md`。旧 CV 原文件保留，未自动改写其中内容。
