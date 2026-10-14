# Chapter 7: 提取数据分段与筛选子集 (Extract Data Epochs)

> 所属手册：EEGLAB 官方教程中英对照（由 `README.md` 按章节拆分）
>
> 章节导航：[00 总览](00_Overview_and_Navigation.md) · [Ch1–4](Ch01-04_Data_Management_Import.md) · [Ch5](Ch05_Preprocess_Data.md) · [Ch6](Ch06_Reject_Artifacts_ASR_ICA.md) · [Ch7](Ch07_Extract_Epochs.md) · [Ch8](Ch08_Spectra_TimeFrequency.md) · [Ch9](Ch09_Source_Analysis_DIPFIT.md) · [Ch10–11](Ch10-11_Group_STUDY_Automated_Pipeline.md) · [ROIconnect](Plugin_ROIconnect_Connectivity.md) · [附录对比](Appendix_Comparison_Official_vs_Makoto.md)

* **English Original** ([Tutorials -\> 7. Extract Data Epochs](https://www.google.com/search?q=https%3A%2F%2Feeglab.org%2Ftutorials%2F07_Extract_epochs%2FExtracting_Data_Epochs.html)):

  Select `Tools -> Extract Epochs` (`pop_epoch.m`), choose the time-locking event type(s), and retain epoch limits such as `[-1 2]` seconds (3 seconds long). **It is often better to extract long data epochs, as here, to make time-frequency decomposition possible at lower (below 10 Hz) frequencies.**

  *Removing baseline values*: After epoching, `Tools -> Remove baseline` (`pop_rmbase.m`) pops up. High-pass filtering is already a form of baseline correction, rendering this step optional. Avoid short baseline windows (on the order of 100 ms) whenever possible.

  *Extracting sub-epochs & Selecting epochs by event info*: Use `Edit -> Select data` (`pop_select.m`) to crop sub-epochs or remove specific trial indices, or `Edit -> Select epochs or events` (`pop_selectevent.m`) to select trials matching specific event metadata fields (making sure `'Remove epochs not referenced by any selected event'` is checked).

* **中文译文与操作解析**：

  在 `Tools -> Extract Epochs`（`pop_epoch.m`）中围绕任务事件分段时，官方特别指出：**为了能够分析 10 Hz 以下（如 Theta、Alpha 频段）的时频功率与相位，应该截取至少 3 秒长（例如 `-1` 到 `2` 秒）的宽时间窗**。若已做过 1 Hz 高通滤波且关注的是频域功率/连接性，时域 `pop_rmbase` 是可选的（若做 ERP 基线校正，应选在 ICA 完成之后，且基线窗口不宜过短）。
