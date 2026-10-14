# EEG-Preprocessing
# EEGLAB Official Tutorials 官方在线教程中英对照完整指南（附 GUI 路径与官方自动化脚本）

> **原文来源 (Official Source)**: [EEGLAB Official Online Tutorials - SCCN (Swartz Center for Computational Neuroscience, UCSD)](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F)  
> **核心专题章节链接**: [5. Preprocess Data](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F05_Preprocess%2FFiltering.html) | [6. Reject Artifacts \& ICA](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F06_RejectArtifacts%2FRunICA.html) | [7. Extract Epochs](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F07_Extract_epochs%2FExtracting_Data_Epochs.html) | [8. Time-Frequency (ERSP/ITC)](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F08_Plot_data%2FTime-Frequency_decomposition.html) | [9. DIPFIT Source Localization](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F09_source%2FDIPFIT.html) | [10. Group STUDY Analysis](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F10_Group_analysis%2Fcomponent_clustering_tools.html) | [11. Automated Scripting](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F11_Scripting%2Fautomated_pipeline.html) | [ROIconnect Connectivity Plugin](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Fplugins%2Froiconnect%2F)  
> **文档说明**: 本文档将 EEGLAB 官方在线教程（`eeglab.org/tutorials/`）全部 11 个核心模块及源空间功能连接插件（`ROIconnect` / `SIFT`）整理为**中英双语对照手册**，完整保留官方 GUI 菜单操作路径、算法原理说明及官方标准 MATLAB 批处理脚本，可直接作为 `EEGLAB_Official_Tutorials_CN_EN.md` 上传至你的 GitHub 仓库与《Makoto's Preprocessing Pipeline》配套使用。

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

## Chapter 6: 伪迹剔除——ASR 自动清洗、ICA 与 ICLabel (Reject Artifacts)

### 6.c 使用 `clean_rawdata` 与 ASR 进行自动伪迹剔除 (Automated Artifact Rejection)

* **English Original** ([Tutorials -\> 6.c Automated rejection](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F06_RejectArtifacts%2Fcleanrawdata.html)):  
  `Clean_rawdata` is installed by default with EEGLAB (`Tools -> Reject data using Clean Rawdata and ASR`, calling `pop_clean_rawdata.m` / `clean_artifacts.m`). There are five sequential sections in its menu:
  1. *High-pass filtering*: Transition bandwidth limits `[0.25 0.75]` Hz indicate a high-pass filter at `0.5` Hz (uncheck if you already high-pass filtered your data).
  2. *Removing bad channels*: Flat channels (e.g., flat for $>5\text{ s}$), noisy channels based on standard deviation (`LineNoiseCriterion = 4`), and channels poorly correlated with surrounding channels (`ChannelCriterion = 0.8`, or `0.85–0.87`). Importing channel locations beforehand is strongly advised so spatial correlation heuristics work accurately.
  3. *Artifact Subspace Reconstruction (ASR)*: ASR finds clean portions of data (calibration data) and calculates PCA-extracted components' standard deviation. It flags or reconstructs data regions exceeding `20` times (by default) the standard deviation of the calibration data (`BurstCriterion = 20`). Note: For offline EEG processing, the official EEGLAB tutorial defaults to *removing* bad data regions (`'BurstRejection', 'on'`), whereas for real-time applications or preserving continuous trial length (as in Makoto's pipeline), ASR *reconstructs/corrects* the data (`'BurstRejection', 'off'`).
  4. *Additional window rejection*: Rejects time windows where more than a set fraction of channels (`WindowCriterion = 0.25`) still exceed a standard deviation threshold (`[-Inf 7]`) after ASR.
