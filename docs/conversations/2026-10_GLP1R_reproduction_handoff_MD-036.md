> From: https://chatgpt.com/c/<UUID>

# you asked

message time: 2026-10-19 22:49:14

# GLP1R semaglutide 复现项目交接词

请继续协助我推进 WSL Ubuntu 中的 GLP-1R / semaglutide ProteinMPNN 复现项目。请先完整阅读以下交接信息，再开始工作。

## 一、项目背景与目标

项目目录：

`LOCAL_PATH

当前终端环境：

`(proteinmpnn)`，WSL Ubuntu。

参考论文：

*AI-Driven De Novo Design of Ultra Long-Acting GLP-1 Receptor Agonists*, Advanced Science (2025)，DOI：`10.1002/advs.202507044`

论文全文：\
[https://pmc.ncbi.nlm.nih.gov/articles/PMC12561408/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12561408/)

论文补充材料包含 Table S1：GLP-1RAs sequences for biosynthesis and chemical synthesis。

项目目标是尽可能严谨地复现论文中的候选序列生成、计算初筛和后续评价流程，保留可追溯的输入、参数、脚本、审计表和工作记录，而不是只追求筛出更多候选物。

我希望最终形成一个规范、可审计的科研项目仓库。

## 二、当前项目环境与参考结构

- GPU：NVIDIA RTX 5070 Laptop GPU，8 GB VRAM。
- ProteinMPNN 仓库：`USER_HOME/ProteinMPNN`
- 模型：`v_48_020`
- 参考结构：PDB 7KI0。
- 受体链：R。
- semaglutide 肽链：P。
- 当前用于结构建模的坐标支持序列为 30 aa：

`HAEGTFTSDVSSYLEGQAAKEFIAWLVRGR`

论文表格中的完整生物合成序列为 31 aa：

`HAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG`

末端 Gly 在当前参考结构中没有坐标，因此之前的 ProteinMPNN 输入使用 30 aa。后续必须明确区分 30 aa 坐标支持序列与 31 aa 论文序列，不能混用位置编号。

项目目录中已有 `data/`、`docs/`、`logs/`、`references/`、`results/`、`scripts/`、`structures/` 等目录。开始任何修改前先检查真实文件，不要假定文件一定存在。

## 三、ProteinMPNN 序列生成与现有数据

共生成 10,000 条候选序列，数据位于：

`results/proteinmpnn/test_2000seq_renumbered/`

分 50 个批次，每批 200 条生成序列。每个批次 FASTA 还包含 1 条参考序列，因此每个文件有 201 条记录。

去重结果：

- 原始生成序列：10,000 条
- 去重后唯一序列：1,435 条

主要文件：

- `deduplicated/unique_candidates_all50_v2.fasta`
- `deduplicated/sequence_counts_all50_v2.csv`

此前已完成的酶切位点筛选：

**第一轮**

- 输入 1,435 条
- 保留 787 条
- 剔除 648 条
- 文件：`screening_step1_cleavage/`

**第二轮**

- 输入 787 条
- 保留 308 条
- 剔除 479 条
- 文件：`screening_step2_cleavage/`

第二轮的 308 条已完成基本 QC：

- 长度均为 30 aa
- 无非标准氨基酸
- 序列无重复
- FASTA 与审计表一致

注意：以上是此前实现的筛选流程，并不意味着它已经被证实与论文原始流程完全一致。尤其是酶切位点的处理规则需要重新核对。

## 四、此前调查的 DV 位点问题

当前序列的位置约定为 1-based：

- 第 9 位 D 对应成熟肽 Asp15。
- 第 10 位 V 对应成熟肽 Val16。
- 因此序列位置 9–10 的 DV 对应论文中的 Asp15–Val16。

此前发现：

- 10,000 条 ProteinMPNN 生成序列的第 10 位均为 V。
- 已保存的 fixed-position 配置未将第 10 位列入固定位置。
- 输入 PDB、FASTA 参考序列及位置映射已核对。
- 原始生成命令和实际运行时参数尚未找到，因此实际运行时的设计掩码、固定位置设置等尚未完全确认。

不能据此认定 ProteinMPNN 出错，也不能将 10,000 条均为 V 解释成已证实的生物学保守性。

此前调查记录：

- `logs/2026-10-19_DV_site_investigation.md`
- `logs/2026-10-19_proteinmpnn_generation.md`

当前已经决定暂时停止追查运行时掩码问题，不要反复围绕“为什么 10,000 条都为 V”展开，而是优先从论文实验验证候选物及其筛选规则入手。

## 五、研究方向的关键转折：D13、D41、D44 作为参考锚点

最新从论文 Table S1 核实了三条候选物的准确生物合成序列：

**D13**

`HAEGTFTSDVSSYLEEQAAKAFVERLKRGRG`

**D41**

`HAEGTFTSDVSSYLEEQQVKQFVERLKRGRG`

**D44**

`HAEGTFTSDVSRYLEEKAVKDFVERLKRGAG`

这三条均为 30 aa，与当前坐标支持序列长度一致。

论文报告的主要实验结果：

| 指标        | D13            | D41            | D44           |
| --------- | -------------- | -------------- | ------------- |
| SPR (K_D) | 8.58 × 10⁻⁶ M  | 5.19 × 10⁻⁶ M  | 6.78 × 10⁻⁶ M |
| cAMP 功能   | 阳性             | 阳性             | 阳性            |
| PK 半衰期    | 19.86 ± 1.55 h | 23.16 ± 3.69 h | 4.19 ± 0.37 h |
| 小鼠 PD     | 已开展            | 已开展            | 已开展           |

论文还报告了 DIO 肥胖小鼠中的体重下降结果：

- D13：约 19.25%
- D41：约 14.42%
- D44：约 16.46%
- semaglutide 对照：约 21.54%

三者都经过多阶段实验验证，但不能据此断言它们在所有指标上表现相同。D13、D41 的半衰期较长；D44 的半衰期短于文中比较的 semaglutide。也不能将它们称为全部 10,000 条设计中经全面实验比较后排名前三的候选物。

**重要：后续请以以上 Table S1 序列为准确参考，不要使用之前对话中未经核实的序列版本。**

## 六、DV 问题出现了新的重要证据

将三条参考序列与 semaglutide 对齐：

| 位点        | D13 | D41 | D44 |
| --------- | --- | --- | --- |
| 第 9–10 位  | DV  | DV  | DR  |
| 第 12–13 位 | SY  | SY  | RY  |
| 第 13–14 位 | YL  | YL  | YL  |
| 第 21–22 位 | EQ  | QQ  | KD  |
| 第 25–26 位 | RL  | RL  | RL  |

注意，上表为直接从序列读取的局部序列信息；若讨论 NEP-24.11 切割位点，必须严格区分“成熟肽编号”“当前 30 aa 序列编号”和实际筛选脚本使用的位置编号。

最重要的发现：

**D13、D41 保留 DV，但 D44 的第 10 位是 R，因此 D44 不保留 DV。**

D44 仍然是论文中具有 cAMP 功能活性、开展 PK 和小鼠 PD 研究的候选物。

因此：

- DV 不是这三条实验验证候选物共同具备的必要序列特征。
- 这足以促使我们重新核查 DV 的处理规则。
- 但不能据此直接断言论文从未过滤 DV，也不能认定 D44 生成时该位点一定没有受到任何设计约束。
- 还需核实论文的具体设计约束、过滤顺序、酶切位点规则及实验序列编号。

这次发现促使项目发生方法上的转折：不再将 DV 当成未经验证的固定规则，而是尝试从实验验证候选物出发，结合论文方法反推计算筛选流程。

## 七、下一阶段的核心任务

**目标：以 D13、D41、D44 为参考锚点，从 1,435 条去重序列重新开展可审计的初筛。**

建议依次完成：

1. 检查项目现有的论文、补充材料、工作记录和筛选脚本。
2. 将 D13、D41、D44 的准确序列与 semaglutide 进行逐位对齐，统一位置编号。
3. 从论文正文及补充材料中核实酶切位点、净电荷、疏水性、SAP、结构约束、稳定性及序列多样性等指标的原文描述。
4. 区分论文明确写出的筛选规则、论文报告但无法完整复现的指标，以及我们自行提出的假设。
5. 比较三条参考序列的共同特征与差异，分析哪些指标可能具有区分价值。
6. 在保留旧结果的基础上，建立新的独立初筛版本，输入为 1,435 条去重序列。
7. 每一步记录输入数、保留数、剔除数、具体规则、参数来源和审计结果。
8. 重新审视 DV、SY、YL、EF、FI、WL 的处理逻辑，不要在核实论文规则前预先设定它们必须保留或必须删除。
9. 如果论文没有提供明确阈值，不要凭三条候选序列虚构阈值；可以把它们用于探索性比较，但必须标明假设性质。
10. 最终形成与论文原始流程一致程度明确、可追溯的复现流程，而不是仅仅得到一个数量更少的候选集。

## 八、项目已有记录和材料

请先检查这些文件是否存在，再决定如何使用：

- `docs/README.md`
- `logs/2026-10-19_proteinmpnn_generation.md`
- `logs/2026-10-19_DV_site_investigation.md`
- `logs/2026-10-19_interface_analysis.md`
- `results/proteinmpnn/test_2000seq_renumbered/physicochemical_screening/`
- `results/proteinmpnn/test_2000seq_renumbered/helix_constraint_screening/`
- `results/proteinmpnn/test_2000seq_renumbered/screening_step1_cleavage/`
- `results/proteinmpnn/test_2000seq_renumbered/screening_step2_cleavage/`

此前已有净电荷、Kyte–Doolittle 疏水性、简单序列聚集倾向、近似螺旋特征、Hamming 距离和聚类分析等结果。这些属于已有探索性分析，不能自动视为论文的正式筛选标准。

此前发现一些复现材料不完整：

- 原始 ProteinMPNN 生成命令及完整运行时参数尚未找到。
- 部分去重和第一轮筛选的原始执行脚本尚未定位。
- 需要在适当时机将这些问题记录为可复现性缺口，而不是伪造缺失脚本或命令。

## 九、补充材料下载情况

项目内存在：

`references/advs71185-sup-0002-DataFile.zip`

但它当前是 **0 字节空文件**，不能当作有效补充数据包使用。不要删除或覆盖它；如需重新下载，请另存为新文件。

论文 Table S1 的内容已由我在当前对话中直接提供并核实了 D13、D41、D44 的序列，但完整补充材料包是否成功获取仍未解决。

## 十、协作方式与重要约束

请严格遵循以下工作方式：

1. 使用中文交流。
2. 采取逐步推进方式，一次先给一条或少量终端命令，等我运行并发回输出后再继续。
3. 先检查实际文件，再做分析；不要猜测本地文件内容。
4. 默认只读检查。任何修改、生成新脚本或工作记录前，说明会创建什么文件以及是否会影响旧文件。
5. 不覆盖或删除已有科研材料、原始数据和历史结果。
6. 若需要重新筛选，建立独立版本目录，不直接替换旧筛选结果。
7. 区分事实、假设、待验证问题和论文原文结论。
8. 不把三条参考序列当成足以唯一反推全部筛选阈值的样本。
9. 不把计算筛选结果描述为已验证的生物学功能。
10. 代码修改时，优先提供完整脚本，而不是只给差异片段。
11. 如果涉及论文方法、数值或实验阶段，优先核对原文和补充材料，不要只依赖之前对话的概述。
12. 目前的首要工作不是继续生成序列，也不是继续单独追查 ProteinMPNN 的 DV 现象，而是以 D13、D41、D44 为锚点，核实论文筛选规则，并从 1,435 条去重序列重新开展初筛。

**请从检查项目中现有的工作记录、补充材料和筛选脚本开始，然后给出下一条具体操作命令。不要直接跳到重跑筛选。**

---

# chatgpt response

我已经按这份交接词接上项目进度。我们先不重跑筛选，也不继续追查 ProteinMPNN 的 DV 现象，而是先盘点现有材料，确认哪些论文方法、筛选规则和历史结果能够被实际文件支持。

接下来严格遵守：**只读检查 → 核对论文规则 → 设计独立初筛版本 → 再决定是否运行。** 旧结果全部保留，缺失的脚本和参数不会凭空补造。

## 第一步：检查现有工作记录、补充材料和筛选脚本

请在 WSL Ubuntu 的终端中执行下面这条命令。它只读取文件系统信息，不会修改或删除文件。

\n' 2>/dev/null | sort
}
</CodeBlock>

### 我们要从输出中确认什么？

1. **工作记录是否完整**：尤其是生成参数、DV 位点调查和此前的筛选方法。
2. **补充材料是否有效**：确认 ZIP 的实际大小与文件类型，不会因为文件名存在就认定下载成功。
3. **旧筛选结果是否可追溯**：检查每轮筛选的输出、审计表和相关文件。
4. **脚本是否真实存在**：定位可用的筛选代码，同时记录尚未找到的原始执行脚本。

这一步暂时不读取或修改任何候选序列，也不对 D13、D41、D44 设定新的筛选阈值。

**请运行后，把完整终端输出发给我。** 我会根据实际结果确定下一步优先阅读哪些文件，而不是提前假定项目中的材料已经齐全。

---

# you asked

message time: 2026-10-19 22:51:28

===== KEY DOCUMENTS AND LOGS =====
-rwxrwxrwx 1 ziguimu ziguimu 3.5K Oct 19 21:27 docs/README.md
docs/README.md: Unicode text, UTF-8 text
-rwxrwxrwx 1 ziguimu ziguimu 3.0K Oct 19 19:20 logs/2026-10-19_proteinmpnn_generation.md
logs/2026-10-19_proteinmpnn_generation.md: Unicode text, UTF-8 text
-rwxrwxrwx 1 ziguimu ziguimu 4.2K Oct 19 21:25 logs/2026-10-19_DV_site_investigation.md
logs/2026-10-19_DV_site_investigation.md: Unicode text, UTF-8 text
-rwxrwxrwx 1 ziguimu ziguimu 7.4K Oct 19 13:13 logs/2026-10-19_interface_analysis.md
logs/2026-10-19_interface_analysis.md: Unicode text, UTF-8 text, with very long lines (402)
-rwxrwxrwx 1 ziguimu ziguimu 0 Oct 19 13:19 references/advs71185-sup-0002-DataFile.zip
references/advs71185-sup-0002-DataFile.zip: empty

===== SCREENING DIRECTORIES =====
--- results/proteinmpnn/test_2000seq_renumbered/physicochemical_screening
results/proteinmpnn/test_2000seq_renumbered/physicochemical_screening/aggregation_sequence_audit.csv (68771 bytes)
results/proteinmpnn/test_2000seq_renumbered/physicochemical_screening/hydrophobicity_KD.csv (42804 bytes)
results/proteinmpnn/test_2000seq_renumbered/physicochemical_screening/net_charge_pH7.4.csv (56409 bytes)
--- results/proteinmpnn/test_2000seq_renumbered/helix_constraint_screening
results/proteinmpnn/test_2000seq_renumbered/helix_constraint_screening/analyze_helix_sequence_features.py (2973 bytes)
results/proteinmpnn/test_2000seq_renumbered/helix_constraint_screening/pro_gly_reference_helix_audit.csv (82365 bytes)
--- results/proteinmpnn/test_2000seq_renumbered/screening_step1_cleavage
results/proteinmpnn/test_2000seq_renumbered/screening_step1_cleavage/rejected_step1.fasta (28512 bytes)
results/proteinmpnn/test_2000seq_renumbered/screening_step1_cleavage/retained_step1.fasta (34628 bytes)
results/proteinmpnn/test_2000seq_renumbered/screening_step1_cleavage/screening_step1_audit.csv (284464 bytes)
--- results/proteinmpnn/test_2000seq_renumbered/screening_step2_cleavage
results/proteinmpnn/test_2000seq_renumbered/screening_step2_cleavage/rejected_step2.fasta (21076 bytes)
results/proteinmpnn/test_2000seq_renumbered/screening_step2_cleavage/retained_step2.fasta (13552 bytes)
results/proteinmpnn/test_2000seq_renumbered/screening_step2_cleavage/screen_cleavage_step2.py (3102 bytes)
results/proteinmpnn/test_2000seq_renumbered/screening_step2_cleavage/screening_step2_audit.csv (91405 bytes)

===== SCRIPT FILES =====
results/proteinmpnn/test_2000seq_renumbered/clustering_complete_linkage_d3/cluster_complete_linkage.py (11063 bytes)
results/proteinmpnn/test_2000seq_renumbered/helix_constraint_screening/analyze_helix_sequence_features.py (2973 bytes)
results/proteinmpnn/test_2000seq_renumbered/screening_step2_cleavage/screen_cleavage_step2.py (3102 bytes)
scripts/analyze_glp1r_interface.py (9088 bytes)
scripts/analyze_interface_atom_pairs.py (5872 bytes)
scripts/check_7ki0.py (534 bytes)
scripts/check_7ki0_residue_details.py (900 bytes)
scripts/export_7ki0_sequences.py (884 bytes)
scripts/export_glp1r_residue_mapping.py (2097 bytes)
scripts/extract_7ki0_chains.py (873 bytes)
scripts/inspect_7ki0_structure.py (444 bytes)
scripts/make_semaglutide_peptide_only.py (1107 bytes)
scripts/map_7ki0_entities.py (720 bytes)
scripts/map_glp1r_pdb_to_fasta.py (2348 bytes)
scripts/prepare_proteinmpnn_complex.py (2467 bytes)
scripts/summarize_glp1r_structure.py (676 bytes)
scripts/validate_extracted_pdbs.py (875 bytes)
scripts/validate_semaglutide_sequence.py (840 bytes)
(proteinmpnn) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH

---

# chatgpt response

第一轮检查结果已经明确了几个重要事实。

## 现有材料盘点

| 项目 | 当前状态 |
|---|---|
| `docs/README.md` | 存在，约 3.5 KB |
| ProteinMPNN 生成记录 | 存在，约 3.0 KB |
| DV 位点调查记录 | 存在，约 4.2 KB |
| 界面分析记录 | 存在，约 7.4 KB |
| 补充材料 ZIP | **0 字节，当前不可用** |
| 理化性质分析 | 已有净电荷、疏水性、序列聚集倾向 CSV |
| 螺旋特征分析 | 已有分析脚本及审计 CSV |
| 第一轮酶切筛选 | 有保留序列、剔除序列和审计表 |
| 第二轮酶切筛选 | 有完整的保留/剔除文件、审计表及一个筛选脚本 |

还发现一个值得注意的可复现性缺口：目前定位到的筛选脚本只有第二轮 `screen_cleavage_step2.py`，第一轮尚未找到对应脚本；生成记录是否保存了足够的运行参数，还需要阅读正文才能判断。

**现在不要运行任何筛选脚本。** 下一步应先阅读已有记录，确认历史筛选的真实规则和证据来源，避免在不了解旧流程的情况下重复实现。

## 第二步：读取四份核心工作记录

请继续在同一个项目目录中执行下面这条命令。它只会显示现有文档内容，不会更改文件。

<CodeBlock "$f"
  done
}
</CodeBlock>

我会重点核对：

- 生成时记录的模型、参数和仍然缺失的信息。
- 之前两轮酶切筛选采用的规则、位置编号和依据。
- 已有理化性质与结构分析究竟是探索性结果还是论文明确规定的方法。
- 哪些问题已经核实，哪些仍需要回到论文正文或补充材料确认。

收到输出后，我们再决定下一步是检查第二轮筛选脚本，还是先从论文方法部分提取正式规则。不会提前重跑筛选，也不会用 D13、D41、D44 三条序列反向编造阈值。

---

# you asked

message time: 2026-10-19 22:52:08

(proteinmpnn) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH
cd LOCAL_PATH && {
  for f in \
    docs/README.md \
    logs/2026-10-19_proteinmpnn_generation.md \
    logs/2026-10-19_DV_site_investigation.md \
    logs/2026-10-19_interface_analysis.md
  do
    echo
    echo "========== $f =========="
    cat "$f"
  done
}

========== docs/README.md ==========
# GLP-1R Semaglutide ProteinMPNN Reproduction

## 1. Project purpose

This project reproduces and audits the sequence-design and candidate-screening stages associated with the paper:

*AI-Driven De Novo Design of Ultra Long-Acting GLP-1 Receptor Agonists*
Advanced Science (2025). DOI: [10.1002/advs.202507044](https://doi.org/10.1002/advs.202507044)

The project records the structures, ProteinMPNN sequence-generation outputs, screening procedures, and intermediate results. Reproduction status and deviations from the published workflow should be documented explicitly.

## 2. Current workflow and verified counts

| Stage | Records | Status |
|---|---:|---|
| ProteinMPNN-generated candidates | 10,000 | Generated across 50 batches |
| Unique sequences after deduplication | 1,435 | Count and total records checked |
| First cleavage-site screening | 787 retained | 648 rejected |
| Second cleavage-site screening | 308 retained | 479 rejected |
| Final retained sequence set | 308 | Length, residue alphabet, uniqueness, and audit-table consistency checked |

These counts describe the current local workflow. They do not, by themselves, establish equivalence to every step of the published paper.

## 3. Important unresolved issue: DV at positions 9–10

All 10,000 generated candidates have valine (V) at sequence position 10, so the DV motif at positions 9–10 is present in all candidates.

The saved fixed-position configuration does not list position 10 as fixed. However, the original generation command and complete runtime configuration have not been recovered, so the actual runtime design mask has not been independently verified.

This observation is unresolved. It must not be presented as proof that DV is biologically conserved or that ProteinMPNN is malfunctioning. The current screening workflow allowed DV; strict reproduction of the paper's cleavage-site filtering requires separate review.

See `../logs/2026-10-19_DV_site_investigation.md` for the investigation record.

## 4. Directory guide

- `data/`: input data and derived data, as present in the project.
- `docs/`: project overview and methodological documentation.
- `logs/`: dated run records, investigation notes, and analysis records.
- `references/`: literature and reference materials.
- `results/`: generated outputs, screening results, and analyses.
- `scripts/`: scripts used for processing and analysis.
- `structures/`: structural input files.

Directory descriptions indicate intended roles; they do not imply that every directory currently contains files.

## 5. Key records

- `../logs/2026-10-19_proteinmpnn_generation.md`: ProteinMPNN generation record.
- `../logs/2026-10-19_DV_site_investigation.md`: DV-site investigation and unresolved questions.
- `../logs/2026-10-19_interface_analysis.md`: interface-analysis record.

The backup file `2026-10-19_interface_analysis.md.bak-20261019-131326` is retained as-is and is not treated as the current primary record.

## 6. Reproducibility principles

1. Preserve original generation outputs and source files.
2. Keep screening scripts, audit tables, and retained/rejected sequence sets traceable to one another.
3. Distinguish directly verified observations from working hypotheses and unresolved questions.
4. Record deviations from the published procedure rather than silently treating them as equivalent.
5. Do not claim biological activity, receptor agonism, binding affinity, or in-vivo performance from sequence generation and computational screening alone.

========== logs/2026-10-19_proteinmpnn_generation.md ==========
# GLP-1R ProteinMPNN Sequence Generation Record

Date: 2026-10-19
Project: GLP1R_reproduction
Stage: ProteinMPNN candidate sequence generation and validation

## 1. Input and design setup

- Reference complex: semaglutide-bound GLP-1R structure derived from PDB 7KI0.
- ProteinMPNN-compatible input: `GLP1R_semaglutide_ProteinMPNN_input_renumbered.pdb`.
- Model: `v_48_020`.
- Designed chain: P (peptide); fixed chain: R (receptor).
- Candidate peptide length in the generated FASTA files: 30 amino acids.
- Fixed peptide positions checked: 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 20, 28.
- All checked candidates matched the expected amino acids at these fixed positions.
- Full runtime parameters have not yet been independently verified from a preserved run command or log.

## 2. Generation and deduplication

- Batch folders inspected: `batch200_seed1` through `batch200_seed50`.
- Candidate records: 200 per batch, 10,000 total, excluding the first reference record in each FASTA.
- Unique sequences across all batches: 1,435.
- Duplicate excess records: 8,565 (85.65% of all candidate records).
- Per-batch unique sequence count: 104–130 out of 200.
- The original FASTA outputs and earlier deduplicated files were preserved.

## 3. Deduplicated outputs

- `results/proteinmpnn/test_2000seq_renumbered/deduplicated/unique_candidates_all50_v2.fasta`
- `results/proteinmpnn/test_2000seq_renumbered/deduplicated/sequence_counts_all50_v2.csv`

Validation of the deduplicated outputs:
- FASTA sequence count: 1,435.
- CSV row count: 1,435.
- Sum of CSV `count` values: 10,000.
- FASTA/CSV unique sequence consistency: passed.
- Fixed-position validation: passed.

## 4. Interpretation and limitations

- The generated sequences and their frequencies describe ProteinMPNN sampling output only.
- Repeated sequences indicate sampling concentration; they do not establish binding, receptor activation, potency, stability, or pharmacological activity.
- The high-frequency sequence patterns merit further analysis, but the cause of the observed distribution has not been established.
- The peptide structure contains 30 coordinate-supported residues, while the full polymer sequence contains 31 positions; these outputs remain 30 residues long. No missing residue was appended during deduplication.
- This record documents computational sequence generation and validation, not experimental validation.

## 5. Run metadata cross-check

- Checked FASTA headers for all 50 batch outputs.
- All 50 headers matched their expected seed number.
- All 50 headers reported model `v_48_020`, fixed chain `R`, and designed chain `P`.
- Candidate records show the sampling temperature marker `T=0.1`.
- The model identifier recorded in the FASTA header is `8907e6671bfbfc92303b5f79c4b5e6ce47cdef57`.
- This check validates output metadata, not every runtime argument. The original batch command or run script was not found; consistency of all parameters such as `num_seq_per_target` and `batch_size` remains unverified.

========== logs/2026-10-19_DV_site_investigation.md ==========
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

========== logs/2026-10-19_interface_analysis.md ==========
# GLP-1R Reference Interface Analysis

Date: 2026-10-19
Project: GLP1R_reproduction
Stage: Semaglutide-bound reference structure and interface analysis

## 1. Reference structure

- Structure: PDB 7KI0
- Receptor chain used: author chain R
- Peptide chain used: author chain P
- Peptide: semaglutide
- Receptor chain contains 384 observed standard residues.
- Receptor residue mapping: 384/384 observed residues mapped to the receptor FASTA.
- Peptide coordinate model contains 30 residues; the full polymer sequence contains 31 positions. The final Gly is present in the sequence record but has no coordinates in the extracted peptide structure.

## 2. Generated analysis files

- `results/GLP1R_7KI0_residue_mapping.csv`
- `results/GLP1R_semaglutide_contacts_4A.csv`
- `results/GLP1R_semaglutide_contacts_5A.csv`
- `results/GLP1R_semaglutide_peptide_summary_4A.csv`
- `results/GLP1R_semaglutide_peptide_summary_5A.csv`
- `results/GLP1R_semaglutide_nearest_atom_pairs_4A.csv`

Analysis scripts include:
- `scripts/analyze_glp1r_interface.py`
- `scripts/analyze_interface_atom_pairs.py`

## 3. Heavy-atom contact analysis

Using heavy-atom distance cutoffs:

- 4 Å: 196 heavy-atom pairs, 60 unique peptide–receptor residue pairs.
- 5 Å: 832 heavy-atom pairs, 108 unique peptide–receptor residue pairs.
- At 4 Å, 24 peptide residues and 40 receptor residues participate in contacts.

These are geometric contact counts, not binding-energy estimates or experimental activity measurements.

## 4. Example interface observations

Selected peptide positions and nearby receptor FASTA positions:

- Peptide position 1 (His): receptor positions 243, 246, 315, 318, 319 and 322.
- Peptide position 3 (Glu): receptor positions 161, 199, 397 and 400.
- Peptide position 6 (Phe): receptor positions 150, 153 and 157, among others.
- Peptide position 15 (Glu): receptor positions 39, 40, 41 and 308.
- Peptide position 23 (Ile): receptor positions 97–100.

Selected minimum heavy-atom distances:

- Peptide Glu position 3 OE1 – receptor Arg FASTA position 199 NH2: 2.691 Å.
- Peptide Glu position 15 OE1 – receptor Arg FASTA position 308 NE: 2.870 Å.
- Peptide Glu position 3 OE2 – receptor Tyr FASTA position 161 OH: 2.580 Å.
- Peptide Glu position 15 OE2 – receptor Ser FASTA position 40 OG: 3.031 Å.

These close contacts are candidates for further chemical-geometry inspection. Distance alone does not establish a hydrogen bond or salt bridge.

## 5. Current limitations

- Neither extracted structure contains explicit hydrogen atoms.
- Hydrogen-bond angles have not been evaluated.
- No binding free energy, experimental affinity, or agonist activity was calculated in this stage.
- Structural proximity does not prove that a residue is functionally essential.
- Peptide residue numbering in the PDB differs from peptide sequence position. For the analyzed peptide, sequence position = PDB author residue number - 6.
- Receptor positions reported as FASTA positions are mapped separately from receptor PDB residue numbers.

## 6. Interpretation

This stage establishes a reproducible geometric description of the semaglutide–GLP-1R reference interface. It provides a structural reference for later candidate design and comparison, but it does not by itself validate a new peptide's binding affinity or agonist function.

## 7. Next step

Review the reference interface and analysis scripts, then define a cautious candidate-comparison protocol before starting new sequence design. Preserve the distinction between structural plausibility and experimentally established agonism.

## 8. Input-file consistency check (2026-10-19)

Compared the two extracted peptide-chain files:

- `structures/semaglutide_7KI0_chainP.pdb`: 31 residue records, 256 atoms; includes `AIB` and `WF1`.
- `structures/semaglutide_peptide_only_7KI0.pdb`: 30 residue records, 236 atoms; includes `AIB` and excludes `WF1`.

The difference in residue and atom counts is consistent with the explicit `WF1` exclusion in `scripts/make_semaglutide_peptide_only.py`.

`scripts/analyze_glp1r_interface.py` explicitly uses:
- `structures/semaglutide_peptide_only_7KI0.pdb`
- `structures/GLP1R_7KI0_chainR.pdb`

The interface analysis was rerun successfully using these configured paths. The shared atoms' coordinates across the two peptide files have not yet been compared atom by atom. The two files should not be treated as interchangeable without further validation.

## 9. Shared-atom coordinate comparison (2026-10-19)

Compared atom identities using residue identifier, residue name, atom name, and element.

- Original chain-P file: 256 atoms.
- Peptide-only analysis file: 236 atoms.
- Shared atom keys: 236.
- Atoms only in the original file: 20.
- Atoms only in the peptide-only file: 0.
- Maximum coordinate difference among shared atoms: 0.000000 Å.
- Shared atoms differing by more than 0.001 Å: 0.

This confirms that all 236 atoms retained in the peptide-only file have matching coordinates in the original chain-P file. The 20 additional atoms in the original file are consistent with the previously identified `WF1` residue. This is a file-consistency check, not an independent validation of the biological interpretation of the reference structure.

## 10. Receptor residue mapping validation (2026-10-19)

Inspected `results/GLP1R_7KI0_residue_mapping.csv`.

- Total mapping records: 384.
- Exact amino-acid matches: 384.
- Amino-acid mismatches: 0.
- PDB residue-number range: 29–423.
- Receptor construct FASTA-position range: 38–432.

All records in the mapping table have matching amino-acid identities at the mapped positions. PDB residue numbering and construct FASTA numbering must remain distinct. The mapping should be used directly rather than assuming a constant numerical offset. This validation applies only to positions represented in the mapping table and does not establish complete coverage of the native receptor sequence.

## 11. Reference interface coverage at a 4 Å cutoff (2026-10-19)

Inspected `results/GLP1R_semaglutide_contacts_4A.csv`.

- Contact records: 60.
- Distinct peptide residues involved: 24.
- Distinct receptor PDB residues involved: 40.
- Distinct receptor construct FASTA positions involved: 40.
- Records with non-exact receptor mapping: 0.

The contact table records peptide–receptor residue pairs with heavy-atom contacts within the 4.0 Å cutoff. These records are geometric descriptors, not counts of hydrogen bonds, binding-energy contributions, or experimentally verified functional interactions.

The receptor FASTA positions represented in the table are:
39, 40, 41, 44, 48, 77, 78, 97, 98, 99, 100, 130, 132, 147, 150, 153, 157, 161, 199, 206, 210, 214, 219, 223, 239, 243, 246, 307, 308, 309, 315, 318, 319, 322, 381, 389, 393, 396, 397, 400.

## 12. Candidate-input inventory (2026-10-19)

Inspected project files to a maximum depth of four, excluding Git internals, the reference mmCIF file, and the results directory.

The inspected project currently contains:
- The 7KI0 reference structure and extracted receptor/peptide PDB files.
- Receptor and semaglutide FASTA files.
- Reference-interface analysis scripts and result tables.
- The existing interface-analysis log.

No candidate peptide sequence files or candidate predicted structures were found in the inspected file inventory.

This is an inventory of the inspected project directory, not proof that no candidate materials exist elsewhere on the computer or in external storage. Candidate comparison and ranking have n

---

# chatgpt response

读完这四份记录后，当前最重要的结论是：**我们已经知道旧流程做了什么，但还没有充分证据证明这些筛选规则来自论文原文。**

有三个具体问题需要继续核查：

1. 生成记录确认了模型版本、采样温度和设计链，但原始运行命令及完整参数仍未找到。
2. DV 调查记录说明两轮旧筛选都没有淘汰 DV；这只是现有流程的行为，不能直接当作论文规则。
3. 第二轮筛选脚本已经找到，第一轮脚本尚未定位。我们应先检查第二轮的实际实现和审计表，明确旧规则到底如何执行。

## 下一步：只读检查第二轮筛选脚本与审计表

请运行以下命令。它不会运行筛选程序，也不会修改任何文件。

eening_step1_audit.csv
}
</CodeBlock>

收到输出后，我会先判断：

- 两轮筛选各自检查哪些序列位置和切割基序；
- 审计表是否记录了每条序列的具体淘汰原因；
- 第二轮规则是否能追溯到明确的论文依据；
- 下一步应先核查论文方法，还是继续调查旧筛选结果的实现细节。

我们暂时不改动 308 条旧结果，也不把任何未经论文证实的规则直接用于新的 1,435 条序列。

---

# you asked

message time: 2026-10-19 22:53:09

要不要我把工作记录给你看看

---

# chatgpt response

**要，而且我建议先看工作记录，再看筛选脚本。** 这样能避免只看代码，却不知道当时为什么采用这些规则。

你刚才已经给我看了四份核心记录。接下来最值得看的，是能够帮助我们追溯筛选规则来源的记录。

建议按这个顺序：

1. **论文筛选方法相关的工作记录**：有没有摘录论文正文、补充材料中关于 NEP-24.11、酶切位点、净电荷、疏水性、SAP 等指标的原文。
2. **此前筛选过程的记录**：为什么设置两轮筛选、各轮采用什么规则、阈值从哪里来。
3. **D13、D41、D44 的序列核对记录**：确认参考序列的来源、位置编号和与 semaglutide 的比较方式。
4. **其他相关记录**：特别是记录了待解决问题、曾经修改过的规则或尚未验证的假设的文件。

## 现在先做一件小事

请在项目目录下运行这条只读命令，列出全部 Markdown 工作记录：

s)\n' 2>/dev/null | sort
</CodeBlock>

把输出发给我，我来判断**哪些记录最值得优先阅读**，再一次看一两份，不用你把所有材料一次性贴过来。

我们的核心原则不变：区分论文明确规定的规则、已有工作实际采用的规则，以及我们为了探索数据而提出的假设。尤其不能因为 D13、D41、D44 是实验验证过的候选物，就反过来为三条序列量身定制筛选阈值。

---

# you asked

message time: 2026-10-19 22:53:52

# GLP-1R 从头肽设计项目工作记录

## 阶段一：参考序列与结构准备

**项目名称：** GLP-1R 计算设计与候选肽评估  
**阶段名称：** 参考序列与结构准备（序列处理阶段）  
**阶段状态：** 基础数据准备已完成；进入结合界面分析前的检查阶段  
**工作环境：** WSL Ubuntu 22.04.5  
**项目根目录：** `LOCAL_PATH

