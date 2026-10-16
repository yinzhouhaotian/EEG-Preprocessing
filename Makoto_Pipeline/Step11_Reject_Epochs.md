# Step 11：试次清理的目的与阈值

> 类型：对用户提供的既有笔记进行重写校订；英文为校订说明，中文为对应译释，均非网页逐字引文。新增学习要点另列。核对日期：2026-10-16。
> 来源：[Makoto原文](https://eeglab.ucsd.edu/wiki/Makoto%27s_preprocessing_pipeline)；原文为个人建议。[覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

Before fitting a stable mixing model, identify rare severe disturbances that the model is unlikely to explain. After cleaning, inspect remaining artifacts again. Amplitude and probability thresholds are screening choices, not proof of signal origin or universal rejection rules.

## 对应中文译释

拟合稳定混合模型前，应识别模型难以解释的罕见严重干扰；清理后再检查残余伪迹。振幅和概率阈值是筛查选择，不是来源证明或统一删除规则。

## 学习要点与适用限制

吞咽是生理性伪迹，不能和电极线晃动一起称为非生物活动。应明确绝对幅度、峰峰值或联合概率等不同标准。示例中的数值与5%至10%比例不能作为必须达到的目标。按条件记录剩余试次数和删除原因，避免只为了保留更多试次而放过明显污染。

## 进一步学习

阅读[原理、例子与检查方法](../Learning_Guide/05_Artifacts_and_ASR.md)。这里的说明不是一条可直接运行的通用管线；代码状态见[示例说明](../03_MATLAB_Scripts/README.md)。
