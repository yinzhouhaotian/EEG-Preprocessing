# Step 13：拟合、判读与迁移分解

> 类型：对用户提供的既有笔记进行重写校订；英文为校订说明，中文为对应译释，均非网页逐字引文。新增学习要点另列。核对日期：2026-10-16。
> 来源：[Makoto原文](https://eeglab.ucsd.edu/wiki/Makoto%27s_preprocessing_pipeline)；原文为个人建议。[覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

ICA estimates a statistical separation under a mixing model. Quality depends on representative data, stable spatial relationships, dimensions and optimization. Removing a component changes the retained information; refitting cannot restore what was discarded and need not return identical components.

## 对应中文译释

独立成分分析在混合模型下估计统计分离。质量取决于代表性数据、稳定空间关系、维度和优化。删除成分改变保留信息；再次拟合不能恢复被删信息，也不保证得到完全相同的其他成分。

## 学习要点与适用限制

本页原有英文被压缩为若干规则，不能冒充原文10个子节的逐字译文。完整学习包括最小数据量的经验性质、空间混合假设、输入通道、成分判读、迁移一致性和失败诊断。成分投影是线性操作，但删除错误成分仍会改变目标波形、频谱和相位；不保证恢复未知真实神经相位。

## 进一步学习

阅读[原理、例子与检查方法](../Learning_Guide/06_ICA_and_Component_Review.md)。这里的说明不是一条可直接运行的通用管线；代码状态见[示例说明](../03_MATLAB_Scripts/README.md)。