---

### 一、阶段目标

建立后续 GLP-1R 候选肽设计与结构评估所需的基础数据，包括：

1. 建立独立的项目目录，避免与已有 EGFR、TNF-α、GPD 等项目混杂。
2. 获取 GLP-1R 与 Semaglutide 的实验复合物参考结构。
3. 提取肽链与受体链的结构文件及对应序列。
4. 核对结构中实际存在的残基，并识别非标准残基和修饰基团。
5. 建立受体 PDB 残基编号与构建体 FASTA 序列位置的对应关系。
6. 为后续结合界面分析和 ProteinMPNN 序列设计建立可追溯的数据基础。

### 二、项目目录与运行环境

建立项目目录：

`LOCAL_PATH

当前主要子目录：

- `data/`：序列和基础数据
- `docs/`：文档记录
- `logs/`：运行日志
- `results/`：分析结果
- `scripts/`：分析与数据处理脚本
- `structures/`：结构文件

检查了已有计算环境，确认可以使用 BioPython 处理结构文件，并确认 ProteinMPNN 环境能够导入相关结构处理模块。

本阶段尚未执行 ProteinMPNN 序列生成或 AlphaFold/ColabFold 候选结构预测。

### 三、参考结构获取与链识别

从 RCSB PDB 获取实验结构：

- **PDB ID：** 7KI0
- **文件：** `structures/7KI0.cif`
- **参考对象：** Semaglutide 与 GLP-1R 形成的复合物结构
- **实验方法：** 冷冻电镜
- **报告分辨率：** 2.50 Å

通过结构链信息检查，识别出：

- 链 P：Semaglutide 肽链所在链
- 链 R：GLP-1R 受体所在链

本阶段的结构处理聚焦于链 P 和链 R，没有把整个复合物中的所有链都作为后续肽链设计输入。

### 四、序列提取与结构文件生成

生成或检查了以下文件：

**序列文件**

- `data/semaglutide_7KI0_chainP.fasta`
- `data/GLP1R_7KI0_chainR.fasta`

**结构文件**

- `structures/semaglutide_7KI0_chainP.pdb`
- `structures/GLP1R_7KI0_chainR.pdb`

另外，建立了一个用于肽链结构分析的副本：

- `structures/semaglutide_peptide_only_7KI0.pdb`

该副本保留了肽链中的 AIB 残基，排除了水分子和 WF1 修饰基团。

需要强调：去除 WF1 的文件用于标准肽链结构分析，不代表它等同于完整的化学修饰 Semaglutide 药物。

### 五、Semaglutide 参考肽链检查

对提取后的链 P 进行残基统计。

结果：

- 肽链结构文件中共识别到 30 个残基记录。
- 其中包含非标准氨基酸 AIB。
- 原始提取文件中还包含 WF1。
- 后续分析副本中 AIB 得以保留，WF1 已排除。

AIB 是 Semaglutide 中的重要非标准氨基酸修饰，不能简单当作普通 Ala 处理。WF1 是与脂肪链修饰有关的非肽基团，不应被误当作一个氨基酸参与标准肽序列分析。

**尚待核对的问题：**

此前导出的肽链 FASTA 长度为 31 aa，而当前从结构坐标中统计到的肽链残基记录为 30 个。两者可能涉及序列记录与实验结构实际解析残基之间的差异，尚未完成逐位核对。

在将该参考序列用于后续设计前，应核对 FASTA、PDB/mmCIF 中的聚合物序列以及实际解析残基之间的对应关系。

### 六、GLP-1R 受体结构检查

受体结构文件：

`structures/GLP1R_7KI0_chainR.pdb`

对应构建体序列：

`data/GLP1R_7KI0_chainR.fasta`

FASTA 序列长度：491 aa。

当前提取的受体结构包含 384 个标准氨基酸残基，分布在以下 PDB 编号区段：

- 29–129：101 个残基
- 137–339：203 个残基
- 344–423：80 个残基

合计 384 个标准氨基酸残基。

结构中存在编号间断，说明这些区段之间并未连续呈现全部残基坐标。不能仅凭结构文件中缺少坐标，就断言相应残基在受体天然序列中不存在。

本阶段没有对缺失区域进行建模，也没有擅自修改原始结构。

### 七、受体结构编号与序列位置映射

建立脚本：

`scripts/map_glp1r_pdb_to_fasta.py`

并生成映射表：

`results/GLP1R_7KI0_residue_mapping.csv`

映射结果：

- 参与映射的结构残基：384
- 完全匹配：384
- 氨基酸错配：0

已确认结构编号与构建体 FASTA 位置并非完全相同。例如：

- PDB 链 R 残基 29 对应 FASTA 位置 38。
- PDB 链 R 残基 423 对应 FASTA 位置 432。

因此，后续分析受体接触残基时，应明确标注所用编号体系，必要时通过映射表转换，避免混淆 PDB 编号与序列位置。

### 八、本阶段主要成果

1. 建立了独立的 GLP-1R 项目目录。
2. 获取并保留了 7KI0 原始 mmCIF 参考结构。
3. 提取了 Semaglutide 肽链与 GLP-1R 受体链的结构文件和 FASTA 文件。
4. 检查了肽链中的 AIB 和 WF1，并建立了排除 WF1 的肽链结构副本。
5. 统计了 GLP-1R 结构实际解析的残基区段。
6. 完成了 384 个受体结构残基与构建体序列位置的映射，得到 384 个完全匹配、0 个错配的结果。
7. 建立了后续可重复使用的 Python 检查与映射脚本。

### 九、本阶段的科学意义

本阶段建立了后续计算设计所需的参考数据基础，并明确区分了实验复合物结构、实际解析的结构残基、构建体序列和非标准化学修饰。

这些工作可以降低后续结合界面分析中的编号错误与输入数据混淆风险。

但目前还没有完成结合界面分析、ProteinMPNN 序列设计、候选结构预测或激动活性评价。因此，本阶段成果属于数据准备与结构核验，不代表已经获得新的候选肽，也不构成结合能力或激动活性的证据。

### 十、遗留问题与下一阶段计划

**遗留问题：**

1. 核对 Semaglutide FASTA 与实际解析肽链残基数之间的差异。
2. 确认受体构建体序列、PDB 编号及实际解析区域的对应关系是否满足后续分析需求。
3. 结合界面分析前，明确使用的受体与肽链编号体系。
4. 后续根据建模软件的兼容性，决定是否需要为特定软件准备单独的标准化输入副本。

**下一阶段：参考复合物与结合界面分析**

计划开展：

1. 分析 7KI0 中 Semaglutide 与 GLP-1R 的空间接触。
2. 使用明确的距离阈值定义几何接触，并保存逐残基接触结果。
3. 将受体接触残基转换为构建体 FASTA 序列位置。
4. 根据参考复合物结构，进一步讨论后续序列设计的输入与约束。

下一阶段完成后，单独建立阶段二工作记录，并保存脚本、原始输出和分析结果。

### 序列与结构核对补充（7KI0，Semaglutide）

- 聚合物序列记录长度：31 个位置，序列为 `HAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG`。
- 结构中有坐标的肽链残基数：30。
- mmCIF 的 `_pdbx_poly_seq_scheme` 显示第 31 位 GLY 对应的作者残基编号为 37，但实际残基编号、残基名称等坐标映射字段为缺失值。
- 因此，第 31 位 Gly 存在于聚合物序列记录中，但没有对应的已建模残基坐标。FASTA 与坐标序列的长度差异不应简单视为提取错误。
- 用于后续结构接触分析的参考肽链应以实际有坐标的 30 个残基为准；进行序列级比较时仍需保留 31 位聚合物序列，并明确处理 AIB 等非标准残基及修饰信息。
- 当前肽链提取文件保留了 AIB，排除了 WF1。WF1 属于与脂肪链修饰相关的非肽部分，不应混入普通肽残基接触统计；但在讨论 Semaglutide 完整药物分子时，不能忽略这些化学修饰。
# GLP-1R Reproduction Project
# 阶段二：参考结构界面分析与输入文件核查

项目目录：`LOCAL_PATH