* **中文译文与操作解析**：  
  `clean_rawdata` 是目前 EEGLAB 默认集成的标准化前端清洗工具（通过 `Tools -> Reject data using Clean Rawdata and ASR` 调用）。需特别注意**官方教程与 Makoto 管线在 `BurstRejection` 参数上的微小差异**：
  * **EEGLAB 官方离线默认策略（`'BurstRejection', 'on'`）**：对超过校准数据 20 倍标准差（`BurstCriterion = 20`）的剧烈伪迹时间段直接予以切除（不进行子空间合成修复），以避免 ASR 重构对离线信号特性的潜在改变。
  * **长时程任务态 / 保持试次完整策略（`'BurstRejection', 'off'`）**：如果你的任务态试次较长，直接切除连续片段会导致大量试次被 `"boundary"` 事件打断而作废，此时可将 `'BurstRejection'` 设为 `'off'`（启用 ASR 修复），或将 `BurstCriterion` 放宽至 `20–40`。

```matlab
% 官方推荐的 clean_rawdata 自动清洗命令（配合先行的 FIR 高通滤波）
EEG = pop_eegfiltnew(EEG, 'locutoff', 0.5);
EEG = clean_artifacts(EEG, ...
    'FlatlineCriterion', 5, ...
    'ChannelCriterion', 0.85, ...
    'LineNoiseCriterion', 4, ...
    'Highpass', 'off', ...
    'BurstCriterion', 20, ...
    'WindowCriterion', 0.25, ...
    'BurstRejection', 'on', ...
    'Distance', 'Euclidian', ...
    'WindowCriterionTolerances', [-Inf 7]);
```

### 6.d 独立成分分析（ICA）原理、质量优化与 ICLabel 自动分类 (Independent Component Analysis)

* **English Original** ([Tutorials -\> 6.d Indep. Comp. Analysis](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F06_RejectArtifacts%2FRunICA.html)):  
  *Running ICA*: Select `Tools -> Decompose data by ICA` (`pop_runica.m`).  
  *Which ICA Algorithm?*
  - `runica` (Infomax ICA): Default in EEGLAB, robust but relatively slow. Use `'extended', 1` (default) to detect sub-Gaussian sources like line noise, and optionally `'stop', 1e-7` for high-density arrays.
  - `picard`: Optimizes the same objective function as Infomax using Newton optimization (designed by J.-F. Cardoso), converging much faster and with lower residuals.
  - `AMICA`: Best overall ICA algorithm based on SCCN benchmarks (Delorme et al., 2012), though computationally slow.
  - `FastICA`: Advise using the symmetric approach rather than default iterative approach.  
  *Selecting channel types*: If you have both EEG and EMG channels, run ICA on EEG channels ONLY (`Edit -> Channel locations` to define channel types), because any relationship between EEG and peripheral EMG involves propagation delays, violating ICA's assumption of instantaneous volume conduction.  
  *Studying and flagging artifactual ICs*: Select `Tools -> Inspect/label components by maps` or `Plot -> Component properties`. Four main criteria distinguish brain vs. artifact ICs:
  1. **Scalp map (2-D topography)**: Eye blinks have strong far-frontal projection; lateral eye movements have opposite polarities at left/right temples; muscle artifacts are spatially focal/localized at the edge of the cap; brain components have smooth dipolar projections.
  2. **Component time course (`Plot -> Component activations (scroll)`)**: Spot discrete blinks, saccades, or single-channel pops.
  3. **Power spectrum (PSD)**: Eye artifacts show smoothly decreasing low-frequency dominance; **muscle (EMG) artifacts show high power at high frequencies (20–50 Hz and above)**; line noise shows sharp 50/60 Hz peaks; brain components typically show $1/f$ decay with distinct Alpha (~10 Hz) or Theta/Beta peaks.
  4. **ERP-image (`erpimage.m`)**: Visualizes single-trial component activity across trials.  
  *Optimizing ICA Quality — The 4 Golden Rules*:
  1. **Dual-dataset strategy for aggressive high-pass filtering**: High-pass filtering at 1–2 Hz dramatically improves ICA quality. If you need $<1\text{ Hz}$ features preserved, filter Dataset 1 at 1–2 Hz to obtain Dataset 2, run ICA on Dataset 2, and copy `ALLEEG(2).icaweights` and `ALLEEG(2).icasphere` back to Dataset 1 (`Edit -> Dataset info`).
  2. **Handling Rank Deficiency & Corrupted/Ghost ICs**: Average referencing $N$ channels reduces data rank to $N-1$. If the first two ICs blow up with identical maps and opposite polarities (compensating for each other), the data is rank-deficient. Pass `'pca', -1` (or `'pca', N_effective`) in `pop_runica` options!
  3. **Continuous vs. Epoched ICA & Baseline Caution**: In general, we recommend running ICA on **continuous data** rather than epoched data: first, continuous data provides more time points; second, you are not tempted to remove the epoch baseline before ICA (**removing epoch baselines introduces random offsets in each channel that severely corrupt ICA**). If you must epoch before ICA, never use overlapping epochs and never subtract the baseline until after ICA!
  4. **NEVER re-reference after ICA**: Re-referencing is best performed *before* running ICA and left unchanged afterward. Changing the reference after ICA applies a linear transform inconsistent with the learned unmixing matrix, degrading component interpretability and causing numerical rank issues.  
  *Automated IC Classification with `ICLabel`*: Select `Tools -> Classify components using ICLabel -> Label components` (`pop_iclabel.m`), then `Flag components as artifacts` (`pop_icflag.m`). `ICLabel` estimates probabilities across 7 categories: **1. Brain, 2. Muscle, 3. Eye, 4. Heart, 5. Line Noise, 6. Channel Noise, 7. Other**. By default, `pop_icflag` flags components with $>90\%$ probability of being Muscle or Eye artifacts, which can then be subtracted via `Tools -> Remove components from data` (`pop_subcomp.m`) or automatically excluded at the `STUDY` level.
