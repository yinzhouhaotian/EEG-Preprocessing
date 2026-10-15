# Step 1–4: 双精度设置、路径检查、降采样与 1 Hz 高通滤波原理

> **原文来源 (Original Source)**: [Makoto's preprocessing pipeline - SCCN (Swartz Center for Computational Neuroscience, UCSD)](https://www.google.com/search?q=https%3A%2F%2Feeglab.ucsd.edu%2Fwiki%2FMakoto%27s_preprocessing_pipeline)
>
> **原作者 (Original Author)**: Makoto Miyakoshi (UCSD SCCN)
>
> **配套代码库参考 (Companion Code Wiki)**: [Makoto's useful EEGLAB code - SCCN](https://www.google.com/search?q=https%3A%2F%2Feeglab.ucsd.edu%2Fwiki%2FMakoto%27s_useful_EEGLAB_code) | [EEGLAB Official Tutorials](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F06_RejectArtifacts%2FRunICA.html)
>
> **文档说明**: 本文档将加州大学圣迭戈分校（UCSD）SCCN 维护的经典脑电预处理指南《Makoto's preprocessing pipeline》核心章节（第 1–17 节完整管线、数学原理推导、常见 Bug 修复、ASR 自动化流程、ICLabel 成分筛选及 SIFT 连接性分析准则）整理为**中英双语对照版**，并保留全部原始 MATLAB / EEGLAB 代码片段，方便科研人员学习与在 GitHub 仓库中归档参考。

> 所属手册：Makoto's Preprocessing Pipeline 中英对照（SCCN Wiki，原作者 Makoto Miyakoshi）
>
> 章节导航：[01 导入/降采样/1Hz滤波](01_Import_Resample_and_1Hz_Filter.md) · [02 电极/坏导/插值/重参考/CleanLine](02_Chanlocs_BadChans_Interp_Reref.md) · [03 分段/秩/ICA/DIPFIT](03_Epoch_Rank_ICA_and_DIPFIT.md) · [04 STUDY/ASR/ICLabel/SIFT](04_STUDY_ASR_ICLabel_and_SIFT.md) · [返回 README](../README.md)

## 版权与引用声明 (Disclaimer & Citation)

* **English Original**:

  *Note from Arnaud Delorme (main developer of EEGLAB)*: The opinions expressed below are those of Makoto Miyakoshi and should not be taken as official EEGLAB guidelines. This Wiki page is a forever beta version and subject to change anytime.

  *How to cite this page (APA style)*:

  `Makoto's preprocessing pipeline. (n.d.). Retrieved October 14, 2026, from https://eeglab.ucsd.edu/wiki/Makoto's_preprocessing_pipeline`

* **中文译文**：

  *EEGLAB 主开发者 Arnaud Delorme 注*：以下观点仅代表 Makoto Miyakoshi 个人经验建议，不应被视为 EEGLAB 官方硬性指南。本页面处于持续更新的 Beta 状态。若在论文或开源项目中引用本管线，请按上方 APA 格式标注原始 SCCN Wiki 链接。

## 目录概览 (Table of Contents)

| 章节编号 | 英文标题 (English Title) | 中文标题 (Chinese Title) | 核心关联函数 / 工具 |
| ----- | ----- | ----- | ----- |
| **Step 1** | Change the option to use double precision | 更改选项以使用双精度浮点运算 | `pop_editoptions` |
| **Step 2** | Check the path and import data (`EEG.icaact` bug fix) | 检查路径并导入数据（含 `EEG.icaact` 为空的修复） | `eeg_options.m`, `icadefs.m` |
| **Step 3** | Downsample if necessary | 按需降采样（含自动抗混叠滤波） | `pop_resample` |
| **Step 4** | High-pass filter the data at 1-Hz (1 Hz vs. 0.1 Hz trick) | 1 Hz 高通滤波（含 1 Hz 与 0.1 Hz 权重迁移策略） | `pop_eegfiltnew` |
| **Step 5** | Import channel info & Dedicated EOG channels | 导入通道位置信息与独立眼电（EOG）通道策略 | `pop_chanedit` |
| **Step 6** | Remove bad channels | 识别并剔除坏导 | `clean_rawdata`, `trimOutlier` |
| **Step 7** | Interpolate all the removed channels | 球面样条插值恢复被剔除的通道 | `pop_interp`, `eeg_interp` |
| **Step 8** | Re-reference the data to average (Full-rank method) | 重参考至全脑平均（补零通道满秩防幽灵成分法） | `pop_reref`, `fullRankAveRef` |
| **Step 9** | Remove line noise using CleanLine | 使用 CleanLine 去除 50/60 Hz 工频噪声 | `pop_cleanline`, `cleanLineNoise` |
| **Step 10** | Epoch data to -1 to 2 sec (Baseline & COI cautions) | 数据分段至 -1 到 2 秒（基线校正禁忌与小波边缘效应） | `pop_epoch` |
| **Step 11** | Reject epochs for cleaning | 剔除伪迹试次（波幅阈值与联合概率检验） | `pop_eegthresh`, `pop_jointprob` |
| **Step 12** | Adjust data rank for ICA | 为 ICA 调整数据矩阵的有效秩（Rank） | `rank`, `eig`, `loc_subsets` |
| **Step 13** | Run ICA (Data length, Stationarity, Phase & PCA) | 运行独立成分分析（数据长度、平稳性、相位与 PCA） | `pop_runica`, `runamica15` |
| **Step 14** | Head model coregistration and dipole fitting | 头模型空间配准与单等效电流偶极子拟合 | `pop_dipfit_settings`, `pop_multifit` |
| **Step 15** | Estimate symmetrically constrained bilateral dipoles | 搜索并估计对称约束的双侧偶极子 | `fitTwoDipoles` |
| **Step 16** | Create STUDY & Avoid double dipping | 创建群组 STUDY 分析并避免“双重蘸取（循环推断）” | `std_editset`, `newtimef` |
| **Step 17** | Notes: ASR Pipeline, ICLabel, Dependencies & SIFT Tips | 进阶笔记：ASR 自动管线、ICLabel、步骤依赖与 SIFT 连接性 | `ICLabel`, `pop_subcomp`, `SIFT` |

## Step 1: 更改选项以使用双精度运算 (Change the option to use double precision)

* **English Original**:

  In EEGLAB2019, `'File' -> 'Preferences'`. In EEGLAB 14, from main GUI top left tab, `'File' -> 'Memory and other options' -> 'If set, use single precision under...'` uncheck it. Note that when computing ICA etc where double precision is necessary, EEGLAB functions internally convert input data to double precision. So mostly this is taken care of automatically as long as you stick to GUI operations. Note that if you want to run calculation that involves matrix operation, you have to check whether the input data is always converted to double at your own risk. Otherwise you will encounter problems when data rank is calculated with single vs. double precisions right after importing it from `.raw` file.

* **中文译文与原理解析**：

  在 EEGLAB 2019 及更新版本中，进入菜单 `'File' -> 'Preferences'`（旧版 EEGLAB 14 为 `'File' -> 'Memory and other options'`），**取消勾选“使用单精度（single precision）”选项**，确保全程使用双精度（double precision）。虽然通过 GUI 运行 ICA 时 EEGLAB 内部会自动将数据转为双精度，但如果你自己编写批处理脚本进行矩阵运算（例如刚导入数据时用 `rank(double(EEG.data))` 计算矩阵秩、协方差矩阵特征值分解或空间滤波），单精度浮点数极易因数值截断导致矩阵秩计算错误。

```
% 设置 EEGLAB 使用双精度并保留独立成分激活矩阵 (EEG.icaact)
pop_editoptions('option_single', false, 'option_computeica', true);
```

## Step 2: 检查路径并导入数据 (Check the path and import data)

### 2.1 路径与命名规范 (Path and Naming Rules)

* **English Original**:

  Before importing the data, check these points:

  1. Your full path to eeglab folders and your data does NOT contain any non-alphabetic, non-numeric, non-underscore characters such as `!@#$%^&*()-=\`\[\];',`and`\[space\]`. For example, if your folder name is `'Experiment 1'`, that is bad. Change it to `'Experiment1'`or`'Experiment_1'\`.

  2. Any folder and file name in your full path, as well as your variable names in Matlab workspace, does not start with numbers. For example, `'2018_Oddball_Project'` is better changed to `'Oddball_Project_2018'`.

  3. Avoid using names that are (likely to be) used as Matlab function. For example, `'eeglab'` or `'interp'` is a name of a function. If you are not sure if a name is already used by Matlab, type `which -all [variableName]`.

  4. After importing, check if you have extra channels that are filled with zeros or complete garbage. Never include those problematic channels into ICA, it crashes the process (and for infomax, it slows the process significantly).

* **中文译文与原理解析**：

  在导入数据前，请严格检查以下 4 点：

  1. **路径禁含空格与特殊字符**：EEGLAB 文件夹和数据文件的完整路径中，绝不能包含除字母、数字、下划线以外的特殊字符（尤其是空格和中文路径），例如 `'Experiment 1'` 应改为 `'Experiment_1'`（否则调用外部二进制插件如 AMICA 时会直接崩溃）。

  2. **禁止以数字开头**：文件夹名、文件名以及 MATLAB 工作区变量名不要以数字开头（例如将 `'2018_Oddball_Project'` 改为 `'Oddball_Project_2018'`）。

  3. **避开 MATLAB 内置函数名**：不要用 `'eeglab'`、`'interp'` 等内置函数名作为文件夹或变量名，不确定时可在命令行输入 `which -all 变量名` 检查。

  4. **剔除全零或纯噪声附加通道**：导入数据后，立即检查是否存在全为 0 或纯噪声的空余物理通道（如未接电极的辅助口或参考口），**绝不能将这些通道送入 ICA**，否则会导致分解崩溃或使 Infomax 收敛极度缓慢。

### 2.2 修复 `EEG.icaact` 为空的常见 Bug (`EEG.icaact` is empty!?)

* **English Original**:

  This problem is caused by missing `eeg_options.m` that was supposed to be created properly when you first launched EEGLAB. To diagnose the problem, try `which -all eeg_options`. Usually, you have to find two of them, one under `adminfunc` (read-only archetype), and the other under `userpath`. If EEGLAB cannot access `eeg_options.m`, `'precompute ICA activations...'` is unselected, hence `EEG.icaact` is NEVER calculated by `eeg_checkset()`. To fix this, go into `functions/sigprocfunc/icadefs.m` and manually set `EEGOPTION_PATH = userpath;`, or checkmark `'Precompute ICA activations'` in `File -> Preferences`.

* **中文译文与原理解析**：

  如果你运行完 ICA 保存数据后发现 `EEG.icaact`（ICA 成分时间序列）总是变成空矩阵 `[]`，通常有两个原因：一是 EEGLAB 未能在你的 MATLAB `userpath` 下正常生成可写的 `eeg_options.m` 配置文件（可在命令行运行 `which -all eeg_options` 检查是否同时存在 `adminfunc` 模板文件和 `userpath` 配置文件）；二是在 `File -> Preferences` 中未勾选 `'Precompute ICA activations'`。也可手动计算恢复：

```
% 手动计算恢复 ICA 激活时间序列矩阵 EEG.icaact
EEG.icaact = (EEG.icaweights * EEG.icasphere) * EEG.data(EEG.icachansind, :);
```

## Step 3: 按需降采样 (Downsample if necessary)

* **English Original**:

  You may downsample the data to around 250Hz if the original sampling frequency is higher than that. Usually low-pass filter is necessary before downsampling for anti-aliasing, but EEGLAB function applies the anti-aliasing filter automatically. Downsampling is useful to compress the data size. It also helps ICA to produce better decomposition by cutting off unnecessary high-frequency information, though we have not tested it quantitatively.

* **中文译文与原理解析**：

  如果原始采样率较高（例如 1000 Hz），可以将连续数据降采样至 **250 Hz**（若原始为 512/1024 Hz 则可降至 256 Hz；若做 SIFT 格兰杰因果连接性分析可降至 100–128 Hz）。降采样前必须进行抗混叠低通滤波（Anti-aliasing low-pass filter），而 EEGLAB 的 `pop_resample()` 函数会自动内置执行抗混叠滤波。降采样不仅能大幅压缩数据体积、加速后续计算，还能通过滤除不必要的高频噪声来帮助 ICA 获得更好的分解质量。

```
% 将连续脑电数据降采样至 250 Hz（内置自动抗混叠低通滤波）
EEG = pop_resample(EEG, 250);
```

## Step 4: 1 Hz 高通滤波 (High-pass filter the data at 1-Hz)

### 4.1 为什么针对 ICA、ASR 和 CleanLine 推荐使用 1 Hz 通带边缘？

* **English Original**:

  The purpose of the application of high-pass filter is to remove the 'baseline drift'. It is generally recommended to use lower cutoff frequencies, for example 0.01 Hz (cooperative subjects) – 0.1 Hz (children and patients) (Luck, 2005) than our recommended 1-Hz pass-band edge (equivalent to cutoff frequency of 0.5 Hz @ -6dB). The reason for the 1-Hz pass band edge is because:

  1. ICA is biased toward high amplitude if data length is finite.

  2. EEG data have $1/f$ power spectral density (PSD) curve. The combination of these two facts means that the leftmost values on the PSD plot will have the most influence on your decomposition result, although the most useful EEG information you are probably looking for is in 3–13 Hz (theta and alpha). Therefore, cutting off the leftmost values helps ICA to focus on the important 3–13 Hz.

  3. Low-frequency EEG < 1Hz could be contaminated by sweating etc, which adds spatiotemporal non-stationarity and affects ICA.

  4. Also, the lowest frequency in ERSP (blended wavelet/STFT transform) is typically 3 Hz if you want to have a decent frequency resolution (in EEGLAB parameters, 3 cycle at 3 Hz generates 1116 ms sliding window length). 3 Hz is sufficiently high relative to the 0.5-Hz cutoff.

  5. Winkler et al. (2015) concluded that high-pass filtered data at 1–2 Hz consistently produced good results in terms of SNR, single-trial classification accuracy and the percentage of 'near-dipolar' ICA components.

* **中文译文与原理解析**：

  高通滤波的目的是消除“基线慢漂移”。虽然传统 ERP 教材（如 Luck, 2005）推荐使用 0.01–0.1 Hz 的低截止频率，但在运行 ICA、ASR 和 CleanLine 时，Makoto 强烈推荐设置 **1 Hz 的通带边缘（Pass-band edge，对应 -6 dB 截止频率约为 0.5 Hz）**，原因如下：

  1. **有限长度下 ICA 对高波幅敏感**：在实际有限时长的数据中，ICA 分解会强烈偏向高振幅信号。

  2. **脑电的** $1/f$ **功率谱分布**：脑电功率随频率降低呈指数级增大（$1/f$ 曲线），这意味着功率谱最左端（$<1\text{ Hz}$）的极低频漂移会主导 ICA 的分解结果，尽管我们真正关注的认知节律主要在 3–30 Hz（Theta、Alpha、Beta）。切掉 $<1\text{ Hz}$ 的部分能让 ICA 聚焦于真正的脑振荡。

  3. **消除出汗等非平稳伪迹**：$<1\text{ Hz}$ 的超慢波极易受皮肤出汗、电极极化等时空非平稳噪声污染，破坏 ICA 的平稳性假设。

  4. **对时频分析（ERSP）完全够用**：在计算 ERSP 时，为了兼顾时间窗长度，最低分析频率通常设为 3 Hz（3 Hz 处使用 3 个小波周期对应的滑动窗长已达 1116 ms），0.5 Hz 的截止频率对 3 Hz 以上的功率与连接性分析没有任何负面影响。

  5. **实证文献支持**：Winkler 等人（2015）证实，1–2 Hz 高通滤波能显著提升 ICA 分解出的“近偶极子（near-dipolar）”脑源成分比例及单试次信噪比。

```
% 使用 EEGLAB 默认新 FIR 滤波器进行 1 Hz 通带边缘高通滤波（对应 -6 dB 截止频率为 0.5 Hz）
EEG = pop_eegfiltnew(EEG, 'locutoff', 1, 'plotfreqz', 0);
```

### 4.2 如果在 >1 Hz 数据上训练 ICA 并迁移到 >0.1 Hz 数据会发生什么？(“自助餐停电”比喻)

* **English Original**:

  On the other hand, 1-Hz high-pass filter attenuates (or distorts) low-frequency 'late slow waves' of ERP family, such as N400 or P600 (Rousselet, 2012). To avoid this problem, one may calculate an ICA weight matrix and a sphering matrix with 1-Hz high-pass filtered data, then apply it to 0.1-Hz high-pass filtered data.

  *What happens to the < 1 Hz data if ICA is calculated on > 1 Hz data and applied to 0.1 Hz data?*

  Imagine you are in a buffet party. On a table, there are four big plates of salad, steak, salmon, and a pudding. The moment you reached your arm to the salad plate, suddenly a blackout happens. You take the salad to your plate in the darkness because you remember where the salad plate is. Now power is back: your salad is drenched with mushroom soup that someone spilled in the darkness!

  This is the situation when > 1-Hz ICA is applied to > 0.1 Hz data. ICA is just a spatial filter, like the locations of the four plates on the table. How much mushroom soup (i.e., 0.1–1.0 Hz EEG info not present in the 1-Hz learning data) you get depends on the spatial distribution of the 0.1–1.0 Hz activity. Practically speaking, 0.1–1.0 Hz data is less likely to be completely independent of > 1.0 Hz data, so most likely it does not hurt very much, though strictly speaking you cannot claim theoretical validity of the decomposition between 0.1–1.0 Hz.

* **中文译文与原理解析**：

  如果你必须分析 N400、P600 等晚期慢波 ERP，1 Hz 高通滤波会扭曲慢波波形。常见折中方案是在 1 Hz 滤波数据上计算 ICA 权重矩阵（`icaweights` 和 `icasphere`），再将其复制迁移到 0.1 Hz 滤波的数据集上。

  为了解释这种做法在 0.1–1.0 Hz 频段内的数学本质，Makoto 提出了著名的“自助餐停电比喻”：ICA 本质上是一个只认空间位置的“空间滤波器”（好比你记住了餐桌上沙拉、牛排、三文鱼和布丁四个盘子的空间位置）；在 $>1\text{ Hz}$ 数据上训练 ICA 并应用到 $>0.1\text{ Hz}$ 数据，就好比你在关灯黑暗中凭记忆去夹沙拉（$>1\text{ Hz}$ 空间滤波器），但黑暗中有人把一碗蘑菇汤（$0.1\text{–}1.0\text{ Hz}$ 慢波）洒在了餐桌上——由于 ICA 训练时“看不见”这碗蘑菇汤，凡是空间分布与沙拉重叠的蘑菇汤都会被一并夹走。如果研究重点是 $>3\text{ Hz}$ **的功率与连接性**，无需使用此折中技巧，直接全程使用 1 Hz 高通滤波最为稳妥。
