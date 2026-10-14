# Step 5: 导入通道坐标与眼电通道处理 (Import channel info & Dedicated EOG channels)

> 所属手册：Makoto's Preprocessing Pipeline 中英对照（由 `Makotos_Preprocessing_Pipeline_CN_EN.md` 按章节拆分）
>
> 章节导航：[00 声明与目录](00_Disclaimer_and_TOC.md) · [Step1](Step01_Double_Precision.md) · [Step2](Step02_Path_Import_icaact_Fix.md) · [Step3](Step03_Downsample.md) · [Step4](Step04_Highpass_1Hz.md) · [Step5](Step05_Channel_Info_EOG.md) · [Step6](Step06_Remove_Bad_Channels.md) · [Step7](Step07_Interpolate_Channels.md) · [Step8](Step08_Average_Reference_FullRank.md) · [Step9](Step09_CleanLine.md) · [Step10](Step10_Epoch_1to2s.md) · [Step11](Step11_Reject_Epochs.md) · [Step12](Step12_Adjust_Rank_ICA.md) · [Step13](Step13_Run_ICA.md) · [Step14-15](Step14-15_Dipole_Fitting.md) · [Step16](Step16_STUDY_No_Double_Dipping.md) · [Step17](Step17_Notes_ASR_ICLabel_SIFT.md) · [附录脚本](Appendix_Full_Batch_Script.md)

* **English Original**:

  `'Edit' -> 'Channel locations'`. If you have channel labels such as `'Fz' 'Cz' 'Pz'` etc, that means that your channel montage follows International 10-20 / 10-10 / 10-5 system (Oostenveld and Praamstra, 2001). Click `'Look up locs'` and choose `'use MNI coordinate file for BEM dipfit model'`. Don't forget to click `'Opt. head center'`.

  *Do we want to have dedicated EOG channels?*

  If your system spares two electrodes to record EOG: (1) Bipolar referenced EOG; (2) Monopolar referenced EOG sharing the scalp reference; (3) Re-purpose them as scalp EEG channels.

  If you use ICA in your preprocessing, having dedicated EOG electrode(s) is not that necessary because ocular artifacts have broad scalp topography modeled very well by ICA. So (3) is the best answer, and (2) is just as good (using locations AFp9 and AFp10 in the 10-5 system). The worst choice is (1), because by bipolar referencing you lose data dimension by 1 and cannot include them in scalp ICA or average reference.

* **中文译文与原理解析**：

  在 `'Edit' -> 'Channel locations'` 中根据国际 10-5 系统标签自动匹配 MNI 坐标（用于 BEM 偶极子拟合模型），并点击 `'Opt. head center'` 优化球心。

  **关于眼电（EOG）通道的黄金法则**：如果你在预处理中使用 ICA，专门贴双极眼电（Bipolar EOG，即上下眼电或左右眼电互为参考相减）其实是最糟糕的选择，因为双极导联与头皮电极不共享同一个物理参考点，无法纳入全脑平均参考或 ICA 分解。最佳做法是将这些电极改作头皮通道，或者让眼电电极**与头皮脑电共享同一个单极物理参考（Monopolar reference）**（例如贴在 10-5 系统的 `AFp9` 和 `AFp10` 位置），这样它们既能监测眨眼/眼动，又能捕获极具价值的前额叶内侧皮层脑电信号（Delorme et al., 2007）。

```
% 自动查找并匹配 MNI 标准 BEM 头模通道坐标（需将路径替换为你的 EEGLAB 安装路径）
dipfitPath = fileparts(which('dipfitdefs'));
bemFile = fullfile(dipfitPath, 'standard_BEM', 'elec', 'standard_1005.elc');
EEG = pop_chanedit(EEG, 'lookup', bemFile, 'eval', 'chans = pop_chancenter(chans, [], []);');
```