* **中文译文与操作解析**：  
  [EEGLAB 官方 ICA 教程](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F06_RejectArtifacts%2FRunICA.html)给出了非常明确的操作规范：
  1. **算法选择**：除了默认的 `runica`（扩展 Infomax），官方现在在自动化脚本中高度推荐使用 **`picard` 插件**（与 Infomax 目标函数完全相同，但采用牛顿法优化，收敛速度极快且残差更小）或 **`AMICA`**。
  2. **四大鉴别标准**：通过 `Tools -> Inspect/label components by maps` 查看每个成分的① 头皮地形图、② 时间序列、③ 功率谱（注意：**肌电成分在 20–50 Hz 高频段功率显著翘起**，这对你做高频功率和连接性尤为重要，必须剔除！）、④ 单试次 ERP-image。
  3. **官方强调的三大禁忌**：
     - **严禁在 ICA 之前做分段基线校正（`pop_rmbase`）**：会给每个通道注入随机偏移，彻底破坏 ICA 空间建模。
     - **严禁在 ICA 之后再更改参考电极（Re-referencing after ICA）**：ICA 学习的解混矩阵依赖于训练时的参考方式，事后重参考会导致解混矩阵与通道数据失配（EEGLAB 会弹出警告）。所有重参考必须在跑 ICA 之前定型！
     - **必须处理秩亏缺**：做完平均参考后跑 ICA，必须在选项中传入 `'pca', -1`（自动将维度减 1）或真实有效秩，否则会出现前两个成分波幅暴增、极性相反相互抵消的“崩溃 / 幽灵成分”。
  4. **ICLabel 的 7 类概率矩阵**：运行 `EEG = pop_iclabel(EEG, 'default')` 后，`EEG.etc.ic_classification.ICLabel.classifications` 是一个 $N_{\text{IC}} \times 7$ 的概率矩阵，7 列依次对应：`[Brain, Muscle, Eye, Heart, Line Noise, Channel Noise, Other]`。

