# Ch 1–5: 数据结构、导入、高通/低通分离滤波与连接性滤波禁忌

> **原文来源 (Official Source)**: [EEGLAB Official Online Tutorials - SCCN (Swartz Center for Computational Neuroscience, UCSD)](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F)
> **核心专题章节链接**: [5. Preprocess Data](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F05_Preprocess%2FFiltering.html) | [6. Reject Artifacts \& ICA](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F06_RejectArtifacts%2FRunICA.html) | [7. Extract Epochs](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F07_Extract_epochs%2FExtracting_Data_Epochs.html) | [8. Time-Frequency (ERSP/ITC)](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F08_Plot_data%2FTime-Frequency_decomposition.html) | [9. DIPFIT Source Localization](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F09_source%2FDIPFIT.html) | [10. Group STUDY Analysis](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F10_Group_analysis%2Fcomponent_clustering_tools.html) | [11. Automated Scripting](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F11_Scripting%2Fautomated_pipeline.html) | [ROIconnect Connectivity Plugin](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Fplugins%2Froiconnect%2F)
> **文档说明**: 本文档将 EEGLAB 官方在线教程（`eeglab.org/tutorials/`）全部 11 个核心模块及源空间功能连接插件（`ROIconnect` / `SIFT`）整理为**中英双语对照手册**，完整保留官方 GUI 菜单操作路径、算法原理说明及官方标准 MATLAB 批处理脚本，可直接作为 `EEGLAB_Official_Tutorials_CN_EN.md` 上传至你的 GitHub 仓库与《Makoto's Preprocessing Pipeline》配套使用。

> 所属手册：EEGLAB Official Tutorials 官方在线教程中英对照（eeglab.org/tutorials/，SCCN / UCSD）
>
> 章节导航：[01 导入与滤波规则](01_Import_and_Filtering_Rules.md) · [02 clean_rawdata/ICA/ICLabel](02_CleanRawdata_ICA_and_ICLabel.md) · [03 分段与时频ERSP](03_Epochs_and_TimeFrequency_ERSP.md) · [04 DIPFIT/STUDY/ROIconnect](04_DIPFIT_STUDY_and_ROIconnect.md) · [返回 README](../README.md)

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

## Chapters 1–4: 数据结构与导入规范 (Dataset Management & Importing Data)

* **English Original**:

  Welcome to the EEGLAB tutorial. The EEGLAB Tutorial is split into core single-subject processing steps, group analysis (`STUDY`), scripting, and Concepts Guides.

  When working with a dataset that does not have channel locations, select the `Edit -> Channel locations` menu item and press `Ok` to look up channel locations based on channel labels (using the default MNI BEM template `standard_1005.elc`), then close the channel editor. For BIDS-formatted datasets, EEGLAB supports direct group import via `File -> Import data -> From BIDS folder structure` (`pop_importbids.m`).

* **中文译文与操作解析**：

  在 MATLAB 命令窗口输入 `eeglab` 启动主界面后，当前激活的数据集保存在结构体变量 `EEG` 中，所有已加载的数据集保存在结构体数组 `ALLEEG` 中。

  1. **导入连续数据**：通过 `File -> Import data -> Using EEGLAB functions and plugins` 选择对应采集设备格式（如 BrainVision `.vhdr`、Neuroscan `.cnt`、BioSemi `.bdf` 或通用格式 `pop_biosig`）。
  2. **匹配标准电极位置**：选择 `Edit -> Channel locations`（调用 `pop_chanedit.m`），只要电极名称符合国际 10-20 / 10-5 命名规范（如 `Fz, Cz, Pz, Oz`），点击 `Ok` 即可自动从 `standard_1005.elc` 模板中匹配 MNI 三维坐标。**官方特别提醒：务必在进行自动化伪迹剔除（`clean_rawdata`）、插值、全脑平均参考和源定位之前导入通道位置！**
  3. **导入 BIDS 标准数据集**：若数据遵循脑成像数据结构标准（BIDS），可直接调用 `pop_importbids()` 一键导入所有被试并自动生成 `STUDY` 群组结构。

```matlab
% 启动 EEGLAB 并加载示例数据，匹配默认 10-5 系统电极坐标
[ALLEEG, EEG, CURRENTSET, ALLCOM] = eeglab;
EEG = pop_loadset('filename', 'eeglab_data.set', 'filepath', fullfile(fileparts(which('eeglab')), 'sample_data'));
EEG = pop_chanedit(EEG, 'lookup', 'standard_1005.elc');
```

## Chapter 5: 数据预处理——滤波、重参考与重采样 (Preprocess Data)

### 5.a 时域滤波与连接性分析滤波准则 (Filtering the Data)

