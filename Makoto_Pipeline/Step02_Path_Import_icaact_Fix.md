# Step 2：导入、路径与激活矩阵

> 类型：对用户提供的既有笔记进行重写校订；英文为校订说明，中文为对应译释，均非网页逐字引文。新增学习要点另列。核对日期：2026-10-16。
> 来源：[Makoto原文](https://eeglab.ucsd.edu/wiki/Makoto%27s_preprocessing_pipeline)；原文为个人建议。[覆盖状态](../docs/COVERAGE.md) · [术语全称](../docs/GLOSSARY.md)。

## 英文校订说明

Check the data, labels, units and event timing after import. Path and function-name conflicts may depend on the environment and external programs. An empty activation array does not by itself prove that the ICA decomposition is missing.

## 对应中文译释

导入后应检查数据、标签、单位和事件时间。路径和函数重名问题可能依赖具体环境及外部程序。激活矩阵为空，本身不证明独立成分分解结果缺失。

## 学习要点与适用限制

区分存储的解混权重、白化矩阵和按需计算的激活。先检查偏好设置、软件版本与实际字段，再判断是否需要重算。不要把历史路径避坑经验当成所有操作系统的语法限制；变量名、文件名和路径的规则也不同。必要时用 `which -all` 查看函数解析。分段数据计算激活时还要正确处理试次维度。

## 进一步学习

阅读[原理、例子与检查方法](../Learning_Guide/02_Events_and_Data_Checks.md)。这里的说明不是一条可直接运行的通用管线；代码状态见[示例说明](../03_MATLAB_Scripts/README.md)。
