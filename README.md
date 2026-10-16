# 脑电预处理：从原理到判断的中文学习资料

面向从零入门：理解每种方法解决什么问题、依赖什么假设、改变什么信号，以及怎样检查效果。脑电（Electroencephalography，EEG）的处理流程应围绕研究目标选择。

**当前定位：既有英文笔记校订＋新增中文讲解＋原文导航。** 本仓库不是两套网上教程的完整逐段译本。2026-10-16修订已纠正原有确定错误、补充基础学习说明；全文翻译范围与未完成项见[覆盖清单](docs/COVERAGE.md)。

## 建议从这里开始

1. [学习顺序与目标](Learning_Guide/00_Start_Here.md)
2. [信号、采样与频谱](Learning_Guide/01_Signal_Sampling_Spectrum.md)
3. [事件、单位与原始数据检查](Learning_Guide/02_Events_and_Data_Checks.md)
4. [参考、插值和矩阵秩](Learning_Guide/03_Reference_Interpolation_Rank.md)
5. [滤波与降采样](Learning_Guide/04_Filtering_and_Resampling.md)
6. [坏通道、坏段与自动清理](Learning_Guide/05_Artifacts_and_ASR.md)
7. [独立成分分析与成分判读](Learning_Guide/06_ICA_and_Component_Review.md)
8. [分段与基线](Learning_Guide/07_Epochs_and_Baselines.md)
9. [功率、时频与统计解释](Learning_Guide/08_Power_TimeFrequency_and_Inference.md)
10. [流程选择与质量检查](Learning_Guide/09_Pipeline_and_Quality_Control.md)
11. [练习与参考解答](Learning_Guide/10_Exercises.md)

选读：[回归、投影、去趋势与特殊采集情形](Learning_Guide/11_Optional_Methods_and_Special_Cases.md)。

每章围绕目的、原理、效果、条件、失败场景和检查方法展开。图示使用人工模拟信号，不代替真实数据判读练习。

## 两套资料与补充页

- [Makoto笔记的校订版](Makoto_Pipeline/00_Disclaimer_and_TOC.md)：保留个人建议的性质和历史状态。
- [官方教程对应笔记与补充讲解](EEGLAB_Tutorials/00_Overview_and_Navigation.md)：含新增事件、重参考、降采样、目视检查、波形与频谱专页。
- [源定位、群组、脚本与连接性进阶地图](EEGLAB_Tutorials/Advanced_Topics_Map.md)：建立后续学习入口。
- [两种工作流怎样比较](EEGLAB_Tutorials/Appendix_Comparison_Official_vs_Makoto.md)。

## 查阅与复现

- [术语全称](docs/GLOSSARY.md)
- [来源、版本与覆盖状态](docs/COVERAGE.md)
- [本轮修正记录](docs/REVISION_NOTES.md)
- [内容类型与后续翻译规则](docs/EDITORIAL_POLICY.md)
- [配套代码的验证状态](03_MATLAB_Scripts/README.md)

`01_Makoto_Pipeline/` 与 `02_EEGLAB_Official_Tutorials/` 保留原路径，现作为分组导航；避免在多个目录维护同一正文。代码示例没有在目标 MATLAB 和插件环境运行验证，不宣称为可直接套用的通用管线。

原文：[Makoto’s preprocessing pipeline](https://eeglab.ucsd.edu/wiki/Makoto%27s_preprocessing_pipeline)、[官方教程总目录](https://eeglab.org/tutorials/)。原文作者保有其文字与图示的权利，本仓库不将公开可读等同于允许全文翻译再发布。
