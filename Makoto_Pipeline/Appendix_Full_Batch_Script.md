# 附：可直接运行的完整 MATLAB 批处理脚本模板 (`makoto_batch_pipeline.m`)

> 所属手册：Makoto's Preprocessing Pipeline 中英对照（由 `Makotos_Preprocessing_Pipeline_CN_EN.md` 按章节拆分）
>
> 章节导航：[00 声明与目录](00_Disclaimer_and_TOC.md) · [Step1](Step01_Double_Precision.md) · [Step2](Step02_Path_Import_icaact_Fix.md) · [Step3](Step03_Downsample.md) · [Step4](Step04_Highpass_1Hz.md) · [Step5](Step05_Channel_Info_EOG.md) · [Step6](Step06_Remove_Bad_Channels.md) · [Step7](Step07_Interpolate_Channels.md) · [Step8](Step08_Average_Reference_FullRank.md) · [Step9](Step09_CleanLine.md) · [Step10](Step10_Epoch_1to2s.md) · [Step11](Step11_Reject_Epochs.md) · [Step12](Step12_Adjust_Rank_ICA.md) · [Step13](Step13_Run_ICA.md) · [Step14-15](Step14-15_Dipole_Fitting.md) · [Step16](Step16_STUDY_No_Double_Dipping.md) · [Step17](Step17_Notes_ASR_ICLabel_SIFT.md) · [附录脚本](Appendix_Full_Batch_Script.md)

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
