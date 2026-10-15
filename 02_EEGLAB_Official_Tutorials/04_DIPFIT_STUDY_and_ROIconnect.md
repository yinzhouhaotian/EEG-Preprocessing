# Ch 9–11 & Plugin: DIPFIT 源定位、官方全自动频谱管线与 ROIconnect 源空间连接性

> 所属手册：EEGLAB Official Tutorials 官方在线教程中英对照（eeglab.org/tutorials/，SCCN / UCSD）
>
> 章节导航：[01 导入与滤波规则](01_Import_and_Filtering_Rules.md) · [02 clean_rawdata/ICA/ICLabel](02_CleanRawdata_ICA_and_ICLabel.md) · [03 分段与时频ERSP](03_Epochs_and_TimeFrequency_ERSP.md) · [04 DIPFIT/STUDY/ROIconnect](04_DIPFIT_STUDY_and_ROIconnect.md) · [返回 README](../README.md)

## Chapter 9: 源定位分析——DIPFIT 等效偶极子与 eLORETA (Source Analysis)

* **English Original** ([Tutorials -\> 9.b DIPFIT](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F09_source%2FDIPFIT.html)):

  *Rationale for localizing ICA components*: Because local cortical connections have a much higher density than longer-range connections, synchronous coupling of local field potential (LFP) activity isolated by ICA usually occurs within a single connected cortical patch, producing scalp maps that nearly perfectly match the projection of a single equivalent dipole (Delorme et al., 2012).

  *What reference for ICA components in DIPFIT?* Although ICA unmixing is reference-free, before performing source localization in DIPFIT, both the ICA component scalp topography and the electrical forward head model are automatically converted to **average reference** so that they use the exact same approximation of the infinity reference.

  *Two-step fitting procedure*:

  1. **Coarse fit (grid scan)**: Scans a 3-D grid across the brain volume to find the best starting position.
  2. **Fine fit (non-linear optimization)**: Iteratively adjusts dipole position (`posxyz`) and dipole moment (`momxyz`) to minimize **Residual Variance (`rv`)**.

  Select `Tools -> Locate dipoles using DIPFIT -> Head model and settings` (`pop_dipfit_settings.m`), then `Autofit (coarse fit, fine fit, plot)` (`pop_multifit.m`). For distributed cortical source reconstruction, DIPFIT also integrates with FieldTrip (`ft_sourceanalysis`) via `Locate component using eLoreta` and `Distributed source leadfield matrix`.

* **中文译文与操作解析**：

  EEGLAB 的源定位插件 `DIPFIT` 既能为每个独立成分拟合单/双等效偶极子（存储在 `EEG.dipfit.model` 中，其中 `.posxyz` 为 MNI 坐标，`.rv` 为残差方差），也能生成全脑分布式源模型的**导联场矩阵（Leadfield Matrix）**，直接供 eLORETA 或后续的 `ROIconnect` 源空间脑区功能连接插件调用：

| `EEG.dipfit` 字段名 | 英文定义 (Official Definition) | 中文说明与用途 |
| :--- | :--- | :--- |
| `EEG.dipfit.hdmfile` | Head volume conductor model file | 头容积导体模型文件（如标准 BEM 模型 `standard_vol.mat`） |
| `EEG.dipfit.mrifile` | Anatomical MRI template file | 解剖结构 MRI 背景模板文件（`standard_mri.mat`） |
| `EEG.dipfit.coord_transform` | 9-parameter Talairach alignment vector | 将被试电极坐标对齐至标准头模的 9 参数空间变换向量 |
| `EEG.dipfit.model(i).posxyz` | 3-D MNI coordinates `[x y z]` (mm) | 第 `i` 个独立成分偶极子的三维 MNI 空间坐标（毫米） |
| `EEG.dipfit.model(i).rv` | Relative residual variance (`0` to `1`) | 偶极子拟合残差方差（`< 0.15` 即 `< 15%` 代表高质量脑源） |

## Chapters 10 & 11: 群组 `STUDY` 分析与官方全自动频谱脚本 (Group Analysis & Automated Pipelines)

