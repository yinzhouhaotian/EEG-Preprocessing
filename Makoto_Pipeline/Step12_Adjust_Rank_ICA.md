# Step 12：分解成分数与有效秩

> 类型：对用户提供的既有笔记进行重写校订；英文为校订说明，中文为对应译释，均非网页逐字引文。新增学习要点另列。核对日期：2026-10-16。
> 来源：[Makoto原文](https://eeglab.ucsd.edu/wiki/Makoto%27s_preprocessing_pipeline)；原文为个人建议。[覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

The number of independent dimensions available to ICA is bounded by data rank. Referencing, interpolation, bridged channels and component removal can affect it. Numerical estimates depend on units, scaling and tolerance; a fixed covariance-eigenvalue threshold is not universal.

## 对应中文译释

独立成分可用的独立维度受数据秩限制。参考、插值、桥接与去成分都可能影响它。数值估计依赖单位、缩放和容差；固定协方差特征值阈值不是通用标准。

## 学习要点与适用限制

把微伏改成伏后，协方差特征值缩小一万亿倍。先查看奇异值谱，并结合已知线性约束判断。数学秩、计算函数给出的数值秩和适合实际分解的有效维度应区分。不要只减1就以为已处理所有维度损失，也不要把每项估计损失不加检查地相加。

## 进一步学习

阅读[原理、例子与检查方法](../Learning_Guide/03_Reference_Interpolation_Rank.md)。这里的说明不是一条可直接运行的通用管线；代码状态见[示例说明](../03_MATLAB_Scripts/README.md)。
