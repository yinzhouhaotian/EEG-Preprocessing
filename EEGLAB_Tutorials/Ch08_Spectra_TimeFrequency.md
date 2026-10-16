# 第8章：频谱、功率与时频

> 类型：既有英文笔记的重写校订与新增学习说明；非官方网页逐段译本。核对日期：2026-10-16。
> [对应原文入口](https://eeglab.org/tutorials/08_Plot_data/Time-Frequency_decomposition.html) · [覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

Power and phase consistency describe different aspects of data. A significant power effect with nonsignificant phase locking does not establish the complete absence of phase locking. Window duration, cycle count, baseline definition and multiple comparisons all affect interpretation.

## 对应中文译释

功率和相位一致性描述数据的不同方面。功率效应显著而相位锁定不显著，并不能证明完全不存在相位锁定。窗长、周期数、基线定义与多重比较都会影响解释。

## 学习要点与补充入口

补充[平均波形、试次图、频谱与成分显示](Ch08a_Waveforms_Images_and_Spectra.md)。实际最低频率需检查分析核和返回频率，不能只靠延长片段保证。零填充让频率坐标更密，不增加独立信息。单被试图中的显著性也不替代群组条件差异检验。

完整概念讲解见[学习指南](../Learning_Guide/08_Power_TimeFrequency_and_Inference.md)。配套代码的实际验证状态见[代码说明](../03_MATLAB_Scripts/README.md)。
