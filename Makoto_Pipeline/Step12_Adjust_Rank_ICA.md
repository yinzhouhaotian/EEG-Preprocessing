# Step 12: 为 ICA 调整数据矩阵的有效秩 (Adjust data rank for ICA)

> 所属手册：Makoto's Preprocessing Pipeline 中英对照（由 `Makotos_Preprocessing_Pipeline_CN_EN.md` 按章节拆分）
>
> 章节导航：[00 声明与目录](00_Disclaimer_and_TOC.md) · [Step1](Step01_Double_Precision.md) · [Step2](Step02_Path_Import_icaact_Fix.md) · [Step3](Step03_Downsample.md) · [Step4](Step04_Highpass_1Hz.md) · [Step5](Step05_Channel_Info_EOG.md) · [Step6](Step06_Remove_Bad_Channels.md) · [Step7](Step07_Interpolate_Channels.md) · [Step8](Step08_Average_Reference_FullRank.md) · [Step9](Step09_CleanLine.md) · [Step10](Step10_Epoch_1to2s.md) · [Step11](Step11_Reject_Epochs.md) · [Step12](Step12_Adjust_Rank_ICA.md) · [Step13](Step13_Run_ICA.md) · [Step14-15](Step14-15_Dipole_Fitting.md) · [Step16](Step16_STUDY_No_Double_Dipping.md) · [Step17](Step17_Notes_ASR_ICLabel_SIFT.md) · [附录脚本](Appendix_Full_Batch_Script.md)

* **English Original**:

  When performing ICA, the number of ICs to generate must not exceed the true 'effective rank' of the input data. Your data becomes rank-deficient by:

  1. Re-referencing without including the initial reference (rank deficient by 1);

  2. Interpolating $k$ channels (rank deficient by $k$);

  3. Bridging $n$ channels due to conductive gel spreading (rank deficient by $n-1$).

     Because EEGLAB's spherical spline interpolation is non-linear, `rank()` fails to detect the rank reduction and leaves eigenvalues $< 10^{-6}$, causing **ghost ICs**. Always compute the effective rank using an eigenvalue threshold of $10^{-7}$ (or $10^{-6}$) on the covariance matrix, and pass it to `runica` via the `'pca'` option (or `'pcakeep'` for AMICA).

* **中文译文与原理解析**：

  ICA 分解生成的独立成分数量绝不能超过输入数据的真实**有效秩（Effective Rank）**。不加初始参考的平均重参考会使秩减 1，球面插值 $k$ 个坏导会使有效秩减 $k$，导电膏连桥（Bridging）$n$ 个电极会使秩减 $n-1$。由于 MATLAB 自带的 `rank()` 函数会被球面样条插值产生的微小非线性特征值欺骗，最稳健的做法是直接计算数据协方差矩阵的特征值，统计大于 $10^{-7}$（或 $10^{-6}$）的特征值个数作为真实有效秩 `dataRank`，并在运行 ICA 时通过 `'pca', dataRank` 显式传入。

```
% 使用协方差矩阵特征值阈值 (1e-7) 计算真实的数值有效秩，彻底杜绝幽灵成分 (Ghost ICs)
tmpdata = double(EEG.data(:, :));
covarianceMatrix = cov(tmpdata', 1);
[~, D] = eig(covarianceMatrix);
rankTolerance = 1e-7;
dataRank = sum(diag(D) > rankTolerance);
fprintf('Current effective data rank for ICA: %d (out of %d channels)\n', dataRank, EEG.nbchan);
```
