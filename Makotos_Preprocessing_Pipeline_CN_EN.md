# Makoto's Preprocessing Pipeline 中英对照完整指南（附 MATLAB 批处理代码）

> **原文来源 (Original Source)**: [Makoto's preprocessing pipeline - SCCN (Swartz Center for Computational Neuroscience, UCSD)](https://www.google.com/search?q=https%3A%2F%2Feeglab.ucsd.edu%2Fwiki%2FMakoto%27s_preprocessing_pipeline)
>
> **原作者 (Original Author)**: Makoto Miyakoshi (UCSD SCCN)
>
> **配套代码库参考 (Companion Code Wiki)**: [Makoto's useful EEGLAB code - SCCN](https://www.google.com/search?q=https%3A%2F%2Feeglab.ucsd.edu%2Fwiki%2FMakoto%27s_useful_EEGLAB_code) | [EEGLAB Official Tutorials](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F06_RejectArtifacts%2FRunICA.html)
>
> **文档说明**: 本文档将加州大学圣迭戈分校（UCSD）SCCN 维护的经典脑电预处理指南《Makoto's preprocessing pipeline》核心章节（第 1–17 节完整管线、数学原理推导、常见 Bug 修复、ASR 自动化流程、ICLabel 成分筛选及 SIFT 连接性分析准则）整理为**中英双语对照版**，并保留全部原始 MATLAB / EEGLAB 代码片段，方便科研人员学习与在 GitHub 仓库中归档参考。

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

## Step 5: 导入通道坐标与眼电通道处理 (Import channel info & Dedicated EOG channels)

* **English Original**:

  `'Edit' -> 'Channel locations'`. If you have channel labels such as `'Fz' 'Cz' 'Pz'` etc, that means that your channel montage follows International 10-20 / 10-10 / 10-5 system (Oostenveld and Praamstra, 2001). Click `'Look up locs'` and choose `'use MNI coordinate file for BEM dipfit model'`. Don't forget to click `'Opt. head center'`.

  *Do we want to have dedicated EOG channels?*

  If your system spares two electrodes to record EOG: (1) Bipolar referenced EOG; (2) Monopolar referenced EOG sharing the scalp reference; (3) Re-purpose them as scalp EEG channels.

  If you use ICA in your preprocessing, having dedicated EOG electrode(s) is not that necessary because ocular artifacts have broad scalp topography modeled very well by ICA. So (3) is the best answer, and (2) is just as good (using locations AFp9 and AFp10 in the 10-5 system). The worst choice is (1), because by bipolar referencing you lose data dimension by 1 and cannot include them in scalp ICA or average reference.

* **中文译文与原理解析**：

  在 `'Edit' -> 'Channel locations'` 中根据国际 10-5 系统标签自动匹配 MNI 坐标（用于 BEM 偶极子拟合模型），并点击 `'Opt. head center'` 优化球心。

  **关于眼电（EOG）通道的黄金法则**：如果你在预处理中使用 ICA，专门贴双极眼电（Bipolar EOG，即上下眼电或左右眼电互为参考相减）其实是最糟糕的选择，因为双极导联与头皮电极不共享同一个物理参考点，无法纳入全脑平均参考或 ICA 分解。最佳做法是将这些电极改作头皮通道，或者让眼电电极**与头皮脑电共享同一个单极物理参考（Monopolar reference）**（例如贴在 10-5 系统的 `AFp9` 和 `AFp10` 位置），这样它们既能监测眨眼/眼动，又能捕获极具价值的前额叶内侧皮层脑电信号（Delorme et al., 2007）。

```
% 自动查找并匹配 MNI 标准 BEM 头模通道坐标（需将路径替换为你的 EEGLAB 安装路径）
dipfitPath = fileparts(which('dipfitdefs'));
bemFile = fullfile(dipfitPath, 'standard_BEM', 'elec', 'standard_1005.elc');
EEG = pop_chanedit(EEG, 'lookup', bemFile, 'eval', 'chans = pop_chancenter(chans, [], []);');

```

## Step 6: 剔除坏导 (Remove bad channels)

* **English Original**:

  What do you mean bad here? In short, the channels that you can't save even if you reject 5–10% of your datapoints. Removing bad channels is a critical step particularly for average referencing. This is because average reference signal is an average of all channels. If you have channels that are noisy all the time, including such channels to average will introduce noise to all the channels (see Nima's PREP pipeline paper, Bigdely-Shamlo et al., 2015).

  For objective rejection criteria, check out: (1) Nima's PREP pipeline; (2) Christian's `clean_rawdata()` plugin; (3) Makoto's `trimOutlier()`. In writing batch scripts, keep the original `chanlocs` structure (`originalEEG = EEG;`) before channel rejection so that you can refer to it later for channel interpolation.

* **中文译文与原理解析**：

  什么是“坏导”？简言之，就是哪怕你删掉 5%–10% 的时间点也依然救不回来的高噪声或断路（平线）通道。**在进行全脑平均重参考（Average Referencing）之前，必须先剔除坏导！** 因为全脑平均参考会计算所有通道的均值并从每个通道中减去；如果保留了一个持续高噪声的坏导，它的噪声就会通过均值计算扩散污染到全脑每一个好通道中。在写批处理脚本时，务必在剔除坏导前先备份原始通道坐标（`originalEEG = EEG;`），以便后续插值时作为完整坐标模板。

```
% 备份原始完整通道结构，以便后续球面插值使用
originalEEG = EEG;

% 使用 clean_rawdata 仅执行平线通道与高噪坏导剔除（暂不开启 ASR 与时间窗裁剪）
EEG = pop_clean_rawdata(EEG, ...
    'FlatlineCriterion', 5, ...
    'ChannelCriterion', 0.8, ...
    'LineNoiseCriterion', 4, ...
    'Highpass', 'off', ...
    'BurstCriterion', 'off', ...
    'WindowCriterion', 'off', ...
    'BurstRejection', 'off', ...
    'Distance', 'Euclidian');

```

## Step 7: 插值恢复被剔除的通道 (Interpolate all the removed channels)

* **English Original**:

  There are two primary reasons why you want to interpolate the rejected electrodes before average referencing and ICA:

  1. To minimize a bias in the next average referencing. For example, if there are 64 channels and 16 channels are rejected only from the right hemisphere, the average potential across the electrodes is biased toward the left hemisphere.

  2. The rejected electrodes cannot be recovered after ICA because there is no way to interpolate `EEG.icaweights` or `EEG.icasphere`.

     *Caution on Rank Issue*: EEGLAB's default interpolation (`eeg_interp()`, implementing Perrin et al., 1989 spherical spline interpolation with default parameters $m=4, n=7$; note Kang et al., 2015 recommend $m=3, n=50$ for phase analysis) introduces a rank issue because non-linearly interpolated data does not cause a clean rank deficiency; instead, it adds an additional dimension whose eigenvalue is near-zero ($< 10^{-7}$), making the problem ill-conditioned and causing **ghost IC problems** if PCA rank adjustment is not explicitly used during ICA!

* **中文译文与原理解析**：

  在全脑平均重参考之前对坏导进行球面样条插值（Spherical Spline Interpolation，基于 Perrin et al., 1989，默认阶数 $m=4$、截断项数 $n=7$；若做电极间相位连接分析，Kang et al., 2015 证明 $m=3, n=50$ 能最小化相位插值伪迹）有两个原因：一是防止某侧半球剔除通道过多导致全脑平均电位向另一侧半球偏置；二是便于后续群组分析时通道维度对齐。

  **重要方法学警告（插值引发的秩亏缺与连接性污染）**：

  1. **对 ICA 的影响**：球面样条插值属于非线性插值，不会产生干净的零特征值，而是产生约 $10^{-8}$ 的极小特征值，导致 EEGLAB 内置的 `rank()` 检查器误以为数据仍是满秩，从而在运行 ICA 时分解出病态的“幽灵成分（Ghost ICs）”！因此，若在 ICA 前进行了插值，**必须在运行 ICA 时用 `'pca'` 参数显式扣减被插值的通道数**。

  2. **对传感器级连接性的影响**：插值通道是由周围好导拟合而成的虚拟信号，若在传感器层面直接计算通道间功能连接（如相干性、PLV），切勿将被插值通道作为独立网络节点纳入统计，否则会与邻近通道产生极高的假阳性连接。

```
% 使用备份的 originalEEG.chanlocs 进行球面样条插值恢复缺失通道
EEG = pop_interp(EEG, originalEEG.chanlocs, 'spherical');

```

## Step 8: 重参考至全脑平均——为什么必须先补零通道？(Re-reference the data to average)

* **English Original**:

  If EEG is generated on the cortex with dipolar current distribution and with no external sources, there are same amount of positive and negative potential changes at every moment due to charge conservation. Hence the scalp topography should sum to zero. Also, average referencing is often very helpful to suppress common-mode line noise before running CleanLine.

  *Why should we add zero-filled channel before average referencing?* (Published in Kim et al., 2023, *Front. Signal Process.*, DOI: 10.3389/frsip.2023.1064138):

  Unipolar re-referencing should have the 'no memory' property (Hu et al., 2019), meaning one can safely re-reference EEG recordings multiple times without accumulating artifacts or losing data rank. Suppose there are three scalp recordings $Fz, Cz, Pz$, and $Pz$ is chosen as initial reference ($Pz_{\text{REF\_Pz}} = 0$). Correct average potential across all 3 channels (including the initial reference) is:
  

  $$
  AVE_{\text{correct}} = \frac{Fz_{\text{REF\_Pz}} + Cz_{\text{REF\_Pz}} + Pz_{\text{REF\_Pz}}}{3} = \frac{Fz_{\text{REF\_Pz}} + Cz_{\text{REF\_Pz}}}{3}
  $$

  
  However, standard `pop_reref(EEG, [])` without including the initial reference divides by $N$ (here 2) instead of $N+1$ (here 3), which causes $Fz_{\text{AVE}} = -Cz_{\text{AVE}}$ and reduces the data rank by 1!

  By adding a zero-filled channel as the initial reference before computing the average, and then removing that initial reference channel afterward (or simply dividing the channel sum by `EEG.nbchan + 1`), the data rank remains unchanged (full-ranked)!

* **中文译文与原理解析**：

  根据电荷守恒定律，皮层偶极子源在闭合头皮表面产生的正负电位积分之和应为零，全脑平均参考（CAR）正是对参考无关电位的良好近似，同时还能通过共模抑制大幅削弱非平稳工频噪声。

  **核心纠错（Kim et al., 2023 论文证明）**：为什么常规的全脑平均参考会导致数据矩阵的秩（Rank）减 1？因为采集脑电时共有 $N$ 个记录电极和 $1$ 个物理参考电极（其自身相对于参考的电位恒为 $0$），总电极数实际上是 $N+1$。真正的全脑平均电位应当除以 $N+1$；如果直接对现有的 $N$ 个非零记录通道求均值并相减（除以 $N$），不仅违反了单极参考的“无记忆性（No-memory property）”，还会强制使 $N$ 个通道之和恒等于 0，人为造成线性相关（秩亏缺 1 维），进而在 ICA 中引发正负极性反转成对出现的“幽灵成分（Ghost ICs）”。

  **正确做法**：在全脑平均参考前，先向数据矩阵追加一个全为 0 的虚拟初始参考通道（`'initialReference'`），执行平均重参考后再将该通道删去（即分母除以 `EEG.nbchan + 1`），即可完美保持数据满秩！

```
% 满秩全脑平均重参考法 (Full-Rank Average Referencing, Kim et al., 2023)
EEG.nbchan = EEG.nbchan + 1;
EEG.data(end+1, :) = zeros(1, EEG.pnts);
EEG.chanlocs(1, EEG.nbchan).labels = 'initialReference';
EEG = pop_reref(EEG, []);
EEG = pop_select(EEG, 'nochannel', {'initialReference'});

```

## Step 9: 使用 CleanLine 去除工频噪声 (Remove line noise using CleanLine)

* **English Original**:

  CleanLine (developed by Tim Mullen) is not a standard frequency notch filter, but uses a sliding window and multitapers to adaptively estimate sine wave amplitude to subtract. It does not make a hole in the background EEG spectrum.

  *Critical Bug Warning*: The original implementation of CleanLine suffered from a bug. In the newer plugin version, you MUST check the very last checkbox `'Use new implementation (send us feedback)'` (setting `legacy` to `false` / using PREP's `cleanLineNoise` implementation). By default it is set to `false`, which completely destroys the effect of CleanLine! Note that CleanLine assumes the 50/60 Hz line noise amplitude envelope is stationary within the sliding window (default 4 s); performing average referencing before CleanLine helps remove non-stationary common-mode line noise.

* **中文译文与原理解析**：

  传统的 50/60 Hz 陷波滤波器（Notch Filter）会在背景脑电频谱上挖出一个深坑，并造成时域振铃失真与自回归模型阶数膨胀。`CleanLine` 插件利用滑动窗口与多锥度谱（Multitaper）自适应拟合确定性的正弦工频干扰并从原信号中减去，不会损伤同一频段的随机脑电活动。

  **防坑必看**：旧版 `CleanLine` 存在一个未报错的代码 Bug，导致去工频效果大打折扣。在使用新版 `CleanLine` 时，**必须在 GUI 最底部勾选 `'Use new implementation'`**（或在代码中调用修复后的 `cleanLineNoise` 实现）。另外，先做完第 8 步的全脑平均参考再跑 `CleanLine`，能先消除共模工频波动，显著提升 `CleanLine` 的平稳拟合效果。

```
% 使用 CleanLine 去除 50 Hz 及 100 Hz 谐波工频干扰（我国市电为 50 Hz，北美为 60 Hz）
EEG = pop_cleanline(EEG, 'bandwidth', 2, 'chanlist', 1:EEG.nbchan, ...
    'computepower', 1, 'linefreqs', [50 100], 'newversion', 1, ...
    'normSpectrum', 0, 'p', 0.01, 'pad', 2, 'plotfigures', 0, ...
    'scanforlines', 0, 'sigtype', 'Channels', 'taperbandwidth', 2, ...
    'tau', 100, 'verb', 1, 'winsize', 4, 'winstep', 4);

```

## Step 10: 数据分段至 -1 到 2 秒 (Epoch data to -1 to 2 sec)

* **English Original**:

  If you have sufficient number of data points after epoching, epoching before ICA is recommended so that ICA can focus on peri-event brain dynamics. If your Stimulus Onset Asynchrony (SOA) is shorter than 3 seconds or data points are insufficient, do NOT epoch before ICA—use continuous data to perform ICA, then epoch, because overlapping epochs submitted to ICA will cause it to learn the duplicated part as positively weighted data.

  *Why -1 to 2 sec for Time-Frequency (ERSP/ITC)?*

  This phenomenon of shortening the epoch after wavelet transform is related to the **Cone of Influence (COI)**. With a 3-cycle wavelet at 3 Hz (at 250 Hz sampling rate), the wavelet sliding window length is $1116\text{ ms}$ ($279\text{ samples}$). You lose half of the window length ($556\text{ ms}$) from the beginning and half ($556\text{ ms}$) from the ending of the epoch! Thus, epoching from $-1000\text{ ms}$ to $+2000\text{ ms}$ leaves you with an effective time-frequency window of roughly $-444\text{ ms}$ to $+1444\text{ ms}$.

  *Crucial Baseline Rule before ICA*: Do NOT subtract a short baseline (such as $-100$ to $0\text{ ms}$) before running ICA! David Groppe et al. (2009) showed that subtracting a short baseline before ICA severely degrades ICA reliability because background alpha rhythms randomly shift the short-window mean across channels. Since the data is already 1-Hz high-pass filtered (zero-mean), baseline subtraction before ICA is completely unnecessary.

* **中文译文与原理解析**：

  在分段（Epoching）环节有三条针对时频功率与 ICA 的核心准则：

  1. **何时在 ICA 前分段 vs. 连续数据跑 ICA**：如果试次间间隔（SOA）较长且分段后数据点充足，在 ICA 前分段可让 ICA 专注于任务事件周边的脑动态；但如果你的实验刺激间隔较短（导致相邻 Epoch 时间窗重叠）或任务试次较少，**切勿在 ICA 前分段**（重叠的数据点会让 ICA 重复学习相同片段），应直接在连续数据上跑完 ICA 后再分段。

  2. **为什么时频分析（ERSP/ITC）必须预留超过 0.5 秒的缓冲期（影响锥 COI）**：小波变换的最低频率决定了滑动窗口的宽度。例如最低分析频率为 $3\text{ Hz}$、使用 $3$ 个周期的小波时，其时间窗宽度为 $3 \times (1000 / 3) \approx 1116\text{ ms}$。由于滑动窗中心在抵达试次首尾两端各一半窗宽（约 $556\text{ ms}$）处就无法继续向外滑动，算出的时频图首尾两端会各被裁掉 $556\text{ ms}$！因此，截取 $-1000\text{ ms}$ 到 $+2000\text{ ms}$ 的分段，在小波变换后实际只剩下约 $-444\text{ ms}$ 到 $+1444\text{ ms}$ 的有效时间窗。

  3. **严禁在 ICA 前减去短时域基线**：Groppe 等人（2009，*NeuroImage*）证实，如果在 ICA 前减去 $-100\text{ 至 }0\text{ ms}$（或 $-200\text{ 至 }0\text{ ms}$）的短基线均值，由于背景 Alpha 波在该短窗口内的随机相位波动，会给每个通道人为注入独立的直流偏移，严重破坏 ICA 分解的可靠性。只要之前做过了 1 Hz 高通滤波，数据本身就是零均值的，**在 ICA 前不需要做基线校正**。

```
% 围绕目标事件标记分段（例如 -1.0 秒至 +2.0 秒），注意此时不执行短基线相减
EEG = pop_epoch(EEG, {'S1', 'S2'}, [-1.0 2.0], 'newname', 'Epoched_EEG', 'epochinfo', 'yes');

```

## Step 11: 剔除极端坏段试次 (Reject epochs for cleaning)

* **English Original**:

  Aim for around 5–10% rejection rate (Delorme et al., 2007). Apply amplitude threshold of $-500$ to $500\,\mu\text{V}$ (don't capture eye blinks here; eye blinks will be removed by ICA), reject the selected epochs, and apply improbability test with $6\text{ SD}$ for single channels and $2\text{ SD}$ for all channels, and reject the selected again.

* **中文译文与原理解析**：

  在送入 ICA 前剔除坏段的目标是**清除罕见的非生物大振幅突变（如电极线剧烈晃动、吞咽动作）**，而不是剔除眨眼（眨眼具有极稳定的空间拓扑，留给 ICA 去除即可）。因此，在 ICA 前使用宽松的波幅阈值（如 $\pm 500\,\mu\text{V}$）配合联合概率分布检验（单通道 $6\text{ SD}$，全通道 $2\text{ SD}$），将总试次剔除率控制在 5%–10% 左右；待 ICA 去除眼电和肌电后，再用严格阈值（如 $\pm 100\,\mu\text{V}$）做最终质控。

```
% ICA 前预清洗：剔除波幅超出 [-500, 500] uV 及联合概率异常（单通道 6 SD, 全通道 2 SD）的极端坏段
EEG = pop_eegthresh(EEG, 1, 1:EEG.nbchan, -500, 500, EEG.xmin, EEG.xmax, 0, 1);
EEG = pop_jointprob(EEG, 1, 1:EEG.nbchan, 6, 2, 0, 1, 0, [], 0);

```

## Step 12: 为 ICA 调整数据矩阵的有效秩 (Adjust data rank for ICA)

* **English Original**:

  When performing ICA, the number of ICs to generate must not exceed the true 'effective rank' of the input data. Your data becomes rank-deficient by:

  1. Re-referencing without including the initial reference (rank deficient by 1);

  2. Interpolating $k$ channels (rank deficient by $k$);

  3. Bridging $n$ channels due to conductive gel spreading (rank deficient by $n-1$).

     Because EEGLAB's spherical spline interpolation is non-linear, `rank()` fails to detect the rank reduction and leaves eigenvalues $< 10^{-6}$, causing **ghost ICs**. Always compute the effective rank using an eigenvalue threshold of $10^{-7}$ (or $10^{-6}$) on the covariance matrix, and pass it to `runica` via the `'pca'` option (or `'pcakeep'` for AMICA).

* **中文译文与原理解析**：

  ICA 分解生成的独立成分数量绝不能超过输入数据的真实**有效秩（Effective Rank）**。不加初始参考的平均重参考会使秩减 1，球面插值 $k$ 个坏导会使有效秩减 $k$，导电膏连桥（Bridging）$n$ 个电极会使秩减 $n-1$。由于 MATLAB 自带的 `rank()` 函数会被球面样条插值产生的微小非线性特征值欺骗，最稳健的做法是直接计算数据协方差矩阵的特征值，统计大于 $10^{-7}$（或 $10^{-6}$）的特征值个数作为真实有效秩 `dataRank`，并在运行 ICA 时通过 `'pca', dataRank` 显式传入。

```
% 使用协方差矩阵特征值阈值 (1e-7) 计算真实的数值有效秩，彻底杜绝幽灵成分 (Ghost ICs)
tmpdata = double(EEG.data(:, :));
covarianceMatrix = cov(tmpdata', 1);
[~, D] = eig(covarianceMatrix);
rankTolerance = 1e-7;
dataRank = sum(diag(D) > rankTolerance);
fprintf('Current effective data rank for ICA: %d (out of %d channels)\n', dataRank, EEG.nbchan);

```

## Step 13: 运行独立成分分析 (Run ICA)

### 13.1 最小数据长度、空间平稳性假设与实操准则

* **English Original**:

  *Minimum length of data*: SCCN recommends at least $(\text{number of channels})^2 \times k$ data points, where $k = 20\text{ to }30$ (Makeig & Onton, 2011). Note that actual recording duration in time is more important than raw sample count inflated by high sampling rates.

  *Assumption of spatial stationarity*: ICA assumes that the spatial mixing relationship between cortical sources and scalp sensors remains constant throughout the recording. Therefore:

  1. Never concatenate blocks where the subject took off and re-applied the electrode cap, or where you re-gelled electrodes during a break (even shifting or re-gelling a single electrode splits ICA components into before/after blocks!).

  2. Include monopolar EOG/ECG channels ONLY if they share the exact same reference electrode as scalp channels; exclude bipolar channels.

  3. *Why rejecting ICs and running a second ICA does NOT work*: If you have 100-ch full-rank data, reject 1 blink IC, back-project the remaining 99 ICs to the 100 channels, and run ICA again, the rank is now 99 and the remaining 99 ICs will be identical to the first run because the blink IC was already independent of the other ICs! (To improve ICA, you must reject bad *time points/epochs* that violate stationarity, not ICs).

  4. *Does ICA distort phase?* (Response to Montefusco-Siegmund et al., 2013): Resounding NO. Removing an artifactual IC changes the scalp phase simply because you subtracted the artifact's phase contribution ($4 + 8 - 4 = 8$), which is linear unmixing, not phase distortion.

  5. *Is using PCA bad for ICA?* Using PCA is completely fine and recommended to match true effective rank (Case 1) or when recording duration is too short for high-density arrays (Case 2), but should NOT be used merely to speed up computation (Case 3, Artoni et al., 2018).

* **中文译文与原理解析**：

  1. **样本量要求**：经验公式要求送入 ICA 的总时间点数至少达到 $\text{通道数}^2 \times (20\text{ 至 }30)$（例如 64 导脑电建议至少有 $64^2 \times 20 = 81,920$ 个采样点）。注意：真实物理记录时长比单纯靠高采样率堆砌的点数更重要。

  2. **空间平稳性铁律**：ICA 假设大脑源到头皮电极的空间传导矩阵全程恒定。因此，如果被试在实验中途摘下重戴过脑电帽，甚至哪怕你**在中途休息时给某一个电极补注了导电膏（Re-gelling）**，改变了局部阻抗和空间投影，都不能直接合并跑同一个 ICA（否则 ICA 会把补膏前后分裂成两套独立成分）。

  3. **为什么“剔除眼电成分后再跑第二次 ICA”是无效的？** 从 100 导满秩数据中剔除 1 个眨眼 IC 并反投影回 100 导后，数据矩阵的秩已经变成了 99；由于各独立成分之间本身就是统计独立的，拿反投影数据再跑一次 ICA 只会原封不动地得到剩下的 99 个成分。想要提升 ICA 分解质量，应当剔除破坏平稳性的坏时间段（Bad epochs/timepoints）后重跑 ICA，而不是剔除 IC 后重跑。

  4. **ICA 去伪迹会扭曲相位（Phase）从而影响连接性分析吗？** 不会。从混合信号中减去眼电 IC 引起的相位变化，就如同从 $4+8$ 中减去 $4$ 得到 $8$ 一样，是剥离伪迹相位后的真实神经相位恢复，而非非线性相位失真。

```
% 使用扩展 Infomax (runica) 并结合有效秩 dataRank 运行 ICA
EEG = pop_runica(EEG, 'icatype', 'runica', 'extended', 1, 'pca', dataRank, 'interrupt', 'off');

```

## Step 14 & Step 15: 头模配准与单/双侧等效电流偶极子拟合 (Dipole Fitting with DIPFIT)

* **English Original**:

  `'Tools' -> 'Locate dipoles using DIPFIT 2.x' -> 'Head model and settings'`, then `'Autofit (coarse fit, fine fit & plot)'`. Note that EEGLAB's head model uses `millimeter (mm)` as default unit; if all your fitted dipoles cluster at the very center of the head, your electrode coordinates are in `cm` or `m`—multiply `X, Y, Z` by `10` or `1000`.

  After fitting single dipoles, run the `fitTwoDipoles` plugin (`EEG = fitTwoDipoles(EEG, 'LRR', 35);`, Piazza et al., 2016) to capture symmetrically constrained bilateral sources (such as bilateral occipital alpha or auditory cortex sources).

* **中文译文与原理解析**：

  为什么要做偶极子拟合（DIPFIT）？因为真正的皮层脑源成分在头皮上的拓扑投影具有高度的“偶极子性（Dipolarity）”，通过拟合等效电流偶极子并计算**残差方差（Residual Variance, RV，即理论偶极子投影与实际 IC 拓扑之差的方差占比）**，我们可以用客观定量指标（通常要求 $\text{RV} < 15\%$ 且偶极子位于脑实质内）筛选高质量脑成分，并为源空间连接性分析（如 SIFT）提供三维空间坐标。此外，调用 `fitTwoDipoles` 插件可进一步拟合左右半球对称激活的双侧同步脑源。

```
% 配置 MNI 标准四层 BEM 头模型并进行单偶极子自动拟合 (DIPFIT)
dipfitPath = fileparts(which('dipfitdefs'));
EEG = pop_dipfit_settings(EEG, ...
    'hdmfile', fullfile(dipfitPath, 'standard_BEM', 'standard_vol.mat'), ...
    'coordformat', 'MNI', ...
    'mrifile', fullfile(dipfitPath, 'standard_BEM', 'standard_mri.mat'), ...
    'chanfile', fullfile(dipfitPath, 'standard_BEM', 'elec', 'standard_1005.elc'), ...
    'coord_transform', [0 0 0 0 0 -1.5708 1 1 1], ...
    'chansel', 1:EEG.nbchan);

% 自动执行粗拟合与精拟合，设置初始剔除阈值为 100%（保留所有偶极子以便后续筛选）
EEG = pop_multifit(EEG, 1:size(EEG.icaweights, 1), 'threshold', 100, 'plotopt', {'normlen', 'on'});

% （可选，需安装 fitTwoDipoles 插件）搜索并拟合对称双侧偶极子
if exist('fitTwoDipoles', 'file')
    EEG = fitTwoDipoles(EEG, 'LRR', 35);
end

```

## Step 16: 创建 STUDY 群组分析与避免循环推断 (Create STUDY & Avoid Double Dipping)

* **English Original**:

  When creating a STUDY across subjects, it automatically filters ICs based on two criteria: (1) Dipoles with $< 15\%$ residual variance (Artoni et al., 2014); (2) Dipoles located inside the brain volume.

  *Avoid Double Dipping (Circular Inference)*: If you are going to test ERP / ERSP / ITC / PSD differences across conditions at the end of the day, **DO NOT choose any of them to cluster ICs**! Clustering ICs using ERSP or ERP waveforms minimizes within-cluster variance on that exact metric and kicks out dissimilar waveforms, inflating Type I error (false positives, Kriegeskorte et al., 2009). **Solution**: USE ONLY DIPOLE LOCATIONS (`xyz` coordinates) to cluster ICs (Miyakoshi et al., 2020, 2021). Because ICA is completely agnostic to spatial coordinates, clustering solely by dipole 3D location never causes double dipping when testing time-frequency or connectivity metrics.

  *Tip for Time-Frequency (ERSP & ITC) parameters*: Recommend `3 cycles at 3 Hz` for the lowest frequency, and `7–10 cycles at 50 Hz` (i.e., `cycles = [3 0.5]` or `[3 0.8]` in `newtimef`).

* **中文译文与原理解析**：

  在多被试群组分析（STUDY）中，如果直接在 ICA 源空间对独立成分进行 K-means 聚类，**切忌使用 ERP 波形、功率谱（PSD）或时频图（ERSP）特征参与聚类，然后再对聚类后的同一个指标做条件间统计检验**！这种做法属于典型的“双重蘸取 / 循环推断（Double Dipping, Kriegeskorte et al., 2009）”，会人为压低组内方差并导致假阳性率暴增。**唯一合规的做法是：仅使用偶极子的三维空间坐标（Dipole XYZ locations）进行聚类**。

  在进行时频变换（`newtimef`）计算事件相关谱扰动（ERSP）和试次间相干性（ITC）时，推荐将小波周期参数设为在最低频率 3 Hz 处使用 3 个周期，随频率升高线性递增至 50 Hz 处约 7–10 个周期。

## Step 17: 进阶笔记：ASR 自动管线、ICLabel 自动筛选与 SIFT 连接性准则 (Notes & Automated Pipelines)

### 17.1 基于 ASR 与 ICLabel 的现代 15 步全自动管线 (Suggested Automated Pipeline)

* **English Original**:

  In high-density EEG, rejecting an entire epoch whenever a single channel has a brief artifact wastes too much data. Using **Artifact Subspace Reconstruction (ASR)** in `clean_rawdata()` (with empirically validated threshold $\text{SD} = 20$, Chang et al., 2020; make sure to uncheck `'Remove bad data periods'` so ASR repairs bursts rather than chopping up the data) followed by automated component classification via **`ICLabel()`** provides a reproducible automated pipeline:

  1. Set double precision -> 2. Import data -> 3. Downsample -> 4. High-pass filter at 1 Hz -> 5. Import channel info -> 6. Bad channel rejection -> 7. CleanLine -> 8. Apply ASR (`SD = 20`) to repair continuous bursts -> 9. Interpolate removed channels -> 10. Full-rank average reference -> 11. Run ICA with `'pca'` adjusted to effective rank -> 12. Fit single dipoles (DIPFIT) -> 13. Fit bilateral dipoles -> 14. Automated IC selection using `ICLabel()` -> 15. Epoch cleaned data (e.g., -1 to 2 sec).

* **中文译文与原理解析**：

  针对通道数较多或任务试次珍贵的数据，Makoto 推荐结合 ASR（伪迹子空间重构，阈值设为 `SD = 20`，仅修复不删时间段）与 ICLabel（基于深度学习的自动独立成分分类器）构建全自动批处理管线。在通过 `ICLabel` 筛选成分时，标准准则为：**保留“脑源（Brain）”分类概率** $\ge 0.70$ **且偶极子残差方差** $\text{RV} < 0.15$**（且偶极子位于脑内）的成分**（若你的目标是仅剔除眼电/肌电等明确伪迹并尽量保留全部脑信号，也可采取“反向剔除法”：仅剔除 Eye / Muscle / Heart / Line Noise / Channel Noise 概率 $> 0.70$ 或 $0.80$ 的伪迹成分）。

```
% 使用 ICLabel 自动分类独立成分并筛选高质量脑源成分（概率 >= 0.7 且偶极子残差方差 RV < 0.15）
EEG = iclabel(EEG, 'default');
brainIdx  = find(EEG.etc.ic_classification.ICLabel.classifications(:, 1) >= 0.70);
rvList    = [EEG.dipfit.model.rv];
goodRvIdx = find(rvList < 0.15);
goodIcIdx = intersect(brainIdx, goodRvIdx);

% 仅保留筛选出的高质量脑源成分，将其余伪迹成分从通道数据中减去
EEG = pop_subcomp(EEG, goodIcIdx, 0, 1);
EEG.etc.ic_classification.ICLabel.classifications = ...
    EEG.etc.ic_classification.ICLabel.classifications(goodIcIdx, :);

```

### 17.2 针对连接性分析（SIFT / 多变量格兰杰因果）的专属预处理准则 (SIFT & Connectivity Tips)

* **English Original**:

  1. *Why avoid sensor-level connectivity directly?* Calculating connectivity directly at the scalp sensor level suffers severely from **volume conduction** (Brunner et al., 2016). Decomposing data into temporally independent sources via ICA (and running SIFT on ICs) or projecting to cortical source space addresses volume conduction.

  2. *What filter should be used for Granger Causality / MVAR?* While Barnett and Seth (2011) showed multivariate Granger causality is theoretically invariant under zero-phase filtering, in practice **filtering complicates the power spectral density (PSD) and inflates the required MVAR model order**: steep roll-offs, stopband floors, and deep spectral holes created by notch filters all worsen model order estimation! Therefore, NEVER use a notch filter or steep low-pass filter before MVAR connectivity. Use a gentle high-pass filter (1 Hz) to ensure stationarity, and use `CleanLine` if needed.

  3. *Downsample data to 100 Hz (or 128 Hz) to keep PSD simple*: Downsampling to \~100 Hz pushes the 50/60 Hz line noise near or outside the Nyquist frequency and keeps the PSD smooth, allowing a much lower and more stable MVAR model order. Use custom anti-aliasing parameters so the stopband does not fall below the Nyquist frequency: `EEG = pop_resample(EEG, 100, 0.8, 0.4);` (for 100 Hz target rate, Nyquist is 50 Hz, -6 dB cutoff is $50 \times 0.8 = 40\text{ Hz}$, transition bandwidth is $50 \times 0.4 = 20\text{ Hz}$, so passband edge is 30 Hz and stopband hits 50 Hz).

  4. *Datapoint-to-parameter ratio*: To reliably fit an MVAR model, the ratio `(num_IC * model_order) / (window_length_samples * num_trials)` should be $< 0.1$ (at least 10 data points per estimated parameter). Combining trials or using longer sliding windows improves model stability.

* **中文译文与原理解析（专为你的“任务态功率与连接性”研究划重点）**：

  1. **克服容积传导**：直接在头皮电极上算连接性会受到容积传导的严重干扰（Brunner et al., 2016），建议在 ICA 独立成分空间（使用 EEGLAB 的 SIFT 工具箱）或源定位空间（使用 FieldTrip 的 Beamformer）计算连接性，或者在传感器空间仅使用去零延迟指标（如 wPLI、相干性虚部 iCoh）。

  2. **连接性分析的滤波禁忌**：虽然理论上零相位滤波不改变因果方向（Barnett & Seth, 2011），但在实际计算自回归模型（MVAR / 格兰杰因果）时，**任何陡峭的低通滤波或 50 Hz 陷波滤波都会在频谱上留下阻带平底或深坑，导致自回归模型阶数（Model Order）急剧膨胀甚至拟合失败**！因此做连接性时应只做温和的 1 Hz 高通滤波以保证平稳性，严禁使用传统陷波滤波器。

  3. **100 Hz 定制降采样技巧**：如果主要关注 3–40 Hz（Theta / Alpha / Beta / 低 Gamma）的功率与连接性，且 50 Hz 工频干扰极强，Makoto 推荐使用 `EEG = pop_resample(EEG, 100, 0.8, 0.4);` 将采样率降至 100 Hz。该命令将抗混叠滤波器的 -6 dB 截止点设在 40 Hz、过渡带宽度设为 20 Hz（即 30 Hz 以下完全无损通过，到 50 Hz 奈奎斯特频率处刚好衰减至阻带），既能完美避开 50 Hz 市电干扰，又能让功率谱保持平滑，大幅降低连接性建模难度。

## 附：可直接运行的完整 MATLAB 批处理脚本模板 (`makoto_batch_pipeline.m`)

以下脚本串联了上述全部核心步骤，适配任务态功率与连接性分析需求：

```
%% ========================================================================
%  Makoto's Preprocessing Pipeline - Standardized MATLAB Batch Script
%  适用场景：任务态脑电功率谱（PSD/ERSP）与功能连接（Connectivity）预处理
%  依赖工具箱：EEGLAB (含 clean_rawdata, CleanLine, DIPFIT, ICLabel 插件)
% =========================================================================
clear; clc;

% 1. 启动 EEGLAB 并强制开启双精度运算 (Step 1)
[ALLEEG, EEG, CURRENTSET, ALLCOM] = eeglab;
pop_editoptions('option_single', false, 'option_computeica', true);

% 设置数据路径与待处理文件列表（注意路径名不要包含空格或中文字符，Step 2）
rawFolder  = '/path/to/your/raw_data';
saveFolder = '/path/to/your/preprocessed_data';
if ~exist(saveFolder, 'dir'), mkdir(saveFolder); end

subFiles = dir(fullfile(rawFolder, '*.set')); % 若为其他格式可改为 pop_biosig / pop_loadbv
targetSfreq = 250;                            % 常规时频与相位连接用 250 Hz；若跑 SIFT MVAR 可设为 100
eventMarkers = {'S1', 'S2'};                  % 替换为你的任务态刺激 Trigger 名称
epochWindow  = [-1.0 2.5];                    % 两端预留 >0.5s 缓冲窗以抵消小波边缘效应 (COI)

for iSub = 1:length(subFiles)
    subName = subFiles(iSub).name;
    fprintf('\n================ Processing Subject %d/%d: %s ================\n', ...
        iSub, length(subFiles), subName);
    
    % 2. 导入原始数据 (Step 2)
    EEG = pop_loadset('filename', subName, 'filepath', rawFolder);
    EEG = eeg_checkset(EEG);
    
    % 3. 连续数据降采样（内置抗混叠滤波，必须在分段前执行，Step 3）
    if EEG.srate > targetSfreq
        EEG = pop_resample(EEG, targetSfreq);
    end
    
    % 4. 1 Hz 高通滤波消除慢漂移，保障宽平稳性 WSS 与 ICA 质量 (Step 4)
    EEG = pop_eegfiltnew(EEG, 'locutoff', 1, 'plotfreqz', 0);
    
    % 5. 导入标准 10-5 系统 MNI 通道坐标并优化头心 (Step 5)
    dipfitPath = fileparts(which('dipfitdefs'));
    bemChanFile = fullfile(dipfitPath, 'standard_BEM', 'elec', 'standard_1005.elc');
    EEG = pop_chanedit(EEG, 'lookup', bemChanFile, ...
        'eval', 'chans = pop_chancenter(chans, [], []);');
    
    % 备份完整通道坐标供后续插值使用（若做纯传感器空间连接性，可跳过插值步骤）
    originalEEG = EEG;
    
    % 6. 剔除坏导并使用 ASR (SD = 20) 修复连续突发大伪迹（不切碎时间轴，Step 6 & 17.1）
    EEG = pop_clean_rawdata(EEG, ...
        'FlatlineCriterion', 5, ...
        'ChannelCriterion', 0.8, ...
        'LineNoiseCriterion', 4, ...
        'Highpass', 'off', ...
        'BurstCriterion', 20, ...
        'WindowCriterion', 'off', ...
        'BurstRejection', 'off', ...
        'Distance', 'Euclidian');
    
    % 7. 球面样条插值恢复坏导以防止平均参考偏置 (Step 7)
    %    注意：若后续在传感器空间直接计算通道间连接性，请记录被插值通道索引并在连接矩阵中将其排除
    EEG = pop_interp(EEG, originalEEG.chanlocs, 'spherical');
    
    % 8. 满秩全脑平均重参考（先补零值初始参考通道，求平均后再移除，Step 8）
    EEG.nbchan = EEG.nbchan + 1;
    EEG.data(end+1, :) = zeros(1, EEG.pnts);
    EEG.chanlocs(1, EEG.nbchan).labels = 'initialReference';
    EEG = pop_reref(EEG, []);
    EEG = pop_select(EEG, 'nochannel', {'initialReference'});
    
    % 9. 使用新版 CleanLine 去除 50 Hz 及 100 Hz 工频正弦噪声，不破坏背景频谱 (Step 9)
    if exist('pop_cleanline', 'file')
        EEG = pop_cleanline(EEG, 'bandwidth', 2, 'chanlist', 1:EEG.nbchan, ...
            'computepower', 1, 'linefreqs', [50 100], 'newversion', 1, ...
            'normSpectrum', 0, 'p', 0.01, 'pad', 2, 'plotfigures', 0, ...
            'scanforlines', 0, 'sigtype', 'Channels', 'taperbandwidth', 2, ...
            'tau', 100, 'verb', 0, 'winsize', 4, 'winstep', 4);
    end
    
    % 10. 计算数据协方差矩阵的真实有效秩，防止插值引发 ICA 幽灵成分 (Step 12)
    tmpdata = double(EEG.data(:, :));
    covarianceMatrix = cov(tmpdata', 1);
    [~, D] = eig(covarianceMatrix);
    dataRank = sum(diag(D) > 1e-7);
    
    % 11. 运行扩展 Infomax ICA，显式传入 pca 维度 = dataRank (Step 13)
    EEG = pop_runica(EEG, 'icatype', 'runica', 'extended', 1, ...
        'pca', dataRank, 'interrupt', 'off');
    
    % 12. 使用 DIPFIT 拟合等效电流偶极子 (Step 14)
    EEG = pop_dipfit_settings(EEG, ...
        'hdmfile', fullfile(dipfitPath, 'standard_BEM', 'standard_vol.mat'), ...
        'coordformat', 'MNI', ...
        'mrifile', fullfile(dipfitPath, 'standard_BEM', 'standard_mri.mat'), ...
        'chanfile', bemChanFile, ...
        'coord_transform', [0 0 0 0 0 -1.5708 1 1 1], ...
        'chansel', 1:EEG.nbchan);
    EEG = pop_multifit(EEG, 1:size(EEG.icaweights, 1), 'threshold', 100, ...
        'plotopt', {'normlen', 'on'});
    
    % 13. 使用 ICLabel 自动剔除眼电与肌电伪迹（或保留脑源概率 >= 0.7 且 RV < 0.15 成分，Step 17.1）
    EEG = iclabel(EEG, 'default');
    icScores = EEG.etc.ic_classification.ICLabel.classifications;
    % 策略：剔除眼电(第3列)或肌电(第2列)或心电(第4列)概率 > 0.70 的伪迹成分
    artifactIcIdx = find(icScores(:, 2) > 0.70 | icScores(:, 3) > 0.70 | icScores(:, 4) > 0.70);
    EEG = pop_subcomp(EEG, artifactIcIdx, 0);
    
    % 14. 任务态分段（不减短时域基线，保留频域基线归一化，Step 10）
    EEG = pop_epoch(EEG, eventMarkers, epochWindow, 'epochinfo', 'yes');
    
    % 15. 最终波幅阈值质控：剔除残留超过 [-100, 100] uV 的极端坏段 (Step 11)
    EEG = pop_eegthresh(EEG, 1, 1:EEG.nbchan, -100, 100, EEG.xmin, EEG.xmax, 0, 1);
    
    % 保存预处理完成的 .set 文件（后续可直接用 eeglab2fieldtrip 导入 FieldTrip 算功率和连接性）
    EEG = pop_saveset(EEG, 'filename', ['clean_' subName], 'filepath', saveFolder);
end

```