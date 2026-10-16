# Step 8：平均参考、原参考与秩

> 类型：对用户提供的既有笔记进行重写校订；英文为校订说明，中文为对应译释，均非网页逐字引文。新增学习要点另列。核对日期：2026-10-16。
> 来源：[Makoto原文](https://eeglab.ucsd.edu/wiki/Makoto%27s_preprocessing_pipeline)；原文为个人建议。[覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

An arithmetic average reference defines potentials relative to the selected channel mean. It imposes a zero-sum constraint on those channels. Restoring a genuinely omitted initial reference is a distinct operation and cannot recover rank already lost through other processing.

## 对应中文译释

算术平均参考将电位定义为相对于所选通道的均值，并使这些通道满足和为零的约束。补回确实被省略的初始参考是另一项操作，不能恢复其他处理已经损失的秩。

## 学习要点与适用限制

普通平均参考是一种可用定义，并不因产生一维线性约束就自动“错误”。若确实需要将原始物理参考纳入通道集合，应知道该参考是否已保留及其位置。不要任意追加零通道，也不要保证任何数据经过补零都会满秩。后续算法应匹配真实可用维度；参考方案要与记录布局和研究目的一致。

## 进一步学习

阅读[原理、例子与检查方法](../Learning_Guide/03_Reference_Interpolation_Rank.md)。这里的说明不是一条可直接运行的通用管线；代码状态见[示例说明](../03_MATLAB_Scripts/README.md)。
