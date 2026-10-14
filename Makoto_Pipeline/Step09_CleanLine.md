# Step 9: 使用 CleanLine 去除工频噪声 (Remove line noise using CleanLine)

> 所属手册：Makoto's Preprocessing Pipeline 中英对照（由 `Makotos_Preprocessing_Pipeline_CN_EN.md` 按章节拆分）
>
> 章节导航：[00 声明与目录](00_Disclaimer_and_TOC.md) · [Step1](Step01_Double_Precision.md) · [Step2](Step02_Path_Import_icaact_Fix.md) · [Step3](Step03_Downsample.md) · [Step4](Step04_Highpass_1Hz.md) · [Step5](Step05_Channel_Info_EOG.md) · [Step6](Step06_Remove_Bad_Channels.md) · [Step7](Step07_Interpolate_Channels.md) · [Step8](Step08_Average_Reference_FullRank.md) · [Step9](Step09_CleanLine.md) · [Step10](Step10_Epoch_1to2s.md) · [Step11](Step11_Reject_Epochs.md) · [Step12](Step12_Adjust_Rank_ICA.md) · [Step13](Step13_Run_ICA.md) · [Step14-15](Step14-15_Dipole_Fitting.md) · [Step16](Step16_STUDY_No_Double_Dipping.md) · [Step17](Step17_Notes_ASR_ICLabel_SIFT.md) · [附录脚本](Appendix_Full_Batch_Script.md)

* **English Original**:

  CleanLine (developed by Tim Mullen) is not a standard frequency notch filter, but uses a sliding window and multitapers to adaptively estimate sine wave amplitude to subtract. It does not make a hole in the background EEG spectrum.

  *Critical Bug Warning*: The original implementation of CleanLine suffered from a bug. In the newer plugin version, you MUST check the very last checkbox `'Use new implementation (send us feedback)'` (setting `legacy` to `false` / using PREP's `cleanLineNoise` implementation). By default it is set to `false`, which completely destroys the effect of CleanLine! Note that CleanLine assumes the 50/60 Hz line noise amplitude envelope is stationary within the sliding window (default 4 s); performing average referencing before CleanLine helps remove non-stationary common-mode line noise.

* **中文译文与原理解析**：

  传统的 50/60 Hz 陷波滤波器（Notch Filter）会在背景脑电频谱上挖出一个深坑，并造成时域振铃失真与自回归模型阶数膨胀。`CleanLine` 插件利用滑动窗口与多锥度谱（Multitaper）自适应拟合确定性的正弦工频干扰并从原信号中减去，不会损伤同一频段的随机脑电活动。

  **防坑必看**：旧版 `CleanLine` 存在一个未报错的代码 Bug，导致去工频效果大打折扣。在使用新版 `CleanLine` 时，**必须在 GUI 最底部勾选 `'Use new implementation'`**（或在代码中调用修复后的 `cleanLineNoise` 实现）。另外，先做完第 8 步的全脑平均参考再跑 `CleanLine`，能先消除共模工频波动，显著提升 `CleanLine` 的平稳拟合效果。

```
% 使用 CleanLine 去除 50 Hz 及 100 Hz 谐波工频干扰（我国市电为 50 Hz，北美为 60 Hz）
EEG = pop_cleanline(EEG, 'bandwidth', 2, 'chanlist', 1:EEG.nbchan, ...
    'computepower', 1, 'linefreqs', [50 100], 'newversion', 1, ...
    'normSpectrum', 0, 'p', 0.01, 'pad', 2, 'plotfigures', 0, ...
    'scanforlines', 0, 'sigtype', 'Channels', 'taperbandwidth', 2, ...
    'tau', 100, 'verb', 1, 'winsize', 4, 'winstep', 4);
```
