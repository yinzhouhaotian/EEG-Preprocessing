# EEG 脑电数据预处理与功率/连接性分析中英双语手册 (MATLAB / EEGLAB)

本仓库整理并翻译了加州大学圣迭戈分校（UCSD）SCCN 维护的两大核心脑电分析指南，重点针对**任务态频域功率（PSD / ERSP）与功能连接（Functional Connectivity）**研究进行了方法学批注。

## 📚 第一部分：Makoto's Preprocessing Pipeline 中英对照（分章精读）
* [Step 1–4：双精度设置、路径检查、降采样与 1 Hz 高通滤波原理](./01_Makoto_Pipeline/01_Import_Resample_and_1Hz_Filter.md)
* [Step 5–9：电极配准、剔除坏导、球面插值、满秩全脑平均参考与 CleanLine](./01_Makoto_Pipeline/02_Chanlocs_BadChans_Interp_Reref.md)
* [Step 10–15：小波边缘效应与分段、矩阵有效秩校准、ICA 分解与 DIPFIT 偶极子拟合](./01_Makoto_Pipeline/03_Epoch_Rank_ICA_and_DIPFIT.md)
* [Step 16–17：STUDY 群组分析、ASR + ICLabel 全自动管线与 SIFT 连接性准则](./01_Makoto_Pipeline/04_STUDY_ASR_ICLabel_and_SIFT.md)

## 📖 第二部分：EEGLAB Official Tutorials 官方在线教程中英对照
* [Ch 1–5：数据结构、导入、高通/低通分离滤波与连接性滤波禁忌](./02_EEGLAB_Official_Tutorials/01_Import_and_Filtering_Rules.md)
* [Ch 6：clean_rawdata (ASR) 自动清洗、ICA 四大优化法则与 ICLabel 自动分类](./02_EEGLAB_Official_Tutorials/02_CleanRawdata_ICA_and_ICLabel.md)
* [Ch 7–8：分段基线注意事项与时频分解实战（ERSP 功率与 ITC 相干性）](./02_EEGLAB_Official_Tutorials/03_Epochs_and_TimeFrequency_ERSP.md)
* [Ch 9–11 & Plugin：DIPFIT 源定位、官方全自动频谱管线与 ROIconnect 源空间连接性](./02_EEGLAB_Official_Tutorials/04_DIPFIT_STUDY_and_ROIconnect.md)

## 💻 第三部分：配套 MATLAB 批处理脚本 (`03_MATLAB_Scripts/`)
* [`makoto_batch_pipeline.m`](./03_MATLAB_Scripts/makoto_batch_pipeline.m) — 融合有效秩校准与 ICLabel 的单被试批处理模板
* [`eeglab_official_spectral_study.m`](./03_MATLAB_Scripts/eeglab_official_spectral_study.m) — 官方 STUDY 多被试功率谱全自动管线
* [`eeglab_roiconnect_pipeline.m`](./03_MATLAB_Scripts/eeglab_roiconnect_pipeline.m) — 基于 LCMV 波束成形、FOOOF 与 MIM/TRGC 的源空间脑区连接脚本