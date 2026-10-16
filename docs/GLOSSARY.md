# 术语与常见缩写

首次学习按中文概念理解；不同文档、软件中的具体定义仍以相应说明为准。

| 缩写或术语 | 全称 | 本仓库含义 |
|---|---|---|
| EEG | Electroencephalography | 脑电记录；本文主要指头皮记录 |
| EOG | Electrooculography | 眼电记录 |
| ECG | Electrocardiography | 心电记录；有些资料写 EKG |
| EMG | Electromyography | 肌电记录 |
| ADC | Analog-to-Digital Converter | 模数转换器 |
| GUI | Graphical User Interface | 图形用户界面 |
| FIR | Finite Impulse Response | 有限冲激响应滤波器 |
| IIR | Infinite Impulse Response | 无限冲激响应滤波器 |
| FFT | Fast Fourier Transform | 快速傅里叶变换算法 |
| PSD | Power Spectral Density | 功率谱密度 |
| ICA | Independent Component Analysis | 独立成分分析 |
| PCA | Principal Component Analysis | 主成分分析 |
| IC | Independent Component | 独立成分 |
| ASR | Artifact Subspace Reconstruction | 伪迹子空间重构 |
| SSP | Signal Space Projection | 信号空间投影 |
| CSD | Current Source Density | 电流密度；在头皮表面变换语境下解释 |
| ERP | Event-Related Potential | 事件相关电位 |
| ERSP | Event-Related Spectral Perturbation | 事件相关谱扰动 |
| ITC | Inter-Trial Coherence | 试次间相干性；这里指跨试次相位一致性 |
| SNR | Signal-to-Noise Ratio | 信噪比 |
| RV | Residual Variance | 残差方差；使用前说明残差、归一化及计算对象 |
| RMS | Root Mean Square | 均方根 |
| SD | Standard Deviation | 标准差；算法内部尺度不一定等于原始电压的标准差 |
| FDR | False Discovery Rate | 假发现率 |
| SOA | Stimulus Onset Asynchrony | 两刺激起始时刻的间隔 |
| COI | Cone of Influence | 影响锥；具体边缘定义依赖时频方法 |
| MVAR | Multivariate Autoregressive | 多变量自回归模型 |
| GC | Granger Causality | 格兰杰因果；不自动等于实验操纵的因果 |
| SIFT | Source Information Flow Toolbox | 源信息流工具箱 |
| ROI | Region of Interest | 感兴趣区域 |
| LCMV | Linearly Constrained Minimum Variance | 线性约束最小方差波束成形 |
| eLORETA | exact Low-Resolution Electromagnetic Tomography | 精确低分辨率电磁断层成像方法名称 |
| BEM | Boundary Element Method | 边界元方法 |
| MNI | Montreal Neurological Institute | 蒙特利尔神经研究所；常用于模板或坐标命名 |
| MRI | Magnetic Resonance Imaging | 磁共振成像 |
| BIDS | Brain Imaging Data Structure | 脑成像数据结构 |
| RANSAC | Random Sample Consensus | 随机采样一致性算法 |
| MIC | Maximized Imaginary Coherency | 最大化相干虚部 |
| MIM | Multivariate Interaction Measure | 多变量交互测度 |
| TRGC | Time-Reversed Granger Causality | 时间反转格兰杰因果 |
| wPLI | weighted Phase Lag Index | 加权相位滞后指数 |
| iCOH | imaginary Coherency | 相干虚部，具体大小写随软件 |
| FOOOF | Fitting Oscillations & One-Over F | 对周期峰与非周期背景进行参数化的工具名称 |
| AMICA | Adaptive Mixture Independent Component Analysis | 自适应混合独立成分分析 |
| Infomax | Information Maximization | 信息最大化；一种相关优化原则 |
| MATLAB | Matrix Laboratory | 数值计算软件名称 |
| EEGLAB | 工具箱项目专名；EEG全称见首行 | 不将项目名称视作单一算法 |
| ICLabel | 成分分类项目专名；IC全称见上表 | 输出类别概率；不人为补造官方全称 |
| rank | matrix rank | 矩阵秩，线性独立维度的数量 |
| epoch | data epoch | 分段或试次；需说明它对应哪个事件或时间窗 |
| boundary | boundary event | 表示数据不连续的边界事件 |
| baseline | baseline period/value | 比较基准；区分电位均值校正与功率归一化 |

注意：同为“相干”“同步”或“因果”，不同分析对象和定义不能互换。工具包名称也不代表其每种操作都适合当前研究。
