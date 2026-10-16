# 第6章：目视检查、自动清理与分解

> 类型：既有英文笔记的重写校订与新增学习说明；非官方网页逐段译本。核对日期：2026-10-16。
> [对应原文入口](https://eeglab.org/tutorials/06_RejectArtifacts/) · [覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

Artifact handling starts with inspecting data, not with choosing an automatic threshold. Automated rejection, reconstruction and ICA remove or estimate different kinds of information. Review their outputs, known assumptions and failure cases before combining them.

## 对应中文译释

伪迹处理从检查数据开始，而不是从选择自动阈值开始。自动删除、重构和独立成分分析删除或估计的是不同信息。组合方法前应审查输出、已知假设和失败情形。

## 学习要点与补充入口

新增[坏通道检查](Ch06a_Visual_Bad_Channels.md)和[坏时间段检查](Ch06b_Visual_Bad_Segments.md)。自动清理需说明各阶段开关，修复与保留时间轴不等于保留全部信息。分解要匹配有效维度，成分判读综合地形、时间、频谱和辅助记录。短试次基线通常放在拟合之后；变更参考必须与模型一致，不能只改通道数据。

完整概念讲解见[学习指南](../Learning_Guide/06_ICA_and_Component_Review.md)。配套代码的实际验证状态见[代码说明](../03_MATLAB_Scripts/README.md)。
