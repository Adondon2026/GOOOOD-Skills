# Chatterbox Turbo：Windows 部署路线与实际排障记录

适用场景：本机英文声音克隆，Windows、NVIDIA GPU、Python 隔离环境。以下区分本机已验证事实与新机器应按当时版本调整的步骤。记录日期为 2026-10-12。

路线：**检查已有部署 → 选择 Python → 先验证 GPU PyTorch → 处理应用依赖与安装形式 → 下载并校验权重 → 原生短段试音 → 网页服务**。任何一层失败，先在该层定位，避免把所有组件一起反复重装。

## 0. 已有部署优先复用

本次已部署目录见 [gnaoe-case.md](gnaoe-case.md)，无需重新安装。以下命令在该项目根目录执行，目标是检查已有环境：

```powershell
$ttsRoot = (Get-Location).Path
$ttsPython = Join-Path $ttsRoot '.venv312/Scripts/python.exe'
& $ttsPython -X utf8 diagnose.py
uv pip check --python $ttsPython
& $ttsPython -X utf8 launcher.py
```

网页已运行时 `launcher.py` 先核查 `/config` 中的应用标题，然后打开已有服务，不再加载第二份模型。不要同时运行会独立加载模型的命令行生成脚本和网页，尤其在 8 GB 显存机器上。

最小完整成功条件：GPU 真运算、音频特征、模型导入通过；权重校验通过；实际短段 WAV 可播放；MP3 导出成功；网页 API 可生成。包能安装或页面能打开都不是完整成功。

### 迁移当前网页到新机器时需要带走什么

`engine.py`、`app.py`、`launcher.py`、`diagnose.py`、`download_models.py`、`download_large_weights.py`、启动/停止 BAT 是本次自建脚本，不在 Chatterbox 官方仓库里。本共享技能不附带这些案例工程文件；拿到原工程后，复现当前网页时把它们复制到新项目根目录，同时带走 `source`、`wheels`、`bin/ffmpeg.exe`、`models/turbo` 及权重校验记录；讲稿和参考音频按实际路径配置。

虚拟环境在新机器重新建立，不能把旧 `.venv312` 复制过去当成可移植安装。原有代码中的目录、首页讲稿、7861 端口及参考路径要检查。只部署官方模型而不复现网页时不需要这些自建脚本，按下面的独立短段验收即可。

## 1. Python 与 Windows 路径

新目录的可选基础步骤：

```powershell
# uv、Python 3.12 与驱动应先按当前官方渠道准备。
# C:/AI/tts-project 只是新项目示例目录；不要覆盖已有部署目录。
$ttsRoot = 'C:/AI/tts-project'
$ttsSkillRoot = 'C:/AI/skills/ppt-voice-clone-video'  # 换成实际技能安装位置
New-Item -ItemType Directory -Force -Path $ttsRoot | Out-Null
Set-Location -LiteralPath $ttsRoot
uv venv --python 3.12 .venv312
$ttsPython = Join-Path $ttsRoot '.venv312/Scripts/python.exe'
& $ttsPython -X utf8 -c 'import sys; print(sys.executable); print(sys.version)'
```

不需要激活脚本，每次指定虚拟环境解释器即可，避免 PowerShell execution policy 和误用系统 Python。本例最初试过 Python 3.11 环境，最终稳定在 3.12；不能因此宣称 3.11 一概不可用。

本例所有路径含中文。在可编辑安装过程中，`.pth` 启动文件解码曾遇到 GBK/Unicode 问题，因此最终使用**构建 wheel 后普通安装**。Python 命令统一带 `-X utf8`，读写文本显式 UTF-8，PowerShell 文件操作用 `-LiteralPath`。

`-X utf8` 有助于编码，但不能保证修复所有第三方 `.pth` 内容；发生此类启动错误时检查可编辑安装和实际 `.pth`，不要继续把它误判为模型错误。无需为了部署移动或改名原始素材目录。

## 2. 先解决显卡，而不是先安装全部 TTS 依赖

