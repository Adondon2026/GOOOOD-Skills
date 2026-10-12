# GOOOOD-Skills

可复用的 Agent Skills。每个根目录文件夹是一份独立技能，入口为 `SKILL.md`，配套流程、参考资料和脚本放在同一文件夹内。

| 技能 | 用途 |
|---|---|
| [evidence-first-writing-zh](evidence-first-writing-zh/SKILL.md) | 依据事实与材料组织科研、技术和专业表达，修改文字并校准结论强度 |
| [ppt-voice-clone-video](ppt-voice-clone-video/SKILL.md) | 英文声音克隆、逐页 PPT 配音、真实语音对齐、单行短句字幕及剪映换页提示 |

## PPT 配音与声音克隆

从参考音频开始，先试听确认音色，再逐页生成配音，核对数字及漏词，生成短句字幕和图片时长表。最终利用换页提示 SRT 在剪映中快速对齐图片。

- [完整技术流程](ppt-voice-clone-video/references/workflow.md)
- [Chatterbox Turbo Windows 部署路线与排障](ppt-voice-clone-video/references/chatterbox-turbo-deployment.md)
- [已验证案例与参数](ppt-voice-clone-video/references/gnaoe-case.md)
- [字幕转换、换页提示及校验工具](ppt-voice-clone-video/scripts/subtitle_tools.py)
- [环境诊断工具](ppt-voice-clone-video/scripts/deployment_probe.py)
- [案例运行依赖清单](ppt-voice-clone-video/assets/requirements-runtime-20261012.txt)

## 使用

将所需技能的完整文件夹复制到所用 Agent 的技能目录，保留 `references`、`scripts`、`assets` 等配套文件。Codex 可放到个人 `~/.codex/skills/`；运行脚本使用实际的绝对路径和适当的 Python 环境。

例如：

```text
使用 $ppt-voice-clone-video，根据 PPT 图片、逐页讲稿和参考声音制作配音，先试听，再生成单行短句字幕和剪映换页提示。
```

部署文档中的版本为 2026-10-12 案例记录，换机器需核对显卡和依赖兼容性。仓库包含技能规范、参考资料和辅助脚本，不包含模型权重、个人录音或原始讲稿。
