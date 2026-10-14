# Step 14 & Step 15: 头模配准与单/双侧等效电流偶极子拟合 (Dipole Fitting with DIPFIT)

> 所属手册：Makoto's Preprocessing Pipeline 中英对照（由 `Makotos_Preprocessing_Pipeline_CN_EN.md` 按章节拆分）
>
> 章节导航：[00 声明与目录](00_Disclaimer_and_TOC.md) · [Step1](Step01_Double_Precision.md) · [Step2](Step02_Path_Import_icaact_Fix.md) · [Step3](Step03_Downsample.md) · [Step4](Step04_Highpass_1Hz.md) · [Step5](Step05_Channel_Info_EOG.md) · [Step6](Step06_Remove_Bad_Channels.md) · [Step7](Step07_Interpolate_Channels.md) · [Step8](Step08_Average_Reference_FullRank.md) · [Step9](Step09_CleanLine.md) · [Step10](Step10_Epoch_1to2s.md) · [Step11](Step11_Reject_Epochs.md) · [Step12](Step12_Adjust_Rank_ICA.md) · [Step13](Step13_Run_ICA.md) · [Step14-15](Step14-15_Dipole_Fitting.md) · [Step16](Step16_STUDY_No_Double_Dipping.md) · [Step17](Step17_Notes_ASR_ICLabel_SIFT.md) · [附录脚本](Appendix_Full_Batch_Script.md)

* **English Original**:

  `'Tools' -> 'Locate dipoles using DIPFIT 2.x' -> 'Head model and settings'`, then `'Autofit (coarse fit, fine fit & plot)'`. Note that EEGLAB's head model uses `millimeter (mm)` as default unit; if all your fitted dipoles cluster at the very center of the head, your electrode coordinates are in `cm` or `m`—multiply `X, Y, Z` by `10` or `1000`.

  After fitting single dipoles, run the `fitTwoDipoles` plugin (`EEG = fitTwoDipoles(EEG, 'LRR', 35);`, Piazza et al., 2016) to capture symmetrically constrained bilateral sources (such as bilateral occipital alpha or auditory cortex sources).

* **中文译文与原理解析**：

  为什么要做偶极子拟合（DIPFIT）？因为真正的皮层脑源成分在头皮上的拓扑投影具有高度的“偶极子性（Dipolarity）”，通过拟合等效电流偶极子并计算**残差方差（Residual Variance, RV，即理论偶极子投影与实际 IC 拓扑之差的方差占比）**，我们可以用客观定量指标（通常要求 $\text{RV} < 15\%$ 且偶极子位于脑实质内）筛选高质量脑成分，并为源空间连接性分析（如 SIFT）提供三维空间坐标。此外，调用 `fitTwoDipoles` 插件可进一步拟合左右半球对称激活的双侧同步脑源。

```
% 配置 MNI 标准四层 BEM 头模型并进行单偶极子自动拟合 (DIPFIT)
dipfitPath = fileparts(which('dipfitdefs'));
EEG = pop_dipfit_settings(EEG, ...
    'hdmfile', fullfile(dipfitPath, 'standard_BEM', 'standard_vol.mat'), ...
    'coordformat', 'MNI', ...
    'mrifile', fullfile(dipfitPath, 'standard_BEM', 'standard_mri.mat'), ...
    'chanfile', fullfile(dipfitPath, 'standard_BEM', 'elec', 'standard_1005.elc'), ...
    'coord_transform', [0 0 0 0 0 -1.5708 1 1 1], ...
    'chansel', 1:EEG.nbchan);

% 自动执行粗拟合与精拟合，设置初始剔除阈值为 100%（保留所有偶极子以便后续筛选）
EEG = pop_multifit(EEG, 1:size(EEG.icaweights, 1), 'threshold', 100, 'plotopt', {'normlen', 'on'});

% （可选，需安装 fitTwoDipoles 插件）搜索并拟合对称双侧偶极子
if exist('fitTwoDipoles', 'file')
    EEG = fitTwoDipoles(EEG, 'LRR', 35);
end
```
