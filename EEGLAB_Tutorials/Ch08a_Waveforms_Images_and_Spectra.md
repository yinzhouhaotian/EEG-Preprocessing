# 第8章补充：波形、试次图、频谱和成分图

> 类型：新增中文学习说明。原文各页在末尾列出；原文图像通过链接查阅，不在本仓库批量复制。

## 平均波形

事件锁定的电压平均能显示跨试次相位和时间较一致的活动。检查平均之前，先确认事件、参考、基线与保留试次。不同试次数或少数极端试次可能影响平均，不能只凭一条平滑曲线判断数据质量。

## 试次图

把各试次的时间序列按行显示，可以看出平均掩盖的变化。按反应时等变量排序能发现关系，但排序和平滑也改变视觉效果；应记录设置，不能把图像条纹直接当成统计证据。

## 通道频谱与头皮图

先确认频谱单位、窗长和估计方法。一个明显的窄峰与广泛高频抬升通常需要不同检查。头皮图是空间插值显示，不是直接测得的连续头皮表面，更不是脑源图。

## 成分图

成分头皮图显示其在通道上的投影模式，与成分时间序列不同。分量编号、顺序和正负号可能随拟合改变，不应把“第1成分”当成跨数据通用类别。

将地形、时间、频谱与辅助通道对应起来，再判断伪迹。详见[成分判读](../Learning_Guide/06_ICA_and_Component_Review.md)。

## 原文入口

- [平均波形](https://eeglab.org/tutorials/08_Plot_data/Data_Averaging.html)
- [试次图](https://eeglab.org/tutorials/08_Plot_data/Plotting_ERP_images.html)
- [通道频谱与头皮图](https://eeglab.org/tutorials/08_Plot_data/Plotting_Channel_Spectra_and_Maps.html)
- [独立成分显示](https://eeglab.org/tutorials/08_Plot_data/Plotting_ICA_components.html)
