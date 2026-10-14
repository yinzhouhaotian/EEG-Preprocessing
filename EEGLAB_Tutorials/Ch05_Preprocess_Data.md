# Chapter 5: 数据预处理——滤波、重参考与重采样 (Preprocess Data)

> 所属手册：EEGLAB 官方教程中英对照（由 `README.md` 按章节拆分）
>
> 章节导航：[00 总览](00_Overview_and_Navigation.md) · [Ch1–4](Ch01-04_Data_Management_Import.md) · [Ch5](Ch05_Preprocess_Data.md) · [Ch6](Ch06_Reject_Artifacts_ASR_ICA.md) · [Ch7](Ch07_Extract_Epochs.md) · [Ch8](Ch08_Spectra_TimeFrequency.md) · [Ch9](Ch09_Source_Analysis_DIPFIT.md) · [Ch10–11](Ch10-11_Group_STUDY_Automated_Pipeline.md) · [ROIconnect](Plugin_ROIconnect_Connectivity.md) · [附录对比](Appendix_Comparison_Official_vs_Makoto.md)

## 5.a 时域滤波与连接性分析滤波准则 (Filtering the Data)

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

## 5.b 重参考与重采样 (Re-referencing & Resampling)

* **English Original**:

  Select `Tools -> Re-reference the data` (`pop_reref.m`) to convert the data to common average reference or specific reference channels. In modern EEGLAB automated pipelines, average referencing is often computed twice: once before `clean_rawdata` (because artifact cleaning works better on average-referenced data) and once again after bad channels have been removed (the second average reference undoes the first biased one). EEGLAB also supports robust Huber average referencing (`'huber', 25`) which reduces the influence of outlier channels.

  Select `Tools -> Change sampling rate` (`pop_resample.m`) to downsample high-frequency recordings and speed up analysis.

* **中文译文与操作解析**：

  在 `Tools -> Re-reference the data`（调用 `pop_reref.m`）中可执行全脑平均参考。官方自动化管线提出了一个非常实用的技巧——**“两次平均参考法”**：由于 `clean_rawdata` 在全脑平均参考下识别坏导和突发伪迹更敏锐，可以先做一次初步的全脑平均参考，跑完 `clean_rawdata` 剔除坏导后，**再重新执行第二次全脑平均参考**（由于单极重参考具有线性无记忆可逆性，第二次平均参考会自动抵消第一次包含坏导时的均值偏置）。此外，`pop_reref` 还支持传入 `'huber', 25` 参数启用 Huber 鲁棒均值估计，进一步抗击离群噪声。