记录日期：2026-10-19

阶段状态：参考结构界面分析已复跑，主要输入文件差异已核查。

---

## 1. 阶段目标

本阶段以 PDB 7KI0 中 semaglutide 与 GLP-1R 的复合物结构为参考，完成以下工作：

1. 复跑已有的肽—受体界面接触分析。
2. 检查选定肽残基与受体残基之间的最近重原子距离。
3. 盘点现有分析脚本，确认主要分析输入文件。
4. 核查两个 semaglutide 肽链文件之间的残基、原子数差异。
5. 验证两个文件共有原子的坐标是否一致。
6. 明确当前结构分析能够支持的结论及其局限。

本阶段的目标是建立可复现的参考结构分析基础，为后续 GLP-1R 候选肽的结构比较制定统一规则。

本阶段不涉及新候选肽设计、实验亲和力测定或激动活性验证。

## 2. 参考结构与输入文件

### 2.1 参考结构

- PDB ID：7KI0
- 结构对象：semaglutide–GLP-1R 复合物
- 受体链：R
- 肽链：P
- 参考结构分辨率：2.50 Å

该结构用于描述已知 GLP-1R 激动剂 semaglutide 在复合物中的结构界面。

### 2.2 界面分析实际输入

受体结构：

`structures/GLP1R_7KI0_chainR.pdb`

肽链结构：

`structures/semaglutide_peptide_only_7KI0.pdb`

输入检查结果：

- 受体：384 个残基，3175 个重原子。
- 肽链：30 个残基，236 个重原子。
- 受体结构残基映射至 FASTA 序列：384/384。
- 肽链中的非标准氨基酸 AIB 被保留。
- 肽链分析文件中的 WF1 被排除。

需要注意，PDB 残基编号与序列位置并不总是一致。分析报告中的受体位点采用 FASTA 序列位置；引用结构中的残基时，应明确标注所使用的编号体系。

## 3. 界面接触分析

### 3.1 分析方法

脚本：

`scripts/analyze_glp1r_interface.py`

分析方法：

1. 读取肽链和受体结构。
2. 提取重原子，排除氢原子和氘原子。
3. 计算肽链与受体之间的重原子欧氏距离。
4. 分别以 4 Å 和 5 Å 为阈值统计接触。
5. 输出肽—受体残基对表和肽残基汇总表。

本阶段已重新运行脚本，运行成功，统计结果与此前记录一致。

### 3.2 结果

4 Å 阈值：

- 重原子对数量：196
- 不同肽—受体残基对：60
- 有接触的肽残基：24
- 有接触的受体残基：40

5 Å 阈值：

- 重原子对数量：832
- 不同肽—受体残基对：108
- 有接触的肽残基：28
- 有接触的受体残基：49

### 3.3 输出文件

- `results/GLP1R_semaglutide_contacts_4A.csv`
- `results/GLP1R_semaglutide_contacts_5A.csv`
- `results/GLP1R_semaglutide_peptide_summary_4A.csv`
- `results/GLP1R_semaglutide_peptide_summary_5A.csv`

其中，重原子对数量表示满足距离阈值的原子对数量；不同残基对表示发生接触的肽残基—受体残基组合数量。二者不能混为一谈。

接触数量是几何描述指标，不等同于结合能、结合亲和力或激动活性。

## 4. 原子级最近距离分析

### 4.1 分析方法

脚本：

`scripts/analyze_interface_atom_pairs.py`

输出文件：

`results/GLP1R_semaglutide_nearest_atom_pairs_4A.csv`

本次运行成功，输出 22 个选定残基对的最近重原子距离。

### 4.2 代表性观察

以下受体位置均为 FASTA 序列位置。

- Semaglutide Glu3 与受体 Arg199 的最近重原子距离为 2.691 Å。
- Semaglutide Glu3 与受体 Tyr161 的最近重原子距离为 2.580 Å。
- Semaglutide Glu15 与受体 Arg308 的最近重原子距离为 2.870 Å。
- Semaglutide Glu15 与受体 Ser40 的最近重原子距离为 3.031 Å。

这些结果显示，部分肽残基与受体局部区域存在较近的空间接触，可作为进一步检查局部相互作用的候选位置。

但本阶段没有显式氢原子，也没有计算氢键角度或进行专门的相互作用能分析。因此，不能仅凭距离确认氢键、盐桥或其他特定化学相互作用。

同样，结构接近不能单独证明某个残基对受体激动功能具有因果作用。

## 5. 输入文件一致性核查

### 5.1 两份肽链文件的差异

原始提取文件：

`structures/semaglutide_7KI0_chainP.pdb`

- 残基记录：31
- 原子数：256
- 包含 AIB
- 包含 WF1

用于界面分析的肽链文件：

`structures/semaglutide_peptide_only_7KI0.pdb`

- 残基记录：30
- 原子数：236
- 包含 AIB
- 不包含 WF1

### 5.2 差异来源

检查了以下脚本：

- `scripts/extract_7ki0_chains.py`
- `scripts/make_semaglutide_peptide_only.py`

原始提取脚本保留了 WF1；肽链整理脚本则明确排除 WF1，同时保留 AIB。

因此，两份文件的残基数和原子数差异与 WF1 的筛选规则一致。

### 5.3 共有原子坐标比较

采用残基标识、残基名称、原子名称和元素作为原子匹配键，对两份文件进行比较。

结果：

- 原始提取文件：256 个原子。
- 肽链分析文件：236 个原子。
- 成功匹配的共有原子：236 个。
- 仅存在于原始文件的原子：20 个。
- 仅存在于肽链分析文件的原子：0 个。
- 共有原子的最大坐标差异：0.000000 Å。
- 坐标差异大于 0.001 Å 的共有原子：0 个。

该结果确认，肽链分析文件保留的 236 个原子在原始提取文件中均能找到对应原子，且坐标完全一致。多出的 20 个原子与 WF1 相对应。

这项检查证明了两个提取后文件之间共有部分的坐标一致性，不等于对原始 mmCIF 到 PDB 的整个转换过程进行了独立验证，也不单独证明结构的生物学解释完全正确。

### 5.4 主分析脚本的输入路径

检查 `scripts/analyze_glp1r_interface.py` 后，确认其使用：

- `structures/semaglutide_peptide_only_7KI0.pdb`
- `structures/GLP1R_7KI0_chainR.pdb`

因此，本阶段复跑的界面分析使用的是排除 WF1、保留 AIB 的 30 残基肽链文件，没有误用包含 WF1 的 31 残基版本。

## 6. 本阶段涉及的主要脚本

- `scripts/check_7ki0.py`
- `scripts/check_7ki0_residue_details.py`
- `scripts/export_7ki0_sequences.py`
- `scripts/export_glp1r_residue_mapping.py`
- `scripts/extract_7ki0_chains.py`
- `scripts/inspect_7ki0_structure.py`
- `scripts/make_semaglutide_peptide_only.py`
- `scripts/map_7ki0_entities.py`
- `scripts/map_glp1r_pdb_to_fasta.py`
- `scripts/summarize_glp1r_structure.py`
- `scripts/validate_extracted_pdbs.py`
- `scripts/validate_semaglutide_sequence.py`
- `scripts/analyze_glp1r_interface.py`
- `scripts/analyze_interface_atom_pairs.py`

本阶段已运行并复核的核心分析脚本为：

- `scripts/analyze_glp1r_interface.py`
- `scripts/analyze_interface_atom_pairs.py`

同时检查了结构提取和肽链整理脚本，以及主分析脚本的实际输入路径。

## 7. 当前结论

本阶段建立了 semaglutide–GLP-1R 参考界面的可复现几何描述，并完成了界面分析输入文件的关键一致性核查。

当前证据支持以下结论：