执行 `nvidia-smi` 确认驱动和显卡。选择支持该 GPU 架构、Windows/Python 版本的 PyTorch wheel，按 [PyTorch 官方安装选择器](https://pytorch.org/get-started/locally/) 确认命令和下载源。不要把 `nvidia-smi` 显示的最高 CUDA 版本当作 PyTorch 实际运行时版本。

本机验证结果：

| 项目 | 值 |
|---|---|
| Python | 3.12.11 |
| GPU | RTX 5060 Laptop，8 GB |
| Compute capability | 12.0 |
| torch | 2.14.0+cu132 |
| torch CUDA runtime | 13.2 |
| 编译支持架构 | 包含 `sm_120` |
| torchaudio | 2.11.0+cpu |

本次保存的 Chatterbox 0.1.7 源码把 Python 3.14 以下的 torch/torchaudio 固定为 2.6.0。直接照其依赖安装，可能与新显卡所需的 CUDA 构建冲突，因此不能先让 TTS 包把已经适配好的 GPU PyTorch 降级。

先运行下面的真运算。CUDA 可见却 kernel 失败，应先修复驱动/wheel/架构支持，暂不下载模型：

```powershell
& $ttsPython -X utf8 -c 'import torch; print(torch.__version__, torch.version.cuda); print(torch.cuda.is_available()); print(torch.cuda.get_device_capability()); print(torch.cuda.get_arch_list()); print((torch.ones(4, device="cuda") * 2).sum().item())'
```

本机 torch wheel 来自已缓存的阿里云 PyTorch wheel 链接，详见项目 `requirements-installed.txt`；这是历史来源记录。新机器优先采用官方可验证的下载渠道，不把镜像地址和本机版本写成通用“最新版”。

### torchaudio 的兼容性经验

本机音频变换在 CPU 上，TTS 神经网络在 CUDA 上，因此验证的是这个分工，而不是只比较两个包版本号。当前 [TorchAudio 官方文档](https://docs.pytorch.org/audio/main/installation.html) 说明 2.11 使用稳定 ABI，支持 PyTorch 2.11 及以后版本；较旧 TorchAudio 仍应按兼容矩阵匹配。不能沿用“所有版本必须完全同号”的旧判断，也不能将任意 CPU/CUDA 混搭当作已验证。

需要实际运行 Spectrogram、Kaldi fbank 和短段合成。最近版本的 `torchaudio.load/save` 还可能涉及 TorchCodec；本例输入使用 librosa，WAV 输出使用 soundfile，MP3 使用独立 FFmpeg，不为未使用的 I/O 路径安装额外解码依赖。

## 3. 应用依赖、Perth 和源码安装

官方项目：[Chatterbox](https://github.com/resemble-ai/chatterbox)、[Perth](https://github.com/resemble-ai/Perth)。普通环境可先遵循其当前安装方式；只有实际遇到 GPU 版本固定、网络或编码问题时才使用下述本地修正路线。

本例 Git clone/依赖中的 Git 下载曾失败，而官方 codeload ZIP 下载成功。因此先下载两个官方源码 ZIP，不无限重试同一 Git 连接：

```powershell
Invoke-WebRequest -Uri 'https://codeload.github.com/resemble-ai/chatterbox/zip/refs/heads/master' -OutFile 'chatterbox-source.zip'
Invoke-WebRequest -Uri 'https://codeload.github.com/resemble-ai/Perth/zip/refs/heads/master' -OutFile 'perth-source.zip'
Expand-Archive -LiteralPath 'chatterbox-source.zip' -DestinationPath 'source'
Expand-Archive -LiteralPath 'perth-source.zip' -DestinationPath 'source'
```

`master` 是本例快照的分支名，部署时核实当前分支并记录具体 revision/归档摘要。已有目录不重复解压覆盖。保留源 ZIP 作为修正前版本。

本次只对 Chatterbox 本地 `pyproject.toml` 作如下依赖修正，未修改模型算法或水印：

| 保存的原源码依赖 | 本地构建依赖 |
|---|---|
| `torch==2.6.0; python_version < '3.14'` | `torch>=2.11.0; python_version < '3.14'` |
| `torchaudio==2.6.0; python_version < '3.14'` | `torchaudio>=2.11.0; python_version < '3.14'` |
| `resemble-perth @ git+https://github.com/resemble-ai/Perth.git@master` | `resemble-perth>=1.1.0` |

这些不是让所有电脑无条件套用的补丁。新源码如果已修正，不再重复补丁；选择好具体 GPU 包后，用约束固定已验证的 torch/torchaudio，避免宽范围依赖解析再次替换它们。Perth 仍然安装并保留水印机制。

本例其他关键包版本：numpy 1.26.4、librosa 0.11.0、Transformers 5.2.0、diffusers 0.29.0、safetensors 0.5.3、Gradio 6.8.0、gradio-client 2.2.0、huggingface-hub 1.33.0、soundfile 0.14.0、pyloudnorm 0.2.0。完整快照是项目 `requirements-installed.txt`。

技能附带 [requirements-runtime-20261012.txt](../assets/requirements-runtime-20261012.txt)，是本例可复用的直接运行依赖，不含需按显卡先选定的 torch/torchaudio 或本地构建包，也不是完整的传递依赖锁。GPU 栈验证后，先把实际版本约束住，再装运行依赖：

```powershell
$ttsTorchVersion = & $ttsPython -X utf8 -c 'import torch; print(torch.__version__)'
$ttsAudioVersion = & $ttsPython -X utf8 -c 'import torchaudio; print(torchaudio.__version__)'
@("torch==$ttsTorchVersion", "torchaudio==$ttsAudioVersion") | Set-Content -LiteralPath 'constraints-gpu.txt' -Encoding utf8
uv pip install --python $ttsPython -c 'constraints-gpu.txt' -r (Join-Path $ttsSkillRoot 'assets/requirements-runtime-20261012.txt')
```

技能目录在新机器可能不同，应替换路径。较新的 torch/torchaudio 元数据和这些历史依赖发生冲突时应查具体缺项，不解除所有约束盲目升级。

安装顺序建议：先 GPU torch/兼容 torchaudio 并验证 → 安装其他运行依赖（约束已选 torch）→ 构建本地 wheel → 安装这两个 wheel → `uv pip check`。例如在已有源码目录中：

```powershell
uv build --wheel 'source/Perth-master' --out-dir 'wheels'
uv build --wheel 'source/chatterbox-master' --out-dir 'wheels'
# --no-deps 仅在运行依赖已经安装并已约束 GPU 栈的阶段使用。
uv pip install --python $ttsPython --no-deps 'wheels/resemble_perth-1.1.0-py3-none-any.whl' 'wheels/chatterbox_tts-0.1.7-py3-none-any.whl'
uv pip check --python $ttsPython
```

wheel 文件名是本例版本，重建时使用实际生成文件名。[uv 命令说明](https://docs.astral.sh/uv/reference/cli/) 支持 build 和针对解释器的 pip 安装。`--no-deps` 不是解决缺依赖的魔法；check 失败时先补齐缺项，不继续生成。

项目 `requirements-app.txt` 包含非 GPU 应用依赖，可供参考；不等于完整冻结文件。`requirements-installed.txt` 包含本机 wheel URL 和绝对路径，也不能不修改就作为另一台机器的安装清单。

## 4. 模型下载：先常规，再针对大文件停滞

官方权重：[ResembleAI/chatterbox-turbo](https://huggingface.co/ResembleAI/chatterbox-turbo)。本例保存到 `models/turbo`，下载文件清单见 `download_models.py`：

```text
t3_turbo_v1.safetensors
s3gen_meanflow.safetensors
ve.safetensors
conds.pt
added_tokens.json
merges.txt
special_tokens_map.json
tokenizer_config.json
vocab.json
```

正常路线：`snapshot_download` 按清单下载；本例设置 `HF_HOME` 到项目模型目录、`HF_HUB_DISABLE_XET=1`、`HF_HUB_DOWNLOAD_TIMEOUT=180`、并发 3。本地已经完成的权重不要重复下载。

本例真正耗时最大的环节是两个大权重整文件传输停滞，不是 TTS 推理。fallback 脚本 `download_large_weights.py` 的策略：

1. 从 resolver 的 HEAD 重定向获得最终 CDN 地址；只在内存中保存签名地址，避免日志泄露。
2. 按 1 MiB 发送 Range 请求，逐块持久化；本次并发 48，网络不同从较小并发试起。
3. 必须检查状态 206、精确 Content-Range 和返回字节数，不能将忽略 Range 的整文件响应当作分块。
4. 已完整的分块续用，失败有限次退避重试；签名过期后重新解析地址，不反复用旧地址。
5. 按顺序组装临时完整文件，计算 SHA-256 一致后再作为权重文件。

本例 fallback resolver 使用 hf-mirror，并最终跳转 CDN；镜像只是传输路径，完整文件哈希仍依据官方文件元数据。`recover_download.py` 可回收已保存的 `.incomplete` 前缀完整块，但只能在确认该文件是从偏移零连续写入时使用。

已校验的本次大文件：

| 文件 | 字节数 | SHA-256 |
|---|---:|---|
| t3_turbo_v1.safetensors | 1915480052 | `fcf1f8c1d651bb7e3acd69ee5be269b4ac10c02980b7708213d598bc9f7cdf87` |
| s3gen_meanflow.safetensors | 1064875036 | `d65cb687a2ed581ee6cc297e919ffefa63386944f42364ae13b78a594945514f` |

新 revision 的文件信息可能变，不能拿本例哈希校验不同版本。本次记录保存在 `models/turbo/sha256_verified.json`。存在文件并不等于完整；正常下载脚本的“文件存在”短路检查要配合哈希/大小核验。

分块方式约需额外一份权重空间，另加缓存、环境和 wheel。本例两个权重约 3 GB，分块另约 3 GB；磁盘占用应在下载前估算。此前自动审批拒绝删除临时分块和测试环境，它们仍在；部署手册不通过换一种工具绕过拒绝。

## 5. FFmpeg、本地加载和短段验证

本机 PATH 最初找不到 FFmpeg，因此项目提供 `bin/ffmpeg.exe`，引擎把该目录加入进程 PATH，MP3 导出使用可执行文件的绝对路径。不能因为 librosa 能读 MP3 就认为 FFmpeg 编码器也可用。

```powershell
& (Join-Path $ttsRoot 'bin/ffmpeg.exe') -version
& $ttsPython -X utf8 diagnose.py
uv pip check --python $ttsPython
```

跨项目可用技能附带的 `scripts/deployment_probe.py`：

```powershell
& $ttsPython -X utf8 (Join-Path $ttsSkillRoot 'scripts/deployment_probe.py') --device cuda --ffmpeg (Join-Path $ttsRoot 'bin/ffmpeg.exe') --output (Join-Path $ttsRoot 'deployment_probe.json')
```

该探针检查真 kernel、Spectrogram、Kaldi fbank、Turbo 导入、soundfile 和 FFmpeg，不加载大模型，不访问远程权重。通过后仍需实际短段合成。

已下载权重时使用 `ChatterboxTurboTTS.from_local(checkpoint, device='cuda')`，避免又触发联网。准备实际参考切片，原速短段生成 WAV，再导出 MP3并检查时长、峰值和可播放性。已有网页时通过其 API 实测，复用模型；选择 1.0，网页当前旧默认值是 0.95。

只验收官方模型时，将以下代码保存为新项目的 `smoke_turbo.py`。`reference.wav` 换成实际的干净参考切片，先确定 GPU 没有另一份驻留模型：

```python
from pathlib import Path
import torch
import soundfile as sf
from chatterbox.tts_turbo import ChatterboxTurboTTS

torch.manual_seed(42)
model = ChatterboxTurboTTS.from_local(Path('models/turbo'), device='cuda')
model.prepare_conditionals('reference.wav')
with torch.inference_mode():
    audio = model.generate('Good afternoon, everyone. Today I will introduce our study.', temperature=0.75)
sf.write('smoke_turbo.wav', audio.squeeze().cpu().numpy(), model.sr, subtype='PCM_16')
print(model.sr, audio.numel() / model.sr)
```

运行及编码示例：

```powershell
& $ttsPython -X utf8 smoke_turbo.py
& (Join-Path $ttsRoot 'bin/ffmpeg.exe') -hide_banner -loglevel error -i smoke_turbo.wav -codec:a libmp3lame -b:a 192k smoke_turbo.mp3
```

这一步沿用已验证的本地模型调用形式，是新部署验收用法；本轮文档补全没有另加载模型或生成新试音，现有案例已有实际生成与解码证据。

本项目 `engine.py --preview --speed 1.0` 会独立加载模型，只在网页服务未占用 GPU 或确认显存足够时运行。生成过的批准音频可做恢复检查，不需要每次健康检查都重新合成。

## 6. 启动、端口与保存可复现记录

网页绑定 `127.0.0.1:7861`。启动前检查已有进程和应用身份，端口被其他服务占用时换空闲端口，不能先杀掉未知进程。后台启动 Windows 服务使用隐藏窗口并保存日志；双击启动器供用户交互打开网页。

模型在引擎单例中复用，合成序列化；不要一页启动一个模型进程。本例驻留服务约占 4 GB 显存，8 GB 卡上多个模型进程容易争抢显存。逐页配音可复用同一服务，字幕 CTC 对齐本次在 CPU 上运行。

保存：源码归档/revision、局部补丁、wheel、安装版本与实际来源、诊断 JSON、包兼容检查、权重哈希、短段实际输出、启动/停止脚本及日志。换机器先按这些证据重建，不只记“一条 pip install 成功”。

## 故障速查

| 症状 | 优先判断 | 处理顺序 |
|---|---|---|
| CUDA 可见，实际 kernel 失败 | wheel 是否包含显卡架构、驱动是否支持 | 修复 GPU 栈后再装应用 |
| 安装应用后 GPU torch 被替换 | 源码固定依赖或解析器选了其他变体 | 局部调整依赖并固定已验证版本 |
| Git clone / Perth Git 依赖失败 | Git 传输路径 | 官方 ZIP + 本地 wheel，保留 Perth |
| Python 一启动就 `.pth` / GBK 错误 | 中文路径与 editable 启动映射 | UTF-8 模式，优先普通 wheel 安装 |
| 小文件下载成功，大权重一直不动 | CDN 整文件传输 | 可续传 Range，校验范围、大小和 SHA |
| 页面可打开，但生成失败 | 未加载模型、缺权重或运行依赖 | 探针 → 权重核验 → 实际短段 API |
| WAV 成功，MP3 失败 | FFmpeg 路径或编码器 | 用绝对路径检查 FFmpeg与 libmp3lame |
| 生成声音有机器人感 | 参考/后处理/响度/合成伪影 | 同波形响度匹配 A/B，先保留原速 |

本次经验并非“以后都安装同一组最新包”，而是把每层检查与 fallback 固定下来，已有成功环境先复用，真正有证据的问题才调整。
