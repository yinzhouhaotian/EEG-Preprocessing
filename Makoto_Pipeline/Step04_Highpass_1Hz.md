# Step 4：高通与分解训练副本

> 类型：对用户提供的既有笔记进行重写校订；英文为校订说明，中文为对应译释，均非网页逐字引文。新增学习要点另列。核对日期：2026-10-16。
> 来源：[Makoto原文](https://eeglab.ucsd.edu/wiki/Makoto%27s_preprocessing_pipeline)；原文为个人建议。[覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

High-pass filtering can reduce slow drifts that interfere with decomposition. A training cutoff or passband edge is not automatically the final analysis setting. If weights are transferred between copies, their channel order, reference, scale and spatial preprocessing must remain compatible.

## 对应中文译释

高通可以衰减干扰分解的慢漂移。训练数据采用的截止点或通带边缘，并不自动适合作为最终分析设置。若在数据副本之间迁移权重，通道顺序、参考、缩放与空间处理必须兼容。

## 学习要点与适用限制

先分清通带边缘与截止点的定义。1赫兹在某种默认设计中对应另一数值的半幅截止点，不代表所有滤波器都有同一关系。非周期背景近似幂律，不是指数函数；较低频率并非天然无用。慢电位与有向连接尤其需要检查滤波影响。权重迁移到训练时未包含的低频时，也不能保证这些频率仍满足同样的独立分离。

## 进一步学习

阅读[原理、例子与检查方法](../Learning_Guide/04_Filtering_and_Resampling.md)。这里的说明不是一条可直接运行的通用管线；代码状态见[示例说明](../03_MATLAB_Scripts/README.md)。
