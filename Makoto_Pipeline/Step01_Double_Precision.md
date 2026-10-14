# Step 1: 更改选项以使用双精度运算 (Change the option to use double precision)

> 所属手册：Makoto's Preprocessing Pipeline 中英对照（由 `Makotos_Preprocessing_Pipeline_CN_EN.md` 按章节拆分）
>
> 章节导航：[00 声明与目录](00_Disclaimer_and_TOC.md) · [Step1](Step01_Double_Precision.md) · [Step2](Step02_Path_Import_icaact_Fix.md) · [Step3](Step03_Downsample.md) · [Step4](Step04_Highpass_1Hz.md) · [Step5](Step05_Channel_Info_EOG.md) · [Step6](Step06_Remove_Bad_Channels.md) · [Step7](Step07_Interpolate_Channels.md) · [Step8](Step08_Average_Reference_FullRank.md) · [Step9](Step09_CleanLine.md) · [Step10](Step10_Epoch_1to2s.md) · [Step11](Step11_Reject_Epochs.md) · [Step12](Step12_Adjust_Rank_ICA.md) · [Step13](Step13_Run_ICA.md) · [Step14-15](Step14-15_Dipole_Fitting.md) · [Step16](Step16_STUDY_No_Double_Dipping.md) · [Step17](Step17_Notes_ASR_ICLabel_SIFT.md) · [附录脚本](Appendix_Full_Batch_Script.md)

* **English Original**:

  In EEGLAB2019, `'File' -> 'Preferences'`. In EEGLAB 14, from main GUI top left tab, `'File' -> 'Memory and other options' -> 'If set, use single precision under...'` uncheck it. Note that when computing ICA etc where double precision is necessary, EEGLAB functions internally convert input data to double precision. So mostly this is taken care of automatically as long as you stick to GUI operations. Note that if you want to run calculation that involves matrix operation, you have to check whether the input data is always converted to double at your own risk. Otherwise you will encounter problems when data rank is calculated with single vs. double precisions right after importing it from `.raw` file.

* **中文译文与原理解析**：

  在 EEGLAB 2019 及更新版本中，进入菜单 `'File' -> 'Preferences'`（旧版 EEGLAB 14 为 `'File' -> 'Memory and other options'`），**取消勾选“使用单精度（single precision）”选项**，确保全程使用双精度（double precision）。虽然通过 GUI 运行 ICA 时 EEGLAB 内部会自动将数据转为双精度，但如果你自己编写批处理脚本进行矩阵运算（例如刚导入数据时用 `rank(double(EEG.data))` 计算矩阵秩、协方差矩阵特征值分解或空间滤波），单精度浮点数极易因数值截断导致矩阵秩计算错误。

```
% 设置 EEGLAB 使用双精度并保留独立成分激活矩阵 (EEG.icaact)
pop_editoptions('option_single', false, 'option_computeica', true);
```
