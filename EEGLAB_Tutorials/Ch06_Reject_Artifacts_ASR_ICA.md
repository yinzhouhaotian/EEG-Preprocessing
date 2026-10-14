# Chapter 6: 伪迹剔除——ASR 自动清洗、ICA 与 ICLabel (Reject Artifacts)

> 所属手册：EEGLAB 官方教程中英对照（由 `README.md` 按章节拆分）
>
> 章节导航：[00 总览](00_Overview_and_Navigation.md) · [Ch1–4](Ch01-04_Data_Management_Import.md) · [Ch5](Ch05_Preprocess_Data.md) · [Ch6](Ch06_Reject_Artifacts_ASR_ICA.md) · [Ch7](Ch07_Extract_Epochs.md) · [Ch8](Ch08_Spectra_TimeFrequency.md) · [Ch9](Ch09_Source_Analysis_DIPFIT.md) · [Ch10–11](Ch10-11_Group_STUDY_Automated_Pipeline.md) · [ROIconnect](Plugin_ROIconnect_Connectivity.md) · [附录对比](Appendix_Comparison_Official_vs_Makoto.md)

## 6.c 使用 `clean_rawdata` 与 ASR 进行自动伪迹剔除 (Automated Artifact Rejection)

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

## 6.d 独立成分分析（ICA）原理、质量优化与 ICLabel 自动分类 (Independent Component Analysis)

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
