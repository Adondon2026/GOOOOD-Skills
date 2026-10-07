---
name: clear-grounded-writing-zh
description: 用于科研论文、技术说明、专业邮件、项目沟通和日常说明的清晰、自然、基于事实的写作技能。强调事实、证据、因果逻辑、自然节奏和克制表达，避免过度包装、空泛总结和明显的 AI 式措辞。
---

# 清晰、扎实地把一件事说清楚

> 本文件保留用户提供的完整写作规范，供 `evidence-first-writing-zh` 在正式写作、长文修改和“去 AI 味”任务中按需读取。

这个 Skill 适用于任何以“把事情说清楚”为主要目标的写作任务，包括科研论文、技术说明、项目报告、合作者邮件、导师沟通、审稿意见回复、研究现状总结、结果汇报、普通解释、日常专业沟通，以及对现有文字进行“去 AI 味”修改。

**本技能的宗旨是减轻读者不必要的理解负担，让读者能够快速、准确、流畅地理解所表达的内容。** 科研内容写作据此安排信息、解释设计依据、呈现证据和校准结论。作者承担整理材料与连接逻辑的工作，避免让读者反复回读、猜测指代、补齐推理或自行拼接信息。

默认采用直接陈述和连续论证。避免问答式标题、连续设问、自问自答以及“问题—答案”模板；用户明确要求FAQ、访谈或教学问答时除外。章节标题直接标明研究对象、方法、比较或结果。必要定义和背景在使用前给出，比较同时交代共同条件与变化因素，术语与指代保持一致。

减轻理解负担不等于一味缩短文字。实验条件、设计依据、逻辑衔接和结论边界属于必要信息，应就近说明；重复、跳跃、结构播报和无内容的修辞可以删除。

## 1. 总原则

在材料允许的情况下，优先按下面的逻辑写：

**做了什么 / 发生了什么 → 证据或原因 → 说明什么 → 有什么边界或下一步**

不要反过来先写一大堆意义、框架、价值，再慢慢告诉读者实际发生了什么。

不推荐：

> 本研究提出了一套具有较强鲁棒性和广泛适用性的综合分析框架，为复杂运行数据的深层次挖掘提供了重要支撑。

更推荐：

> 该方法将 3 min 观测间隔下的 ROT RMSE 降低了 31.4%。不过，剩余误差仍占实际 ROT 变化幅度的约三分之一。

后一种写法更有力量，因为证据本身在说话。

## 2. 先判断文字要完成什么任务

写之前确定读者需要掌握的核心事实：

- 科研论文：研究对象、检验内容和数据支持的结论。
- Methods：实验条件、操作步骤及设计依据。
- Results：变化方向、大小和成立条件。
- Discussion：结果的解释、意义与适用范围。
- 邮件：写信目的、必要更新和需要对方采取的行动。
- 技术说明：对象定义、工作原理及其与当前任务的联系。
- 普通说明：具体事情、原因和下一步行动。

如果一句话或一段话没有帮助完成这个任务，就考虑删掉、缩短或移动。

## 3. 先守住事实，再谈语言

当用户提供论文、数据、文档、实验结果、审稿意见或已有文字时：

1. 以已有材料为事实基础。
2. 不因为想让文字更顺就补充材料里没有的事实。
3. 区分“观察到 / 数据显示”“可以合理解释为”“尚未证明 / 未来需要验证”。
4. 不要为了显得有结论，把措辞写得比证据更强。
5. “比 baseline 好”不等于“高精度”。
6. “有部分信息”不等于“已经可辨识”。
7. “没有稳定证据”不等于“绝对不存在”。

修改已有文字时，默认采用局部手术式修改。不要一看到几句不自然，就把整篇全部重写。

## 4. 一段话围绕一个核心事实

科研和技术写作中，一个好的段落通常包括：

1. 结果或观察；
2. 数据或证据；
3. 解释；
4. 必要时给出边界。

例如：

> WNOA 在三个观测间隔下均降低了 ROT 重建误差。相对于线性插值，2、3 和 5 min 下的航段级 RMSE 分别下降 28.0%、31.4% 和 25.6%。这种改善较为稳定，但剩余误差仍不可忽略。

不需要再添加“这一结果充分证明了 WNOA 方法具有显著优势和良好应用潜力”，因为前面的数据已经说明问题了。

普通说明也一样：

> 会议改到周一，因为周五有两位评审无法参加。周一下午是四个人都能参加的最早时间，所以已经改到那个时间。

## 5. 优先使用“发生了什么”的动词

优先使用具体动词：增加、降低、上升、下降、改变符号、保持、超过、低于、删除、保留、隐藏、比较、估计、测量、预测、收敛、发散、覆盖、相关、未改善、显著恶化。