* **English Original** ([Tutorials -\> 11.e Automated pipeline](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F11_Scripting%2Fautomated_pipeline.html)):

  You can process an entire group of subjects from raw BIDS data to grand-average power spectra or ERPs using a compact script. Key design choices in the official EEGLAB automated pipeline:

  1. *Why do we reference twice?* Artifact cleaning using `clean_rawdata` works better on average-referenced data. After bad channels are removed by `clean_rawdata`, we recompute the average reference (`pop_reref(ALLEEG, [])`) so the final reference is unbiased by the removed bad channels.
  2. *Missing channel interpolation*: Rather than interpolating channels before ICA (which causes rank issues), the official STUDY pipeline lets `std_precomp(..., 'interp', 'on', 'rmicacomps', 'on')` automatically subtract flagged artifact ICs and interpolate missing channels at the group `STUDY` level!

* **中文译文与操作解析**：

  在[官方第 11.e 节自动化管线教程](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F11_Scripting%2Fautomated_pipeline.html)中，EEGLAB 团队展示了一套极其精炼的**官方标准多被试频谱（Spectral）与功率分析批处理代码**。与 Makoto 管线相比，官方脚本有一个非常巧妙的设计：**不在跑 ICA 之前插值坏导**（从而彻底规避球面样条插值带来的非线性秩亏缺问题），而是只传入 `'pca', -1` 处理平均参考减去的 1 个维度，把“减去标记的伪迹 IC（`'rmicacomps', 'on'`）”和“插值补齐坏导（`'interp', 'on'`）”统一交给群组层的 `std_precomp` 函数自动完成！

  完整脚本见 [`../03_MATLAB_Scripts/eeglab_official_spectral_study.m`](../03_MATLAB_Scripts/eeglab_official_spectral_study.m)（官方 STUDY 多被试功率谱全自动管线）。

## Official Connectivity Plugin: 使用 `ROIconnect` 进行源空间功率与功能连接分析

因为你的课题聚焦于**任务态功率与连接性（非强锁时指标）**，EEGLAB 官方团队与 Stefan Haufe 课题组联合开发的 **[ROIconnect 官方插件](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Fplugins%2Froiconnect%2F)**（发表于 Pellegrini et al., 2023, *NeuroImage*）正是专门为此设计的标准化工具。

* **English Original** ([Plugins -\> ROIconnect](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Fplugins%2Froiconnect%2F)):

  `ROIconnect` is an open-source plugin to EEGLAB that performs linear and nonlinear functional connectivity (FC) analysis between regions of interest (ROIs) at the **cortical source level** (avoiding sensor-level volume conduction).

  1. *Installation*: `File -> Manage EEGLAB extensions -> select ROIconnect`.
  2. *Data Preparation & Leadfield*: Compute a distributed source leadfield matrix via `Tools -> Source localization using DIPFIT -> Head model settings`, then `Distributed source leadfield matrix`. Note that `ROIconnect` requires data resampled to ~`100 Hz` and extracts `2-second` segments.
  3. *Source Reconstruction & FOOOF Power (`pop_roi_activity`)*: Calculates spatial filters using **LCMV Beamforming** or **eLORETA**, projects sensor data to cortical atlas regions (e.g., `'LORETA-Talairach-BAs'` or Desikan-Killiani), computes region-wise Welch power spectra (with optional **FOOOF** aperiodic $1/f$ parameterization!), and extracts the top `nPCA` (e.g., 3) principal components per ROI.
  4. *Robust Connectivity Estimation (`pop_roi_connect`)*: Supports **Maximized Imaginary Coherency (`MIC`)**, **Multivariate Interaction Measure (`MIM`)**, **Imaginary Coherency (`iCOH`)**, and **Time-Reversed Granger Causality (`TRGC`, which suppresses weak-asymmetry volume conduction artifacts!)**.
     *Crucial note on data length bias*: Connectivity values vary systematically with total data length! Always keep the number of epochs or snippet length (`'snip_length', 60` seconds) strictly constant across all experimental conditions being compared.

