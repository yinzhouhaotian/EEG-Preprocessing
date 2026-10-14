# Step 16: 创建 STUDY 群组分析与避免循环推断 (Create STUDY & Avoid Double Dipping)

> 所属手册：Makoto's Preprocessing Pipeline 中英对照（由 `Makotos_Preprocessing_Pipeline_CN_EN.md` 按章节拆分）
>
> 章节导航：[00 声明与目录](00_Disclaimer_and_TOC.md) · [Step1](Step01_Double_Precision.md) · [Step2](Step02_Path_Import_icaact_Fix.md) · [Step3](Step03_Downsample.md) · [Step4](Step04_Highpass_1Hz.md) · [Step5](Step05_Channel_Info_EOG.md) · [Step6](Step06_Remove_Bad_Channels.md) · [Step7](Step07_Interpolate_Channels.md) · [Step8](Step08_Average_Reference_FullRank.md) · [Step9](Step09_CleanLine.md) · [Step10](Step10_Epoch_1to2s.md) · [Step11](Step11_Reject_Epochs.md) · [Step12](Step12_Adjust_Rank_ICA.md) · [Step13](Step13_Run_ICA.md) · [Step14-15](Step14-15_Dipole_Fitting.md) · [Step16](Step16_STUDY_No_Double_Dipping.md) · [Step17](Step17_Notes_ASR_ICLabel_SIFT.md) · [附录脚本](Appendix_Full_Batch_Script.md)

* **English Original**:

  When creating a STUDY across subjects, it automatically filters ICs based on two criteria: (1) Dipoles with $< 15\%$ residual variance (Artoni et al., 2014); (2) Dipoles located inside the brain volume.

  *Avoid Double Dipping (Circular Inference)*: If you are going to test ERP / ERSP / ITC / PSD differences across conditions at the end of the day, **DO NOT choose any of them to cluster ICs**! Clustering ICs using ERSP or ERP waveforms minimizes within-cluster variance on that exact metric and kicks out dissimilar waveforms, inflating Type I error (false positives, Kriegeskorte et al., 2009). **Solution**: USE ONLY DIPOLE LOCATIONS (`xyz` coordinates) to cluster ICs (Miyakoshi et al., 2020, 2021). Because ICA is completely agnostic to spatial coordinates, clustering solely by dipole 3D location never causes double dipping when testing time-frequency or connectivity metrics.

  *Tip for Time-Frequency (ERSP & ITC) parameters*: Recommend `3 cycles at 3 Hz` for the lowest frequency, and `7–10 cycles at 50 Hz` (i.e., `cycles = [3 0.5]` or `[3 0.8]` in `newtimef`).

* **中文译文与原理解析**：

  在多被试群组分析（STUDY）中，如果直接在 ICA 源空间对独立成分进行 K-means 聚类，**切忌使用 ERP 波形、功率谱（PSD）或时频图（ERSP）特征参与聚类，然后再对聚类后的同一个指标做条件间统计检验**！这种做法属于典型的“双重蘸取 / 循环推断（Double Dipping, Kriegeskorte et al., 2009）”，会人为压低组内方差并导致假阳性率暴增。**唯一合规的做法是：仅使用偶极子的三维空间坐标（Dipole XYZ locations）进行聚类**。

  在进行时频变换（`newtimef`）计算事件相关谱扰动（ERSP）和试次间相干性（ITC）时，推荐将小波周期参数设为在最低频率 3 Hz 处使用 3 个周期，随频率升高线性递增至 50 Hz 处约 7–10 个周期。
