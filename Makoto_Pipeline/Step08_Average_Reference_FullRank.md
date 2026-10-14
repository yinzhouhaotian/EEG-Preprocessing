# Step 8: 重参考至全脑平均——为什么必须先补零通道？(Re-reference the data to average)

> 所属手册：Makoto's Preprocessing Pipeline 中英对照（由 `Makotos_Preprocessing_Pipeline_CN_EN.md` 按章节拆分）
>
> 章节导航：[00 声明与目录](00_Disclaimer_and_TOC.md) · [Step1](Step01_Double_Precision.md) · [Step2](Step02_Path_Import_icaact_Fix.md) · [Step3](Step03_Downsample.md) · [Step4](Step04_Highpass_1Hz.md) · [Step5](Step05_Channel_Info_EOG.md) · [Step6](Step06_Remove_Bad_Channels.md) · [Step7](Step07_Interpolate_Channels.md) · [Step8](Step08_Average_Reference_FullRank.md) · [Step9](Step09_CleanLine.md) · [Step10](Step10_Epoch_1to2s.md) · [Step11](Step11_Reject_Epochs.md) · [Step12](Step12_Adjust_Rank_ICA.md) · [Step13](Step13_Run_ICA.md) · [Step14-15](Step14-15_Dipole_Fitting.md) · [Step16](Step16_STUDY_No_Double_Dipping.md) · [Step17](Step17_Notes_ASR_ICLabel_SIFT.md) · [附录脚本](Appendix_Full_Batch_Script.md)

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
