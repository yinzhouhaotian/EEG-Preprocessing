# Step 3: 按需降采样 (Downsample if necessary)

> 所属手册：Makoto's Preprocessing Pipeline 中英对照（由 `Makotos_Preprocessing_Pipeline_CN_EN.md` 按章节拆分）
>
> 章节导航：[00 声明与目录](00_Disclaimer_and_TOC.md) · [Step1](Step01_Double_Precision.md) · [Step2](Step02_Path_Import_icaact_Fix.md) · [Step3](Step03_Downsample.md) · [Step4](Step04_Highpass_1Hz.md) · [Step5](Step05_Channel_Info_EOG.md) · [Step6](Step06_Remove_Bad_Channels.md) · [Step7](Step07_Interpolate_Channels.md) · [Step8](Step08_Average_Reference_FullRank.md) · [Step9](Step09_CleanLine.md) · [Step10](Step10_Epoch_1to2s.md) · [Step11](Step11_Reject_Epochs.md) · [Step12](Step12_Adjust_Rank_ICA.md) · [Step13](Step13_Run_ICA.md) · [Step14-15](Step14-15_Dipole_Fitting.md) · [Step16](Step16_STUDY_No_Double_Dipping.md) · [Step17](Step17_Notes_ASR_ICLabel_SIFT.md) · [附录脚本](Appendix_Full_Batch_Script.md)

* **English Original**:

  You may downsample the data to around 250Hz if the original sampling frequency is higher than that. Usually low-pass filter is necessary before downsampling for anti-aliasing, but EEGLAB function applies the anti-aliasing filter automatically. Downsampling is useful to compress the data size. It also helps ICA to produce better decomposition by cutting off unnecessary high-frequency information, though we have not tested it quantitatively.

* **中文译文与原理解析**：

  如果原始采样率较高（例如 1000 Hz），可以将连续数据降采样至 **250 Hz**（若原始为 512/1024 Hz 则可降至 256 Hz；若做 SIFT 格兰杰因果连接性分析可降至 100–128 Hz）。降采样前必须进行抗混叠低通滤波（Anti-aliasing low-pass filter），而 EEGLAB 的 `pop_resample()` 函数会自动内置执行抗混叠滤波。降采样不仅能大幅压缩数据体积、加速后续计算，还能通过滤除不必要的高频噪声来帮助 ICA 获得更好的分解质量。

```
% 将连续脑电数据降采样至 250 Hz（内置自动抗混叠低通滤波）
EEG = pop_resample(EEG, 250);
```