1. 两项界面分析脚本均能成功运行。
2. 4 Å 和 5 Å 接触统计结果已复现。
3. 两份肽链文件的原子数差异可由 WF1 的筛选规则解释。
4. 肽链分析文件的 236 个共有原子与原始提取文件坐标完全一致。
5. 主分析脚本使用了预期的肽链与受体结构文件。

这些结果为后续候选肽结构比较提供了参考基础，但不能直接用于判断新候选肽的实验结合亲和力或激动能力。

## 8. 当前限制

- 未计算结合自由能。
- 未计算或测定实验结合亲和力。
- 未进行实验激动活性验证。
- 未对氢键角度、质子化状态或局部化学几何进行系统分析。
- 未验证任何候选肽的功能。
- 未独立完成原始 mmCIF 到所有提取 PDB 文件的逐原子转换验证。
- WF1 被排除是当前分析文件的处理规则，不代表该修饰基团在真实分子中没有生物学意义。

结构接触和结构预测只能提供有限的计算证据。不能把它们直接等同于实验亲和力或受体激动活性。

## 9. 下一阶段计划

下一阶段建议建立统一、可复现的 GLP-1R 候选肽结构比较协议。

重点包括：

1. 明确候选肽和参考结构的输入与预处理规则。
2. 统一序列位置、PDB 编号和受体残基映射方式。
3. 规定结构对齐、界面接触及局部几何比较指标。
4. 区分结构合理性、计算结合证据与实验激动活性证据。
5. 再开展候选肽的结构比较与排序，避免根据结果临时选择有利指标。

项目的核心目标是利用结构证据评估候选肽的合理性，而不是仅凭高分或局部接触宣称候选肽具有更强的结合能力或激动活性。

---

文档类型：阶段科研记录

文档状态：基于已完成的计算分析与输入文件核查整理

对应详细日志：`logs/2026-10-19_interface_analysis.md`

---

# chatgpt response

这两份阶段工作记录很有价值。我已经把它们与前面四份日志对应起来了。它们补足了项目早期的结构准备背景，但也进一步说明：**我们现在最需要补齐的不是结构分析，而是候选序列筛选规则的论文依据与实现证据。**

## 一、这两份记录对当前任务有什么帮助？

<box border radius="lg" padding={3} gap={3}>
  <row align="start" gap={3}>
    <icon name="check-circle" color="success" size="xl"/>
    <box flex="1" gap={1}>
      **已经有较明确证据的部分**

      - 参考结构是 PDB 7KI0，受体链 R、肽链 P。
      - 当前用于 ProteinMPNN 的参考肽序列为 30 aa 坐标支持序列。
      - 完整聚合物序列是 31 aa，末端 Gly 没有对应坐标。
      - 参考界面分析使用保留 AIB、排除 WF1 的结构文件。
      - 结构接触统计和受体残基映射已有相应脚本与结果。
    </box>
  </row>
  <divider color="subtle"/>
  <row align="start" gap={3}>
    <icon name="alert-circle" color="warning" size="xl"/>
    <box flex="1" gap={1}>
      **尚不能据此确定的部分**

      - 论文究竟规定了哪些酶切位点过滤规则。
      - DV、SY、YL、EF、FI、WL 分别依据哪段论文原文。
      - 两轮旧筛选为什么采用当 SCRIPT ====="
  cat results/proteinmpnn/test_2000seq_renumbered/screening_step2_cleavage/screen_cleavage_step2.py

  echo
  echo "===== STEP 1 AUDIT COLUMN NAMES ====="
  head -n 1 results/proteinmpnn/test_2000seq_renumbered/screening_step1_cleavage/screening_step1_audit.csv

  echo
  echo "===== STEP 2 AUDIT COLUMN NAMES ====="
  head -n 1 results/proteinmpnn/test_2000seq_renumbered/screening_step2_cleavage/screening_step2_audit.csv
}
</CodeBlock>

这一步只读取脚本和审计表表头，不运行程序，也不修改旧结果。

## 三、接下来我们如何判断规则是否可靠？

收到输出后，我会把每条规则放入以下三类：

| 分类 | 判断依据 | 后续处理 |
|---|---|---|
| 论文明确规定 | 正文或补充材料存在明确依据 | 按原文核对实现 |
| 论文相关但无法完整复现 | 论文报告了指标，但缺少完整阈值、参数或算法细节 | 保留复现缺口说明 |
| 项目探索性规则 | 由我们自行提出或采用，尚无论文依据 | 与论文复现流程分开保存 |

随后才是以 D13、D41、D44 为参考锚点，检查它们与 1,435 条去重序列之间的关系。

**我们的目标不是让新流程筛出更少的序列，而是让每一次保留或淘汰都有明确、可追溯的理由。**

---

# you asked

message time: 2026-10-19 22:54:17

# GLP-1R 论文复现阶段记录：ProteinMPNN 输入准备与小规模验证

**记录日期：** 2026-10-19  
**项目目录：** `LOCAL_PATH  
**当前阶段：** ProteinMPNN 输入准备与 2 条测试序列验证  
**状态：** 小规模测试通过；尚未启动正式的 10,000 条序列生成

## 1. 本阶段目标

复现论文 *AI-Driven De Novo Design of Ultra Long-Acting GLP-1 Receptor Agonists*（Advanced Science，2025，DOI: 10.1002/advs.202507044）中涉及的 GLP-1RA 序列设计流程。

本阶段重点是：

1. 提取 GLP-1R 与 semaglutide 的复合物结构。
2. 准备 ProteinMPNN 使用的受体—肽链复合物输入。
3. 设置肽链固定位置。
4. 生成少量测试序列，检查设计链和固定位置是否符合预期。

本阶段不涉及候选序列的活性验证，也不代表已经复现论文全部实验结果。

## 2. 结构与序列准备

### 2.1 结构来源

输入结构来自 `7KI0.cif`，使用的链为：

- 受体链 R：GLP-1R
- 肽链 P：semaglutide

项目中的相关文件：

- `structures/7KI0.cif`
- `structures/GLP1R_7KI0_chainR.pdb`
- `structures/semaglutide_7KI0_chainP.pdb`
- `structures/semaglutide_peptide_only_7KI0.pdb`
- `structures/GLP1R_semaglutide_ProteinMPNN_input.pdb`

### 2.2 肽链长度差异

原始 semaglutide 序列长度为 31 aa：

`HAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG`

当前结构中具有坐标的肽链只有 30 个残基：

`HAEGTFTSDVSSYLEGQAAKEFIAWLVRGR`

末端 Gly 缺少结构坐标。

**当前复现处理假设：** 在现有 30 aa 结构上进行序列设计，后续将末端 Gly 补回，形成 31 aa 序列。该处理是本项目的复现选择，不能据此认定论文作者采用了完全相同的输入处理方式。

### 2.3 非标准氨基酸 Aib

Semaglutide 的第 2 位在化学结构中为 Aib（α-aminoisobutyric acid），属于非标准氨基酸。

当前 ProteinMPNN 输入中将 Aib 近似表示为 Ala（A），以适配标准氨基酸序列设计流程。该近似不保留 Aib 的完整化学特性。

原始结构文件应保持不变；该替代仅用于 ProteinMPNN 输入副本。

## 3. ProteinMPNN 输入与配置

ProteinMPNN 仓库：

`USER_HOME/ProteinMPNN`

运行环境：`proteinmpnn`

使用模型：`v_48_020`

当前输入与配置文件：

- `results/proteinmpnn/input/GLP1R_semaglutide_ProteinMPNN_input.pdb`
- `results/proteinmpnn/parsed_chains.jsonl`
- `results/proteinmpnn/fixed_positions.jsonl`

### 3.1 设计链设置

本项目将链 P 设为设计链，链 R 作为固定受体结构。

测试运行输出明确显示：

- `fixed_chains=['R']`
- `designed_chains=['P']`

因此，小规模测试符合“保持受体结构、设计肽链序列”的预期。

### 3.2 固定位置设置

补充材料中列出以下需要保留的残基：

| 论文位置 | 残基 | 当前结构可对应的序列位置 |
|---:|:---:|---:|
| 7 | H | 1 |
| 8 | Aib（输入近似为 A） | 2 |
| 9 | E | 3 |
| 10 | G | 4 |
| 11 | T | 5 |
| 12 | F | 6 |
| 13 | T | 7 |
| 14 | S | 8 |
| 15 | D | 9 |
| 17 | S | 11 |
| 26 | K | 20 |
| 34 | R | 28 |
| 37 | G | 31（无结构坐标） |

补充材料文字称固定 12 个残基，但实际列出的条目有 13 个。当前结构缺少第 31 位末端 Gly 的坐标，因此当前 ProteinMPNN 固定位置配置包含 12 个有坐标的位置：

`[1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 20, 28]`

固定残基为：

`H, A, E, G, T, F, T, S, D, S, K, R`

需要注意：补充材料提及这些残基的实验背景，并不能单独证明论文在 ProteinMPNN 阶段采用了完全相同的固定位置策略。本项目将其作为可追溯的复现假设。

### 3.3 受体链编号问题

ProteinMPNN 的解析结果中，受体链 R 长度显示为 395，而实际具有坐标的受体残基为 384 个。解析结果会在 PDB 残基编号缺口处插入 `-`。

这说明 PDB 编号缺口被解析成了序列中的占位符。当前小规模测试可以运行，但尚未充分评估这种表示对后续设计的影响。

**待解决：** 检查是否需要在不改变实际结构几何的前提下，将受体链残基重新连续编号后再解析，并比较两种输入的解析结果。

## 4. 小规模测试结果

测试输出目录：

`results/proteinmpnn/test_2seq/`

输出 FASTA：

`results/proteinmpnn/test_2seq/seqs/GLP1R_semaglutide_ProteinMPNN_input.fa`

测试参数：

- 每个目标生成 2 条序列
- `batch_size = 1`
- `sampling_temp = 0.1`
- 模型：`v_48_020`

终端显示：

`2 sequences of length 425 generated in 2.7772 seconds`

这里的 425 是解析后两条链的总长度（受体链 395 + 肽链 30），不是候选肽本身的长度。

### 4.1 测试序列

原始 30 aa 肽链：

`HAEGTFTSDVSSYLEGQAAKEFIAWLVRGR`

候选 1：

`HAEGTFTSDVSRYLDEKAAKEFVERLKRGG`

候选 2：

`HAEGTFTSDVSSYLEEKQAKEFVERLRRGS`

两条候选均为 30 aa。

### 4.2 固定位置核验

通过 Python 脚本逐位检查，两条候选在以下位置均与预期一致：

- 1 H
- 2 A
- 3 E
- 4 G
- 5 T
- 6 F
- 7 T
- 8 S
- 9 D
- 11 S
- 20 K
- 28 R

检查结果：**两条候选的全部 12 个固定位置均通过。**

这验证了当前小规模测试中的固定位置配置有效；尚不能证明后续全部输出均符合预期，正式生成后仍需自动化检查。

## 5. 当前结论

本阶段已完成：

1. 准备 GLP-1R—semaglutide 复合物的 ProteinMPNN 输入副本。
2. 将非标准 Aib 在设计输入中近似表示为 Ala。
3. 设置肽链 P 为设计链、受体链 R 为固定链。
4. 建立固定位置配置。
5. 成功生成 2 条测试序列。
6. 验证两条序列长度均为 30 aa，且全部 12 个有坐标固定位置符合预期。

本阶段尚未完成：

1. 受体链残基编号缺口的影响评估。
2. 末端 Gly 补回方案的自动化实现与验证。
3. 10,000 条候选序列的正式生成。
4. 正式输出数量、重复序列、固定位置和序列长度的批量核验。
5. 后续酶切位点筛选、结构预测、理化性质筛选及其他论文筛选步骤。

## 6. 下一阶段计划

在启动正式生成之前，按以下顺序推进：

1. 检查受体链解析出的 395 位序列与 384 个有坐标残基之间的对应关系。
2. 决定是否需要对受体链 PDB 残基编号进行连续化处理，并重新执行小规模测试。
3. 编写并验证候选序列的批量核验与末端 Gly 补回流程。
4. 确认正式输入和配置后，再运行 10,000 条序列生成。
5. 保存命令、参数、随机种子、输出统计与处理日志，保证后续结果可追溯。

**记录原则：** 区分论文明确报告的事实、项目实际观察到的结果，以及为了复现而作出的假设；不得将计算设计结果直接表述为已经验证的受体结合能力或激动活性。

# 补充记录：ProteinMPNN 受体链连续重编号与回归测试

**日期：** 2026-10-19  
**关联阶段记录：** `2026-10-19_proteinmpnn_stage1.md`  
**状态：** 重编号与小规模回归测试已通过；1,000 条序列尚未生成

## 1. 问题发现

初始 ProteinMPNN 输入结构为：

`structures/GLP1R_semaglutide_ProteinMPNN_input.pdb`

检查发现，受体链 R 有 384 个实际存在的标准氨基酸残基，PDB 编号范围为 29–423。但 ProteinMPNN 解析结果显示链 R 长度为 395，并在残基编号缺口处插入 `-` 占位符。

经逐段检查，发现两处编号缺口：

| 前一残基 | 后一残基 | 缺少的 PDB 编号 | 缺口大小 |
|---|---|---|---:|
| 129 SER | 137 PRO | 130–136 | 7 |
| 339 LEU | 344 ASP | 340–343 | 4 |
| **合计** | | | **11** |

因此：

384 个实际残基 + 11 个编号占位符 = 395 个解析位置。

这 11 个位置来自 PDB 编号不连续，并非 11 个真实存在的氨基酸残基。

## 2. 修正方法

为避免 ProteinMPNN 将 PDB 编号缺口解析为额外序列位置，创建了独立的连续编号输入文件：

`structures/GLP1R_semaglutide_ProteinMPNN_input_renumbered.pdb`

处理原则：

1. 仅对受体链 R 的实际标准氨基酸残基重新编号。
2. 将链 R 的 384 个残基连续编号为 1–384。
3. 不对原子坐标进行几何变换。
4. 不修改原始输入文件。
5. 保留肽链 P 的原有序列与坐标。
6. 为新结构名称重新生成对应的固定位置配置。

新固定位置配置：

`results/proteinmpnn/renumber_check/fixed_positions.jsonl`

其内容为：

`{"GLP1R_semaglutide_ProteinMPNN_input_renumbered": {"P": [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 20, 28], "R": []}}`

## 3. 修正后解析验证

使用 ProteinMPNN 自带的 `parse_multiple_chains.py` 重新解析连续编号后的结构。

结果如下：

| 检查项 | 修正前 | 修正后 |
|---|---:|---:|
| 受体链 R 解析长度 | 395 | 384 |
| 受体链 R 的 `-` 数量 | 11 | 0 |
| 肽链 P 解析长度 | 30 | 30 |
| 肽链 P 的 `-` 数量 | 0 | 0 |

修正后，两条链的解析长度均符合实际输入结构中的残基数量。

## 4. ProteinMPNN 回归测试

使用连续编号后的结构进行 2 条序列的小规模测试。

**输入与参数：**

- 输入结构：`structures/GLP1R_semaglutide_ProteinMPNN_input_renumbered.pdb`
- 设计链：P
- 固定链：R
- 模型：`v_48_020`
- 采样温度：0.1
- 测试序列数：2
- 批次大小：1

输出文件：

`results/proteinmpnn/test_2seq_renumbered/seqs/GLP1R_semaglutide_ProteinMPNN_input_renumbered.fa`

终端报告：

`2 sequences of length 414 generated in 2.5111 seconds`

414 为两条链的解析总长度：

384（受体链 R）+ 30（肽链 P）= 414。

输出头信息确认：

- `fixed_chains=['R']`
- `designed_chains=['P']`

两条候选肽序列分别为：

1. `HAEGTFTSDVSRYLEEKAVKAFVERLKRGA`
2. `HAEGTFTSDVSRYLEEKAAKEFVERLKRGS`

两条序列均为 30 aa。

## 5. 固定位置回归检查

对两条候选序列执行逐位检查，确认以下 12 个位置均保持预设残基：

| 序列位置 | 固定残基 |
|---:|:---:|
| 1 | H |
| 2 | A |
| 3 | E |
| 4 | G |
| 5 | T |
| 6 | F |
| 7 | T |
| 8 | S |
| 9 | D |
| 11 | S |
| 20 | K |
| 28 | R |

**检查结果：两条候选序列的全部固定位置均通过。**

## 6. 结论与影响

连续重编号解决了 ProteinMPNN 解析受体链时产生的 11 个编号占位符问题。修正后的输入能够正常完成序列生成，并通过设计链、序列长度和固定位置检查。

后续正式设计应优先使用：

- `structures/GLP1R_semaglutide_ProteinMPNN_input_renumbered.pdb`
- `results/proteinmpnn/renumber_check/fixed_positions.jsonl`

原始结构及旧测试结果保留作为处理前的记录，不应与修正后的正式结果混淆。

## 7. 尚未解决的问题

1. 当前结构中肽链只有 30 个有坐标的残基，原始 semaglutide 序列为 31 aa，末端 Gly 尚未纳入 ProteinMPNN 设计。
2. Aib 在设计输入中近似表示为 Ala，不能体现其完整的非标准氨基酸化学特性。
3. 本次回归测试只验证了 2 条候选序列；正式批量生成后仍需检查实际数量、重复率、固定位置和长度。
4. 尚未运行 1,000 条候选序列生成，也尚未进入后续筛选步骤。

**可复现性说明：** 本记录仅陈述已执行的结构处理和测试结果。连续重编号是针对解析器行为的输入修正，不代表原始生物学结构中的缺失环区已被恢复，也不意味着模型已验证候选序列的结合能力或激动活性。
# GLP-1R 从头肽设计项目工作记录

## 阶段四：ProteinMPNN 正式序列生成与结果审计

**项目名称：** GLP-1R 计算设计与候选肽评估  
**阶段名称：** ProteinMPNN 批量序列生成、去重与评分字段审计  
**记录日期：** 2026-10-19  
**项目根目录：** `LOCAL_PATH  
**运行环境：** WSL Ubuntu 22.04.5  
**软件环境：** `proteinmpnn`  
**模型：** ProteinMPNN `v_48_020`  
**参考结构：** PDB 7KI0  
**阶段状态：** 50 组生成任务及基础数据核验已完成；序列频率与模型评分的关系分析待继续；尚未完成候选结构预测与生物学活性评价。

