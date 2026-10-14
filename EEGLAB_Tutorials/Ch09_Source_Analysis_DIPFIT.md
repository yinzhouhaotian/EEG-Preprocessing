# Chapter 9: 源定位分析——DIPFIT 等效偶极子与 eLORETA (Source Analysis)

> 所属手册：EEGLAB 官方教程中英对照（由 `README.md` 按章节拆分）
>
> 章节导航：[00 总览](00_Overview_and_Navigation.md) · [Ch1–4](Ch01-04_Data_Management_Import.md) · [Ch5](Ch05_Preprocess_Data.md) · [Ch6](Ch06_Reject_Artifacts_ASR_ICA.md) · [Ch7](Ch07_Extract_Epochs.md) · [Ch8](Ch08_Spectra_TimeFrequency.md) · [Ch9](Ch09_Source_Analysis_DIPFIT.md) · [Ch10–11](Ch10-11_Group_STUDY_Automated_Pipeline.md) · [ROIconnect](Plugin_ROIconnect_Connectivity.md) · [附录对比](Appendix_Comparison_Official_vs_Makoto.md)

* **English Original** ([Tutorials -\> 9.b DIPFIT](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F09_source%2FDIPFIT.html)):

  *Rationale for localizing ICA components*: Because local cortical connections have a much higher density than longer-range connections, synchronous coupling of local field potential (LFP) activity isolated by ICA usually occurs within a single connected cortical patch, producing scalp maps that nearly perfectly match the projection of a single equivalent dipole (Delorme et al., 2012).

  *What reference for ICA components in DIPFIT?* Although ICA unmixing is reference-free, before performing source localization in DIPFIT, both the ICA component scalp topography and the electrical forward head model are automatically converted to **average reference** so that they use the exact same approximation of the infinity reference.

  *Two-step fitting procedure*:

  1. **Coarse fit (grid scan)**: Scans a 3-D grid across the brain volume to find the best starting position.
  2. **Fine fit (non-linear optimization)**: Iteratively adjusts dipole position (`posxyz`) and dipole moment (`momxyz`) to minimize **Residual Variance (`rv`)**.

  Select `Tools -> Locate dipoles using DIPFIT -> Head model and settings` (`pop_dipfit_settings.m`), then `Autofit (coarse fit, fine fit, plot)` (`pop_multifit.m`). For distributed cortical source reconstruction, DIPFIT also integrates with FieldTrip (`ft_sourceanalysis`) via `Locate component using eLoreta` and `Distributed source leadfield matrix`.

* **中文译文与操作解析**：

  EEGLAB 的源定位插件 `DIPFIT` 既能为每个独立成分拟合单/双等效偶极子（存储在 `EEG.dipfit.model` 中，其中 `.posxyz` 为 MNI 坐标，`.rv` 为残差方差），也能生成全脑分布式源模型的**导联场矩阵（Leadfield Matrix）**，直接供 eLORETA 或后续的 `ROIconnect` 源空间脑区功能连接插件调用：

| `EEG.dipfit` 字段名 | 英文定义 (Official Definition) | 中文说明与用途 |
| :--- | :--- | :--- |
| `EEG.dipfit.hdmfile` | Head volume conductor model file | 头容积导体模型文件（如标准 BEM 模型 `standard_vol.mat`） |
| `EEG.dipfit.mrifile` | Anatomical MRI template file | 解剖结构 MRI 背景模板文件（`standard_mri.mat`） |
| `EEG.dipfit.coord_transform` | 9-parameter Talairach alignment vector | 将被试电极坐标对齐至标准头模的 9 参数空间变换向量 |
| `EEG.dipfit.model(i).posxyz` | 3-D MNI coordinates `[x y z]` (mm) | 第 `i` 个独立成分偶极子的三维 MNI 空间坐标（毫米） |
| `EEG.dipfit.model(i).rv` | Relative residual variance (`0` to `1`) | 偶极子拟合残差方差（`< 0.15` 即 `< 15%` 代表高质量脑源） |
