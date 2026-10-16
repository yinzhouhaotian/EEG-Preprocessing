# 第5章：滤波、参考与重采样

> 类型：既有英文笔记的重写校订与新增学习说明；非官方网页逐段译本。核对日期：2026-10-16。
> [对应原文入口](https://eeglab.org/tutorials/05_Preprocess/) · [覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

Preprocessing choices should follow the target bandwidth, timing requirements and downstream model. Separate high- and low-pass designs can provide independent transition-band control, but band-pass filtering is not inherently invalid. Reference and resampling choices also change the data representation.

## 对应中文译释

预处理选择应服从目标带宽、时间要求和后续模型。分别设计高通和低通可独立控制过渡带，但带通滤波并非天然无效。参考与重采样也会改变数据表示。

## 学习要点与补充入口

通常优先对连续数据滤波，但合理处理边缘的分段滤波并非绝对禁止。截止点定义要看软件；重参考不产生绝对电位。Huber均值不宜在独立成分分析之前使用。降采样要保证抗混叠并核对事件。见[参考专页](Ch05b_References.md)和[降采样专页](Ch05c_Resampling.md)。

完整概念讲解见[学习指南](../Learning_Guide/04_Filtering_and_Resampling.md)。配套代码的实际验证状态见[代码说明](../03_MATLAB_Scripts/README.md)。
