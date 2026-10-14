# Step 7: 插值恢复被剔除的通道 (Interpolate all the removed channels)

> 所属手册：Makoto's Preprocessing Pipeline 中英对照（由 `Makotos_Preprocessing_Pipeline_CN_EN.md` 按章节拆分）
>
> 章节导航：[00 声明与目录](00_Disclaimer_and_TOC.md) · [Step1](Step01_Double_Precision.md) · [Step2](Step02_Path_Import_icaact_Fix.md) · [Step3](Step03_Downsample.md) · [Step4](Step04_Highpass_1Hz.md) · [Step5](Step05_Channel_Info_EOG.md) · [Step6](Step06_Remove_Bad_Channels.md) · [Step7](Step07_Interpolate_Channels.md) · [Step8](Step08_Average_Reference_FullRank.md) · [Step9](Step09_CleanLine.md) · [Step10](Step10_Epoch_1to2s.md) · [Step11](Step11_Reject_Epochs.md) · [Step12](Step12_Adjust_Rank_ICA.md) · [Step13](Step13_Run_ICA.md) · [Step14-15](Step14-15_Dipole_Fitting.md) · [Step16](Step16_STUDY_No_Double_Dipping.md) · [Step17](Step17_Notes_ASR_ICLabel_SIFT.md) · [附录脚本](Appendix_Full_Batch_Script.md)

* **English Original**:

  There are two primary reasons why you want to interpolate the rejected electrodes before average referencing and ICA:

  1. To minimize a bias in the next average referencing. For example, if there are 64 channels and 16 channels are rejected only from the right hemisphere, the average potential across the electrodes is biased toward the left hemisphere.

  2. The rejected electrodes cannot be recovered after ICA because there is no way to interpolate `EEG.icaweights` or `EEG.icasphere`.

     *Caution on Rank Issue*: EEGLAB's default interpolation (`eeg_interp()`, implementing Perrin et al., 1989 spherical spline interpolation with default parameters $m=4, n=7$; note Kang et al., 2015 recommend $m=3, n=50$ for phase analysis) introduces a rank issue because non-linearly interpolated data does not cause a clean rank deficiency; instead, it adds an additional dimension whose eigenvalue is near-zero ($< 10^{-7}$), making the problem ill-conditioned and causing **ghost IC problems** if PCA rank adjustment is not explicitly used during ICA!

* **中文译文与原理解析**：

  在全脑平均重参考之前对坏导进行球面样条插值（Spherical Spline Interpolation，基于 Perrin et al., 1989，默认阶数 $m=4$、截断项数 $n=7$；若做电极间相位连接分析，Kang et al., 2015 证明 $m=3, n=50$ 能最小化相位插值伪迹）有两个原因：一是防止某侧半球剔除通道过多导致全脑平均电位向另一侧半球偏置；二是便于后续群组分析时通道维度对齐。

  **重要方法学警告（插值引发的秩亏缺与连接性污染）**：

  1. **对 ICA 的影响**：球面样条插值属于非线性插值，不会产生干净的零特征值，而是产生约 $10^{-8}$ 的极小特征值，导致 EEGLAB 内置的 `rank()` 检查器误以为数据仍是满秩，从而在运行 ICA 时分解出病态的“幽灵成分（Ghost ICs）”！因此，若在 ICA 前进行了插值，**必须在运行 ICA 时用 `'pca'` 参数显式扣减被插值的通道数**。

  2. **对传感器级连接性的影响**：插值通道是由周围好导拟合而成的虚拟信号，若在传感器层面直接计算通道间功能连接（如相干性、PLV），切勿将被插值通道作为独立网络节点纳入统计，否则会与邻近通道产生极高的假阳性连接。

```
% 使用备份的 originalEEG.chanlocs 进行球面样条插值恢复缺失通道
EEG = pop_interp(EEG, originalEEG.chanlocs, 'spherical');
```
