# Makoto's Preprocessing Pipeline 中英对照完整指南（附 MATLAB 批处理代码）

> **原文来源 (Original Source)**: [Makoto's preprocessing pipeline - SCCN (Swartz Center for Computational Neuroscience, UCSD)](https://www.google.com/search?q=https%3A%2F%2Feeglab.ucsd.edu%2Fwiki%2FMakoto%27s_preprocessing_pipeline)
>
> **原作者 (Original Author)**: Makoto Miyakoshi (UCSD SCCN)
>
> **配套代码库参考 (Companion Code Wiki)**: [Makoto's useful EEGLAB code - SCCN](https://www.google.com/search?q=https%3A%2F%2Feeglab.ucsd.edu%2Fwiki%2FMakoto%27s_useful_EEGLAB_code) | [EEGLAB Official Tutorials](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F06_RejectArtifacts%2FRunICA.html)
>
> **文档说明**: 本文档将加州大学圣迭戈分校（UCSD）SCCN 维护的经典脑电预处理指南《Makoto's preprocessing pipeline》核心章节（第 1–17 节完整管线、数学原理推导、常见 Bug 修复、ASR 自动化流程、ICLabel 成分筛选及 SIFT 连接性分析准则）整理为**中英双语对照版**，并保留全部原始 MATLAB / EEGLAB 代码片段，方便科研人员学习与在 GitHub 仓库中归档参考。

> **章节拆分说明**: 本文件夹由 `Makotos_Preprocessing_Pipeline_CN_EN.md` 按 Step 拆分而来，每一步为独立 md 文件，便于单独查阅与版本管理。

## 章节导航 (Chapter Navigation)

| 章节文件 | 内容 |
| :--- | :--- |
| [00_Disclaimer_and_TOC.md](00_Disclaimer_and_TOC.md) | 版权与引用声明、目录概览（本文件） |
| [Step01_Double_Precision.md](Step01_Double_Precision.md) | Step 1 更改选项以使用双精度浮点运算 |
| [Step02_Path_Import_icaact_Fix.md](Step02_Path_Import_icaact_Fix.md) | Step 2 检查路径并导入数据（含 `EEG.icaact` 修复） |
| [Step03_Downsample.md](Step03_Downsample.md) | Step 3 按需降采样（含自动抗混叠滤波） |
| [Step04_Highpass_1Hz.md](Step04_Highpass_1Hz.md) | Step 4 1 Hz 高通滤波（含 1 Hz 与 0.1 Hz 权重迁移策略） |
| [Step05_Channel_Info_EOG.md](Step05_Channel_Info_EOG.md) | Step 5 导入通道位置信息与独立眼电（EOG）通道策略 |
| [Step06_Remove_Bad_Channels.md](Step06_Remove_Bad_Channels.md) | Step 6 识别并剔除坏导 |
| [Step07_Interpolate_Channels.md](Step07_Interpolate_Channels.md) | Step 7 球面样条插值恢复被剔除的通道 |
| [Step08_Average_Reference_FullRank.md](Step08_Average_Reference_FullRank.md) | Step 8 重参考至全脑平均（补零通道满秩防幽灵成分法） |
| [Step09_CleanLine.md](Step09_CleanLine.md) | Step 9 使用 CleanLine 去除 50/60 Hz 工频噪声 |
| [Step10_Epoch_1to2s.md](Step10_Epoch_1to2s.md) | Step 10 数据分段至 -1 到 2 秒（基线校正禁忌与小波边缘效应） |
| [Step11_Reject_Epochs.md](Step11_Reject_Epochs.md) | Step 11 剔除伪迹试次（波幅阈值与联合概率检验） |
| [Step12_Adjust_Rank_ICA.md](Step12_Adjust_Rank_ICA.md) | Step 12 为 ICA 调整数据矩阵的有效秩（Rank） |
| [Step13_Run_ICA.md](Step13_Run_ICA.md) | Step 13 运行独立成分分析（数据长度、平稳性、相位与 PCA） |
| [Step14-15_Dipole_Fitting.md](Step14-15_Dipole_Fitting.md) | Step 14 & 15 头模型空间配准与单/双侧偶极子拟合 |
| [Step16_STUDY_No_Double_Dipping.md](Step16_STUDY_No_Double_Dipping.md) | Step 16 创建群组 STUDY 分析并避免“双重蘸取（循环推断）” |
| [Step17_Notes_ASR_ICLabel_SIFT.md](Step17_Notes_ASR_ICLabel_SIFT.md) | Step 17 进阶笔记：ASR 自动管线、ICLabel、步骤依赖与 SIFT 连接性 |
| [Appendix_Full_Batch_Script.md](Appendix_Full_Batch_Script.md) | 附：可直接运行的完整 MATLAB 批处理脚本模板 |

## 版权与引用声明 (Disclaimer & Citation)

* **English Original**:

  *Note from Arnaud Delorme (main developer of EEGLAB)*: The opinions expressed below are those of Makoto Miyakoshi and should not be taken as official EEGLAB guidelines. This Wiki page is a forever beta version and subject to change anytime.

  *How to cite this page (APA style)*:

  `Makoto's preprocessing pipeline. (n.d.). Retrieved October 14, 2026, from https://eeglab.ucsd.edu/wiki/Makoto's_preprocessing_pipeline`

* **中文译文**：

  *EEGLAB 主开发者 Arnaud Delorme 注*：以下观点仅代表 Makoto Miyakoshi 个人经验建议，不应被视为 EEGLAB 官方硬性指南。本页面处于持续更新的 Beta 状态。若在论文或开源项目中引用本管线，请按上方 APA 格式标注原始 SCCN Wiki 链接。

## 目录概览 (Table of Contents)

| 章节编号 | 英文标题 (English Title) | 中文标题 (Chinese Title) | 核心关联函数 / 工具 |
| ----- | ----- | ----- | ----- |
| **Step 1** | Change the option to use double precision | 更改选项以使用双精度浮点运算 | `pop_editoptions` |
| **Step 2** | Check the path and import data (`EEG.icaact` bug fix) | 检查路径并导入数据（含 `EEG.icaact` 为空的修复） | `eeg_options.m`, `icadefs.m` |
| **Step 3** | Downsample if necessary | 按需降采样（含自动抗混叠滤波） | `pop_resample` |
| **Step 4** | High-pass filter the data at 1-Hz (1 Hz vs. 0.1 Hz trick) | 1 Hz 高通滤波（含 1 Hz 与 0.1 Hz 权重迁移策略） | `pop_eegfiltnew` |
| **Step 5** | Import channel info & Dedicated EOG channels | 导入通道位置信息与独立眼电（EOG）通道策略 | `pop_chanedit` |
| **Step 6** | Remove bad channels | 识别并剔除坏导 | `clean_rawdata`, `trimOutlier` |
| **Step 7** | Interpolate all the removed channels | 球面样条插值恢复被剔除的通道 | `pop_interp`, `eeg_interp` |
| **Step 8** | Re-reference the data to average (Full-rank method) | 重参考至全脑平均（补零通道满秩防幽灵成分法） | `pop_reref`, `fullRankAveRef` |
| **Step 9** | Remove line noise using CleanLine | 使用 CleanLine 去除 50/60 Hz 工频噪声 | `pop_cleanline`, `cleanLineNoise` |
| **Step 10** | Epoch data to -1 to 2 sec (Baseline & COI cautions) | 数据分段至 -1 到 2 秒（基线校正禁忌与小波边缘效应） | `pop_epoch` |
| **Step 11** | Reject epochs for cleaning | 剔除伪迹试次（波幅阈值与联合概率检验） | `pop_eegthresh`, `pop_jointprob` |
| **Step 12** | Adjust data rank for ICA | 为 ICA 调整数据矩阵的有效秩（Rank） | `rank`, `eig`, `loc_subsets` |
| **Step 13** | Run ICA (Data length, Stationarity, Phase & PCA) | 运行独立成分分析（数据长度、平稳性、相位与 PCA） | `pop_runica`, `runamica15` |
| **Step 14** | Head model coregistration and dipole fitting | 头模型空间配准与单等效电流偶极子拟合 | `pop_dipfit_settings`, `pop_multifit` |
| **Step 15** | Estimate symmetrically constrained bilateral dipoles | 搜索并估计对称约束的双侧偶极子 | `fitTwoDipoles` |
| **Step 16** | Create STUDY & Avoid double dipping | 创建群组 STUDY 分析并避免“双重蘸取（循环推断）” | `std_editset`, `newtimef` |
| **Step 17** | Notes: ASR Pipeline, ICLabel, Dependencies & SIFT Tips | 进阶笔记：ASR 自动管线、ICLabel、步骤依赖与 SIFT 连接性 | `ICLabel`, `pop_subcomp`, `SIFT` |
