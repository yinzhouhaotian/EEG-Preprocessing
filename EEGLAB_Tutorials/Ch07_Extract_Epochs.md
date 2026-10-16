# 第7章：提取分段、选择试次与基线

> 类型：既有英文笔记的重写校订与新增学习说明；非官方网页逐段译本。核对日期：2026-10-16。
> [对应原文入口](https://eeglab.org/tutorials/07_Extract_epochs/Extracting_Data_Epochs.html) · [覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

Epochs align data to events or fixed windows. Their duration depends on the scientific interval, analysis support and edge handling. Baseline subtraction changes an offset; it is not a universal drift correction. Verify retained events and trials after every selection.

## 对应中文译释

分段把数据对齐到事件或固定窗口。长度取决于科学问题的区间、分析所需数据及边缘处理。基线相减改变偏移，不是通用去漂移方法。每次选择后都应核对保留事件和试次。

## 学习要点与补充入口

三秒窗口只是示例。按事件元数据选择时，区分“只保留事件”与“删除不含该事件的试次”等不同选项。试次索引在删除后改变，应保留来源映射。时域电位基线与功率基线不是同一步。

完整概念讲解见[学习指南](../Learning_Guide/07_Epochs_and_Baselines.md)。配套代码的实际验证状态见[代码说明](../03_MATLAB_Scripts/README.md)。
