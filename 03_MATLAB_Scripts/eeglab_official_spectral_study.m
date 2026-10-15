%% ========================================================================
%  EEGLAB Official Automated Spectral (Power) Pipeline (Tutorial 11.e)
%  官方标准多被试功率谱全自动预处理与群组统计脚本
%  参考：https://eeglab.org/tutorials/11_Scripting/automated_pipeline.html
%  配套文档：../02_EEGLAB_Official_Tutorials/04_DIPFIT_STUDY_and_ROIconnect.md
% =========================================================================
eeglab;
rng(1); % 固定随机种子以保证 ASR 与 ICA 结果完全可复现
pop_editoptions('option_storedisk', 1); % 内存中仅驻留单个数据集以节省内存

% 1. 从 BIDS 文件夹批量导入多被试数据（也可替换为循环 pop_loadset）
filepath = '/path/to/your/bids_dataset';
[STUDY, ALLEEG] = pop_importbids(filepath, 'studyName', 'Task_Power_Study');

% 2. 移除非脑电辅助通道（如外接肌电 EXG、皮电 GSR、呼吸 Resp 等）
ALLEEG = pop_select(ALLEEG, 'rmchannel', {'EXG1','EXG2','EXG3','EXG4','GSR1','Resp'});

% 3. 第一次全脑平均参考（提升后续 clean_rawdata 识别坏导的准确度）
ALLEEG = pop_reref(ALLEEG, []);

% 4. 使用 clean_rawdata 进行高通滤波 (0.5 Hz)、剔除坏导及 ASR 伪迹清理
ALLEEG = pop_clean_rawdata(ALLEEG, ...
    'FlatlineCriterion', 5, 'ChannelCriterion', 0.87, ...
    'LineNoiseCriterion', 4, 'Highpass', [0.25 0.75], ...
    'BurstCriterion', 20, 'WindowCriterion', 0.25, ...
    'BurstRejection', 'on', 'Distance', 'Euclidian', ...
    'WindowCriterionTolerances', [-Inf 7], 'fusechanrej', 1);

% 5. 剔除坏导后重新计算第二次全脑平均参考（消除坏导对第一次均值的污染）
ALLEEG = pop_reref(ALLEEG, []);

% 6. 运行 Picard (或 runica) ICA，设置 'pca', -1 以匹配平均参考减少的 1 个秩维度
ALLEEG = pop_runica(ALLEEG, 'icatype', 'picard', 'concatcond', 'on', 'options', {'pca', -1});

% 7. 运行 ICLabel 并自动标记概率 > 90% 的肌电 (Muscle) 与眼电 (Eye) 伪迹成分
ALLEEG = pop_iclabel(ALLEEG, 'default');
ALLEEG = pop_icflag(ALLEEG, [NaN NaN; 0.9 1; 0.9 1; NaN NaN; NaN NaN; NaN NaN; NaN NaN]);

% 8. 提取任务态事件分段（例如条件 1 与条件 2，时间窗 -1 至 2 秒）
ALLEEG = pop_epoch(ALLEEG, {'condition_A', 'condition_B'}, [-1 2], 'epochinfo', 'yes');
ALLEEG = eeg_checkset(ALLEEG);

% 9. 创建 STUDY 实验设计矩阵（对比不同任务条件）
STUDY = std_maketrialinfo(STUDY, ALLEEG);
STUDY = std_makedesign(STUDY, ALLEEG, 1, 'name', 'Condition_Contrast', ...
    'delfiles', 'off', 'defaultdesign', 'off', ...
    'variable1', 'type', 'values1', {'condition_A', 'condition_B'}, ...
    'vartype1', 'categorical', 'subjselect', STUDY.subject);

% 10. 在 STUDY 群组层面自动减去伪迹 IC ('rmicacomps','on')、插值坏导 ('interp','on') 并预计算功率谱 ('spec','on')
%     （若需预计算时频功率 ERSP/ITC，可将 'spec','on' 改为 'ersp','on','itc','on'）
[STUDY, ALLEEG] = std_precomp(STUDY, ALLEEG, {}, ...
    'savetrials', 'on', 'rmicacomps', 'on', 'interp', 'on', ...
    'recompute', 'on', 'spec', 'on');

% 11. 绘制 10 Hz Alpha 频段全脑功率地形图与频谱对比曲线
STUDY = pop_specparams(STUDY, 'topofreq', 10);
chanlocs = eeg_mergelocs(ALLEEG.chanlocs);
STUDY = std_specplot(STUDY, ALLEEG, 'channels', {chanlocs.labels}, 'design', 1);
pop_editoptions('option_storedisk', 0);
