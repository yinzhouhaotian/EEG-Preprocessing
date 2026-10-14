# Chapter 1–4: 数据结构与导入规范 (Dataset Management & Importing Data)

> 所属手册：EEGLAB 官方教程中英对照（由 `README.md` 按章节拆分）
>
> 章节导航：[00 总览](00_Overview_and_Navigation.md) · [Ch1–4](Ch01-04_Data_Management_Import.md) · [Ch5](Ch05_Preprocess_Data.md) · [Ch6](Ch06_Reject_Artifacts_ASR_ICA.md) · [Ch7](Ch07_Extract_Epochs.md) · [Ch8](Ch08_Spectra_TimeFrequency.md) · [Ch9](Ch09_Source_Analysis_DIPFIT.md) · [Ch10–11](Ch10-11_Group_STUDY_Automated_Pipeline.md) · [ROIconnect](Plugin_ROIconnect_Connectivity.md) · [附录对比](Appendix_Comparison_Official_vs_Makoto.md)

* **English Original**:

  Welcome to the EEGLAB tutorial. The EEGLAB Tutorial is split into core single-subject processing steps, group analysis (`STUDY`), scripting, and Concepts Guides.

  When working with a dataset that does not have channel locations, select the `Edit -> Channel locations` menu item and press `Ok` to look up channel locations based on channel labels (using the default MNI BEM template `standard_1005.elc`), then close the channel editor. For BIDS-formatted datasets, EEGLAB supports direct group import via `File -> Import data -> From BIDS folder structure` (`pop_importbids.m`).

* **中文译文与操作解析**：

  在 MATLAB 命令窗口输入 `eeglab` 启动主界面后，当前激活的数据集保存在结构体变量 `EEG` 中，所有已加载的数据集保存在结构体数组 `ALLEEG` 中。

  1. **导入连续数据**：通过 `File -> Import data -> Using EEGLAB functions and plugins` 选择对应采集设备格式（如 BrainVision `.vhdr`、Neuroscan `.cnt`、BioSemi `.bdf` 或通用格式 `pop_biosig`）。
  2. **匹配标准电极位置**：选择 `Edit -> Channel locations`（调用 `pop_chanedit.m`），只要电极名称符合国际 10-20 / 10-5 命名规范（如 `Fz, Cz, Pz, Oz`），点击 `Ok` 即可自动从 `standard_1005.elc` 模板中匹配 MNI 三维坐标。**官方特别提醒：务必在进行自动化伪迹剔除（`clean_rawdata`）、插值、全脑平均参考和源定位之前导入通道位置！**
  3. **导入 BIDS 标准数据集**：若数据遵循脑成像数据结构标准（BIDS），可直接调用 `pop_importbids()` 一键导入所有被试并自动生成 `STUDY` 群组结构。

```matlab
% 启动 EEGLAB 并加载示例数据，匹配默认 10-5 系统电极坐标
[ALLEEG, EEG, CURRENTSET, ALLCOM] = eeglab;
EEG = pop_loadset('filename', 'eeglab_data.set', 'filepath', fullfile(fileparts(which('eeglab')), 'sample_data'));
EEG = pop_chanedit(EEG, 'lookup', 'standard_1005.elc');
```
