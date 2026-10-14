# Step 4: 1 Hz 高通滤波 (High-pass filter the data at 1-Hz)

> 所属手册：Makoto's Preprocessing Pipeline 中英对照（由 `Makotos_Preprocessing_Pipeline_CN_EN.md` 按章节拆分）
>
> 章节导航：[00 声明与目录](00_Disclaimer_and_TOC.md) · [Step1](Step01_Double_Precision.md) · [Step2](Step02_Path_Import_icaact_Fix.md) · [Step3](Step03_Downsample.md) · [Step4](Step04_Highpass_1Hz.md) · [Step5](Step05_Channel_Info_EOG.md) · [Step6](Step06_Remove_Bad_Channels.md) · [Step7](Step07_Interpolate_Channels.md) · [Step8](Step08_Average_Reference_FullRank.md) · [Step9](Step09_CleanLine.md) · [Step10](Step10_Epoch_1to2s.md) · [Step11](Step11_Reject_Epochs.md) · [Step12](Step12_Adjust_Rank_ICA.md) · [Step13](Step13_Run_ICA.md) · [Step14-15](Step14-15_Dipole_Fitting.md) · [Step16](Step16_STUDY_No_Double_Dipping.md) · [Step17](Step17_Notes_ASR_ICLabel_SIFT.md) · [附录脚本](Appendix_Full_Batch_Script.md)

## 4.1 为什么针对 ICA、ASR 和 CleanLine 推荐使用 1 Hz 通带边缘？

* **English Original**:

  The purpose of the application of high-pass filter is to remove the 'baseline drift'. It is generally recommended to use lower cutoff frequencies, for example 0.01 Hz (cooperative subjects) – 0.1 Hz (children and patients) (Luck, 2005) than our recommended 1-Hz pass-band edge (equivalent to cutoff frequency of 0.5 Hz @ -6dB). The reason for the 1-Hz pass band edge is because:

  1. ICA is biased toward high amplitude if data length is finite.

  2. EEG data have $1/f$ power spectral density (PSD) curve. The combination of these two facts means that the leftmost values on the PSD plot will have the most influence on your decomposition result, although the most useful EEG information you are probably looking for is in 3–13 Hz (theta and alpha). Therefore, cutting off the leftmost values helps ICA to focus on the important 3–13 Hz.

  3. Low-frequency EEG < 1Hz could be contaminated by sweating etc, which adds spatiotemporal non-stationarity and affects ICA.

  4. Also, the lowest frequency in ERSP (blended wavelet/STFT transform) is typically 3 Hz if you want to have a decent frequency resolution (in EEGLAB parameters, 3 cycle at 3 Hz generates 1116 ms sliding window length). 3 Hz is sufficiently high relative to the 0.5-Hz cutoff.

  5. Winkler et al. (2015) concluded that high-pass filtered data at 1–2 Hz consistently produced good results in terms of SNR, single-trial classification accuracy and the percentage of 'near-dipolar' ICA components.

* **中文译文与原理解析**：

  高通滤波的目的是消除“基线慢漂移”。虽然传统 ERP 教材（如 Luck, 2005）推荐使用 0.01–0.1 Hz 的低截止频率，但在运行 ICA、ASR 和 CleanLine 时，Makoto 强烈推荐设置 **1 Hz 的通带边缘（Pass-band edge，对应 -6 dB 截止频率约为 0.5 Hz）**，原因如下：

  1. **有限长度下 ICA 对高波幅敏感**：在实际有限时长的数据中，ICA 分解会强烈偏向高振幅信号。

  2. **脑电的** $1/f$ **功率谱分布**：脑电功率随频率降低呈指数级增大（$1/f$ 曲线），这意味着功率谱最左端（$<1\text{ Hz}$）的极低频漂移会主导 ICA 的分解结果，尽管我们真正关注的认知节律主要在 3–30 Hz（Theta、Alpha、Beta）。切掉 $<1\text{ Hz}$ 的部分能让 ICA 聚焦于真正的脑振荡。

  3. **消除出汗等非平稳伪迹**：$<1\text{ Hz}$ 的超慢波极易受皮肤出汗、电极极化等时空非平稳噪声污染，破坏 ICA 的平稳性假设。

  4. **对时频分析（ERSP）完全够用**：在计算 ERSP 时，为了兼顾时间窗长度，最低分析频率通常设为 3 Hz（3 Hz 处使用 3 个小波周期对应的滑动窗长已达 1116 ms），0.5 Hz 的截止频率对 3 Hz 以上的功率与连接性分析没有任何负面影响。

  5. **实证文献支持**：Winkler 等人（2015）证实，1–2 Hz 高通滤波能显著提升 ICA 分解出的“近偶极子（near-dipolar）”脑源成分比例及单试次信噪比。

