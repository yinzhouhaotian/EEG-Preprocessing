# 来源版本与覆盖状态

核对日期：2026-10-16。原仓库基线：`44fad22f51ca34ce7622f518ae60639a7a6a9042`。

本轮按用户确认的范围完成已有文档修订与新增学习讲解。**未宣称完成两套网页全文逐段翻译。** 下列原文链接有些仅提供导航；读到目录条目不代表对应正文已经翻译。

## 已新增的实质学习内容

[学习指南](../Learning_Guide/00_Start_Here.md)覆盖记录、采样、频谱、事件、参考、插值、有效秩、滤波、降采样、伪迹、自动清理、分解、成分判读、分段、两类基线、时频、统计解释、流程选择与质量检查，并提供人工图示和练习。

官方教程新增事件、参考、重采样、目视坏导、目视坏段与波形/频谱专页，进阶主题通过独立地图说明。Makoto主要主题已重写校订，第18部分增加导航。

## 原文结构与后续工作

| 来源部分 | 当前状态 | 后续全文工作 |
|---|---|---|
| Makoto主要主题及子节 | 校订说明、译释及学习链接 | 原文各段、图注、代码与脚注尚未逐段译入 |
| Makoto额外专题 | 第18部分有独立导航 | 额外专题全文待授权或用户提供原文后处理 |
| 官方第1至11章 | 主题笔记、基础补充与全目录导航 | 各子页面全文尚未逐段译入 |
| 官方概念指南 | 有原文导航，部分知识纳入原创教学 | 完整原文翻译未完成 |
| 插件资料 | 条件与限制说明、来源链接 | 不视为基础必做步骤或全文译本 |
| 代码示例 | 保留并明确未运行验证 | 需在目标工具版本和示例数据上实际核对 |

## 版本记录

- 官方文档来源仓库提交：`24cf578d851d0142f296a976df3625c3b4301ce8`。网站快照与仓库提交不保证逐文件完全同步；实际核对依据包括此次网页内容。
- Makoto网页修订标识：`36694`；网页显示最后编辑日期2026-09-17。
- 逐页下载日期、重定向、状态及内容校验值见[source_manifest.json](source_manifest.json)。仅保存元数据，不批量发布原文正文或图像。
- 未核实适用于两套网页全文翻译再发布的公开许可；不把软件许可证自动套到网页文档。

## 逐页原文入口

以下为来源导航清单，不表示全文翻译完成。非200状态需要单独核验，不能记作链接已正常通过。