```matlab
% 使用 Picard（或 runica）在扣减 1 个平均参考秩维度下运行 ICA，并用 ICLabel 自动标记眼电和肌电
EEG = pop_runica(EEG, 'icatype', 'runica', 'extended', 1, 'pca', -1);
EEG = pop_iclabel(EEG, 'default');

% pop_icflag 阈值矩阵为 7x2，对应 [Brain; Muscle; Eye; Heart; LineNoise; ChanNoise; Other]
% 下方设置表示：将 Muscle (第2行) 或 Eye (第3行) 概率在 [0.9, 1.0] (即 >90%) 的成分标记为伪迹并剔除
EEG = pop_icflag(EEG, [NaN NaN; 0.9 1; 0.9 1; NaN NaN; NaN NaN; NaN NaN; NaN NaN]);
EEG = pop_subcomp(EEG, [], 0); % 将被 pop_icflag 标记为拒绝的伪迹成分从数据中减去
```

## Chapter 7: 提取数据分段与筛选子集 (Extract Data Epochs)

* **English Original** ([Tutorials -\> 7. Extract Data Epochs](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F07_Extract_epochs%2FExtracting_Data_Epochs.html)):  
  Select `Tools -> Extract Epochs` (`pop_epoch.m`), choose the time-locking event type(s), and retain epoch limits such as `[-1 2]` seconds (3 seconds long). **It is often better to extract long data epochs, as here, to make time-frequency decomposition possible at lower (below 10 Hz) frequencies.**  
  *Removing baseline values*: After epoching, `Tools -> Remove baseline` (`pop_rmbase.m`) pops up. High-pass filtering is already a form of baseline correction, rendering this step optional. Avoid short baseline windows (on the order of 100 ms) whenever possible.  
  *Extracting sub-epochs & Selecting epochs by event info*: Use `Edit -> Select data` (`pop_select.m`) to crop sub-epochs or remove specific trial indices, or `Edit -> Select epochs or events` (`pop_selectevent.m`) to select trials matching specific event metadata fields (making sure `'Remove epochs not referenced by any selected event'` is checked).
* **中文译文与操作解析**：  
  在 `Tools -> Extract Epochs`（`pop_epoch.m`）中围绕任务事件分段时，官方特别指出：**为了能够分析 10 Hz 以下（如 Theta、Alpha 频段）的时频功率与相位，应该截取至少 3 秒长（例如 `-1` 到 `2` 秒）的宽时间窗**。若已做过 1 Hz 高通滤波且关注的是频域功率/连接性，时域 `pop_rmbase` 是可选的（若做 ERP 基线校正，应选在 ICA 完成之后，且基线窗口不宜过短）。

## Chapter 8: 频谱与时频分解实战——ERSP 与 ITC (Spectra & Time-Frequency Decomposition)

* **English Original** ([Tutorials -\> 8.d Time-Frequency](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F08_Plot_data%2FTime-Frequency_decomposition.html)):  
  To detect transient **Event-Related Spectral Perturbation (ERSP)** (event-related shifts in the power spectrum in dB relative to baseline, Makeig, 1993) and **Inter-Trial Coherence (ITC)** (event-related phase-locking across trials) in epoched datasets, select `Plot -> Time-frequency transforms -> Channel time-frequency` (`pop_newtimef.m`).  
  *Understanding `"Wavelet cycles" = [3 0.8]`*:  
  The default entry `3 0.8` means that the sinusoidal wavelet (Hanning-tapered) begins with a **3-cycle wavelet** at the lowest frequency, and the number of cycles continues to expand slowly with frequency, reaching $20\%$ ($1 - 0.8$) of the number of cycles in the equivalent FFT window at the highest frequency (this achieves higher frequency resolution at higher frequencies while maintaining good temporal resolution).  
  *How to reach 3 Hz at the lowest frequency (`'winlen'`)*:  
  By default, the lowest-frequency sliding window is about $0.5\text{ seconds}$ long; fitting 3 cycles into $0.5\text{ s}$ sets the lowest analyzed frequency to $6\text{ Hz}$. To lower the minimum analyzed frequency to **$3\text{ Hz}$** with 3 cycles, the window length must be $1\text{ second}$ long—add the optional argument `'winlen', EEG.srate` (or lengthen the epoch range).  
  *Significance masking & `padratio`*:  
  Enter `0.05` in the *Bootstrap significance level* box and check `FDR correct` to mask non-significant time-frequency pixels using permutation/bootstrap shuffling and False Discovery Rate correction. Increase `'padratio'` (e.g., from default `2` to `4` or `8`) via zero-padding to interpolate and smooth the frequency axis.
