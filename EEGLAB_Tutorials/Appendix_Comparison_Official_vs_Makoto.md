# 附：官方教程 (`EEGLAB Tutorials`) 与 `Makoto's Pipeline` 核心异同速查表

> 所属手册：EEGLAB 官方教程中英对照（由 `README.md` 按章节拆分）
>
> 章节导航：[00 总览](00_Overview_and_Navigation.md) · [Ch1–4](Ch01-04_Data_Management_Import.md) · [Ch5](Ch05_Preprocess_Data.md) · [Ch6](Ch06_Reject_Artifacts_ASR_ICA.md) · [Ch7](Ch07_Extract_Epochs.md) · [Ch8](Ch08_Spectra_TimeFrequency.md) · [Ch9](Ch09_Source_Analysis_DIPFIT.md) · [Ch10–11](Ch10-11_Group_STUDY_Automated_Pipeline.md) · [ROIconnect](Plugin_ROIconnect_Connectivity.md) · [附录对比](Appendix_Comparison_Official_vs_Makoto.md)

在你的 GitHub 仓库中同时收录这两篇文档时，可以用下表向读者清晰展示两者的互补关系：

| 对比维度 | EEGLAB 官方在线教程 (`eeglab.org/tutorials/`) | Makoto's Preprocessing Pipeline (`SCCN Wiki`) | 针对你的“任务态功率 + 连接性”建议 |
| :--- | :--- | :--- | :--- |
| **定位与风格** | 官方标准功能指南，侧重 GUI 菜单与 `STUDY` 群组批处理框架 | 资深研究者深度避坑笔记，侧重线性代数（矩阵秩）、信号处理底层证明 | 两者结合：用 Makoto 的原理排雷，用官方的 `STUDY` / `ROIconnect` 架构写脚本 |
| **重参考时机** | 推荐“两次平均参考法”：`clean_rawdata` 前做一次，剔除坏导后再做一次 | 推荐在剔除并插值坏导后做一次“补零通道满秩全脑平均参考” | 两种方法在数学上均能消除坏导偏置；若在 ICA 前做重参考，建议补零通道或设 `'pca', -1` |
| **坏导插值时机** | 推荐留到最后在 `STUDY` 群组层（`std_precomp(..., 'interp', 'on')`）再插值 | 推荐在平均参考和 ICA 之前插值，但必须用特征值阈值（$10^{-7}$）显式扣减 ICA 维度 | **官方策略更省心**：在 ICA 和连接性计算前只剔除坏导不插值，既避免幽灵成分，又防止插值通道伪造连接 |
| **ASR 处理模式** | 离线分析默认直接切除超阈值伪迹段（`'BurstRejection', 'on'`） | 推荐仅用子空间重构修复而不切碎时间轴（`'BurstRejection', 'off'`, `SD = 20`） | 短试次多重复任务可用 `'on'`；长时程任务态（几秒至几十秒）推荐用 `'off'` 保留完整试次 |
| **连接性工具链** | 最新力推 **`ROIconnect`**（LCMV/eLORETA 源投影 + MIM/MIC/TRGC）与 `SIFT` | 重点介绍基于 ICA 源成分的 **`SIFT`**（多变量自回归 MVAR 格兰杰因果） | 若关注全脑图谱 ROI 间功率与连接性，优先使用官方 **`ROIconnect`** 或 **FieldTrip** |