| 原文页面 | 获取状态 | 本轮用途 |
|---|---|---|
| [1. Installing EEGLAB ](https://eeglab.org/tutorials/01_Install/Install.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [2. Quickstart ](https://eeglab.org/tutorials/02_Quickstart/quickstart.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [3. Dataset management ](https://eeglab.org/tutorials/03_Dataset_management/datasets.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [4. Import data ](https://eeglab.org/tutorials/04_Import/Import.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [a. Continuous data ](https://eeglab.org/tutorials/04_Import/Importing_Continuous_and_Epoched_Data.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [b. Events ](https://eeglab.org/tutorials/04_Import/Importing_Event_Epoch_Info.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [c. Importing channel locations ](https://eeglab.org/tutorials/04_Import/Channel_Locations.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [d. Brain Imaging Data Structure data ](https://eeglab.org/tutorials/04_Import/BIDS.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [5. Preprocess data ](https://eeglab.org/tutorials/05_Preprocess/) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [a. Filtering ](https://eeglab.org/tutorials/05_Preprocess/Filtering.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [b. Re-referencing ](https://eeglab.org/tutorials/05_Preprocess/rereferencing.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [c. Resampling ](https://eeglab.org/tutorials/05_Preprocess/resampling.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [6. Reject artifacts ](https://eeglab.org/tutorials/06_RejectArtifacts/) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [a. Remove bad channels by visual inspection ](https://eeglab.org/tutorials/06_RejectArtifacts/Channel_rejection.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [b. Remove bad data by visual inspection ](https://eeglab.org/tutorials/06_RejectArtifacts/Scrolling_data.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [c. Automated artifact rejection ](https://eeglab.org/tutorials/06_RejectArtifacts/cleanrawdata.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [d. Independent Component Analysis ](https://eeglab.org/tutorials/06_RejectArtifacts/RunICA.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [7. Extract Data Epochs ](https://eeglab.org/tutorials/07_Extract_epochs/Extracting_Data_Epochs.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [8. Plot data ](https://eeglab.org/tutorials/08_Plot_data/) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [a. Event Related Potentials ](https://eeglab.org/tutorials/08_Plot_data/Data_Averaging.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [b. ERP-image ](https://eeglab.org/tutorials/08_Plot_data/Plotting_ERP_images.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [c. Spectra ](https://eeglab.org/tutorials/08_Plot_data/Plotting_Channel_Spectra_and_Maps.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [d. Time-Frequency decompositions ](https://eeglab.org/tutorials/08_Plot_data/Time-Frequency_decomposition.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [e. ICA components ](https://eeglab.org/tutorials/08_Plot_data/Plotting_ICA_components.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [9. Source analysis ](https://eeglab.org/tutorials/09_source/) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [a. Head model settings ](https://eeglab.org/tutorials/09_source/Model_Settings.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [b. ICA equivalent dipole sources ](https://eeglab.org/tutorials/09_source/DIPFIT.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [c. EEG source model ](https://eeglab.org/tutorials/09_source/EEG_sources.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [d. Using a custom head model ](https://eeglab.org/tutorials/09_source/Custom_head_model.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [10. Group analysis ](https://eeglab.org/tutorials/10_Group_analysis/) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [a. Batch processing for groups of subjects ](https://eeglab.org/tutorials/10_Group_analysis/multiple_subject_proccessing_overview.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [b. How to create and EEGLAB STUDY ](https://eeglab.org/tutorials/10_Group_analysis/study_creation.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [c. STUDY designs ](https://eeglab.org/tutorials/10_Group_analysis/working_with_study_designs.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [d. STUDY visualization and plots ](https://eeglab.org/tutorials/10_Group_analysis/study_data_visualization_tools.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [e. STUDY statistics ](https://eeglab.org/tutorials/10_Group_analysis/study_statistics.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [f. ICA clusters in EEGLAB studies ](https://eeglab.org/tutorials/10_Group_analysis/component_clustering_tools.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [e. Advanced statistics ](https://eeglab.org/tutorials/10_Group_analysis/advanced_statistics.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [g. Custom measures ](https://eeglab.org/tutorials/10_Group_analysis/custom_measures.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [11. Write scripts ](https://eeglab.org/tutorials/11_Scripting/) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [a. Using EEGLAB history ](https://eeglab.org/tutorials/11_Scripting/Using_EEGLAB_history.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [b. Event Processing ](https://eeglab.org/tutorials/11_Scripting/Event_Processing_command_line.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [c. Group-level analysis ](https://eeglab.org/tutorials/11_Scripting/command_line_study_functions.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [d. Scripts for advanced plots ](https://eeglab.org/tutorials/11_Scripting/EEG_scalp_measures.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [e. Automated pipeline ](https://eeglab.org/tutorials/11_Scripting/automated_pipeline.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [e. BIDS pipeline ](https://eeglab.org/tutorials/11_Scripting/Analyzing_EEG_BIDS_data_in_EEGLAB.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [Concepts guide ](https://eeglab.org/tutorials/ConceptsGuide/) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [Setting up your lab ](https://eeglab.org/tutorials/ConceptsGuide/Setting_up_your_EEG_lab.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [EEGLAB data structures ](https://eeglab.org/tutorials/ConceptsGuide/Data_Structures.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [Coordinate systems ](https://eeglab.org/tutorials/ConceptsGuide/coordinateSystem.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [EEGLAB functions ](https://eeglab.org/tutorials/ConceptsGuide/EEGLAB_functions.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [How to construct ERP images ](https://eeglab.org/tutorials/ConceptsGuide/erp_image_background.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [Independent Component Analysis of EEG data ](https://eeglab.org/tutorials/ConceptsGuide/ICA_background.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [Learning EEG ](https://eeglab.org/tutorials/ConceptsGuide/LearningEEG.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [Re-referencing EEG data ](https://eeglab.org/tutorials/ConceptsGuide/rereferencing_background.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [Spectral analysis and time-frequency decompositions ](https://eeglab.org/tutorials/ConceptsGuide/Time_frequency_tutorial.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [Statistics ](https://eeglab.org/tutorials/ConceptsGuide/statistics_theory.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [Makoto pipeline ](https://eeglab.ucsd.edu/wiki/Makoto%27s_preprocessing_pipeline) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [Filtering FAQ ](https://eeglab.org/others/Firfilt_FAQ.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [Clean rawdata plugin ](https://eeglab.org/plugins/clean_rawdata/) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [ROIconnect ](https://eeglab.org/plugins/roiconnect/) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [Preprocessing overview ](https://mne.tools/stable/auto_tutorials/preprocessing/index.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [Filtering and resampling ](https://mne.tools/stable/auto_tutorials/preprocessing/30_filtering_resampling.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [ICA correction ](https://mne.tools/stable/auto_tutorials/preprocessing/40_artifact_correction_ica.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [Regression baseline ](https://mne.tools/stable/auto_tutorials/epochs/15_baseline_regression.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [Bad channels ](https://mne.tools/stable/auto_tutorials/preprocessing/15_handling_bad_channels.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [Filter background ](https://mne.tools/stable/auto_tutorials/preprocessing/25_background_filtering.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [Filter design paper metadata ](https://pubmed.ncbi.nlm.nih.gov/25128257/) | 203 | 原文导航、版本核对或知识参考；非全文译本 |
| [Tutorial data ](https://eeglab.org/tutorials/tutorial_data.html) | 200 | 原文导航、版本核对或知识参考；非全文译本 |
| [Official tutorial index](https://eeglab.org/tutorials/) | 200 | 新增方法参考；非全文译本 |
| [14_quality_control_report.html](https://mne.tools/stable/auto_tutorials/preprocessing/14_quality_control_report.html) | 200 | 新增方法参考；非全文译本 |
| [35_artifact_correction_regression.html](https://mne.tools/stable/auto_tutorials/preprocessing/35_artifact_correction_regression.html) | 200 | 新增方法参考；非全文译本 |
| [50_artifact_correction_ssp.html](https://mne.tools/stable/auto_tutorials/preprocessing/50_artifact_correction_ssp.html) | 200 | 新增方法参考；非全文译本 |
| [mne.preprocessing.compute_current_source_density.html](https://mne.tools/stable/generated/mne.preprocessing.compute_current_source_density.html) | 200 | 新增方法参考；非全文译本 |

新增选读：[其他方法与特殊情形](../Learning_Guide/11_Optional_Methods_and_Special_Cases.md)，涵盖回归、投影、去趋势、回归式基线和表面空间变换。