* **中文译文与操作解析（专为你的任务态功率研究详解）**：  
  在 EEGLAB 中计算任务态时频功率的核心函数是 `pop_newtimef.m`（菜单 `Plot -> Time-frequency transforms -> Channel time-frequency` 或 `Component time-frequency`），它会同时输出两张核心图：
  1. **上半图 ERSP（事件相关谱扰动，单位 dB）**：衡量每个时间点和频率相对于刺激前基线的**总功率变化（包含锁相与非锁相诱发振荡）**。正值（暖色）代表事件相关同步化（ERS，功率增强），负值（冷色）代表事件相关去同步化（ERD，功率下降）。
  2. **下半图 ITC（试次间相干性，取值 0–1）**：衡量不同试次在同一时刻的相位锁定程度。**正如你前面提到的“不强调强锁时性指标”，当你看到某个时频区域 ERSP 显著增强（通过 Bootstrap `alpha = 0.05` + `FDR` 校正），而对应的 ITC 并不显著时，就证明这完全是一个纯粹的非锁相诱发振荡（Induced Oscillation）！**
  3. **小波参数 `[3 0.8]` 的精确含义**：第一个数字 `3` 表示在最低频率处使用 3 个周期的 Morlet/Hanning 小波；第二个数字 `0.8`（当小于 1 时）表示随着频率升高，小波周期数按 $(1 - 0.8) = 20\%$ 的等效 FFT 窗比例递增（等价于高频端时间窗不会缩得太窄，从而兼顾高频的频率分辨率）。如果默认最低频率只到 6 Hz，只需把 Epoch 分段拉长（如 `[-1 2]` 秒）或在附加参数中传入 `'freqs', [3 50]`，函数就会自动采用约 1 秒宽的滑动窗从 3 Hz 开始计算。

```matlab
% 调用 pop_newtimef 计算第 14 号通道 (Cz) 在 3–50 Hz 的任务态 ERSP 功率与 ITC，开启 0.05 Bootstrap 与 FDR 校正
figure;
[ersp, itc, powbase, times, freqs, erspboot, itcboot] = pop_newtimef(EEG, 1, 14, ...
    [EEG.xmin EEG.xmax]*1000, [3 0.8], ...
    'topovec', 14, 'elocs', EEG.chanlocs, 'chaninfo', EEG.chaninfo, ...
    'baseline', [-500 0], 'freqs', [3 50], 'alpha', 0.05, 'mcorrect', 'fdr', ...
    'padratio', 4, 'plotphase', 'off');
```

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

