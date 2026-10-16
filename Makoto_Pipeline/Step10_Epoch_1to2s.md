# Step 10：分段窗口、边缘与基线

> 类型：对用户提供的既有笔记进行重写校订；英文为校订说明，中文为对应译释，均非网页逐字引文。新增学习要点另列。核对日期：2026-10-16。
> 来源：[Makoto原文](https://eeglab.ucsd.edu/wiki/Makoto%27s_preprocessing_pipeline)；原文为个人建议。[覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

Epoch duration should cover the scientific time range and the support of the analysis kernel. Three cycles at three hertz span one second in the idealized calculation. Software-specific window lengths require their own explanation. Avoid short per-epoch baseline subtraction before fitting ICA.

## 对应中文译释

分段长度应覆盖科学问题的时间范围及分析核所需数据。理想计算中，3赫兹的3个周期持续1秒。软件特定窗口长度需要另行解释。拟合独立成分前通常避免逐试次短基线相减。

## 学习要点与适用限制

原来的负1到正2秒只是示例。不要把约半秒的边缘缓冲套给所有频率与周期数。高通不保证每个短片段均值为零；不在拟合前减短基线的理由，应从其对试次偏移与模型的影响理解。若训练包含重叠试次，要考虑重复样本权重。

## 进一步学习

阅读[原理、例子与检查方法](../Learning_Guide/07_Epochs_and_Baselines.md)。这里的说明不是一条可直接运行的通用管线；代码状态见[示例说明](../03_MATLAB_Scripts/README.md)。
