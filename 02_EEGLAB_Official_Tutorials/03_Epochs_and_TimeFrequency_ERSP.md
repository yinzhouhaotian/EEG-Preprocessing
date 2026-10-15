# Ch 7–8: 分段基线注意事项与时频分解实战（ERSP 功率与 ITC 相干性）

> 所属手册：EEGLAB Official Tutorials 官方在线教程中英对照（eeglab.org/tutorials/，SCCN / UCSD）
>
> 章节导航：[01 导入与滤波规则](01_Import_and_Filtering_Rules.md) · [02 clean_rawdata/ICA/ICLabel](02_CleanRawdata_ICA_and_ICLabel.md) · [03 分段与时频ERSP](03_Epochs_and_TimeFrequency_ERSP.md) · [04 DIPFIT/STUDY/ROIconnect](04_DIPFIT_STUDY_and_ROIconnect.md) · [返回 README](../README.md)

## Chapter 7: 提取数据分段与筛选子集 (Extract Data Epochs)

* **English Original** ([Tutorials -\> 7. Extract Data Epochs](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F07_Extract_epochs%2FExtracting_Data_Epochs.html)):

  Select `Tools -> Extract Epochs` (`pop_epoch.m`), choose the time-locking event type(s), and retain epoch limits such as `[-1 2]` seconds (3 seconds long). **It is often better to extract long data epochs, as here, to make time-frequency decomposition possible at lower (below 10 Hz) frequencies.**

  *Removing baseline values*: After epoching, `Tools -> Remove baseline` (`pop_rmbase.m`) pops up. High-pass filtering is already a form of baseline correction, rendering this step optional. Avoid short baseline windows (on the order of 100 ms) whenever possible.

  *Extracting sub-epochs & Selecting epochs by event info*: Use `Edit -> Select data` (`pop_select.m`) to crop sub-epochs or remove specific trial indices, or `Edit -> Select epochs or events` (`pop_selectevent.m`) to select trials matching specific event metadata fields (making sure `'Remove epochs not referenced by any selected event'` is checked).

* **中文译文与操作解析**：

  在 `Tools -> Extract Epochs`（`pop_epoch.m`）中围绕任务事件分段时，官方特别指出：**为了能够分析 10 Hz 以下（如 Theta、Alpha 频段）的时频功率与相位，应该截取至少 3 秒长（例如 `-1` 到 `2` 秒）的宽时间窗**。若已做过 1 Hz 高通滤波且关注的是频域功率/连接性，时域 `pop_rmbase` 是可选的（若做 ERP 基线校正，应选在 ICA 完成之后，且基线窗口不宜过短）。

## Chapter 8: 频谱与时频分解实战——ERSP 与 ITC (Spectra & Time-Frequency Decomposition)

* **English Original** ([Tutorials -\> 8.d Time-Frequency](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F08_Plot_data%2FTime-Frequency_decomposition.html)):

  To detect transient **Event-Related Spectral Perturbation (ERSP)** (event-related shifts in the power spectrum in dB relative to baseline, Makeig, 1993) and **Inter-Trial Coherence (ITC)** (event-related phase-locking across trials) in epoched datasets, select `Plot -> Time-frequency transforms -> Channel time-frequency` (`pop_newtimef.m`).

  *Understanding `"Wavelet cycles" = [3 0.8]`*:

  The default entry `3 0.8` means that the sinusoidal wavelet (Hanning-tapered) begins with a **3-cycle wavelet** at the lowest frequency, and the number of cycles continues to expand slowly with frequency, reaching $20\%$ ($1 - 0.8$) of the number of cycles in the equivalent FFT window at the highest frequency (this achieves higher frequency resolution at higher frequencies while maintaining good temporal resolution).

  *How to reach 3 Hz at the lowest frequency (`'winlen'`)*:

  By default, the lowest-frequency sliding window is about $0.5\text{ seconds}$ long; fitting 3 cycles into $0.5\text{ s}$ sets the lowest analyzed frequency to $6\text{ Hz}$. To lower the minimum analyzed frequency to **$3\text{ Hz}$** with 3 cycles, the window length must be $1\text{ second}$ long—add the optional argument `'winlen', EEG.srate` (or lengthen the epoch range).

  *Significance masking & `padratio`*:

  Enter `0.05` in the *Bootstrap significance level* box and check `FDR correct` to mask non-significant time-frequency pixels using permutation/bootstrap shuffling and False Discovery Rate correction. Increase `'padratio'` (e.g., from default `2` to `4` or `8`) via zero-padding to interpolate and smooth the frequency axis.

* **中文译文与操作解析（专为你的任务态功率研究详解）**：

  在 EEGLAB 中计算任务态时频功率的核心函数是 `pop_newtimef.m`（菜单 `Plot -> Time-frequency transforms -> Channel time-frequency` 或 `Component time-frequency`），它会同时输出两张核心图：

  1. **上半图 ERSP（事件相关谱扰动，单位 dB）**：衡量每个时间点和频率相对于刺激前基线的**总功率变化（包含锁相与非锁相诱发振荡）**。正值（暖色）代表事件相关同步化（ERS，功率增强），负值（冷色）代表事件相关去同步化（ERD，功率下降）。
  2. **下半图 ITC（试次间相干性，取值 0–1）**：衡量不同试次在同一时刻的相位锁定程度。**正如你前面提到的“不强调强锁时性指标”，当你看到某个时频区域 ERSP 显著增强（通过 Bootstrap `alpha = 0.05` + `FDR` 校正），而对应的 ITC 并不显著时，就证明这完全是一个纯粹的非锁相诱发振荡（Induced Oscillation）！**
  3. **小波参数 `[3 0.8]` 的精确含义**：第一个数字 `3` 表示在最低频率处使用 3 个周期的 Morlet/Hanning 小波；第二个数字 `0.8`（当小于 1 时）表示随着频率升高，小波周期数按 $(1 - 0.8) = 20\%$ 的等效 FFT 窗比例递增（等价于高频端时间窗不会缩得太窄，从而兼顾高频的频率分辨率）。如果默认最低频率只到 6 Hz，只需把 Epoch 分段拉长（如 `[-1 2]` 秒）或在附加参数中传入 `'freqs', [3 50]`，函数就会自动采用约 1 秒宽的滑动窗从 3 Hz 开始计算。

```matlab
% 调用 pop_newtimef 计算第 14 号通道 (Cz) 在 3–50 Hz 的任务态 ERSP 功率与 ITC，开启 0.05 Bootstrap 与 FDR 校正
figure;
[ersp, itc, powbase, times, freqs, erspboot, itcboot] = pop_newtimef(EEG, 1, 14, ...
    [EEG.xmin EEG.xmax]*1000, [3 0.8], ...
    'topovec', 14, 'elocs', EEG.chanlocs, 'chaninfo', EEG.chaninfo, ...
    'baseline', [-500 0], 'freqs', [3 50], 'alpha', 0.05, 'mcorrect', 'fdr', ...
    'padratio', 4, 'plotphase', 'off');
```
