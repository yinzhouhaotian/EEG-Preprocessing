# 第9章：源定位与模型检查

> 类型：既有英文笔记的重写校订与新增学习说明；非官方网页逐段译本。核对日期：2026-10-16。
> [对应原文入口](https://eeglab.org/tutorials/09_source/) · [覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

Source estimation requires a forward model and additional assumptions. Equivalent dipoles and distributed models answer different modeling questions. A small fitting residual is not a general certificate of a clean brain component or accurate anatomical localization.

## 对应中文译释

源估计需要正向模型及额外假设。等效偶极子和分布式模型回答不同的建模问题。较小拟合残差不是成分纯脑源或解剖定位准确的通用证明。

## 学习要点与补充入口

检查头模、电极坐标、单位及配准图。不要把头容积导体模型文件当作源空间网格，也不应套用固定旋转矩阵。源定位不是所有预处理的必做步骤。不同模型及原文页面见[进阶地图](Advanced_Topics_Map.md)。

完整概念讲解见[学习指南](../Learning_Guide/09_Pipeline_and_Quality_Control.md)。配套代码的实际验证状态见[代码说明](../03_MATLAB_Scripts/README.md)。
