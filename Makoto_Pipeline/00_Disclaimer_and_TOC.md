# Makoto笔记：校订说明与章节导航

原文：[Makoto’s preprocessing pipeline](https://eeglab.ucsd.edu/wiki/Makoto%27s_preprocessing_pipeline)。此次核对的修订标识为36694，原文最后编辑日期为2026-09-17；来源校验记录见[来源清单](../docs/source_manifest.json)。

作者明确将该网页定位为个人建议，不等于工具箱官方指南。本文各页为已有笔记的重写校订：英文是校订说明，中文为对应译释，另列学习要点。它们不是原文全文或逐字引文。对网页中已撤回、历史性或推断性的内容，应保留其状态。

从零学习请先读[学习指南](../Learning_Guide/00_Start_Here.md)；术语见[术语表](../docs/GLOSSARY.md)。

## 对应主题

- [Step 1：数值精度与已撤回的历史步骤](Step01_Double_Precision.md)
- [Step 2：导入、路径与激活矩阵](Step02_Path_Import_icaact_Fix.md)
- [Step 3：按目标决定是否降采样](Step03_Downsample.md)
- [Step 4：高通与分解训练副本](Step04_Highpass_1Hz.md)
- [Step 5：通道位置与辅助记录](Step05_Channel_Info_EOG.md)
- [Step 6：坏通道与局部异常](Step06_Remove_Bad_Channels.md)
- [Step 7：插值的估计与维度限制](Step07_Interpolate_Channels.md)
- [Step 8：平均参考、原参考与秩](Step08_Average_Reference_FullRank.md)
- [Step 9：工频正弦干扰的估计](Step09_CleanLine.md)
- [Step 10：分段窗口、边缘与基线](Step10_Epoch_1to2s.md)
- [Step 11：试次清理的目的与阈值](Step11_Reject_Epochs.md)
- [Step 12：分解成分数与有效秩](Step12_Adjust_Rank_ICA.md)
- [Step 13：拟合、判读与迁移分解](Step13_Run_ICA.md)
- [Step 14–15：偶极子拟合及其边界](Step14-15_Dipole_Fitting.md)
- [Step 16：群组结构与避免循环推断](Step16_STUDY_No_Double_Dipping.md)
- [Step 17：自动清理、标签与连接性扩展](Step17_Notes_ASR_ICLabel_SIFT.md)
- [原文第18部分：额外专题导航与学习边界](Step18_Additional_Topics.md)

- [代码示例与运行前核对](Appendix_Full_Batch_Script.md)
- [原文章节覆盖与未完成项](../docs/COVERAGE.md)
