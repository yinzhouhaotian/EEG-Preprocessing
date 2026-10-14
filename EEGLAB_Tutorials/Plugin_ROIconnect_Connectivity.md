# Official Connectivity Plugin: 使用 `ROIconnect` 进行源空间功率与功能连接分析

> 所属手册：EEGLAB 官方教程中英对照（由 `README.md` 按章节拆分）
>
> 章节导航：[00 总览](00_Overview_and_Navigation.md) · [Ch1–4](Ch01-04_Data_Management_Import.md) · [Ch5](Ch05_Preprocess_Data.md) · [Ch6](Ch06_Reject_Artifacts_ASR_ICA.md) · [Ch7](Ch07_Extract_Epochs.md) · [Ch8](Ch08_Spectra_TimeFrequency.md) · [Ch9](Ch09_Source_Analysis_DIPFIT.md) · [Ch10–11](Ch10-11_Group_STUDY_Automated_Pipeline.md) · [ROIconnect](Plugin_ROIconnect_Connectivity.md) · [附录对比](Appendix_Comparison_Official_vs_Makoto.md)

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
