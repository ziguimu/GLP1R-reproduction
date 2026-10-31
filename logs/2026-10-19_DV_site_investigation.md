# DV 位点调查记录：ProteinMPNN 生成结果中的 DV 保留现象

日期：2026-10-19
项目：GLP1R_reproduction
状态：记录已观察证据；原因待讨论；暂不重跑模型

## 1. 调查问题

在复现 GLP-1R 相关论文的 ProteinMPNN 序列设计流程时，
10,000 条候选记录的第 9–10 位全部为 DV。
论文将 DV 列为 NEP-24.11 相关潜在切割位点，因此需要记录
这一现象及其与论文筛选流程之间的差异。

## 2. 已确认的生成结果

- 模型记录：ProteinMPNN `v_48_020`
- 输入结构：基于 PDB 7KI0 的 semaglutide–GLP-1R 复合物
- 设计链：P（肽链）
- 固定链：R（受体）
- 记录的采样温度：T=0.1
- 批次：batch200_seed1 至 batch200_seed50
- 候选记录总数：10,000（每批 200 条，不计每个 FASTA 的参考序列）
- 第 10 位氨基酸分布：V = 10,000
- 第 9–10 位为 DV：10,000 / 10,000（100%）
- 生成序列长度：30 aa

证据来源：
- results/proteinmpnn/test_2000seq_renumbered/batch200_seed1/ 至 batch200_seed50/
- 各批次 seqs/GLP1R_semaglutide_ProteinMPNN_input_renumbered.fa
- logs/2026-10-19_proteinmpnn_generation.md

## 3. 固定位置配置核查

以下两个配置文件均记录肽链 P 的固定位置为：
1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 20, 28。

第 10 位不在所保存的固定位置列表中。

配置文件：
- results/proteinmpnn/fixed_positions.jsonl
- results/proteinmpnn/renumber_check/fixed_positions.jsonl

限制：
原始批次运行命令和完整运行日志尚未找到。因此，现有配置文件
不能单独证明 50 个批次实际使用的就是这些配置。

## 4. 输入结构和序列编号核查

检查过的文件：
- structures/GLP1R_semaglutide_ProteinMPNN_input.pdb
- structures/GLP1R_semaglutide_ProteinMPNN_input_renumbered.pdb
- batch200_seed1 的 FASTA 参考序列

三者的肽链序列均为：

HAEGTFTSDVSSYLEGQAAKEFIAWLVRGR

肽链位置与 PDB 残基编号对应关系：
- 序列位置 9：Asp (D)，PDB 残基编号 15
- 序列位置 10：Val (V)，PDB 残基编号 16

因此，已检查的结构和参考序列在这一段完全一致；
目前没有发现由这两份 PDB 的序列映射差异导致的编号错误。

## 5. 与后续筛选的关系

全量生成记录中，DV 已经存在于全部候选中。
第一轮和第二轮切割位点筛选均没有把 DV 作为淘汰条件。

第二轮结果：
- 输入：787 条
- 保留：308 条
- 淘汰：479 条
- 308 条保留序列均为 30 aa 标准氨基酸序列
- 保留序列均未在指定位置命中 SY、YL、EF、FI、WL
- 308 条序列全部保留第 9–10 位 DV
- 308 条序列互不重复
- 筛选审计表与保留 FASTA 一致

相关文件：
- results/proteinmpnn/test_2000seq_renumbered/screening_step1_cleavage/
- results/proteinmpnn/test_2000seq_renumbered/screening_step2_cleavage/

重要限制：
当前 308 条候选的筛选结果不代表已完整复现论文的 DV 过滤步骤。
如后续需要严格复现论文，应单独核对并记录 DV 过滤方案。

## 6. 当前工作假设与未解决问题

工作假设：
在本次 ProteinMPNN 生成条件下，DV 是一个高度保守的序列特征。
为不影响当前工作进度，暂时保留现有序列结果，继续后续分析。

这不是已证实的生物学规律，也不意味着 DV 已被证明不可设计。

待讨论问题：
1. 为什么 10,000 条候选的第 10 位全部为 V？
2. 在所保存的固定位置列表中，第 10 位并未被指定为固定位置；
   实际运行时的设计掩码是否与保存的配置一致？
3. 这一现象是模型在当前输入结构和采样条件下的偏好，
   还是存在尚未核实的运行参数或其他因素？
4. 论文中 DV 的过滤步骤应如何与本项目现有候选衔接？

目前尚无充分证据确定原因。后续可向蛋白质设计方向的教授或导师请教。

## 7. 后续处理原则

- 不覆盖或删除原始 ProteinMPNN 输出。
- 不因这一现象直接判定模型错误。
- 不把 DV 在当前结果中的 100% 保留解释为已证实的生物学保守性。
- 后续汇报中区分已观察事实、工作假设和未解决问题。
- 如开展严格论文复现，应把 DV 过滤作为单独、可审计的步骤记录。
