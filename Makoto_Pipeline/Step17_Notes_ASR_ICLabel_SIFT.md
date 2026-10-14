# Step 17: 进阶笔记：ASR 自动管线、ICLabel 自动筛选与 SIFT 连接性准则 (Notes & Automated Pipelines)

> 所属手册：Makoto's Preprocessing Pipeline 中英对照（由 `Makotos_Preprocessing_Pipeline_CN_EN.md` 按章节拆分）
>
> 章节导航：[00 声明与目录](00_Disclaimer_and_TOC.md) · [Step1](Step01_Double_Precision.md) · [Step2](Step02_Path_Import_icaact_Fix.md) · [Step3](Step03_Downsample.md) · [Step4](Step04_Highpass_1Hz.md) · [Step5](Step05_Channel_Info_EOG.md) · [Step6](Step06_Remove_Bad_Channels.md) · [Step7](Step07_Interpolate_Channels.md) · [Step8](Step08_Average_Reference_FullRank.md) · [Step9](Step09_CleanLine.md) · [Step10](Step10_Epoch_1to2s.md) · [Step11](Step11_Reject_Epochs.md) · [Step12](Step12_Adjust_Rank_ICA.md) · [Step13](Step13_Run_ICA.md) · [Step14-15](Step14-15_Dipole_Fitting.md) · [Step16](Step16_STUDY_No_Double_Dipping.md) · [Step17](Step17_Notes_ASR_ICLabel_SIFT.md) · [附录脚本](Appendix_Full_Batch_Script.md)

## 17.1 基于 ASR 与 ICLabel 的现代 15 步全自动管线 (Suggested Automated Pipeline)

* **English Original**:

  In high-density EEG, rejecting an entire epoch whenever a single channel has a brief artifact wastes too much data. Using **Artifact Subspace Reconstruction (ASR)** in `clean_rawdata()` (with empirically validated threshold $\text{SD} = 20$, Chang et al., 2020; make sure to uncheck `'Remove bad data periods'` so ASR repairs bursts rather than chopping up the data) followed by automated component classification via **`ICLabel()`** provides a reproducible automated pipeline:

  1. Set double precision -> 2. Import data -> 3. Downsample -> 4. High-pass filter at 1 Hz -> 5. Import channel info -> 6. Bad channel rejection -> 7. CleanLine -> 8. Apply ASR (`SD = 20`) to repair continuous bursts -> 9. Interpolate removed channels -> 10. Full-rank average reference -> 11. Run ICA with `'pca'` adjusted to effective rank -> 12. Fit single dipoles (DIPFIT) -> 13. Fit bilateral dipoles -> 14. Automated IC selection using `ICLabel()` -> 15. Epoch cleaned data (e.g., -1 to 2 sec).

* **中文译文与原理解析**：

  针对通道数较多或任务试次珍贵的数据，Makoto 推荐结合 ASR（伪迹子空间重构，阈值设为 `SD = 20`，仅修复不删时间段）与 ICLabel（基于深度学习的自动独立成分分类器）构建全自动批处理管线。在通过 `ICLabel` 筛选成分时，标准准则为：**保留“脑源（Brain）”分类概率** $\ge 0.70$ **且偶极子残差方差** $\text{RV} < 0.15$**（且偶极子位于脑内）的成分**（若你的目标是仅剔除眼电/肌电等明确伪迹并尽量保留全部脑信号，也可采取“反向剔除法”：仅剔除 Eye / Muscle / Heart / Line Noise / Channel Noise 概率 $> 0.70$ 或 $0.80$ 的伪迹成分）。

```
% 使用 ICLabel 自动分类独立成分并筛选高质量脑源成分（概率 >= 0.7 且偶极子残差方差 RV < 0.15）
EEG = iclabel(EEG, 'default');
brainIdx  = find(EEG.etc.ic_classification.ICLabel.classifications(:, 1) >= 0.70);
rvList    = [EEG.dipfit.model.rv];
goodRvIdx = find(rvList < 0.15);
goodIcIdx = intersect(brainIdx, goodRvIdx);

% 仅保留筛选出的高质量脑源成分，将其余伪迹成分从通道数据中减去
EEG = pop_subcomp(EEG, goodIcIdx, 0, 1);
EEG.etc.ic_classification.ICLabel.classifications = ...
    EEG.etc.ic_classification.ICLabel.classifications(goodIcIdx, :);
```