```matlab
%% ========================================================================
%  EEGLAB Official Automated Spectral (Power) Pipeline (Tutorial 11.e)
%  官方标准多被试功率谱全自动预处理与群组统计脚本
% =========================================================================
eeglab;
rng(1); % 固定随机种子以保证 ASR 与 ICA 结果完全可复现
pop_editoptions('option_storedisk', 1); % 内存中仅驻留单个数据集以节省内存

% 1. 从 BIDS 文件夹批量导入多被试数据（也可替换为循环 pop_loadset）
filepath = '/path/to/your/bids_dataset';
[STUDY, ALLEEG] = pop_importbids(filepath, 'studyName', 'Task_Power_Study');

% 2. 移除非脑电辅助通道（如外接肌电 EXG、皮电 GSR、呼吸 Resp 等）
ALLEEG = pop_select(ALLEEG, 'rmchannel', {'EXG1','EXG2','EXG3','EXG4','GSR1','Resp'});

% 3. 第一次全脑平均参考（提升后续 clean_rawdata 识别坏导的准确度）
ALLEEG = pop_reref(ALLEEG, []);

% 4. 使用 clean_rawdata 进行高通滤波 (0.5 Hz)、剔除坏导及 ASR 伪迹清理
ALLEEG = pop_clean_rawdata(ALLEEG, ...
    'FlatlineCriterion', 5, 'ChannelCriterion', 0.87, ...
    'LineNoiseCriterion', 4, 'Highpass', [0.25 0.75], ...
    'BurstCriterion', 20, 'WindowCriterion', 0.25, ...
    'BurstRejection', 'on', 'Distance', 'Euclidian', ...
    'WindowCriterionTolerances', [-Inf 7], 'fusechanrej', 1);

% 5. 剔除坏导后重新计算第二次全脑平均参考（消除坏导对第一次均值的污染）
ALLEEG = pop_reref(ALLEEG, []);

% 6. 运行 Picard (或 runica) ICA，设置 'pca', -1 以匹配平均参考减少的 1 个秩维度
ALLEEG = pop_runica(ALLEEG, 'icatype', 'picard', 'concatcond', 'on', 'options', {'pca', -1});

% 7. 运行 ICLabel 并自动标记概率 > 90% 的肌电 (Muscle) 与眼电 (Eye) 伪迹成分
ALLEEG = pop_iclabel(ALLEEG, 'default');
ALLEEG = pop_icflag(ALLEEG, [NaN NaN; 0.9 1; 0.9 1; NaN NaN; NaN NaN; NaN NaN; NaN NaN]);

% 8. 提取任务态事件分段（例如条件 1 与条件 2，时间窗 -1 至 2 秒）
ALLEEG = pop_epoch(ALLEEG, {'condition_A', 'condition_B'}, [-1 2], 'epochinfo', 'yes');
ALLEEG = eeg_checkset(ALLEEG);

% 9. 创建 STUDY 实验设计矩阵（对比不同任务条件）
STUDY = std_maketrialinfo(STUDY, ALLEEG);
STUDY = std_makedesign(STUDY, ALLEEG, 1, 'name', 'Condition_Contrast', ...
    'delfiles', 'off', 'defaultdesign', 'off', ...
    'variable1', 'type', 'values1', {'condition_A', 'condition_B'}, ...
    'vartype1', 'categorical', 'subjselect', STUDY.subject);

% 10. 在 STUDY 群组层面自动减去伪迹 IC ('rmicacomps','on')、插值坏导 ('interp','on') 并预计算功率谱 ('spec','on')
%     （若需预计算时频功率 ERSP/ITC，可将 'spec','on' 改为 'ersp','on','itc','on'）
[STUDY, ALLEEG] = std_precomp(STUDY, ALLEEG, {}, ...
    'savetrials', 'on', 'rmicacomps', 'on', 'interp', 'on', ...
    'recompute', 'on', 'spec', 'on');

% 11. 绘制 10 Hz Alpha 频段全脑功率地形图与频谱对比曲线
STUDY = pop_specparams(STUDY, 'topofreq', 10);
chanlocs = eeg_mergelocs(ALLEEG.chanlocs);
STUDY = std_specplot(STUDY, ALLEEG, 'channels', {chanlocs.labels}, 'design', 1);
pop_editoptions('option_storedisk', 0);
```

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

