# Step 11: 剔除极端坏段试次 (Reject epochs for cleaning)

> 所属手册：Makoto's Preprocessing Pipeline 中英对照（由 `Makotos_Preprocessing_Pipeline_CN_EN.md` 按章节拆分）
>
> 章节导航：[00 声明与目录](00_Disclaimer_and_TOC.md) · [Step1](Step01_Double_Precision.md) · [Step2](Step02_Path_Import_icaact_Fix.md) · [Step3](Step03_Downsample.md) · [Step4](Step04_Highpass_1Hz.md) · [Step5](Step05_Channel_Info_EOG.md) · [Step6](Step06_Remove_Bad_Channels.md) · [Step7](Step07_Interpolate_Channels.md) · [Step8](Step08_Average_Reference_FullRank.md) · [Step9](Step09_CleanLine.md) · [Step10](Step10_Epoch_1to2s.md) · [Step11](Step11_Reject_Epochs.md) · [Step12](Step12_Adjust_Rank_ICA.md) · [Step13](Step13_Run_ICA.md) · [Step14-15](Step14-15_Dipole_Fitting.md) · [Step16](Step16_STUDY_No_Double_Dipping.md) · [Step17](Step17_Notes_ASR_ICLabel_SIFT.md) · [附录脚本](Appendix_Full_Batch_Script.md)

* **English Original**:

  Aim for around 5–10% rejection rate (Delorme et al., 2007). Apply amplitude threshold of $-500$ to $500\,\mu\text{V}$ (don't capture eye blinks here; eye blinks will be removed by ICA), reject the selected epochs, and apply improbability test with $6\text{ SD}$ for single channels and $2\text{ SD}$ for all channels, and reject the selected again.

* **中文译文与原理解析**：

  在送入 ICA 前剔除坏段的目标是**清除罕见的非生物大振幅突变（如电极线剧烈晃动、吞咽动作）**，而不是剔除眨眼（眨眼具有极稳定的空间拓扑，留给 ICA 去除即可）。因此，在 ICA 前使用宽松的波幅阈值（如 $\pm 500\,\mu\text{V}$）配合联合概率分布检验（单通道 $6\text{ SD}$，全通道 $2\text{ SD}$），将总试次剔除率控制在 5%–10% 左右；待 ICA 去除眼电和肌电后，再用严格阈值（如 $\pm 100\,\mu\text{V}$）做最终质控。

```
% ICA 前预清洗：剔除波幅超出 [-500, 500] uV 及联合概率异常（单通道 6 SD, 全通道 2 SD）的极端坏段
EEG = pop_eegthresh(EEG, 1, 1:EEG.nbchan, -500, 500, EEG.xmin, EEG.xmax, 0, 1);
EEG = pop_jointprob(EEG, 1, 1:EEG.nbchan, 6, 2, 0, 1, 0, [], 0);
```
