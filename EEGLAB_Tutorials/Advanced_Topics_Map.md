# 进阶内容地图：知道何时需要，再深入学习

> 新增学习导航；不是这些原文页面的全文翻译。入门主线见[从零开始](../Learning_Guide/00_Start_Here.md)。

## 源定位

头皮信号到脑源不是唯一可解的逆问题，需要头模型、电极配准、导电性等假设。单等效偶极子与分布式源模型提出的约束不同，不能把相近的头皮图直接当成同一脑区。

拟合残差较小只说明某个模型能较好解释所用空间分布；不能单凭残差证明成分纯粹来自脑内。检查电极坐标单位、左右方向、头模配准及异常深部估计，并保留实际配准图。

原文：[头模设置](https://eeglab.org/tutorials/09_source/Model_Settings.html)、[偶极子拟合](https://eeglab.org/tutorials/09_source/DIPFIT.html)、[源模型](https://eeglab.org/tutorials/09_source/EEG_sources.html)、[自定义头模](https://eeglab.org/tutorials/09_source/Custom_head_model.html)。

## 群组与实验设计

群组数据结构组织被试、条件和会话。先确认比较单位、配对关系、缺失条件和重复测量，再进行绘图与检验。不能把同一人的许多试次当成许多独立被试。

对独立成分聚类后比较条件，需要避免用同一待检验效应同时选择聚类和检验。空间信息、预定义区域或独立数据选区等方案，也要根据实际统计问题检查独立性。

原文：[创建群组](https://eeglab.org/tutorials/10_Group_analysis/study_creation.html)、[实验设计](https://eeglab.org/tutorials/10_Group_analysis/working_with_study_designs.html)、[统计](https://eeglab.org/tutorials/10_Group_analysis/study_statistics.html)、[成分聚类](https://eeglab.org/tutorials/10_Group_analysis/component_clustering_tools.html)、[高级统计](https://eeglab.org/tutorials/10_Group_analysis/advanced_statistics.html)。

## 脚本化

先用示例数据理解一次操作，再查看操作历史和函数参数。脚本需要明确输入、输出、通道、单位、参数及版本，而不是简单把界面命令堆叠。

批处理前先对一个代表性数据集做完整人工检查，再检查不同条件与质量范围的数据。函数正常返回不等于数据含义、事件对应或科学假设正确。

原文：[操作历史](https://eeglab.org/tutorials/11_Scripting/Using_EEGLAB_history.html)、[事件处理](https://eeglab.org/tutorials/11_Scripting/Event_Processing_command_line.html)、[群组脚本](https://eeglab.org/tutorials/11_Scripting/command_line_study_functions.html)、[自动管线](https://eeglab.org/tutorials/11_Scripting/automated_pipeline.html)。

## 功能连接

先选择问题与估计对象：头皮通道还是源时间序列、无向还是有向、频域还是时间域。共同参考与空间混合可能产生关联；源重建也会产生泄漏和模型误差。

自回归建模要检查模型阶数、有效样本、平稳性、稳定性与残差。滤波会改变频谱复杂度和估计行为；某些理论不变性不意味着有限样本实现不受影响。“用因果滤波”或“只做某个高通”都不是所有连接分析的统一答案。

对数据量敏感的指标，应采用可比的有效时长和估计方案。时间反转等方法可以帮助诊断或减少部分偏差，不保证排除全部混杂。

原文：[滤波与因果分析问答](https://eeglab.org/others/Firfilt_FAQ.html)、[源空间连接插件](https://eeglab.org/plugins/roiconnect/)。

## Makoto额外专题

原文的额外专题可作为按问题查阅的扩展资料，其中含个人推断、历史讨论与引用文献。目录覆盖位置见[来源与覆盖清单](../docs/COVERAGE.md)。本轮不把这些讨论伪装为已验证的统一理论，也不把它们作为常规预处理的必做步骤。
