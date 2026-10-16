# 连接插件：源空间分析的前提与限制

> 类型：既有英文笔记的重写校订与新增学习说明；非官方网页逐段译本。核对日期：2026-10-16。
> [对应原文入口](https://eeglab.org/plugins/roiconnect/) · [覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

Source-level connectivity can reduce some sensor-mixing problems but remains sensitive to source leakage, model assumptions and data length. Equal-duration snippet analysis is distinct from event epoching and must be configured explicitly. No metric guarantees removal of all spurious connections.

## 对应中文译释

源空间连接分析可以减少部分传感器混合问题，但仍受源泄漏、模型假设和数据长度影响。等时长片段分析不同于事件分段，需要明确设置。任何指标都不保证移除全部伪连接。

## 学习要点与补充入口

插件文档说明了所验证的情境；约100赫兹和两秒片段属于所述工作流，不能推广成所有源分析的统一要求。`snippet`默认关闭时，不会仅因给出片段长度就自动启用。确认导联场、图谱、模型和插件版本；原有代码仅作待核验示例。

完整概念讲解见[学习指南](../Learning_Guide/08_Power_TimeFrequency_and_Inference.md)。配套代码的实际验证状态见[代码说明](../03_MATLAB_Scripts/README.md)。
