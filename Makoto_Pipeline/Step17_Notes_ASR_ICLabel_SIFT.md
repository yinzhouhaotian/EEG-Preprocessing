# Step 17：自动清理、标签与连接性扩展

> 类型：对用户提供的既有笔记进行重写校订；英文为校订说明，中文为对应译释，均非网页逐字引文。新增学习要点另列。核对日期：2026-10-16。
> 来源：[Makoto原文](https://eeglab.ucsd.edu/wiki/Makoto%27s_preprocessing_pipeline)；原文为个人建议。[覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

Automated cleaning and component labeling make decisions reproducible only when inputs, parameters and versions are recorded. Thresholds and component-selection strategies have different information-loss tradeoffs. Connectivity analysis introduces additional assumptions beyond ordinary artifact reduction.

## 对应中文译释

自动清理与成分标签只有在输入、参数和版本被记录时才有助于复现。不同阈值及成分选择策略具有不同的信息损失权衡。连接性分析还引入普通去伪迹之外的假设。

## 学习要点与适用限制

分别学习校准数据、重构与删除、最终窗口拒绝、自动类别概率和人工核对。只保留高概率脑成分与只删除明确伪迹不是同一策略。连接性要考虑参考、容积传导、源泄漏、滤波、有效数据量及模型稳定性。1赫兹高通、100赫兹降采样或某个概率阈值都不是所有连接分析的固定答案。更多原文分支见覆盖清单。

## 进一步学习

阅读[原理、例子与检查方法](../Learning_Guide/05_Artifacts_and_ASR.md)。这里的说明不是一条可直接运行的通用管线；代码状态见[示例说明](../03_MATLAB_Scripts/README.md)。