* **中文译文与操作解析**：

  [ROIconnect 插件](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Fplugins%2Froiconnect%2F)直接解决了你在 MATLAB 中计算功率与功能连接的三大痛点：

  1. **自动完成源空间投影与脑区降维**：通过 `pop_roi_activity` 利用 LCMV 波束成形或 eLORETA 将头皮脑电投影到标准脑图谱（Atlas），对每个脑区提取前 3 个主成分（`nPCA = 3`），同时还能开启 `'fooof', 'on'` 自动分离周期性振荡功率与 $1/f$ 非周期背景斜率！
  2. **内置最先进的抗容积传导连接指标**：通过 `pop_roi_connect` 直接计算抗容积传导的无向连接指标 **MIM（多变量交互测度）/ MIC（最大化相干虚部）**，以及最稳健的有向连接指标 **TRGC（时间反转格兰杰因果，通过对比正向与时间反转序列的因果差值，彻底消除容积传导和信噪比差异带来的伪因果连接，见 Pellegrini et al., 2023）**。
  3. **自动对齐条件间数据长度**：由于连接性估计对试次数量/数据总时长高度敏感，`ROIconnect` 强制将各条件重采样至 100 Hz、切分为 2 秒片段，并通过随机抽样或等长切片（如 60 秒 `snip_length`）确保各任务条件参与计算的数据长度完全一致。

  完整脚本见 [`../03_MATLAB_Scripts/eeglab_roiconnect_pipeline.m`](../03_MATLAB_Scripts/eeglab_roiconnect_pipeline.m)（基于 LCMV 波束成形、FOOOF 与 MIM/TRGC 的源空间脑区连接脚本）。

## 附：官方教程 (`EEGLAB Tutorials`) 与 `Makoto's Pipeline` 核心异同速查表

在你的 GitHub 仓库中同时收录这两篇文档时，可以用下表向读者清晰展示两者的互补关系：

| 对比维度 | EEGLAB 官方在线教程 (`eeglab.org/tutorials/`) | Makoto's Preprocessing Pipeline (`SCCN Wiki`) | 针对你的“任务态功率 + 连接性”建议 |
| :--- | :--- | :--- | :--- |
| **定位与风格** | 官方标准功能指南，侧重 GUI 菜单与 `STUDY` 群组批处理框架 | 资深研究者深度避坑笔记，侧重线性代数（矩阵秩）、信号处理底层证明 | 两者结合：用 Makoto 的原理排雷，用官方的 `STUDY` / `ROIconnect` 架构写脚本 |
| **重参考时机** | 推荐“两次平均参考法”：`clean_rawdata` 前做一次，剔除坏导后再做一次 | 推荐在剔除并插值坏导后做一次“补零通道满秩全脑平均参考” | 两种方法在数学上均能消除坏导偏置；若在 ICA 前做重参考，建议补零通道或设 `'pca', -1` |
| **坏导插值时机** | 推荐留到最后在 `STUDY` 群组层（`std_precomp(..., 'interp', 'on')`）再插值 | 推荐在平均参考和 ICA 之前插值，但必须用特征值阈值（$10^{-7}$）显式扣减 ICA 维度 | **官方策略更省心**：在 ICA 和连接性计算前只剔除坏导不插值，既避免幽灵成分，又防止插值通道伪造连接 |
| **ASR 处理模式** | 离线分析默认直接切除超阈值伪迹段（`'BurstRejection', 'on'`） | 推荐仅用子空间重构修复而不切碎时间轴（`'BurstRejection', 'off'`, `SD = 20`） | 短试次多重复任务可用 `'on'`；长时程任务态（几秒至几十秒）推荐用 `'off'` 保留完整试次 |
| **连接性工具链** | 最新力推 **`ROIconnect`**（LCMV/eLORETA 源投影 + MIM/MIC/TRGC）与 `SIFT` | 重点介绍基于 ICA 源成分的 **`SIFT`**（多变量自回归 MVAR 格兰杰因果） | 若关注全脑图谱 ROI 间功率与连接性，优先使用官方 **`ROIconnect`** 或 **FieldTrip** |
