# Step 6：坏通道与局部异常

> 类型：对用户提供的既有笔记进行重写校订；英文为校订说明，中文为对应译释，均非网页逐字引文。新增学习要点另列。核对日期：2026-10-16。
> 来源：[Makoto原文](https://eeglab.ucsd.edu/wiki/Makoto%27s_preprocessing_pipeline)；原文为个人建议。[覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

Persistent channel failures can contaminate spatial operations, including an arithmetic average reference. A channel with only a brief problem may be handled differently from a channel that is unusable throughout the recording. Rejection percentages are not targets to optimize.

## 对应中文译释

持续的通道故障可能污染包括算术平均参考在内的空间操作。只短时异常的通道，与全程不可用的通道可以采取不同处理。删除比例不是需要刻意达到的优化目标。

## 学习要点与适用限制

综合波形、频谱、平线、跳变及空间关系判断。记录坏导位置、原因与时段，并保留原布局供插值与比较。自动相关检测依赖参考、布局和算法实现；不把一个相关阈值当作所有数据的客观真值。不同管线也可能先作临时参考，再剔除坏导后重新定义参考。

## 进一步学习

阅读[原理、例子与检查方法](../Learning_Guide/05_Artifacts_and_ASR.md)。这里的说明不是一条可直接运行的通用管线；代码状态见[示例说明](../03_MATLAB_Scripts/README.md)。
