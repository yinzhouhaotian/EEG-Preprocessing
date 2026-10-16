# Step 3：按目标决定是否降采样

> 类型：对用户提供的既有笔记进行重写校订；英文为校订说明，中文为对应译释，均非网页逐字引文。新增学习要点另列。核对日期：2026-10-16。
> 来源：[Makoto原文](https://eeglab.ucsd.edu/wiki/Makoto%27s_preprocessing_pipeline)；原文为个人建议。[覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

Downsampling reduces storage and computation but limits bandwidth and timing precision. Apply an appropriate anti-aliasing operation before sample reduction, or use a resampling function that includes it. A lower sampling rate does not guarantee a better decomposition.

## 对应中文译释

降采样减少存储与计算量，但会限制带宽和时间精度。减少采样点之前应有适当的抗混叠处理，或使用内置该处理的重采样函数。降低采样率不保证分解质量改善。

## 学习要点与适用限制

250或256赫兹只是可能的工作值；较高频率研究、事件潜伏期研究及自回归建模可能有不同需要。核对实际目标带宽、滤波过渡带和事件变换，不把简单抽点与带滤波重采样混用。已有笔记中的“改善分解”需要保留其未经定量确认的限定。

## 进一步学习

阅读[原理、例子与检查方法](../Learning_Guide/04_Filtering_and_Resampling.md)。这里的说明不是一条可直接运行的通用管线；代码状态见[示例说明](../03_MATLAB_Scripts/README.md)。