```matlab
%% ========================================================================
%  EEGLAB ROIconnect 源空间脑区功率 (含 FOOOF) 与功能连接 (MIM / TRGC) 标准代码
%  参考：https://eeglab.org/plugins/roiconnect/ (Pellegrini et al., 2023, NeuroImage)
% =========================================================================

% 1. 确保数据已降采样至 100 Hz 并生成分布式源模型导联场 (Leadfield)
if EEG.srate > 100
    EEG = pop_resample(EEG, 100);
end
EEG = pop_dipfit_settings(EEG, 'coordformat', 'MNI');
EEG = pop_leadfield(EEG, 'sourcemodel', 'standard_BEM/standard_vol.mat');

% 2. 计算源空间脑区活动 (LCMV 波束成形, 提取每个脑区前 3 个主成分) 及腦区功率谱 (开启 1-30 Hz FOOOF 拟合)
EEG = pop_roi_activity(EEG, ...
    'leadfield', EEG.dipfit.sourcemodel, ...
    'model', 'LCMV', ...
    'modelparams', {0.05}, ...
    'atlas', 'LORETA-Talairach-BAs', ...
    'nPCA', 3, ...
    'fooof', 'on', ...
    'fooof_frange', [1 30]);

% 3. 计算脑区间无向功能连接 (MIM) 与抗容积传导有向连接 (TRGC)，固定 60 秒等长切片消除长度偏置
EEG = pop_roi_connect(EEG, ...
    'methods', {'MIM', 'TRGC'}, ...
    'snippet', 'on', ...
    'snip_length', 60, ...
    'fcsave_format', 'mean_snips');

% 4. 可视化 8–13 Hz (Alpha 频段) 的源空间皮层功率地形图与脑区连接矩阵
EEG = pop_roi_connectplot(EEG, 'measure', 'roipsd', 'plotcortex', 'on', 'freqrange', [8 13]);
EEG = pop_roi_connectplot(EEG, 'measure', 'mim', 'plotcortex', 'off', 'plotmatrix', 'on', ...
    'freqrange', [8 13], 'grouphemispheres', 'on');
```

## 附：官方教程 (`EEGLAB Tutorials`) 与 `Makoto's Pipeline` 核心异同速查表

在你的 GitHub 仓库中同时收录这两篇文档时，可以用下表向读者清晰展示两者的互补关系：

| 对比维度 | EEGLAB 官方在线教程 (`eeglab.org/tutorials/`) | Makoto's Preprocessing Pipeline (`SCCN Wiki`) | 针对你的“任务态功率 + 连接性”建议 |
| :--- | :--- | :--- | :--- |
| **定位与风格** | 官方标准功能指南，侧重 GUI 菜单与 `STUDY` 群组批处理框架 | 资深研究者深度避坑笔记，侧重线性代数（矩阵秩）、信号处理底层证明 | 两者结合：用 Makoto 的原理排雷，用官方的 `STUDY` / `ROIconnect` 架构写脚本 |
| **重参考时机** | 推荐“两次平均参考法”：`clean_rawdata` 前做一次，剔除坏导后再做一次 | 推荐在剔除并插值坏导后做一次“补零通道满秩全脑平均参考” | 两种方法在数学上均能消除坏导偏置；若在 ICA 前做重参考，建议补零通道或设 `'pca', -1` |
| **坏导插值时机** | 推荐留到最后在 `STUDY` 群组层（`std_precomp(..., 'interp', 'on')`）再插值 | 推荐在平均参考和 ICA 之前插值，但必须用特征值阈值（$10^{-7}$）显式扣减 ICA 维度 | **官方策略更省心**：在 ICA 和连接性计算前只剔除坏导不插值，既避免幽灵成分，又防止插值通道伪造连接 |
| **ASR 处理模式** | 离线分析默认直接切除超阈值伪迹段（`'BurstRejection', 'on'`） | 推荐仅用子空间重构修复而不切碎时间轴（`'BurstRejection', 'off'`, `SD = 20`） | 短试次多重复任务可用 `'on'`；长时程任务态（几秒至几十秒）推荐用 `'off'` 保留完整试次 |
| **连接性工具链** | 最新力推 **`ROIconnect`**（LCMV/eLORETA 源投影 + MIM/MIC/TRGC）与 `SIFT` | 重点介绍基于 ICA 源成分的 **`SIFT`**（多变量自回归 MVAR 格兰杰因果） | 若关注全脑图谱 ROI 间功率与连接性，优先使用官方 **`ROIconnect`** 或 **FieldTrip** |

