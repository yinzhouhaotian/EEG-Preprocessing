# 第10–11章：群组设计与脚本化

> 类型：既有英文笔记的重写校订与新增学习说明；非官方网页逐段译本。核对日期：2026-10-16。
> [对应原文入口](https://eeglab.org/tutorials/11_Scripting/automated_pipeline.html) · [覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

An automated pipeline is an example of a specified workflow, not a universal analysis standard. Group design, subject pairing, condition labels and data quantity need explicit verification. A successful function call does not validate scientific assumptions.

## 对应中文译释

自动管线是对特定工作流的示例，不是通用分析标准。群组设计、被试配对、条件标签及数据量需要明确验证。函数调用成功不验证科学假设。

## 学习要点与补充入口

保留操作历史，核对函数对数据集数组的支持，再开展批处理。成分移除和插值可在不同层面完成，但要检查具体实现。群组统计、设计、聚类、事件脚本和自动管线的完整原文入口见[进阶地图](Advanced_Topics_Map.md)，不能用一段改编脚本替代所有章节。

完整概念讲解见[学习指南](../Learning_Guide/09_Pipeline_and_Quality_Control.md)。配套代码的实际验证状态见[代码说明](../03_MATLAB_Scripts/README.md)。