---

## 一、本阶段目标

在完成参考结构准备、ProteinMPNN 输入处理和小规模测试后，开展正式的批量序列生成，并检查输出数据是否完整、符合预设约束且可供后续分析。

主要任务：

1. 使用固定的受体—肽链复合物输入，批量生成 GLP-1R 相关候选肽序列。
2. 使用多个随机种子运行生成任务，累计获得 10,000 条候选序列记录。
3. 检查每条候选序列的长度、氨基酸字符和固定位置。
4. 汇总不同批次的重复序列，生成去重序列集及出现次数表。
5. 检查 ProteinMPNN 输出的 `score`、`global_score` 和 `seq_recovery` 字段。
6. 初步分析候选序列的重复程度、采样分布与模型评分，为后续候选筛选建立数据基础。

本阶段仅涉及计算序列生成与输出审计，不代表已经获得具有 GLP-1R 结合能力或激动活性的候选肽。

## 二、输入结构与设计约束

### 2.1 输入结构

使用 PDB 7KI0 中 GLP-1R 与 Semaglutide 的复合物结构作为设计参考。

ProteinMPNN 输入副本：

`structures/GLP1R_semaglutide_ProteinMPNN_input_renumbered.pdb`

输入链设置：

- 链 R：GLP-1R 受体，作为固定结构链。
- 链 P：Semaglutide 参考肽链，作为序列设计链。

在正式生成前，已准备受体残基连续编号的输入副本，以减少原始结构残基编号缺口对 ProteinMPNN 序列解析的影响。原始结构文件仍保留，不以处理后的副本替代原始数据。

### 2.2 肽链长度

参考肽链在聚合物序列记录中有 31 个位置，但 7KI0 中只有 30 个残基具有坐标。

本阶段 ProteinMPNN 实际设计的是具有结构坐标的 30 aa 肽链。所有候选序列均按 30 aa 进行检查。

**重要限制：** 本阶段没有将缺少坐标的末端 Gly 自动补入候选序列。因此，不能将当前输出直接描述为已经完成了 31 aa 完整肽序列的恢复，也不能把末端字符为 G 的 30 aa 序列解释为已经补回缺失的第 31 位 Gly。

### 2.3 固定位置

当前项目使用以下 12 个固定位置：

`[1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 20, 28]`

对应固定残基：

`H, A, E, G, T, F, T, S, D, S, K, R`

这些位置来自本项目根据论文补充材料和当前结构进行的复现假设。由于论文中固定残基描述与实际列出的条目存在需要解释的差异，不能据此断言本项目配置与论文作者的原始实现完全一致。

### 2.4 生成策略

当前批量结果位于：

`results/proteinmpnn/test_2000seq_renumbered/`

主要生成目录为：

`results/proteinmpnn/test_2000seq_renumbered/batch200_seed1/` 至 `batch200_seed50/`

每个批次的 FASTA 文件位于相应目录的 `seqs/` 子目录。

已核验的运行设置包括：

- 模型：`v_48_020`
- 设计链：P
- 固定链：R
- 采样温度：`0.1`
- 随机种子：1–50
- 每个批次的候选序列数：200

以上共计 50 个批次、10,000 条候选序列记录。

需要说明：本阶段核验了 FASTA 输出中记录的采样温度、样本编号及评分字段。对于所有底层运行参数是否完整一致，仍应以正式命令、配置文件和运行日志为最终依据，不将尚未核实的参数写成已确认事实。

---

## 三、批量生成结果与完整性核验

### 3.1 输出数量

对 50 个批次的 FASTA 输出进行检查。

结果：

- 批次数：50
- 每批候选序列记录数：200
- 候选序列记录总数：10,000
- 每个 FASTA 文件的记录总数：201，其中包括 1 条参考序列记录和 200 条生成候选记录。

因此，后续统计候选序列时，应排除每个文件中的参考序列记录，避免将参考序列重复计入候选集。

### 3.2 序列格式核验

对 10,000 条候选序列进行基础检查，结果如下：

- 序列长度：全部为 30 aa
- 非标准氨基酸字符：未发现
- 固定位置不符合预设残基的序列：0 条
- 格式异常记录：0 条

所有候选序列均符合当前项目设置的长度、字符和固定位置要求。

这里的“通过”只说明序列满足当前输入与生成约束，不代表序列在结构上合理，也不代表其具有受体结合能力、激动活性、药代动力学优势或其他药物性质。

### 3.3 输出评分字段

检查每条候选记录的 FASTA 标题，确认以下字段完整：

- `score`
- `global_score`
- `seq_recovery`

50 个批次中，每批 200 条候选记录均包含上述三个字段。

这些字段可用于后续模型内部评分分析，但其含义不同，不能不加区分地合并为一个“候选质量分数”。

---

## 四、全批次去重与序列多样性统计

### 4.1 去重结果

将 50 个批次的候选序列合并，并按完整氨基酸序列进行去重。

结果：

| 指标 | 数值 |
|---|---:|
| 候选记录总数 | 10,000 |
| 全局唯一序列数 | 1,435 |
| 重复记录超额数 | 8,565 |
| 至少出现两次的不同序列数 | 603 |
| 仅出现一次的不同序列数 | 832 |
| 重复记录占全部候选记录的比例 | 85.65% |

说明：这里的“重复记录超额数”定义为总记录数减去唯一序列数，即 10,000 − 1,435 = 8,565。它不是指有 8,565 种重复序列。

结果显示，10,000 条采样记录最终对应 1,435 条不同序列，采样结果存在明显的重复现象。

这一结果描述的是当前 ProteinMPNN 输入、模型、采样温度和运行设置下的输出分布，不能直接解释为自然界中的序列出现概率，也不能作为生物学活性的证据。

### 4.2 频次最高的序列

当前出现次数最高的序列包括：

| 候选序列 | 出现次数 |
|---|---:|
| `HAEGTFTSDVSRYLEEKAAKEFVERLKRGR` | 636 |
| `HAEGTFTSDVSRYLEEKAAKEFVERLKRGS` | 495 |
| `HAEGTFTSDVSRYLEEKAAKEFVERLKRGG` | 467 |
| `HAEGTFTSDVSRYLEEKAVKEFVERLKRGR` | 440 |
| `HAEGTFTSDVSRYLEEKAVKEFVERLKRGS` | 370 |
| `HAEGTFTSDVSSYLEEKAAKEFVERLKRGR` | 200 |
| `HAEGTFTSDVSRYLEEKAVKEFVERLKRGG` | 187 |
| `HAEGTFTSDVSSYLEEKAAKEFVERLKRGS` | 154 |
| `HAEGTFTSDVSSYLEEKAAKEFVERLKRGG` | 141 |
| `HAEGTFTSDVSRYLEEKQVKEFVERLKRGR` | 131 |

其中，出现次数最高的序列累计出现 636 次。

多个高频序列之间仅有少数位置不同，说明当前采样结果在部分序列模式附近较为集中。

但仅凭频次不能判断这种集中是由模型偏好、约束位置、采样设置或其他因素中的哪一项造成的。需要结合模型评分、不同随机种子的支持情况以及后续结构分析进一步研究。

### 4.3 不同随机种子的贡献

50 个批次均有候选序列输出，各批次的唯一序列数存在差异。

每个批次 200 条候选记录中的唯一序列数约为 104–130 条。

以 seed 1 为参照，各其他种子与 seed 1 的唯一序列集合交集数量为 33–48 条。各批次之间既有共同序列，也有新的序列。

这说明不同随机种子产生了部分重叠、部分不同的采样结果；但不同种子并没有消除序列重复现象。

本阶段尚未据此计算严格的独立性指标，也没有将不同种子视为完全独立的生物学重复实验。

### 4.4 末端残基观察

在 10,000 条候选记录中，有 2,564 条序列的第 30 位为 G。

这些序列仍然全部是 30 aa，而不是 31 aa。第 30 位的 G 不能被误认为是结构中缺失的第 31 位 Gly 已经恢复。

---

## 五、去重数据文件与一致性检查

已生成全 50 批次的去重结果。

**唯一序列 FASTA：**

`results/proteinmpnn/test_2000seq_renumbered/deduplicated/unique_candidates_all50_v2.fasta`

**序列计数 CSV：**

`results/proteinmpnn/test_2000seq_renumbered/deduplicated/sequence_counts_all50_v2.csv`

CSV 包含以下字段：

- `unique_id`：唯一序列编号
- `sequence`：氨基酸序列
- `length`：序列长度
- `count`：在全部候选记录中的出现次数
- `first_seed`：首次出现的种子编号
- `first_candidate`：首次出现时的候选记录编号
- `all_sources`：出现过该序列的来源记录信息

一致性核验结果：

1. CSV 中共有 1,435 条唯一序列记录。
2. 去重 FASTA 中共有 1,435 条序列。
3. CSV 的 `count` 列总和为 10,000。
4. CSV 与 FASTA 中的唯一序列内容一致。

因此，当前 `all50_v2` 文件可以作为后续唯一序列分析的全批次去重数据入口。

注意：较早生成的 `deduplicated/unique_candidates.fasta` 和 `deduplicated/sequence_counts.csv` 并非全 50 批次最终版本。需要分析全部 10,000 条记录时，应使用文件名包含 `all50_v2` 的版本。

---

## 六、ProteinMPNN 评分字段的代码审计

### 6.1 代码来源

检查了以下源代码：

- `USER_HOME/ProteinMPNN/protein_mpnn_run.py`
- `USER_HOME/ProteinMPNN/protein_mpnn_utils.py`

在 `protein_mpnn_utils.py` 中，`_scores` 函数将负对数概率按掩码进行平均。

简化表示：

`score = masked negative log-probability 的平均值`

因此，在可比较的模型、输入和计算条件下，较低的 `score` 通常意味着模型对相应已生成氨基酸序列赋予了较高的概率。

这是模型内部的序列似然类指标，不是实验结合自由能、解离常数 Kd 或受体激动活性的直接测量。

### 6.2 `score` 的含义

在当前运行设置中，链 R 固定、链 P 设计。

代码使用的评分掩码为：

`mask * chain_M * chain_M_pos`

该掩码用于选取参与设计的残基。因此，当前 `score` 主要反映设计链 P 上生成序列的平均负对数概率。

后续候选排序时，可以将其作为一个模型内部序列评分指标，但不能单凭该值判断候选肽是否具有更强的 GLP-1R 结合能力。

### 6.3 `global_score` 的含义

代码中 `global_score` 使用整个有效结构残基的掩码计算：

`mask`

因此，在当前复合物设计设置下，它对应包含固定受体链 R 和设计肽链 P 在内的整体结构—序列评分，而不是只针对设计肽链的评分。

由于固定受体链占据了大部分结构残基，`global_score` 与设计肽自身的 `score` 不应视为同一个指标，也不应未经分析便直接用 `global_score` 替代肽链评分。

### 6.4 `seq_recovery` 的含义

`seq_recovery` 用于计算设计掩码范围内生成序列与输入参考序列的匹配比例。

在当前设置中，它主要描述生成肽链在可设计位置上与输入参考肽链的序列恢复程度。

它不等同于序列相似性的全面评价，也不是结合活性或药效指标。

---

## 七、10,000 条记录的评分分布

对全部候选记录的三个字段进行描述性统计。

| 指标 | 最小值 | 第一四分位数 | 中位数 | 第三四分位数 | 最大值 | 均值 |
|---|---:|---:|---:|---:|---:|---:|
| `score` | 1.0111 | 1.0766 | 1.0952 | 1.1156 | 1.2677 | 1.0975 |
| `global_score` | 1.8847 | 1.9210 | 1.9286 | 1.9360 | 1.9743 | 1.9284 |
| `seq_recovery` | 0.2778 | 0.5000 | 0.5556 | 0.5556 | 0.7222 | 0.5267 |

以上统计单位是 10,000 条候选记录，而不是 1,435 条唯一序列。

同一条氨基酸序列可能在不同运行记录中具有不同的评分。因此，记录级统计与去重序列级统计回答的是不同问题，后续分析必须明确统计单位。

### 7.1 相同序列的评分差异

在至少出现两次的 603 条不同序列中，603 条序列均存在至少一个评分字段随记录变化的情况。

这意味着，不能简单地把某次采样记录中的最低 `score` 当作该唯一序列唯一且固定的模型评分。

后续应按唯一序列汇总重复记录的评分，例如：

- `score_mean`
- `score_median`
- `score_std`
- `global_score_mean`
- `global_score_median`
- `seq_recovery_mean`
- `count`
- `n_seeds`

其中，`score_std` 可用于描述同一序列不同记录的评分波动；`count` 与 `n_seeds` 则描述采样支持程度。

这些字段应分别保留，不应在未经验证的情况下合并为单一综合分数。

---

## 八、当前结果的解释边界

### 8.1 生成频次不等于生物学活性

一条序列在 10,000 条记录中出现次数较多，说明它在当前 ProteinMPNN 采样设置下被多次生成。

这可以作为“采样支持程度”或“生成频次”指标，用于研究模型采样分布，但不能直接解释为：

- 该序列在自然界中更常见；
- 该序列更有可能结合 GLP-1R；
- 该序列具有更强的受体激动能力；
- 该序列具有更好的药代动力学性质；
- 该序列一定优于其他候选。

### 8.2 频次与评分是不同维度

`score` 反映模型对生成序列的内部概率评分；频次反映某一序列在多次采样记录中出现的次数。

两者可以用于互补分析，但不能直接互换。

后续应检验频次与唯一序列平均评分之间是否存在统计关联，并观察这种关联是否受到不同种子支持数量、重复记录和评分波动的影响。

即使发现相关性，也不能据此证明频次可以替代评分，更不能直接推导出生物学活性。

### 8.3 目前没有经过校准的候选筛选阈值

当前尚未建立与实验结合能力或激动活性相对应的校准数据集。因此：

- 不将某个 `score` 数值直接定义为候选合格线。
- 不将高频序列直接认定为优先实验候选。
- 不将最低评分序列直接认定为最佳设计。
- 不声称已经获得可验证的预测准确率、最佳阈值或 ROC-AUC。

候选筛选规则需要结合结构质量、序列性质、对照样本和后续实验或可靠外部证据建立。

---

## 九、本阶段主要成果

本阶段已完成：

1. 使用 50 个种子批次累计生成 10,000 条候选序列记录。
2. 验证所有候选序列均为 30 aa，未发现非标准字符。
3. 验证全部候选序列符合当前 12 个固定位置的要求。
4. 完成 10,000 条候选记录的全局去重，得到 1,435 条唯一序列。
5. 生成全批次去重 FASTA 与序列计数 CSV。
6. 核验去重数据的记录数量、频次总和及序列一致性。
7. 确认全部候选记录包含 `score`、`global_score` 和 `seq_recovery`。
8. 检查 ProteinMPNN 源代码，明确三个字段的主要计算含义。
9. 初步发现同一序列在不同采样记录中可能存在评分变化，因此后续需要进行唯一序列级聚合分析。
10. 明确区分模型内部评分、采样频次与生物学活性之间的关系。

---

## 十、尚未完成的工作

以下事项仍未完成：

1. 完成唯一序列级评分统计，计算平均值、中位数、标准差等汇总指标。
2. 分析序列出现频次与平均 `score`、`global_score` 之间的相关性。
3. 分析序列频次与不同随机种子的支持数量之间的关系。
4. 判断高频序列是否同时表现出较低的平均模型评分，或两者并无稳定关联。
5. 检查是否存在需要进一步核查的异常序列模式。
6. 对唯一序列进行理化性质分析和候选预筛选。
7. 确认后续结构预测的实际输入、软件、运行参数及输出保存路径。
8. 对筛选后的候选序列开展结构预测与结构质量评估。
9. 在有适当对照或可靠证据的条件下，评估计算指标与真实结合能力或激动活性的关系。

本阶段尚未证明任何候选序列具有 GLP-1R 结合能力、受体激动活性或长效药物性质。

---

## 十一、下一阶段计划

### 第一步：完成唯一序列级评分聚合

以全批次去重表为序列清单，回到原始 50 个 FASTA 文件，将同一氨基酸序列的全部采样记录聚合，计算：

- 记录数 `count`
- 不同种子数 `n_seeds`
- `score_mean`、`score_median`、`score_std`
- `global_score_mean`、`global_score_median`
- `seq_recovery_mean`

不得只保留最低评分记录作为该序列的代表值。

### 第二步：分析频次与评分的关系

在唯一序列层面分析：

