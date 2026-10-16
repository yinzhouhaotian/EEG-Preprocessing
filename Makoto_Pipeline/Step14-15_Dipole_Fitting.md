# Step 14–15：偶极子拟合及其边界

> 类型：对用户提供的既有笔记进行重写校订；英文为校订说明，中文为对应译释，均非网页逐字引文。新增学习要点另列。核对日期：2026-10-16。
> 来源：[Makoto原文](https://eeglab.ucsd.edu/wiki/Makoto%27s_preprocessing_pipeline)；原文为个人建议。[覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

Dipole fitting compares a component scalp map with predictions from a head model. Low residual error supports that spatial model fit but does not prove a pure brain source. Coordinate units, electrode alignment and model assumptions must be checked before interpreting a fitted location.

## 对应中文译释

偶极子拟合比较成分头皮图与头模型的预测。较低残差支持空间模型拟合较好，但不证明成分是纯脑源。解释位置前应检查坐标单位、电极配准和模型假设。

## 学习要点与适用限制

单源、对称双源与分布式模型的约束不同。不要根据模板文件名猜层数；也不要复制固定旋转参数而不查看实际配准。残差需要说明归一化与参与通道，低通道数的低残差不能直接等同于更好数据。源定位属于后续模型分析，不是每次传感器功率研究的必做预处理。

## 进一步学习

阅读[原理、例子与检查方法](../Learning_Guide/09_Pipeline_and_Quality_Control.md)。这里的说明不是一条可直接运行的通用管线；代码状态见[示例说明](../03_MATLAB_Scripts/README.md)。
