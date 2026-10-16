# Step 9：工频正弦干扰的估计

> 类型：对用户提供的既有笔记进行重写校订；英文为校订说明，中文为对应译释，均非网页逐字引文。新增学习要点另列。核对日期：2026-10-16。
> 来源：[Makoto原文](https://eeglab.ucsd.edu/wiki/Makoto%27s_preprocessing_pipeline)；原文为个人建议。[覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

A line-noise estimator models narrowband sinusoidal interference rather than simply removing an entire stopband. Its performance depends on the implementation, window settings and changes in the interference. Check the effect instead of assuming perfect removal or perfect preservation.

## 对应中文译释

工频估计方法对窄带正弦干扰建模，不只是移除整个阻带。效果取决于实现、窗口和干扰变化。应检查结果，而不假定完全去噪或完全保真。

## 学习要点与适用限制

历史版本的缺陷与选项应随具体版本记录，不应把某年的界面最后一个复选框描述为所有新版固定规则。先确认干扰频率及谐波在当前带宽内，再检查处理前后频谱、波形和窗口接缝。工具正常返回不等于干扰已被成功移除。

## 进一步学习

阅读[原理、例子与检查方法](../Learning_Guide/04_Filtering_and_Resampling.md)。这里的说明不是一条可直接运行的通用管线；代码状态见[示例说明](../03_MATLAB_Scripts/README.md)。