1. 出现次数与平均 `score` 的相关性。
2. 不同种子支持数量与平均 `score` 的相关性。
3. 评分波动与序列出现次数之间的关系。
4. 高频序列与低平均评分序列是否具有明显重叠。

报告统计方法、样本数量及结果，不预设相关方向或显著性。

### 第三步：建立候选预筛选数据集

在保留原始 10,000 条记录和 1,435 条唯一序列的前提下，建立可追溯的候选汇总表。

序列频次、ProteinMPNN 评分、序列相似性、理化性质和后续结构评价应作为不同维度保留。若需要合并为综合排序，应说明方法及验证依据。

### 第四步：结构预测与后续评价

在完成数据审计后，确定适合当前计算资源的结构预测方案，保存实际使用的序列、命令、参数、运行日志和输出结构。

后续可考虑分析结构置信度、受体—肽链界面几何、接触情况及其他适用指标。但任何结构预测分数都不能单独视为实验结合能力或受体激动活性的证明。

---

## 十二、数据与复现原则

本项目后续记录遵循以下原则：

1. 保留原始结构、原始 FASTA 输出和原始运行日志。
2. 将原始采样记录与去重序列数据分开保存。
3. 明确区分论文报告事实、项目实际观察结果和复现假设。
4. 记录实际执行的命令和可核验参数，不补写未经确认的配置。
5. 统计时明确使用的是候选记录还是唯一序列。
6. 不以最低评分、最高频次或单一结构指标直接认定最佳候选。
7. 不将计算设计与结构预测结果表述为已验证的生物学活性。
8. 对后续新增结果建立独立记录，保留文件路径与生成时间，确保数据来源可追溯。

**阶段总结：** 当前已经完成 GLP-1R 参考复合物上的 ProteinMPNN 批量序列生成和基础质量核验，获得 10,000 条候选记录、1,435 条唯一序列，并建立全批次去重数据。下一步重点不是立即认定哪条序列最好，而是先完成唯一序列级评分聚合，检验采样频次与模型评分之间的关系，再结合后续结构与生物学证据开展候选筛选。

## 补充分析：唯一序列的采样支持程度与模型评分

### 1. 分析目的

在完成 50 个随机种子批次、共 10,000 条候选记录的生成与去重后，进一步分析唯一序列的出现频次、跨随机种子支持数量与 ProteinMPNN 平均评分之间的关系。

本分析用于判断采样频次能否作为模型内部评分之外的辅助描述指标，不用于直接判断候选肽的结合能力或激动活性。

### 2. 统计结果

唯一序列总数为 1,435 条，其中出现至少两次的序列有 603 条。

按不同随机种子的覆盖情况统计：

- 跨 5 个及以上 seed 的序列：260 条。
- 跨 10 个及以上 seed 的序列：147 条。

在唯一序列层面计算 Spearman 秩相关系数，结果如下：

| 分析变量 | Spearman 相关系数 |
|---|---:|
| 出现频次与平均 `score` | −0.5156 |
| 跨 seed 数与平均 `score` | −0.5155 |

由于当前 `score` 为平均负对数概率类指标，较低数值通常代表模型对相应生成序列赋予较高的概率。因此，以上负相关结果表明，在本批次数据中，出现频次较高或跨 seed 支持程度较高的唯一序列，整体上倾向于具有较低的平均 `score`。

当前结果尚未包含相关系数的置信区间和显著性检验，也未完成敏感性分析，因此暂将其作为描述性统计发现，不进一步声称统计显著性或普遍规律。

### 3. 高频序列与评分结果

频次最高的序列为：

`HAEGTFTSDVSRYLEEKAAKEFVERLKRGR`

其统计结果为：

- 出现频次：636。
- 跨 seed 数：50。
- 平均 `score`：1.0702。
- 中位 `score`：1.0694。
- `score` 标准差：0.0187。

另一条频次为 495 的序列，其平均 `score` 为 1.0747；频次为 467 的序列，其平均 `score` 为 1.0703。

在平均 `score` 最低的 10 条唯一序列中，既有只出现一次的序列，也有跨多个 seed 重复出现的高频序列。

例如，一条仅出现一次的序列平均 `score` 为 1.0701，而频次为 636 的高频序列平均 `score` 为 1.0702。两者平均评分非常接近，但采样支持程度存在明显差异。

该观察说明，单次采样获得的较低评分与跨多次采样重复出现并非完全等价的证据维度。

### 4. 重复序列的评分波动

在 603 条重复序列中，同一序列的 `score` 会随不同采样记录而变化。

重复序列的组内 `score` 标准差中位数为 0.0176，其中有 184 条序列的标准差大于 0.02。

因此，不能直接将某次采样记录中的最低 `score` 视为该唯一序列的固定评分。当前分析采用平均值、中位数和标准差描述同一序列在不同记录中的评分分布，更适合用于后续候选比较。

### 5. 结果解释与限制

本分析支持将生成频次和跨 seed 数作为辅助的采样支持指标，并与平均 `score` 分开记录。

但这些指标均来源于同一 ProteinMPNN 生成流程，不能视为相互独立的生物学证据。频次较高只能说明序列在当前采样设置下更常出现，不意味着其具有更强的 GLP-1R 结合能力、激动活性或更优药物性质。

此外，当前相关性分析尚未检验不同固定位置、采样温度、模型版本或输入结构是否会改变该关系，也没有使用实验活性数据校准模型评分。

### 6. 后续计划

1. 保留每条唯一序列的 `count`、`n_seeds`、平均 `score`、中位 `score` 和 `score` 标准差。
2. 补充相关系数的置信区间和适当的统计检验。
3. 检查频次与跨 seed 数的关系，并评估两者是否提供不同的信息。
4. 在后续候选排序中，将采样支持程度与模型评分分别报告。
5. 结合序列性质、结构预测和适当的阳性／阴性对照，进一步判断这些计算指标的实际筛选价值。

**阶段性结论：** 在当前 10,000 条 ProteinMPNN 候选记录对应的 1,435 条唯一序列中，采样频次和跨 seed 数均与平均 `score` 呈中等程度负相关。该结果支持将采样支持程度作为候选分析的辅助维度，但尚不足以证明它能够替代模型评分或预测真实生物学活性。

---

# chatgpt response

我看完了。这份工作记录非常有用，已经足够让我接上 GLP-1R 项目的主线，而且你把**实际完成的工作、复现假设、待解决问题和结论边界**区分得比较清楚。

我先帮你把当前进度钉住。我们不需要重新做已经完成的工作，也不应该因为生成了 10,000 条序列就直接跳到预测结构。

## 一、我对当前项目进度的判断

<box border radius="lg" padding={4} gap={3}>
  <row align=start gap={3}>
    <icon name="check-circle" color="success" size="xl"/>
    <box flex="1" gap={1}>
      **阶段一：参考序列与结构准备**

      <text color="secondary" size="sm">已完成主要数据准备、链提取、非标准残基检查和受体结构残基映射。</text>
    </box>
  </row>
  <divider color="subtle"/>
  <row align=start gap={3}>
    <icon name="check-circle" color="success" size="xl"/>
    <box flex="1" gap={1}>
      **阶段二：参考复合物界面分析**

      <text color="secondary" size="sm">已完成 4 Å / 5 Å 接触统计、选定原子对距离分析和肽链输入文件一致性检查。</text>
    </box>
  </row>
  <divider color="subtle"/>
  <row align=start gap={3}>
    <icon name="check-circle" color="success" size="xl"/>
    <box flex="1" gap={1}>
      **阶段三：ProteinMPNN 输入准备与回归测试**

      <text color="secondary" size="sm">已解决受体链编号缺口造成的 11 个占位符问题，并通过小规模测试核验设计链、序列长度和固定位置。</text>
    </box>
  </row>
  <divider color="subtle"/>
  <row align=start gap={3}>
    <icon name="check-circle" color="success" size="xl"/>
    <box flex="1" gap={1}>
      **阶段四：10,000 条序列生成与初步审计**

      <text color="secondary" size="sm">已获得 10,000 条生成记录、1,435 条唯一序列，并完成基本约束检查、去重和初步评分分析。</text>
    </box>
  </row>
  <divider color="subtle"/>
  <row align=start gap={3}>
    <icon name="circle-dot" size="xl" color="info"/>
    <box flex="1" gap={1}>
      **当前阶段：进入唯一序列筛选**

      <text color="secondary" size="sm">核心任务从检查生成流程转向筛选候选序列，随后再进入结构预测与结构评价。</text>
    </box>
  </row>
</box>

## 二、我认为现在最重要的三个决定

### 1. 不再把生成频次和跨 seed 数当作筛选条件

你已有的分析显示：

- 1,435 条唯一序列中，频次与平均 `score` 的 Spearman 相关系数为 −0.5156。
- 跨 seed 数与平均 `score` 的相关系数为 −0.5155。
- 高频序列和低平均 `score` 序列并不完全重合。

这说明两者存在明显关联，但不能说明频次能够独立预测活性。

因此，**生成频次和跨 seed 数保留为结果描述，不作为候选序列的硬性筛选门槛。** 这也避免了把同一生成模型产生的相关统计量误当成独立的生物学证据。

### 2. 进入筛选之前，明确序列长度和化学修饰的处理方式

目前 ProteinMPNN 实际设计的是 30 aa 肽链，而参考 Semaglutide 的聚合物序列有 31 个位置。

还需要明确两个问题：

- 缺失坐标的末端 Gly 应如何恢复到候选序列中，并保持所有序列的编号一致。
- 第 2 位 Aib 在设计时被近似为 Ala，后续序列比较和结构预测必须保留这一处理记录，不能把标准氨基酸序列直接当成完整的化学修饰肽。

尤其要注意：补回末端 Gly 是序列处理，不是结构建模；恢复一个字符并不会自动产生对应的三维坐标。

### 3. 先建立可审计的候选筛选表，再决定结构预测名单

当前有 1,435 条唯一序列。下一步应该以这些序列为基础，明确记录：

- 唯一序列 ID 和氨基酸序列；
- 序列长度、固定位置检查结果；
- ProteinMPNN `score` 的均值、中位数及标准差；
- 序列重复次数和跨 seed 数，作为辅助描述；
- 后续序列性质与结构评价结果。

不能只选最低 `score` 的若干条，也不应该仅凭最高频次选候选。筛选规则应在查看最终结构预测结果之前明确，减少事后挑选有利结果的风险。

## 三、下一步具体做什么？

我建议按照下面的顺序推进。

<list marker="number" gap={2}>
  <list-item>**核实唯一序列级汇总文件。** 确认评分聚合文件是否已经生成，以及 `count`、`n_seeds` 和各项评分统计是否齐全。</list-item>
  <list-item>**建立第一轮序列筛选规则。** 结合固定位置、序列完整性、重复性检查和理化性质，保留可追溯的筛选理由；不把生成频次或跨 seed 数设为硬门槛。</list-item>
  <list-item>**确定候选规模与结构预测协议。** 根据你的本地计算资源和可用软件，选择合理的候选数量，统一输入处理、预测参数和输出记录。</list-item>
  <list-item>**开展结构评价。** 分别考察预测结构置信度、肽—受体界面几何及与参考结构的差异，不把任何单一结构分数直接解释为激动活性。</list-item>
</list>

## 四、现在只需要确认一个问题

你的工作记录已经很完整，但它记录的最后一步仍然是初步评分分析和下一阶段计划。为了避免我让你重复运行已经完成的脚本，我想先确认当前文件实际进度。

**你现在是否已经生成了唯一序列级评分汇总 CSV？**

例如，是否已经有包含 `score_mean`、`score_median`、`score_std`、`global_score_mean`、`seq_recovery_mean`、`count` 和 `n_seeds` 等字段的文件？

如果已经生成，下一步就直接检查现有汇总表并进入候选筛选；如果尚未生成，我们先补齐这一步。无需重新生成那 10,000 条序列。

---

# you asked

message time: 2026-10-19 22:54:51

# GLP-1R 半胱素序列设计复现：候选筛选与多样性聚类工作记录

**日期：** 2026-10-19  
**项目：** GLP1R_reproduction  
**阶段：** ProteinMPNN 序列生成后的筛选、质量检查与代表序列选择  
**研究性质：** 计算方法复现与候选序列分析，尚无实验功能验证

---

## 一、阶段目标

本阶段承接 ProteinMPNN 序列生成与去重工作，对去重后的 GLP-1R 候选肽序列进行分阶段筛选、基础质量检查和序列多样性分析，最终建立一套可追溯的候选代表序列集合，供后续结构预测与评估使用。

本阶段主要回答三个问题：

1. 生成的候选序列中，有多少能够通过当前设定的 NEP-24.11 相关切割位点筛选？
2. 筛选后序列的长度、氨基酸组成及基础理化性质是否存在明显异常？
3. 如何在减少序列冗余的同时，保留具有一定序列差异的候选代表？

需要注意：序列生成、切割位点筛选和序列聚类均属于计算分析，不能单独证明候选肽具有 GLP-1R 结合能力、受体激动活性或药理学效果。

## 二、输入数据与上一阶段结果

### 2.1 ProteinMPNN 序列生成

参考复合物来自 PDB 7KI0，为 semaglutide 与 GLP-1R 的复合物结构。ProteinMPNN 输入结构为：

`structures/GLP1R_semaglutide_ProteinMPNN_input_renumbered.pdb`

已记录的模型与链设置：

- 模型：`v_48_020`
- 设计链：P，即肽链
- 固定链：R，即受体链
- 候选肽长度：30 个氨基酸
- FASTA 头信息记录的采样温度：`T=0.1`

检查了 `batch200_seed1` 至 `batch200_seed50` 共 50 个批次。每个批次包含 200 条生成候选，合计 10,000 条候选记录，不计每个 FASTA 中的参考序列记录。

跨批次去重后得到：

| 项目 | 结果 |
|---|---:|
| 生成候选记录 | 10,000 |
| 唯一序列 | 1,435 |
| 重复冗余记录 | 8,565 |
| 重复冗余比例 | 85.65% |

去重结果文件：

- `results/proteinmpnn/test_2000seq_renumbered/deduplicated/unique_candidates_all50_v2.fasta`
- `results/proteinmpnn/test_2000seq_renumbered/deduplicated/sequence_counts_all50_v2.csv`

已核实 FASTA 与 CSV 均包含 1,435 条唯一序列，CSV 中 `count` 列的总和为 10,000，FASTA 与 CSV 的唯一序列对应关系检查通过。

### 2.2 复现参数的已知限制

虽然 50 个批次的 FASTA 头信息与预期 seed、模型标识及链设置一致，但原始批量运行命令或完整运行脚本尚未找到。因此，`num_seq_per_target`、`batch_size` 等所有实际运行参数还不能完全独立核实。

这属于当前复现记录中的未解决问题，不应将输出文件头信息等同于完整的运行参数证明。

## 三、第一轮切割位点筛选

第一轮对 1,435 条唯一候选进行指定位置的切割位点筛查。

本轮检查的位点：

- EF：序列位置 21–22
- WL：序列位置 25–26

结果如下：

| 项目 | 序列数 |
|---|---:|
| 输入候选 | 1,435 |
| 保留 | 787 |
| 剔除 | 648 |

对应文件：

目录：`results/proteinmpnn/test_2000seq_renumbered/screening_step1_cleavage/`

- `retained_step1.fasta`
- `rejected_step1.fasta`
- `screening_step1_audit.csv`

本轮筛选记录了每条序列的处理结果，以便后续追溯保留与剔除情况。

需要说明的是，这一轮并未对所有论文提及的切割位点进行完整筛查，因此 787 条序列只能视为通过第一轮指定规则的候选，不能视为已经完成全部切割风险评估。

## 四、第二轮切割位点筛选

第二轮以第一轮保留的 787 条候选为输入，进一步检查以下位置：

| 位点 | 序列位置 | 本轮规则 |
|---|---|---|
| DV | 9–10 | 允许保留 |
| SY | 12–13 | 命中则剔除 |
| YL | 13–14 | 命中则剔除 |
| EF | 21–22 | 命中则剔除 |
| FI | 22–23 | 命中则剔除 |
| WL | 25–26 | 命中则剔除 |

筛选结果：

| 项目 | 序列数 |
|---|---:|
| 输入候选 | 787 |
| 保留 | 308 |
| 剔除 | 479 |

对应文件：

目录：`results/proteinmpnn/test_2000seq_renumbered/screening_step2_cleavage/`

- `screen_cleavage_step2.py`
- `retained_step2.fasta`
- `rejected_step2.fasta`
- `screening_step2_audit.csv`

筛选审计表记录了每条输入序列的判定结果，保留与剔除数量之和等于 787。

### 4.1 第二轮筛选后的质量检查

对 308 条保留序列进行了独立检查：

- 序列总数：308；
- 序列长度：全部为 30 aa；
- 非标准氨基酸：未发现；
- 重复序列：未发现；
- DV（9–10）：308/308；
- SY（12–13）：0/308；
- YL（13–14）：0/308；
- EF（21–22）：0/308；
- FI（22–23）：0/308；
- WL（25–26）：0/308。

因此，308 条候选与当前第二轮筛选规则及其预期输出一致。

## 五、DV 位点问题与复现差异

在对 10,000 条原始生成候选进行检查时，发现所有候选在序列第 10 位均为 V，即第 9–10 位均为 DV。

但已保存的固定位置配置中，肽链 P 的固定位置列表为：

