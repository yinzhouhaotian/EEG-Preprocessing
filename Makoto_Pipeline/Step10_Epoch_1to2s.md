# Step 10: 数据分段至 -1 到 2 秒 (Epoch data to -1 to 2 sec)

> 所属手册：Makoto's Preprocessing Pipeline 中英对照（由 `Makotos_Preprocessing_Pipeline_CN_EN.md` 按章节拆分）
>
> 章节导航：[00 声明与目录](00_Disclaimer_and_TOC.md) · [Step1](Step01_Double_Precision.md) · [Step2](Step02_Path_Import_icaact_Fix.md) · [Step3](Step03_Downsample.md) · [Step4](Step04_Highpass_1Hz.md) · [Step5](Step05_Channel_Info_EOG.md) · [Step6](Step06_Remove_Bad_Channels.md) · [Step7](Step07_Interpolate_Channels.md) · [Step8](Step08_Average_Reference_FullRank.md) · [Step9](Step09_CleanLine.md) · [Step10](Step10_Epoch_1to2s.md) · [Step11](Step11_Reject_Epochs.md) · [Step12](Step12_Adjust_Rank_ICA.md) · [Step13](Step13_Run_ICA.md) · [Step14-15](Step14-15_Dipole_Fitting.md) · [Step16](Step16_STUDY_No_Double_Dipping.md) · [Step17](Step17_Notes_ASR_ICLabel_SIFT.md) · [附录脚本](Appendix_Full_Batch_Script.md)

* **English Original**:

  If you have sufficient number of data points after epoching, epoching before ICA is recommended so that ICA can focus on peri-event brain dynamics. If your Stimulus Onset Asynchrony (SOA) is shorter than 3 seconds or data points are insufficient, do NOT epoch before ICA—use continuous data to perform ICA, then epoch, because overlapping epochs submitted to ICA will cause it to learn the duplicated part as positively weighted data.

  *Why -1 to 2 sec for Time-Frequency (ERSP/ITC)?*

  This phenomenon of shortening the epoch after wavelet transform is related to the **Cone of Influence (COI)**. With a 3-cycle wavelet at 3 Hz (at 250 Hz sampling rate), the wavelet sliding window length is $1116\text{ ms}$ ($279\text{ samples}$). You lose half of the window length ($556\text{ ms}$) from the beginning and half ($556\text{ ms}$) from the ending of the epoch! Thus, epoching from $-1000\text{ ms}$ to $+2000\text{ ms}$ leaves you with an effective time-frequency window of roughly $-444\text{ ms}$ to $+1444\text{ ms}$.

  *Crucial Baseline Rule before ICA*: Do NOT subtract a short baseline (such as $-100$ to $0\text{ ms}$) before running ICA! David Groppe et al. (2009) showed that subtracting a short baseline before ICA severely degrades ICA reliability because background alpha rhythms randomly shift the short-window mean across channels. Since the data is already 1-Hz high-pass filtered (zero-mean), baseline subtraction before ICA is completely unnecessary.

* **中文译文与原理解析**：

  在分段（Epoching）环节有三条针对时频功率与 ICA 的核心准则：

  1. **何时在 ICA 前分段 vs. 连续数据跑 ICA**：如果试次间间隔（SOA）较长且分段后数据点充足，在 ICA 前分段可让 ICA 专注于任务事件周边的脑动态；但如果你的实验刺激间隔较短（导致相邻 Epoch 时间窗重叠）或任务试次较少，**切勿在 ICA 前分段**（重叠的数据点会让 ICA 重复学习相同片段），应直接在连续数据上跑完 ICA 后再分段。

  2. **为什么时频分析（ERSP/ITC）必须预留超过 0.5 秒的缓冲期（影响锥 COI）**：小波变换的最低频率决定了滑动窗口的宽度。例如最低分析频率为 $3\text{ Hz}$、使用 $3$ 个周期的小波时，其时间窗宽度为 $3 \times (1000 / 3) \approx 1116\text{ ms}$。由于滑动窗中心在抵达试次首尾两端各一半窗宽（约 $556\text{ ms}$）处就无法继续向外滑动，算出的时频图首尾两端会各被裁掉 $556\text{ ms}$！因此，截取 $-1000\text{ ms}$ 到 $+2000\text{ ms}$ 的分段，在小波变换后实际只剩下约 $-444\text{ ms}$ 到 $+1444\text{ ms}$ 的有效时间窗。

  3. **严禁在 ICA 前减去短时域基线**：Groppe 等人（2009，*NeuroImage*）证实，如果在 ICA 前减去 $-100\text{ 至 }0\text{ ms}$（或 $-200\text{ 至 }0\text{ ms}$）的短基线均值，由于背景 Alpha 波在该短窗口内的随机相位波动，会给每个通道人为注入独立的直流偏移，严重破坏 ICA 分解的可靠性。只要之前做过了 1 Hz 高通滤波，数据本身就是零均值的，**在 ICA 前不需要做基线校正**。

```
% 围绕目标事件标记分段（例如 -1.0 秒至 +2.0 秒），注意此时不执行短基线相减
EEG = pop_epoch(EEG, {'S1', 'S2'}, [-1.0 2.0], 'newname', 'Epoched_EEG', 'epochinfo', 'yes');
```
