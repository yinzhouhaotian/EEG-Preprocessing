# Step 16：群组结构与避免循环推断

> 类型：对用户提供的既有笔记进行重写校订；英文为校订说明，中文为对应译释，均非网页逐字引文。新增学习要点另列。核对日期：2026-10-16。
> 来源：[Makoto原文](https://eeglab.ucsd.edu/wiki/Makoto%27s_preprocessing_pipeline)；原文为个人建议。[覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

Group analysis requires explicit subject, condition and session structure. Feature selection or clustering should not be optimized on the same effect later tested without accounting for that dependence. Dipole-location clustering is one proposed strategy, not the only possible independent definition.

## 对应中文译释

群组分析需要明确被试、条件和会话结构。特征选择或聚类不能在不处理依赖关系的情况下，根据同一个随后检验的效应进行优化。用偶极子位置聚类是一种建议，不是唯一可能的独立定义。

## 学习要点与适用限制

也可以根据预定义区域或独立数据安排选区，但其有效性要由实际设计判断。先确定统计独立单位、配对关系和缺失数据，再比较条件。时频参数、聚类数及来源定位应分别记录，不把群组结构本身当成质量保证。

## 进一步学习

阅读[原理、例子与检查方法](../Learning_Guide/08_Power_TimeFrequency_and_Inference.md)。这里的说明不是一条可直接运行的通用管线；代码状态见[示例说明](../03_MATLAB_Scripts/README.md)。
