# Step 13: 运行独立成分分析 (Run ICA)

> 所属手册：Makoto's Preprocessing Pipeline 中英对照（由 `Makotos_Preprocessing_Pipeline_CN_EN.md` 按章节拆分）
>
> 章节导航：[00 声明与目录](00_Disclaimer_and_TOC.md) · [Step1](Step01_Double_Precision.md) · [Step2](Step02_Path_Import_icaact_Fix.md) · [Step3](Step03_Downsample.md) · [Step4](Step04_Highpass_1Hz.md) · [Step5](Step05_Channel_Info_EOG.md) · [Step6](Step06_Remove_Bad_Channels.md) · [Step7](Step07_Interpolate_Channels.md) · [Step8](Step08_Average_Reference_FullRank.md) · [Step9](Step09_CleanLine.md) · [Step10](Step10_Epoch_1to2s.md) · [Step11](Step11_Reject_Epochs.md) · [Step12](Step12_Adjust_Rank_ICA.md) · [Step13](Step13_Run_ICA.md) · [Step14-15](Step14-15_Dipole_Fitting.md) · [Step16](Step16_STUDY_No_Double_Dipping.md) · [Step17](Step17_Notes_ASR_ICLabel_SIFT.md) · [附录脚本](Appendix_Full_Batch_Script.md)

## 13.1 最小数据长度、空间平稳性假设与实操准则

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
