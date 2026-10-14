# Step 2: 检查路径并导入数据 (Check the path and import data)

> 所属手册：Makoto's Preprocessing Pipeline 中英对照（由 `Makotos_Preprocessing_Pipeline_CN_EN.md` 按章节拆分）
>
> 章节导航：[00 声明与目录](00_Disclaimer_and_TOC.md) · [Step1](Step01_Double_Precision.md) · [Step2](Step02_Path_Import_icaact_Fix.md) · [Step3](Step03_Downsample.md) · [Step4](Step04_Highpass_1Hz.md) · [Step5](Step05_Channel_Info_EOG.md) · [Step6](Step06_Remove_Bad_Channels.md) · [Step7](Step07_Interpolate_Channels.md) · [Step8](Step08_Average_Reference_FullRank.md) · [Step9](Step09_CleanLine.md) · [Step10](Step10_Epoch_1to2s.md) · [Step11](Step11_Reject_Epochs.md) · [Step12](Step12_Adjust_Rank_ICA.md) · [Step13](Step13_Run_ICA.md) · [Step14-15](Step14-15_Dipole_Fitting.md) · [Step16](Step16_STUDY_No_Double_Dipping.md) · [Step17](Step17_Notes_ASR_ICLabel_SIFT.md) · [附录脚本](Appendix_Full_Batch_Script.md)

## 2.1 路径与命名规范 (Path and Naming Rules)

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

## 2.2 修复 `EEG.icaact` 为空的常见 Bug (`EEG.icaact` is empty!?)

* **English Original**:

  This problem is caused by missing `eeg_options.m` that was supposed to be created properly when you first launched EEGLAB. To diagnose the problem, try `which -all eeg_options`. Usually, you have to find two of them, one under `adminfunc` (read-only archetype), and the other under `userpath`. If EEGLAB cannot access `eeg_options.m`, `'precompute ICA activations...'` is unselected, hence `EEG.icaact` is NEVER calculated by `eeg_checkset()`. To fix this, go into `functions/sigprocfunc/icadefs.m` and manually set `EEGOPTION_PATH = userpath;`, or checkmark `'Precompute ICA activations'` in `File -> Preferences`.

* **中文译文与原理解析**：

  如果你运行完 ICA 保存数据后发现 `EEG.icaact`（ICA 成分时间序列）总是变成空矩阵 `[]`，通常有两个原因：一是 EEGLAB 未能在你的 MATLAB `userpath` 下正常生成可写的 `eeg_options.m` 配置文件（可在命令行运行 `which -all eeg_options` 检查是否同时存在 `adminfunc` 模板文件和 `userpath` 配置文件）；二是在 `File -> Preferences` 中未勾选 `'Precompute ICA activations'`。也可手动计算恢复：

```
% 手动计算恢复 ICA 激活时间序列矩阵 EEG.icaact
EEG.icaact = (EEG.icaweights * EEG.icasphere) * EEG.data(EEG.icachansind, :);
```