谨慎使用抽象动词：支持、促进、赋能、提供、揭示、彰显、强调、证明、定义、捕获、保留、展现。这些词不是不能用，但不能拿它们代替真正的实验结果。

不推荐：

> 结果表明该方法具有更优的预测性能。

推荐：

> 5 min heading MAE 从 11.67° 降到 6.44°。

## 6. 避免常见的“AI 形状”语言

以下句式和词语容易让文字显得像自动生成，尤其不能高频出现：

- “Rather than X, this study...”
- “Not only..., but also...”
- “This highlights the importance of...”
- “This underscores...”
- “To address this gap...”
- “It is worth noting that...”
- “It should be emphasized that...”
- “In today's rapidly evolving...”
- “A comprehensive / robust / advanced framework...”
- 连续使用 First、Then、Finally；
- 每段最后都加一句意义总结；
- 为了好看强行写三个并列点；
- 反复使用 support、framework、boundary、capability、applicability、transferability、robustness、significance；
- 反复使用 attractive、promising、powerful、sophisticated、highly effective。

直接说具体问题。

不推荐：

> Rather than treating sparse data as a generic reconstruction problem, the proposed framework separates state recoverability from dynamic identifiability.

更自然：

> State reconstruction and dynamic identification were analysed separately because they require different information from the recorded data.

如果上下文已经表达清楚，甚至可以直接删掉这句话。

## 7. 不要过度播报文章结构

好的文章本身有结构，不需要每隔一段告诉读者现在要做什么。减少“本节旨在”“下文将”“接下来首先”“随后”“最后”“本文其余结构如下”。只有读者确实需要导航时才使用。

不推荐：

> First, the data were segmented. Then, the observations were masked. Finally, the models were evaluated.

更自然：

> The data were segmented before 2-, 3-, and 5-min masking was applied. Model performance was then evaluated at the withheld one-minute observations.

## 8. 科研写作

### 8.1 Abstract

摘要只保留问题、数据或对象、核心方法、最重要的定量结果和一个克制的实际意义。推荐“问题 → 数据 → 方法 → 数字 → 结论”，不要把摘要写成缩小版 Discussion。

### 8.2 Introduction

Introduction 主要说明为什么问题值得研究、现有方法或数据有什么具体限制、本文到底测试什么。不要每段都强调 novelty，不要每段都创造抽象概念，也不要重复 Methods 中的完整流程。

推荐：

> Operational records contain long-term vessel-specific information, but their sampling rate is determined by routine logging rather than manoeuvring identification. This raises two separate questions: whether missing motion states can be reconstructed, and whether control-response dynamics can still be identified.

### 8.3 Methods

Methods 应该朴素，重点是让别人知道到底怎么做的。

推荐：

> The record was divided at temporal gaps and voyage discontinuities.

不要：

> A comprehensive preprocessing framework was implemented to ensure robust segmentation of the operational archive.

### 8.4 Results

Results 默认让数字和现象先行。

推荐：

> ROT RMSE decreased by 31.4% at the 3-min observation interval.

不推荐：

> The proposed method demonstrated superior reconstruction capability.

### 8.5 Discussion

Discussion 负责解释。使用克制表达，例如“is consistent with...”“may reflect...”“did not provide evidence for...”“under the investigated conditions...”“cannot be resolved at the available sampling rate...”“improved the point estimate but did not calibrate uncertainty...”。不要把“没看到稳定关系”写成“不存在关系”。

### 8.6 Conclusion

Conclusion 不是第二个 Abstract。通常只回答最重要的结果、最重要的边界、实际上应该怎么使用这些结果，不要重新讲一遍所有方法和数字。

## 9. 技术解释

按“定义 → 原理 → 例子 → 当前问题中的意义”组织。

例如：

> 奈奎斯特采样定理要求采样频率高于待解析最高频率的两倍。若用 1 Hz 采样一个 1 Hz 正弦信号，每次采样可能恰好落在相同相位，因此样本甚至无法反映它正在振荡。

不要一上来先讲一大段历史。

## 10. 专业邮件

默认结构是“写信目的 → 必要背景或更新 → 决定或请求 → 结束”。

例如：

> Please find attached the revised version. We have incorporated the main comments on the workflow, practical implications and figure references. Because the submission deadline is close, we plan to submit this version first and continue the remaining refinements afterwards.

不要把普通合作者邮件写成正式 rebuttal，除非用户明确要求逐条回复。

## 11. 普通解释和沟通

普通文字不需要学术化。按“事情 → 原因 → 下一步”组织。

推荐：

> 我可能晚到 20 分钟，地铁现在停在站外。你们先开始，我到了以后直接加入。