## 17.2 针对连接性分析（SIFT / 多变量格兰杰因果）的专属预处理准则 (SIFT & Connectivity Tips)

* **English Original**:

  1. *Why avoid sensor-level connectivity directly?* Calculating connectivity directly at the scalp sensor level suffers severely from **volume conduction** (Brunner et al., 2016). Decomposing data into temporally independent sources via ICA (and running SIFT on ICs) or projecting to cortical source space addresses volume conduction.

  2. *What filter should be used for Granger Causality / MVAR?* While Barnett and Seth (2011) showed multivariate Granger causality is theoretically invariant under zero-phase filtering, in practice **filtering complicates the power spectral density (PSD) and inflates the required MVAR model order**: steep roll-offs, stopband floors, and deep spectral holes created by notch filters all worsen model order estimation! Therefore, NEVER use a notch filter or steep low-pass filter before MVAR connectivity. Use a gentle high-pass filter (1 Hz) to ensure stationarity, and use `CleanLine` if needed.

  3. *Downsample data to 100 Hz (or 128 Hz) to keep PSD simple*: Downsampling to \~100 Hz pushes the 50/60 Hz line noise near or outside the Nyquist frequency and keeps the PSD smooth, allowing a much lower and more stable MVAR model order. Use custom anti-aliasing parameters so the stopband does not fall below the Nyquist frequency: `EEG = pop_resample(EEG, 100, 0.8, 0.4);` (for 100 Hz target rate, Nyquist is 50 Hz, -6 dB cutoff is $50 \times 0.8 = 40\text{ Hz}$, transition bandwidth is $50 \times 0.4 = 20\text{ Hz}$, so passband edge is 30 Hz and stopband hits 50 Hz).

  4. *Datapoint-to-parameter ratio*: To reliably fit an MVAR model, the ratio `(num_IC * model_order) / (window_length_samples * num_trials)` should be $< 0.1$ (at least 10 data points per estimated parameter). Combining trials or using longer sliding windows improves model stability.

* **中文译文与原理解析（专为你的“任务态功率与连接性”研究划重点）**：

  1. **克服容积传导**：直接在头皮电极上算连接性会受到容积传导的严重干扰（Brunner et al., 2016），建议在 ICA 独立成分空间（使用 EEGLAB 的 SIFT 工具箱）或源定位空间（使用 FieldTrip 的 Beamformer）计算连接性，或者在传感器空间仅使用去零延迟指标（如 wPLI、相干性虚部 iCoh）。

  2. **连接性分析的滤波禁忌**：虽然理论上零相位滤波不改变因果方向（Barnett & Seth, 2011），但在实际计算自回归模型（MVAR / 格兰杰因果）时，**任何陡峭的低通滤波或 50 Hz 陷波滤波都会在频谱上留下阻带平底或深坑，导致自回归模型阶数（Model Order）急剧膨胀甚至拟合失败**！因此做连接性时应只做温和的 1 Hz 高通滤波以保证平稳性，严禁使用传统陷波滤波器。

  3. **100 Hz 定制降采样技巧**：如果主要关注 3–40 Hz（Theta / Alpha / Beta / 低 Gamma）的功率与连接性，且 50 Hz 工频干扰极强，Makoto 推荐使用 `EEG = pop_resample(EEG, 100, 0.8, 0.4);` 将采样率降至 100 Hz。该命令将抗混叠滤波器的 -6 dB 截止点设在 40 Hz、过渡带宽度设为 20 Hz（即 30 Hz 以下完全无损通过，到 50 Hz 奈奎斯特频率处刚好衰减至阻带），既能完美避开 50 Hz 市电干扰，又能让功率谱保持平滑，大幅降低连接性建模难度。
