# 第1–4章：安装、数据管理与导入

> 类型：既有英文笔记的重写校订与新增学习说明；非官方网页逐段译本。核对日期：2026-10-16。
> [对应原文入口](https://eeglab.org/tutorials/04_Import/Import.html) · [覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

Importing a file is only the beginning of data verification. Check dimensions, units, sampling rate, channel types, reference and event timing before analysis. Preserve the original recording and identify which dataset is currently active.

## 对应中文译释

导入文件只是数据验证的开始。分析前应检查维度、单位、采样率、通道类型、参考及事件时间。保留原始记录，并明确当前激活的是哪个数据集。

## 学习要点与补充入口

先用官方示例熟悉加载、保存和切换，再学习自己的采集格式。`EEG` 与 `ALLEEG` 表示当前数据和数据集集合，批处理时不要混淆。模板位置匹配与个体电极实测是不同精度的输入。事件单独见[补充页](Ch04_Events_and_Timing.md)。

完整概念讲解见[学习指南](../Learning_Guide/02_Events_and_Data_Checks.md)。配套代码的实际验证状态见[代码说明](../03_MATLAB_Scripts/README.md)。
