# EEGLAB Official Tutorials 官方在线教程中英对照完整指南（附 GUI 路径与官方自动化脚本）

> **原文来源 (Official Source)**: [EEGLAB Official Online Tutorials - SCCN (Swartz Center for Computational Neuroscience, UCSD)](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F)
> **核心专题章节链接**: [5. Preprocess Data](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F05_Preprocess%2FFiltering.html) | [6. Reject Artifacts \& ICA](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F06_RejectArtifacts%2FRunICA.html) | [7. Extract Epochs](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F07_Extract_epochs%2FExtracting_Data_Epochs.html) | [8. Time-Frequency (ERSP/ITC)](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F08_Plot_data%2FTime-Frequency_decomposition.html) | [9. DIPFIT Source Localization](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F09_source%2FDIPFIT.html) | [10. Group STUDY Analysis](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F10_Group_analysis%2Fcomponent_clustering_tools.html) | [11. Automated Scripting](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F11_Scripting%2Fautomated_pipeline.html) | [ROIconnect Connectivity Plugin](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Fplugins%2Froiconnect%2F)
> **文档说明**: 本文档将 EEGLAB 官方在线教程（`eeglab.org/tutorials/`）全部 11 个核心模块及源空间功能连接插件（`ROIconnect` / `SIFT`）整理为**中英双语对照手册**，完整保留官方 GUI 菜单操作路径、算法原理说明及官方标准 MATLAB 批处理脚本，可直接作为 `EEGLAB_Official_Tutorials_CN_EN.md` 上传至你的 GitHub 仓库与《Makoto's Preprocessing Pipeline》配套使用。

> **章节拆分说明**: 本文件夹由 `README.md` 按章节拆分而来，每一章为独立 md 文件，便于单独查阅与版本管理。

## 章节导航 (Chapter Navigation)

| 章节文件 | 内容 |
| :--- | :--- |
| [00_Overview_and_Navigation.md](00_Overview_and_Navigation.md) | 官方教程全景架构与章节导航（本文件） |
| [Ch01-04_Data_Management_Import.md](Ch01-04_Data_Management_Import.md) | Ch 1–4 安装、快速入门与数据集管理、导入数据 |
| [Ch05_Preprocess_Data.md](Ch05_Preprocess_Data.md) | Ch 5 数据预处理（滤波、重参考、重采样） |
| [Ch06_Reject_Artifacts_ASR_ICA.md](Ch06_Reject_Artifacts_ASR_ICA.md) | Ch 6 伪迹剔除（clean_rawdata / ASR、ICA 与 ICLabel） |
| [Ch07_Extract_Epochs.md](Ch07_Extract_Epochs.md) | Ch 7 提取数据分段与基线校正 |
| [Ch08_Spectra_TimeFrequency.md](Ch08_Spectra_TimeFrequency.md) | Ch 8 数据可视化与时频分解（ERSP / ITC） |
| [Ch09_Source_Analysis_DIPFIT.md](Ch09_Source_Analysis_DIPFIT.md) | Ch 9 源定位分析（DIPFIT 与 eLORETA） |
| [Ch10-11_Group_STUDY_Automated_Pipeline.md](Ch10-11_Group_STUDY_Automated_Pipeline.md) | Ch 10–11 群组 STUDY 分析与官方全自动频谱脚本 |
| [Plugin_ROIconnect_Connectivity.md](Plugin_ROIconnect_Connectivity.md) | 源空间脑区功能连接（ROIconnect & SIFT） |
| [Appendix_Comparison_Official_vs_Makoto.md](Appendix_Comparison_Official_vs_Makoto.md) | 附：官方教程与 Makoto's Pipeline 核心异同速查表 |

## 官方教程全景架构与章节导航 (Overview of the 11 Tutorial Modules)

| 官方章节 | 英文标题 (English Title) | 中文标题 (Chinese Title) | GUI 菜单路径 / 核心 MATLAB 函数 |
| :--- | :--- | :--- | :--- |
| **Ch 1–3** | Installing, Quickstart & Dataset Management | 安装、快速入门与数据集管理 | `eeglab`, `ALLEEG`, `EEG`, `CURRENTSET`, `pop_editoptions` |
| **Ch 4** | Import Data (Continuous, Events, Locations, BIDS) | 导入数据（连续数据、事件、通道坐标与 BIDS） | `File -> Import data`, `Edit -> Channel locations` (`pop_chanedit`, `pop_importbids`) |
| **Ch 5** | Preprocess Data (Filtering, Re-referencing, Resampling) | 数据预处理（滤波、重参考、重采样） | `Tools -> Filter / Re-reference / Change sampling rate` (`pop_eegfiltnew`, `pop_reref`, `pop_resample`) |
| **Ch 6.a–c** | Reject Artifacts (Visual & `clean_rawdata` / ASR) | 伪迹剔除（目视检查与 `clean_rawdata` 自动清洗） | `Tools -> Reject data using Clean Rawdata and ASR` (`pop_clean_rawdata`, `clean_artifacts`) |
| **Ch 6.d** | Independent Component Analysis (ICA & `ICLabel`) | 独立成分分析去伪迹与 `ICLabel` 自动分类 | `Tools -> Decompose data by ICA`, `Classify components using ICLabel` (`pop_runica`, `pop_iclabel`, `pop_icflag`) |
| **Ch 7** | Extract Data Epochs & Remove Baseline | 提取数据分段与基线校正 | `Tools -> Extract epochs`, `Remove baseline` (`pop_epoch`, `pop_rmbase`, `pop_selectevent`) |
| **Ch 8** | Plot Data (ERPs, Spectra, ERSP & ITC Time-Frequency) | 数据可视化与时频分解（功率谱、ERSP 与 ITC） | `Plot -> Channel spectra and maps`, `Time-frequency transforms` (`pop_spectopo`, `pop_newtimef`) |
| **Ch 9** | Source Analysis (DIPFIT & Distributed eLORETA) | 源定位分析（等效偶极子拟合 DIPFIT 与 eLORETA） | `Tools -> Locate dipoles using DIPFIT` (`pop_dipfit_settings`, `pop_multifit`) |
| **Ch 10** | Group Analysis (`STUDY` Creation, Designs & Clustering) | 多被试群组分析（`STUDY` 创建、设计与成分聚类） | `File -> Create study`, `Study -> Precompute / Plot / Cluster` (`std_makedesign`, `std_precomp`, `pop_clust`) |
| **Ch 11** | Write Scripts & Official Automated Pipelines | 编写脚本与官方全自动 ERP / 频谱管线 | `eegh`, `pop_importbids`, `picard`, `std_specplot` |
| **Plugin** | Source-Level Functional Connectivity (`ROIconnect` & `SIFT`) | 源空间脑区功能连接与因果分析（`ROIconnect` & `SIFT`） | `Tools -> ROIconnect` (`pop_roi_activity`, `pop_roi_connect`, `pop_roi_connectplot`) |