* **English Original** ([Tutorials -\> 5.a Filtering](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F05_Preprocess%2FFiltering.html)):

  *Basic rule*: In the default Windowed Sinc FIR filter, the basic rule is to have the transition band as wide (roll-off soft) as possible to avoid time-domain ringing artifacts, but separated from the signal of interest.

  *Removing linear trends*: We recommend filtering continuous EEG data before epoching or artifact removal. Filtering the continuous data minimizes the introduction of filtering artifacts at epoch boundaries. Select `Tools -> Filter the data -> Basic FIR filter (new, default)`, enter `1` (Hz) as the Lower edge frequency, and press `Ok`. High-pass filtering the data at 1 Hz is recommended to obtain good quality ICA decompositions (Klug & Gramann, 2020). Note that the EEGLAB legacy filter (`pop_eegfilt`) is no longer recommended (Widmann & Schröger, 2012).

  *Important caution on bandpass filtering*: If high-pass and low-pass cutoff frequencies are BOTH selected in a single call, low-pass and high-pass parts will be forced to have the same transition slopes! Frequently, the low-pass slope is therefore much steeper than necessary. **To avoid this problem, we recommend first applying the low-pass filter and then, in a second call, the high-pass filter (or vice versa).**

  *Major spikes before filtering*: Removing data portions containing major artifacts (large spikes) before filtering can be preferable since filtering can "spread" the artifact out over "good" data. When you remove major artifacts, a `"boundary"` event replaces the removed data. Filtering is only applied to continuous data segments, never across `"boundary"` events.

  *Filtering for connectivity analysis*: **High-pass filtering introduces dependencies in neighboring data samples and is often not recommended for connectivity analysis.** In this case, it is usually better to apply piecewise detrending to remove data trends (available in the SIFT EEGLAB plugin). For causal analysis (assessing if one process causes another), standard zero-phase forward-backward filtering (`filtfilt`) compromises temporal causality because future samples influence past samples; instead, use a **causal filter** (applied only forward in time) or piecewise detrending, keeping in mind that causal filters introduce phase delays.

  *Alternative to notch filtering*: To remove 50-Hz or 60-Hz line noise, instead of notch filtering, one may use the `CleanLine` EEGLAB plugin, which adaptively estimates and removes sinusoidal line noise using multi-tapering and a Thompson F-statistic.

* **中文译文与操作解析**：

  1. **连续数据优先原则**：必须在提取分段（Epoching）之前对连续脑电数据进行滤波，以避免在每个试次边界引入滤波边缘效应；若先手动剪除了包含巨大尖峰伪迹的连续片段，切口处会自动生成 `"boundary"`（边界）标记，EEGLAB 的滤波器会在 `"boundary"` 处自动分段独立滤波，不会跨越边界把伪迹抹开。
  2. **高通与低通必须分两次调用（防踩坑细节）**：在 `Tools -> Filter the data -> Basic FIR filter (new, default)`（即 `pop_eegfiltnew.m`）中，**切勿在同一个对话框里同时填写高通（Lower edge）和低通（Higher edge）频率！** 因为同时填写时，滤波器会按照高通所需的窄过渡带去強制设定低通的过渡带斜率，导致低通滤波器过于陡峭而产生严重的时域波纹（Ripples / Ringing）。**官方推荐：先单独调用一次高通滤波，再单独调用一次低通滤波。**
  3. **连接性与因果分析的专属滤波警告**：官方教程明确指出，常规高通滤波会在相邻采样点之间引入线性依赖，而零相位正反向滤波（`filtfilt`）会让未来的采样点影响过去的采样点，从而干扰**因果连接分析（如格兰杰因果 GC）**。若进行有向因果分析，推荐使用 SIFT 插件中的**分段线性去趋势（Piecewise detrending）**，或者勾选**因果滤波器（Causal filter，仅正向滤波）**。

```matlab
% 官方推荐做法：分开调用高通与低通滤波，避免低通过渡带过陡产生振铃伪迹
EEG = pop_eegfiltnew(EEG, 'locutoff', 1, 'plotfreqz', 0);   % 第1步：1 Hz 高通滤波
EEG = pop_eegfiltnew(EEG, 'hicutoff', 40, 'plotfreqz', 0);  % 第2步：40 Hz 低通滤波（按需）
```

### 5.b 重参考与重采样 (Re-referencing & Resampling)

* **English Original**:

  Select `Tools -> Re-reference the data` (`pop_reref.m`) to convert the data to common average reference or specific reference channels. In modern EEGLAB automated pipelines, average referencing is often computed twice: once before `clean_rawdata` (because artifact cleaning works better on average-referenced data) and once again after bad channels have been removed (the second average reference undoes the first biased one). EEGLAB also supports robust Huber average referencing (`'huber', 25`) which reduces the influence of outlier channels.

  Select `Tools -> Change sampling rate` (`pop_resample.m`) to downsample high-frequency recordings and speed up analysis.

* **中文译文与操作解析**：

  在 `Tools -> Re-reference the data`（调用 `pop_reref.m`）中可执行全脑平均参考。官方自动化管线提出了一个非常实用的技巧——**“两次平均参考法”**：由于 `clean_rawdata` 在全脑平均参考下识别坏导和突发伪迹更敏锐，可以先做一次初步的全脑平均参考，跑完 `clean_rawdata` 剔除坏导后，**再重新执行第二次全脑平均参考**（由于单极重参考具有线性无记忆可逆性，第二次平均参考会自动抵消第一次包含坏导时的均值偏置）。此外，`pop_reref` 还支持传入 `'huber', 25` 参数启用 Huber 鲁棒均值估计，进一步抗击离群噪声。
