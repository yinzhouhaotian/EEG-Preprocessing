# Step 5–9: 电极配准、剔除坏导、球面插值、满秩全脑平均参考与 CleanLine

> 所属手册：Makoto's Preprocessing Pipeline 中英对照（SCCN Wiki，原作者 Makoto Miyakoshi）
>
> 章节导航：[01 导入/降采样/1Hz滤波](01_Import_Resample_and_1Hz_Filter.md) · [02 电极/坏导/插值/重参考/CleanLine](02_Chanlocs_BadChans_Interp_Reref.md) · [03 分段/秩/ICA/DIPFIT](03_Epoch_Rank_ICA_and_DIPFIT.md) · [04 STUDY/ASR/ICLabel/SIFT](04_STUDY_ASR_ICLabel_and_SIFT.md) · [返回 README](../README.md)

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
