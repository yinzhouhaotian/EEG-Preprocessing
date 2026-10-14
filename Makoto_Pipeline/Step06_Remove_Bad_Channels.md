# Step 6: 剔除坏导 (Remove bad channels)

> 所属手册：Makoto's Preprocessing Pipeline 中英对照（由 `Makotos_Preprocessing_Pipeline_CN_EN.md` 按章节拆分）
>
> 章节导航：[00 声明与目录](00_Disclaimer_and_TOC.md) · [Step1](Step01_Double_Precision.md) · [Step2](Step02_Path_Import_icaact_Fix.md) · [Step3](Step03_Downsample.md) · [Step4](Step04_Highpass_1Hz.md) · [Step5](Step05_Channel_Info_EOG.md) · [Step6](Step06_Remove_Bad_Channels.md) · [Step7](Step07_Interpolate_Channels.md) · [Step8](Step08_Average_Reference_FullRank.md) · [Step9](Step09_CleanLine.md) · [Step10](Step10_Epoch_1to2s.md) · [Step11](Step11_Reject_Epochs.md) · [Step12](Step12_Adjust_Rank_ICA.md) · [Step13](Step13_Run_ICA.md) · [Step14-15](Step14-15_Dipole_Fitting.md) · [Step16](Step16_STUDY_No_Double_Dipping.md) · [Step17](Step17_Notes_ASR_ICLabel_SIFT.md) · [附录脚本](Appendix_Full_Batch_Script.md)

* **English Original**:

  What do you mean bad here? In short, the channels that you can't save even if you reject 5–10% of your datapoints. Removing bad channels is a critical step particularly for average referencing. This is because average reference signal is an average of all channels. If you have channels that are noisy all the time, including such channels to average will introduce noise to all the channels (see Nima's PREP pipeline paper, Bigdely-Shamlo et al., 2015).

  For objective rejection criteria, check out: (1) Nima's PREP pipeline; (2) Christian's `clean_rawdata()` plugin; (3) Makoto's `trimOutlier()`. In writing batch scripts, keep the original `chanlocs` structure (`originalEEG = EEG;`) before channel rejection so that you can refer to it later for channel interpolation.

* **中文译文与原理解析**：

  什么是“坏导”？简言之，就是哪怕你删掉 5%–10% 的时间点也依然救不回来的高噪声或断路（平线）通道。**在进行全脑平均重参考（Average Referencing）之前，必须先剔除坏导！** 因为全脑平均参考会计算所有通道的均值并从每个通道中减去；如果保留了一个持续高噪声的坏导，它的噪声就会通过均值计算扩散污染到全脑每一个好通道中。在写批处理脚本时，务必在剔除坏导前先备份原始通道坐标（`originalEEG = EEG;`），以便后续插值时作为完整坐标模板。

```
% 备份原始完整通道结构，以便后续球面插值使用
originalEEG = EEG;

% 使用 clean_rawdata 仅执行平线通道与高噪坏导剔除（暂不开启 ASR 与时间窗裁剪）
EEG = pop_clean_rawdata(EEG, ...
    'FlatlineCriterion', 5, ...
    'ChannelCriterion', 0.8, ...
    'LineNoiseCriterion', 4, ...
    'Highpass', 'off', ...
    'BurstCriterion', 'off', ...
    'WindowCriterion', 'off', ...
    'BurstRejection', 'off', ...
    'Distance', 'Euclidian');
```