不要：

> 由于当前公共交通运行情况存在一定的不确定性，我预计到达时间可能受到影响。

## 12. 让句子有自然节奏

不要连续五句话使用相同短句或相同连接方式。可以长短结合，重点是自然，不是故意不整齐。

例如：

> WNOA improved the withheld ROT estimates at all three observation intervals. Increasing the state order with WNOJ did not provide a further gain and caused much larger forward-prediction errors. Adding measured rudder angle through the soft Nomoto model was also ineffective. The posterior intervals, meanwhile, were strongly under-dispersed.

## 13. 一次只处在一个抽象层级

如果一段正在报数字，就先把数字讲清楚；如果正在解释意义，再谈意义。不要把原始结果和高度抽象概念揉在一个句子里。

不推荐：

> The 31.4% RMSE reduction demonstrates the recoverability boundary of low-order state information and highlights the limited transferability of higher-order dynamics.

推荐：

> At the 3-min interval, WNOA reduced ROT RMSE by 31.4%. This shows that useful low-order state information remains in the sparse observations. It does not establish that higher-order dynamics can also be recovered.

## 14. 图表也是论证的一部分

图不是装饰。一张图最好只回答一个主要问题。正文引用图时，不只写“Figure 3 shows the results”，而要说明比较对象和主要现象。

例如：

> Figure 3 compares strictly causal forecasts at 1, 2 and 5 min. WNOA remained stable across the three horizons, whereas WNOJ error increased sharply with forecast length.

流程图优先体现“输入 → 操作 → 输出 → 下一步怎么用”。如果画了 Step 1、Step 2、Step 3，要让读者看见每一步产出了什么。

## 15. “去 AI 味”修改流程

用户明确说“AI 味很重”时，不要故意加错别字、口语词或不规范语法。按以下轮次检查：

1. 删除没有具体证据支撑的空泛评价词，如 robust、comprehensive、attractive、promising、advanced、powerful、significant。
2. 把评价换成数据，如将“The method showed superior performance”改成“RMSE decreased from 4.21 to 3.10 deg/min”。
3. 删除重复总结，连续两句话说同一件事时只保留更具体的一句。
4. 打破过度工整的结构，减少连续 First、Then、Finally、Whereas、While、Not only... but also...。
5. 减少“文章在解释文章”，删除没有实质信息的“This section aims to investigate...”等句子。
6. 检查结论强度：相关性不要写成因果，单一数据集不要写成普遍规律。
7. 按真实交流方式检查：真正做过实验的人在办公室里给同行解释时会不会这么说？如果不会，就简化。

## 16. 修改已有文字时的原则

- 保留原来的技术含义；
- 保留全文术语一致性；
- 不因润色增加新结论；
- 原本已经直接自然的句子不要硬改；
- 只有几句话有问题时，只改那几句；
- 不把所有段落统一成同一种句式；
- 保持目标文体原本的正式程度；
- 用户要求标黄、标注或 Track Changes 时，只标真正改动的部分。

## 17. 基于来源写作

如果用户提供论文、PDF、数据报告、审稿意见或文件：

- 以材料实际内容为依据；
- 保留原文的术语和范围；
- 材料之间有矛盾时，不要偷偷替用户解决；
- 加入外部研究时要明确区分；
- 不编造引用、结果或实验细节；
- 不能因为某篇文献主题相关，就拿来支持它没有说过的结论。

## 18. 最后检查

先检查阅读路径：对象和条件明确；必要背景先于使用；章节采用直接陈述；段落间有实质联系；比较无需读者自行换算或跨段拼接；没有问答式标题、连续设问或自问自答。检查时以减少不必要的理解负担为准，同时保留准确理解所需的信息。

- 主旨能不能很快看出来？
- 最重要的判断有没有证据？
- 能用数字的地方是不是用了数字？
- 有没有把相关写成因果？
- 有没有一句话只是为了告诉读者“下面我要解释”？
- 有没有大量抽象词可以换成具体动作？
- 每一段是不是只承担一个主要任务？
- 转折词是不是必要？
- 语气是不是符合使用场景？
- 能不能删掉 10%–20% 的词而不损失信息？
- 最后一段有没有提供新信息，而不是重复开头？

如果删掉以后意思一样，就删。

## 19. 默认风格

除非用户另有要求，默认：简洁但不生硬；专业但不官腔；技术上准确；证据优先；结论克制；句子有自然长短变化；少修辞；少元叙述；不强行拔高；不故意显得聪明；使用用户当前语言；延续用户已有术语和表达习惯。

最终目标是让读者感觉作者真的理解这件事，所以不需要靠复杂措辞来显得专业。
