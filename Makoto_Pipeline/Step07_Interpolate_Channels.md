# Step 7：插值的估计与维度限制

> 类型：对用户提供的既有笔记进行重写校订；英文为校订说明，中文为对应译释，均非网页逐字引文。新增学习要点另列。核对日期：2026-10-16。
> 来源：[Makoto原文](https://eeglab.ucsd.edu/wiki/Makoto%27s_preprocessing_pipeline)；原文为个人建议。[覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

Interpolation estimates missing channel signals from available spatial information. With fixed geometry and parameters, it is a linear map of the good-channel signals and cannot create new independent measurements. The timing of interpolation must be coordinated with referencing and decomposition.

## 对应中文译释

插值根据可用空间信息估计缺失通道。固定位置和参数后，它是好通道信号的线性映射，不能创造新的独立测量。插值时机需要与参考和分解共同安排。

## 学习要点与适用限制

球面样条的空间核并非对坐标的简单线性函数，但不能因此把它说成对电压值的非线性运算。有限精度可能影响数值有效秩。大面积集中缺失尤其难恢复；记录插值清单，避免把虚拟通道当成新增独立网络节点。分解前与分解后插值各有实现前提，不设统一必需时机。

## 进一步学习

阅读[原理、例子与检查方法](../Learning_Guide/03_Reference_Interpolation_Rank.md)。这里的说明不是一条可直接运行的通用管线；代码状态见[示例说明](../03_MATLAB_Scripts/README.md)。
