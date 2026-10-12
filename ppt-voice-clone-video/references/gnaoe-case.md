# G-NAOE 已验证案例（2026-10-12）

## 位置和批准

本例项目目录名为 `VOCAL_CLONE`，下文用 `<BASE>` 表示，复用时设置自己的绝对路径，例如 `C:/AI/tts-project`。本共享技能不包含案例工程、模型权重、音频或讲稿；文中已有脚本属于案例工程，复现时需提供工程文件或按技术流程实现。

Python：`<BASE>/.venv312/Scripts/python.exe -X utf8`。参考是上级 `audio [vocals].mp3`，逐页文本是上级 `narration_source/slide_01.txt` 至 `slide_16.txt`。图片在 `GNAOE_PPT/V2_Liu et al., G-NAOE2026_PPT/1.jpg` 至 `16.jpg`。

网页：`http://127.0.0.1:7861/`，优先复用已有进程；需要启动时双击 `<BASE>/启动声音克隆.bat`。FFmpeg：`<BASE>/bin/ffmpeg.exe`。

用户已批准 A 并要求全量配音。A 是 `analysis/audio_quality/A_native_matched.wav`，对应原生波形 `native_speed_1_00.wav`。速度 1.0，固定增益匹配 -24 LUFS；没有后期时间拉伸。温度 0.75、种子 42，不保证跨环境相同波形。

参考窗口起点约 51 秒，请求 15 秒，trim 后实际约 12.907 秒；切片 `preview/reference_selected.wav`，以元数据为准。每页短段间 0.22 秒静音，页面间 0.5 秒静音，末页不加。

用户最终要求文字不换行。正式使用 `GNAOE_full_narration_single_line.srt`；180 条的断句和时间与双行版一致。

## 环境

详细从零部署路线、安装补丁、分块下载和故障定位见 [chatterbox-turbo-deployment.md](chatterbox-turbo-deployment.md)。

本机 RTX 5060 Laptop 8 GB，Python 3.12，torch 2.14.0+cu132，torchaudio 2.11.0+cpu。这个非标准组合在本机通过实际 GPU 计算、频谱、Kaldi 特征、导入和生成测试，不是其他机器的通用安装方案。

Transformers 5.2.0、Gradio 6.8.0、librosa 0.11.0、numpy 1.26.4、soundfile、pyloudnorm。完整版本见 `requirements-installed.txt`，诊断见 `diagnostics.json` 和 `package-check.log`。模型在 `models/turbo` 和 `models/wav2vec2-base-960h`，已有大权重 SHA-256 记录，避免重复下载。

网页 `app.py` 仍默认速度 0.95，展示早期试音。批准方案为 1.0；调用 API 或网页时显式指定原速，不能把旧默认值当作最后批准设置。

## 当前脚本的适用范围

| 文件 | 说明 |
|---|---|
| `engine.py` / `app.py` | 本机克隆引擎、网页和模型单例 |
| `batch_narration.py` | 本次 16 页；硬编码交付日期、源目录及批准首页波形 |
| `repair_narration.py` | 修复指定片段并保留旧证据；第 9 页第 3 段小数已修复 |
| `align_subtitles.py` | CPU CTC 对齐与双行排版，写定本例路径 |
| `package_narration.py` | 合并音频、双行全局 SRT、页表、质量记录及原文件包 |
| `download_models.py` / `download_alignment.py` | 下载模型；已有本地权重不需重复 |
| `download_large_weights.py` | CDN 大文件停滞时的断点分块下载，并校验 SHA |

不要直接在新项目运行这些硬编码脚本：旧输出存在可能跳过新输入，首页可能复用本例旧音频。新项目需新清单、输入摘要、参数化脚本和独立输出目录。

## 交付状态

`<BASE>/delivery_20261012/`：16 页，总时长 611.100 秒，180 条字幕，质量记录按空白分词计 1386 个原稿词。

- `GNAOE_full_narration.mp3` / `.wav`：合并配音。
- `GNAOE_full_narration_single_line.srt`：正式单行字幕。
- `GNAOE_full_narration.srt`：原双行字幕，保留作历史。
- `GNAOE_slide_guides.srt`：16 个连续页区间，匹配合并配音。
- `slide_01/` 至 `slide_16/`：各页 MP3/WAV/SRT、讲稿及元数据；原逐页 SRT 为双行，需要单行时另转换。
- `slide_timings.csv` / `.json`：包含页间停顿的图片显示区间。
- `quality_report.json`：覆盖、时序、重叠、越页和峰值检查通过。
- `GNAOE_narration_and_subtitles.zip`：原全量包，尚不含后来新增的单行 SRT 和换页提示。需要最新版整包时更新包装；重新运行原打包脚本仍只会打原版本。

原始 DOCX、图片和参考音频未改。临时下载分块和早期环境仍在，之前自动审批拒绝删除；本技能不自行清理。
