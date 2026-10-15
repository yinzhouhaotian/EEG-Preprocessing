# Step 10–15: 小波边缘效应与分段、矩阵有效秩校准、ICA 分解与 DIPFIT 偶极子拟合

> 所属手册：Makoto's Preprocessing Pipeline 中英对照（SCCN Wiki，原作者 Makoto Miyakoshi）
>
> 章节导航：[01 导入/降采样/1Hz滤波](01_Import_Resample_and_1Hz_Filter.md) · [02 电极/坏导/插值/重参考/CleanLine](02_Chanlocs_BadChans_Interp_Reref.md) · [03 分段/秩/ICA/DIPFIT](03_Epoch_Rank_ICA_and_DIPFIT.md) · [04 STUDY/ASR/ICLabel/SIFT](04_STUDY_ASR_ICLabel_and_SIFT.md) · [返回 README](../README.md)

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