`[1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 20, 28]`

其中没有第 10 位。与此同时，原始 ProteinMPNN 批量运行命令和完整运行参数尚未找到，因此目前无法确认这一现象究竟与实际运行配置、模型采样偏好或其他因素有关。

当前处理原则：

1. 将“10,000 条候选的第 10 位均为 V”记录为已观察到的结果。
2. 不将该现象直接解释为生物学保守性。
3. 不据此认定 ProteinMPNN 模型存在错误。
4. 将实际运行时的设计掩码与完整参数列为待核查问题。
5. 明确记录：本阶段筛选规则允许 DV，因此当前流程与将 DV 也纳入剔除的严格论文复现方案存在差异。

论文将 DV 列为潜在的 NEP-24.11 切割位点之一。若后续目标是严格复现论文的筛选策略，需要重新核对 DV 的处理依据，并保留不同筛选方案的独立结果，避免在没有明确依据时直接覆盖现有候选集。

相关记录：

- `logs/2026-10-19_DV_site_investigation.md`
- `logs/2026-10-19_proteinmpnn_generation.md`

## 六、基础理化性质分析

此前对第一轮保留的 787 条候选进行了基础理化性质统计。该分析用于描述序列集合的特征，不作为已经验证的生物学筛选阈值。

### 6.1 净电荷估计

基于近似 Henderson–Hasselbalch 方法估算 pH 7.4 下的净电荷：

| 统计量 | 结果 |
|---|---:|
| 平均值 | +0.752 |
| 中位数 | +0.836 |
| 最小值 | −2.161 |
| 最大值 | +3.835 |

其中，741/787 条候选的估算净电荷处于 −1 至 +2 之间，约占 94.2%。

这些数值是基于简化假设的计算估计，不代表实验测得的真实电荷，也不应直接作为候选活性或稳定性的判据。

### 6.2 平均疏水性

采用 Kyte–Doolittle 疏水性尺度进行描述性统计：

| 统计量 | 结果 |
|---|---:|
| 平均值 | −0.808 |
| 中位数 | −0.8067 |
| 第一四分位数 | −0.9367 |
| 第三四分位数 | −0.6850 |
| 最小值 | −1.2767 |
| 最大值 | −0.1967 |

### 6.3 简单疏水连续片段检查

对连续疏水残基片段和 7 aa 滑动窗口进行了初步统计：

- 最长连续 KD>0 片段为 4 aa，共有 7 条序列达到该长度；
- 未观察到长度不少于 5 aa 的连续 KD>0 片段；
- 79 条序列存在平均 KD 大于 1.0 的 7 aa 窗口；
- 最高窗口平均 KD 为 1.8143，对应片段 `AVKAFVA`，位于序列位置 18–24。

这些指标只能作为简单的疏水性代理指标，不能替代实验聚集倾向测试，也不能等同于 SAP 等经过特定定义的方法。

### 6.4 α 螺旋相关观察

基于近似的主链 φ/ψ 角度检查，参考肽在位置 2–19 和 22–27 附近呈现 α 螺旋区段特征。当前分析尚未通过 DSSP 等标准化方法完成正式二级结构确认，也未完整核实补充材料中的全部结构约束。

因此，不能仅根据 Pro/Gly 的出现情况判断候选序列能否保留参考肽的螺旋结构。

## 七、308 条候选的序列多样性分析

### 7.1 两两 Hamming 距离

对 308 条候选进行两两序列距离分析，共计：

$$
\frac{308 \times 307}{2}=47{,}278
$$

对序列而言，Hamming 距离表示对应位置上氨基酸不同的数量。由于本阶段所有候选长度均为 30 aa，可以直接比较对齐序列。

两两距离分布：

| Hamming 距离 | 序列对数 |
|---:|---:|
| 1 | 695 |
| 2 | 3,202 |
| 3 | 8,221 |
| 4 | 12,476 |
| 5 | 11,924 |
| 6 | 7,057 |
| 7 | 2,730 |
| 8 | 769 |
| 9 | 183 |
| 10 | 20 |
| 11 | 1 |

距离不超过 3 的序列对共有 12,118 对；距离不超过 5 的序列对共有 36,518 对。最大两两 Hamming 距离为 11。

这一结果显示，308 条候选中存在明显的近邻关系与一定程度的序列差异，但距离分布本身不能证明这些序列具有相同或不同的结构、结合模式或生物学功能。

### 7.2 聚类方法的选择

首先测试了 Hamming 距离阈值为 3 时的单链接连通分量方法，结果形成两个连通分量，其中一个包含 307 条序列，另一个包含 1 条序列。

该结果表明，单链接允许通过一系列近邻关系将差异较大的序列连接到同一分量中，因此不适合直接作为本项目的最终代表序列压缩方案。

随后测试了贪心完全连接分组。该方法对输入顺序较敏感：原始顺序、逆序和随机顺序下得到的簇数与最大簇大小均有所不同。因此，未将其作为最终主分析结果。

最终采用确定性的凝聚层次完全连接聚类（agglomerative hierarchical complete linkage），以 Hamming 距离 3 作为探索性切割阈值。

完全连接方法要求簇间合并距离由两簇成员之间的最大 Hamming 距离决定，因此切割后同一簇内任意两条序列的 Hamming 距离均不超过 3。

阈值 3 是为了探索序列冗余压缩效果而选择的参数，并非论文已经验证的生物学阈值。

## 八、完全连接聚类结果

### 8.1 方法与参数

- 输入：第二轮筛选后的 308 条候选序列；
- 序列长度：30 aa；
- 距离指标：Hamming 距离；
- 算法：凝聚层次完全连接聚类；
- 切割阈值：3；
- 合并平局处理：根据原始输入索引确定性处理；
- 代表序列：每个簇选取一个 medoid，即簇内到其他成员的 Hamming 距离总和最小的成员；
- medoid 平局处理：选择原始输入顺序更靠前的成员。

### 8.2 聚类结果

| 项目 | 结果 |
|---|---:|
| 输入候选数 | 308 |
| 聚类数 | 65 |
| 代表序列数 | 65 |
| 合并次数 | 243 |
| 最大簇大小 | 12 |
| 单成员簇数量 | 7 |
| 最大簇内直径 | 3 |

簇大小分布：

`{1: 7, 2: 5, 3: 18, 4: 8, 5: 5, 6: 5, 7: 3, 8: 5, 9: 3, 10: 5, 12: 1}`

聚类结果表明，在当前数据集、距离定义、切割阈值和确定性平局处理规则下，可以将 308 条候选压缩为 65 条代表序列。

这一步的目的在于降低后续评估的候选数量并保留一定的序列多样性，不代表 65 条序列优于其余候选，也不意味着不同簇在结构或功能上已经得到区分。

### 8.3 聚类输出文件

输出目录：

`results/proteinmpnn/test_2000seq_renumbered/clustering_complete_linkage_d3/`

包含以下文件：

- `cluster_complete_linkage.py`：聚类脚本；
- `medoids.fasta`：65 条代表序列；
- `cluster_membership.tsv`：308 条候选的簇归属、代表序列标记及相关距离信息；
- `cluster_summary.tsv`：每个簇的大小、代表序列及簇内距离统计；
- `clustering_run_info.md`：运行参数、输入校验和、结果、审计检查和方法限制。

聚类报告记录的输入 FASTA SHA-256 为：

`e09aaf1f54d036f62f9168e26454abcbff43f21b2977ba7150b4563dce4992f2`

该值用于确认本次聚类使用的输入文件版本。

### 8.4 审计结果

脚本运行完成，六项程序化审计全部通过：

1. 输入候选数量符合预期；
2. 所有候选均被分配到且仅分配到一个簇；
3. 所有簇的直径均不超过阈值 3；
4. 每个 medoid 都属于其对应簇；
5. 每个 medoid 均满足簇内距离总和最小的选择规则；
6. 65 条代表序列之间没有重复序列。

独立文件核对结果：

- `medoids.fasta`：65 条序列；
- `cluster_membership.tsv`：308 条数据记录；
- `cluster_summary.tsv`：65 条数据记录；
- `clustering_run_info.md`：包含方法、参数、输入校验和、结果与限制说明。

以上检查验证的是聚类流程的内部一致性与输出完整性，不是对候选肽生物学功能的验证。

## 九、当前阶段结论

截至本阶段结束，已完成以下工作：

1. 对 50 个 ProteinMPNN 批次共 10,000 条生成候选进行跨批次去重，得到 1,435 条唯一序列；
2. 完成两轮指定切割位点筛选，得到 308 条保留序列；
3. 检查保留序列的长度、氨基酸组成和切割位点筛选结果；
4. 对候选集合的基础理化性质和序列多样性进行了描述性分析；
5. 使用确定性的完全连接层次聚类将 308 条候选压缩为 65 条代表序列；
6. 保存聚类脚本、代表序列、成员关系、簇汇总与运行审计报告。

目前可以确认的是：**在已记录的输入和参数条件下，候选序列筛选与聚类流程已运行完成，输出通过了规定的程序化一致性检查。**

目前尚不能确认的是：65 条代表序列中哪些能够形成合理的 GLP-1R 结合构象、哪些能够激活受体，以及它们是否具有足够的稳定性或药理学潜力。

因此，65 条代表序列应被称为“用于后续评估的多样性压缩候选集”，而不是“已验证的功能性先导物”。

## 十、尚待解决的复现问题

后续工作应继续保留以下问题，不能因本阶段筛选与聚类完成而将其视为已经解决。

### 10.1 ProteinMPNN 原始运行命令与参数

原始批量运行命令或完整运行脚本尚未找到。尽管 FASTA 头信息可以支持部分元数据核对，仍需进一步确认实际运行时的完整参数与设计掩码。

### 10.2 DV 位点的处理

所有 10,000 条生成候选的第 10 位均为 V，而已保存的固定位置配置不包含第 10 位。该现象的原因尚未确定。

此外，当前第二轮筛选允许 DV，与将论文列出的全部潜在切割位点纳入筛选的严格复现方案存在差异。需要在后续记录中明确比较筛选规则，并保留现有结果。

### 10.3 原始筛选与去重脚本的完整可追溯性

当前已找到并保存第二轮切割位点筛选脚本与聚类脚本，但仍需核查原始去重、第一轮筛选以及 ProteinMPNN 批量生成阶段的完整脚本和运行命令是否均有可追溯记录。

对于尚未找到的文件，应标记为“未找到”或“尚未核实”，不应推测其内容或用新写的脚本冒充原始运行脚本。

### 10.4 论文筛选流程的一致性

当前筛选与聚类结果基于本项目已经执行并记录的规则。若后续需要更严格地复现论文中的筛选流程，应先核对补充材料中的具体规则，再明确记录差异及其影响，而不是将现有流程默认视为与论文完全一致。

## 十一、下一阶段建议

在开始大量结构预测之前，建议按以下顺序推进：

1. 保存当前 65 条代表序列及其簇归属，确保后续结构预测结果能回溯到原始 308 条候选；
2. 确认后续结构预测工具、输入格式、链标识、运行参数与输出命名规则；
3. 为每条代表序列建立稳定的候选 ID，并将候选 ID、原始序列、簇 ID、结构预测文件和后续评价指标关联起来；
4. 在结构评价阶段记录实际使用的结构置信度与界面指标，避免仅凭单一指标认定候选优劣；
5. 将所有计算预测结论与实验验证结论明确区分；
6. 在适当时机补齐原始生成命令、去重脚本、第一轮筛选脚本及相关运行记录的可追溯性。

**本阶段最终产物：** 308 条经过当前筛选规则的候选序列，以及 65 条用于后续结构与界面评估的代表序列。所有结论均限于已执行的计算分析和程序化审计范围。
# 工作记录：从已验证候选物反推筛选逻辑

**日期：2026-10-19**

## 1. 思路转折

此前的工作主要围绕 ProteinMPNN 生成的 10,000 条序列展开，完成去重、两轮酶切位点筛选，并对 DV 位点在所有生成序列中的一致性进行了排查。

目前已知：10,000 条生成序列在第 10 位均为 V，但现有固定位置配置未列出该位点，且原始生成命令与实际运行时配置尚未找到。因此，DV 现象的原因仍未确定，也不能据此认定其为生物学规律或模型错误。

考虑到论文已报告 D13、D41、D44 经过结合与细胞功能实验验证，并进一步开展了药代动力学及小鼠药效研究，后续研究调整方向：**先以这些经过实验验证的候选序列为参考，尝试反推论文的计算筛选逻辑。**

## 2. 新的研究问题

我们已有 D13、D41、D44 的候选序列信息。它们能否作为参考锚点，帮助我们回答：

- 这三条序列分别具有哪些序列特征？
- 它们在酶切位点、净电荷、疏水性、SAP 及结构相关指标上有什么共同点和差异？
- 这些特征能否帮助识别论文筛选指标的可能作用，以及哪些规则可以从论文方法或补充材料中得到直接确认？
- DV 位点应如何理解：它是固定的功能相关位置、潜在酶切位点，还是当前复现流程中尚未正确对齐的筛选规则？

需要注意：三条成功候选物只能提供有限的正向参考，不能单独确定论文的全部筛选阈值，也不能证明某个共同特征就是候选成功的原因。

## 3. 后续工作安排

1. **核实参考序列。** 从论文及补充材料中确认 D13、D41、D44 的准确序列、长度和残基编号，并与当前 30 aa 坐标支持序列及 31 aa 论文序列统一对齐。
2. **建立参考特征表。** 记录三条序列的酶切位点、净电荷、疏水性、SAP 及可获得的结构评价结果；区分论文明确规定的条件与我们自行提出的假设。
3. **回到 1,435 条去重序列。** 以论文实际方法为依据，重新整理初筛流程。对缺少明确阈值或无法复现的指标，单独标注，不擅自补造论文参数。
4. **重新审视 DV 问题。** 核对 D15–V16 的残基编号、论文固定位置与酶切筛选规则，以及参考候选序列中的实际残基。只有在这些信息核实后，才决定如何处理 DV。
5. **保留可审计记录。** 原始序列、此前两轮筛选结果及相关脚本均保留；新的初筛作为独立版本开展，记录输入、规则、输出和数量变化。

## 4. 当前结论

本阶段不是直接宣称已还原论文筛选算法，而是将研究重心从单个位点异常排查转向**以实验验证候选物为参考、以论文方法为依据的筛选流程重建**。

后续目标是从 1,435 条去重序列重新开始初筛，并明确区分论文已证实的规则、当前复现的实现方式和仍待验证的假设。

---

# chatgpt response

我已经接上这份工作记录。接下来我们以 **GLP1R_reproduction 的论文筛选逻辑重建** 为主线，而不是直接沿用此前的 308 条候选或 65 条代表序列作为最终筛选结果。

当前最重要的变化是：从 D13、D41、D44 这三条经过实验验证的候选序列出发，先核实论文证据与残基编号，再回到 1,435 条去重序列，独立重建筛选流程。

## 当前工作状态

| 工作项 | 状态 | 后续处理 |
|---|---|---|
| ProteinMPNN 生成与跨批次去重 | 已完成 | 保留 1,435 条唯一序列及审计文件 |
| 原有两轮切割位点筛选 | 已完成 | 保留结果，但不视为最终论文复现筛选 |
| 308 条候选的质量检查 | 已完成 | 作为既有分析记录 |
| 65 条代表序列的完全连接聚类 | 已完成 | 供后续参考，不直接替代新筛选 |
| D13、D41、D44 参考序列核实 | 待开展 | 核实准确序列、长度与编号 |
| 30 aa 与 31 aa 坐标对齐 | 待开展 | 统一残基映射，重点核对 DV |
| 论文筛选规则重建 | 待开展 | 区分论文明确规定、已实现规则与待验证假设 |
| 新版初筛 | 待开展 | 从 1,435 条序列重新执行 |

## 我们接下来遵守的原则

1. **先核实证据，再写代码。** 不根据 D13、D41、D44 的结果猜测论文阈值。
2. **DV 问题单独审计。** 不把所有候选第 10 位均为 V 的现象直接解释为模型偏好或生物学规律。
3. **保留旧结果，建立新版本。** 新筛选使用独立目录和审计记录，不覆盖原有的 787、308 或 65 条结果。
4. **不把预测当成实验结论。** 序列特征与结构指标只能提供计算证据，不能单独证明结合能力或受体激动活性。
5. **保持来源可追溯。** 论文原文、补充材料、实际运行参数和我们自行提出的假设分别记录。

## 下一步：先核实 D13、D41、D44

我建议先从已有的论文、补充材料和项目文件中找到三条参考序列及其筛选方法依据，完成以下核对：

- 三条序列的准确氨基酸序列与长度；
- 论文采用的残基编号与当前 30 aa 输入序列之间的映射；
- NEP-24.11 相关切割位点的原文规则；
- SAP、净电荷、疏水性和结构约束中，哪些是论文明确使用的筛选条件；
- D13、D41、D44 在 DV 位点及其他相关位点上的实际情况。

**我们不急着重跑 1,435 条序列。** 先建立一份有论文依据的规则表，再实现独立的初筛脚本，这样才能判断新流程究竟复现了哪些内容、与旧流程有什么差异。

如果你准备继续操作本地项目，下一步可以先检查已有的论文 PDF、补充材料和相关序列文件；我会根据实际文件内容带你逐项核对，不假定任何尚未找到的文件或参数已经存在。

---

# you asked

message time: 2026-10-19 22:55:25

