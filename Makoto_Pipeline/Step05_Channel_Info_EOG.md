# Step 5：通道位置与辅助记录

> 类型：对用户提供的既有笔记进行重写校订；英文为校订说明，中文为对应译释，均非网页逐字引文。新增学习要点另列。核对日期：2026-10-16。
> 来源：[Makoto原文](https://eeglab.ucsd.edu/wiki/Makoto%27s_preprocessing_pipeline)；原文为个人建议。[覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

Channel locations support spatial inspection, interpolation and source modeling. Dedicated eye channels can remain useful for artifact detection and validation even when they are excluded from a particular ICA or reference calculation.

## 对应中文译释

通道位置支持空间检查、插值与源模型。专用眼电通道即使不进入某次分解或参考计算，仍可用于伪迹检测和验证。

## 学习要点与适用限制

模板匹配不等于测得个体真实位置。核对电极名称、坐标单位、左右方向、头心与实际布局。双极眼电和单极头皮通道的参考定义不同，不能随意一起算头皮平均；但不能据此断言双极眼电没有价值。作者对电极配置的个人偏好不应直接改成采集规范。

## 进一步学习

阅读[原理、例子与检查方法](../Learning_Guide/02_Events_and_Data_Checks.md)。这里的说明不是一条可直接运行的通用管线；代码状态见[示例说明](../03_MATLAB_Scripts/README.md)。