```
% 使用 EEGLAB 默认新 FIR 滤波器进行 1 Hz 通带边缘高通滤波（对应 -6 dB 截止频率为 0.5 Hz）
EEG = pop_eegfiltnew(EEG, 'locutoff', 1, 'plotfreqz', 0);
```

## 4.2 如果在 >1 Hz 数据上训练 ICA 并迁移到 >0.1 Hz 数据会发生什么？(“自助餐停电”比喻)

* **English Original**:

  On the other hand, 1-Hz high-pass filter attenuates (or distorts) low-frequency 'late slow waves' of ERP family, such as N400 or P600 (Rousselet, 2012). To avoid this problem, one may calculate an ICA weight matrix and a sphering matrix with 1-Hz high-pass filtered data, then apply it to 0.1-Hz high-pass filtered data.

  *What happens to the < 1 Hz data if ICA is calculated on > 1 Hz data and applied to 0.1 Hz data?*

  Imagine you are in a buffet party. On a table, there are four big plates of salad, steak, salmon, and a pudding. The moment you reached your arm to the salad plate, suddenly a blackout happens. You take the salad to your plate in the darkness because you remember where the salad plate is. Now power is back: your salad is drenched with mushroom soup that someone spilled in the darkness!

  This is the situation when > 1-Hz ICA is applied to > 0.1 Hz data. ICA is just a spatial filter, like the locations of the four plates on the table. How much mushroom soup (i.e., 0.1–1.0 Hz EEG info not present in the 1-Hz learning data) you get depends on the spatial distribution of the 0.1–1.0 Hz activity. Practically speaking, 0.1–1.0 Hz data is less likely to be completely independent of > 1.0 Hz data, so most likely it does not hurt very much, though strictly speaking you cannot claim theoretical validity of the decomposition between 0.1–1.0 Hz.

* **中文译文与原理解析**：

  如果你必须分析 N400、P600 等晚期慢波 ERP，1 Hz 高通滤波会扭曲慢波波形。常见折中方案是在 1 Hz 滤波数据上计算 ICA 权重矩阵（`icaweights` 和 `icasphere`），再将其复制迁移到 0.1 Hz 滤波的数据集上。

  为了解释这种做法在 0.1–1.0 Hz 频段内的数学本质，Makoto 提出了著名的“自助餐停电比喻”：ICA 本质上是一个只认空间位置的“空间滤波器”（好比你记住了餐桌上沙拉、牛排、三文鱼和布丁四个盘子的空间位置）；在 $>1\text{ Hz}$ 数据上训练 ICA 并应用到 $>0.1\text{ Hz}$ 数据，就好比你在关灯黑暗中凭记忆去夹沙拉（$>1\text{ Hz}$ 空间滤波器），但黑暗中有人把一碗蘑菇汤（$0.1\text{–}1.0\text{ Hz}$ 慢波）洒在了餐桌上——由于 ICA 训练时“看不见”这碗蘑菇汤，凡是空间分布与沙拉重叠的蘑菇汤都会被一并夹走。如果研究重点是 $>3\text{ Hz}$ **的功率与连接性**，无需使用此折中技巧，直接全程使用 1 Hz 高通滤波最为稳妥。