Table S1. GLP-1RAs sequences for biosynthesis and chemical synthesis
ID	Biosynthesis	Chemical synthesis
	Protein Sequences	Affinity tag	Linker	GST-Linker-Peptide	DNA of Linker-Peptide	Protein Sequences
Semaglutide	HAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG	GST	GGDDDDK	MSPILGYWKIKGLVQPTRLLLEYLEEKYEEHLYERDEGDKWRNKKFELGLEFPNLPYYIDGDVKLTQSMAIIRYIADKHNMLGGCPKERAEISMLEGAVLDIRYGVSRIAYSKDFETLKVDFLSKLPEMLKMFEDRLCHKTYLNGDHVTHPDFMLYDALDVVLYMDPMCLDAFPKLVCFKKRIEAIPQIDKYLKSSKYIAWPLQGWQATFGGGDHPPKSDLVPRGSGGDDDDKHAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG	GGAGGGGATGATGACGATAAACACGCCGAGGGAACATTCACGTCTGATGTTTCATCCTACCTGGAAGGACAGGCGGCAAAAGAGTTTATTGCCTGGCTTGTTCGCGGCCGCGGCtaatag	H-Aib-EGTFTSDVSSYLEGQAAK(AEEA-AEEA-γE-C18Diacid)EFIAWLVRGRG-COOH
D13	HAEGTFTSDVSSYLEEQAAKAFVERLKRGRG	GST	GGDDDDK	MSPILGYWKIKGLVQPTRLLLEYLEEKYEEHLYERDEGDKWRNKKFELGLEFPNLPYYIDGDVKLTQSMAIIRYIADKHNMLGGCPKERAEISMLEGAVLDIRYGVSRIAYSKDFETLKVDFLSKLPEMLKMFEDRLCHKTYLNGDHVTHPDFMLYDALDVVLYMDPMCLDAFPKLVCFKKRIEAIPQIDKYLKSSKYIAWPLQGWQATFGGGDHPPKSDLVPRGSGGDDDDKHAEGTFTSDVSSYLEEQAAKAFVERLKRGRG	GGAGGGGATGATGACGATAAACACGCCGAGGGAACATTCACGTCTGATGTTTCATCCTACCTGGAAGAACAGGCGGCAAAAGCGTTTGTGGAACGCCTTAAACGCGGCCGCGGCtaatag	H-Aib-EGTFTSDVSSYLEEQAAK(AEEA-AEEA-γE-C20Diacid)AFVERLKRGRG-COOH
D41	HAEGTFTSDVSSYLEEQQVKQFVERLKRGRG	GST	GGDDDDK	MSPILGYWKIKGLVQPTRLLLEYLEEKYEEHLYERDEGDKWRNKKFELGLEFPNLPYYIDGDVKLTQSMAIIRYIADKHNMLGGCPKERAEISMLEGAVLDIRYGVSRIAYSKDFETLKVDFLSKLPEMLKMFEDRLCHKTYLNGDHVTHPDFMLYDALDVVLYMDPMCLDAFPKLVCFKKRIEAIPQIDKYLKSSKYIAWPLQGWQATFGGGDHPPKSDLVPRGSGGDDDDKHAEGTFTSDVSSYLEEQQVKQFVERLKRGRG	GGAGGGGATGATGACGATAAACACGCCGAGGGAACATTCACGTCTGATGTTTCATCCTACCTGGAAGAACAGCAGGTGAAACAGTTTGTGGAACGCCTTAAACGCGGCCGCGGCtaatag	H-Aib-EGTFTSDVSSYLEEQQVK(AEEA-AEEA-γE-C20Diacid)QFVERLKRGRG-
D44	HAEGTFTSDVSRYLEEKAVKDFVERLKRGAG	GST	GGDDDDK	MSPILGYWKIKGLVQPTRLLLEYLEEKYEEHLYERDEGDKWRNKKFELGLEFPNLPYYIDGDVKLTQSMAIIRYIADKHNMLGGCPKERAEISMLEGAVLDIRYGVSRIAYSKDFETLKVDFLSKLPEMLKMFEDRLCHKTYLNGDHVTHPDFMLYDALDVVLYMDPMCLDAFPKLVCFKKRIEAIPQIDKYLKSSKYIAWPLQGWQATFGGGDHPPKSDLVPRGSGGDDDDKHAEGTFTSDVSRYLEEKAVKDFVERLKRGAG	GGAGGGGATGATGACGATAAACACGCCGAGGGAACATTCACGTCTGATGTTTCACGCTACCTGGAAGAAAAAGCGGTGAAAGATTTTGTGGAACGCCTTAAACGCGGCGCGGGCtaatag	H-Aib-EGTFTSDVSRYLEEKAVK(AEEA-AEEA-γE-C20Diacid)DFVERLKRGAG-COOH

---

# chatgpt response

很好，这份 Table S1 已经能作为 D13、D41、D44 的序列核对依据。我们可以先得到一个关键结果：**三条实验验证候选并不共享完全相同的序列模式，因此应该用它们检查筛选规则是否合理，而不是从三条序列直接推导硬性阈值。**

## 1. 核对三条参考序列

根据你贴出的 Table S1，三条 Biosynthesis 序列均为 30 aa，与当前 ProteinMPNN 使用的 30 aa 坐标支持序列长度一致。

| ID | 序列 | 长度 | 第 9–10 位 |
|---|---|---:|---|
| D13 | `HAEGTFTSDVSSYLEEQAAKAFVERLKRGRG` | 30 aa | DV |
| D41 | `HAEGTFTSDVSSYLEEQQVKQFVERLKRGRG` | 30 aa | DV |
| D44 | `HAEGTFTSDVSRYLEEKAVKDFVERLKRGAG` | 30 aa | DR |

三个序列可作为后续计算分析的参考锚点。不过，它们在 Table S1 中的 Biosynthesis 序列，并不等同于 Chemical synthesis 栏中的完整化学结构：化学合成版本还包含 Aib、连接臂及脂肪二酸修饰等信息。

因此，我们应当分开保存两种表示：

- **标准氨基酸序列**：用于序列比对、切割位点检查和 ProteinMPNN 候选比较。
- **化学修饰信息**：用于解释实际合成分子与标准序列表示之间的区别。

## 2. 这三条序列对筛选逻辑有什么启示？

<box border radius="lg" padding={3} gap={3}>
  <box gap={1}>
    **发现一：DV 不是三条候选共同具有的模式**

    D13、D41 在第 9–10 位为 DV，D44 则为 DR。D44 同样是论文报告的实验研究候选。

    因此，不能把“第 10 位必须为 V”作为所有成功候选的必要条件。至于 DV 是否属于论文明确规定要剔除的潜在酶切位点，仍需依据方法原文核对。
  </box>
  <divider color="subtle"/>
  <box gap={1}>
    **发现二：部分位置存在明显差异**

    D13、D41、D44 在第 12–14 位、约第 18–24 位及 C 端附近均有差异。说明我们不能简单要求所有候选保留 Semaglutide 的完整局部序列。
  </box>
  <divider color="subtle"/>
  <box gap={1}>
    **发现三：不能仅凭三条阳性候选确定筛选阈值**

    三条序列可用于检查规则是否会误删已知候选，但仅凭它们不能估计筛选规则的特异性，也不能证明保留的序列具有相同功能。
  </box>
</box>

## 3. 对原有筛选流程的直接影响

此前两轮筛选将 1,435 条序列缩减到 308 条，其中第二轮明确允许 DV，并检查 SY、YL、EF、FI、WL 等模式。

现在应增加一项重要审计：**用 D13、D41、D44 作为参考锚点，逐条运行旧筛选规则，记录每条序列是否会被保留以及具体原因。**

这只是规则审计，不是立即重跑全部候选。它可以帮助我们判断：

- 旧规则是否会误删已知参考候选；
- 不同规则分tep1_audit.csv

  echo
  echo "===== STEP 2 AUDIT HEADER ====="
  head -n 1 results/proteinmpnn/test_2000seq_renumbered/screening_step2_cleavage/screening_step2_audit.csv
}
```

把输出贴给我。接下来我会先根据真实代码确认旧规则的具体行为，再结合论文方法核实结果，避免在证据不足时自行补造筛选阈值。

---

# you asked

message time: 2026-10-19 22:56:02

(proteinmpnn) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH cd LOCAL_PATH && {
  echo "===== STEP 2 SCREENING SCRIPT ====="
  cat results/proteinmpnn/test_2000seq_renumbered/screening_step2_cleavage/screen_cleavage_step2.py

  echo
  echo "===== STEP 1 AUDIT HEADER ====="
  head -n 1 results/proteinmpnn/test_2000seq_renumbered/screening_step1_cleavage/screening_step1_audit.csv

  echo
  echo "===== STEP 2 AUDIT HEADER ====="
  head -n 1 results/proteinmpnn/test_2000seq_renumbered/screening_step2_cleavage/screening_step2_audit.csv
}
===== STEP 2 SCREENING SCRIPT =====
#!/usr/bin/env python3
import csv
from pathlib import Path
from Bio import SeqIO

ROOT = Path("LOCAL_PATH")
INPUT = ROOT / "results/proteinmpnn/test_2000seq_renumbered/screening_step1_cleavage/retained_step1.fasta"
OUTDIR = ROOT / "results/proteinmpnn/test_2000seq_renumbered/screening_step2_cleavage"

# Positions are 1-based and specific to the 30-aa candidate sequence.
# DV is intentionally exempt from rejection.
SITES = {
    "DV": (9, 10),
    "SY": (12, 13),
    "YL": (13, 14),
    "EF": (21, 22),
    "FI": (22, 23),
    "WL": (25, 26),
}
REJECT_SITES = ["SY", "YL", "EF", "FI", "WL"]

def motif_at(seq, positions):
    start, end = positions
    return seq[start - 1:end]

records = list(SeqIO.parse(INPUT, "fasta"))
if not records:
    raise SystemExit(f"No FASTA records found: {INPUT}")

kept = []
rejected = []
audit_rows = []

for rec in records:
    seq = str(rec.seq).upper()
    if len(seq) != 30:
        raise ValueError(f"Unexpected length: {rec.id}, {len(seq)}")

    observed = {site: motif_at(seq, pos) for site, pos in SITES.items()}
    hits = [
        site for site in REJECT_SITES
        if observed[site] == site
    ]
    dv_hit = observed["DV"] == "DV"

    row = {
        "sequence_id": rec.id,
        "sequence": seq,
        "length": len(seq),
        "DV_pos9_10": observed["DV"],
        "SY_pos12_13": observed["SY"],
        "YL_pos13_14": observed["YL"],
        "EF_pos21_22": observed["EF"],
        "FI_pos22_23": observed["FI"],
        "WL_pos25_26": observed["WL"],
        "DV_present": dv_hit,
        "rejection_hits": ";".join(hits),
        "decision": "REJECT" if hits else "KEEP",
        "reason": (
            "Contains non-DV cleavage site(s): " + ";".join(hits)
            if hits else "No specified non-DV cleavage sites"
        ),
    }
    audit_rows.append(row)

    if hits:
        rejected.append(rec)
    else:
        kept.append(rec)

OUTDIR.mkdir(parents=True, exist_ok=True)
with (OUTDIR / "retained_step2.fasta").open("w") as f:
    SeqIO.write(kept, f, "fasta")
with (OUTDIR / "rejected_step2.fasta").open("w") as f:
    SeqIO.write(rejected, f, "fasta")

with (OUTDIR / "screening_step2_audit.csv").open(
    "w", newline="", encoding="utf-8"
) as f:
    writer = csv.DictWriter(f, fieldnames=list(audit_rows[0].keys()))
    writer.writeheader()
    writer.writerows(audit_rows)

print("=== 第二轮切割位点筛选 ===")
print("输入候选:", len(records))
print("保留:", len(kept))
print("淘汰:", len(rejected))
print("数量核对:", len(kept) + len(rejected) == len(records))
print("\n=== 各非 DV 位点命中数（允许重叠）===")
for site in REJECT_SITES:
    count = sum(row[site + "_pos" + "_unused"] == site for row in []) if False else sum(
        row[{
            "SY": "SY_pos12_13",
            "YL": "YL_pos13_14",
            "EF": "EF_pos21_22",
            "FI": "FI_pos22_23",
            "WL": "WL_pos25_26",
        }[site]] == site for row in audit_rows
    )
    print(f"{site}: {count}")
print("\n输出目录:", OUTDIR)
print("原始第一轮结果未修改。")

===== STEP 1 AUDIT HEADER =====
sequence,length,position_21_22,position_25_26,result,rejection_reason,count,first_seed,first_candidate,all_sources

===== STEP 2 AUDIT HEADER =====
sequence_id,sequence,length,DV_pos9_10,SY_pos12_13,YL_pos13_14,EF_pos21_22,FI_pos22_23,WL_pos25_26,DV_present,rejection_hits,decision,reason
(proteinmpnn) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH

---

# chatgpt response

这份输出已经把旧筛选流程的关键行为确认下来了。我们现在可以从“怀疑 DV 规则是否处理正确”推进到更具体的**筛选规则审计**，而且暂时不需要运行新筛选或修改任何文件。

## 一、从真实脚本确认的事实

### 第二轮筛选实际做了什么

脚本 `screen_cleavage_step2.py` 明确设置：

- 输入：第一轮保留的 787 条序列；
- 检查位置：DV（9–10）、SY（12–13）、YL（13–14）、EF（21–22）、FI（22–23）、WL（25–26）；
- **剔除规则只包括 SY、YL、EF、FI、WL；DV 被明确豁免。**
- 任意一个被列入剔除规则的位点命中，就淘汰该序列。

因此，308 条保留序列不是“通过了所有六个位点的切割风险筛查”，而是“通过了当前脚本指定的五类非 DV 位点筛查”。

第一轮审计表的列名则显示，它只记录位置 21–22 和 25–26 的结果。由于我们尚未看到第一轮实际筛选脚本，当前只能确认其审计字段，不能单凭表头完整还原所有实现细节。

## 二、发现了一个比 DV 单个位点更重要的问题

我对照了你提供的 Table S1 和论文正文，发现需要先纠正我上一条回答中的两处错误：**D13、D41、D44 都是 31 aa，而不是 30 aa；D44 的第 9–10 位也是 DV，不是 DR。** 抱歉，上一条的序列长度和位点判断有误。

按 Table S1 的 Biosynthesis 序列重新逐位核对，结果如下。

| 参考序列 | 长度 | DV（9–10） | SY（12–13） | YL（13–14） |
|---|---:|---|---|---|
| Semaglutide | 31 aa | 命中 | 命中 | 命中 |
| D13 | 31 aa | 命中 | 命中 | 命中 |
| D41 | 31 aa | 命中 | 命中 | 命中 |
| D44 | 31 aa | 命中 | 未命中 | 命中 |

这里的位点编号均为完整 31 aa 序列的 **1-based 序列位置**。

论文正文确实将 DV、SY、YL、EF、FI、WL 列为 NEP-24.11 的六个潜在切割位点，并称过滤了含有这些位点的序列。citeturn412212search0

这就产生了一个必须认真核实的矛盾：

- 按照六种二肽模式的字面含义，D13、D41、D44 都会因为 DV 和 YL 被剔除。
- D13、D41、D44 却又是论文报告经过结合及 cAMP 功能实验的候选物。citeturn412212search0
- Semaglutide 参考序列本身也包含这六种模式。如果按完全相同的字面规则处理它，也会被剔除。

**因此，目前不能直接把“论文列出了六种潜在切割位点”翻译成“按六个二肽模式逐字匹配并全部剔除”。** 我们需要查清论文的实际筛选实现，或者确认正文是否省略了重要条件。

## 三、旧脚本与论文方法之间的差异

| 项目 | 当前项目实现 | 论文正文的表述 |
|---|---|---|
| EF、WL | 第一轮检查 | 列为潜在切割位点 |
| SY、YL、FI | 第二轮检查并剔除 | 列为潜在切割位点 |
| DV | 第二轮检查，但明确允许保留 | 列为潜在切割位点 |
| 是否与实验参考候选一致 | 尚未核对规则整体影响 | D13、D41、D44 已被实验研究 |

这张表只比较现有脚本与正文的表述，尚不代表已经确定论文实际执行了哪一种规则。

还有一个值得记录的数据差异：论文正文报告去重后得到 **1,443 条唯一序列**，而你的项目得到 **1,435 条**。citeturn412212search0 这可能来自输入、运行参数、去重口径或其他流程差异，目前不能确定原因。

## 四、下一步先查什么

我建议先不运行新的筛选，而是查看项目中已有的论文资料和补充材料，重点寻找：

1. 六个潜在切割位点的原始描述与筛选条件；
2. 虚拟筛选流程图中各阶段的候选数量；
3. SAP、净电荷和疏水性筛选的实际定义；
4. 是否存在正文未展开的额外条件或例外处理。

如果本地没有完整补充材料，我们再从出版方提供的 Supporting Information 核实。出版方页面列有补充材料文件，包括 `advs71185-sup-0001-SuppMat.docx` 和 `advs71185-sup-0002-DataFile.zip`。citeturn412212search1

当前最重要的结论是：**先不要用六个二肽模式直接重筛 1,435 条序列。** 如果机械套用这些模式，已知实验候选会被规则排除，说明我们还没有充分理解论文的筛选流程。先把这一矛盾查清楚，才能可靠地重建新版筛选规则。