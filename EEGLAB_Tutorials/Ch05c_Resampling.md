# 第5.c节补充：改变采样率

> 类型：新增中文学习说明。对应[重采样原文](https://eeglab.org/tutorials/05_Preprocess/resampling.html)。

## 目的与代价

采样率高于研究所需时，降低采样率可减少数据量和计算开销。同时会限制可保留频率及事件的时间网格精度。提高采样率只是重新表示，并不能恢复采集时没有记录到的信息。

## 原理

降采样前需要抗混叠。某些函数把低通与插值/抽取组合在一起；简单保留每隔若干点的一个样本则没有自动完成这个步骤。查清实际函数，而不是只看名称。

在工具箱中，菜单 `Tools → Change sampling rate` 对应 `pop_resample`。目标值应由分析带宽、过渡带和事件要求决定，250或100赫兹都只是可能的选择。

```matlab
% 单数据集教学示例：targetFs 由分析目的确定，不是推荐常数
targetFs = 250;
EEG_resampled = pop_resample(EEG, targetFs);
% 保留原 EEG，并比较采样率、时长、频谱和事件位置。
```

## 检查

核对重采样后记录时长、事件类型与数量、新事件位置误差及目标频带。若后续需要精细潜伏期，检查误差是否在可接受范围内。信号、事件和行为日志必须使用一致时间映射。

推导和反例见[采样基础](../Learning_Guide/01_Signal_Sampling_Spectrum.md)与[滤波和重采样](../Learning_Guide/04_Filtering_and_Resampling.md)。
