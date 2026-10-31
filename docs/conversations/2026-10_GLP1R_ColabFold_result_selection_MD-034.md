> From: https://chatgpt.com/c/<UUID>

# you asked

message time: 2026-10-21 22:20:36

那你觉得界面相关指标应该怎么设置阈值

---

# you asked

message time: 2026-10-21 23:46:11

ipTM和pTM有什么区别

---

# chatgpt response

**一句话区别：pTM 看“整体结构预测得怎么样”，ipTM 看“不同链之间的相对位置预测得怎么样”。**

对于你目前的 GLP1R 项目——384 aa 的受体胞外结构与 31 aa 的候选肽组成的复合物——如果目的是筛选值得进一步验证的候选，**ipTM 通常比 pTM 更值得优先关注**，但二者都不能直接证明真实结合。

## 1. 两个指标分别在衡量什么？

<box gap={3}>
  <row align="start" gap={3}>
    <AsyncImage query="protein structure single chain ribbon folding 3D molecular structure" aspectRatio="4:5" maxWidth="124px" />
    <box flex="1" gap={1}>
      <title size="lg">pTM</title>
      <text color="secondary" size="sm">Predicted Template Modeling score</text>
      **整体结构的拓扑与相对位置置信度**

      主要反映预测模型能否较好地恢复整体蛋白结构及其空间布局。它关注整个复合物的结构，不专门针对肽与受体之间的界面。

      <text color="secondary" size="sm">局限：受体本身结构置信度较高，可能使整体指标显得不错，但这不代表候选肽的结合姿势正确。</text>
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <AsyncImage query="protein protein complex two molecular chains binding interface ribbon structure" aspectRatio="4:5" maxWidth="124px" />
    <box flex="1" gap={1}>
      <title size="lg">ipTM</title>
      <text color="secondary" size="sm">Interface predicted Template Modeling score</text>
      **不同链之间相对排布的置信度**

      在多链复合物中，它更关注链与链之间的相对位置是否有较好的预测支持。因此，更直接关联到你想评估的 GLP1R—候选肽复合物构象。

      <text color="secondary" size="sm">局限：高 ipTM 仍不等于真实结合，也不直接代表结合亲和力或受体激动活性。</text>
    </box>
  </row>
</box>

## 2. 放到你的 GLP1R 筛选中，应该怎样解读？

| pTM | ipTM | 对候选的初步解释 |
|---|---|---|
| 高 | 高 | 整体结构和链间排布都有较好的预测支持，值得进一步检查界面 |
| 高 | 低 | 整体结构可能可信，但链间相对排布缺乏足够支持 |
| 低 | 高 | 链间排布的预测支持较好，但仍需检查整体结构是否存在问题 |
| 低 | 低 | 当前预测对整体结构及链间排布的支持都较弱 |

这些只是解释框架，不是经过 GLP1R 阳性、阴性对照校准的分类规则。

### 3. 那么，阈值应该设多少？

我不建议直接规定“ipTM 大于 0.8 就入围”或“pTM 大于 0.7 才合格”。这些数值不能脱离模型类型、预测设置和具体任务，直接作为真实结合的判定标准。

对你这 241 条候选，我会这样处理：

- **ipTM：** 作为主要参考指标之一，但与界面相关指标共同评估。
- **pTM：** 作为辅助质量信息，不建议用它单独淘汰候选。
- **ipSAE、pDockQ2：** 用来补充界面证据，检查高 ipTM 是否也得到其他指标支持。
- **结构检查：** 对入围候选进一步查看接触位置、空间冲突以及肽的结合姿势是否合理。

尤其需要注意：你目前的受体与候选肽长度相差较大，整体 pTM 可能受到较大的受体结构部分影响。因此，**不应因为某条候选的 pTM 高，就认为它比 ipTM 略低但界面证据更一致的候选更好。**

我的建议是先画出 241 条候选的 ipTM 与 pTM 分布，并观察高 ipTM 候选是否同时具备较好的 ipSAE 和 pDockQ2，再根据实际分布讨论阈值，而不是先套用固定数字。

---

# you asked

message time: 2026-10-22 08:33:11

这是我经过一轮主观筛选后剩下的candidate，现在你直接开始聚类工作就行了，以下是筛选过程，虽然没有什么科学依据，但还是应该记录**WorkBuddy**

完成。D13/D44 的参照值直接从候选表的 `mapping` 列定位到（candidate_0165=D13、candidate_0173=D44，两者都在保留表中），对删除表 180 行逐条比对六项 mean 指标，**入选 49 行**，新表已生成。

## 参照值（mean）

| **指标**           | **D13 (candidate_0165)** | **D44 (candidate_0173)** |
| :--------------- | :----------------------- | :----------------------- |
| pLDDT_mean       | 88.369679                | 86.629341                |
| ipTM_mean        | 0.83                     | 0.816667                 |
| ipSAE_B-A_mean   | 0.604593                 | 0.572254                 |
| pDockQ_mean      | 0.5207                   | 0.5137                   |
| pDockQ2_A-B_mean | 0.343267                 | 0.246933                 |
| pDockQ2_B-A_mean | 0.300733                 | 0.2867                   |

## 结果

| **项目**                           | **数值**        |
| :------------------------------- | :------------ |
| 删除表总数                            | 180           |
| **入选（任意一项超过 D13 或 D44）**&#x200B; | **49**        |
| 其中超过 D13 的                       | 10（均同时超过 D44） |
| 仅超过 D44 的                        | 39            |

**各指标超过次数**（按参考拆分，行间可重叠）：

| **指标**           | **>D13** | **>D44** |
| :--------------- | :------- | :------- |
| pLDDT_mean       | 0        | **37**   |
| pDockQ_mean      | **10**   | 28       |
| pDockQ2_A-B_mean | 0        | 19       |
| ipSAE_B-A_mean   | 0        | 7        |
| pDockQ2_B-A_mean | 1        | 6        |
| ipTM_mean        | 0        | 3        |

两个值得注意的点：**D13 的标杆很高**——pLDDT（88.37）、ipTM（0.83）、ipSAE_B-A（0.605）、pDockQ2_A-B（0.343）四项无人超过，只有 pDockQ（10 个）和 pDockQ2_B-A（1 个）被越过；而 **D44 的门槛相对更容易越过**，49 个入选者全部超过 D44 的至少一项，其中 37 个胜在 pLDDT——这批候选多是结构置信度高、但栽在 ipTM/pDockQ/ipSAE 上的“偏科生”。

新表 `candidate_metrics_removed_exceeds_D13_D44.csv`（49 行）保留原列 + 删除原因列，另加了两列：**超过项数**（超过几项）和**超过明细**（如 `pLDDT_mean>D44; pDockQ_mean>D13+D44`），可直接按超过项数排序挑候选。“超过”按严格大于处理，超过任一参考即入选。

查看所有产物 (21)

svg

svgsvg

svg

svg

svg

svg

把超过项数大于等于4的合并到保留表里面，然后删掉除保留表以外的表

svg**WorkBuddy**

完成。保留表现 **67 行**，其他表已清理。

## 合并情况

超过项数分布：1 项 ×20、2 项 ×15、3 项 ×8、**4 项 ×4、5 项 ×2**——≥4 项的共 **6 个**，已全部合并进保留表（61 → 67 行，按候选 ID 重排，无重复）：

| **候选**         | **超过项数** | **超过明细**                                                              |
| :------------- | :------- | :-------------------------------------------------------------------- |
| candidate_0032 | 5 项      | pLDDT>D44; ipTM>D44; pDockQ>D13+D44; pDockQ2_A-B>D44; pDockQ2_B-A>D44 |
| candidate_0068 | 5 项      | 同上（5 项全超）                                                             |
| candidate_0018 | 4 项      | pLDDT>D44; pDockQ>D13+D44; pDockQ2_A-B>D44; pDockQ2_B-A>D44           |
| candidate_0097 | 4 项      | pLDDT>D44; pDockQ>D13+D44; pDockQ2_A-B>D44; pDockQ2_B-A>D13+D44       |
| candidate_0194 | 4 项      | pLDDT>D44; pDockQ>D13+D44; pDockQ2_A-B>D44; pDockQ2_B-A>D44           |
| candidate_0232 | 4 项      | pLDDT>D44; pDockQ>D13+D44; pDockQ2_A-B>D44; pDockQ2_B-A>D44           |

这 6 个的备注列已注明“自删除表恢复：超过D13/D44参照 N 项（明细）”，恢复来源可追溯。0032 和 0068 最强——五项全超 D44，其中 pDockQ 还超过 D13。

## 清理情况

已删除：`candidate_metrics_final_removed.csv`（180 行删除表）、`candidate_metrics_removed_exceeds_D13_D44.csv`（49 行提取表）。

目录现在只剩：

- **保留表** `candidate_metrics_final_kept.csv`（67 行）——唯一交付表
- **原文件** `candidate_metrics_merged_sorted.csv`（241 行全量）
- 你的研究材料（PK 数据 PDF×4、补充材料 docx、source data.xlsx、阶段一\~九等 txt）

一点说明：原文件我按上轮“原文件”的口径保留了未删（它是全量数据源，删了无法从保留表重建）。如果这个也要删，说一声即可。

---

# chatgpt response

我已经直接对你上传的 `candidate_metrics_final_kept.csv` 中的 **67 条保留候选序列**完成了第一轮聚类。表中包含完整的 31 aa 序列，因此这一步不需要依赖之前手动粘贴的 FASTA，也没有改动你的原始文件。

## 一、聚类结果

<box border radius="lg" padding={4} gap={3}>
  <row align="center" justify="between">
    <text color="secondary" size="sm">参与聚类的候选</text>
    <title size="xl" color="default">67</title>
  </row>
  <divider color="subtle" />
  <row align="center" justify="between">
    <text color="secondary" size="sm">主方案聚类数</text>
    <title size="xl" color="default">16</title>
  </row>
  <divider color="subtle" />
  <row align="center" justify="between">
    <text color="secondary" size="sm">最大类群</text>
    <title size="xl" color="default">9 条</title>
  </row>
  <text color="secondary" size="sm">方法：31 aa 等长序列的氨基酸逐位比较，采用完全连接层次聚类（complete linkage）。</text>
</box>

### 采用的主方案

我暂时将**同一类群内任意两条序列最多相差 3 个氨基酸**作为聚类条件，即序列一致性至少为 $28/31 \approx 90.3\%$。

这不是经过生物学实验校准的通用阈值，而是适合当前短肽候选池的第一版操作标准。选择完全连接而不是简单的连通分组，是为了避免 A 接近 B、B 接近 C，就把彼此差异其实较大的 A 和 C 强行合并。

我还做了阈值敏感性检查：

| 最多允许的两两差异 | 最低序列一致性 | 聚类数 |
|---:|---:|---:|
| 2 个氨基酸 | 93.5% | 24 |
| **3 个氨基酸（主方案）** | **90.3%** | **16** |
| 4 个氨基酸 | 87.1% | 9 |

这说明聚类数量确实会随阈值明显变化。现阶段建议以 16 个类群作为讨论和挑选代表序列的工作版本，同时保留严格阈值结果供复核。

## 二、16 个类群及成员

这里的“代表序列”先按**类群中心序列（medoid）**确定：即与同类其他序列总体差异较小的候选。它不是结构得分最高者，也不代表生物学活性最好。

| 类群 | 数量 | 中心代表候选 | 成员 |
|---|---:|---|---|
| C01 | 9 | candidate_0031 | 0009、0029、0031、0058、0086、0160、0164、0194、0216 |
| C02 | 8 | candidate_0018 | 0018、0023、0032、0045、0052、0068、0081、0175 |
| C03 | 7 | candidate_0131 | 0056、0093、0109、0112、0131、0138、0166 |
| C04 | 6 | candidate_0046 | 0039、0046、0057、0108、0195、0227 |
| C05 | 6 | candidate_0047 | 0044、0047、0062、0106、0113、0137 |
| C06 | 6 | candidate_0111 | 0051、0111、0173、0183、0201、0207 |
| C07 | 4 | candidate_0043 | 0043、0085、0096、0237 |
| C08 | 3 | candidate_0008 | 0008、0128、0236 |
| C09 | 3 | candidate_0021 | 0021、0027、0171 |
| C10 | 3 | candidate_0225 | 0153、0225、0228 |
| C11 | 3 | candidate_0213 | 0213、0219、0232 |
| C12 | 2 | candidate_0071 | 0071、0097 |
| C13 | 2 | candidate_0082 | 0082、0200 |
| C14 | 2 | candidate_0129 | 0129、0165 |
| C15 | 2 | candidate_0167 | 0167、0170 |
| C16 | 1 | candidate_0241 | 0241 |

表中成员编号均省略了 `candidate_` 前缀，以便阅读。

## 三、结合你现有筛选结果，值得注意的地方

### 1. 67 条候选并不是 67 种独立的序列方案

最大的 7 个类群合计有 46 条，占全部保留候选约 69%。这说明当前保留表里存在明显的序列冗余。

后续如果每条候选都分别进入结构复核，很可能花费不少计算资源，却主要是在反复评估相近的序列变体。因此，下一阶段应优先考虑**类群内代表性与结构证据，而不是单纯按指标排名取前若干名**。

### 2. D13 和 D44 分别落在不同类群

- **D13（candidate_0165）**位于 C14，与 candidate_0129 同组。
- **D44（candidate_0173）**位于 C06，该组共 6 条候选。

这可以帮助你检查已知参照附近的序列变体，但不能因为它们与参照相似，就直接认为它们具有相似的受体结合能力或激动活性。

### 3. candidate_0241 应单独标记

candidate_0241 的序列与提供的 `reference_D41` 序列完全一致。在主聚类标准下它是单例 C16。

因此，后续候选筛选时建议把它标注为 **D41 参考序列**，与新设计候选区分开来；不要仅因为它单独成簇，就把它解释成一个新颖且优质的设计家族。

### 4. 类群中心不等于最优候选

例如，C03 的中心代表是 candidate_0131，但该组中 candidate_0093 的 `ipTM_mean` 更高。两者角色不同：

- **中心代表**：用于描述这个序列家族，减少冗余。
- **结构证据优先候选**：用于从该家族中挑出值得进一步复核的成员。

我建议保留这两个概念，不要用一个指标把它们混为一谈。后续应在每个类群内部综合看界面指标、模型间一致性和结构合理性，再决定保留谁。

## 四、聚类文件

我生成了 3 个新文件，没有覆盖或删除原文件。

<box border radius="lg" padding={3} gap={3}>
  <row align="start" gap={3}>
    <icon name="file-spreadsheet" size="xl" color="secondary" />
    <box flex="1" gap={1}>
      **候选指标表（增加聚类标注）**

      <text color="secondary" size="sm">保留原有 67 条候选和指标，新增主方案类群、类群大小、中心代表、到中心的差异数，以及严格/宽松阈值下的类群编号。</text>
      [下载 candidate_metrics_kept_clustered.csv](sandbox:/mnt/data/candidate_metrics_kept_clustered.csv)
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <icon name="file-spreadsheet" size="xl" color="secondary" />
    <box flex="1" gap={1}>
      **类群汇总表**

      <text color="secondary" size="sm">每个类群的成员、中心代表、类群大小，以及组内最高 ipTM 候选，方便后续做类群内复核。</text>
      [下载 sequence_cluster_summary.csv](sandbox:/mnt/data/sequence_cluster_summary.csv)
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <icon name="file-text" size="xl" color="secondary" />
    <box flex="1" gap={1}>
      **中心代表序列 FASTA**

      <text color="secondary" size="sm">每个主方案类群一条中心代表序列，可用于后续结构检查或与其他参考序列比较。</text>
      [下载 cluster_medoid_sequences.fasta](sandbox:/mnt/data/cluster_medoid_sequences.fasta)
    </box>
  </row>
</box>

**我的建议是暂时不要再按序列相似性继续删候选。** 先以这 16 个类群为框架，进入“每个类群挑代表、再做结构证据复核”的阶段。序列聚类解决的是冗余问题，并不能单独解决结合可信度或 GLP1R 激动活性的问题。

如果你希望，我也可以在你完成下一轮结构复核后提醒你继续做类群内候选筛选。需要我安排一个后续提醒吗？

---

# you asked

message time: 2026-10-22 08:39:18

那开始挑选代表吧，最终可以挑出20～30条，如果有必要的话也可以到40

---

# chatgpt response

我建议这一轮先定下 **24 条候选：14 条类群代表 + 10 条类群内补充候选**。这样既能覆盖大部分不同的序列家族，也能保留部分结构指标较好的近缘变体；不必为了达到 30 或 40 条而把证据较弱的候选硬塞进名单。

筛选时我没有把 `ipTM`、`pDockQ` 或 `pDockQ2` 中任何一个指标当作最终判决。它们反映的是不同方面的结构置信度，不能直接证明真实结合、亲和力或 GLP1R 激动活性。AlphaFold 数据库的说明也建议综合多个界面指标，而不是依赖单一分数。<Cite refs={["turn852932search2","turn852932search10"]}/>

## 一、第一轮优先复核名单

以下 8 条是我建议优先检查结构的候选。它们在当前 67 条保留候选中，综合界面指标表现相对突出。

| 候选 | 序列类群 | ipTM mean | pDockQ mean | pDockQ2 A–B | pDockQ2 B–A |
|---|---|---:|---:|---:|---:|
| candidate_0044 | C05 | 0.840 | 0.544 | 0.337 | 0.370 |
| candidate_0093 | C03 | 0.843 | 0.526 | 0.368 | 0.326 |
| candidate_0228 | C10 | 0.837 | 0.540 | 0.362 | 0.386 |
| candidate_0112 | C03 | 0.837 | 0.535 | 0.328 | 0.346 |
| candidate_0227 | C04 | 0.837 | 0.535 | 0.307 | 0.336 |
| candidate_0153 | C10 | 0.843 | 0.520 | 0.364 | 0.328 |
| candidate_0062 | C05 | 0.830 | 0.534 | 0.312 | 0.343 |
| candidate_0175 | C02 | 0.833 | 0.542 | 0.309 | 0.337 |

这只是**计算复核优先级**，不是实验成功概率排名。尤其要注意，candidate_0093、0112 同属 C03，candidate_0044、0062 同属 C05，candidate_0228、0153 同属 C10。它们不应被当成六种独立的设计思路。

## 二、完整 24 条名单

### A 组：14 条类群代表

每个入选序列家族先保留一条代表。这里的“代表”是综合界面指标与序列多样性选出来的，并不要求一定是聚类算法计算出的中心序列。

| 类群 | 首选候选 | 选择理由 |
|---|---|---|
| C01 | `candidate_0009` | 该类群中界面指标相对较好 |
| C02 | `candidate_0175` | ipTM、pDockQ 和双向 pDockQ2 综合表现较好 |
| C03 | `candidate_0093` | ipTM 与 pDockQ2 A–B 较突出 |
| C04 | `candidate_0227` | ipTM、ipSAE B–A 与 pDockQ2 B–A 较好 |
| C05 | `candidate_0044` | 多项界面指标均较突出 |
| C06 | `candidate_0051` | 保留该类群的代表性序列变体 |
| C07 | `candidate_0096` | 相较其他成员，双向 pDockQ2 更均衡 |
| C09 | `candidate_0027` | 综合表现较好，且保留独立类群 |
| C10 | `candidate_0228` | 两个方向的 pDockQ2 均较突出 |
| C11 | `candidate_0213` | ipTM 与双向 pDockQ2 表现较好 |
| C12 | `candidate_0071` | 保留该小类群的代表性序列 |
| C13 | `candidate_0200` | ipTM、ipSAE B–A 与 pDockQ2 综合较好 |
| C14 | `candidate_0129` | 保留 D13 所在类群的非参照候选 |
| C15 | `candidate_0170` | 保留该类群中界面指标较好的变体 |

### B 组：10 条补充候选

这些候选用于保留同一类群内值得继续检查的序列差异，或者提供中心代表与高分变体之间的比较。

`candidate_0081`、`candidate_0112`、`candidate_0046`、`candidate_0062`、`candidate_0111`、`candidate_0043`、`candidate_0021`、`candidate_0153`、`candidate_0219`、`candidate_0082`。

其中部分候选是为了补充序列多样性而保留，并非因为它们在所有结构指标上都优于对应类群的首选。

## 三、为什么暂时不选满 30–40 条？

- **C08 暂不纳入。** 该类群的 pDockQ2 均相对偏低，整体界面证据弱于本轮入选的其他类群。后续如果发现它具有明显不同的结合模式，可以重新考虑。
- **D13、D44、D41 作为参照单独保留。** 源表分别将 `candidate_0165`、`candidate_0173`、`candidate_0241` 标记为这些参照，不计入 24 条新候选。D13 所在类群仍通过 `candidate_0129` 进入名单。
- **没有为了数量增加大量近似序列。** 已入选的 24 条足以开展下一轮结构复核；如果复核发现某个类群的首选存在明显结构问题，再从该类群的剩余成员补入，比一开始机械地扩大到 40 条更合理。

还要提醒一点：`models_kept=3` 代表当前汇总表保留了 3 个模型，但不能据此直接称为 3 个独立随机种子。你此前的运行设置并不等同于独立重复实验，所以目前的排名还没有充分的跨种子稳健性证据。

## 四、结果文件

我把选择结果整理成了新的文件，原始候选表与聚类表均未修改。

<box border radius="lg" padding={3} gap={3}>
  <row align="start" gap={3}>
    <icon name="file-spreadsheet" size="xl" color="secondary" />
    <box flex="1" gap={1}>
      **24 条候选选择表**

      <text color="secondary" size="sm">包含序列、类群、选择角色、结构指标、综合排序分数和选择理由。</text>
      [下载 GLP1R_representative_selection_24.csv](sandbox:/mnt/data/GLP1R_representative_selection_24.csv)
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <icon name="file-spreadsheet" size="xl" color="secondary" />
    <box flex="1" gap={1}>
      **完整 67 条候选标注表**

      <text color="secondary" size="sm">保留全部候选，并标记入选状态、选择角色与原因，便于审计和后续补选。</text>
      [下载 candidate_metrics_selection_annotated.csv](sandbox:/mnt/data/candidate_metrics_selection_annotated.csv)
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <icon name="file-text" size="xl" color="secondary" />
    <box flex="1" gap={1}>
      **24 条候选 FASTA**

      <text color="secondary" size="sm">可直接用于后续结构复核流程。</text>
      [下载 GLP1R_representatives_24.fasta](sandbox:/mnt/data/GLP1R_representatives_24.fasta)
    </box>
  </row>
</box>

**下一步建议：** 先复核这 24 条的实际复合物结构，重点检查肽链是否稳定落在合理的 GLP1R 结合区域、关键接触是否合理、是否存在明显穿插或不合理构象，以及不同模型是否给出相近的结合姿态。再决定是否从剩余候选中补到 30 条左右。

综合分数只是用于整理优先级的启发式排序，不是校准过的成功概率；在结构复核之前，不建议把这 24 条直接称为“最佳结合剂”。

---

# you asked

message time: 2026-10-22 08:43:18

| 指标               | 最大候选           |
| ---------------- | -------------- |
| pLDDT_mean       | candidate_0165 |
| ipTM_mean        | candidate_0093 |
| ipTM_mean        | candidate_0153 |
| ipSAE_A-B_mean   | candidate_0093 |
| ipSAE_B-A_mean   | candidate_0044 |
| pDockQ_mean      | candidate_0044 |
| pDockQ2_A-B_mean | candidate_0093 |
| pDockQ2_B-A_mean | candidate_0228 |

这些candidate都包含进去了吗，还有D13D41D44这三条参考序列，如果都包括了的话我就拿去跑boltz了

---

# chatgpt response

**所以，先不要直接用原来的 24 条 FASTA 开跑。** 我核对了实际文件，结果如下：

| 你关注的候选 | 原 24 条中是否包含 | 处理 |
|---|---|---|
| `candidate_0165`（D13） | 否 | 已补入 |
| `candidate_0093` | 是 | 保留 |
| `candidate_0153` | 是 | 保留 |
| `candidate_0044` | 是 | 保留 |
| `candidate_0228` | 是 | 保留 |
| D13 参考 | 否 | 已补入 |
| D44 参考（`candidate_0173`） | 否 | 已补入 |
| D41 参考（`candidate_0241`） | 否 | 已补入 |

注意：你列出的最大值中，`candidate_0093` 同时对应多个指标，因此去重后，实际上是 **5 条不同的候选 ID**，不是 8 条。

我已把三条参照加入原来的 24 条，生成了新的 **27 条 FASTA**。所有序列均为 31 aa，并检查了候选 ID 没有重复。

[下载 GLP1R_representatives_24_plus_D13_D41_D44.fasta](sandbox:/mnt/data/GLP1R_representatives_24_plus_D13_D41_D44.fasta)

现在可以用这份文件启动 Boltz。建议保留 D13、D41、D44 的参考标签，并在后续结果分析中将它们与 24 条设计候选分开统计。这样既不会漏掉你关注的最高指标候选，也能用参照序列帮助判断这轮结构预测的相对表现。

---

# you asked

message time: 2026-10-22 08:48:51

现在来讨论一下boltz体系，首先是模版，boltz能自定义模版吗

---

# chatgpt response

可以。对于你现在的 GLP1R 短肽候选筛选，**Boltz 支持使用自定义结构模板（custom templates）**，但需要区分两个问题：

1. **能不能指定模板结构？** 可以，Boltz 的输入与推理流程支持模板相关配置。
2. **能不能让模板强制决定肽链的结合姿态？** 不能简单这么理解。模板是结构预测的参考信息，不等于把模板中的结合姿态硬性锁定；实际效果取决于模板覆盖范围、链与残基映射、输入配置以及推理过程。

对你的项目来说，关键不只是“给 Boltz 一个 GLP1R 模板”，而是确定模板是否包含**受体与已知配体的复合物结构**，以及模板是否能为 31 aa 候选肽提供有意义的结合位点和构象参考。

## 1. Boltz 本地版的模板怎么设置？

Boltz-2 的本地 YAML 输入通常使用 `templates` 字段。模板可以是 `.cif` / `.mmCIF` 或 `.pdb` 文件，并且可以指定输入链对应模板中的哪条链；模板也可以配置为软参考，或通过 `force` 和 `threshold` 更强地约束模板附近的结构。具体可参考 [Boltz 官方预测说明](https://github.com/jwohlwend/boltz/blob/main/docs/prediction.md)。<Cite refs={["turn854344search10","turn854344search3"]}/>

一_id: R
```

这里的 `chain_id` 是**待预测输入中的链 ID**，`template_id` 是**模板文件中的链 ID**。这两个名称必须按照实际输入和结构文件填写，不能直接照抄示例。不同 Boltz 版本的配置细节可能不同，正式运行前要以你安装版本的 `docs/prediction.md` 为准。

## 2. 对你的 GLP1R 项目，应该选什么模板？

你之前提到的 **7KI0** 是一个很有价值的起点。它是实验解析的 semaglutide–GLP-1R–Gs 复合物，分辨率为 2.50 Å；其中 semaglutide 是 31 aa 肽链。<Cite refs={["turn534784search0","turn534784search3"]}/>

<AsyncImageGroup query={["PDB 7KI0 semaglutide GLP-1 receptor complex structure","PDB 7KI0 semaglutide GLP-1R peptide binding pocket structure"]} aspectRatio="5:4" layout="bento" />

我建议先区分两种模板策略：

<box gap={3}>
  <row align="start" gap={3}>
    <AsyncImage query="GLP-1 receptor 7KI0 receptor protein structure without ligand" aspectRatio="4:5" maxWidth="104px" />
    <box flex="1" gap={1}>
      **方案 A：只给受体链提供模板**

      目的：利用实验结构提供 GLP1R 的局部折叠和受体构象参考，同时让候选肽的结合姿态有更多自由度。

      优点：较适合先比较不同候选可能采用的结合姿态。

      局限：不保证肽链会落在正确的结合口袋。
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <AsyncImage query="PDB 7KI0 semaglutide peptide bound to GLP-1 receptor structure" aspectRatio="4:5" maxWidth="104px" />
    <box flex="1" gap={1}>
      **方案 B：受体链和 semaglutide 肽链都提供模板**

      目的：利用已知 GLP1R 激动剂的结合姿态，为候选肽提供结合模式参考。

      优点：你的候选与 semaglutide 同属 GLP-1 样短肽序列，这种参考可能有价值。

      局限：候选可能被引导到 semaglutide 的姿态附近，导致不同候选的结构看起来更相似；这不代表它们真实活性相同。
    </box>
  </row>
</box>

## 3. 我推荐怎样开展第一轮 Boltz 预测？

建议先不要直接给 27 条候选全部使用同一种强模板约束。可以先用少量代表候选做一个模板对照实验：

| 设置 | 受体模板 | 肽链模板 | 目的 |
|---|---|---|---|
| A | 7KI0 | 无 | 观察受体参考对结果的影响 |
| B | 7KI0 | 7KI0 中的 semaglutide 链 | 观察已知激动剂结合姿态参考的影响 |
| C | 无 | 无 | 作为无模板对照 |

比较三种设置下的肽链结合位置、构象、界面接触、ipTM、pDockQ2 等结果。如果 B 的分数普遍更高，但不同候选都被拉到几乎相同的姿态，就需要警惕模板引导造成的偏差。

**一个关键细节：** 7KI0 中的受体链是实验结构中解析的受体构建体，并不等同于完整的 491 aa 全长受体；同时该复合物还包含 G 蛋白及其他组分。<Cite refs={["turn534784search0","turn534784search3"]}/> 因此，不能直接假设将整个 7KI0 文件作为模板就一定正确。应先检查你当前输入的 GLP1R 链序列、残基编号、模板链映射，以及是否需要去除与预测目标无关的链。

## 4. 在写具体 YAML 之前，我需要确认一件事

你现在实际运行的是哪一种 Boltz？

{@body const [version,setVersion] = DIL.useState("local")}
{@body const [template,setTemplate] = DIL.useState("7ki0")}
<box border radius="lg" padding={3} gap={4}>
  <text weight="medium">运行环境</text>
  <radio-group value={version} onChange={setVersion} direction="col">
    <radio value="local">本地 / HPC 安装的 Boltz-2，通过 YAML 和命令行运行</radio>
    <radio value="api">Boltz API 或网页服务</radio>
    <radio value="other">不确定具体版本</radio>
  </radio-group>
  <divider color="subtle" />
  <text weight="medium">目前准备使用的模板</text>
  <radio-group value={template} onChange={setTemplate} direction="col">
    <radio value="7ki0">7KI0，semaglutide–GLP1R 复合物</radio>
    <radio value="prepared">已经从 7KI0 提取、裁剪或处理过的 CIF/PDB</radio>
    <radio value="none">还没有准备模板文件</radio>
  </radio-group>
  <button block onClick={() => GenUI.issueNewTurn("我的 Boltz 运行环境是："+({"local":"本地/HPC 安装的 Boltz-2，通过 YAML 和命令行运行","api":"Boltz API 或网页服务","other":"暂时不确定具体版本"}[version])+"；当前模板准备情况是："+({"7ki0":"准备使用原始 7KI0 复合物","prepared":"已经准备过处理后的 CIF/PDB","none":"尚未准备模板文件"}[template])+"。请按这个环境继续讨论 GLP1R 的模板设置与验证方案。")}>确认并继续</button>
</box>

确认后，我们就可以进一步确定模板文件应该保留哪些链、如何映射链 ID，以及第一轮是否需要同时跑有模板和无模板对照。

---

# you asked

message time: 2026-10-22 09:17:30

我的 Boltz 运行环境是：本地/HPC 安装的 Boltz-2，通过 YAML 和命令行运行；当前模板准备情况是：准备使用原始 7KI0 复合物。请按这个环境继续讨论 GLP1R 的模板设置与验证方案。

---

# chatgpt response

## 5. 先明确 7KI0 的链映射

RCSB 的 7KI0 条目列出 semaglutide 为 31 aa、GLP1R 为 491 aa，并且复合物中还包含 Gs 蛋白及其他组分。<Cite refs={["turn722677search1","turn722677search12"]}/>

在 RCSB 的生物学装配编号中，GLP1R 显示为链 `F`，semaglutide 显示为链 `E`；但作者链标识分别是 `R` 和 `P`。**不能把 YAML 中的 `template_id` 直接假设为 `E` 或 `F`，必须以你实际下载的 mmCIF 文件中 Boltz 能识别的链标识为准。** <Cite refs={["turn722677search1","turn722677search2"]}/>

我建议先做以下准备：

1. 下载原始 7KI0 mmCIF，保留一份只读原件。
2. 检查文件中 GLP1R 和 semaglutide 对应的链 ID、序列与残基编号。
3. 确认你输入 Boltz 的 GLP1R 序列与模板序列的对应关系，特别是受体构建体缺失区域、非天然残基和编号偏移。
4. 第一轮先不设置 `force: true`，避免在尚未验证映射前对结构施加强约束。

## 6. YAML 建议：先做受体模板组

假设你的输入 YAML 中，GLP1R 是链 A，候选肽是链 B，且本地 CIF 中实际确认的模板链标识为 `R`（受体）和 `: A
    template_id: R
```

这是**结构示意，不是可以直接提交的最终配置**：需要把序列、路径和链 ID 换成你实际使用的值。`R` 只是示例；如果 Boltz 读取该 CIF 时使用的是 `F`，就必须填 `F`。官方文档支持通过 `chain_id` 与 `template_id` 明确映射输入链和模板链。<Cite refs={["turn356588search0","turn356588search6"]}/>

另外，`msa: empty` 只适合你明确希望采用单序列模式的情况。若你之前的 Boltz 流程使用 MSA server，就应在模板对照实验中保持相同的 MSA 策略，避免同时改变两个变量。

## 7. 具体实验设计

我建议先挑 3–5 条具有代表性的候选，包括 D13、D44 参考，以及一两条界面指标较好的设计候选，做下面的对照：

| 实验组 | 模板设置 | 是否强制模板 | 要回答的问题 |
|---|---|---|---|
| A | 无模板 | 否 | 基准预测结果是什么？ |
| B | 仅 GLP1R 链 | 否 | 受体模板是否改善受体结构？ |
| C | GLP1R + semaglutide 链 | 否 | 已知肽结合姿态是否影响候选的结合模式？ |
| D（可选） | GLP1R + semaglutide 链 | 是 | 更强的模板约束会造成什么变化？ |

D 组先不要作为正式筛选的主结果。Boltz 的 `force` 会引入用于限制结构偏离模板的势函数；设置它时还需要指定 `threshold`。<Cite refs={["turn356588search0","turn356588search5"]}/>

每组应保持候选序列、MSA 设置、recycling steps、sampling steps 和种子策略一致。重点比较：

- 肽链是否进入合理的 GLP1R 结合口袋；
- 肽链结合姿态与 semaglutide 是否高度相似；
- 不同候选之间是否仍能呈现有意义的结构差异；
- ipTM、ipSAE、pDockQ2 等指标是否与可见的界面几何相互支持；
- 改变模板设置后，结果是否出现明显的姿态变化。

**我的初步推荐是：先做 A、B、C 三组，不强制模板。** 如果 C 组结果普遍看起来更好，还需要判断这是因为模板提供了有效的结合模式参考，还是因为模型被引导到了已知激动剂的姿态附近。单纯分数升高不能区分这两种情况。

最后，在正式写 27 条候选的批量 YAML 前，还需要核对你实际安装的 Boltz 
```bash
boltz predict --help
```

并查看安装目录中对应版本的 `docs/prediction.md`。本地安装版本的输入字段才是最终依据。

如果你把**当前实际运行的一个 YAML 文件**和**7KI0 CIF 的链 ID 检查结果**贴出来，我就可以按你的真实配置逐项核对，而不是猜测链映射。

---

# you asked

message time: 2026-10-22 09:19:08

没那么多算力，只做B组，下一个问题是boltz能否处理Aib

---

# chatgpt response

**结论：Boltz-2 对 Aib（α-氨基异丁酸，α-aminoisobutyric acid）不能简单地按普通氨基酸序列处理。** 即使某个版本能接受非标准残基的 CCD 定义，也不代表它一定能准确预测 Aib 所在的肽链主链构象。

这对你的 GLP1R 项目很重要：Aib 经常用于改变短肽的构象倾向和稳定性。如果模型把 Aib 当成普通氨基酸，或者虽然读入了它的化学定义，却没有正确处理主链几何，那么预测出的结合姿态和界面评分就可能不可靠。

官方 Boltz 文档支持通过 YAML 描述蛋白质序列与部分修饰残基；但具体支持范围取决于本地版本和残基类型。近期官方仓库也有关于非天然氨基酸主链几何失真的问题报告，因此不能仅凭 YAML 成功解析就认定模型正确处理了 Aib。<Cite refs={["turn605245search0","turn605245search11"]}/>

## 对你当前这批候选，建议这样处理

| 情况 | 建议 |
|---|---|
| 候选序列全部由 20 种标准氨基酸组成 | 可以按普通 protein sequence 输入 Boltz |
| 肽链中有一个或多个 Aib | 先验证本地 Boltz 版本对该残基的支持，不要直接批量运行 |
| 用 Aib 对应的 CCD 代码声明修饰残基 | 需要同时验证残基映射、主链连接和输出结构的几何合理性 |
| 仅仅把 Aib 替换成 Ala 或其他标准氨基酸 | 只能作为近似对照，不能视为真正的 Aib 预测 |

对于 Aib，我会特别检查三个方面：

1. **化学身份**：输出结构是否仍能识别为 Aib，而不是被转换成普通氨基酸。
2. **主链几何**：N–Cα、Cα–C 和肽键连接是否合理，是否存在异常键长、键角或主链断裂。
3. **构象与界面**：Aib 周围的主链构象是否合理，以及它是否改变了肽链在 GLP1R 结合口袋中的姿态。

这些检查都通过，也只能说明模型在结构表示层面基本可用，不能证明其对 Aib 肽的预测精度已经得到验证。

## 我建议下一步先确认

你说的 Aib 是：

- **A.** 你的 27 条 GLP1R 候选序列中，实际存在 Aib 修饰；
- **B.** 你准备额外加入含 Aib 的新候选；
- **C.** 你只是想提前确认 Boltz 对非天然氨基酸的通用支持能力。

如果是 A 或 B，我建议先检查本地 Boltz 版本和 Aib 的 CCD 映射，再决定 YAML 的具体写法；如果是 C，那么目前最稳妥的结论就是：**Boltz 的通用非天然残基表示能力，不等于已经可靠支持 Aib 这种主链修饰型非标准氨基酸。**

---

# you asked

message time: 2026-10-22 09:22:57

semaglutide受体复合物中有Aib残基，但是直接导入cif/pdb文件应该可以处理吧，预测序列里对应位置都映射成A了，如果麻烦的话预测序列就还是全用天然氨基酸

---

# chatgpt response

你提出的方案有一個需要區分的細節：**直接讀取包含 Aib 的 CIF，不代表 Boltz 一定能正確把模板中的 Aib 映射到輸入序列中的 Ala。**

Boltz 的本地 YAML 文件可以用 `templates` 指定 CIF/PDB，並把輸入鏈映射到模板鏈。官方文件說明，模板主要用來提供結構參考；是否能正確處理非標準殘基，還取決於模板解析與序列／殘基對應。<Cite refs={["turn741506search0","turn741506search4"]}/>

對你目前算力有限、只打算跑 B 組的情況，我建議：

1. **預測序列繼續全部使用天然氨基酸。** 如果候選原本就是天然氨基酸序列，就不需要為了模板中的 Aib 修改候選序列。
2. **原始 7KI0 CIF 可以先作為受體模板測試。** 先確認 Boltz 能讀取 CIF、正確找到 GLP1R 模板鏈，並確認模板殘基與輸入受體序列的對應。
3. **不要把 semaglutide 的 Aib 當成普通 Ala 直接強行對齊。** 如果只映射受體鏈，候選肽鏈本身就不需要處理模板中的 Aib。若後續要加入 semaglutide 肽鏈作模板，才需要仔細核對 Aib 的位置和映射。
4. **不要因為預測序列使用天然氨基酸，就認為模板中的非標準殘基已被完全解決。** 兩者是不同的輸入路徑。

因此，按你已決定的 B 組方案，最穩妥的做法是：**只映射 7KI0 的 GLP1R 受體鏈到輸入受體鏈，候選肽維持天然氨基酸序列，不額外映射 semaglutide 鏈。** 這樣可以避免候選肽模板映射中的 Aib 問題，也符合你目前希望節省算力的目標。

不過，這會是「受體模板組」，不是「受體加已知激動劑結合姿態模板組」。如果你的本意是利用 semaglutide 的結合姿態來引導候選肽，那就需要另一套鏈映射與驗證方案。

---

# you asked

message time: 2026-10-22 09:24:09

你怎么用繁体中文了，我没改设置吧

---

# chatgpt response

没有，你没有改设置。抱歉，刚才突然用了繁体中文，是我这边输出风格出了偏差，不是你操作导致的。

**我接下来会继续使用简体中文**，并保持我们之前的交流习惯：专业术语保留英文，解释尽量清楚、直接。我们继续 GLP1R 和 Boltz-2 的讨论就好。

---

# you asked

message time: 2026-10-22 09:30:01

7KI0文件上传到boltz作为模版时，yaml文件里面应该只需要放R链和P链把，还是说要放一整个pdb文件

---

# chatgpt response

**按我们目前决定的方案，建议 YAML 里只把输入受体链 A 映射到 7KI0 的 GLP1R 受体链 R，不映射 P 链。** 不过，`templates` 里引用的文件可以是整个 7KI0 CIF，也可以是提取出来的受体单链文件，不要求 YAML 里把 R、P 两条链都列出来。

Boltz 的 `templates` 配置支持指定输入链 `chain_id` 与模板链 `template_id` 的对应关系；模板文件可以包含多条链。<Cite refs={["turn850149search0","turn850149search2"]}/>

## 两种写法有什么区别？

<box gap={3}>
  <row} size="44px" align=center justify=center>
      <icon name="file" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **方案 A：直接 - cif: /path/to/7ki0.cif
          chain_id: A
          template_id: R
      ```

      这里的 `A` 是你预测输入中的 GLP1R 链，`R` 是模板文件中的 GLP1R 链。**P 链虽然存在于文件里，但没有被显式映射为候选肽链 B 的模板。**
    </box>
  </row>
  <divider color="subtle" />
  <row align=start gap={3}>
    <box background="surface-secondary" radius="lg" padding={2} size="44px" align=center justify=center>
      <icon name="scissors" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **方案 B：提取 GLP1R 受体链，单独保存 CIF**

      <badge color="success">更适合当前方案</badge>

      ```yaml
      templates:
        - cif: /path/to/7ki0_receptor_only.cif
          chain_id: A
          template_id: R
      ```

      只保留受体链，可以减少无关组分的干扰，也避免 Boltz 处理模板中 semaglutide 的 Aib 等非标准残基时出现额外问题。注意，提取后要确认链 ID 是否仍然是 `R`；如果变了，`template_id` 也必须随之修改。
    </box>
  </row>
</box>

## 那 P 链要不要放？

这取决于你的实验设计：

| 方案 | GLP1R 受体模板 | Semaglutide 的 P 链模板 | 适用目的 |
|---|---|---|---|
| 当前方案 | 使用 | 不映射 | 参考受体结构，让候选肽自行预测结合姿势 |
| 受体与肽都使用模板 | 使用 | 映射到输入 B 链 | 引入已知肽的结构或结合姿势，可能限制候选肽的构象探索 |

你目前的目标是比较候选肽，而不是直接复现 semaglutide 结合姿势，因此我建议先采用**受体链模板，不映射 P 链，也不要启用强制模板约束**。

## 还有一个必须先核对的问题

你目前的输入受体是 **384 aa**，而 7KI0 中的 GLP1R 构建体长度与之不同。因此，不能只凭链名 `R` 就认为映射正确。运行前需要确认：

1. 384 aa 输入序列与 7KI0 的 R 链序列能否正确比对。
2. 模板覆盖了输入受体的哪些残基，是否存在截短、缺失或编号偏移。
3. Boltz 的日志或预处理结果是否真的识别并使用了指定模板。

**我的建议：先检查序列比对，再决定是否直接用完整 CIF 或提取受体链。** 如果你把 7KI0 文件的格式（`.cif` 还是 `.pdb`）和你当前 YAML 中的 `templates` 部分贴出来，我可以直接帮你核对链ID 和配置写法。

---

# you asked

message time: 2026-10-22 09:32:19

让候选肽自行预测结合姿势是否有可能让正确的候选由于结合姿势错误导致被淘汰

---

# chatgpt response

**有可能，而且对于 GLP1R 这种已有已知配体结合结构的靶点，这确实是值得认真考虑的风险。**

如果你只给 Boltz-2 提供 GLP1R 受体模板，却不提供 semaglutide 的肽链及其结合姿势，那么候选肽需要自行预测如何靠近受体、采用什么构象，以及哪些残基参与界面相互作用。

这样做有一个潜在问题：**候选肽本身可能具有结合潜力，但模型没有预测出正确的结合姿势，导致界面指标偏低，最后在候选排序中被淘汰。**

不过要区分两种情况：

- **真实结合能力差：** 候选肽本身就不太可能有效结合 GLP1R。
- **预测姿势错误：** 候选肽可能有结合潜力，但这次结构预测没有恢复出合理的结合模式。

单次 Boltz-2 预测通常不能可靠地区分这两种情况。如果直接按 ipTM、pDockQ2 等指标排序，第二种情况确实可能造成假阴性。

## 那我们应该怎么做？

我建议不要在“完全自由预测”和“完全照搬 semaglutide 姿势”之间二选一，而是采用**两阶段筛选**。

<box border radius="xl" padding={3} gap={3}>
  <row align=start gap={3}>
    <box background="surface-secondary" radius="lg" size="40px" align=center justify=center>
      <title size="lg">1</title>
    </box>
    <box flex="1" gap={1}>
      **第一阶段：受体模板 + 自由预测**

      对现有候选进行初筛。使用 7KI0 的 GLP1R 受体结构作为模板，但不把 semaglutide 的 P 链映射成候选肽的模板。

      目的：找出模型能够自主预测出合理结合模式的候选。
    </box>
  </row>
  <divider color="subtle" />
  <row align=start gap={3}>
    <box background="surface-secondary" radius="lg" size="40px" align=center justify=center>
      <title size="lg">2</title>
    </box>
    <box flex="1" gap={1}>
      **第二阶段：对重点候选进行结合姿势参考测试**

      只挑一部分候选，再尝试引入 semaglutide 的结合姿势作为参考，观察候选的界面质量、关键相互作用和结构合理性是否改善。

      目的：识别可能因为自由预测姿势不佳而被低估的候选。
    </box>
  </row>
</box>

Boltz 支持使用结构模板引导蛋白链几何，但模板提供的是结构先验，不是对真实结合模式的证明。<Cite refs={["turn346091search0","turn346091search14"]}/>

### 第二阶段需要注意什么？

不能简单地把 semaglutide 的 P 链强行对应到所有候选肽的 B 链，然后认为结果更好就代表候选更优秀。

原因有三个：

- **序列差异：** 候选肽与 semaglutide 不一定能进行可靠的逐残基映射。
- **非天然残基：** semaglutide 含有 Aib 等修饰，不能不经核对就当作普通 Ala 处理。
- **模板偏倚：** 模板可能把候选引向与参考肽相似的姿势，即使候选本身不适合这种姿势。

另外，GLP1R 的肽结合涉及胞外结构域与跨膜核心区域，不只是一个静态界面。参考结构有帮助，但也不能保证它适合每条候选肽。<Cite refs={["turn346091search1","turn346091search11"]}/>

## 考虑到你的算力，我会这样安排

不建议把全部 67 条候选都跑两遍。先利用已有的预测结果，挑出大约 **5–10 条具有代表性的候选**做对照测试，包括：

- 自由预测表现较好的候选；
- 指标一般但序列具有代表性的候选；
- 与参考肽差异较大、可能被自由预测低估的候选。

如果参考姿势测试后，部分候选的界面质量明显改善，而且相互作用合理，就把它们列为“需要复核”的候选，而不是直接宣布它们更优。

**最重要的筛选原则：不要因为一次预测的结合姿势不好，就直接淘汰一条候选肽。** 结构置信度、界面几何和序列多样性应共同参与判断；最终的真实结合能力仍需要实验验证。

下一步我最想确认的是：你这 67 条肽与 semaglutide 的序列关系到底有多近。这个信息会决定第二阶段是否值得做，以及能否可靠地把 P 链映射到候选链 B。

---

# you asked

message time: 2026-10-22 09:33:48

算了算了，还是采用双映射吧

---

# chatgpt response

可以，那我们就采用**双映射：GLP1R 受体链 A → 7KI0 的 R 链，候选肽链 B → 7KI0 的 P 链**。

不过，我建议把它定义为**参考结合姿势引导的预测组**，而不是认定双映射一定更准确。它可以降低候选肽完全自由探索结合姿势的负担，但也可能把候选引向 semaglutide 的结合模式。

## YAML 的配置思路

假设你使用的 CIF 中链 ID 确实是 `R` 和 `P`，配置形式如下：



这里有几个关键前提：

1. **先确认链 ID。** 要以你实际下载的 CIF 和本地 Boltz-2 版本的解析结果为准，不能只根据文献里的链名填写。
2. **确认序列比对。** 你的受体输入链 A 是 384 aa，必须核对它与 7KI0 的 R 链能否合理对应。
3. **谨慎处理 Aib。** P 链含有非天然氨基酸 Aib。候选肽序列中的 Ala 不能直接视为与 Aib 完全等价；需要确认模板映射时如何处理该位置。
4. **先不要强制模板。** 初次测试建议不设置 `force: true`，也不人为降低模板匹配阈值来强行接受不可靠的映射。

## 我建议的验证方式

先选少量候选试跑双映射，检查模板是否成功匹配、关键残基是否正确对齐，以及预测结构是否合理。再与已有的自由预测结果比较。

**一个重要提醒：双映射结果的分数不能直接与自由预测结果当作完全同条件的成绩比较。** 因为两组使用的结构先验不同。双映射更适合用来判断候选在参考结合姿势下是否仍然具有合理的界面，而不是单凭分数升高就认定候选更好。

如果你把当前 YAML 的完整内容和本地 Boltz-2 版本的模板配置贴出来，我可以按你现有的输入格式，帮你检查双映射配置是否正确。

---

# you asked

message time: 2026-10-22 09:42:39

设计GLP-1RA的计算筛选——疗效
AlphaFold2被用于预测设计GLP-1RA序列和GLP-1R的复杂结构。每个复形的最佳秩次结构进一步计算了TM评分、RMSD、pLDDT和界面pAE。设计的复合结构（GLP-1 RA和GLP-1R）与原生复合结构（司美格鲁肽和GLP-1R）之间的TM评分;设计的GLP-1RA结构与Semaglutide天然结构之间的RMSD;为设计的GLP-1RA结构提供pLDDT;GLP-1 RA和GLP-1R复合物链间残基对（界面pAE）的平均pAE。这些参数的临界阈值来自Semaglutide和GLP-1R之间的天然复合结构。主要是因为论文里也是吧semaglutide受体复合物作为标准，双映射更符合复现标准，可以不强制规划姿势，但是要让模版引导预测

---

# chatgpt response

我理解你的思路，而且结合你引用的论文方法，我认为**采用 semaglutide–GLP1R 天然复合物作为结构参考，再通过双映射给 Boltz-2 提供模板引导，是有方法学依据的**。这比单纯让候选肽自由寻找结合姿势，更贴近你希望复现的计算筛选框架。

关键在于区分两件事：

- **模板引导（template-guided prediction）：** 利用天然复合物提供受体和肽的结构信息，帮助模型预测候选复合物。
- **强制固定结合姿势（hard restraint）：** 强行要求候选肽保持参考配体的特定位置或构象。

你希望采用前者，而不是后者。这个区分是合理的。

你引用的论文也有类似的逻辑：以 semaglutide–GLP1R 天然复合物作为参考，评估设计复合物与天然复合物的结构相似性，并用天然复合物建立筛选指标的参考阈值。但要注意，论文采用 AlphaFold2 的具体建模和评分流程，不能直接推定 Boltz-2 的模板机制、分数尺度与其完全等价。

## 对应到你现在的 Boltz-2 配置

按照本地 Boltz-2 文档，可以把两个链的映射写在同一个模板条目中：<Cite refs={["turn500158search1","turn500158id: [R, P]
```

这表示：

- 输入链 A → 模板中的 R 链（GLP1R）。
- 输入链 B → 模板中的 P 链（semaglutide）。

这里**不设置 `force: true`，也不设置 `threshold`**，就是使用模板引导，而不额外施加模板强制约束。具体行为仍要以你安装的本地 Boltz-2 版本为准。

但正式跑全部候选前，还有两个必须确认的地方：

1. 你的 GLP1R 输入序列只有 384 aa，需要检查它与模板 R 链的序列对应关系和覆盖范围。
2. 候选肽是 31 aa，而 semaglutide 的 P 链含有 Aib 等非标准残基。需要确认本地 Boltz-2 对 P 链模板的残基映射与序列对齐方式，避免把不对应的位置错误地映射起来。

因此，我们可以把这套方法暂定为 **GLP1R 双链模板引导的候选筛选方案**。它在研究设计上更贴近你引用的论文，但应当将它描述为对论文思路的 Boltz-2 迁移，而不是对原始 AlphaFold2 流程的完全复现。

---

# you asked

message time: 2026-10-22 09:47:01

这里不设置 `force: true`，也不设置 `threshold`  这俩是啥

---

# chatgpt response

这两个参数可以理解为：**`force` 决定是否强行接受模板，`threshold` 决定模板匹配需要达到什么程度。** 不过，它们在 Boltz-2 中的准确含义要结合具体版本的实现来看，不能只凭参数名称推断。

## 1. `force: true` 是什么？

可以把它理解为对模板匹配的额外强制选项。

- 不启用强制选项：模板需要按照 Boltz 的匹配规则被接受。
- 启用强制选项：在该版本支持的情况下，可以让模板在通常匹配条件不满足时仍被接受。

但要注意，**`force: true` 不等于固定候选肽的三维坐标，也不等于把结合姿势完全锁死**。模板是否被接受，与预测时是否强制维持模板几何结构，是两回事。

## 2. `threshold` 是什么？

在本地 Boltz-2 的模板配置中，`threshold` 指的是**预测结构的主链相对于模板允许偏离的距离阈值，单位是 Å（埃）**，不是序列相似度阈值。官方文档说明，启用 `force: true` 时必须同时指定 `threshold`。<Cite refs={["turn342730search0","turn342730search11"]old: 2.0
```

这表示对模板施加额外的几何约束，使预测主链受到限制，不能轻易偏离模板参考结构。

- `threshold: 2.0`：约束相对较紧。
- `threshold: 5.0`：允许更大的偏离。
- 不设置 `force: true`：不启用这种额外的模板几何约束，因此也不需要 `threshold`。

注意，具体实现并不等于简单地逐原子硬锁在指定距离内，而是通过模型中的约束势影响采样。

## 3. 对你的 GLP1R 项目，应该怎么选？

| 配置 | 模板的作用 | 是否适合当前目标 |
|---|---|---|
| 不设置 `force` 和 `threshold` | 提供结构参考，引导预测 | **建议先用这个** |
| `force: true` + `threshold: 5.0` | 提供参考并施加较宽松的几何约束 | 可作为后续对照 |
| `force: true` + `threshold: 2.0` | 施加较严格的几何约束 | 不建议一开始就用 |

因此，当前的双映射配置先写成：

```yam合你想要的方向：**让 semaglutide–GLP1R 复合物引导候选肽的结构预测，但不额外强制其主链贴近参考结构。**

最后有一点很重要：双映射是否真正生效，以及 384 aa 的受体和 31 aa 候选肽是否都能正确匹配，仍需要检查你本地 Boltz-2 版本的解析日志和序列比对结果。

---

# you asked

message time: 2026-10-22 09:48:54

那现在继续确定boltz体系，比如每条序列要跑出几条数据，以及种子选择，类似colabfold的model、recycle等

---

# chatgpt response

我们可以把 Boltz-2 的预测体系正式定下来。考虑到你现在的目标是对 GLP1R 的 67 条候选肽进行计算筛选、算力有限，而且希望尽量贴近以 semaglutide–GLP1R 天然复合物为参照的论文方法，我建议先建立一套**固定参数、可复现、每条候选计算量适中**的基准流程。

核心原则有三个：

1. **同一批候选使用相同的预测参数和模板策略**，避免把参数差异误认为候选差异。
2. **每条候选保留多个独立预测结果**，而不是只挑分数最高的一次。
3. **区分模型数量、随机种子和 recycle 次数**。它们解决的问题不同，不能简单互相替代。

## 一、先把 Boltz-2 的参数对应关系弄清楚

| 参数 | 作用 | 对你这个项目的意义 |
|---|---|---|
| `seeds` / 随机种子 | 控制不同随机初始化或采样过程 | 观察同一候选的预测稳定性 |
| `recycling_steps` | 让模型迭代更新结构表示 | 影响预测质量和计算耗时 |
| `diffusion_samples` | 扩散生成的结构样本数，具体含义取决于版本与运行路径 | 决定每次预测生成多少结构 |
| `use_msa_server` | 是否使用 MSA 服务器获取多序列比对 | 影响输入信息与计算流程 |
| `templates` | 提供参考结构 | 让候选肽受到 semaglutide–GLP1R 复合物的结构引导 |
| `output_format` / 输出目录 | 控制输出组织方式 | 方便追踪每个候选的多个预测结果 |

这里最需要注意的是：**Boltz-2 的 `seeds`、`diffusion_samples` 和 `recycling_steps` 不是 ColabFold 的 `num-seeds`、`num-models`、`num-recycle` 的一一对应参数。** 应当根据你安装的 Boltz-2 版本和实际 CLI 来确定参数含义。

## 二、我建议先采用这套参数

官方 Boltz 命令行文档列出的默认值包括 `recycling_steps=3`、`sampling_steps=200`、`diffusion_samples=1`；Boltz-2 的 `step_scale` 默认值是 **1.5**，不要和 Boltz-1 的 1.638 混淆。<Cite refs={["turn963040view0","turn310183view0"]}/>

<box border radius="xl" padding={3} gap={3}>
  <title size="lg">GLP1R · Boltz-2 初筛参数建议</title>
  <text color="secondary" size="sm">建议版本：先跑小规模试验，再固定参数批量预测</text>
  <table>
    <table-row>
      <table-cell width="42%">
        参数
      </table-cell>
      <table-cell>
        建议值
      </table-cell>
    </table-row>
    <table-row>
      <table-cell>每条候选的结构样本数</table-cell>
      <table-cell>**3**</table-cell>
    </table-row>
    <table-row>
      <table-cell>随机种子</table-cell>
      <table-cell>先固定为 **37**</table-cell>
    </table-row>
    <table-row>
      <table-cell>`recycling_steps`</table-cell>
      <table-cell>**3**</table-cell>
    </table-row>
    <table-row>
      <table-cell>`sampling_steps`</table-cell>
      <table-cell>**200**</table-cell>
    </table-row>
    <table-row>
      <table-cell>`step_scale`</table-cell>
      <table-cell>**1.5**</table-cell>
    </table-row>
    <table-row>
      <table-cell>`max_parallel_samples`</table-cell>
      <table-cell>**1**，先控制显存占用</table-cell>
    </table-row>
    <table-row>
      <table-cell>模板</table-cell>
      <table-cell>7KI0 双链映射；不强制模板</table-cell>
    </table-row>
    <table-row>
      <table-cell>MSA</table-cell>
      <table-cell>所有候选采用同一套 MSA 策略</table-cell>
    </table-row>
  </table>
</box>

这套参数是针对你的筛选任务提出的**工作方案**，不是已经验证为最优的参数组合。

### 三、每条序列究竟跑几次？

这里需要区分两件事：

- `diffusion_samples=3`：一次运行生成 3 个结构样本。
- 使用 3 个不同的随机种子分别运行：进行 3 次不同随机初始化的预测。

它们不完全等价。Boltz 的随机种子控制随机数生成；固定种子有助于复现，但相同种子不保证跨硬件或模型版本得到完全相同的结果。<Cite refs={["turn310183view0","turn574851search1"]}/>

我建议分两个阶段：

<box gap={3}>
  <row align=start gap={3}>
    <box background="surface" border radius="lg" padding={2} align=center justify=center size="44px">
      <title size="lg">3×</title>
    </box>
    <box flex="1" gap={1}>
      **第一阶段：67 条候选，每条 3 个样本**

      - 固定种子 37。
      - 每条候选使用相同参数和模板。
      - 总计 201 个结构样本。
      - 记录每个样本的指标，不要只保存最高分样本。
    </box>
  </row>
  <divider color="subtle" />
  <row align=start gap={3}>
    <box background="surface" border radius="lg" padding={2} align=center justify=center size="44px">
      <title size="lg">3×</title>
    </box>
    <box flex="1" gap={1}>
      **第二阶段：重点候选进行独立种子复核**

      对初筛后表现较好、不同样本间差异较大，以及序列上有代表性的候选，额外使用不同种子（例如 73、101）复核。

      重点观察结合姿势是否稳定、界面指标是否一致，而不是单纯挑选最高分。
    </box>
  </row>
</box>

**为什么不直接每条跑 5 个样本？** 67 条 × 5 已经是 335 个结构样本。考虑你有限的计算资源，先用 3 个样本筛选，再把额外计算集中到重点候选，更经济。

## 四、ColabFold 的 `num-models` 怎么对应？

这部分不能直接照搬。

| ColabFold 参数 | Boltz-2 中的对应思路 |
|---|---|
| `num-models` | Boltz-2 不能简单按相同数字对应；优先关注独立结构样本数 |
| `num-seeds` | 用不同随机种子进行复核 |
| `num-recycle` | 对应 `recycling_steps`，建议先用 3 |
| 每个模型的排名 | 对每个结构样本分别记录指标，再汇总稳定性 |

因此，当前建议先不增加 `recycling_steps` 到 6 或 10。增加 recycle 会改变推理过程，但不能代替独立结构采样；只有在小规模试验显示结构质量有改善时，才值得专门比较。

## 五、正式批量跑之前，还差一个关键核对

我不建议现在就把 67 条全部提交。先用 2–3 条候选做试运行，检查：

- 双映射模板是否成功加载，384 aa 受体和 31 aa 肽链是否正确对齐；
- 每条是否确实输出 3 个独立结构样本；
- `--seed`、`--diffusion_samples` 和 `--max_parallel_samples` 是否与你本地安装的版本一致；
- 显存峰值和单条预测耗时是否可接受。

如果试运行通过，我们就可以把这套参数冻结为正式初筛协议，并记录 Boltz 版本、完整命令、模板文件校验值、种子和输出文件清单。

顺便问一句：你希望我后续也提醒你检查试运行结果、再决定是否启动 67 条批量预测吗？我可以设置一个后续提醒。

---

# you asked

message time: 2026-10-22 10:06:29

sampling_steps=20和step_scale是啥

---

# chatgpt response

## 1. `sampling_steps=20` 是什么？

Boltz-2 使用扩散过程生成三维结构。`sampling_steps` 控制这个结构生成过程中执行多少个采样步骤。

可以把它粗略理解为：模型从初始状态逐步生成、修正三维结构的过程。

- `20`：采样步骤较少，通常更快，适合快速测试。
- `200`：采样步骤更多，是官方本地 CLI 文档列出的默认值，通常计算耗时更长。<Cite refs={["turn748143search0","turn748143search4"]}/>

但要注意：**20 步不等于只预测了 20 个结构，也不代表预测质量只有 200 步的十分之一。** 结构样本数由 `diffusion_samples` 控制，两者是不同的参数。

## 2. `step_scale` 是什么？

`step_scale` 控制扩散采样过程中的尺度，影响采样的多样性和结构生成行为。官方文档给出的默认值是 `1.638`。<Cite refs={["turn748143search0","turn748143search2"]}/>

可以先这样理解：

- 较低的值：通常会增加样本多样性。
- 较高的值：会改变采样轨迹，可能使样本更集中，但不保证结构更准确。

它不是结构评分，也不是结合强度参数。不能因为某个 `step_scale` 产生了更高的 ipTM，就直接认为它更合理。

## 3. 对你的 GLP1R 筛选，该怎么设？

我的建议是：

| 参数 | 建议 |
|---|---:|
| `sampling_steps` | **先用 20 做小规模测试** |
| `step_scale` | **1.638，先保持默认值** |
| `diffusion_samples` | 先设 1，验证运行流程 |
| `recycling_steps` | 3 |

等确认模板双映射、序列对齐和输出结构都正常，再考虑把 `sampling_steps` 提高到 200，并用少量候选对比 20 步与 200 步的结构质量和耗时。

**有一个重要前提：** 上述 20 步与 200 步的对比，应以你本地安装的 Boltz-2 版本确实支持这两个值为准。官方本地 CLI 与不同托管 API 的参数范围并不完全一致；不能直接把 API 的限制套用到你的本地环境。<Cite refs={["turn748143search0","turn748143search4"]}/>

如果你把当前环境中 `boltz predict --help` 关于 `sampling_steps`、`step_scale` 和 `diffusion_samples` 的几行输出贴出来，我们就能按你实际安装的版本把参数最终定下来。

---

# you asked

message time: 2026-10-22 10:07:20

上一条回答怎么消失了

---

# chatgpt response

可能是 ChatGPT 页面发生了临时刷新、消息显示异常，或者上一条回复在客户端没有正常保留。我无法直接查看你的页面状态，所以暂时不能确定具体原因。

我这边仍然能看到我们刚才关于 Boltz-2 参数的讨论，没有主动删除上一条回答的操作。

我们刚才讨论的是：

- `sampling_steps`：控制扩散结构采样的步骤数。
- `step_scale`：影响扩散采样过程及生成结构的多样性。
- GLP1R 初筛暂定方案：先用较少采样步骤做小规模测试，`recycling_steps=3`，其他参数以本地 Boltz-2 版本为准。

**你可以先尝试刷新页面或重新打开这段对话。** 如果仍然看不到，你告诉我消失的是哪一条——是关于每条候选跑几次、随机种子选择的回答，还是刚才解释 `sampling_steps` 和 `step_scale` 的回答？我可以直接完整补回来。

---

# you asked

message time: 2026-10-22 10:07:57

那现在继续确定boltz体系，比如每条序列要跑出几条数据，以及种子选择，类似colabfold的model、recycle等 是这句

---

# chatgpt response

## 六、先纠正一个会影响参数选择的细节

我刚才核对了官方本地 CLI 文档：本地 Boltz-2 的 `sampling_steps` 默认值是 200，最初建议的 `20` 不能直接当作本地 CLI 的有效设置。官方托管 API 的参数限制也不同，不能混用。<Cite refs={["turn173061search1","turn173061search0"]}/>

因此，我们先不要把 `sampling_steps=20` 写入正式批量流程。对本地版本，暂时按默认的 200 规划，等确认你的实际安装版本后再决定是否调整。

## 七、恢复后的完整建议：Boltz-2 正式初筛体系

| 项目 | 当前建议 | 说明 |
|---|---|---|
| 预测对象 | 67 条候选肽 | 受体与候选序列保持一致 |
| 模板 | 7KI0 双链映射 | A→R，B→P；先验证残基映射 |
| `recycling_steps` | 3 | 先用默认值 |
| `sampling_steps` | 200 | 本地 CLI 默认值 |
| `step_scale` | 1.5 | Boltz-2 本地实现的默认值 |
| `diffusion_samples` | 3 | 每条候选生成 3 个结构样本 |
| `max_parallel_samples` | 1 | 先控制显存占用 |
| 随机种子 | 暂不指定 | 标准本地 CLI 文档未列出与 ColabFold `--random-seed` 等价的常规选项 |

本地 Boltz-2 的默认 `step_scale` 是 1.5；1.638 是 Boltz-1 的默认值。<Cite refs={["turn173061search7","turn173061search1"]}/>

### 每条候选最后得到多少条数据？

建议先按每条候选 3 个结构样本规划，总计：

$$
67 \times 3 = 201\text{ 个结构样本}
$$

对每个样本分别提取 ipTM（如果当前输出支持）、界面 PAE、pLDDT、pDockQ2 等指标，再按候选汇总均值、离散程度和结构一致性。注意不同指标的定义与计算方式要固定，不能把不同工具输出的同名指标直接混用。

### 种子怎么处理？

这点与 ColabFold 有区别：本地 Boltz-2 标准 CLI 文档列出了 `diffusion_samples`，但没有列出常规的 `--seed` 参数。<Cite refs={["turn173061search1","turn173061search7"]}/>

所以目前不应该直接规定“每条序列跑种子 37、73、101”，除非确认你的具体版本确实支持这种控制。先用 3 个 diffusion samples 做初筛；之后再检查本地代码是否能显式控制随机种子，对重点候选进行独立重复预测。

**接下来最合适的一步：** 在你的 Boltz 环境运行 `boltz predict --help`，把与 `recycling_steps`、`sampling_steps`、`diffusion_samples`、`step_scale` 相关的选项贴出来。这样我们就能按实际安装版本确定最终命令，而不是把其他版本或 API 的参数误套到本地。

另外，要不要我之后提醒你检查小规模试运行结果，再决定是否启动 67 条候选的批量预测？

---

# you asked

message time: 2026-10-22 10:10:33

种子指定为27，其他的沿用你说的体系，最后就是msa了，由于之前colabfold的msa sever操作都失败了，我觉得要么不使用msa，要么使用本地msa

---

# chatgpt response

## 八、MSA：我建议优先尝试本地 MSA，而不是直接放弃

Boltz-2 的官方说明支持三种模式：

- 自动 MSA：通过 `--use_msa_server` 获取。
- 本地预计算 MSA：在 YAML 中指定 `.a3m` 文件。
- 单序列模式：写 `msa: empty`，不使用 MSA。官方文档明确指出，单序列模式可能降低预测准确性。<Cite refs={["turn431991search0","turn431991search2"]}/>

考虑到你之前 ColabFold 的 MSA Server 多次失败，我倾向于：

**优先检查是否能复用已有的本地 MSA；如果没有，再评估能否离线生成。** 这样不必把整个项目的成功与否押在远程服务器上。

不过 GLP1R 这里有个特别之处：受体是 384 aa 的蛋白质，而候选肽只有 31 aa。两条链不一定都能从 MSA 中获得同等程度的帮助，因此不必为了形式统一而强行给候选肽构造 MSA。

## 九、最终建议的 MSA 方案

<box border radius="xl" padding={3} gap={3}>
  <title size="lg">优先方案：受体本地 MSA + 候选肽单序列</title>
  <row align=start gap={3}>
    <box background="surface-secondary" radius="lg" padding={2} size="44px" align=center justify=center>
      <icon name="check-circle" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **链 A：GLP1R，3eck-circle" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **链 B：候选肽，31 aa**

      暂时使用 `msa: empty`。短肽的同源序列可能有限，而候选肽又是设计序列，不必为了追求两条链的形式一致而强行生成 MSA。
    </box>
  </row>
  <text color="secondary" size="sm">注意：Boltz 支持同一个输入中一条蛋白链使用自定义 MSA、另一条使用 empty 模式；不能在同一次预测中混用自定义 MSA与自动服务器 MSA。<Cite refs={["turn431991search0","turn431991search2"]}/></text>
</box>

对应的 YAML 结构示意：

```yaml
sequences:
  - protein:
      id: A
      sequence: "你的GLP1R输入序列"
      msa: /path/to/glp1r.a3m

  - protein:
      id: B
      sequence: "你的候选肽序列"
      msa: empty

templates:
  - cif: /path/to/7ki0.cif
    chain_id: [A, B]
    template_两条链都使用 `msa: empty`，不再依赖远程 MSA Server。所有候选保持同一套输入策略，并在项目报告中明确说明采用单序列模式，避免把不同 MSA 条件下的分数直接混在一起比较。

## 十、当前待冻结的参数清单

| 参数 | 当前决定 |
|---|---|
| 随机种子 | 27（先确认本地版本如何设置） |
| `recycling_steps` | 3 |
| `sampling_steps` | 200 |
| `step_scale` | 1.5 |
| `diffusion_samples` | 3 |
| `max_parallel_samples` | 1 |
| 模板 | 7KI0 双链映射，不启用强制模板 |
| MSA | 优先受体本地 MSA，候选肽 `empty` |
| 预测批次 | 先做 2–3 条试运行，再扩展到 67 条 |

这里仍有两个待验证项：本地版本是否支持显式指定随机种子 27，以及双链模板是否成功映射。两者确认后，才适合冻结正式批量运行协议。

**我建议下一步先检查你的本地环境有没有可复用的 MSA 文件。** 你可以在 Ubuntu/WSL 中运行：

```bash
find LOCAL_PATH -type f $ -name "*.a3m" -o -name "*.sto" -o -name "*.msa" $ 2>/dev/null | head -50
```

把输出贴给我，我们就能判断能否复用已有 MSA，而不必重新折腾远程服务器。

如果你愿意，我也可以后续提醒你完成这次小规模试运行检查，再决定是否批量跑完 67 条候选。

---

# you asked

message time: 2026-10-22 10:11:44

本地没有msa，需要下载

---

# chatgpt response

明白，那就把 MSA 也纳入正式流程：**下载本地 MSA 数据库，在本地生成 GLP1R 的 MSA，之后让所有候选共用这份受体 MSA。**

但先提醒你一个很重要的现实问题：ColabFold 的完整本地数据库方案可能需要约 **940 GB** 存储空间，而且搜索会占用较多 CPU 和内存。官方文档也指出，大规模本地搜索需要较充足的 RAM。<Cite refs={["turn336967search1","turn336967search11"]}/>

所以我不建议你现在直接下载整套数据库。先检查可用磁盘空间和内存，再选择合适的本地数据库方案。

## 1. 先区分：下载数据库，不是直接下载 MSA 文件

本地 MSA 的生成流程是：

<box border radius="xl" padding={3} align=center gap={2}>
  <box background="surface-secondary" radius="md" padding={3} width="100%" align=center>
    **GLP1R 受体序列（384 aa）**
  </box>
  <icon name="arrow-down" size="lg" color="secondary" />adding={3} width="100%" align=center>
    **本地序列数据库 + MMseqs2 搜索**
  </box>
  <icon name="arrow-down" size="lg" color="secondary" />
  <box background="surface" border radius="md" padding={3} width="100%" align=center>
    **生成 GLP1R 的 `.a3m` 文件**
  </box>
  <icon name="arrow-down" size="lg" color="secondary" />
  <box background="surface" border radius="md" padding={3} width="100%" align=center>
    **Boltz-2：受体使用 MSA，候选肽使用 `msa: empty`**
  </box>
</box>

ColabFold 官方提供数据库下载与 `colabfold_search` 本地搜索流程。<Cite refs={["turn336967search1","turn336967search11"]}/>

## 2. 先检查你的 WSL 资源

请在 Ubuntu/WSL 中依次执行：

```bash
df -h /mnt/d /home
free -h
nvidia-smi
```

这三条命令分别检查磁盘空间、系统内存和 GPU 状态。

**把输出贴给我，我再帮你确定下载方案。** 目前不建议直接执行完整数据库下载脚本，因为它可能需要近 1 TB 空间；如果空间不足，下载到一半会很麻烦。

另外，我也可以在你开始本地 MSA 生成后提醒你检查 `.a3m` 是否成功生成，再进入 Boltz-2 的小规模试运行。

---

# you asked

message time: 2026-10-22 10:12:44

我没有那么多空间，给我一个只搜索下载GLP1R相关MSA的方案

---

# chatgpt response

可以。你不需要下载完整的 ColabFold 数据库。对你现在的 GLP1R 项目，更合适的是建立一个**靶点定向的小型同源序列库**：只收集 GLP1R 及其进化相关受体的序列，再进行本地比对，生成 Boltz-2 能使用的 MSA。

先说明一个关键区别：ColabFold 的 UniRef30、环境序列库等包含大量不同蛋白质，完整下载体积很大；官方数据库页面列出的 UniRef30 单个数据库压缩包就有约 103 GB。<Cite refs={["turn268492search0","turn268492search9"]}/> 我们可以绕过这一步，但小型定向 MSA 不会与完整数据库搜索得到的 MSA 完全等价。

## 推荐方案：下载 GLP1R 同源序列，生成一个小型本地 MSA

我们可以从 UniProt 下载注释为 GLP1R 的蛋白序列，再过滤、比对并生成 `.a3m`。UniProt 支持通过 REST API 按蛋白注释查询并直接导出 FASTA。<Cite refs={["turn694283search2","turn694283search5"]}/>

### 第一步glp1r_homologs_raw.fasta
```

这个请求下载的是 UniProt 中匹配 `GLP1R` 基因字段的记录，**并不保证覆盖所有 GLP1R 直系同源蛋白**。下载后需要检查物种、序列长度和注释，避免把其他相关受体混glp1r_homologs_raw.fasta
```

分别查看序列条数、FASTA 标题和文件大小。

### 第三步：不要急着直接生成 MSA

这里有一个与你的项目直接相关的问题：你的 GLP1R 输入链是 **384 aa**，而数据库中的 GLP1R 序列可能是更长的全长序列。如果直接把这些序列进行多序列比对，最终对齐长度可能与 Boltz 输入链不一致。

因此，我们还需要：

1. 确认输入的 384 aa 对应 GLP1R 的哪一段。
2. 筛选真正的 GLP1R 同源序列，去除重复和明显不匹配的序列。
3. 将同源序列正确映射到输入受体序列。
4. 生成与输入链长度、残基顺序兼容的 `.a3m` 文件。

我不建议现在就给你一条未经验证的转换命令，因为如果 MSA 的查询序列与输入链没有正确对应，Boltz 可能无法使用它，或导致残基对应错误。

## 下一步

先运行上面的下载命令，把以下两项结果贴给我：

- `grep -c '^>' glp1r_homologs_raw.fasta` 的输出；
- `head -20 glp1r_homologs_raw.fasta` 的输出。

我会据此帮你判断下载结果是否合适，再确定过滤和生成 `.a3m` 的具体步骤。整个方案不需要下载完整 ColabFold 数据库。

等 MSA 成功生成后，我也可以提醒你检查它与 384 aa 输入链的对应关系，再启动 Boltz-2 小规模测试。

---

# you asked

message time: 2026-10-22 10:14:10

% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  254k    0  254k    0     0  86493      0 --:--:--  0:00:03 --:--:-- 86506
(base) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH grep -c '^>' glp1r_homologs_raw.fasta
head -20 glp1r_homologs_raw.fasta
du -h glp1r_homologs_raw.fasta
476
>sp|P43220|GLP1R_HUMAN Glucagon-like peptide 1 receptor OS=Homo sapiens OX=9606 GN=GLP1R PE=1 SV=2
MAGAPGPLRLALLLLGMVGRAGPRPQGATVSLWETVQKWREYRRQCQRSLTEDPPPATDL
FCNRTFDEYACWPDGEPGSFVNVSCPWYLPWASSVPQGHVYRFCTAEGLWLQKDNSSLPW
RDLSECEESKRGERSSPEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIH
LNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAAN
YYWLLVEGVYLYTLLAFSVLSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRN
SNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANLMCKTDIKCRLAKSTLTLIPLL
GTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERW
RLEHLHIQRDSSMKPLKCPTSSLSSGATAGSSMYTATCQASCS
>sp|O35659|GLP1R_MOUSE Glucagon-like peptide 1 receptor OS=Mus musculus OX=10090 GN=Glp1r PE=1 SV=2
MASTPSLLRLALLLLGAVGRAGPRPQGTTVSLSETVQKWREYRRQCQRFLTEAPLLATGL
FCNRTFDDYACWPDGPPGSFVNVSCPWYLPWASSVLQGHVYRFCTAEGLWLHKDNSSLPW
RDLSECEESKRGERNFPEEQLLSLYIIYTVGYALSFSALVIASAILVGFRHLHCTRNYIH
LNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLGCRLVFLLMQYCVAAN
YYWLLVEGVYLYTLLAFSVFSEQRIFKLYLSIGWGVPLLFVIPWGIVKYLYEDEGCWTRN
SNMNYWLIIRLPILFAIGVNFLIFIRVICIVVSKLKANLMCKTDIKCRLAKSTLTLIPLL
GTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQMEFRKCWERW
RLEHLNIQRDCSMKPLKCPTSSVSSGATVGSSVYAATCQSSYS
>sp|P32301|GLP1R_RAT Glucagon-like peptide 1 receptor OS=Rattus norvegicus OX=10116 GN=Glp1r PE=2 SV=1
MAVTPSLLRLALLLLGAVGRAGPRPQGATVSLSETVQKWREYRHQCQRFLTEAPLLATGL
256K    glp1r_homologs_raw.fasta
(base) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH

---

# chatgpt response

很好，下载成功了，而且结果比预期更有用：你现在有 **476 条 UniProt 检索结果，文件只有约 256 KB**，不需要额外下载大型序列数据库。

从你贴出的前几条看，结果至少包含人、小鼠和大鼠的 GLP1R 序列。这些序列有助于构建受体 MSA，但还不能直接把这 476 条全部当成合格的同源序列：需要进一步检查重复、序列长度、注释和与输入受体的对应关系。

**现在先不要把整个 FASTA 直接转成 `.a3m`。** 你的 Boltz 输入受体是 384 aa，而 UniProt 示例里的 GLP1R 是全长序列；需要先弄清楚这 384 aa 是哪一段。

## 现在请再做一次小检查

UniProt 的人源 GLP1R 标准序列长度是 **463 aa**，所以我们需要先确认 384 aa 输入链对应的具体区域。<Cite refs={["turn606972search0"]}/>

在当前目录执行下面的命令，统计{h}")
PY
```

然后，再找一下你之前用于 Boltz-2 预测的 YAML 或 Fhead -50
```

把这两段输出发给我。

下一步我们就能根据**实际的 384 aa 受体序列**筛选合适的同源序列，生成与输入链对应的 MSA，而不是把全长 GLP1R 序列不加处理地塞进 Boltz-2。这样也能避免 MSA 残基错位，影响后续候选排序。

---

# you asked

message time: 2026-10-22 10:15:12

431 aa | tr|A0A7K4V3N1|A0A7K4V3N1_9EMBE Glucagon-like peptide 1 receptor (Fragment) OS=Emberiza fucata OX=337179 GN=Glp1r PE=3 SV=1
 383 aa | tr|A0A7K4YGL0|A0A7K4YGL0_BUCAB GLP1R protein (Fragment) OS=Bucorvus abyssinicus OX=153643 GN=Glp1r PE=4 SV=1
 431 aa | tr|A0A7K5J3A2|A0A7K5J3A2_TOXRE Glucagon-like peptide 1 receptor (Fragment) OS=Toxostoma redivivum OX=99882 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K5MQ00|A0A7K5MQ00_CARCD Glucagon-like peptide 1 receptor (Fragment) OS=Cardinalis cardinalis OX=98964 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K5P7G5|A0A7K5P7G5_9CORV Glucagon-like peptide 1 receptor (Fragment) OS=Erythrocercus mccallii OX=107208 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K5SDS9|A0A7K5SDS9_LANLU Glucagon-like peptide 1 receptor (Fragment) OS=Lanius ludovicianus OX=28713 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K5TFV9|A0A7K5TFV9_9FRIN Glucagon-like peptide 1 receptor (Fragment) OS=Urocynchramus pylzowi OX=571890 GN=Glp1r PE=3 SV=1
 367 aa | tr|A0A7K5TZ37|A0A7K5TZ37_CEPOR GLP1R protein (Fragment) OS=Cephalopterus ornatus OX=114276 GN=Glp1r PE=4 SV=1
 431 aa | tr|A0A7K6H0H0|A0A7K6H0H0_9PASS Glucagon-like peptide 1 receptor (Fragment) OS=Malurus elegans OX=720584 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K6HCZ0|A0A7K6HCZ0_9PASS Glucagon-like peptide 1 receptor (Fragment) OS=Dasyornis broadbenti OX=243059 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K6K3B1|A0A7K6K3B1_9PASE Glucagon-like peptide 1 receptor (Fragment) OS=Oreocharis arfaki OX=979223 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K6NNR3|A0A7K6NNR3_PEDTO Glucagon-like peptide 1 receptor (Fragment) OS=Pedionomus torquatus OX=227192 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K6RAP3|A0A7K6RAP3_9PASS Glucagon-like peptide 1 receptor (Fragment) OS=Climacteris rufus OX=47695 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K6Y3U8|A0A7K6Y3U8_9PASE Glucagon-like peptide 1 receptor (Fragment) OS=Promerops cafer OX=254652 GN=Glp1r PE=3 SV=1
 367 aa | tr|A0A7K7E153|A0A7K7E153_9SYLV GLP1R protein (Fragment) OS=Sylvia atricapilla OX=48155 GN=Glp1r PE=4 SV=1
 431 aa | tr|A0A7K7G2S9|A0A7K7G2S9_ERIRU Glucagon-like peptide 1 receptor (Fragment) OS=Erithacus rubecula OX=37610 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K7IPY7|A0A7K7IPY7_LOXCU Glucagon-like peptide 1 receptor (Fragment) OS=Loxia curvirostra OX=64802 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K7XKR2|A0A7K7XKR2_9PASS Glucagon-like peptide 1 receptor (Fragment) OS=Mohoua ochrocephala OX=874463 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K8GE20|A0A7K8GE20_ORTSP Glucagon-like peptide 1 receptor (Fragment) OS=Orthonyx spaldingii OX=38397 GN=Glp1r PE=3 SV=1
 367 aa | tr|A0A7K8I138|A0A7K8I138_9CORV GLP1R protein (Fragment) OS=Aleadryas rufinucha OX=461220 GN=Glp1r PE=4 SV=1
 374 aa | tr|A0A7K8L721|A0A7K8L721_9AVES GLP1R protein (Fragment) OS=Ardeotis kori OX=89386 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K8M2F7|A0A7K8M2F7_9CORV Glucagon-like peptide 1 receptor (Fragment) OS=Ptilorrhoa leucosticta OX=449384 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K8P1C9|A0A7K8P1C9_COCCO Glucagon-like peptide 1 receptor (Fragment) OS=Cochlearius cochlearius OX=110676 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K8QPE1|A0A7K8QPE1_9PASS Glucagon-like peptide 1 receptor (Fragment) OS=Smithornis capensis OX=363769 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K9A2S3|A0A7K9A2S3_9PASS Glucagon-like peptide 1 receptor (Fragment) OS=Grallaria varia OX=117165 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K9HRL3|A0A7K9HRL3_9PICI Glucagon-like peptide 1 receptor (Fragment) OS=Bucco capensis OX=135168 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K9LQ23|A0A7K9LQ23_9PASS Glucagon-like peptide 1 receptor (Fragment) OS=Rhabdornis inornatus OX=237438 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K9MEY9|A0A7K9MEY9_OCETE Glucagon-like peptide 1 receptor (Fragment) OS=Oceanodroma tethys OX=79633 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K9TAG0|A0A7K9TAG0_9PICI Glucagon-like peptide 1 receptor (Fragment) OS=Galbula dea OX=1109041 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K9UTG8|A0A7K9UTG8_ANSSE Glucagon-like peptide 1 receptor (Fragment) OS=Anseranas semipalmata OX=8851 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7K9W0E5|A0A7K9W0E5_9PASS Glucagon-like peptide 1 receptor (Fragment) OS=Rhipidura dahli OX=667186 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7L0D1T1|A0A7L0D1T1_9CHAR Glucagon-like peptide 1 receptor (Fragment) OS=Rostratula benghalensis OX=118793 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7L0G4N7|A0A7L0G4N7_HERCA Glucagon-like peptide 1 receptor (Fragment) OS=Herpetotheres cachinnans OX=56343 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7L0IET0|A0A7L0IET0_PIPCL Glucagon-like peptide 1 receptor (Fragment) OS=Piprites chloris OX=114369 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7L0KGB7|A0A7L0KGB7_CHATO Glucagon-like peptide 1 receptor (Fragment) OS=Chauna torquata OX=30388 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7L0QI36|A0A7L0QI36_SETKR Glucagon-like peptide 1 receptor (Fragment) OS=Setophaga kirtlandii OX=298831 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7L0SEY8|A0A7L0SEY8_PODPO Glucagon-like peptide 1 receptor (Fragment) OS=Podilymbus podiceps OX=9252 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7L0TP40|A0A7L0TP40_CHOAC Glucagon-like peptide 1 receptor (Fragment) OS=Chordeiles acutipennis OX=118183 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7L1B431|A0A7L1B431_GYMTI Glucagon-like peptide 1 receptor (Fragment) OS=Gymnorhina tibicen OX=9132 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7L1DVM1|A0A7L1DVM1_OENON Glucagon-like peptide 1 receptor (Fragment) OS=Oenanthe oenanthe OX=279966 GN=Glp1r PE=3 SV=1
 367 aa | tr|A0A7L1F5Q8|A0A7L1F5Q8_SYLBO GLP1R protein (Fragment) OS=Sylvia borin OX=73324 GN=Glp1r PE=4 SV=1
 431 aa | tr|A0A7L1H9N5|A0A7L1H9N5_9CHAR Glucagon-like peptide 1 receptor (Fragment) OS=Nycticryphes semicollaris OX=227226 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7L1KLJ9|A0A7L1KLJ9_HIMHI Glucagon-like peptide 1 receptor (Fragment) OS=Himantopus himantopus OX=225398 GN=Glp1r PE=3 SV=1
 407 aa | tr|A0A7L1NVQ1|A0A7L1NVQ1_RHICY GLP1R protein (Fragment) OS=Rhinopomastus cyanomelas OX=113115 GN=Glp1r PE=3 SV=1
 367 aa | tr|A0A7L2E4U9|A0A7L2E4U9_ANTMN GLP1R protein (Fragment) OS=Anthoscopus minutus OX=156561 GN=Glp1r PE=4 SV=1
 431 aa | tr|A0A7L2FRC9|A0A7L2FRC9_QUIME Glucagon-like peptide 1 receptor (Fragment) OS=Quiscalus mexicanus OX=64278 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7L2L0D1|A0A7L2L0D1_9PASS Glucagon-like peptide 1 receptor (Fragment) OS=Zosterops hypoxanthus OX=2485327 GN=Glp1r PE=3 SV=1
 367 aa | tr|A0A7L2SLP9|A0A7L2SLP9_9PASS GLP1R protein (Fragment) OS=Mystacornis crossleyi OX=98133 GN=Glp1r PE=4 SV=1
 431 aa | tr|A0A7L2Y7M4|A0A7L2Y7M4_JACJC Glucagon-like peptide 1 receptor (Fragment) OS=Jacana jacana OX=54508 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7L3D9U6|A0A7L3D9U6_PLUSO Glucagon-like peptide 1 receptor (Fragment) OS=Pluvianellus socialis OX=227228 GN=Glp1r PE=3 SV=1
 374 aa | tr|A0A7L3JTK4|A0A7L3JTK4_THACH GLP1R protein (Fragment) OS=Thalassarche chlororhynchos OX=54017 GN=Glp1r PE=4 SV=1
 431 aa | tr|A0A7L3S1K8|A0A7L3S1K8_CEPGR Glucagon-like peptide 1 receptor (Fragment) OS=Cepphus grylle OX=28697 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7L3XSC8|A0A7L3XSC8_9AVES Glucagon-like peptide 1 receptor (Fragment) OS=Calonectris borealis OX=1323832 GN=Glp1r PE=3 SV=1
 367 aa | tr|A0A7L4JPV7|A0A7L4JPV7_9AVES GLP1R protein (Fragment) OS=Ceuthmochares aereus OX=1961834 GN=Glp1r PE=4 SV=1
 431 aa | tr|A0A7L4KTL0|A0A7L4KTL0_9CORV Glucagon-like peptide 1 receptor (Fragment) OS=Callaeas wilsoni OX=1347786 GN=Glp1r PE=3 SV=1
 367 aa | tr|A0A7L4MD15|A0A7L4MD15_GLAPT GLP1R protein (Fragment) OS=Glareola pratincola OX=43316 GN=Glp1r PE=4 SV=1
 431 aa | tr|A0A851PKH7|A0A851PKH7_ANHAN Glucagon-like peptide 1 receptor (Fragment) OS=Anhinga anhinga OX=56067 GN=Glp1r PE=3 SV=1
 366 aa | tr|A0A852IQC5|A0A852IQC5_9PICI GLP1R protein (Fragment) OS=Tricholaema leucomelas OX=240729 GN=Glp1r PE=4 SV=1
 431 aa | tr|A0A8J4NKD2|A0A8J4NKD2_EUDMI Glucagon-like peptide 1 receptor (Fragment) OS=Eudyptula minor OX=37083 GN=Glp1r PE=3 SV=1
 461 aa | tr|A0AAD8D5Y5|A0AAD8D5Y5_ACIOX Glucagon-like peptide 1 receptor OS=Acipenser oxyrinchus oxyrinchus OX=40147 GN=Glp1r PE=3 SV=1
 431 aa | tr|A0A7L2NUK5|A0A7L2NUK5_PYCJO Glucagon-like peptide 1 receptor (Fragment) OS=Pycnonotus jocosus OX=182897 GN=Glp1r_0 PE=3 SV=1
 431 aa | tr|A0A851J4S1|A0A851J4S1_9PASS Glucagon-like peptide 1 receptor (Fragment) OS=Donacobius atricapilla OX=237420 GN=Glp1r_0 PE=3 SV=1
 431 aa | tr|A0A7L0HP99|A0A7L0HP99_AREIN Glucagon-like peptide 1 receptor (Fragment) OS=Arenaria interpres OX=54971 GN=Glp1r_0 PE=3 SV=1
 431 aa | tr|A0A7L4H4J5|A0A7L4H4J5_PODST Glucagon-like peptide 1 receptor (Fragment) OS=Podargus strigoides OX=8905 GN=Glp1r_1 PE=3 SV=1
 367 aa | tr|A0A852PCL1|A0A852PCL1_9PASS GLP1R protein (Fragment) OS=Atrichornis clamosus OX=449594 GN=Glp1r_1 PE=4 SV=1
 464 aa | tr|A0ABI8A1H3|A0ABI8A1H3_FELCA G-protein coupled receptors family 2 profile 2 domain-containing protein OS=Felis catus OX=9685 GN=GLP1R PE=4 SV=1
(base) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH find LOCAL_PATH -type f \
  $ -name "*.yaml" -o -name "*.yml" -o -name "*.fasta" -o -name "*.fa" $ \
  2>/dev/null | head -50
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
(base) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH

---

# chatgpt response

这两段输出已经能确定一个关键问题：**你下载到的 476 条序列不能直接拼成 Boltz-2 的 `.a3m`。** 里面有很多鸟类 GLP1R 条目，长度集中在 431 aa，也有 367、383 aa 等不同长度的片段。长度不同本身不代表不能用于 MSA，但必须先做序列比对、去冗余和覆盖度筛选，不能把它们直接截成 384 aa。

另外，你找到了两个很有用的本地参考文件：

- `LOCAL_PATH
- `LOCAL_PATH

下一步应该先确认 **Boltz 输入受体 A 的 384 aa 序列究竟对应人 GLP1R 的哪一段**，再围绕它建立 MSA。这样可以避免 MSA 的 query 与实际输入序列不一致。

请在 WSL 里运行下面这组命令。它只读取文件，不会修改你的数据。

### 1. 检查现有 GLP1R 序列

`
### 2. 找出 GLP1R 项目中实际使用的 Boltz 输入配置

``然后把上面两步的输出发给我。

**为什么先做这一步？** 我们要确定 384 aa 的受体输入与 7KI0 的 GLP1R 链 R 之间的对应关系。确认之后，我会给你一份完整脚本，用这 476 条 UniProt 序列进行筛选、比对并生成适用于 Boltz-2 的 MSA；不会直接截取序列，也不会把低覆盖度或明显不合适的条目硬塞进去。

---

# you asked

message time: 2026-10-22 10:16:32

======================================================================
FILE: LOCAL_PATH
>GLP1R_7KI0_chainR | GLP-1 receptor construct as recorded in PDB 7KI0
length=491
start: MKTIIALSYIFCLVFADYKDDDDLEVLFQGPARPQGATVSLWETV
end:   CPTSSLSSGATAGSSMYTATCQASCSPAGLEVLFQGPHHHHHHHH
records: 1

======================================================================
FILE: LOCAL_PATH
>semaglutide_7KI0_chainP | Semaglutide peptide as recorded in PDB 7KI0
length=31
start: HAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG
end:   HAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG
records: 1

======================================================================
FILE: LOCAL_PATH
>GLP1R_D13
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSSYLEEQAAKAFVERLKRGRG
records: 1

======================================================================
FILE: LOCAL_PATH
>candidate_0003
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEKQVKAFVERLKRGGG
>candidate_0009
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEKAAKAFVDRLKRGSG
>candidate_0015
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSSYLEEKAVKQFVDRLKRGGG
>candidate_0021
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEKAAKAFVERLKRGGG
>candidate_0027
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSSYLEEKAAKAFVERLKRGGG
>candidate_0033
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEKQVKAFVDRLKRGGG
>candidate_0039
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEKAVKQFVERLKRGSG
>candidate_0045
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSSYLEEKAAKAFVERLKRGSG
>candidate_0051
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEKAAKDFVERLKRGGG
>candidate_0057
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEKAAKQFVDRLKRGAG
>candidate_0063
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEKQVKAFVERLKRGAG
>candidate_0069
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEQQAKAFVERLKRGSG
>candidate_0075
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSSYLEEKQAKAFVDRLKRGRG
>candidate_0081
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSSYLEEKAAKAFVDRLKRGAG
>candidate_0087
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEKAVKAFVDRLKRGSG
>candidate_0093
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSSYLEEKAVKNFVDRLKRGRG
>candidate_0099
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSSYLETKAAKAFVDRLKRGGG
>candidate_0105
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSSYLEEKQAKAFVDRLKRGAG
>candidate_0111
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEKAAKDFVERLKRGAG
>candidate_0117
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSSYLEEKQAKSFVERLKRGSG
>candidate_0123
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSSYLEEKQVKQFVERLKRGRG
>candidate_0129
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEQAAKNFVERLKRGRG
>candidate_0135
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSTYLEEKQAKQFVDRLKRGGG
>candidate_0141
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSSYLEEKQVKSFVDRLKRGGG
>candidate_0147
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEQQVKAFVERLRRGGG
>candidate_0153
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSTYLEEKAVKQFVERLKRGGG
>candidate_0159
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEQQAKAFVDRLKRGRG
>candidate_0165
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSSYLEEQAAKAFVERLKRGRG
>candidate_0171
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEQAAKAFVERLKRGGG
>candidate_0177
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEKQAKAFVERLRRGSG
>candidate_0183
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEKAAKDFVERLKRGSG
>candidate_0189
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSSYLEERQAKAFVERLKRGRG
>candidate_0195
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEKAVKSFVDRLKRGSG
>candidate_0201
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSSYLEEKAAKQFVERLKRGAG
>candidate_0207
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEKAAKQFVERLKRGLG
>candidate_0213
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSSYLEEKAVKDFVERLKRGRG
>candidate_0219
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSSYLEEKAAKDFVERLKRGRG
>candidate_0225
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSSYLEEKAVKQFVERLKRGAG
>candidate_0231
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEQQAKAFVERLKRGAG
>candidate_0237
length=416
start: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWP
end:   LEFRKSWERWRLE:HAEGTFTSDVSRYLEEQAVKAFVDRLKRGSG
records: 40

---

# chatgpt response

这次输出很有价值：`GLP1R_D13.fasta` 和 `batch_2.fasta` 里的序列使用 `:` 分隔受体与肽链。以你给出的长度看，416 个字符对应 **384 aa 受体 + 1 个分隔符 + 31 aa 肽链**。因此，我们可以从现有输入中提取受体的准确查询序列，而不必猜它对应人 GLP1R 的哪些残基。

还有一个需要注意的地方：`GLP1R_7KI0_chainR.fasta` 长度为 491 aa，包含 PDB 构建体的额外序列，不能直接拿它作为 MSA 的 query。

## 下一步：确认输入格式和本地工具

请在 WSL 终端执行下面这段命令。它会检查受体链、肽链的实际长度，并确认有没有可用的序列比对程序。



接着检查 GLP1R 项目中的 Boltz 配置文件：



把这两段命令的输出贴过来即可。

拿到结果后，我会按实际环境给你一份**完整的 MSA 构建脚本**，而不是让你手动处理 476 条序列。流程会是：

1. 从实际输入提取 384 aa 受体 query。
2. 过滤明显不合适的序列，避免低覆盖度片段干扰。
3. 将同源序列与 query 进行多序列比对。
4. 检查 query 是否与 Boltz 输入严格一致，再生成 `.a3m`。
5. 保留筛选统计和质量检查结果，便于之后复现。

在确认序列对应关系和比对工具之前，先不要把全部 476 条序列直接写入 `.a3m`。

---

# you asked

message time: 2026-10-22 10:17:24

=== LOCAL_PATH ===
Traceback (most recent call last):
  File "<stdin>", line 27, in <module>
NameError: name 'print_record' is not defined

=== Alignment tools ===
USER_HOME/miniconda3/bin/mafft

=== Boltz executable ===
(base) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH find LOCAL_PATH \
     LOCAL_PATH \
     -type f $ -name "*.yaml" -o -name "*.yml" $ \
     2>/dev/null
(base) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH

---

# chatgpt response

这个报错是我上一条命令里的代码顺序有问题：`print_record()` 在定义之前就被调用了，抱歉。它没有修改任何文件。

另外，当前环境能找到 `mafft`，这是好消息；但 `command -v boltz` 没有输出，只能说明当前 `base` 环境的 PATH 里没找到 `boltz`，**不能据此判断 Boltz-2 没安装**。我们先修正序列检查，再切换到你实际使用的 Boltz 环境确认配置格式。

直接用下面修正版即可。这次会正确读取 FASTA，并把 `:` 分隔的受体链和肽链分别统计出来。

### 1. 修正序列检查脚本

```bash
python - <<'PY'
from pathlib import Path

def read_fasta(path):
    records = []
    header = None
    parts = []

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    records.append((header, "".join(parts)))
                header = line[1:]
                parts = []
            else:
                parts.append(line)

    if header is not None:
        records.append((header, "".join(parts)))

    return records


files = [
    "LOCAL_PATH",
    "LOCAL_PATH",
    "LOCAL_PATH",
    "LOCAL_PATH",
]

for filename in files:
    path = Path(filename)
    print(f"\n{'=' * 72}\nFILE: {path}")

    if not path.exists():
        print("NOT FOUND")
        continue

    records = read_fasta(path)
    print("records:", len(records))

    for header, seq in records[:3]:
        print(f"\n>{header}")
        print("total length:", len(seq))

        chains = seq.split(":")
        print("chain lengths:", [len(s) for s in chains])

        for i, chain in enumerate(chains, start=1):
            print(
                f"chain {i}: length={len(chain)}, "
                f"start={chain[:25]}, end={chain[-25:]}"
            )

        invalid = sorted(set(seq.upper()) - set(
            "ACDEFGHIKLMNPQRSTVWY:X"
        ))
        if invalid:
            print("nonstandard characters:", invalid)
PY
```

### 2. 确认 Boltz-2 安装在哪个环境

你现在处于 `(base)` 环境，所以暂时找不到 `boltz` 不代表它没有安装。继续运行：

`
如果第二条命令找到类似下面的路径：

`
再用实际找到的路径检查版本和参数，例如：

`
请把两步输出贴过来。

**目前先不要生成 MSA。** 我们已经知道 `GLP1R_D13.fasta` 里有受体与肽链的拼接格式，但还需要确认实际受体序列、Boltz 使用的输入配置，以及本地版本支持的 MSA 格式。确认后再生成文件，才能保证 query 与预测输入严格一致。

---

# you asked

message time: 2026-10-22 10:19:04

========================================================================
FILE: LOCAL_PATH
records: 1

>GLP1R_D13
total length: 416
chain lengths: [384, 31]
chain 1: length=384, start=TVSLWETVQKWREYRRQCQRSLTED, end=AILYCFVNNEVQLEFRKSWERWRLE
chain 2: length=31, start=HAEGTFTSDVSSYLEEQAAKAFVER, end=TSDVSSYLEEQAAKAFVERLKRGRG

========================================================================
FILE: LOCAL_PATH
records: 40

>candidate_0003
total length: 416
chain lengths: [384, 31]
chain 1: length=384, start=TVSLWETVQKWREYRRQCQRSLTED, end=AILYCFVNNEVQLEFRKSWERWRLE
chain 2: length=31, start=HAEGTFTSDVSRYLEEKQVKAFVER, end=TSDVSRYLEEKQVKAFVERLKRGGG

>candidate_0009
total length: 416
chain lengths: [384, 31]
chain 1: length=384, start=TVSLWETVQKWREYRRQCQRSLTED, end=AILYCFVNNEVQLEFRKSWERWRLE
chain 2: length=31, start=HAEGTFTSDVSRYLEEKAAKAFVDR, end=TSDVSRYLEEKAAKAFVDRLKRGSG

>candidate_0015
total length: 416
chain lengths: [384, 31]
chain 1: length=384, start=TVSLWETVQKWREYRRQCQRSLTED, end=AILYCFVNNEVQLEFRKSWERWRLE
chain 2: length=31, start=HAEGTFTSDVSSYLEEKAVKQFVDR, end=TSDVSSYLEEKAVKQFVDRLKRGGG

========================================================================
FILE: LOCAL_PATH
records: 1

>GLP1R_7KI0_chainR | GLP-1 receptor construct as recorded in PDB 7KI0
total length: 491
chain lengths: [491]
chain 1: length=491, start=MKTIIALSYIFCLVFADYKDDDDLE, end=CQASCSPAGLEVLFQGPHHHHHHHH

========================================================================
FILE: LOCAL_PATH
records: 1

>semaglutide_7KI0_chainP | Semaglutide peptide as recorded in PDB 7KI0
total length: 31
chain lengths: [31]
chain 1: length=31, start=HAEGTFTSDVSSYLEGQAAKEFIAW, end=TSDVSSYLEGQAAKEFIAWLVRGRG
(base) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH ziguimu@DESKTOP-8RLFC97:LOCAL_PATH conda activate boltz
(boltz) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH

---

# chatgpt response

现在已经确认了关键输入：**受体链 A 是 384 aa，肽链 B 是 31 aa**，中间用 `:` 分隔。`batch_2.fasta` 中的 40 个候选使用相同的受体序列，因此我们可以只为受体构建一份自定义 MSA，让 Boltz-2 对不同肽链使用同一套受体进化信息。

有两个地方需要特别注意：

- **MSA 必须匹配实际输入的 384 aa 受体序列**，不能直接拿 491 aa 的 7KI0 构建序列作为查询序列；后者含有额外的构建片段和标签。
- UniProt 下载的 476 条记录还需要经过序列覆盖度、相似性和重复序列筛选，不能不加区分地全部塞进 MSA。

接下来先确认你激活的 `boltz` 环境里有哪些命令和工具，再生成 MSA。这样可以避免 MSA 格式正确、但 Boltz 配置或运行方式不匹配的情况。

## 第一步：确认 Boltz-2 环境和版本

你现在已经进入 `(boltz)` 环境了。请直接复制运行下面这组命令：



把完整输出发给我，尤其是 `boltz --help` 和 `pip show boltz` 的结果。

## 第二步：核实 384 aa 受体序列与 UniProt 参考序列的关系

这一步很重要：你的 384 aa 序列可能是受体的特定结构域范围，而不是完整的天然 GLP-1R。我们要确认它在完整人源 GLP-1R 序列中的位置，才能正确筛选同源序列并评估覆盖度。

先运行：



这里的“精确子串位置”若返回 `-1`，**不代表序列不匹配**，因为目标输入可能缺少天然序列中的片段，或者经过了截取。我们会结合比对结果判断，而不是直接据此丢弃序列。

拿到这两组输出后，就可以继续确定：**同源序列筛选标准 → MAFFT 多序列比对 → 转换为 Boltz-2 能识别的 MSA 格式 → 检查查询序列与配置文件是否一致**。

---

# you asked

message time: 2026-10-22 10:19:47

(base) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH conda activate boltz
(boltz) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH echo "=== Python ==="
which python
python --version

echo
echo "=== Boltz executable ==="
which boltz
boltz --help | head -80

echo
echo "=== Installed Boltz package ==="
python -m pip show boltz

echo
echo "=== Alignment tool ==="
which mafft
mafft --version

echo
echo "=== Raw UniProt records ==="
grep -c '^>' LOCAL_PATH
=== Python ===
USER_HOME/miniconda3/envs/boltz/bin/python
Python 3.11.16

=== Boltz executable ===
USER_HOME/miniconda3/envs/boltz/bin/boltz
Usage: boltz [OPTIONS] COMMAND [ARGS]...

  Boltz.

Options:
  --help  Show this message and exit.

Commands:
  predict  Run predictions with Boltz.

=== Installed Boltz package ===
Name: boltz
Version: 2.2.1
Summary: Boltz
Home-page:
Author:
Author-email:
License:
Location: USER_HOME/miniconda3/envs/boltz/lib/python3.11/site-packages
Requires: biopython, chembl_structure_pipeline, click, dm-tree, einops, einx, fairscale, gemmi, hydra-core, mashumaro, modelcif, numba, numpy, pandas, pytorch-lightning, pyyaml, rdkit, requests, scikit-learn, scipy, torch, types-requests, wandb
Required-by:

=== Alignment tool ===
Command 'mafft' not found, but can be installed with:
sudo apt install mafft

=== Raw UniProt records ===
476
(boltz) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH

---

# chatgpt response

很好，环境信息已经明确：

- **Boltz 2.2.1** 已安装，路径是 `USER_HOME/miniconda3/envs/boltz/bin/boltz`。
- Python 是 3.11.16。
- 当前 `boltz` 环境里找不到 `mafft`，但之前在 base 环境中找到过它：`USER_HOME/miniconda3/bin/mafft`。**暂时不需要重新安装**，可以先用绝对路径调用。
- UniProt 原始文件有 476 条序列，尚未筛选。

现在先核实参考序列，并检查 Boltz 2.2.1 的实际参数。请在当前 `(boltz)` 环境中运行下面两组命令。

## 1. 核实 GLP-1R 参考序列

`
这一步主要确认人、小鼠、大鼠 GLP-1R 参考序列是否存在，以及目标受体序列是否能在完整参考序列中定位。暂时不要据此删除任何记录。

## 2. 检查 Boltz 的预测参数和 MAFFT

``把这两组命令的输出发给我。

**下一步的处理原则：**先筛选并比对同源序列，再生成与 384 aa 受体链完全对应的 MSA；31 aa 肽链继续使用 `msa: empty`。在确认 Boltz 2.2.1 的输入配置规则之前，先不生成最终 YAML，也不启动正式预测。这样能减少因链映射或 MSA 格式错误造成的无效计算。

---

# you asked

message time: 2026-10-22 10:20:21

Target receptor length: 384
UniProt records: 476

--- P43220 ---
sp|P43220|GLP1R_HUMAN Glucagon-like peptide 1 receptor OS=Homo sapiens OX=9606 GN=GLP1R PE=1 SV=2
Length: 463
Exact target substring position: -1
Target prefix position: 28
Sequence start: MAGAPGPLRLALLLLGMVGRAGPRPQGATVSLWETVQKWR

--- O35659 ---
sp|O35659|GLP1R_MOUSE Glucagon-like peptide 1 receptor OS=Mus musculus OX=10090 GN=Glp1r PE=1 SV=2
Length: 463
Exact target substring position: -1
Target prefix position: -1
Sequence start: MASTPSLLRLALLLLGAVGRAGPRPQGTTVSLSETVQKWR

--- P32301 ---
sp|P32301|GLP1R_RAT Glucagon-like peptide 1 receptor OS=Rattus norvegicus OX=10116 GN=Glp1r PE=2 SV=1
Length: 463
Exact target substring position: -1
Target prefix position: -1
Sequence start: MAVTPSLLRLALLLLGAVGRAGPRPQGATVSLSETVQKWR
(boltz) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH

---

# chatgpt response

这个结果给出了一个重要线索：**384 aa 的受体输入与人源 GLP-1R（P43220）高度可能存在序列对应关系，但目前不能认为它是完整人源序列的无修改截取。**

- 人源参考序列长 463 aa。
- 目标序列前 30 aa 能在参考序列的第 29 个零基索引位置找到。
- 但完整的 384 aa 目标序列不是参考序列中的精确连续子串，因此还需要检查是否存在替换、缺失或其他构建差异。

在生成 MSA 前，先做一次全局比对，避免把错误的序列映射带进后续预测。

## 1. 比对目标受体与人源 GLP-1R

请在当前 `(boltz)` 环境运行：

`
## 2. 请补上 Boltz 参数检查结果

上一条我还请你运行了下面这两条命令，但目前看到的输出里还没有它们：

``请把这两部分输出也发来。

接下来我会根据实际比对结果确定目标序列与天然受体的映射，再制定同源序列筛选规则。**目前不建议直接把 476 条原始 UniProt 序列全部对齐后当作最终 MSA**：序列长度相近不代表覆盖了正确区域，也不代表每条记录都是可靠的同源序列。

---

# you asked

message time: 2026-10-22 10:21:28

Run predictions with Boltz.

Options:
  --out_dir PATH                  The path where to save the predictions.
  --cache PATH                    The directory where to download the data and
                                  model. Default is ~/.boltz, or $BOLTZ_CACHE
                                  if set.
  --checkpoint PATH               An optional checkpoint, will use the
                                  provided Boltz-1 model by default.
  --devices INTEGER               The number of devices to use for prediction.
                                  Default is 1.
  --accelerator [gpu|cpu|tpu]     The accelerator to use for prediction.
                                  Default is gpu.
  --recycling_steps INTEGER       The number of recycling steps to use for
                                  prediction. Default is 3.
  --sampling_steps INTEGER        The number of sampling steps to use for
                                  prediction. Default is 200.
  --diffusion_samples INTEGER     The number of diffusion samples to use for
                                  prediction. Default is 1.
  --max_parallel_samples INTEGER  The maximum number of samples to predict in
                                  parallel. Default is None.
  --step_scale FLOAT              The step size is related to the temperature
                                  at which the diffusion process samples the
                                  distribution. The lower the higher the
                                  diversity among samples (recommended between
                                  1 and 2). Default is 1.638 for Boltz-1 and
                                  1.5 for Boltz-2. If not provided, the
                                  default step size will be used.
  --write_full_pae                Whether to dump the pae into a npz file.
                                  Default is True.
  --write_full_pde                Whether to dump the pde into a npz file.
                                  Default is False.
  --output_format [pdb|mmcif]     The output format to use for the
                                  predictions. Default is mmcif.
  --num_workers INTEGER           The number of dataloader workers to use for
                                  prediction. Default is 2.
  --override                      Whether to override existing found
                                  predictions. Default is False.
  --seed INTEGER                  Seed to use for random number generator.
                                  Default is None (no seeding).
  --use_msa_server                Whether to use the MMSeqs2 server for MSA
                                  generation. Default is False.
  --msa_server_url TEXT           MSA server url. Used only if
                                  --use_msa_server is set.
  --msa_pairing_strategy TEXT     Pairing strategy to use. Used only if
                                  --use_msa_server is set. Options are
                                  'greedy' and 'complete'
  --msa_server_username TEXT      MSA server username for basic auth. Used
                                  only if --use_msa_server is set. Can also be
                                  set via BOLTZ_MSA_USERNAME environment
                                  variable.
  --msa_server_password TEXT      MSA server password for basic auth. Used
                                  only if --use_msa_server is set. Can also be
                                  set via BOLTZ_MSA_PASSWORD environment
                                  variable.
  --api_key_header TEXT           Custom header key for API key authentication
                                  (default: X-API-Key).
  --api_key_value TEXT            Custom header value for API key
                                  authentication.
  --use_potentials                Whether to use potentials for steering.
                                  Default is False.
  --model [boltz1|boltz2]         The model to use for prediction. Default is
                                  boltz2.
  --method TEXT                   The method to use for prediction. Default is
                                  None.
  --preprocessing-threads INTEGER
                                  The number of threads to use for
                                  preprocessing. Default is 1.
  --affinity_mw_correction        Whether to add the Molecular Weight
                                  correction to the affinity value head.
  --sampling_steps_affinity INTEGER
                                  The number of sampling steps to use for
                                  affinity prediction. Default is 200.
  --diffusion_samples_affinity INTEGER
                                  The number of diffusion samples to use for
                                  affinity prediction. Default is 5.
  --affinity_checkpoint PATH      An optional checkpoint, will use the
                                  provided Boltz-1 model by default.
  --max_msa_seqs INTEGER          The maximum number of MSA sequences to use
                                  for prediction. Default is 8192.
  --subsample_msa                 Whether to subsample the MSA. Default is
                                  True.
  --num_subsampled_msa INTEGER    The number of MSA sequences to subsample.
                                  Default is 1024.
  --no_kernels                    Whether to disable the kernels. Default
                                  False
  --write_embeddings              to dump the s and z embeddings into a npz
                                  file. Default is False.
  --help                          Show this message and exit.

=== MAFFT absolute path ===
v7.526 (2024/Apr/26)Human reference length: 463
Target length: 384
Alignment score: 695.5
target            0 MAGAPGPLRLALLLLGMVGRAGPRPQGATVSLWETVQKWREYRRQCQRSLTEDPPPATDL
                  0 ----------------------------||||||||||||||||||||||||||||||||
query             0 ----------------------------TVSLWETVQKWREYRRQCQRSLTEDPPPATDL

target           60 FCNRTFDEYACWPDGEPGSFVNVSCPWYLPWASSVPQGHVYRFCTAEGLWLQKDNSSLPW
                 60 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
query            32 FCNRTFDEYACWPDGEPGSFVNVSCPWYLPWASSVPQGHVYRFCTAEGLWLQKDNSSLPW

target          120 RDLSECEESKRGERSSPEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIH
                120 ||||||||-------|||||||||||||||||||||||||||||||||||||||||||||
query            92 RDLSECEE-------SPEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIH

target          180 LNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAAN
                180 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
query           145 LNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAAN

target          240 YYWLLVEGVYLYTLLAFSVLSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRN
                240 |||||||||||||||||||.||||||||||||||||||||||||||||||||||||||||
query           205 YYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRN

target          300 SNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANLMCKTDIKCRLAKSTLTLIPLL
                300 |||||||||||||||||||||||||||||||||||||||----|||||||||||||||||
query           265 SNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANL----DIKCRLAKSTLTLIPLL

target          360 GTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERW
                360 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
query           321 GTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERW

target          420 RLEHLHIQRDSSMKPLKCPTSSLSSGATAGSSMYTATCQASCS 463
                420 |||---------------------------------------- 463
query           381 RLE---------------------------------------- 384

---

# chatgpt response

现在有了足够的信息，可以明确一个关键结论：**你的 384 aa 受体不是完整的人源 GLP-1R 天然序列，而是与其高度同源、带有局部缺失和替换的构建序列。**

从全局比对结果看：

- 目标序列前端对应人源 GLP-1R 去掉 N 端约 28 aa 后的区域。
- 目标序列中存在至少两处明显的局部差异：一处约 7 aa 的缺失，另一处约 4 aa 的缺失；此外还有个别氨基酸替换。
- 目标序列末端的 `RLE` 后就结束了，而人源参考序列还包含较长的 C 端尾部。

这意味着我们不能简单地把完整人源 GLP-1R 及其他 463 aa 左右的序列截成 384 aa，也不能直接把所有序列按长度筛选。正确做法是：**以实际的 384 aa 输入作为查询序列，将天然 GLP-1R 同源序列比对到这个查询上，保留可靠的同源信息和缺口，而不是伪造与天然序列的一一对应关系。**

另外，Boltz 2.2.1 的命令行支持 `--seed`、`--model boltz2`、`--max_msa_seqs` 等参数。MAFFT 7.526 也可通过绝对路径调用，不必为了当前任务更改环境。

下面开始生成第一版可审计的自定义 MSA。我们采用两阶段比对：先对筛选后的天然 GLP-1R 序列建立多序列比对，再把实际的 384 aa 受体作为参考加入比对，最后转换为 Boltz-2 可用的 A3M 格式。

这里有一个重要细节：**天然受体中存在、但你的构建序列中缺失的片段，在 A3M 中需要作为相对于查询序列的插入处理，而不能简单删除整列或强行截断序列。**

## 1. 创建 MSA 生成脚本

在终端中完整复制下面的命令。它会创建脚本、保留中间文件，并输出筛选统计，方便之后复现。

```bash
cat > LOCAL_PATH <<'PY'
from pathlib import Path
import subprocess
import tempfile
import json

ROOT = Path("LOCAL_PATH")
RAW = ROOT / "glp1r_homologs_raw.fasta"
TARGET = Path(
    "LOCAL_PATH"
    "inputs/custom_template_test/GLP1R_D13.fasta"
)

MAFFT = "USER_HOME/miniconda3/bin/mafft"
OUT_A3M = ROOT / "GLP1R_receptor_custom.a3m"
OUT_REPORT = ROOT / "GLP1R_msa_report.json"
OUT_FILTERED = ROOT / "glp1r_homologs_filtered.fasta"
OUT_ALIGNED = ROOT / "glp1r_homologs_aligned.fasta"
OUT_WITH_QUERY = ROOT / "glp1r_with_query_aligned.fasta"

AA = set("ACDEFGHIKLMNPQRSTVWY")
MIN_LEN = 300
MAX_LEN = 500
MIN_COVERAGE = 0.70
MIN_IDENTITY = 0.20


def read_fasta(path):
    records = []
    header, parts = None, []
    with open(path) as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    records.append((header, "".join(parts).upper()))
                header, parts = line[1:], []
            else:
                parts.append(line)
    if header is not None:
        records.append((header, "".join(parts).upper()))
    return records


def write_fasta(path, records, width=80):
    with open(path, "w") as handle:
        for header, seq in records:
            handle.write(f">{header}\n")
            for i in range(0, len(seq), width):
                handle.write(seq[i:i + width] + "\n")


def run(cmd, stdout_path):
    print("+", " ".join(map(str, cmd)))
    with open(stdout_path, "w") as out:
        subprocess.run(cmd, stdout=out, check=True, text=True)


def main():
    if not RAW.exists():
        raise FileNotFoundError(RAW)
    if not TARGET.exists():
        raise FileNotFoundError(TARGET)
    if not Path(MAFFT).exists():
        raise FileNotFoundError(f"MAFFT not found: {MAFFT}")

    raw_records = read_fasta(RAW)
    target_records = read_fasta(TARGET)
    if len(target_records) != 1:
        raise ValueError("Expected exactly one record in target FASTA")

    query_header, query_full = target_records[0]
    query_parts = query_full.split(":")
    if len(query_parts) != 2:
        raise ValueError(
            "Expected receptor:peptide sequence separated by ':' "
            f"but found {len(query_parts)} segments"
        )

    query = query_parts[0]
    if len(query) != 384:
        raise ValueError(f"Expected 384-aa receptor, found {len(query)} aa")
    if set(query) - AA:
        raise ValueError(f"Non-standard residues in query: {sorted(set(query)-AA)}")

    # Filter by plausible full-length GLP-1R sequence length, standard amino
    # acid alphabet, and exact sequence duplication.
    seen = set()
    filtered = []
    excluded = {
        "length": 0,
        "noncanonical": 0,
        "duplicate": 0,
    }

    for idx, (header, seq) in enumerate(raw_records, start=1):
        if not (MIN_LEN <= len(seq) <= MAX_LEN):
            excluded["length"] += 1
            continue
        if set(seq) - AA:
            excluded["noncanonical"] += 1
            continue
        if seq in seen:
            excluded["duplicate"] += 1
            continue

        seen.add(seq)
        # Stable IDs keep FASTA headers manageable and unique.
        filtered.append((f"homolog_{len(filtered)+1:04d}", seq))

    if not filtered:
        raise RuntimeError("No homologs passed the initial filters")

    write_fasta(OUT_FILTERED, filtered)

    # Align full-length homologs, then add the actual receptor construct
    # as a fragment. The target sequence remains the query for A3M conversion.
    with tempfile.TemporaryDirectory(prefix="glp1r_msa_") as tmp:
        tmp_aligned = Path(tmp) / "homologs_aligned.fasta"
        tmp_with_query = Path(tmp) / "with_query.fasta"
        tmp_query = Path(tmp) / "query.fasta"
        write_fasta(tmp_query, [("QUERY_GL P1R".replace(" ", ""), query)])

        run(
            [MAFFT, "--auto", "--thread", "4", str(OUT_FILTERED)],
            tmp_aligned,
        )
        run(
            [MAFFT, "--addfragments", str(tmp_query), "--thread", "4",
             str(tmp_aligned)],
            tmp_with_query,
        )

        aligned_records = read_fasta(tmp_with_query)
        OUT_ALIGNED.write_text(tmp_aligned.read_text())
        OUT_WITH_QUERY.write_text(tmp_with_query.read_text())

    query_hits = [
        (h, s) for h, s in aligned_records
        if h.split()[0] == "QUERY_GL P1R".replace(" ", "")
    ]
    if len(query_hits) != 1:
        # Some MAFFT builds may decorate or rewrite the query header.
        query_hits = [
            (h, s) for h, s in aligned_records
            if h.split()[0].startswith("QUERY_GL")
        ]
    if len(query_hits) != 1:
        raise RuntimeError(
            "Could not uniquely identify the aligned query sequence. "
            "Inspect glp1r_with_query_aligned.fasta."
        )

    aligned_query = query_hits[0][1]
    if len(aligned_query.replace("-", "")) != len(query):
        raise RuntimeError("Aligned query length does not match 384-aa input")

    # Convert a conventional gapped alignment to A3M relative to the query:
    # columns where the query has a gap become lowercase insertions in homologs;
    # columns occupied by the query remain uppercase residues or deletion gaps.
    query_core_cols = [i for i, c in enumerate(aligned_query) if c != "-"]
    if len(query_core_cols) != len(query):
        raise RuntimeError("Query core does not contain exactly 384 residues")

    accepted = []
    rejected = []
    stats = []

    for header, aligned_seq in aligned_records:
        if len(aligned_seq) != len(aligned_query):
            raise RuntimeError(f"Alignment width mismatch for {header}")

        if header.split()[0].startswith("QUERY_GL"):
            continue

        core = [aligned_seq[i] for i in query_core_cols]
        covered = sum(c != "-" for c in core)
        coverage = covered / len(query)
        paired = [(q, s) for q, s in zip(
            [aligned_query[i] for i in query_core_cols], core
        ) if s != "-"]
        identity = (
            sum(q == s for q, s in paired) / len(paired)
            if paired else 0.0
        )

        stats.append({
            "id": header.split()[0],
            "coverage": round(coverage, 4),
            "identity_on_paired_core": round(identity, 4),
        })

        if coverage < MIN_COVERAGE or identity < MIN_IDENTITY:
            rejected.append(header.split()[0])
            continue

        # Build A3M sequence: query-gap columns become lowercase insertions.
        chunks = []
        for col, qchar in enumerate(aligned_query):
            schar = aligned_seq[col]
            if qchar == "-":
                if schar != "-":
                    chunks.append(schar.lower())
            else:
                chunks.append(schar)

        a3m_seq = "".join(chunks)
        accepted.append((header.split()[0], a3m_seq))

    # Query first, ungapped and exactly equal to the original receptor sequence.
    a3m_records = [("QUERY_GL P1R".replace(" ", ""), query)] + accepted
    write_fasta(OUT_A3M, a3m_records)

    # Re-open and verify the A3M query sequence.
    written = read_fasta(OUT_A3M)
    if not written or written[0][1] != query:
        raise RuntimeError("A3M query row failed exact-sequence verification")

    report = {
        "input_raw_records": len(raw_records),
        "initial_filter": {
            "min_length": MIN_LEN,
            "max_length": MAX_LEN,
            "unique_sequences_retained": len(filtered),
            "excluded": excluded,
        },
        "query": {
            "source": str(TARGET),
            "receptor_length": len(query),
            "peptide_length": len(query_parts[1]),
            "query_exactly_preserved_in_a3m": True,
        },
        "msa_filter": {
            "minimum_query_coverage": MIN_COVERAGE,
            "minimum_identity": MIN_IDENTITY,
            "accepted_homologs": len(accepted),
            "rejected_homologs": len(rejected),
        },
        "files": {
            "filtered_homologs": str(OUT_FILTERED),
            "aligned_homologs": str(OUT_ALIGNED),
            "alignment_with_query": str(OUT_WITH_QUERY),
            "a3m": str(OUT_A3M),
        },
        "per_sequence_statistics": stats,
    }
    OUT_REPORT.write_text(json.dumps(report, indent=2))

    print("\n=== MSA BUILD SUMMARY ===")
    print("Raw records:", len(raw_records))
    print("Unique full-length-like homologs:", len(filtered))
    print("Accepted homologs:", len(accepted))
    print("Rejected after query-relative filters:", len(rejected))
    print("A3M total records (including query):", len(a3m_records))
    print("A3M query length:", len(written[0][1]))
    print("A3M file:", OUT_A3M)
    print("Report:", OUT_REPORT)
    print("\nFirst 5 A3M records:")
    for h, s in written[:5]:
        print(f">{h}\n{s[:100]}{'...' if len(s) > 100 else ''}")


if __name__ == "__main__":
    main()
PY
```

## 2. 运行并检查结```

如果运行成功，再执行```

把运行摘要发给我，尤其是 `Accepted homologs`、A3M 记录数和是否出现异常。

**说明：**这会先产生一版候选 MSA，不代表筛选已经完成生物学验证。当前过滤条件是初筛标准；我们还需要查看保留序列的覆盖度和相似性分布，并确认 Boltz 配置如何引用这个 `.a3m` 文件。确认这些后，再把 MSA 接入预测配置，避免直接启动大量计算。

---

# you asked

message time: 2026-10-22 10:29:26

是不是7KI0文件里只统计了参与结合的部分，并且个别残基位置不确定也没有计入，比如semaglutide的末位G

---

# chatgpt response

你的判断有一部分是对的，但要区分 **PDB 中实际解析出的残基、用于结构建模的构建序列，以及参与结合的残基**。它们不是同一回事。

## 1. 7KI0 并不是只记录参与结合的残基

根据 wwPDB 的 7KI0 验证报告：

- GLP-1R 的 R 链有 **384 个实际建模残基**。
- Semaglutide 的 P 链有 **30 个实际建模残基**。
- 数据库记录的 GLP-1R 构建序列长 491 aa，包含额外的表达标签等构建成分。<Cite refs={["turn902007search12","turn902007search5"]}/>

所以，PDB 的链序列并不等于完整天然序列，但也不能简单理解成“只留下参与结合的残基”。结构中通常包含许多不直接接触配体的残基；部分区域可能因为柔性、密度不足或实验解析限制而没有被建模。

## 2. Semaglutide 末端的 G 是一个很好的例子

你本地保存的 `semaglutide_7KI0_chainP.fasta` 长 31 aa，序列末端是 `...LVRGRG`。但 7KI0 验证报告列出的 P 链实际建模残基数是 30。<Cite refs={["turn902007search12","turn902007search5"]}/>

这里不能仅凭长度就断定末位 G 一定是因为“不参与结合”而被删掉。可能的情况包括：

- 该残基在结构中未能可靠解析；
- FASTA 记录反映的是完整构建序列，而结构坐标只覆盖部分残基；
- 不同文件对非标准残基或链末端的表示方式不同。

要确定具体原因，需要检查 7KI0 原始 mmCIF 中的 `entity_poly`（聚合物序列）、`atom_site`（实际原子坐标）以及残基缺失记录，不能只比较两个 FASTA 的长度。Semaglutide 还包含非天然氨基酸修饰，因此也不能把所有残基都当作普通的标准氨基酸处理。<Cite refs={["turn902007search5","turn902007search6"]}/>

## 3. 这对你构建 Boltz-2 输入有什么影响？

建议明确区分三种序列：

| 序列类型 | 用途 |
|---|---|
| 天然 GLP-1R 序列（UniProt） | 构建同源 MSA 的来源 |
| 实际输入的 384 aa 受体序列 | Boltz-2 的查询序列，必须与 MSA 查询行严格一致 |
| 7KI0 中实际建模的受体/肽链 | 结构模板和残基映射的依据 |

**不要为了让序列长度一致，直接把天然序列截短到 384 aa；也不要因为末位 G 没有出现在结构坐标里，就直接从 Boltz-2 的 31 aa 肽链中删除它。** 模板覆盖范围、输入序列和实际解析残基需要分别核实。

下一步最有价值的是检查 7KI0 的链 P：确认末位 G 是否出现在聚合物序列中、是否有对应的原子坐标，以及它的残基编号是什么。这样才能判断你的 31 aa FASTA 是完整肽序列还是结构实际解析序列。

---

# you asked

message time: 2026-10-22 10:46:40

那构建msa时也是只考虑实际建模残基更好，还是去掉头尾，把R链中间缺失的残基补上，保证最终序列长度相差不大（实际上因为补了中间的残基多几个）更好

---

# chatgpt response

我的建议是：**构建 MSA 时，以 Boltz-2 实际输入的受体序列为查询序列；保留天然 GLP-1R 同源序列中对应的真实残基和插入/缺失关系，不要为了让序列长度接近而人为补齐 R 链中间缺失的残基。**

这里需要区分两个概念：

- **MSA 的查询序列**：必须严格等于 Boltz-2 输入的 384 aa 受体序列。
- **MSA 中的同源序列**：可以比查询序列长，也可以短；比对时通过插入和缺口表示对应关系，不要求每条序列长度都接近 384 aa。

另外，7KI0 中“没有实际建模”的残基不一定是天然蛋白中不存在的残基。它们可能存在于构建序列中，只是实验结构没有解析出来。因此，不能仅凭结构坐标缺失就把它们从天然序列中删掉。

## 两种方案的区别

<box border radius="lg" padding={3} gap={3}>
  <row align="start" gap={3}>
    <icon name="check-circle" color="success" size="xl" />
    <box flex="1" gap={1}>
      **方案 A：保留真实的天然同源序列，通过比对表示缺口（推荐）**

      <text color="secondary" size="sm">MSA 的每条同源序列保留自身的真实序列；由比对算法建立残基对应关系，不人为添加氨基酸。</text>
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <icon name="x-circle" color="danger" size="xl" />
    <box flex="1" gap={1}>
      **方案 B：为追求长度相近，直接补齐或删去头尾**

      <text color="secondary" size="sm">如果没有序列或构建记录作为依据，这可能造成错误的残基映射，尤其是将原本不相邻的残基错误地连接起来。</text>
    </box>
  </row>
</box>

不过，你的 GLP-1R 项目还存在一个更重要的问题：**目前的 384 aa 受体序列中间有缺口，必须先确认它们究竟是结构未解析，还是实验构建中真实删除了这些残基。**

例如，你的序列中有：

- `RDLSECEE` 后直接接 `SPEEQLL`；
- `...SKLKANL` 后直接接 `DIK...`。

这些差异可能来自结构中未解析的片段，也可能来自实际构建序列的改造。两种情况处理方式不同。

- **如果是结构未解析：**通常应在 Boltz-2 的受体输入序列中恢复这些天然残基。结构模板可以继续保留缺失坐标，由模板映射处理，而不是把缺失残基当成不存在。
- **如果是实际构建中删除：**就应保留真实的删除版本作为输入，不应擅自恢复。
- **如果暂时无法确认：**先不要把当前 384 aa 序列直接认定为最终输入，也不要根据长度差异自动补齐。

## 对你的 MSA，我建议按这个顺序处理

1. 核对 7KI0 的完整构建序列与实际原子坐标，确定内部缺口对应的残基编号。
2. 确认你实际要预测的受体构建序列。
3. 以该输入序列作为 MSA 查询行，利用天然 GLP-1R 同源序列构建比对。
4. 保留可靠的插入/缺失信息，不以“长度接近”为主要筛选标准。

**我最想先确认的是：你现在的 384 aa 序列 `GLP1R_D13.fasta`，是不是直接从 7KI0 的 R 链实际有坐标的残基提取出来的？** 如果是，我们应当先恢复并核实序列，而不是立即继续生成 MSA。

---

# you asked

message time: 2026-10-22 10:58:06

"PRP_ROOT\GLP1R_reproduction\structures\GLP1R_7KI0_chainR.pdb"看这个文件吧，这个是7KI0提出来的

---

# chatgpt response

可以。这个文件正是我们需要核查的证据。不过，我目前不能直接读取你电脑 D 盘上的文件内容；你不必切换到 Work 模式，可以在现有 WSL 终端运行下面的检查脚本，把输出发给我，我就能继续判断。

这次重点不是只看 PDB 提取出来的序列长度，而是区分 **PDB 声明的完整链序列** 和 **实际具有原子坐标的残基**。

## 运行检查脚本

在 WSL 的 `(boltz)` 环境中完整复制执行：



## 我会根据输出判断什么？

1. **如果 PDB 中有 `SEQRES`，而 `ATOM` 坐标残基更少：**可以进一步判断哪些残基属于声明序列、哪些残基缺少坐标。
2. **如果坐标残基编号中间跳号：**这提示存在未出现在当前坐标记录中的编号，但还需要结合 `REMARK 465`、序列映射等确认具体缺失残基。
3. **如果 384 aa 目标序列与坐标序列几乎完全一致，但与完整链序列存在缺口：**需要判断这是结构缺失造成的截取，还是构建序列本身经过了删改。

最终我们要确定的是：**Boltz-2 输入是否应该使用恢复后的完整构建序列，以及 MSA 是否应当以该序列而不是当前 384 aa 序列作为查询。** 在看到这些证据之前，不建议继续生成正式 MSA。

---

# you asked

message time: 2026-10-22 11:01:26

from pathlib import Path
from Bio.PDB import PDBParser, is_aa
from Bio.SeqUtils import seq1
from Bio import Align

pdb_path = Path(
    "LOCAL_PATH"
)
full_fasta = Path(
    "LOCAL_PATH"
)
target_fasta = Path(
    "LOCAL_PATH"
    "inputs/custom_template_test/GLP1R_D13.fasta"
)

def read_fasta(path):
    if not path.exists():
        return None
    records, header, parts = [], None, []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if header is not None:
                records.append((header, "".join(parts)))
            header, parts = line[1:], []
        else:
            parts.append(line)
    if header is not None:
        records.append((header, "".join(parts)))
    return records

print("PDB exists:", pdb_path.exists())
PY          print(line)ches[:12]:f x.startswith(prefix)]SEQRES", "REMARK 465"):
PDB exists: True

=== PDB SEQRES declaration ===
SEQRES residue count: 0

=== Chain R coordinate-derived sequence ===
Observed residue count: 384
Sequence: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWPDGEPGSFVNVSCPWYLPWASSVPQGHVYRFCTAEGLWLQKDNSSLPWRDLSECEESPEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANLDIKCRLAKSTLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLE

=== Residue numbering gaps ===
Between 129 and 137: 7 integer residue number(s) absent
Between 339 and 344: 4 integer residue number(s) absent
First 15 residue IDs: [(29, '', 'THR'), (30, '', 'VAL'), (31, '', 'SER'), (32, '', 'LEU'), (33, '', 'TRP'), (34, '', 'GLU'), (35, '', 'THR'), (36, '', 'VAL'), (37, '', 'GLN'), (38, '', 'LYS'), (39, '', 'TRP'), (40, '', 'ARG'), (41, '', 'GLU'), (42, '', 'TYR'), (43, '', 'ARG')]
Last 15 residue IDs: [(409, '', 'VAL'), (410, '', 'GLN'), (411, '', 'LEU'), (412, '', 'GLU'), (413, '', 'PHE'), (414, '', 'ARG'), (415, '', 'LYS'), (416, '', 'SER'), (417, '', 'TRP'), (418, '', 'GLU'), (419, '', 'ARG'), (420, '', 'TRP'), (421, '', 'ARG'), (422, '', 'LEU'), (423, '', 'GLU')]

=== Saved FASTA lengths ===
Construct FASTA: GLP1R_7KI0_chainR | GLP-1 receptor construct as recorded in PDB 7KI0 length = 491
Target FASTA: GLP1R_D13 receptor = 384 peptide = 31

--- 491-aa saved construct FASTA vs coordinate sequence ---
Lengths: 491 384
Score: 684.5
target            0 MKTIIALSYIFCLVFADYKDDDDLEVLFQGPARPQGATVSLWETVQKWREYRRQCQRSLT
                  0 -------------------------------------|||||||||||||||||||||||
query             0 -------------------------------------TVSLWETVQKWREYRRQCQRSLT

target           60 EDPPPATDLFCNRTFDEYACWPDGEPGSFVNVSCPWYLPWASSVPQGHVYRFCTAEGLWL
                 60 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
query            23 EDPPPATDLFCNRTFDEYACWPDGEPGSFVNVSCPWYLPWASSVPQGHVYRFCTAEGLWL

target          120 QKDNSSLPWRDLSECEESKRGERSSPEEQLLFLYIIYTVGYALSFSALVIASAILLGFRH
                120 |||||||||||||||||-------||||||||||||||||||||||||||||||||||||
query            83 QKDNSSLPWRDLSECEE-------SPEEQLLFLYIIYTVGYALSFSALVIASAILLGFRH

target          180 LHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFL
                180 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
query           136 LHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFL

target          240 LMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLY
                240 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
query           196 LMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLY

target          300 EDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANLMCKTDIKCRLAK
                300 ||||||||||||||||||||||||||||||||||||||||||||||||----||||||||
query           256 EDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANL----DIKCRLAK

target          360 STLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQL
                360 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
query           312 STLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQL

target          420 EFRKSWERWRLEHLHIQRDSSMKPLKCPTSSLSSGATAGSSMYTATCQASCSPAGLEVLF
                420 ||||||||||||------------------------------------------------
query           372 EFRKSWERWRLE------------------------------------------------

target          480 QGPHHHHHHHH 491
                480 ----------- 491
query           384 ----------- 384


--- 384-aa target receptor vs coordinate sequence ---
Lengths: 384 384
Score: 768.0
target            0 TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWPDGEPGSFVNVSCPWY
                  0 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
query             0 TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWPDGEPGSFVNVSCPWY

target           60 LPWASSVPQGHVYRFCTAEGLWLQKDNSSLPWRDLSECEESPEEQLLFLYIIYTVGYALS
                 60 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
query            60 LPWASSVPQGHVYRFCTAEGLWLQKDNSSLPWRDLSECEESPEEQLLFLYIIYTVGYALS

target          120 FSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWD
                120 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
query           120 FSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWD

target          180 GLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWG
                180 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
query           180 GLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWG

target          240 VPLLFVVPWGIVKYLYEDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKL
                240 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
query           240 VPLLFVVPWGIVKYLYEDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKL

target          300 KANLDIKCRLAKSTLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVA
                300 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
query           300 KANLDIKCRLAKSTLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVA

target          360 ILYCFVNNEVQLEFRKSWERWRLE 384
                360 |||||||||||||||||||||||| 384
query           360 ILYCFVNNEVQLEFRKSWERWRLE 384


=== PDB record types ===

---

# chatgpt response

这次输出已经足够判断关键问题了。**你的 384 aa 序列确实与 PDB 文件中 Chain R 的实际坐标序列完全一致；但它不等于 7KI0 的完整构建序列。** 更重要的是，中间两段缺失需要区别对待。

## 1. 目前能确定的事实

| 检查项 | 结果 | 说明 |
|---|---|---|
| PDB Chain R 实际有坐标的残基 | 384 aa | 你提取的序列长度 |
| Chain R 首尾编号 | 29–423 | 与天然受体 N/C 端并非完整覆盖 |
| 中间编号缺口 | 129–136、340–343 | 分别缺少 8 个和 4 个编号位置 |
| 384 aa FASTA 与坐标序列 | 完全一致 | 你的提取过程没有改变坐标序列 |
| 保存的构建 FASTA | 491 aa | 包含额外构建片段和 C 端序列 |

注意：输出中显示的 `Between 129 and 137: 7 integer residue(s) absent` 是脚本计数时的**文字错误**，因为 129 到 137 之间实际缺少的是 130–136，共 7 个编号；而按前面列出的编号关系，应以原始 PDB 中的实际残基编号为准。相应地，339 到 344 之间缺少 340–343，共 4 个编号。

这也解释了你之前看到的两处缺失：它们不是单纯的比对算法造成的，而是反映在 PDB 的坐标残基编号中。

## 2. 构建 MSA 时该用哪条序列？

我的建议是：**不要把当前 384 aa 直接当作最终查询序列，也不要盲目把完整 491 aa 序列拿来做查询。先核实两处缺失究竟是“未解析残基”还是“构建序列删除”。**

<box border radius="lg" padding={3} gap={3}>
  <row align="start" gap={3}>
    <icon name="check-circle" color="success" size="lg" />
    <box flex="1" gap={1}>
      **如果缺失残基仍属于构建序列**

      应恢复其序列位置，并以恢复后的受体序列作为 Boltz-2 输入和 MSA 查询序列。PDB 模板本身仍可存在没有坐标的残基。
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <icon name="check-circle" color="success" size="lg" />
    <box fl构建中也删除了它们**。PDB 的 `SEQRES` 记录数为 om pathlib import Path

p = Path("LOCAL_PATH")
seq = "".join(
    line.strip() for line in p.read_text().splitlines()
    if line.strip() and not line.startswith(">")
)

for start, end in [(110, 155), (320, 360)]:
    print(f"\nConstruct FASTA positions {start}-{end}:")
    print(seq[start-1:end])
PY
```

把这两段输出发来，我们就能进一步判断该如何恢复缺失区域。

**当前结论：先暂停正式 MSA 构建。** 你的 384 aa 提取序列是正确的坐标序列，但还不能确定它是不是最合适的 Boltz-2 查询序列。先厘清两处缺失，才能避免把结构实验中的缺失误当成蛋白质本身的序列缺失。

---

# you asked

message time: 2026-10-22 11:02:24

RCE|DBREF|SEQRES|REMARK 465|REMARK 470|ATOM|HETATM)' \
  LOCAL_PATH \
  | head -100
1:ATOM      1  N   THR R  29     113.384 122.097 169.709  1.00 97.53           N
2:ATOM      2  CA  THR R  29     114.087 120.858 169.388  1.00 97.53           C
3:ATOM      3  C   THR R  29     113.641 119.712 170.289  1.00 97.53           C
4:ATOM      4  O   THR R  29     114.454 118.936 170.776  1.00 97.53           O
5:ATOM      5  CB  THR R  29     115.614 121.034 169.500  1.00 97.53           C
6:ATOM      6  OG1 THR R  29     115.937 121.703 170.729  1.00 97.53           O
7:ATOM      7  CG2 THR R  29     116.145 121.836 168.324  1.00 97.53           C
8:ATOM      8  N   VAL R  30     112.331 119.618 170.492  1.00 88.79           N
9:ATOM      9  CA  VAL R  30     111.690 118.536 171.231  1.00 88.79           C
10:ATOM     10  C   VAL R  30     111.934 117.225 170.496  1.00 88.79           C
11:ATOM     11  O   VAL R  30     112.348 117.229 169.333  1.00 88.79           O
12:ATOM     12  CB  VAL R  30     110.188 118.830 171.382  1.00 88.79           C
13:ATOM     13  CG1 VAL R  30     109.521 118.817 170.030  1.00 88.79           C
14:ATOM     14  CG2 VAL R  30     109.516 117.850 172.329  1.00 88.79           C
15:ATOM     15  N   SER R  31     111.702 116.095 171.157  1.00 79.65           N
16:ATOM     16  CA  SER R  31     111.837 114.813 170.487  1.00 79.65           C
17:ATOM     17  C   SER R  31     110.917 113.794 171.134  1.00 79.65           C
18:ATOM     18  O   SER R  31     110.765 113.779 172.356  1.00 79.65           O
19:ATOM     19  CB  SER R  31     113.278 114.312 170.532  1.00 79.65           C
20:ATOM     20  OG  SER R  31     114.087 115.036 169.630  1.00 79.65           O
21:ATOM     21  N   LEU R  32     110.302 112.947 170.312  1.00 74.28           N
22:ATOM     22  CA  LEU R  32     109.583 111.816 170.872  1.00 74.28           C
23:ATOM     23  C   LEU R  32     110.534 110.861 171.564  1.00 74.28           C
24:ATOM     24  O   LEU R  32     110.249 110.386 172.668  1.00 74.28           O
25:ATOM     25  CB  LEU R  32     108.806 111.078 169.792  1.00 74.28           C
26:ATOM     26  CG  LEU R  32     107.962 109.922 170.318  1.00 74.28           C
27:ATOM     27  CD1 LEU R  32     106.675 109.788 169.549  1.00 74.28           C
28:ATOM     28  CD2 LEU R  32     108.719 108.631 170.223  1.00 74.28           C
29:ATOM     29  N   TRP R  33     111.661 110.553 170.926  1.00 85.90           N
30:ATOM     30  CA  TRP R  33     112.542 109.525 171.465  1.00 85.90           C
31:ATOM     31  C   TRP R  33     113.086 109.930 172.822  1.00 85.90           C
32:ATOM     32  O   TRP R  33     113.107 109.129 173.756  1.00 85.90           O
33:ATOM     33  CB  TRP R  33     113.672 109.234 170.480  1.00 85.90           C
34:ATOM     34  CG  TRP R  33     114.467 108.033 170.856  1.00 85.90           C
35:ATOM     35  CD1 TRP R  33     114.198 106.742 170.531  1.00 85.90           C
36:ATOM     36  CD2 TRP R  33     115.671 108.014 171.623  1.00 85.90           C
37:ATOM     37  NE1 TRP R  33     115.152 105.917 171.062  1.00 85.90           N
38:ATOM     38  CE2 TRP R  33     116.071 106.676 171.734  1.00 85.90           C
39:ATOM     39  CE3 TRP R  33     116.446 109.001 172.232  1.00 85.90           C
40:ATOM     40  CZ2 TRP R  33     117.214 106.297 172.429  1.00 85.90           C
41:ATOM     41  CZ3 TRP R  33     117.582 108.624 172.921  1.00 85.90           C
42:ATOM     42  CH2 TRP R  33     117.958 107.287 173.012  1.00 85.90           C
43:ATOM     43  N   GLU R  34     113.511 111.179 172.962  1.00 87.64           N
44:ATOM     44  CA  GLU R  34     113.997 111.622 174.259  1.00 87.64           C
45:ATOM     45  C   GLU R  34     112.870 111.647 175.284  1.00 87.64           C
46:ATOM     46  O   GLU R  34     113.093 111.358 176.463  1.00 87.64           O
47:ATOM     47  CB  GLU R  34     114.658 112.992 174.135  1.00 87.64           C
48:ATOM     48  CG  GLU R  34     113.695 114.149 174.089  1.00 87.64           C
49:ATOM     49  CD  GLU R  34     114.386 115.487 173.996  1.00 87.64           C
50:ATOM     50  OE1 GLU R  34     113.679 116.515 173.975  1.00 87.64           O
51:ATOM     51  OE2 GLU R  34     115.633 115.516 173.952  1.00 87.64           O
52:ATOM     52  N   THR R  35     111.648 111.964 174.852  1.00 84.59           N
53:ATOM     53  CA  THR R  35     110.519 111.981 175.775  1.00 84.59           C
54:ATOM     54  C   THR R  35     110.242 110.596 176.339  1.00 84.59           C
55:ATOM     55  O   THR R  35     110.064 110.437 177.548  1.00 84.59           O
56:ATOM     56  CB  THR R  35     109.272 112.513 175.075  1.00 84.59           C
57:ATOM     57  OG1 THR R  35     109.512 113.844 174.612  1.00 84.59           O
58:ATOM     58  CG2 THR R  35     108.109 112.518 176.017  1.00 84.59           C
59:ATOM     59  N   VAL R  36     110.215 109.580 175.483  1.00 84.32           N
60:ATOM     60  CA  VAL R  36     109.922 108.233 175.952  1.00 84.32           C
61:ATOM     61  C   VAL R  36     111.024 107.732 176.871  1.00 84.32           C
62:ATOM     62  O   VAL R  36     110.759 107.081 177.885  1.00 84.32           O
63:ATOM     63  CB  VAL R  36     109.709 107.295 174.762  1.00 84.32           C
64:ATOM     64  CG1 VAL R  36     109.268 105.948 175.245  1.00 84.32           C
65:ATOM     65  CG2 VAL R  36     108.680 107.887 173.855  1.00 84.32           C
66:ATOM     66  N   GLN R  37     112.277 108.016 176.532  1.00 88.49           N
67:ATOM     67  CA  GLN R  37     113.365 107.652 177.427  1.00 88.49           C
68:ATOM     68  C   GLN R  37     113.174 108.271 178.796  1.00 88.49           C
69:ATOM     69  O   GLN R  37     113.275 107.585 179.817  1.00 88.49           O
70:ATOM     70  CB  GLN R  37     114.704 108.095 176.845  1.00 88.49           C
71:ATOM     71  CG  GLN R  37     115.020 107.457 175.532  1.00 88.49           C
72:ATOM     72  CD  GLN R  37     115.207 105.983 175.671  1.00 88.49           C
73:ATOM     73  OE1 GLN R  37     114.316 105.204 175.351  1.00 88.49           O
74:ATOM     74  NE2 GLN R  37     116.368 105.582 176.159  1.00 88.49           N
75:ATOM     75  N   LYS R  38     112.882 109.567 178.838  1.00 87.49           N
76:ATOM     76  CA  LYS R  38     112.720 110.226 180.121  1.00 87.49           C
77:ATOM     77  C   LYS R  38     111.566 109.616 180.893  1.00 87.49           C
78:ATOM     78  O   LYS R  38     111.609 109.532 182.124  1.00 87.49           O
79:ATOM     79  CB  LYS R  38     112.519 111.721 179.913  1.00 87.49           C
80:ATOM     80  CG  LYS R  38     113.731 112.388 179.314  1.00 87.49           C
81:ATOM     81  CD  LYS R  38     113.893 113.834 179.738  1.00 87.49           C
82:ATOM     82  CE  LYS R  38     112.580 114.565 179.801  1.00 87.49           C
83:ATOM     83  NZ  LYS R  38     112.775 116.033 179.761  1.00 87.49           N
84:ATOM     84  N   TRP R  39     110.535 109.162 180.184  1.00 88.55           N
85:ATOM     85  CA  TRP R  39     109.408 108.541 180.859  1.00 88.55           C
86:ATOM     86  C   TRP R  39     109.841 107.288 181.597  1.00 88.55           C
87:ATOM     87  O   TRP R  39     109.487 107.089 182.762  1.00 88.55           O
88:ATOM     88  CB  TRP R  39     108.314 108.220 179.855  1.00 88.55           C
89:ATOM     89  CG  TRP R  39     107.180 107.524 180.462  1.00 88.55           C
90:ATOM     90  CD1 TRP R  39     106.350 108.008 181.416  1.00 88.55           C
91:ATOM     91  CD2 TRP R  39     106.731 106.209 180.167  1.00 88.55           C
92:ATOM     92  NE1 TRP R  39     105.410 107.076 181.743  1.00 88.55           N
93:ATOM     93  CE2 TRP R  39     105.619 105.958 180.986  1.00 88.55           C
94:ATOM     94  CE3 TRP R  39     107.156 105.217 179.285  1.00 88.55           C
95:ATOM     95  CZ2 TRP R  39     104.927 104.757 180.952  1.00 88.55           C
96:ATOM     96  CZ3 TRP R  39     106.464 104.026 179.250  1.00 88.55           C
97:ATOM     97  CH2 TRP R  39     105.363 103.805 180.080  1.00 88.55           C
98:ATOM     98  N   ARG R  40     110.630 106.442 180.947  1.00 93.81           N
99:ATOM     99  CA  ARG R  40     111.094 105.235 181.609  1.00 93.81           C
100:ATOM    100  C   ARG R  40     111.979 105.569 182.799  1.00 93.81           C
(boltz) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH python - <<'PY'
from pathlib import Path

p = Path("LOCAL_PATH")
seq = "".join(
    line.strip() for line in p.read_text().splitlines()
    if line.strip() and not line.startswith(">")
)

for start, end in [(110, 155), (320, 360)]:
    print(f"\nConstruct FASTA positions {start}-{end}:")
    print(seq[start-1:end])
PY

Construct FASTA positions 110-155:
YRFCTAEGLWLQKDNSSLPWRDLSECEESKRGERSSPEEQLLFLYI

Construct FASTA positions 320-360:
LPILFAIGVNFLIFVRVICIVVSKLKANLMCKTDIKCRLAK

---

# chatgpt response

从这两段输出看，已经能确定一个关键区别：**你保存的 491 aa construct FASTA 与 7KI0 链 R 的 384 aa 坐标序列并不相同；不能为了让 MSA 长度更接近，就直接把缺失片段补回去。**

目前最值得关注的是两处内部缺口：

| 区域 | construct FASTA 中的序列 | 链 R 坐标序列的情况 |
|---|---|---|
| 第一处 | `...SECEESKRGERSSPEEQLL...` | 缺少 `KRGERSS`（7 aa） |
| 第二处 | `...VSKLKANLMCKTDIK...` | 缺少 `MCKT`（4 aa） |

这两处恰好对应坐标残基编号中的跳号，因此它们**可能是构建体中存在、但晶体/冷冻电镜结构里没有解析出坐标的残基**，而不一定是受体序列中被真正删除的片段。不过，你当前的 PDB 文件没有 `SEQRES`、`DBREF` 等记录，单靠它无法最终确认构建体的完整序列。

## 对 Boltz-2 的实际影响

要把两个问题分开处理：

- **MSA 应该匹配哪个序列？** 应匹配你实际传给 Boltz-2 的受体输入序列。
- **Boltz-2 的受体输入应该用哪个序列？** 取决于你的建模目标，以及这两个缺口究竟是未解析残基还是构建体中的真实缺失。

如果你继续使用目前的 `GLP1R_D13.fasta`，受体链是 384 aa，那么 MSA query 就必须是这条 384 aa 序列。不要把 491 aa construct FASTA 的序列直接拿来当它的 MSA query。

但如果确认 `KRGERSS` 和 `MCKT` 属于实际构建体、只是结构中没有坐标，那么对于希望保留完整受体序列的预测，应该考虑使用恢复这 11 aa 的序列，并重新准备与它匹配的 MSA。**这并不意味着要把所有融合标签也加进受体输入。**

我进一步核对了 7KI0 的公开结构记录，证据已经更明确：RCSB 将 GLP-1R 链 R 对应的聚合物序列记录为 **491 aa**，而 wwPDB 验证报告显示链 R 实际有坐标的残基为 **384 aa**。这支持“构建体序列比坐标序列长”的判断。<Cite refs={["turn584845search0","turn584845search21"]}/>

## 我建议你现在这样做

**如果你的目标是用 7KI0 的受体构建体来预测候选肽与 GLP-1R 的复合物，优先准备一条恢复内部缺口、但去除表达标签的受体序列。**

1. 以当前 384 aa 坐标序列为基础。
2. 在对应位置恢复 `KRGERSS` 和 `MCKT`，得到 **395 aa** 的受体序列。
3. 不要把 491 aa construct FASTA 中的 N 端表达标签、C 端融合/纯化标签一并加入受体链。
4. 用这条 395 aa 序列作为 Boltz-2 受体输入，并让自建 MSA 的 query 与它严格一致。
5. 保留原先 384 aa 版本作为对照，比较两种输入对受体结构、肽结合姿态和置信度的影响。

这里的 395 aa 是按“384 aa 坐标序列 + 两段已知缺口”计算的候选构建体序列长度，并不是说已经证明这一定是所有建模任务的最佳输入。

还有一点需要注意：**不要把“恢复了缺失序列”误认为“恢复了真实结构”**。Boltz-2 会重新预测这些残基的构象，未必能重现 7KI0 中未解析区域的真实状态。对于 GPCR，受体构象和跨膜区的整体稳定性也很重要，所以我建议保留 384 aa 版本作为基线，而不是直接废弃它。

接下来最稳妥的步骤是：先生成并检查这条 395 aa FASTA，再构建 MSA；不要直接修改现有 MSA 文件。

---

# you asked

message time: 2026-10-22 12:47:46

继续

---

# chatgpt response

我们先完成第一步：**生成 395 aa 的候选受体序列，并做严格校验；暂时不改动现有的 384 aa 输入或 MSA。**

## 第一步：生成候选 395 aa FASTA

在 WSL 的终端执行下面整段命令。它会读取已有的 384 aa 序列，在两个已确认的缺口位置插入对应片段，写入一个新文件，并检查长度和插入位置。



注意：这个脚本会将 `GLP1R_7KI0_chainR.fasta` 当作 **491 aa 的构建体序列文件**来检查长度，并从 PDB 重新提取 384 aa 坐标序列。因此，如果文件实际内容或格式与你之前报告的不一致，它会停止，而不是悄悄生成错误结果。

## 第二步：检查结果

成功后，再执行：



确认输出序列开头仍然是：



而且内部包含：



以及：



## 第三步：再构建 MSA

先不要直接对 476 条同源序列运行 MAFFT 并把输出文件交给 Boltz-2。普通多序列比对结果不一定符合 Boltz-2 自定义 MSA 所需的 A3M 格式，直接使用可能造成插入、删除和 query 对齐关系不正确。

下一步需要做三件事：

1. 以新生成的 395 aa 序列作为 query。
2. 检查现有 476 条同源序列的物种、重复序列和覆盖范围，确认它们确实是 GLP1R 同源序列。
3. 生成与 395 aa query 严格对应的 MSA，并验证 query 行与输入 FASTA 完全一致，再接入 Boltz-2。

**你先运行第一步脚本，把终端输出发给我。** 我们确认候选序列无误后，再继续 MSA 构建，避免在序列尚未确认时就把错误传播到后续预测。

另外，如果你希望，我也可以在完成这轮 MSA 与 Boltz-2 验证后提醒你回头比较 384 aa 和 395 aa 两套结果。

---

# you asked

message time: 2026-10-22 12:48:24

坐标序列长度: 384
候选序列长度: 395
第一处恢复: True
第二处恢复: True
输出文件: LOCAL_PATH

候选序列片段:
RDLSECEESKRGERSSPEEQLL: position 93
VSKLKANLMCKTDIKCRL: position 304
(boltz) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH

---

# chatgpt response

很好，第一步通过了：坐标序列为 **384 aa**，恢复两段内部序列后得到 **395 aa**，两处片段也都在预期位置找到。

- `KRGERSS`：候选序列第 93 位开始
- `MCKT`：候选序列第 304 位开始

接下来我们先检查那 476 条同源序列，确认哪些可以用于构建 MSA。这里有个重要原则：**不能只看序列数量；还要看同源性、覆盖率、冗余程度，以及最终 MSA 是否与 395 aa query 严格对应。**

## 第四步：审计现有的 476 条同源序列

这一步只读文件，不会修改原始数据。请在 WSL 中运行下面的命令，检查序列长度、重复情况、字符合法性和代表性序列头。



### 把输出发给我

我主要看四项：

1. **长度分布**：476 条是否主要是 GLP1R 全长同源蛋白，还是混入了大量截短序列。
2. **重复序列**：重复太多会降低 MSA 的有效多样性。
3. **异常字符**：比如 `X`、`-` 或其他非标准符号，需要在建库时妥善处理。
4. **序列头信息**：判断是否包含物种、UniProt accession 等元数据。

下一步再根据审计结果决定如何比对。特别提醒：**MAFFT 生成的普通对齐 FASTA 不能未经转换和验证就直接当作 Boltz-2 的 A3M 文件。** 我们会先保证 395 aa query 与最终 MSA 的对应关系正确，再接入预测流程。

等 MSA 和预测跑通后，你是否也希望我帮你安排一次 384 aa 与 395 aa 的对照评估，比较两种受体输入对预测结果的影响？

---

# you asked

message time: 2026-10-22 12:48:48

=== 基本统计 ===
同源序列记录数: 476
Query 长度: 395
同源序列长度分布: [(431, 210), (463, 70), (367, 22), (462, 10), (459, 10), (426, 7), (464, 5), (449, 5), (458, 5), (253, 4), (457, 3), (470, 3), (443, 3), (482, 3), (454, 3)]
完全重复序列数（按记录计）: 79
含非标准氨基酸或其他字符的记录数: 2
  异常字符: ('tr|A0A3Q0G1T8|A0A3Q0G1T8_ALLSI', ['X'])
  异常字符: ('tr|A0A6P7XPN8|A0A6P7XPN8_9AMPH', ['X'])

=== 前 20 条序列头 ===
>sp|P43220|GLP1R_HUMAN Glucagon-like peptide 1 receptor OS=Homo sapiens OX=9606 GN=GLP1R PE=1 SV=2  [length=463]
>sp|O35659|GLP1R_MOUSE Glucagon-like peptide 1 receptor OS=Mus musculus OX=10090 GN=Glp1r PE=1 SV=2  [length=463]
>sp|P32301|GLP1R_RAT Glucagon-like peptide 1 receptor OS=Rattus norvegicus OX=10116 GN=Glp1r PE=2 SV=1  [length=463]
>tr|Q3ZAW0|Q3ZAW0_MOUSE Glucagon-like peptide 1 receptor (Fragment) OS=Mus musculus OX=10090 GN=Glp1r PE=2 SV=1  [length=462]
>tr|Q104P0|Q104P0_MOUSE Glucagon-like peptide 1 receptor OS=Mus musculus OX=10090 GN=Glp1r PE=2 SV=1  [length=463]
>tr|A0ABK0LHL4|A0ABK0LHL4_RAT Glucagon-like peptide 1 receptor OS=Rattus norvegicus OX=10116 GN=Glp1r PE=3 SV=1  [length=552]
>tr|B7ZP48|B7ZP48_MOUSE Glucagon-like peptide 1 receptor OS=Mus musculus OX=10090 GN=Glp1r PE=2 SV=1  [length=464]
>tr|A0A674HV81|A0A674HV81_9SAUR Glucagon-like peptide 1 receptor OS=Terrapene triunguis OX=2587831 GN=GLP1R PE=3 SV=1  [length=450]
>tr|A0A8B7WDB3|A0A8B7WDB3_CASCN Glucagon-like peptide 1 receptor OS=Castor canadensis OX=51338 GN=Glp1r PE=3 SV=2  [length=463]
>tr|A0A8B9CT63|A0A8B9CT63_9AVES Glucagon-like peptide 1 receptor OS=Anser brachyrhynchus OX=132585 GN=GLP1R PE=3 SV=1  [length=459]
>tr|A0A8C2VG10|A0A8C2VG10_CHILA Glucagon-like peptide 1 receptor OS=Chinchilla lanigera OX=34839 GN=GLP1R PE=3 SV=1  [length=437]
>tr|A0A8C6FJN9|A0A8C6FJN9_MOSMO Glucagon-like peptide 1 receptor OS=Moschus moschiferus OX=68415 GN=GLP1R PE=3 SV=1  [length=457]
>tr|A0A8D2HY94|A0A8D2HY94_UROPR Glucagon-like peptide 1 receptor OS=Urocitellus parryii OX=9999 GN=GLP1R PE=3 SV=1  [length=449]
>tr|A0A9W2VRL2|A0A9W2VRL2_PANPR Glucagon-like peptide 1 receptor OS=Panthera pardus OX=9691 GN=GLP1R PE=3 SV=1  [length=463]
>tr|A0A5F5PR36|A0A5F5PR36_HORSE Glucagon-like peptide 1 receptor OS=Equus caballus OX=9796 GN=GLP1R PE=3 SV=2  [length=463]
>tr|A0A663EVJ2|A0A663EVJ2_AQUCH Glucagon-like peptide 1 receptor OS=Aquila chrysaetos chrysaetos OX=223781 GN=GLP1R PE=3 SV=1  [length=448]
>tr|A0A8B9WT28|A0A8B9WT28_BOSGR Glucagon-like peptide 1 receptor OS=Bos grunniens OX=30521 GN=GLP1R PE=3 SV=1  [length=549]
>tr|A0A8C3W1H3|A0A8C3W1H3_9CETA Glucagon-like peptide 1 receptor OS=Catagonus wagneri OX=51154 GN=GLP1R PE=3 SV=1  [length=458]
>tr|A0A8C8TRE7|A0A8C8TRE7_PERMB Glucagon-like peptide 1 receptor OS=Peromyscus maniculatus bairdii OX=230844 GN=Glp1r PE=3 SV=1  [length=463]
>tr|F1RVR1|F1RVR1_PIG Glucagon-like peptide 1 receptor OS=Sus scrofa OX=9823 GN=GLP1R PE=3 SV=2  [length=463]

=== Query 检查 ===
Query 前 40 aa: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDE
Query 后 40 aa: LFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLE
Query 内部 KRGERSS: 1
Query 内部 MCKT: 1
(boltz) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH

---

# chatgpt response

这份审计结果足够进入 MSA 构建阶段了。我们现在有 **476 条原始记录、397 条按序列内容去重后的唯一序列**，其中 2 条含有 `X`（未知氨基酸），其余序列可以继续检查和比对。

有两个处理决定：

- **完全相同的序列只保留一份**，减少冗余；这会去掉 79 条重复记录，但不会损失独立的序列信息。
- 暂时排除含 `X` 的两条序列，避免未知残基进入自定义 MSA。它们只占原始记录的一小部分。

另外，这批序列长度主要集中在 431 aa 和 463 aa，说明它们不全是与 395 aa query 等长的片段。这本身不是问题：同源序列可以长于 query，关键是要通过比对把相应区域正确对齐。

## 第五步：构建与 395 aa query 对齐的 A3M

我们会先用 MAFFT 对 query 和同源序列进行比对，再将对齐结果转换为 A3M。转换时，query 对齐中的插入列会按 A3M 约定用小写字母表示；删除位置保留为 `-`。最后会自动检查 A3M 的 query 行去掉间隙后是否与 395 aa 输入序列完全一致。

在 WSL 终端完整执行以下命令。它会生成新的文件，不覆盖原始 476 条序列。



如果这一步没有报错，再执行 MAFFT：



接着将比对结果转换为 A3M：



## 成功后把这几项发给我

- `保留的同源序列` 和 `重复记录排除` 的统计结果。
- `A3M 构建与校验通过` 的输出。
- A3M 前两行预览。

我会据此判断格式与 query 对齐是否正确，再指导你把这个 MSA 接入 Boltz-2。**在校验完成前，先不要启动正式的候选肽批量预测。**

等流程跑通后，我也可以帮你设置一个后续提醒，比较 384 aa 和 395 aa 两种受体输入的预测结果；你希望我提醒你吗？

---

# you asked

message time: 2026-10-22 13:21:49

=== MSA 输入准备完成 ===
原始同源记录: 476
含 X 排除: 2
其他异常字符排除: 0
重复记录排除: 79
保留的同源序列: 395
包括 query 的输入记录: 396
Query 长度: 395
输入文件: LOCAL_PATH
(boltz) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH USER_HOME/miniconda3/bin/mafft \
  --auto \
  --thread 4 \
  LOCAL_PATH \
  > LOCAL_PATH
nthread = 4
nthreadpair = 4
nthreadtb = 4
ppenalty_ex = 0
stacksize: 8192 kb
rescale = 1
Gap Penalty = -1.53, +0.00, +0.00



Making a distance matrix ..
  301 / 396 (thread    2)
done.

Constructing a UPGMA tree (efffree=0) ...
  390 / 396
done.

Progressive alignment 1/2...
STEP   378 / 395 (thread    0) f
Reallocating..done. *alloclen = 2888
STEP   395 / 395 (thread    2) h
done.

Making a distance matrix from msa..
  300 / 396 (thread    2)
done.

Constructing a UPGMA tree (efffree=1) ...
  390 / 396
done.

Progressive alignment 2/2...
STEP   369 / 395 (thread    1) f
Reallocating..done. *alloclen = 2874
STEP   395 / 395 (thread    3) d
done.

disttbfast (aa) Version 7.526
alg=A, model=BLOSUM62, 1.53, -0.00, -0.00, noshift, amax=0.0
4 thread(s)

distout=h
rescale = 1
  300 / 396 (thread    0)dndpre (aa) Version 7.526
alg=X, model=BLOSUM62, 1.53, +0.12, -0.00, noshift, amax=0.0
4 thread(s)

minimumweight = 0.000010
autosubalignment = 0.000000
nthread = 4
randomseed = 0
blosum 62 / kimura 200
poffset = 0
niter = 2
sueff_global = 0.100000
nadd = 2
rescale = 1

  390 / 396
Segment   1/  8    1-1091
002-0788-0 (thread    2) better
Reached 2
Segment   2/  8 1101-1175
002-0788-1 (thread    2) worse
Reached 2
Segment   3/  8 1175-1220
001-0788-1 (thread    1) identical
Converged.
Segment   4/  8 1220-1294
002-0788-1 (thread    4) worse
Reached 2
Segment   5/  8 1294-1373
002-0788-1 (thread    2) identical
Converged.

Reached 2
Segment   6/  8 1373-1442
002-0788-1 (thread    2) identical
Converged.

Reached 2
Segment   7/  8 1434-1519
002-0788-1 (thread    1) identical
Converged.

Reached 2
Segment   8/  8 1510-1686
002-0788-1 (thread    1) worse
Reached 2
done
dvtditr (aa) Version 7.526
alg=A, model=BLOSUM62, 1.53, -0.00, -0.00, noshift, amax=0.0
4 thread(s)


Strategy:
 FFT-NS-i (Standard)
 Iterative refinement method (max. 2 iterations)

If unsure which option to use, try 'mafft --auto input > output'.
For more information, see 'mafft --help', 'mafft --man' and the mafft page.

The default gap scoring scheme has been changed in version 7.110 (2013 Oct).
It tends to insert more gaps into gap-rich regions than previous versions.
To disable this change, add the --leavegappyregion option.

(boltz) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH python - <<'PY'
from pathlib import Path
from Bio import AlignIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO

base = Path("LOCAL_PATH")
aligned_path = base / "glp1r_395aa_aligned.fasta"
query_path = Path(
    "LOCAL_PATH"
)
out_path = base / "glp1r_395aa_custom.a3m"

query = "".join(
    str(r.seq).upper()
    for r in SeqIO.parse(query_path, "fasta")
)
alignment = AlignIO.read(aligned_path, "fasta")

records = list(alignment)
query_indices = [
    i for i, rec in enumerate(records)
    if rec.id == "GLP1R_QUERY_395AA"
]
if len(query_indices) != 1:
    raise ValueError(
        f"对齐结果中应恰好有一条 query，实际为 {len(query_indices)} 条。"
    )

qidx = query_indices[0]
q_aln = str(records[qidx].seq).upper()

if q_aln.replace("-", "") != query:
    raise ValueError(
        "MAFFT 对齐中的 query 与输入序列不一致；停止生成 A3M。"
PY  print(line[:180])read_text().splitlines()[:2]:y 不完全一致。")
=== A3M 构建与校验通过 ===
比对记录数: 396
A3M 记录数: 396
Query 长度: 395
A3M Query 与输入序列完全一致: True
A3M 文件: LOCAL_PATH

A3M 前 2 行预览:
>GLP1R_QUERY_395AA
TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWPDGEPGSFVNVSCPWY
(boltz) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH

---

# chatgpt response

很好，**自定义 MSA 已经成功生成，序列层面的基本校验也通过了。** 目前可以进入下一步：先检查 MSA 的对齐质量和 Boltz-2 的输入接口，再做预测；暂时不要直接把它当作已经验证有效的 MSA。

## 当前进度

| 检查项 | 结果 |
|---|---|
| 原始同源序列 | 476 条 |
| 排除含 `X` 的序列 | 2 条 |
| 排除重复序列 | 79 条 |
| 保留同源序列 | 395 条 |
| 包含 query 的比对记录 | 396 条 |
| Query 长度 | 395 aa |
| A3M query 与输入序列一致 | 通过 |

文件已经生成：

`LOCAL_PATH

不过要区分两件事：

- **格式与序列检查通过**：目前有证据支持。
- **同源序列是否正确对齐，以及 Boltz-2 是否会按预期读取这个 A3M**：还需要验证。

另外，395 aa 的 query 是在 384 aa 的结构链序列上补回了缺失的 11 个残基。这样做可以作为实验方案，但补回的环区并不意味着其真实构象已知。

## 下一步：确认 Boltz-2 能读取这份 A3M

Boltz 的输入文档支持在 YAML 中通过 `msa: /path/to/file.a3m` 指定预计算 MSA；没有必要再用 `--use_msa_server` 为同一条链自动生成 MSA。<Cite refs={["turn320718search0","turn320718search4"]}/>

先在当前 `(boltz)` 环境运行下面的检查命令，**这一步先不启动 GPU 预测*
```

把完整输出发给我。下一步我会根据结果检查 A3M 的实际格式，并确认你当前的 GLP1R–候选肽 YAML 应该怎样引用它，避免 MSA 与输入受体序列不匹配。

如果你希望，我也可以在这个流程结束后提醒你比较 **384 aa 原始结构链**和 **395 aa 补回缺失残基的序列**两种方案。

---

# you asked

message time: 2026-10-22 13:22:11

记录数: 396
Query 长度: 395
Query 含 gap: False
Query 非标准字符: []
前 5 条序列长度（忽略大小写）:
GLP1R_QUERY_395AA 395 大写残基数: 395 小写残基数: 0 gap 数: 0
sp_P43220_GLP1R_HUMAN 463 大写残基数: 395 小写残基数: 68 gap 数: 0
sp_O35659_GLP1R_MOUSE 463 大写残基数: 395 小写残基数: 68 gap 数: 0
sp_P32301_GLP1R_RAT 463 大写残基数: 395 小写残基数: 68 gap 数: 0
tr_Q3ZAW0_Q3ZAW0_MOUSE 462 大写残基数: 395 小写残基数: 67 gap 数: 0
A3M 文件大小: 194634 bytes
(boltz) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH

---

# chatgpt response

从输出看，A3M 的**首条 query 正确，且后续同源序列使用了小写字符表示相对于 query 的插入**。例如人、小鼠、大鼠 GLP1R 都是 463 aa，但在 A3M 中显示为 395 个大写残基加 68 个小写残基。这是 A3M 的一种正常表示方式，不代表原始蛋白真的只有 395 个残基。<Cite refs={["turn934968search0","turn934968search8"]}/>

接下来有一个关键点：你的预测 YAML 中，GLP1R 链的序列必须与这份 MSA 的 query **逐个氨基酸完全一致，长度为 395 aa**。如果 YAML 仍然使用 384 aa 的原始链序列，就不能直接套用这份 395 aa MSA。

## 现在请运行这一步

先找出当前实验目录中的 YAML，确认实际输>/dev/null
```

把输出发我，我再针对你正在测试的那个输入文件，给出完整的检查命令。我们要核对受体链序列长度、候选肽链，以及 MSA 路径，然后再启动一次小规模 Boltz-2 预测。

我也可以在流程完成后提醒你对比 **384 aa 与 395 aa 两种受体输入**的预测结果；如果想要这个提醒，告诉我即可。

---

# you asked

message time: 2026-10-22 14:01:40

先等等，把这一阶段的工作记录先写了，这一阶段的主要工作内容就是自241条candidate的colabfold数据表格整理好了之后，进行了筛选、聚类、挑选代表以及boltz的一些准备工作，具体细节你自己根据对话记录整理，尽量详细，记得读取已归档的ColabFold结果取舍任务对话记录，最后直接给我生成文本，我自己复制保存为txt，以下是第九阶段工作记录参考（注意这一阶段不用重复第九阶段工作内容）：

---

# chatgpt response

下面这份是根据第九阶段工作记录、已归档的“ColabFold 结果取舍”相关对话、候选筛选表和当前 MSA 准备进度整理的**第十阶段工作记录**。我把已经完成的工作、筛选方法、关键文件和仍未完成的 Boltz-2 事项分开写了；第九阶段已经详细记录的 ColabFold 计算故障、40 条补算和原始指标清洗过程不再重复。

---

```text
GLP1R reproduction 项目工作记录
阶段十：ColabFold 候选结果筛选、序列聚类、代表候选确定与 Boltz-2 预测准备

记录日期：2026-10-21 至 2026-10-22
项目：GLP1R de novo peptide candidate computational evaluation
工作阶段：候选级指标分析、序列多样性整理与后续 Boltz-2 输入准备

============================================================
一、本阶段工作概述
============================================================

第九阶段完成了 241 条候选相关记录的 ColabFold 数据收集、清洗和候选级指标整理。本阶段不再以完成批量预测为主要目标，而是转向如何利用已经获得的数据，从候选池中筛选出具有一定结构评价证据、序列代表性和后续分析价值的候选，并为下一阶段的 Boltz-2 共折叠预测做好准备。

本阶段的主要工作包括：

1. 在已经整理好的候选级 ColabFold 数据表基础上，开展候选筛选。
2. 以 D13、D41、D44 等参考候选为比较对象，尝试建立基于多项指标的筛选规则。
3. 将人工判断、指标比较和序列多样性纳入候选保留过程，形成 67 条候选的保留表。
4. 对保留候选的 31 aa 肽序列开展序列聚类，识别高度相似的序列家族。
5. 通过聚类代表和补充候选相结合的方式，形成 24 条代表候选的中间选择名单。
6. 核对高指标候选，并将 D13、D41、D44 三条参考序列纳入最终的 Boltz-2 输入候选集合，形成 27 条序列的 FASTA 文件。
7. 开始准备 GLP1R 受体的自定义多序列比对（MSA），包括同源序列整理、去重、MAFFT 多序列比对和 A3M 文件生成。
8. 重新检查 GLP1R 受体序列的长度、结构缺失残基和候选输入之间的对应关系，为 Boltz-2 正式预测解决输入一致性问题。

本阶段的工作重点是从 241 条候选的结构预测数据出发，建立一套兼顾结构指标、序列相似性和代表性选择的候选缩减流程，并将候选筛选结果推进到下一轮预测准备。

需要强调的是，本阶段完成的是计算结果筛选、序列聚类和输入准备。ColabFold 指标较高、进入代表名单或被选入 Boltz-2 输入集合，都不能直接证明候选与 GLP1R 具有真实结合能力，更不能直接证明其激动活性或其他生物学功能。


============================================================
二、从候选级 ColabFold 数据表进入筛选阶段
============================================================

2.1 数据基础

本阶段使用第九阶段已经整理的候选级 ColabFold 数据表作为主要数据基础。

候选序列长度为 31 aa，结构输出中的链组成记录为：

    A:384;B:31

其中：

- Chain A：384 aa 的 GLP1R 受体结构链；
- Chain B：31 aa 的候选肽链。

候选级表格保留了多个模型结果的汇总指标，并记录有效模型数量和候选编号，使后续筛选不必重新逐个读取所有原始结构文件。

本阶段使用的主要指标包括：

- pLDDT_mean：结构局部置信度的均值统计；
- ipTM_mean：复合物相对构象和界面相关的置信度指标；
- ipSAE_B-A_mean：B-A 方向的 ipSAE 均值；
- pDockQ_mean：界面质量相关指标；
- pDockQ2_A-B_mean：A-B 方向的 pDockQ2 均值；
- pDockQ2_B-A_mean：B-A 方向的 pDockQ2 均值。

此外，表格还保留了相应指标的最大值、最小值、有效模型数、候选序列、链组成以及后续聚类信息。

这些指标提供的是不同角度的结构评价信息，不能简单视为六个完全独立的证据，也不能把它们直接等同于实验亲和力。尤其是 ipSAE 和 pDockQ2 等方向性指标，在比较时必须保持链映射和计算方向一致。

2.2 为什么不能仅按单一指标排序

本阶段没有把某一项指标的最高值直接作为最终候选选择的唯一标准。

原因在于，不同指标反映的内容并不完全相同：

- pLDDT 主要反映局部结构预测置信度；
- ipTM 与复合物相对结构和界面预测相关；
- ipSAE、pDockQ 和 pDockQ2 提供其他界面评价信息；
- 不同指标之间可能存在相关性，也可能对同一候选给出不同的评价。

如果只按 ipTM 或其他某一个指标排序，容易忽略其他界面指标的差异，也可能使高度相似的候选在名单中占据过多位置。

因此，本阶段尝试将多项指标的相对表现与序列多样性结合起来，既保留结构评价表现较好的候选，也避免候选选择完全由某一项分数决定。


============================================================
三、以 D13 和 D44 为参照的候选筛选
============================================================

3.1 参考候选的作用

本阶段将 D13、D41、D44 作为需要特别保留和追踪的参考序列。

它们不仅是候选序列集合中的特定对象，也是后续比较候选指标、检查序列聚类结果和组织 Boltz-2 输入的重要参照。

在指标筛选过程中，主要使用 D13 和 D44 的六项 mean 指标作为比较基准；D41 则作为必须保留的参考序列之一，继续参与后续候选集合的组织。

这里的“参照”指计算分析中的比较对象，不意味着它们在本次 ColabFold 预测中已经被证明具有某种确定的真实结合能力。

3.2 六项 mean 指标比较

本阶段采用以下六项均值指标进行参照比较：

1. pLDDT_mean
2. ipTM_mean
3. ipSAE_B-A_mean
4. pDockQ_mean
5. pDockQ2_A-B_mean
6. pDockQ2_B-A_mean

筛选过程中，在初步人工判断的基础上，检查候选在上述指标上相对于 D13 或 D44 的表现。

一类候选需要在六项指标上均严格超过至少一个参照对象，才符合相应的严格比较条件。

这项规则的意义在于：候选不能仅凭单个指标较高就被视为全面优于参照序列，而需要在六项指标上同时满足严格的比较要求。

不过，这仍然是一种基于模型输出的相对筛选规则，并不是已经经过实验校准的结合判定标准。

3.3 从严格筛选到最终保留表

本阶段的候选保留不是简单地将严格筛选结果直接作为最终名单。

实际整理过程中，先进行了人工初步筛选，再按照六项 mean 指标相对于 D13/D44 的严格比较规则筛选候选。随后，又检查了一部分在六项指标中有较多项目超过参照值、但未满足全部严格条件的候选，并将其中符合补充保留规则的候选重新纳入。

具体而言，归档记录中包括：

- 按六项 mean 指标严格超过参照的规则筛出的 49 条候选记录；
- 另外恢复了 6 条在六项指标中至少有 4 项超过参照值的候选；
- 同时保留了人工初筛和代表性判断所需的候选。

经过上述筛选和整理，最终形成了 67 条候选的保留表。

需要注意，67 条是最终保留表的规模，不应简单将 49 条和 6 条相加后误认为最终总数。最终表还包含人工初筛和其他保留判断涉及的候选。

3.4 该筛选规则的局限

这一筛选规则的价值在于建立了可复核的相对比较流程，但仍存在以下限制：

第一，D13 和 D44 的模型分数只能作为当前计算体系中的参照，不能自动成为经过实验验证的普适阈值。

第二，六项指标之间可能存在统计相关性，因此六项同时超过参照，并不意味着获得了六份相互独立的结合证据。

第三，严格超过参照的规则可能排除一些具有不同序列特征或潜在价值的候选。因此，采用人工保留、补充保留和后续聚类等步骤，有助于减少单一硬阈值造成的信息损失。

第四，候选的保留与否应当被解释为进入后续计算的优先级判断，而不是对真实结合能力作出最终结论。


============================================================
四、67 条候选的序列聚类
============================================================

4.1 为什么在结构指标筛选后仍需要聚类

完成指标筛选后，67 条候选仍然不是 67 种完全不同的分子设计。

这些候选的肽长均为 31 aa，序列之间存在较多相似性，部分候选仅有少数氨基酸位点不同。

如果直接将全部候选送入后续计算，可能会在高度相似的序列上重复投入计算资源，也可能使最终分析过度集中于某几个序列家族。

因此，本阶段进一步对保留候选开展序列聚类，目的是识别序列家族、量化候选之间的相似程度，并为代表候选选择提供依据。

4.2 聚类方法与主方案阈值

本阶段对 31 aa 候选肽序列进行逐位氨基酸比较，并采用 complete-linkage（完全连接）聚类。

主方案使用的差异阈值为：

- 任意两条候选之间最多允许 3 个氨基酸位点不同；
- 对于 31 aa 的序列，这相当于至少有 28 个位置一致；
- 28/31 约为 90.3% 的逐位一致比例。

完全连接聚类的特点是，一个类群中的任意两条序列都需要满足规定的最大差异限制，而不是只要求每条序列与某一个中心序列相似。

这一约束能够避免仅通过一系列局部相似关系，将差异较大的序列链式地合并到同一类群。

按照主方案的设置，67 条候选被整理为 16 个序列类群。

4.3 聚类阈值敏感性检查

为了了解聚类结果是否过度依赖单一阈值，本阶段还检查了其他差异阈值下的类群数量。

归档结果如下：

- 最大差异不超过 2 aa：24 个类群；
- 最大差异不超过 3 aa：16 个类群；
- 最大差异不超过 4 aa：9 个类群。

这组结果说明，聚类粒度对差异阈值较为敏感。

当允许的差异更小，候选会被分成更多较细的序列家族；当允许的差异增加，更多候选会被合并到同一类群。

因此，16 个类群是基于本阶段选定的 3 aa 差异阈值所得到的结果，而不是对候选天然家族数量的唯一、绝对判定。

4.4 类群代表与 medoid

在每个类群中，本阶段进一步确定 medoid（类群中心代表序列）。

Medoid 是根据类群内部的序列差异关系确定的实际候选序列，而不是将每个位点取多数氨基酸后人工拼接出的新序列。

采用 medoid 的优势在于：

1. 代表序列本身确实存在于候选集合中；
2. 可以明确追溯其原始候选 ID；
3. 能够计算其他成员与代表序列之间的氨基酸差异数；
4. 有助于在后续计算中同时考虑类群代表性和个别候选的结构指标。

本阶段将类群规模、medoid 身份和候选相对于 medoid 的差异数等信息加入聚类结果表，为后续代表候选选择提供了结构化依据。

4.5 D13、D41、D44 的聚类映射

本阶段的聚类结果还明确记录了三条参考候选在保留表中的对应关系：

- D13：candidate_0165，位于 C14；
- D44：candidate_0173，位于 C06；
- D41：candidate_0241，与 reference_D41 对应，并作为单例位于 C16。

其中，D41 所在类群为单例，说明在当前 67 条保留表和所采用的聚类规则下，没有其他候选被归入该类群。

这些聚类编号只描述当前数据集和阈值下的序列关系，不应被解释为候选的功能分类，也不能直接证明不同类群具有不同的真实结合模式。

4.6 主要聚类文件

本阶段形成或使用的关键文件包括：

    candidate_metrics_kept_clustered.csv
    sequence_cluster_summary.csv
    cluster_medoid_sequences.fasta

其中：

candidate_metrics_kept_clustered.csv：
保留候选的指标表与聚类信息相结合的结果，包含候选编号、序列、指标、有效模型数量、类群编号、类群规模、medoid 和相对差异等信息。

sequence_cluster_summary.csv：
用于汇总各个序列类群及其代表信息。

cluster_medoid_sequences.fasta：
用于集中保存类群代表序列，方便进一步检查、提取和组织后续预测输入。

这几类文件分别承担候选级分析、类群统计和代表序列导出的功能，不应相互替代。


============================================================
五、从聚类结果中挑选代表候选
============================================================

5.1 为什么不只保留 16 条 medoid

在 67 条候选被划分为 16 个类群之后，一个直接方案是每个类群只保留一个 medoid。

但本阶段没有把“一个类群只保留一个候选”作为唯一选择原则。

原因在于，序列中心性与结构指标表现是两个不同维度：

- Medoid 更侧重于代表类群内部的序列关系；
- 结构指标用于描述特定候选的模型预测表现；
- 类群内的不同序列变体可能具有不同的预测结果；
- 只保留一个中心序列，可能会丢失某些在结构指标或局部序列变化上值得进一步研究的候选。

因此，本阶段采用“类群代表 + 补充候选”的思路，尽量兼顾序列家族覆盖和结构评价信息。

5.2 24 条候选的中间选择名单

本阶段形成了 24 条代表候选的中间选择名单。

这份名单采用主代表和次代表相结合的方式：一部分候选作为相应类群的主要代表，另一部分则用于保留有价值的序列变体或补充类群内部信息。

选择时考虑的内容包括：

- 候选所属的序列类群；
- 候选是否为类群 medoid；
- 候选与 medoid 之间的氨基酸差异数；
- 候选的 ipTM_mean；
- 候选的 ipSAE_B-A_mean；
- 候选的 pDockQ_mean；
- 候选的 pDockQ2_A-B_mean 和 pDockQ2_B-A_mean；
- 候选的 pLDDT_mean；
- 候选有效模型数量；
- 候选在综合排序中的位置；
- 类群内部是否已经有其他候选被保留。

归档的选择名单中，候选被标注为 Primary representative 或 Secondary representative，并记录 cluster_id、cluster_size、medoid_candidate、substitutions_to_medoid 和 combined_rank_score 等字段。

这些字段使代表候选的选择过程能够追溯到具体的序列家族和指标，而不是只保留一个没有解释的候选 ID 列表。

5.3 主代表与次代表的含义

Primary representative：
主要用于代表相应序列家族，选择时考虑该候选的结构指标表现及其对类群的代表价值。

Secondary representative：
用于补充保留其他有价值的序列变体或中心候选，以减少只保留单一代表所造成的信息损失。

这里的主代表与次代表是本项目内部的候选组织标签，并不意味着主代表已经被证明在生物学上更优，也不意味着次代表一定具有较低的真实结合能力。

5.4 24 条名单与最终 27 条输入的区别

需要区分两个阶段的文件：

    GLP1R_representative_selection_24.csv
    GLP1R_representatives_24.fasta

这两个文件对应 24 条代表候选的中间选择结果。

随后，本阶段进一步核对了高指标候选，并将 D13、D41、D44 三条参考序列明确加入最终输入集合，形成：

    GLP1R_representatives_24_plus_D13_D41_D44.fasta

该 FASTA 文件包含 27 条记录。

因此，24 条代表候选名单与 27 条最终输入 FASTA 不是相互矛盾的数量：前者是中间选择名单，后者在此基础上额外保留了三条指定参考序列。

D13、D41、D44 的加入，是为了使后续预测能够与已有参考对象进行对照，而不是把它们误认为新产生的候选。

5.5 代表候选选择的意义与限制

通过代表候选筛选，本阶段将候选缩减从简单的分数排序推进到同时考虑序列关系和结构指标的过程。

其主要意义包括：

1. 减少高度相似序列的重复计算；
2. 保留不同序列类群的代表；
3. 为类群内的关键变体保留后续验证机会；
4. 将参考候选纳入后续预测集合；
5. 为后续 Boltz-2 结果与 ColabFold 结果之间的比较建立统一的候选对应关系。

但 27 条候选只是本阶段确定的下一轮计算输入集合，并不意味着已经选出了 27 条真实 binder，也不意味着这些候选都通过了实验验证。

同样，24 条中间名单和最终 27 条 FASTA 的角色不同，在后续报告中应明确其统计口径，避免混淆。


============================================================
六、Boltz-2 阶段的任务定位
============================================================

6.1 为什么在 ColabFold 之后继续开展 Boltz-2 预测

ColabFold 阶段已经为候选提供了初步结构预测及相应的结构置信度和界面评价信息。

本阶段选择代表候选之后，下一步是使用 Boltz-2 对筛选后的候选进行进一步共折叠预测和评价。

这样做的目的不是简单地用另一个模型重复产生一组分数，而是为后续候选比较增加一个不同预测体系下的结构评价结果。

本项目的整体工作顺序由此进一步明确为：

241 条候选序列
→ ColabFold 批量预测与候选级指标整理
→ 依据参考指标和人工判断筛选
→ 67 条候选保留表
→ 31 aa 序列聚类
→ 16 个类群及其代表信息
→ 24 条代表候选中间名单
→ 加入 D13、D41、D44，形成 27 条 Boltz-2 输入集合
→ 准备 GLP1R 受体输入和自定义 MSA
→ 后续开展 Boltz-2 共折叠预测
→ 汇总不同预测体系下的结构与界面评价信息。

6.2 本阶段已经完成的 Boltz 准备

截至本阶段记录时，已经形成 27 条候选输入的 FASTA 文件，并开始整理 GLP1R 受体的自定义 MSA。

这意味着本阶段已经完成从大规模候选池到下一轮预测输入集合的筛选与组织工作，也开始处理 Boltz-2 预测所需的受体序列和同源信息。

但必须明确：候选 FASTA 已生成、MSA 已生成，与 Boltz-2 已成功读取 MSA 并完成正式预测，是不同的工作状态。

截至本记录结束，当前自定义 MSA 已完成初步构建与序列检查，但尚未通过实际 Boltz-2 预测确认其读取行为和最终输入兼容性。

因此，本阶段不应写成“27 条候选已完成 Boltz-2 预测”。


============================================================
七、GLP1R 受体序列与结构缺失残基检查
============================================================

7.1 为什么需要重新检查受体序列

在开始准备自定义 MSA 后，本阶段发现，GLP1R 的结构坐标序列、此前使用的受体输入序列以及用于同源比对的目标序列之间，需要进一步明确长度和残基对应关系。

这一问题会直接影响后续预测：

- MSA 的 query 必须与目标链序列正确对应；
- 受体序列长度变化会改变残基索引；
- 结构中没有坐标的残基，不一定意味着其在理论序列中不存在；
- 将缺失环区恢复到序列中，不代表已经恢复了它们的真实三维构象。

因此，本阶段先检查已有 7KI0 参考结构的 R 链、原有受体 FASTA 和包含更多构建序列信息的 FASTA，而不是直接把一份新的长序列未经检查地替换进预测流程。

7.2 原始结构链的长度与缺失区域

从 GLP1R_7KI0_chainR.fasta 对应的结构坐标序列中，得到的受体链长度为 384 aa。

该序列与此前 GLP1R_D13.fasta 中使用的受体序列完全一致。

对结构残基编号进行检查后，发现两个内部编号区间存在缺口：

- 残基编号 129 后直接到 137，缺少 130–136，共 7 个残基；
- 残基编号 339 后直接到 344，缺少 340–343，共 4 个残基。

两处合计涉及 11 个残基。

这里的“缺失”首先指结构坐标中没有对应残基，不能仅凭 PDB 坐标缺失就断定这些残基在理论蛋白序列中不存在。

7.3 491 aa 构建序列与结构链序列的区别

此前整理的 491 aa 构建序列除了 GLP1R 受体序列信息外，还包含额外的构建片段、连接区域或表达相关尾部。

例如，构建序列中存在结构坐标序列未包含的片段：

    KRGERSS

以及：

    MCKT

同时，构建序列的 C 端还包含额外的延伸和表达相关序列。

因此，不能将完整 491 aa 构建序列不加区分地作为 GLP1R 受体的标准预测输入。

本阶段将重点放在受体本身的序列、结构中未解析的内部残基以及额外构建片段之间的区分上，避免把表达标签或其他构建相关序列误当作天然受体结构的一部分。

7.4 395 aa 受体序列方案

基于上述检查，本阶段建立了一个 395 aa 的受体序列候选版本：

    LOCAL_PATH

其长度来自：

384 aa 结构坐标序列
+ 7 aa 的第一处缺失片段
+ 4 aa 的第二处缺失片段
= 395 aa。

该版本的目的，是将结构中没有坐标但在构建序列中存在的内部残基重新纳入序列，为后续受体序列和 MSA 准备提供另一种更完整的输入方案。

但是，395 aa 仍然是需要验证的输入方案，而不是已经通过结构实验或预测对照证明最优的受体表示方式。

特别是，补回残基只解决序列层面的缺失问题，不意味着 Boltz-2 会自动恢复这些环区的真实构象。

因此，后续正式预测前仍需明确使用 384 aa 还是 395 aa，并保证 MSA query、YAML 受体链序列和最终预测输入完全一致。


============================================================
八、GLP1R 自定义 MSA 的构建
============================================================

8.1 构建 MSA 的目的

为了为 GLP1R 受体准备可追溯的同源序列信息，本阶段开始构建自定义 MSA。

与直接使用一条受体序列不同，多序列比对能够把受体与相关同源蛋白之间的保守区域、插入和缺失关系组织起来。

本阶段的工作重点是：

1. 整理原始 GLP1R 同源序列；
2. 检查序列字符与记录质量；
3. 去除完全重复的序列；
4. 将目标 query 加入输入；
5. 使用 MAFFT 进行多序列比对；
6. 根据目标 query 的比对关系生成 A3M；
7. 检查 A3M 的记录数、query 长度和序列字符。

8.2 原始同源序列数据

原始同源序列文件为：

    LOCAL_PATH

原始文件中共有 476 条同源序列记录。

初步审计发现：

- 原始同源记录数：476；
- 含 X 的记录：2；
- 其他异常字符记录：0；
- 完全重复序列记录：79。

其中，人、小鼠和大鼠 GLP1R 序列都出现在原始同源序列集合中。

审计后，排除含 X 的序列，并去除重复记录，同时避免将与 query 完全相同的序列再次作为独立同源记录加入，最终保留 395 条同源序列。

随后，将 395 aa 的 query 加入输入文件，得到：

    LOCAL_PATH

该输入文件共包含 396 条记录，其中一条是目标 query，另外 395 条为去重后保留的同源序列。

8.3 MAFFT 多序列比对

本阶段使用 MAFFT 7.526 对 396 条输入序列开展多序列比对。

实际调用的程序路径为：

    USER_HOME/miniconda3/bin/mafft

主要参数为：

    --auto
    --thread 4

对应的比对输出文件为：

    LOCAL_PATH

MAFFT 日志显示，比对过程正常完成，并对全部 396 条输入记录进行了处理。

这一过程建立了目标 query 与不同长度同源序列之间的列对应关系，为后续 A3M 转换提供了基础。

需要注意，MAFFT 完成只说明多序列比对程序成功运行，不自动证明所有局部插入和缺失都符合预期的生物学对应关系。因此，后续仍需要根据受体序列结构域和关键区域对比对结果进行质量检查。

8.4 从对齐 FASTA 转换为 A3M

在获得 MAFFT 对齐结果后，本阶段进一步将对齐文件转换为 A3M 格式。

生成文件为：

    LOCAL_PATH

转换过程以 395 aa query 为参照，将 query 对齐位置中对应的同源序列插入残基以小写字母表示，并保留 query 对应位置的氨基酸信息。

生成过程中进行了多项检查：

- 对齐文件能够被读取；
- 对齐结果中恰好存在一条目标 query；
- query 去除对齐缺口后与原始输入序列完全一致；
- A3M 中的 query 与目标输入序列完全一致；
- 输出文件能够被重新读取。

最终检查结果为：

    比对记录数：396
    A3M 记录数：396
    Query 长度：395
    A3M Query 与输入序列完全一致：True

A3M 文件大小约为 194,634 bytes。

8.5 A3M 序列表示的检查

在检查 A3M 前几条记录时，观察到人、小鼠和大鼠 GLP1R 序列均长于 395 aa query。

例如，完整长度为 463 aa 的人、小鼠和大鼠序列，在 A3M 中表现为：

- 大写残基数：395；
- 小写残基数：68；
- gap 数：0。

这是当前 A3M 转换结果相对于 395 aa query 的序列表示方式。

小写残基表示相对于 query 的插入部分，不应将它们直接解释为无效字符或原始序列被截短。

目前已经完成了 A3M 的记录数、query 一致性和基本字符层面的检查。

但还需要明确：A3M 文件生成成功，并不等于 Boltz-2 已经成功读取它，也不等于其中的所有同源序列都能以预期方式参与预测。

8.6 当前 MSA 文件清单

本阶段已经形成以下主要文件：

    LOCAL_PATH
    LOCAL_PATH
    LOCAL_PATH
    LOCAL_PATH

以及 query 文件：

    LOCAL_PATH

它们分别对应原始同源序列、去重后的输入集合、MAFFT 对齐结果、最终 A3M 和目标 query。

保留这些中间文件，有助于追溯同源序列的来源、去重过程、对齐结果以及 A3M 的生成方式，而不只是留下最终 MSA 文件。


============================================================
九、当前 Boltz-2 输入一致性问题
============================================================

9.1 发现的问题

截至本阶段结束，虽然已经生成 395 aa query 对应的自定义 A3M，但此前候选预测输入文件中使用的受体序列为 384 aa。

相关文件为：

    LOCAL_PATH

该输入文件中的受体链与原始 384 aa 结构坐标序列一致。

因此，当前需要解决的不是单纯的 A3M 文件是否存在，而是正式预测输入之间的对应关系：

- 当前自定义 MSA 的 query 长度为 395 aa；
- 原有受体输入序列长度为 384 aa；
- 两者并不完全一致。

如果不解决这一问题，就不能直接将 395 aa query 对应的 A3M 视为 384 aa 受体输入的有效 MSA。

9.2 下一步必须完成的输入核验

正式开展 Boltz-2 预测前，需要明确以下事项：

1. 最终使用 384 aa 还是 395 aa 的受体序列；
2. 目标受体 FASTA 或 YAML 中的序列是否与所选 MSA query 完全一致；
3. 自定义 A3M 是否能够被当前安装的 Boltz-2 版本按预期读取；
4. YAML 中 MSA 的指定方式与实际文件路径是否正确；
5. 候选肽链是否保持 31 aa，且候选编号、序列和最终 FASTA 一致；
6. 预测完成后，是否能从输出文件确认输入链长度和链对应关系。

本阶段已经完成 MSA 的初步构建，但这些输入一致性问题尚未全部解决。

9.3 当前阶段的完成状态

截至本阶段记录结束，工作状态如下：

已完成：
- 241 条候选相关 ColabFold 数据的后续筛选；
- 67 条候选保留表整理；
- 31 aa 序列聚类及聚类结果导出；
- 16 个类群的主方案聚类结果；
- 类群 medoid 与代表候选整理；
- 24 条代表候选的中间选择名单；
- 加入 D13、D41、D44 后的 27 条 Boltz-2 输入 FASTA；
- GLP1R 原始同源序列审计与去重；
- 395 aa query 的建立；
- MAFFT 多序列比对；
- 自定义 A3M 生成和基本一致性检查。

尚未完成：
- 最终受体序列长度方案的确认；
- MSA 与正式预测 YAML 之间的序列一致性核验；
- 自定义 MSA 被 Boltz-2 正确读取的实际验证；
- 27 条候选的正式 Boltz-2 预测；
- Boltz-2 输出结果的质量检查和指标汇总。

因此，本阶段的准确结论是：已经完成从 ColabFold 候选数据整理到代表候选确定，并推进了 Boltz-2 自定义 MSA 的准备；但尚未完成正式的 Boltz-2 预测和跨模型结果比较。


============================================================
十、本阶段形成的主要成果
============================================================

本阶段形成了以下几类成果。

第一，建立了从候选级 ColabFold 数据到代表候选的筛选流程。

筛选不再仅依赖某一项指标的排名，而是结合六项 mean 指标相对于参考候选的表现、人工判断以及后续序列聚类，形成了更具可追溯性的候选缩减流程。

第二，完成了 67 条候选的序列聚类和类群信息整理。

主方案采用 31 aa 序列逐位比较和 complete-linkage 聚类，在最多 3 个氨基酸差异的限制下得到 16 个类群，并对阈值敏感性进行了检查。

第三，建立了类群代表与补充候选相结合的选择策略。

通过主代表、次代表、medoid 和相对序列差异等信息，减少了高度相似候选的重复保留，同时尽量保留有价值的序列变体。

第四，形成了 27 条候选的 Boltz-2 输入 FASTA。

这份输入集合包含 24 条代表候选及 D13、D41、D44 三条指定参考序列，为下一阶段的预测任务提供了候选清单。

第五，建立了 GLP1R 自定义 MSA 的初步处理流程。

原始同源序列经过字符检查、去重、MAFFT 比对和 A3M 转换，形成了 396 条记录的 A3M 文件，并确认其中 query 与 395 aa 输入序列完全一致。

第六，明确了后续预测中必须解决的受体序列一致性问题。

通过比较结构坐标序列和构建序列，确认了 384 aa 与 395 aa 两种输入方案的区别，并明确 MSA query 与正式受体输入必须保持一致。

这些成果使项目从 ColabFold 的初步候选评价推进到代表候选的确定和 Boltz-2 预测准备阶段。


============================================================
十一、本阶段的局限与后续工作
============================================================

11.1 筛选阈值尚未经过实验校准

当前筛选规则是基于已有预测指标和参考候选的相对比较建立的。

即使某条候选在六项 mean 指标上超过 D13 或 D44，也不能据此直接判断它具有更高的真实结合亲和力。

后续应将这些筛选规则视为候选优先级的计算依据，并结合其他预测结果以及可能获得的实验数据进一步校准。

11.2 聚类结果依赖序列差异阈值

在当前数据集下，最大差异不超过 2、3、4 个氨基酸时分别得到 24、16、9 个类群。

因此，16 个类群是当前主方案的结果，不是唯一的生物学分类。

后续如果需要对序列家族作更严格的定义，应进一步明确聚类标准，并确保不同版本的类群编号不会被混用。

11.3 代表候选不等于最终最优候选

类群 medoid、Primary representative 和 Secondary representative 分别服务于不同的选择目的。

序列中心性较高的候选不一定具有最高结构指标；结构指标较高的候选也不一定是类群中心。

因此，后续应继续保留候选 ID、原始序列、类群、指标来源和选择原因，避免将内部代表标签误解为最终生物学排名。

11.4 自定义 MSA 尚未通过 Boltz-2 实测验证

当前 A3M 已完成基本格式和 query 检查，但尚未完成正式 Boltz-2 预测验证。

后续需要确认实际输入格式、MSA 路径、受体序列长度以及预测输出的链对应关系。

尤其是 384 aa 与 395 aa 两种受体输入不能与同一份 query 不一致的 MSA 混用。

11.5 预测结果仍然属于计算证据

无论 ColabFold 还是 Boltz-2，其输出均属于计算预测结果。

不同预测器给出一致结果可以提高后续研究的优先级，但不能自动等同于真实结合、激动活性或实验亲和力。

后续如果获得实验数据，应进一步比较计算指标与实验结果之间的对应关系。


============================================================
十二、下一阶段的工作安排
============================================================

下一阶段的优先事项为：

1. 明确 GLP1R 受体正式输入使用 384 aa 还是 395 aa 序列。
2. 核对最终受体序列与自定义 A3M query 的逐位一致性。
3. 检查当前 Boltz-2 版本对自定义 A3M 的输入方式，并准备对应 YAML。
4. 对单个候选开展小规模测试，确认 Boltz-2 能够正常读取输入并生成结果。
5. 检查预测输出中的受体链和候选肽链是否与输入相符。
6. 在输入和输出检查通过后，再对 27 条候选执行正式预测。
7. 汇总 Boltz-2 输出的结构、置信度和相关评价指标。
8. 将 Boltz-2 结果与 ColabFold 候选级数据进行对应，分析两种预测体系之间的一致性和差异。
9. 在保留原始数据、输入清单和计算条件的基础上，开展进一步候选排序与优先级判断。

本阶段的工作使项目完成了候选数据筛选、序列家族整理和代表候选组织，并初步建立了 GLP1R 自定义 MSA。

下一阶段的重点将从“确定哪些候选进入下一轮计算”转向“确保输入正确、完成 Boltz-2 预测，并检验不同计算体系对候选结构评价的支持程度”。
```

这份记录已经把第十阶段的主线整理出来了：**241 条数据 → 67 条保留候选 → 16 个序列类群 → 24 条代表候选 → 27 条 Boltz 输入 → 395 aa 自定义 MSA 准备**。我也特别保留了目前尚未完成 Boltz-2 实测验证这一状态，避免把输入准备写成正式预测已完成。

如果你后续希望我提醒你继续完成受体序列与 MSA 的一致性检查，并推进 Boltz-2 小规模测试，也可以告诉我。

---

# you asked

message time: 2026-10-22 14:05:20

现在可以开始跑boltz了，不过27条候选的yaml文件还没有生成

---

# chatgpt response

可以。我们现在进入 **GLP1R 的 Boltz-2 复核阶段**。27 条候选的 YAML 还没生成不影响进度，我们先把输入文件规范好，再跑单条测试，确认无误后批量跑完 27 条。

这里有一个关键点要先处理：**目前自定义 MSA 的 Query 是 395 aa，而此前的 GLP1R 结构链 R 是 384 aa。** YAML 中受体序列必须和我们最终选择的 MSA Query 对齐，不能直接把 384 aa 的受体序列与 395 aa 的 MSA 混用。我们先检查现有文件和 Boltz-2 的输入格式，不急着生成可能有问题的 YAML。

## 第一步：检查现有文件和 Boltz-2 输入格式

请在 WSL Ubuntu 中执行下面整段命令。它只读取文件、查看环境，不会修改现有数据。



如果你的 Boltz 环境不叫 `boltz`，第一行 `conda activate boltz` 报错也没关系，先把报错一起发给我，不要为了执行后续命令临时创建新环境。

## 第二步：接下来怎么生成 27 份 YAML

我们按下面的顺序推进：

1. **确认 27 条 FASTA 的记录名和序列。** 其中应包含 24 条代表候选，以及 D13、D41、D44 三条参照序列。
2. **确定受体序列版本。** 检查 395 aa 的 Query 是否确实是当前选定的受体序列；确认之后，候选 YAML 中的受体序列与 MSA Query 保持一致。
3. **沿用现有 Boltz-2 输入规范。** 根据项目里已有的 YAML 示例和协议确定链 ID、MSA 路径、配体序列及输出设置，不凭空假设字段。
4. **生成 27 份 YAML。** 每条候选独立一个输入文件，统一放进新的运行目录，避免覆盖旧结果。
5. **逐份校验后先跑单条测试。** 检查 Boltz 是否正常读取 MSA、受体和 binder 链长度是否正确、输出文件是否完整。
6. **单条测试通过后再批量运行 27 条。** 最后统计成功、失败、缺失输出及日志，保留可追溯的运行记录。

**现在先执行第一步，把终端输出贴过来。** 我们据此确定 YAML 的准确格式和 395 aa 受体的输入方式，再生成文件，不需要你手工编写 27 份 YAML。

---

# you asked

message time: 2026-10-22 14:08:38

========== 1. Boltz-2 环境 ==========
USER_HOME/miniconda3/envs/boltz/bin/boltz
Usage: boltz predict [OPTIONS] DATA

  Run predictions with Boltz.

Options:
  --out_dir PATH                  The path where to save the predictions.
  --cache PATH                    The directory where to download the data and
                                  model. Default is ~/.boltz, or $BOLTZ_CACHE
                                  if set.
  --checkpoint PATH               An optional checkpoint, will use the
                                  provided Boltz-1 model by default.
  --devices INTEGER               The number of devices to use for prediction.
                                  Default is 1.
  --accelerator [gpu|cpu|tpu]     The accelerator to use for prediction.
                                  Default is gpu.
  --recycling_steps INTEGER       The number of recycling steps to use for
                                  prediction. Default is 3.
  --sampling_steps INTEGER        The number of sampling steps to use for
                                  prediction. Default is 200.
  --diffusion_samples INTEGER     The number of diffusion samples to use for
                                  prediction. Default is 1.
  --max_parallel_samples INTEGER  The maximum number of samples to predict in
                                  parallel. Default is None.
  --step_scale FLOAT              The step size is related to the temperature
                                  at which the diffusion process samples the
                                  distribution. The lower the higher the
                                  diversity among samples (recommended between
                                  1 and 2). Default is 1.638 for Boltz-1 and
                                  1.5 for Boltz-2. If not provided, the
                                  default step size will be used.
  --write_full_pae                Whether to dump the pae into a npz file.
                                  Default is True.
  --write_full_pde                Whether to dump the pde into a npz file.
                                  Default is False.
  --output_format [pdb|mmcif]     The output format to use for the
                                  predictions. Default is mmcif.
  --num_workers INTEGER           The number of dataloader workers to use for
                                  prediction. Default is 2.
  --override                      Whether to override existing found
                                  predictions. Default is False.
  --seed INTEGER                  Seed to use for random number generator.
                                  Default is None (no seeding).
  --use_msa_server                Whether to use the MMSeqs2 server for MSA
                                  generation. Default is False.
  --msa_server_url TEXT           MSA server url. Used only if
                                  --use_msa_server is set.
  --msa_pairing_strategy TEXT     Pairing strategy to use. Used only if
                                  --use_msa_server is set. Options are
                                  'greedy' and 'complete'
  --msa_server_username TEXT      MSA server username for basic auth. Used
                                  only if --use_msa_server is set. Can also be
                                  set via BOLTZ_MSA_USERNAME environment
                                  variable.
  --msa_server_password TEXT      MSA server password for basic auth. Used
                                  only if --use_msa_server is set. Can also be
                                  set via BOLTZ_MSA_PASSWORD environment
                                  variable.
  --api_key_header TEXT           Custom header key for API key authentication
                                  (default: X-API-Key).
  --api_key_value TEXT            Custom header value for API key
                                  authentication.
  --use_potentials                Whether to use potentials for steering.
                                  Default is False.
  --model [boltz1|boltz2]         The model to use for prediction. Default is
                                  boltz2.
  --method TEXT                   The method to use for prediction. Default is
                                  None.
  --preprocessing-threads INTEGER
                                  The number of threads to use for
                                  preprocessing. Default is 1.
  --affinity_mw_correction        Whether to add the Molecular Weight
                                  correction to the affinity value head.
  --sampling_steps_affinity INTEGER
                                  The number of sampling steps to use for
                                  affinity prediction. Default is 200.
  --diffusion_samples_affinity INTEGER
                                  The number of diffusion samples to use for
                                  affinity prediction. Default is 5.
  --affinity_checkpoint PATH      An optional checkpoint, will use the
                                  provided Boltz-1 model by default.
  --max_msa_seqs INTEGER          The maximum number of MSA sequences to use
                                  for prediction. Default is 8192.
  --subsample_msa                 Whether to subsample the MSA. Default is
                                  True.
  --num_subsampled_msa INTEGER    The number of MSA sequences to subsample.
                                  Default is 1024.
  --no_kernels                    Whether to disable the kernels. Default
                                  False
  --write_embeddings              to dump the s and z embeddings into a npz
                                  file. Default is False.
  --help                          Show this message and exit.

========== 2. 27条候选FASTA ==========

========== 3. 自定义MSA ==========
-rwxrwxrwx 1 ziguimu ziguimu 191K Oct 22 13:21 LOCAL_PATH
>GLP1R_QUERY_395AA
TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWPDGEPGSFVNVSCPWY
LPWASSVPQGHVYRFCTAEGLWLQKDNSSLPWRDLSECEESKRGERSSPEEQLLFLYIIY
TVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTA
AQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRL

========== 4. 现有YAML示例 ==========

========== 5. Boltz相关协议与配置 ==========

---

# chatgpt response

从这次输出可以确定三件事：

1. **Boltz-2 环境正常。** 已找到 `USER_HOME/miniconda3/envs/boltz/bin/boltz`，并且能正常读取命令参数。
2. **自定义 MSA 文件存在。** `LOCAL_PATH 已生成，Query 为 395 aa。
3. **27 条候选 FASTA、现有 YAML 示例和 Boltz 协议文件都没有在刚才搜索的范围内找到。** 这不代表文件一定不存在；可能是文件名或存放位置不同。我们先定位文件，再生成输入，避免重新制作已有数据或猜测 MSA 格式。

## 第一步：定位 27 条候选和现有项目文件

请继续在 WSL 中执行下面这段命令。它会扩大搜索范围，同时检查已有候选筛选结果。



## 第二步：确认本机 Boltz-2 支持的 MSA 格式

我们也需要确认当前安装版本对自定义 A3M 的具体支持方式，不能仅凭其他版本的示例写 YAML。

执行：



第二段会打印源码目录。先把输出发给我即可，我会根据你当前安装的版本，指导你查找实际的输入字段和 MSA 处理逻辑。

## 第三步：生成 YAML 前必须解决的序列问题

当前 MSA 的 Query 是 395 aa，而结构链 R 的序列是 384 aa。我们不能直接认定 395 aa 一定更好，也不能把两种长度混用。

- 如果最终使用 **395 aa 受体**，YAML 中的受体序列应与 A3M Query 一致，并确认新增的 11 个残基确实对应原结构序列中缺失的片段。
- 如果最终使用 **384 aa 受体**，则需要确认能否为该序列构建匹配的 MSA，不能直接把现有 395 aa A3M 当成完全匹配的输入。
- 还需要确认候选 binder 的链分配方式和 YAML 中 MSA 路径的写法。

**目前先不要启动 27 条正式预测。** 下一步先把上述命令输出发给我，重点是 FASTA 搜索结果、筛选文件路径和 Boltz 源码目录。定位成功后，我们再生成 27 份 YAML，并先用一条候选进行端到端测试。

---

# you asked

message time: 2026-10-22 14:17:34

(boltz) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH conda activate boltz

python - <<'PY'
import boltz
print("Boltz module:", boltz.__file__)
PY

python - <<'PY'
import os
import boltz
root = os.path.dirname(boltz.__file__)
print("Boltz source:", root)
PY
Boltz module: USER_HOME/miniconda3/envs/boltz/lib/python3.11/site-packages/boltz/__init__.py
Boltz source: USER_HOME/miniconda3/envs/boltz/lib/python3.11/site-packages/boltz
(boltz) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH"LOCAL_PATH (11).fasta"

---

# chatgpt response

好，找到这 27 条待测序列的来源了。Windows 路径：

`LOCAL_PATH (11).fasta`

在 WSL 中通常对应：

`LOCAL_PATH (11).fasta`

我们先验证文件确实存在、记录数是否为 27，再检查 Boltz 当前版本对自定义 MSA 的输入要求。**暂时不改动原始 FASTA，也不启动整批预测。**

## 第一步：检查 27 条 FASTA

请在当前 `(boltz)` 终端执行：



重点确认：

- 是否恰好有 27 条记录；
- 24 条代表候选和 D13、D41、D44 是否都在；
- binder 序列是否均为预期的 31 aa；
- 是否存在重复名称、空序列或非标准氨基酸。

## 第二步：检查 Boltz 源码中的 MSA 输入规范

你的 Boltz 模块位置已经确认：

`USER_HOME/miniconda3/envs/boltz/lib/python3.11/site-packages/boltz`

接着执行：



这一步是为了确认当前安装版本实际支持的 YAML 字段和 MSA 文件格式，而不是套用其他版本的示例。

## 接下来会怎么做

拿到这两部分输出后，我们按顺序完成：

1. 确认 27 条序列及候选名称。
2. 根据当前 Boltz 源码和官方输入规范，确定 YAML 结构及自定义 MSA 的引用方式。
3. 解决 **384 aa 结构链与 395 aa MSA Query** 的一致性问题。
4. 生成 27 份 YAML，统一放入独立的新运行目录。
5. 先测试一条候选，确认日志、链长度、MSA 加载及输出文件正常，再运行全部 27 条。

注意：**现在还不能把 395 aa MSA 直接分配给所有候选。** 必须先确认 YAML 的受体序列与 MSA Query 一致，并验证 Boltz 确实按预期读取该 MSA。

---

# you asked

message time: 2026-10-22 14:19:09

========== 文件检查 ==========
-rwxrwxrwx 1 ziguimu ziguimu 2.1K Oct 22 08:46 'LOCAL_PATH (11).fasta'

========== FASTA记录数 ==========
27

========== 所有序列名称 ==========
>candidate_0044|T3_C05|Primary_representative
>candidate_0093|T3_C03|Primary_representative
>candidate_0228|T3_C10|Primary_representative
>candidate_0112|T3_C03|Secondary_representative
>candidate_0227|T3_C04|Primary_representative
>candidate_0153|T3_C10|Secondary_representative
>candidate_0062|T3_C05|Secondary_representative
>candidate_0175|T3_C02|Primary_representative
>candidate_0213|T3_C11|Primary_representative
>candidate_0200|T3_C13|Primary_representative
>candidate_0129|T3_C14|Primary_representative
>candidate_0219|T3_C11|Secondary_representative
>candidate_0082|T3_C13|Secondary_representative
>candidate_0081|T3_C02|Secondary_representative
>candidate_0027|T3_C09|Primary_representative
>candidate_0009|T3_C01|Primary_representative
>candidate_0046|T3_C04|Secondary_representative
>candidate_0021|T3_C09|Secondary_representative
>candidate_0071|T3_C12|Primary_representative
>candidate_0051|T3_C06|Primary_representative
>candidate_0096|T3_C07|Primary_representative
>candidate_0111|T3_C06|Secondary_representative
>candidate_0043|T3_C07|Secondary_representative
>candidate_0170|T3_C15|Primary_representative
>candidate_0165|reference_D13|control_reference
>candidate_0173|reference_D44|control_reference
>candidate_0241|reference_D41|control_reference

========== 序列长度 ==========
记录数: 27
candidate_0044|T3_C05|Primary_representative    长度=31 非标准字符=[]
candidate_0093|T3_C03|Primary_representative    长度=31 非标准字符=[]
candidate_0228|T3_C10|Primary_representative    长度=31 非标准字符=[]
candidate_0112|T3_C03|Secondary_representative  长度=31 非标准字符=[]
candidate_0227|T3_C04|Primary_representative    长度=31 非标准字符=[]
candidate_0153|T3_C10|Secondary_representative  长度=31 非标准字符=[]
candidate_0062|T3_C05|Secondary_representative  长度=31 非标准字符=[]
candidate_0175|T3_C02|Primary_representative    长度=31 非标准字符=[]
candidate_0213|T3_C11|Primary_representative    长度=31 非标准字符=[]
candidate_0200|T3_C13|Primary_representative    长度=31 非标准字符=[]
candidate_0129|T3_C14|Primary_representative    长度=31 非标准字符=[]
candidate_0219|T3_C11|Secondary_representative  长度=31 非标准字符=[]
candidate_0082|T3_C13|Secondary_representative  长度=31 非标准字符=[]
candidate_0081|T3_C02|Secondary_representative  长度=31 非标准字符=[]
candidate_0027|T3_C09|Primary_representative    长度=31 非标准字符=[]
candidate_0009|T3_C01|Primary_representative    长度=31 非标准字符=[]
candidate_0046|T3_C04|Secondary_representative  长度=31 非标准字符=[]
candidate_0021|T3_C09|Secondary_representative  长度=31 非标准字符=[]
candidate_0071|T3_C12|Primary_representative    长度=31 非标准字符=[]
candidate_0051|T3_C06|Primary_representative    长度=31 非标准字符=[]
candidate_0096|T3_C07|Primary_representative    长度=31 非标准字符=[]
candidate_0111|T3_C06|Secondary_representative  长度=31 非标准字符=[]
candidate_0043|T3_C07|Secondary_representative  长度=31 非标准字符=[]
candidate_0170|T3_C15|Primary_representative    长度=31 非标准字符=[]
candidate_0165|reference_D13|control_reference  长度=31 非标准字符=[]
candidate_0173|reference_D44|control_reference  长度=31 非标准字符=[]
candidate_0241|reference_D41|control_reference  长度=31 非标准字符=[]
(boltz) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH

---

# chatgpt response

很好，**27 条候选 FASTA 已经通过第一轮检查，可以作为本次 Boltz-2 批量复核的 binder 输入。**

检查结果：

- 共 27 条序列：24 条代表候选 + D13、D44、D41 三条参照。
- 每条 binder 都是 31 aa。
- 全部只包含标准氨基酸字符。
- 三条参照的对应关系正确：`candidate_0165 = D13`、`candidate_0173 = D44`、`candidate_0241 = D41`。

现在还不能生成最终 YAML，因为需要先确认当前 Boltz 版本的自定义 MSA 输入规范，并解决受体序列与 MSA Query 的长度问题。

## 下一步：检查 Boltz-2 的真实输入格式

你刚才贴出的结果只包含 FASTA 检查部分，源码检查部分还没有输出。请直接复制执行下面这段更精简的命令：



## 接下来要特别确认的受体序列问题

目前我们手头有两个长度版本：

| 版本 | 长度 | 说明 |
|---|---:|---|
| 7KI0 链 R | 384 aa | 由结构中实际存在坐标的残基提取 |
| 补回缺失片段的 Query | 395 aa | 在序列中补回 11 个缺失坐标的残基 |

395 aa 比 384 aa 多出的残基对应结构中缺失的片段，但**序列补齐不代表我们已经恢复了这些残基的实际空间构象**。

我的建议是先保留现有 395 aa A3M，不要重做；根据 Boltz 当前版本的代码确认 MSA 引用格式，然后检查 395 aa 受体序列能否与它正确配对。确认后再生成 YAML。

拿到这次源码检查结果，我们就可以进入生成 27 份 YAML 的步骤，随后先跑一条测试，验证 MSA 确实被加载，再启动整批预测。

---

# you asked

message time: 2026-10-22 14:21:53

*(No content)*

---

# chatgpt response

输出收到了。现在已经确认：

- Boltz 版本是 **2.2.1**。
- 27 条候选 FASTA 路径有效，记录数和序列长度检查已通过。
- 自定义 MSA 文件为 `glp1r_395aa_custom.a3m`。
- 之前的源码搜索主要命中了模型内部的 MSA 模块，**还没有定位到解析 YAML 和读取自定义 A3M 的代码**，因此现在还不能据此确定 YAML 的确切写法。

下一步我们直接定位输入解析器，不再重复前面的检查。

## 请执行这段命令



把完整输出贴过来即可。

## 后续处理方案

我们会以当前安装的 Boltz 2.2.1 源码为准，确认下面这些问题后再生成文件：

1. YAML 是否支持直接指定自定义 A3M 文件路径，以及具体字段名称。
2. MSA 的 Query 与受体序列是否需要逐位完全一致。
3. 如何为 27 条 binder 分别生成输入，同时复用同一份受体 MSA。
4. 如何先运行一条候选验证输入，再启动全部 27 条预测。

受体序列方面，目前最直接的方案是优先验证 **395 aa 受体序列 + 395 aa Query 的自定义 MSA**。这能避免受体序列和 MSA 长度不一致的问题，但仍需检查序列补齐方式以及 Boltz 的实际读取行为。

在确认解析规则前，先不批量生成 YAML，也不启动正式预测，避免 27 条任务一起因为输入格式错误而失败。

---

# you asked

message time: 2026-10-22 14:22:56

*(No content)*

---

# chatgpt response

这次输出已经定位到关键代码了，下一步不需要再做泛泛的 `grep` 搜索。

**目前最重要的发现：**

- 你的 Boltz 版本是 `2.2.1`。
- `boltz/main.py` 的 605–624 行会检查 MSA 路径，并支持 `.a3m` 和 `.csv` 文件。
- `boltz/data/parse/schema.py` 的 957–961 行包含 MSA 字段的示例。
- 这说明当前版本存在通过输入字段指定 MSA 文件的处理路径；但我们还需要核实 YAML 结构、相对路径的解析方式，以及受体序列是否与 A3M Query 匹配。

## 下一步：直接查看关键源码

请在当前 `(boltz)` 终端执行下面这段命令。它只读取源码，不会修改任何文件。



## 看完后，我们就进入实际生成阶段

计划采用一个独立目录，例如：



每份 YAML 对应一条 binder，复用同一份经过核验的受体 MSA，并在清单中记录候选 ID、binder 序列、受体序列版本和输入文件路径。原始 FASTA 和现有 MSA 都保留不动。

有一点需要特别强调：**395 aa 的序列补齐方案仍需核验，不能仅仅因为它与 MSA Query 长度一致，就认定它在生物学上必然优于 384 aa 结构链。** 我们会先检查补齐后的序列和现有 MSA，再运行一条测试候选；确认输入正常、MSA 被正确读取后，才启动全部 27 条预测。

把这次四段源码输出贴过来，我们就能据此确定 YAML 的具体字段，不再反复做前置检查。

---

# you asked

message time: 2026-10-22 14:23:53

*(No content)*

---

# chatgpt response

这份输出已经确认了 Boltz-2 的关键输入规则：**可以在 YAML 中为 GLP-1R 指定现成的 `.a3m` 文件，不需要重新通过 MSA Server 搜索。** 对我们这次的 27 条 binder，建议先做一个单候选测试，确认输入解析和 MSA 读取正常，再批量运行。

目前还需要核实一个细节：安装的 Boltz 2.2.1 如何处理 `msa: empty`，以及 YAML 中相对路径和绝对路径的实际解析方式。先不要直接启动 27 个预测，避免输入格式错误导致整批失败。

## 下一步：核实 `msa` 的解析逻辑

请在 WSL 终端运行下面这组命令，把完整输出贴回来：



### 核实后我们会按这个顺序推进

1. **输入校验：** 检查 27 条 binder 的序列、395 aa 受体序列，以及 A3M 查询序列是否一致。
2. **生成输入：** 为每个候选建立独立 YAML，受体链 A 使用自定义 MSA，binder 链 B 的 MSA 设置则以本机源码确认的规则为准。
3. **单例试跑：** 先跑一个候选，检查预测是否正常生成、日志是否有报错、输出文件是否完整。
4. **批量预测：** 单例通过后再运行 27 个候选，并保存输入清单、参数、日志和预测结果，便于后续与 ColabFold 对比。

有一点需要始终保留在实验记录里：**395 aa 序列中补回的 11 个残基并不等于补回了缺失的结构坐标。** 预测模型可能会为这些位置生成构象，但不能将其当作实验结构中已有的坐标。

如果你希望，我也可以在这次预测流程中安排一次后续提醒，检查 27 个任务是否全部完成，并继续分析 Boltz-2 与 ColabFold 的结果。

---

# you asked

message time: 2026-10-22 14:24:20

继续

---

# you asked

message time: 2026-10-22 14:24:40

========== 1. YAML输入格式示例 ==========
    chain_name, residue_index_or_atom_name, chain_to_idx, atom_idx_map, chains
):
    if chains[chain_name].type == const.chain_type_ids["NONPOLYMER"]:
        # Non-polymer chains are indexed by atom name
        _, _, atom_idx = atom_idx_map[(chain_name, 0, residue_index_or_atom_name)]
        return (chain_to_idx[chain_name], atom_idx)
    else:
        # Polymer chains are indexed by residue index
        return chain_to_idx[chain_name], residue_index_or_atom_name - 1


def parse_boltz_schema(  # noqa: C901, PLR0915, PLR0912
    name: str,
    schema: dict,
    ccd: Mapping[str, Mol],
    mol_dir: Optional[Path] = None,
    boltz_2: bool = False,
) -> Target:
    """Parse a Boltz input yaml / json.

    The input file should be a dictionary with the following format:

    version: 1
    sequences:
        - protein:
            id: A
            sequence: "MADQLTEEQIAEFKEAFSLF"
            msa: path/to/msa1.a3m
        - protein:
            id: [B, C]
            sequence: "AKLSILPWGHC"
            msa: path/to/msa2.a3m
        - rna:
            id: D
            sequence: "GCAUAGC"
        - ligand:
            id: E
            smiles: "CC1=CC=CC=C1"
    constraints:
        - bond:
            atom1: [A, 1, CA]
            atom2: [A, 2, N]
        - pocket:
            binder: E
            contacts: [[B, 1], [B, 2]]
            max_distance: 6
        - contact:
            token1: [A, 1]
            token2: [B, 1]
            max_distance: 6
    templates:
        - cif: path/to/template.cif
    properties:
        - affinity:
            binder: E

    Parameters
    ----------
    name : str
        A name for the input.
    schema : dict

========== 2. YAML解析器 ==========
from pathlib import Path

import yaml
from rdkit.Chem.rdchem import Mol

from boltz.data.parse.schema import parse_boltz_schema
from boltz.data.types import Target


def parse_yaml(
    path: Path,
    ccd: dict[str, Mol],
    mol_dir: Path,
    boltz2: bool = False,
) -> Target:
    """Parse a Boltz input yaml / json.

    The input file should be a yaml file with the following format:

    sequences:
        - protein:
            id: A
            sequence: "MADQLTEEQIAEFKEAFSLF"
        - protein:
            id: [B, C]
            sequence: "AKLSILPWGHC"
        - rna:
            id: D
            sequence: "GCAUAGC"
        - ligand:
            id: E
            smiles: "CC1=CC=CC=C1"
        - ligand:
            id: [F, G]
            ccd: []
    constraints:
        - bond:
            atom1: [A, 1, CA]
            atom2: [A, 2, N]
        - pocket:
            binder: E
            contacts: [[B, 1], [B, 2]]
    templates:
        - path: /path/to/template.pdb
          ids: [A] # optional, specify which chains to template

    version: 1

    Parameters
    ----------
    path : Path
        Path to the YAML input format.
    components : Dict
        Dictionary of CCD components.
    boltz2 : bool
        Whether to parse the input for Boltz2.

    Returns
    -------
    Target
        The parsed target.

    """
    with path.open("r") as file:
        data = yaml.safe_load(file)

    name = path.stem
    return parse_boltz_schema(name, data, ccd, mol_dir, boltz2)

========== 3. MSA路径读取与处理 ==========
            if (chain.mol_type == prot_id) and (chain.msa_id == 0):
                entity_id = chain.entity_id
                msa_id = f"{target_id}_{entity_id}"
                to_generate[msa_id] = target.sequences[entity_id]
                chain.msa_id = msa_dir / f"{msa_id}.csv"

            # We do not support msa generation for non-protein chains
            elif chain.msa_id == 0:
                chain.msa_id = -1

        # Generate MSA
        if to_generate and not use_msa_server:
            msg = "Missing MSA's in input and --use_msa_server flag not set."
            raise RuntimeError(msg)  # noqa: TRY301

        if to_generate:
            msg = f"Generating MSA for {path} with {len(to_generate)} protein entities."
            click.echo(msg)
            compute_msa(
                data=to_generate,
                target_id=target_id,
                msa_dir=msa_dir,
                msa_server_url=msa_server_url,
                msa_pairing_strategy=msa_pairing_strategy,
                msa_server_username=msa_server_username,
                msa_server_password=msa_server_password,
                api_key_header=api_key_header,
                api_key_value=api_key_value,
            )

        # Parse MSA data
        msas = sorted({c.msa_id for c in target.record.chains if c.msa_id != -1})
        msa_id_map = {}
        for msa_idx, msa_id in enumerate(msas):
            # Check that raw MSA exists
            msa_path = Path(msa_id)
            if not msa_path.exists():
                msg = f"MSA file {msa_path} not found."
                raise FileNotFoundError(msg)  # noqa: TRY301

            # Dump processed MSA
            processed = processed_msa_dir / f"{target_id}_{msa_idx}.npz"
            msa_id_map[msa_id] = f"{target_id}_{msa_idx}"
            if not processed.exists():
                # Parse A3M
                if msa_path.suffix == ".a3m":
                    msa: MSA = parse_a3m(
                        msa_path,
                        taxonomy=None,
                        max_seqs=max_msa_seqs,
                    )
                elif msa_path.suffix == ".csv":
                    msa: MSA = parse_csv(msa_path, max_seqs=max_msa_seqs)
                else:
                    msg = f"MSA file {msa_path} not supported, only a3m or csv."
                    raise RuntimeError(msg)  # noqa: TRY301

                msa.dump(processed)

        # Modify records to point to processed MSA
        for c in target.record.chains:
            if (c.msa_id != -1) and (c.msa_id in msa_id_map):
                c.msa_id = msa_id_map[c.msa_id]

        # Dump templates
        for template_id, template in target.templates.items():

========== 4. FASTA输入格式及MSA ID ==========
from collections.abc import Mapping
from pathlib import Path

from Bio import SeqIO
from rdkit.Chem.rdchem import Mol

from boltz.data.parse.yaml import parse_boltz_schema
from boltz.data.types import Target


def parse_fasta(  # noqa: C901, PLR0912
    path: Path,
    ccd: Mapping[str, Mol],
    mol_dir: Path,
    boltz2: bool = False,
) -> Target:
    """Parse a fasta file.

    The name of the fasta file is used as the name of this job.
    We rely on the fasta record id to determine the entity type.

    > CHAIN_ID|ENTITY_TYPE|MSA_ID
    SEQUENCE
    > CHAIN_ID|ENTITY_TYPE|MSA_ID
    ...

    Where ENTITY_TYPE is either protein, rna, dna, ccd or smiles,
    and CHAIN_ID is the chain identifier, which should be unique.
    The MSA_ID is optional and should only be used on proteins.

    Parameters
    ----------
    fasta_file : Path
        Path to the fasta file.
    ccd : Dict
        Dictionary of CCD components.
    mol_dir : Path
        Path to the directory containing the molecules.
    boltz2 : bool
        Whether to parse the input for Boltz2.

    Returns
    -------
    Target
        The parsed target.

    """
    # Read fasta file
    with path.open("r") as f:
        records = list(SeqIO.parse(f, "fasta"))

    # Make sure all records have a chain id and entity
    for seq_record in records:
        if "|" not in seq_record.id:
            msg = f"Invalid record id: {seq_record.id}"
            raise ValueError(msg)

        header = seq_record.id.split("|")
        assert len(header) >= 2, f"Invalid record id: {seq_record.id}"

        chain_id, entity_type = header[:2]
        if entity_type.lower() not in {"protein", "dna", "rna", "ccd", "smiles"}:
            msg = f"Invalid entity type: {entity_type}"
            raise ValueError(msg)
        if chain_id == "":
            msg = "Empty chain id in input fasta!"
            raise ValueError(msg)
        if entity_type == "":
            msg = "Empty entity type in input fasta!"
            raise ValueError(msg)

    # Convert to yaml format
    sequences = []
    for seq_record in records:
        # Get chain id, entity type and sequence
        header = seq_record.id.split("|")
        chain_id, entity_type = header[:2]
        if len(header) == 3 and header[2] != "":
            assert entity_type.lower() == "protein", (
                "MSA_ID is only allowed for proteins"
            )
            msa_id = header[2]
        else:
            msa_id = None

        entity_type = entity_type.upper()
        seq = str(seq_record.seq)

        if entity_type == "PROTEIN":
            molecule = {
                "protein": {
                    "id": chain_id,
                    "sequence": seq,
                    "modifications": [],
                    "msa": msa_id,
                },
            }
        elif entity_type == "RNA":
            molecule = {
                "rna": {
                    "id": chain_id,
                    "sequence": seq,
                    "modifications": [],
                },
            }
        elif entity_type == "DNA":
            molecule = {
                "dna": {
                    "id": chain_id,
                    "sequence": seq,
                    "modifications": [],
                }
            }
        elif entity_type.upper() == "CCD":
            molecule = {
                "ligand": {
                    "id": chain_id,
                    "ccd": seq,
                }
            }
        elif entity_type.upper() == "SMILES":
            molecule = {
                "ligand": {
                    "id": chain_id,
                    "smiles": seq,
                }
            }

        sequences.append(molecule)

    data = {
        "sequences": sequences,
        "bonds": [],
        "version": 1,
    }

    name = path.stem
    return parse_boltz_schema(name, data, ccd, mol_dir, boltz2)
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

我们继续。你贴回来的内容确认了 Boltz-2 能读取 `.a3m`，但这次输出仍然是上一轮的四段源码摘录，还没有包含我们需要核实的 `msa: empty` 处理逻辑，也没有文件存在性检查。

## 第一步：确认 MSA 规则和输入文件

请直接复制运行下面这组命令：


```

## 第二步：根据结果生成输入

目前已经确定的设计是：

- **链 A：** GLP-1R，395 aa，使用已有的自定义 A3M。
- **链 B：** 每条 31 aa 的 binder，每个候选独立预测。
- **候选数量：** 27 条，包括 24 个代表序列和 3 个参考序列。
- **预测策略：** 先测试一个候选，再批量运行，避免输入问题影响整批任务。

等你把上面这次的输出发回来，我就给你下一条可以直接运行的命令，生成输入 YAML 并验证解析。我们先不启动正式预测。

另外，等 27 个预测完成后，我也可以帮你安排一次提醒，继续检查结果并比较 Boltz-2 与 ColabFold。你需要我到时候提醒你吗？

---

# you asked

message time: 2026-10-22 14:28:53

========== 1. schema 中 msa 的具体处理 ==========
1119-                if (item_msa is None) or (item_msa == ""):
1120-                    item_msa = 0
1121-
1122-                if item_msa != msa:
1123-                    msg = "All proteins with the same sequence must share the same MSA!"
1124-                    raise ValueError(msg)
1125-
1126-            # Set the MSA, warn if passed in single-sequence mode
1127:            if msa == "empty":
1128-                msa = -1
1129-                msg = (
1130-                    "Found explicit empty MSA for some proteins, will run "
1131-                    "these in single sequence mode. Keep in mind that the "
1132-                    "model predictions will be suboptimal without an MSA."
1133-                )
1134-                click.echo(msg)
1135-
--
1791-    struct_info = StructureInfo(num_chains=len(chains))
1792-    chain_infos = []
1793-    for chain in chains:
1794-        chain_info = ChainInfo(
1795-            chain_id=int(chain["asym_id"]),
1796-            chain_name=chain["name"],
1797-            mol_type=int(chain["mol_type"]),
1798-            cluster_id=-1,
1799:            msa_id=chain_to_msa[chain["name"]],
1800-            num_residues=int(chain["res_num"]),
1801-            valid=True,
1802-            entity_id=int(chain["entity_id"]),
1803-        )
1804-        chain_infos.append(chain_info)
1805-
1806-    options = InferenceOptions(
1807-        pocket_constraints=pocket_constraints, contact_constraints=contact_constraints

========== 2. 输入文件检查 ==========
FASTA exists
-rwxrwxrwx 1 ziguimu ziguimu 2.1K Oct 22 08:46 'LOCAL_PATH (11).fasta'
MSA exists
-rwxrwxrwx 1 ziguimu ziguimu 191K Oct 22 13:21 LOCAL_PATH

========== 3. FASTA 记录数和序列长度 ==========
Records: 27
01      candidate_0044|T3_C05|Primary_representative    length=31
02      candidate_0093|T3_C03|Primary_representative    length=31
03      candidate_0228|T3_C10|Primary_representative    length=31
04      candidate_0112|T3_C03|Secondary_representative  length=31
05      candidate_0227|T3_C04|Primary_representative    length=31
06      candidate_0153|T3_C10|Secondary_representative  length=31
07      candidate_0062|T3_C05|Secondary_representative  length=31
08      candidate_0175|T3_C02|Primary_representative    length=31
09      candidate_0213|T3_C11|Primary_representative    length=31
10      candidate_0200|T3_C13|Primary_representative    length=31
11      candidate_0129|T3_C14|Primary_representative    length=31
12      candidate_0219|T3_C11|Secondary_representative  length=31
13      candidate_0082|T3_C13|Secondary_representative  length=31
14      candidate_0081|T3_C02|Secondary_representative  length=31
15      candidate_0027|T3_C09|Primary_representative    length=31
16      candidate_0009|T3_C01|Primary_representative    length=31
17      candidate_0046|T3_C04|Secondary_representative  length=31
18      candidate_0021|T3_C09|Secondary_representative  length=31
19      candidate_0071|T3_C12|Primary_representative    length=31
20      candidate_0051|T3_C06|Primary_representative    length=31
21      candidate_0096|T3_C07|Primary_representative    length=31
22      candidate_0111|T3_C06|Secondary_representative  length=31
23      candidate_0043|T3_C07|Secondary_representative  length=31
24      candidate_0170|T3_C15|Primary_representative    length=31
25      candidate_0165|reference_D13|control_reference  length=31
26      candidate_0173|reference_D44|control_reference  length=31
27      candidate_0241|reference_D41|control_reference  length=31
All sequences are 31 aa: True

========== 4. Boltz 版本 ==========
Usage: boltz [OPTIONS] COMMAND [ARGS]...
Try 'boltz --help' for help.

Error: No such option: --version

---

# chatgpt response

很好，这次检查通过了关键的输入文件验证。

- **27 条 FASTA 记录均存在，且每条 binder 都是 31 aa。**
- 自定义受体 MSA 文件存在，大小约 191 KB。
- Boltz 源码明确规定：`msa: empty` 会将该链设为单序列模式（不使用 MSA）；而提供 `.a3m` 路径时，程序会读取并处理该文件。<text color="secondary" size="sm">源码位置：`schema.py` 中的 MSA 处理逻辑，以及 `main.py` 中的 MSA 读取逻辑。</text>

还有一个小问题：`boltz --version` 不是该 CLI 支持的参数，因此报错不代表安装失败。我们可以用 Python 读取包版本。

**下一步先不跑模型，先自动生成 27 份 YAML，并验证受体序列与 A3M 查询序列完全一致。** 这里采用链 A = GLP-1R、链 B = binder；binder 使用 `msa: empty`，受体使用你已有的自定义 A3M。

---

# chatgpt response

## 第二步：生成 27 份 Boltz-2 输入 YAML

下面这段脚本会自动从 A3M 的第一条记录提取受体查询序列，验证其长度和氨基酸字符，再生成 27 份独立输入文件。这样不用手动复制 395 aa 的序列，也不会把序列补缺位的结构坐标误当作已有数据。

请在 WSL 中整段复制运行：



## 第三步：检查预测命令参数

只有当脚本显示 `SUCCESS` 且 `YAML files: 27` 后，再运行：



把这两段命令的输出贴回来。

### 接下来怎么做

我们会先选 `candidate_0044` 进行单候选试跑，检查：

- Boltz-2 是否成功解析 YAML 和 A3M；
- 链 A、链 B 是否按预期进入预测；
- 输出结构、置信度结果和日志是否正常；
- GPU 显存是否足够。

单例验证通过后，再批量运行其余候选。暂时不要加 `--use_msa_server`，因为受体已有自定义 MSA，而 binder 明确使用单序列模式；先保持输入条件固定，避免额外的 MSA 搜索改变实验条件。

---

# you asked

message time: 2026-10-22 14:31:53

SUCCESS
YAML files: 27
Input directory: LOCAL_PATH
Manifest: LOCAL_PATH

First input preview:
version: 1
sequences:
- protein:
    id: A
    sequence: TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWPDGEPGSFVNVSCPWYLPWASSVPQGHVYRFCTAEGLWLQKDNSSLPWRDLSECEESKRGERSSPEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANLMCKTDIKCRLAKSTLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLE
    msa: LOCAL_PATH
- protein:
    id: B
    sequence: HAEGTFTSDVSRYLEEKAVKAFVDRLKRGAG
    msa: empty

(boltz) ziguimu@DESKTOP-8RLFC97:~$ conda activate boltz

boltz predict --help | grep -E -A 2 \
  -- '--model|--out_dir|--recycling_steps|--sampling_steps|--diffusion_samples|--seed|--use_msa_server'
  --out_dir PATH                  The path where to save the predictions.
  --cache PATH                    The directory where to download the data and
                                  model. Default is ~/.boltz, or $BOLTZ_CACHE
--
  --recycling_steps INTEGER       The number of recycling steps to use for
                                  prediction. Default is 3.
  --sampling_steps INTEGER        The number of sampling steps to use for
                                  prediction. Default is 200.
  --diffusion_samples INTEGER     The number of diffusion samples to use for
                                  prediction. Default is 1.
  --max_parallel_samples INTEGER  The maximum number of samples to predict in
--
  --seed INTEGER                  Seed to use for random number generator.
                                  Default is None (no seeding).
  --use_msa_server                Whether to use the MMSeqs2 server for MSA
                                  generation. Default is False.
  --msa_server_url TEXT           MSA server url. Used only if
                                  --use_msa_server is set.
  --msa_pairing_strategy TEXT     Pairing strategy to use. Used only if
                                  --use_msa_server is set. Options are
                                  'greedy' and 'complete'
  --msa_server_username TEXT      MSA server username for basic auth. Used
                                  only if --use_msa_server is set. Can also be
                                  set via BOLTZ_MSA_USERNAME environment
                                  variable.
--
                                  only if --use_msa_server is set. Can also be
                                  set via BOLTZ_MSA_PASSWORD environment
                                  variable.
--
  --model [boltz1|boltz2]         The model to use for prediction. Default is
                                  boltz2.
  --method TEXT                   The method to use for prediction. Default is
--
  --sampling_steps_affinity INTEGER
                                  The number of sampling steps to use for
                                  affinity prediction. Default is 200.
  --diffusion_samples_affinity INTEGER
                                  The number of diffusion samples to use for
                                  affinity prediction. Default is 5.
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

很好，**27 份 YAML 已成功生成，命令行参数也确认支持我们需要的 Boltz-2 预测设置。** 现在可以进入单候选试跑阶段。

先提醒一个实验设计上的细节：你当前 YAML 中的链 A 使用 395 aa 受体序列及自定义 MSA，链 B 使用 31 aa binder 且 `msa: empty`。这意味着 binder 采用单序列模式，而不是为 binder 单独搜索 MSA；后续比较不同候选时应保持这一条件一致。

另外，当前预览中的受体序列长度为 395 aa，但这只能确认 YAML 使用了 A3M 第一条记录提取出的序列，**还不能单凭这段输出证明它与原始设计所依据的 GLP-1R 序列或实验结构完全一致**。这项核对可以在试跑期间单独做，不必阻塞当前的输入解析测试。

## 第四步：运行第一个候选 `candidate_0044`

先确认 GPU 状态，然后启动单候选预测。这里使用 `seed=37`、3 次 recycling、200 个 sampling steps 和 1 个 diffusion sample。先沿用 Boltz-2 的默认 sampling steps，不要为了提速同时改变多个参数。

在 WSL 终端运行：



注意：

- **不要添加 `--use_msa_server`**，因为受体已有指定的 A3M 文件。
- 你的 RTX 5070 Laptop GPU 是 8 GB 显存，395 aa 受体加 binder 的预测可能遇到显存不足。先观察单例，不要直接并行运行 27 个任务。
- 如果报错，不要立刻重跑；保存完整日志，我们先判断是 MSA 解析、模型下载、显存不足还是其他问题。

## 第五步：检查结果

等命令结束后，再运行：



把**预测命令的末尾日志、退出码，以及输出文件列表**贴给我。确认单例成功后，我们再决定是否直接批量运行 27 条，以及如何整理结构置信度指标和候选排序表。

如果你愿意，我也可以在你预计完成预测的时间后提醒你检查输出、继续做 Boltz-2 与 ColabFold 的对比。

---

# you asked

message time: 2026-10-22 14:32:25

seed取27

---

# chatgpt response

好的，单候选试跑的随机种子改为 **27**，其余参数保持不变。

把预测命令中的 `--seed 37` 改成：



完整命令如下：



后续如果批量预测也采用相同设置，建议统一使用 `seed=27`，并在实验记录中注明。注意：固定随机种子有助于提高可复现性，但不保证不同硬件或软件环境下结果完全一致。

---

# you asked

message time: 2026-10-22 14:33:19

tee: LOCAL_PATH No such file or directory
Seed set to 27
Checking input data.
Processing 1 inputs with 1 threads.
  0%|          | 0/1 [00:00<?, ?it/s]Found explicit empty MSA for some proteins, will run these in single sequence mode. Keep in mind that the model predictions will be suboptimal without an MSA.
100%|██████████| 1/1 [00:00<00:00,  5.10it/s]
Using bfloat16 Automatic Mixed Precision (AMP)
GPU available: True (cuda), used: True
TPU available: False, using: 0 TPU cores
HPU available: False, using: 0 HPUs
USER_HOME/miniconda3/envs/boltz/lib/python3.11/site-packages/pytorch_lightning/trainer/connectors/logger_connector/logger_connector.py:76: Starting from v1.9.0, `tensorboardX` has been removed as a dependency of the `pytorch_lightning` package, due to potential conflicts with other packages in the ML ecosystem. For this reason, `logger=True` will use `CSVLogger` as the default logger, unless the `tensorboard` or `tensorboardX` packages are found. Please `pip install lightning[extra]` or one of them to enable TensorBoard support by default
Running structure prediction for 1 input.

---

# chatgpt response

从日志看，**Boltz-2 已经启动结构预测，当前没有看到 GPU 或 MSA 格式错误**。现在有一个小问题：日志目录不存在，导致 `tee` 无法创建日志文件。

- `Seed set to 27`：随机种子已正确设置。
- `Found explicit empty MSA`：符合我们为 binder 链 B 设置 `msa: empty` 的方案。
- `GPU available: True`：已启用 GPU。
- `Running structure prediction for 1 input`：已进入结构预测阶段。

## 现在先这样做

**先不要中断当前进程。** 它可能正在继续计算，只是日志没有被保存。

等终端返回命令提示符后，执行以下命令检查预测输出：



如果终端长时间没有返回提示符，先观察 GPU 显存和利用率，不要急着启动第二次预测。

## 修复日志目录

当前预测结束后，再执行：



之后的任务就能正常写入 `logs` 目录。

**下一步：** 把预测结束后的输出文件列表和终端最后几行发给我。我会帮你确认是否成功生成结构文件、结果目录具体在哪里，以及是否可以开始剩余 26 个候选物的批量预测。

---

# you asked

message time: 2026-10-22 14:37:52

========== 输出文件 ==========
LOCAL_PATH  8 KB
LOCAL_PATH  304 KB
LOCAL_PATH      0 KB
LOCAL_PATH      628 KB
LOCAL_PATH      620 KB
LOCAL_PATH    4 KB
LOCAL_PATH       4 KB
LOCAL_PATH       0 KB
LOCAL_PATH      0 KB
LOCAL_PATH     20 KB
LOCAL_PATH  0 KB
LOCAL_PATH        12 KB

========== GPU 状态 ==========
Thu Oct 22 14:37:39 2026
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 590.57                 Driver Version: 591.86         CUDA Version: 13.1     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 5070 ...    On  |   00000000:02:00.0 Off |                  N/A |
| N/A   37C    P0             10W /  115W |    1917MiB /   8151MiB |      4%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

这次单候选预测已经生成了关键结构文件，**从输出看，`candidate_0044` 的 Boltz-2 预测流程大概率已完成，可以进入结果完整性检查。**

目前确认到：

- **结构文件已生成：** `candidate_0044_model_0.cif`，约 304 KB。
- **PAE 和 PDE 数据已生成：** 分别约 628 KB 和 620 KB。
- **pLDDT 数据已生成：** 约 4 KB。
- **GPU 显存：** 当前约占用 1.9 GB，GPU 利用率为 4%；预测进程已退出，符合任务结束后的状态。

但有一点需要注意：`confidence_candidate_0044_model_0.json` 显示为 `0 KB`，而且几个 JSON 文件也显示为 `0 KB`。这可能是文件本身为空，也可能是文件系统显示的大小经过了取整；我们应当检查实际字节数和预测目录中的汇总文件，再决定是否批量运行。

## 1. 先确认文件是否真的为空

在当前 WSL 终端直接运行：

`
之前的 `0 KB` 是按磁盘占用块数显示的，**不能单凭这个数字就判断文件为空**。

## 2. 如果结构和置信度文件都正常，再准备批量预测

先创建日志目录：

``建议剩余候选物继续统一使用以下参数：

| 参数 | 设置 |
|---|---|
| 模型 | Boltz-2 |
| Recycling steps | 3 |
| Sampling steps | 200 |
| Diffusion samples | 1 |
| Max parallel samples | 1 |
| Seed | 27 |
| GLP1R 链 A | 395 aa，使用自定义 A3M |
| Binder 链 B | 31 aa，`msa: empty` |

**先把第 1 步的精确文件大小和 JSON 内容发给我。** 确认后我们再启动剩余 26 个候选物，避免把异常结果批量复制到整套数据中。

---

# you asked

message time: 2026-10-22 14:38:35

========== 精确文件大小 ==========
651 bytes  LOCAL_PATH
656 bytes  LOCAL_PATH
641 bytes  LOCAL_PATH
309364 bytes  LOCAL_PATH

========== Confidence JSON 内容 ==========
{
    "confidence_score": 0.8288321495056152,
    "ptm": 0.9045966267585754,
    "iptm": 0.944831371307373,
    "ligand_iptm": 0.0,
    "protein_iptm": 0.944831371307373,
    "complex_plddt": 0.7998323440551758,
    "complex_iplddt": 0.736814022064209,
    "complex_pde": 0.4828665852546692,
    "complex_ipde": 0.9731285572052002,
    "chains_ptm": {
        "0": 0.9028254747390747,
        "1": 0.973287045955658
    },
    "pair_chains_iptm": {
        "0": {
            "0": 0.9028254747390747,
            "1": 0.8785755634307861
        },
        "1": {
            "0": 0.944831371307373,
            "1": 0.973287045955658
        }
    }
}
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

很好，`candidate_0044` 的结果文件完整，JSON 也确实包含数值，不是空文件。**单候选试跑可以通过初步检查，下一步可以准备批量预测。**

这次得到的关键指标如下：

| Boltz-2 指标 | candidate_0044 |
|---|---:|
| `confidence_score` | 0.8288 |
| `ptm` | 0.9046 |
| `iptm` | 0.9448 |
| `complex_plddt` | 0.7998 |
| `complex_iplddt` | 0.7368 |
| `complex_ipde` | 0.9731 |

注意：这些是**模型预测的结构置信度指标，不是实验结合亲和力或结合成功率**。尤其不能因为 `iptm = 0.9448` 就断定该候选物一定能结合 GLP-1R。后续还需要检查结合界面、结构合理性，并与其他候选物和参考对照进行一致条件下的比较。

## 3. 批量运行剩余 26 个候选物

下面的脚本会**逐个运行、统一使用 seed 27、保存每个候选物的日志，并记录成功或失败**。它会跳过已经完成的 `candidate_0044`，不会同时占满 GPU。

直接复制到终端执行：

```bash
cat意

- 这会依次提交 27 个 YAML 中尚未完成的候选物；`candidate_0044` 不会重复预测。
- 不建议在这个批次运行时同时启动其他 GPU 预测任务。
- 关闭终端可能中断任务。若预计运行时间较长，建议先保持当前终端打开。
- 脚本会在每个候选物完成后验证结构文件和置信度 JSON。若个别任务失败，不代表其余任务也会失败；状态表会记录问题。
- `success` 仅代表预测和基础文件检查通过，不代表候选物具有真实结合能力。

任务完成后，把 `batch_status.csv` 的内容发给我，我们就可以继续提取 27 个候选物的 `iptm`、`ptm`、`complex_plddt` 等指标，整理成与 ColabFold 结果可比较的汇总表。

另外，如果你希望，我也可以在后续某个时间提醒你检查这批预测结果、整理指标并开展 Boltz-2 与 ColabFold 的对比分析。

---

# you asked

message time: 2026-10-22 14:39:08

Max parallel samples是啥

---

# chatgpt response

`--max_parallel_samples` 是 Boltz-2 控制**同时并行处理多少个结构采样任务**的参数。

结合你现在的 GLP-1R 项目，可以这样理解。

## 1. 它和其他参数有什么区别？

| 参数 | 作用 | 你当前的设置 |
|---|---|---:|
| `--diffusion_samples` | 每个输入生成多少个扩散采样结果 | 1 |
| `--max_parallel_samples` | 最多同时处理多少个采样任务 | 1 |
| `--seed` | 控制随机数生成的种子 | 27 |
| `--recycling_steps` | 结构预测中的迭代更新次数 | 3 |
| `--sampling_steps` | 扩散采样过程的步数 | 200 |

举个例子：

- `diffusion_samples=1, max_parallel_samples=1`：一个输入生成一个采样结果，同时只处理一个采样任务。
- `diffusion_samples=4, max_parallel_samples=1`：一个输入生成四个采样结果，但最多同时处理一个采样任务。
- `diffusion_samples=4, max_parallel_samples=4`：请求四个采样结果，并允许最多同时处理四个采样任务；这可能显著增加显存需求。

## 2. 为什么你的 RTX 5070 Laptop 设为 1？

你目前的 GPU 显存是 **8 GB**，而 GLP-1R 受体序列有 395 aa，binder 有 31 aa，复合物总长度为 426 aa。

因此建议先保持：

```bash
--diffus外显存压力，降低多任务同时运行导致显存不足（OOM）的风险。

## 3. 对你的 27 个候选物意味着什么？

**`max_parallel_samples=1` 不代表整个项目只能预测一个候选物。**

你的批量脚本会依次预测 27 个 YAML，每个 YAML 生成一个采样结果。它控制的是单次 Boltz 预测内部的采样并行度，而不是项目总候选物数量。

另外，`diffusion_samples=1` 意味着每个候选物目前只生成一份预测结构。如果以后要研究预测稳定性，可以考虑对部分候选物使用多个采样结果，但应额外记录采样数量和随机种子，不能把单次预测的高置信度直接当作真实结合证据。

---

# you asked

message time: 2026-10-22 14:40:18

--diffusion_samples改成3，把刚刚跑出来的结果删掉，再重新跑27条

---

# chatgpt response

可以。我们把实验方案统一改成：

- `--diffusion_samples 3`
- `--max_parallel_samples 1`
- `--seed 27`
- `--recycling_steps 3`
- `--sampling_steps 200`

这样每个候选物请求生成 3 个扩散采样结果，27 个候选物总计请求 **81 个采样结果**。注意，具体生成数量仍需以 Boltz-2 实际输出为准。

你刚才的要求还包括删除旧预测结果并重新跑全部 27 条。由于我没有直接操作你 WSL 文件系统，而且你已经拒绝了交由 Work 执行，下面给你一套可以在本机执行的步骤。

## 第一步：检查并删除旧预测输出

**此操作会删除该项目 `predictions` 目录下的旧预测结果和 `logs` 目录下的旧日志，但保留输入 YAML、FASTA、MSA 和 `manifest.csv`。** 请先确认路径没有写错。



确认列出的都是本次 GLP1R 项目的旧结果后，再执行：



## 第二步：重新生成批量运行脚本

下面脚本会逐个运行 27 个候选物，每个候选物请求 3 个采样结果，逐条记录日志和状态。不会并行占用多个采样任务。



## 第三步：启动 27 条预测



运行期间不要再启动其他 GPU 预测任务。由于受体有 395 aa、每个 binder 有 31 aa，采样数增加到 3 后，运行时间和资源占用预计都会增加。

## 第四步：检查结果

全部运行完后执行：



**重要：** 这次的 3 个 diffusion samples 是同一个候选物的多个预测采样，不是 3 个独立实验，也不能把 3 个结构直接当作 3 个独立 binder。后续比较 ColabFold 与 Boltz-2 时，应当保留每个采样结果的指标，并明确记录汇总规则（例如每个候选物报告 3 个结果及其中位数），避免只挑最高分造成偏差。

---

# you asked

message time: 2026-10-22 18:22:28

========== 批量预测结束 ==========
状态表：LOCAL_PATH
candidate_id,status,exit_code
candidate_0009,success,0
candidate_0021,success,0
candidate_0027,success,0
candidate_0043,success,0
candidate_0044,success,0
candidate_0046,success,0
candidate_0051,success,0
candidate_0062,success,0
candidate_0071,success,0
candidate_0081,success,0
candidate_0082,success,0
candidate_0093,success,0
candidate_0096,success,0
candidate_0111,success,0
candidate_0112,success,0
candidate_0129,success,0
candidate_0153,success,0
candidate_0165,success,0
candidate_0170,success,0
candidate_0173,success,0
candidate_0175,success,0
candidate_0200,success,0
candidate_0213,success,0
candidate_0219,success,0
candidate_0227,success,0
candidate_0228,success,0
candidate_0241,success,0

---

# chatgpt response

很好，**27 个候选物的 Boltz-2 批量任务全部返回成功，退出码均为 0，没有脚本记录到的失败任务。**

这次采用的统一设置是：

- 模型：Boltz-2
- 随机种子：27
- `recycling_steps = 3`
- `sampling_steps = 200`
- `diffusion_samples = 3`
- `max_parallel_samples = 1`

接下来先不要急着按 `iptm` 排名。我们需要确认每个候选物是否实际生成了 3 个结构、读取每个采样对应的置信度指标，并检查输出是否完整。任务退出码为 0 是好消息，但还不等于每个候选物都一定有 3 份有效结果。

## 下一步：统计每个候选物实际生成的采样数并提取指标

在 WSL 里复制运行下面这段脚本。它会检查 27 个候选物的 CIF 和置信度 JSON，并生成逐采样明细表和每个候选物的汇总表。



正常情况下，应该看到 **27 个候选物、81 份有效采样记录、0 个完整性异常**。如果结果不同，以脚本实际报告为准。

生成的文件：

- `boltz_sample_metrics.csv`：每个模型采样的独立指标。
- `boltz_candidate_summary.csv`：每个候选物各指标的中位数、最小值和最大值。
- `boltz_validation_issues.txt`：缺失结构、缺失 JSON 或采样数不符合预期的记录。

中位数适合作为候选物的初步汇总，但不要只依据它筛选 binder；后面还应分析三个采样间的波动、界面几何和与参考对照的差异。

你运行后，把终端输出贴给我，我们继续检查并分析候选物排序。我也可以之后提醒你整理这批 Boltz-2 与 ColabFold 的对比结果；如果需要，告诉我希望何时提醒即可。

---

# you asked

message time: 2026-10-22 19:49:46

候选物数量：27
有效采样记录：81
预期采样记录：81
异常条目：0

逐采样指标：LOCAL_PATH
候选物汇总：LOCAL_PATH
检查报告：LOCAL_PATH

========== 检查报告 ==========
未发现采样数或文件完整性问题。

---

# chatgpt response

很好，当前这轮 Boltz-2 预测的**完整性检查全部通过**：

- 27 个候选物全部完成。
- 81/81 份采样记录有效，每个候选物都有 3 份有效结构及对应置信度数据。
- 0 个完整性异常。

这意味着我们可以进入下一阶段：**候选物质量分析，以及与 ColabFold 结果的交叉比较。**

## 接下来建议按这个顺序做

<box gap={3}>
  <row align=start gap={3}>
    <box background="surface-secondary" radius="lg" size="44px" align=center justify=center>
      <icon name="file-spreadsheet" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **1. 检查指标分布与采样稳定性**

      分析 27 个候选物的 `iptm`、`ptm`、`complex_plddt`、`complex_iplddt` 等指标，查看三个采样之间的中位数、范围和波动，避免只看最高分。
    </box>
  </row>
  <divider color="subtle" />
  <row align=start gap={3}>
    <box background="surface-secondary" radius="lg" size="44px" align=center justify=center>
      <icon name="git-compare" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **2. 与 ColabFold 结果交叉比较**

      对齐同一个候选物，检查两种模型的排序是否一致、哪些候选物存在明显分歧。不同模型的同名指标也不能默认完全等价。
    </box>
  </row>
  <divider color="subtle" />
  <row align=start gap={3}>
    <box background="surface-secondary" radius="lg" size="44px" align=center justify=center>
      <icon name="scan" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **3. 检查结合界面**

      对优先候选物检查链间接触、界面埋藏面积、关键相互作用和结构合理性。置信度分数高只能作为线索，不是实验结合证据。
    </box>
  </row>
</box>

## 现在先做第一步

请把这两个 CSV 文件上传到聊天中：

- `boltz_sample_metrics.csv`
- `boltz_candidate_summary.csv`

它们位于 `LOCAL_PATH

拿到实际数据后，我可以直接帮你生成候选物排序表、三次采样稳定性分析，以及下一步值得优先检查的候选物清单，不会凭空假设任何指标或阈值。

---

# you asked

message time: 2026-10-22 19:51:01

*(No content)*

---

# chatgpt response

我已经读取了你上传的两份 CSV。第一轮分析可以开始了：**27 个候选物的 Boltz-2 批次运行完整，81 个预测样本都通过文件完整性检查；接下来需要判断的是预测结果是否稳定、不同指标是否一致，以及哪些候选物值得优先检查结构。**

先强调一个重要区别：`ipTM`、`pTM` 和 `confidence_score` 衡量的是模型对预测结构及相互关系的信心，**不能直接证明候选物真的会与 GLP-1R 结合，更不能代替实验亲和力数据**。下面的排序只能作为计算筛选的第一轮结果。

## 1. 第一轮结果：哪些候选物值得优先看？

我用每个候选物 3 次采样的**中位数**进行排序，减少单个预测样本对排名的影响。

| 候选物 | ipTM 中位数 | complex_ipLDDT 中位数 | complex_ipDE 中位数 | 初步判断 |
|---|---:|---:|---:|---|
| `candidate_0096` | 0.953 | 0.726 | 0.773 | 界面指标较好，优先检查 |
| `candidate_0082` | 0.951 | 0.765 | 0.735 | 多项指标均较好，优先检查 |
| `candidate_0129` | 0.948 | 0.707 | 0.967 | ipTM 较高，可进一步检查 |
| `candidate_0046` | 0.946 | 0.716 | 1.184 | ipTM 较高，可进一步检查 |
| `candidate_0044` | 0.945 | 0.737 | 0.972 | 多项指标较好，优先检查 |
| `candidate_0200` | 0.944 | 0.748 | 0.841 | 多项指标较好，优先检查 |
| `candidate_0170` | 0.943 | 0.761 | 0.934 | 界面局部置信度较高，优先检查 |

<text color="secondary" size="sm">注：ipTM、complex_ipLDDT 通常越高越好；complex_ipDE 通常越低越好。这里仅比较本批次结果，不设未经验证的通用合格阈值。</text>

这张表有两个值得注意的地方：

- **`candidate_0082` 是较均衡的候选物。** 它的 ipTM、complex_ipLDDT 和 complex_ipDE 都处于本批次较好的水平。
- **`candidate_0096` 的 ipTM 最高，但 complex_ipLDDT 不如 `candidate_0082`。** 这说明只看一个综合分数，可能会忽略界面局部结构置信度的差别。

因此，我不建议现在就把 ipTM 排名直接当作最终候选物排名。更合理的做法是先选出一组候选物，再看实际界面。

## 2. 三次采样的一致性：哪些结果需要谨慎？

每个候选物只有 3 个采样，所以现在能做的是**初步稳定性检查**，还不足以证明某个候选物的结果稳定。

几个值得关注的案例：

- **`candidate_0051`：有明显的单次异常。** 三个模型的 ipTM 分别约为 0.942、0.932、0.774；第三个模型的 complex_ipDE 达到 4.069，明显高于另外两个模型。不能只看它的中位数就忽略这次分歧。
- **`candidate_0228`：也有类似现象。** ipTM 分别约为 0.940、0.923、0.817，第三个模型的 complex_ipDE 升至 3.146。
- **`candidate_0175`：三次结果也存在分歧。** ipTM 从 0.940 到 0.825，complex_ipDE 从 1.109 到 3.040。

这并不自动说明它们是错误结构，而是提示：需要检查不同采样的结合姿态是否一致，特别是 binder 是否在不同模型中接触了不同的受体区域。

## 3. 参考序列表现如何？

你提供的序列中包含三个参考对照。按照此前的序列映射，结果如下：

| 参考序列 | ipTM 中位数 | complex_ipDE 中位数 |
|---|---:|---:|
| D13（`candidate_0165`） | 0.929 | 1.208 |
| D44（`candidate_0173`） | 0.929 | 1.063 |
| D41（`candidate_0241`） | 0.890 | 2.451 |

<text color="secondary" size="xs">参考序列映射依据此前提供的项目记录。<MemoryCite /></text>

D13 和 D44 的结构置信度指标在本批次中较高，而 D41 相对较低。**但这还不能说明模型成功区分了真实 binder 与非 binder**：我们需要先明确这三个参考序列的实验结合证据、功能状态和可比性；仅凭名称中的 reference 不能把它们都当作已验证的阳性对照。

另一个统计细节：本批次 `protein_iptm` 与 `iptm` 的中位数完全相同。因此，在目前这份输出中，不应把这两个字段当成两条独立证据重复计分。

## 4. 下一步我建议怎么做

现在不需要立刻再跑一遍全部 27 个候选物。建议分两步推进。

<box border radius="lg" padding={3} gap={3}>
  <row align="start" gap={3}>
    <box background="surface-secondary" radius="md" padding={2}>
      <icon name="scan-search" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **第一步：检查优先候选物的实际界面**

      优先看 `candidate_0082`、`candidate_0096`、`candidate_0044`、`candidate_0200` 和 `candidate_0170`。对每个候选物比较三个模型的结合姿态、受体接触残基、界面接触数量、空间冲突，以及是否落在合理的 GLP-1R 结合区域。
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <box backgro      **第二步：与 ColabFold 结果交叉比较**

      对相同候选物对照两种方法的预测姿态与界面质量。如果两种方法得到相似的结合模式，这会增加结构假设的可信度，但仍然不是实验结合证据。如果两种方法分歧很大，则应优先检查该候选物，而不是简单取两者的平均分。
    </box>
  </row>
</box>

**现在最有价值的下一份数据是结构文件，而不是更多综合分数。** 请从 Boltz 输出目录中提供优先候选物的 3 个 CIF 结构文件；如果方便，先提供 `candidate_0082`、`candidate_0096` 和 `candidate_0044` 的三个采样。这样就可以开始检查它们是否形成一致、合理的界面。

路径通常在：

`LOCAL_PATH

具体文件名可以先在 WSL 里运行：

```bash
find LOCAL_PATH \
  -type f -name '*.cif' \
  | grep -E 'candidate_(0082|0096|0044)/'
```

把命令输出贴过来，我可以据此告诉你应该上传哪些文件，以及下一步如何做结构比较。

---

# you asked

message time: 2026-10-22 19:54:58

AlphaFold2被用于预测设计GLP-1RA序列和GLP-1R的复杂结构。每个复形的最佳秩次结构进一步计算了TM评分、RMSD、pLDDT和界面pAE。设计的复合结构（GLP-1 RA和GLP-1R）与原生复合结构（司美格鲁肽和GLP-1R）之间的TM评分;设计的GLP-1RA结构与Semaglutide天然结构之间的RMSD;为设计的GLP-1RA结构提供pLDDT;GLP-1 RA和GLP-1R复合物链间残基对（界面pAE）的平均pAE。这些参数的临界阈值来自Semaglutide和GLP-1R之间的天然复合结构。
论文里的这些比对，现有数据、工具能实现吗

---

# chatgpt response

可以实现，而且你现在的 Boltz-2 预测结果已经提供了一部分基础。不过，要复现论文中的整套评估，必须把它拆成**复合物整体结构相似度、binder 自身结构相似度、结构置信度、受体—binder 界面不确定性**四类指标。

这里有一个关键区别：论文使用的是 AlphaFold2 预测的复合物，参考物是天然的司美格鲁肽（Semaglutide）—GLP-1R 复合物；你目前使用的是 Boltz-2，并且已有 27 个候选物各 3 次采样。因此，**指标可以复现，但不能直接把论文阈值照搬到 Boltz-2 的输出上**。我们应尽量保持论文的比较定义，同时用相同的参考结构、统一的结构对齐和清楚的链对应关系来计算。

## 2. 论文中的四项指标，现有数据能做到什么程度？

论文方法段确实明确了这四项计算：复合物 TM-score、GLP-1RA 相对司美格鲁肽的 RMSD、设计肽的 pLDDT，以及链间残基对的平均 pAE。<Cite refs={["turn371934search0","turn371934search24"]} />

| 论文指标 | 现有 Boltz-2 数据 | 还需要什么 | 可实现性 |
|---|---|---|---|
| 复合物 TM-score | 有预测的复合物 CIF | 天然复合物参考结构；TM-align 等结构比对工具 | 可以 |
| 设计肽与司美格鲁肽的 RMSD | 有设计肽的预测结构 | 参考肽结构；序列对应和结构对齐 | 可以 |
| 设计肽的 pLDDT | 有 `complex_plddt` 和 `complex_iplddt` 等汇总值 | 设计肽链的逐残基置信度，通常可从 CIF 的 B-factor 列提取并验证 | 可以，但不能直接用复合物平均值替代 |
| 界面平均 pAE | 目前 CSV 有 `complex_ipde` 等汇总指标 | 每个残基对的 PAE 矩阵，或能生成该矩阵的预测输出 | 需要检查输出文件 |

Boltz-2 的 `ptm` 是模型预测的全局 TM 类置信度，`iptm` 是界面相对定位置信度；它们**不等于两个实际结构对齐后计算出来的 TM-score**。同理，`complex_ipde` 是界面预测距离误差指标，不能直接当作论文里的平均界面 pAE。<Cite refs={["turn371934search1","turn371934search5","turn371934search6"]} />

### 需要特别注意：pLDDT 和 pAE 的定义

- **pLDDT：** 论文统计的是设计 GLP-1RA 本身的结构置信度。因此应只统计 binder 链对应的残基，而不是把 395 aa 的受体也算进去。
- **界面 pAE：** 应先明确作者的计算定义，再对 GLP-1RA 与 GLP-1R 之间的跨链残基对求平均。不能把整条复合物的 PAE 全部平均，也不能将 `complex_ipde` 改名为 pAE。

另外，你的 GLP-1RA 只有 31 aa，而 GLP-1R 受体链为 395 aa，二者长度差异很大。计算复合物 TM-score 时，应按论文的比较目的明确是否对齐整个复合物、受体链或特定结构区域。不同对齐策略的结果不能混用。

## 3. 你已经具备的工具和需要补齐的部分

你目前的 WSL 环境中已经有 Boltz-2 和预测输出，不必重新预测 27 个候选物。论文采用的天然参考是 PDB `7KI0`，即司美格鲁肽结合的 GLP-1R 复合物。<Cite refs={["turn838950search0","turn838950search3"]} />

<box gap={2}>
  <row align="start" gap={3}>
    <icon name="check-circle" color="success" size="lg" />
    <box flex="1" gap={1}>
      **现有数据即可计算**

      - 设计肽链的 pLDDT（从预测结构逐残基提取）。
      - 设计肽相对于天然司美格鲁肽的 RMSD。
      - 设计复合物与天然复合物的结构 TM-score。
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <icon name="search" size="lg" />
    <box flex="1" gap={1}>
      **需要先检查输出是否齐全**

      - 界面 pAE 矩阵。
      - 每个预测样本的逐残基置信度。
      - Boltz 输出中的链 ID、残基编号与 7KI0 参考结构的对应关系。
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <icon name="wrench" size="lg" />
    <box flex="1" gap={1}>
      **可补充的免费工具**

      - **TM-align**：结构对齐和 TM-score。
      - **Biopython**：读取结构、选择链、处理残基对应关系。
      - **MDAnalysis 或 NumPy**：计算 RMSD 和处理 PAE 矩阵。
      - **PyMOL**：可视化、检查链和结合姿态。
    </box>
  </row>
</box>

## 4. 如何复现论文的天然复合物阈值？

这是整套流程里最值得认真处理的部分。

论文称阈值来自天然司美格鲁肽—GLP-1R 复合物，但仅凭方法段目前还不能确定每项阈值的具体数 对你已有的 81 个 Boltz-2 模型，按论文定义统一计算四项指标。
3. 对天然参考复合物采用同样的结构处理与计算定义，记录天然参考值。
4. 如果希望复现论文中的**筛选阈值**，需要从论文补充材料确认作者具体的阈值规则；不能直接将天然结构的某一个测量值擅自当作四项指标共同的阈值。
5. 对 27 个候选物的三次采样同时报告结果分布，而不仅仅保留最高分的一个模型。

还要注意，7KI0 是包含 G 蛋白等组分的实验复合物；与预测模型比较前，需要明确只保留哪些链，避免把 G 蛋白等额外组分引入 TM-score 比较。<Cite refs={["turn838950search3","turn838950search8"]} />

## 5. 我建议现在先做一个小检查

先不安装新工具，也不重跑预测。请在 WSL 中运行下面的命令，检查 Boltz 输出目录里有没有 PAE 相关文件：

```bash
find LOCAL_PATH \
  -type f $ -iname '*pae*' -o -iname '*confidence*.json' -o -iname '*.cif' $ \
  | head -60
```

把输出贴给我。我会据此判断现有文件能否直接完成界面 pAE 计算，以及如何从 CIF 中准确提取 31 aa 设计肽的 pLDDT。

**结论：四项指标都可以在现有预测基础上实现；目前最不确定的不是计算能力，而是 PAE 矩阵是否保存，以及论文阈值的具体定义。** 这两点确认后，就能建立一个针对 27 个候选物的、可重复运行的结构评价脚本。

---

# you asked

message time: 2026-10-22 20:04:11

先等等，semaglutide和GLP1R的boltz是不是没跑，现在先补一个吧

---

# chatgpt response

对，按我们前面跑批次时的输入，27 个复合物是 **GLP-1R + 24 个设计候选物 + D13、D44、D41 三个参考序列**，没有单独的 Semaglutide–GLP-1R 参考预测。因此，补跑一个是合理的。

我们单独建一个 reference 任务，**不动已有 27 个候选物的结果**，并沿用之前的 Boltz-2 参数和 GLP-1R 自定义 MSA。

有一点要提前说明：Semaglutide 含有非天然氨基酸 Aib 和脂化修饰。若直接用普通氨基酸序列跑 Boltz-2，得到的是近似参考模型，并非完整化学修饰的 Semaglutide。我们可以先补跑这个序列级参考，同时保留实验结构 `7KI0` 作为论文指标计算的天然结构基准。

## 现在按下面步骤补跑

打开 WSL Ubuntu 终端，整段复制执行。脚本会从你现有的 A3M 中提取 GLP-1R 序列，生成一个独立的 YAML 输入。

### 第一步：生成参考输入



### 第二步：运行 Boltz-2

如果第一步没有报错，继续执行：



这里的参数与前面 27 个候选物保持一致：3 次 diffusion sampling、200 个 sampling steps、3 次 recycling，单个样本并行运行。参考任务会输出到独立目录，不会覆盖已有预测。

### 第三步：检查结果



预期应能找到结构 CIF 和置信度 JSON。具体文件数、路径和运行是否成功，以实际输出为准。

**你先执行第一步和第二步，把终端最后的运行状态以及第三步的文件列表贴给我。** 如果成功，我们再验证 3 个样本是否齐全，并把这个参考复合物纳入后续四项指标的计算。

另外，跑完后如果你愿意，我也可以帮你设置一个后续提醒，避免忘记完成参考结构分析；现在先把这次预测跑通。

---

# you asked

message time: 2026-10-22 20:10:19

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'LOCAL_PATH'
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

这个报错说明：脚本找不到之前假定的 A3M 文件路径。**不是 Boltz-2 预测失败，而是还没成功生成输入文件。** 先不要重跑预测，也不要删除任何文件。

你现在在 WSL 终端里，直接复制下面这段命令，搜索真实的 MSA 文件位置：



如果没有结果，再搜索整个 D 盘挂载目录：



把终端输出贴给我，我会根据**实际找到的路径**修正脚本，继续补跑 Semaglutide–GLP-1R 参考复合物。

如果两条命令都没有输出，也没关系，我们再检查 MSA 是否放在其他目录，或者从已有项目文件中恢复它。

---

# you asked

message time: 2026-10-22 20:10:59

PRP_ROOT\GLP1R_reproduction\GLP1R_MSA挪到这了

---

# chatgpt response

好，那现在 MSA 的 Windows 路径是：

`PRP_ROOT\GLP1R_reproduction\GLP1R_MSA`

对应的 WSL 路径通常是：

`LOCAL_PATH

先在终端执行下面的命令，确认文件名：



如果看到 `glp1r_395aa_custom.a3m`，直接修正刚才的脚本：



然后重新生成 YAML：



**先不要急着重新运行 Boltz。** 把 `ls` 和 Python 脚本的输出贴给我，确认输入文件成功生成后，再继续预测，避免路径或序列问题导致重复计算。

---

# you asked

message time: 2026-10-22 20:11:57

-rwxrwxrwx 1 ziguimu ziguimu 2.2K Oct 22 13:21 build_glp1r_msa.py
-rwxrwxrwx 1 ziguimu ziguimu 672K Oct 22 13:21 glp1r_395aa_aligned.fasta
-rwxrwxrwx 1 ziguimu ziguimu 191K Oct 22 13:21 glp1r_395aa_custom.a3m
-rwxrwxrwx 1 ziguimu ziguimu 177K Oct 22 13:21 glp1r_395aa_unique_input.fasta
-rwxrwxrwx 1 ziguimu ziguimu 255K Oct 22 10:13 glp1r_homologs_raw.fasta
(boltz) ziguimu@DESKTOP-8RLFC97:~$ sed -i \
  's#LOCAL_PATH' \
  /tmp/prepare_semaglutide_reference.py
(boltz) ziguimu@DESKTOP-8RLFC97:~$ USER_HOME/miniconda3/envs/boltz/bin/python \
  /tmp/prepare_semaglutide_reference.py
GLP-1R 长度：395 aa
Semaglutide 序列长度：31 aa
输入文件：LOCAL_PATH

Semaglutide 序列：
HAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG

请注意：这是普通氨基酸序列近似，不含完整 Aib/脂化化学修饰。
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

很好，路径已经修正，YAML 也成功生成了。现在确认了：

- GLP-1R 输入序列：395 aa。
- Semaglutide 输入序列：31 aa。
- 输入文件已生成：`LOCAL_PATH

但先提醒一个需要修正的细节：我们当前使用的肽序列是普通氨基酸近似，**不能完整表示 Semaglutide 的 Aib 替换和脂化修饰**。因此，这次预测可以作为序列级参考模型，但不能视为完整修饰药物的精确结构复现。

## 下一步：正式运行 3 次预测

直接复制下面整段命令。它会使用与前 27 个候选物相同的主要参数，并将结果放到独立目录。



运行完成后，再执行下面这条检查命令：



把**退出状态和文件列表**发给我，我们就能确认参考预测是否完整成功。之后再处理四项指标的计算，并明确区分 Boltz-2 预测参考与实验结构 `7KI0`。

---

# you asked

message time: 2026-10-22 20:20:13

LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

很好，参考复合物预测已经生成了 **3 个 CIF 结构和对应的 3 个 confidence JSON 文件**，文件编号为 `model_0`、`model_1`、`model_2`。从文件列表看，三个采样的输出文件都存在。

接下来先检查置信度数据和结构文件是否可正常读取，再把这组结果纳入后续的参考比较。注意：文件存在不等于预测结构一定合理；而且这个 Boltz-2 参考模型使用的是未显式编码 Aib 和脂化修饰的普通序列。

## 下一步：验证 3 个模型并查看指标

请在 WSL 终端执行下面这段命令。它会读取三个 JSON，列出可用的置信度指标，并检查 CIF 文件是否非空。



把输出贴给我，我会根据实际字段确认：

1. 哪些 Boltz-2 置信度指标可以直接提取；
2. 能否从结构文件提取 Semaglutide 链的逐残基 pLDDT；
3. 是否需要额外导出 PAE 矩阵，才能计算论文定义的跨链平均 pAE。

完成这一步后，就可以着手搭建统一计算 27 个候选物和参考模型指标的脚本。如果你希望，我也可以之后提醒你继续完成结构比对和指标汇总。

---

# you asked

message time: 2026-10-22 20:20:42

模型输出检查
============================================================

Model 0
CIF 存在且非空：True
JSON 存在且非空：True
JSON 顶层字段： ['confidence_score', 'ptm', 'iptm', 'ligand_iptm', 'protein_iptm', 'complex_plddt', 'complex_iplddt', 'complex_pde', 'complex_ipde', 'chains_ptm', 'pair_chains_iptm']
  confidence_score: 0.849350094795227
  ptm: 0.8849537968635559
  iptm: 0.9397348761558533
  ligand_iptm: 0.0
  protein_iptm: 0.9397348761558533
  complex_plddt: 0.8267538547515869
  complex_iplddt: 0.7891954183578491
  complex_pde: 0.5787855386734009
  complex_ipde: 1.3426334857940674
  chains_ptm: dict，字段 ['0', '1']
  pair_chains_iptm: dict，字段 ['0', '1']

Model 1
CIF 存在且非空：True
JSON 存在且非空：True
JSON 顶层字段： ['confidence_score', 'ptm', 'iptm', 'ligand_iptm', 'protein_iptm', 'complex_plddt', 'complex_iplddt', 'complex_pde', 'complex_ipde', 'chains_ptm', 'pair_chains_iptm']
  confidence_score: 0.8450039029121399
  ptm: 0.9220272302627563
  iptm: 0.9602588415145874
  ligand_iptm: 0.0
  protein_iptm: 0.9602588415145874
  complex_plddt: 0.8161901235580444
  complex_iplddt: 0.76842200756073
  complex_pde: 0.42479565739631653
  complex_ipde: 0.7761623859405518
  chains_ptm: dict，字段 ['0', '1']
  pair_chains_iptm: dict，字段 ['0', '1']

Model 2
CIF 存在且非空：True
JSON 存在且非空：True
JSON 顶层字段： ['confidence_score', 'ptm', 'iptm', 'ligand_iptm', 'protein_iptm', 'complex_plddt', 'complex_iplddt', 'complex_pde', 'complex_ipde', 'chains_ptm', 'pair_chains_iptm']
  confidence_score: 0.812520444393158
  ptm: 0.9172718524932861
  iptm: 0.8924143314361572
  ligand_iptm: 0.0
  protein_iptm: 0.8924143314361572
  complex_plddt: 0.7925469279289246
  complex_iplddt: 0.7181130051612854
  complex_pde: 0.4521203637123108
  complex_ipde: 1.726453185081482
  chains_ptm: dict，字段 ['0', '1']
  pair_chains_iptm: dict，字段 ['0', '1']
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

这组结果可以继续往下用了：3 个模型的 CIF 和 JSON 都能正常读取，置信度字段齐全。

## 1. Semaglutide–GLP-1R 参考预测的初步结果

| 指标 | Model 0 | Model 1 | Model 2 |
|---|---:|---:|---:|
| `confidence_score` | 0.8494 | 0.8450 | 0.8125 |
| `ptm` | 0.8850 | 0.9220 | 0.9173 |
| `iptm` | 0.9397 | 0.9603 | 0.8924 |
| `complex_plddt` | 0.8268 | 0.8162 | 0.7925 |
| `complex_iplddt` | 0.7892 | 0.7684 | 0.7181 |
| `complex_ipde` | 1.3426 | 0.7762 | 1.7265 |

从这三个样本看，Model 1 的 ipTM 最高，Model 2 的界面局部置信度较低、界面误差指标较高。三个模型的结果有一定差异，所以后续不应该只保留最高 ipTM 的一个模型。

不过，这里有一个**重要的指标解释问题**：`complex_plddt` 是复合物级别的汇总指标，不是单独 Semaglutide 链的 pLDDT；`complex_ipde` 也不是论文要求的跨链平均 pAE。我们仍需要从结构文件中提取肽链的逐残基置信度，并确认能否取得 Boltz 的 PAE 矩阵。

## 2. 下一步：确认 pLDDT 和 PAE 是否能直接提取

请在 WSL 中运行下面两组检查。

**A. 查看参考预测的全部输出文件**

```bash
find /mnt/d**

```bash
CIF=LOCAL_PATH

1. 确认链 A 是 GLP-1R、链 B 是 Semaglutide，并核实实际残基数和编号。
2. 从 CIF 提取肽链逐残基 pLDDT，并计算肽链平均值。
3. 检查有没有保存 PAE 矩阵；若没有，再确认当前 Boltz 输出能否通过已有预测结果重新导出，而不是盲目重跑。
4. 最后才计算与实验结构 `7KI0` 的 RMSD 和 TM-score。

这样能保证你后续的 27 个候选物与天然参考使用同一套指标定义，避免把不同含义的置信度分数混在一起。

---

# you asked

message time: 2026-10-22 20:21:24

(boltz) ziguimu@DESKTOP-8RLFC97:~$ find LOCAL_PATH \
  -type f -printf '%f\t%s bytes\n' | sort
confidence_semaglutide_glp1r_reference_model_0.json     656 bytes
confidence_semaglutide_glp1r_reference_model_1.json     656 bytes
confidence_semaglutide_glp1r_reference_model_2.json     655 bytes
hparams.yaml    4148 bytes
manifest.json   682 bytes
pae_semaglutide_glp1r_reference_model_0.npz     642890 bytes
pae_semaglutide_glp1r_reference_model_1.npz     643181 bytes
pae_semaglutide_glp1r_reference_model_2.npz     643024 bytes
pde_semaglutide_glp1r_reference_model_0.npz     636816 bytes
pde_semaglutide_glp1r_reference_model_1.npz     630213 bytes
pde_semaglutide_glp1r_reference_model_2.npz     634009 bytes
plddt_semaglutide_glp1r_reference_model_0.npz   1698 bytes
plddt_semaglutide_glp1r_reference_model_1.npz   1701 bytes
plddt_semaglutide_glp1r_reference_model_2.npz   1714 bytes
semaglutide_glp1r_reference.json        667 bytes
semaglutide_glp1r_reference.npz 1555 bytes
semaglutide_glp1r_reference.npz 9009 bytes
semaglutide_glp1r_reference.pkl 5 bytes
semaglutide_glp1r_reference_0.npz       18623 bytes
semaglutide_glp1r_reference_model_0.cif 308640 bytes
semaglutide_glp1r_reference_model_1.cif 308828 bytes
semaglutide_glp1r_reference_model_2.cif 308264 bytes
(boltz) ziguimu@DESKTOP-8RLFC97:~$ CIF=LOCAL_PATH

head -45 "$CIF"
data_model
_entry.id model
_struct.entry_id model
_struct.pdbx_model_details .
_struct.pdbx_structure_determination_methodology computational
_struct.title .
_audit_conform.dict_location https://raw.githubusercontent.com/ihmwg/ModelCIF/d18ba38/base/mmcif_ma-core.dic
_audit_conform.dict_name mmcif_ma.dic
_audit_conform.dict_version 1.4.6
#
loop_
_chem_comp.id
_chem_comp.type
_chem_comp.name
_chem_comp.formula
_chem_comp.formula_weight
_chem_comp.ma_provenance
ALA 'L-peptide linking' . . . 'CCD Core'
ARG 'L-peptide linking' . . . 'CCD Core'
ASN 'L-peptide linking' . . . 'CCD Core'
ASP 'L-peptide linking' . . . 'CCD Core'
CYS 'L-peptide linking' . . . 'CCD Core'
GLN 'L-peptide linking' . . . 'CCD Core'
GLU 'L-peptide linking' . . . 'CCD Core'
GLY 'L-peptide linking' . . . 'CCD Core'
HIS 'L-peptide linking' . . . 'CCD Core'
ILE 'L-peptide linking' . . . 'CCD Core'
LEU 'L-peptide linking' . . . 'CCD Core'
LYS 'L-peptide linking' . . . 'CCD Core'
MET 'L-peptide linking' . . . 'CCD Core'
PHE 'L-peptide linking' . . . 'CCD Core'
PRO 'L-peptide linking' . . . 'CCD Core'
SER 'L-peptide linking' . . . 'CCD Core'
THR 'L-peptide linking' . . . 'CCD Core'
TRP 'L-peptide linking' . . . 'CCD Core'
TYR 'L-peptide linking' . . . 'CCD Core'
VAL 'L-peptide linking' . . . 'CCD Core'
#
#
loop_
_entity.id
_entity.type
_entity.src_method
_entity.pdbx_description
_entity.formula_weight

---

# chatgpt response

这次检查很有价值：**Boltz-2 已经保存了我们需要的 PAE 和 pLDDT 原始数据，不需要为这两项指标重新跑预测。**

你贴出的文件列表确认每个模型都有：

- `pae_*_model_*.npz`：预测对齐误差（PAE）矩阵。
- `plddt_*_model_*.npz`：逐残基 pLDDT 数据。
- `pde_*_model_*.npz`：预测距离误差（PDE）数据。
- `*_model_*.cif`：三维结构。

所以，我们可以直接从现有输出计算设计肽链的平均 pLDDT，以及 GLP-1R 与肽链之间的平均跨链 PAE。接下来最重要的是**核实 NPZ 中的数组结构、残基顺序和链映射**，再开始批量计算，避免把受体残基也计入肽链指标。

## 下一步：检查 PAE / pLDDT 数组和 CIF 链信息

请在 WSL 里运行下面的完整脚本。它只读取文件，不修改或重新生成任何预测结果。



把输出贴给我，尤其是 `pae`、`plddt` 的 `shape`、`key`，以及 CIF 的链长度。

拿到这些信息后，我们就可以编写一个统一脚本，对 27 个候选物的 81 个模型和这 3 个参考模型计算：

1. **肽链平均 pLDDT**：只统计设计肽或参考肽。
2. **跨链平均 PAE**：只统计受体—肽链残基对。
3. **三次采样的中位数、范围和波动**：保留采样差异，不只挑最高分。
4. **与 7KI0 实验结构的 RMSD / TM-score**：另行进行结构对齐，和模型内部置信度指标分开报告。

这样得到的指标才适合用于后续的候选物排序与论文方法复现。

---

# you asked

message time: 2026-10-22 20:22:22

======================== MODEL 0 ========================

[pae] pae_semaglutide_glp1r_reference_model_0.npz
  key='pae', shape=(426, 426), dtype=float32

[plddt] plddt_semaglutide_glp1r_reference_model_0.npz
  key='plddt', shape=(426,), dtype=float32

[pde] pde_semaglutide_glp1r_reference_model_0.npz
  key='pde', shape=(426, 426), dtype=float32
CIF chain 'A': 395 standard amino-acid residues; first=['THR', 'VAL', 'SER', 'LEU', 'TRP']; last=['ARG', 'TRP', 'ARG', 'LEU', 'GLU']
CIF chain 'B': 31 standard amino-acid residues; first=['HIS', 'ALA', 'GLU', 'GLY', 'THR']; last=['VAL', 'ARG', 'GLY', 'ARG', 'GLY']

Confidence JSON:
{
  "confidence_score": 0.849350094795227,
  "ptm": 0.8849537968635559,
  "iptm": 0.9397348761558533,
  "ligand_iptm": 0.0,
  "protein_iptm": 0.9397348761558533,
  "complex_plddt": 0.8267538547515869,
  "complex_iplddt": 0.7891954183578491,
  "complex_pde": 0.5787855386734009,
  "complex_ipde": 1.3426334857940674,
  "chains_ptm": {
    "0": 0.8816429376602173,
    "1": 0.9677049517631531
  },
  "pair_chains_iptm": {
    "0": {
      "0": 0.8816429376602173,
      "1": 0.8332440853118896
    },
    "1": {
      "0": 0.9397348761558533,
      "1": 0.9677049517631531
    }
  }
}

======================== MODEL 1 ========================

[pae] pae_semaglutide_glp1r_reference_model_1.npz
  key='pae', shape=(426, 426), dtype=float32

[plddt] plddt_semaglutide_glp1r_reference_model_1.npz
  key='plddt', shape=(426,), dtype=float32

[pde] pde_semaglutide_glp1r_reference_model_1.npz
  key='pde', shape=(426, 426), dtype=float32
CIF chain 'A': 395 standard amino-acid residues; first=['THR', 'VAL', 'SER', 'LEU', 'TRP']; last=['ARG', 'TRP', 'ARG', 'LEU', 'GLU']
CIF chain 'B': 31 standard amino-acid residues; first=['HIS', 'ALA', 'GLU', 'GLY', 'THR']; last=['VAL', 'ARG', 'GLY', 'ARG', 'GLY']

Confidence JSON:
{
  "confidence_score": 0.8450039029121399,
  "ptm": 0.9220272302627563,
  "iptm": 0.9602588415145874,
  "ligand_iptm": 0.0,
  "protein_iptm": 0.9602588415145874,
  "complex_plddt": 0.8161901235580444,
  "complex_iplddt": 0.76842200756073,
  "complex_pde": 0.42479565739631653,
  "complex_ipde": 0.7761623859405518,
  "chains_ptm": {
    "0": 0.9201355576515198,
    "1": 0.9762029051780701
  },
  "pair_chains_iptm": {
    "0": {
      "0": 0.9201355576515198,
      "1": 0.8890680074691772
    },
    "1": {
      "0": 0.9602588415145874,
      "1": 0.9762029051780701
    }
  }
}

======================== MODEL 2 ========================

[pae] pae_semaglutide_glp1r_reference_model_2.npz
  key='pae', shape=(426, 426), dtype=float32

[plddt] plddt_semaglutide_glp1r_reference_model_2.npz
  key='plddt', shape=(426,), dtype=float32

[pde] pde_semaglutide_glp1r_reference_model_2.npz
  key='pde', shape=(426, 426), dtype=float32
CIF chain 'A': 395 standard amino-acid residues; first=['THR', 'VAL', 'SER', 'LEU', 'TRP']; last=['ARG', 'TRP', 'ARG', 'LEU', 'GLU']
CIF chain 'B': 31 standard amino-acid residues; first=['HIS', 'ALA', 'GLU', 'GLY', 'THR']; last=['VAL', 'ARG', 'GLY', 'ARG', 'GLY']

Confidence JSON:
{
  "confidence_score": 0.812520444393158,
  "ptm": 0.9172718524932861,
  "iptm": 0.8924143314361572,
  "ligand_iptm": 0.0,
  "protein_iptm": 0.8924143314361572,
  "complex_plddt": 0.7925469279289246,
  "complex_iplddt": 0.7181130051612854,
  "complex_pde": 0.4521203637123108,
  "complex_ipde": 1.726453185081482,
  "chains_ptm": {
    "0": 0.9253096580505371,
    "1": 0.9176965355873108
  },
  "pair_chains_iptm": {
    "0": {
      "0": 0.9253096580505371,
      "1": 0.8064205646514893
    },
    "1": {
      "0": 0.8924143314361572,
      "1": 0.9176965355873108
    }
  }
}

检查结束：以上只展示数组结构和链信息，不计算或假定任何阈值。
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

很好，这次检查已经把关键结构确认了：**Boltz-2 的 PAE 和 pLDDT 数组都能用于提取我们需要的两项指标**，而且链与数组长度可以对应起来。

## 1. 已确认的数据结构

| 项目 | 已确认结果 | 含义 |
|---|---|---|
| 受体链 A | 395 aa | GLP-1R |
| 多肽链 B | 31 aa | Semaglutide 的标准氨基酸序列近似体 |
| PAE 矩阵 | $426\times426$ | 覆盖两条链的残基对 |
| pLDDT 数组 | 426 个值 | 覆盖两条链的残基 |
| PDE 矩阵 | $426\times426$ | 另一种残基对误差指标；本次论文指标暂时不需要 |

因为 $395+31=426$，所以在确认 Boltz 输出数组的残基顺序与 CIF 链顺序一致后，可以按以下索引计算：

- **多肽 pLDDT**：取最后 31 个值，即 `plddt[395:426]`，计算平均值。
- **链间平均 PAE**：取受体与多肽之间的矩阵块，即 `pae[0:395, 395:426]`，计算平均值。

这里的链间平均 PAE 与 Boltz JSON 里的 `complex_ipde` **不是同一个指标**，不能互相替代。

还有一个需要保留的化学限制：当前输入使用的是 31 aa 的标准序列近似体，不能完整表达 Semaglutide 的非天然氨基酸及脂肪链修饰。因此，这一轮适合作为 **Boltz-2 的参考预测基线**，但不能称为对真实修饰后 Semaglutide 的完整复现。

## 2. 下一步：正式计算 3 个模型的参考指标

请直接在当前终端执行下面的完整命令。它会读取三个模型的 NPZ 文件，计算多肽链平均 pLDDT，以及两个方向的链间平均 PAE，并输出汇总 CSV。

```bash
cat > /tm
- **多肽平均 pLDDT**：对应论文所说的 designed GLP-1RA 的 pLDDT，但当前是 Semaglutide 参考序列近似体的预测值。
- **双方向平均 PAE**：是一个明确可复现的链间平均 PAE 定义。论文若指定只取某个方向、特定残基范围或特定原子/残基映射，需要按其方法调整。
- **三个模型之间的波动**：可用于观察参考预测的稳定性，但不能仅凭三个模型确定合格阈值。

下一步我们再处理实验结构 **PDB 7KI0**：正确识别其中的 GLP-1R 与 Semaglutide 链，计算结构比对后的 TM-score 和多肽 RMSD。只有先统一链选择、残基范围和比对方式，才能将这些参考值与 27 个候选物公平比较。

把上面命令的输出贴过来，我会帮你核对计算结果并整理成可以加入项目数据表的格式。

---

# you asked

message time: 2026-10-22 20:23:02

FileNotFoundError: [Errno 2] No such file or directory: 'LOCAL_PATH'
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

这个报错是我上一条脚本里的**文件路径假设有误**，不是你的 NPZ 文件损坏。你之前的检查已经成功读取了这些文件，因此我们先找到它们的真实位置，再修正脚本，不需要重新运行 Boltz-2。

请在终端执行下面这条命令：



它会输出这两个文件的实际完整路径。

**把输出贴给我即可。** 我会据此修正脚本中的目录设置，并保留之前确定的计算方法：

- 多肽链 B 的平均 pLDDT：31 个残基。
- 受体链 A 与多肽链 B 之间的平均 PAE。
- 三个模型的结果汇总为 CSV。

暂时不要重新预测，也不需要删除或移动任何文件。

---

# you asked

message time: 2026-10-22 20:23:46

-o -name 'plddt_semaglutide_glp1r_reference_model_0.npz' \)
LOCAL_PATH
LOCAL_PATH
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

找到原因了：NPZ 文件实际位于更深一层的 `predictions/semaglutide_glp1r_reference/` 目录。我们只需要修正路径，不必重新预测。

请直接运行下面这份**修正后的完整脚本**：



成功后会打印三个模型的多肽平均 pLDDT、链间平均 PAE、ipTM 等指标，并生成 `semaglutide_reference_metrics.csv`。

注意：链间 PAE 的计算暂时按照数组顺序与 CIF 链顺序一致来处理。等结果出来后，我们再核对指标并与论文的定义对齐；不要直接把这些参考预测值当成实验阈值。

---

# you asked

message time: 2026-10-22 20:24:24

CSV 已保存：LOCAL_PATH
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

很好，说明三个模型的指标已经成功计算并写入 CSV，**不需要重新运行 Boltz-2**。

现在先检查实际数值，再决定如何将 Semaglutide 参考预测与 27 个候选物进行比较。注意我们目前得到的是标准氨基酸序列近似体的预测指标，而不是实验结构 7KI0 的结构比对结果。

请在终端执行：



如果输出排版不整齐，也可以用下面的命令：



把结果贴过来，我会核对三个模型的多肽平均 pLDDT 和链间平均 PAE 的波动，并说明哪些数值适合记录到项目数据表中。

另外，如果你愿意，我也可以帮你安排后续提醒，继续完成 **7KI0 实验结构解析 → 候选物与参考结构比对 → 指标汇总与阈值校准**，避免项目中断后忘记下一步。

---

# you asked

message time: 2026-10-22 20:24:55

(boltz) ziguimu@DESKTOP-8RLFC97:~$ cat LOCAL_PATH
﻿model,iptm,ptm,confidence_score,peptide_mean_pLDDT,peptide_median_pLDDT,peptide_pLDDT_std,mean_PAE_receptor_to_peptide,mean_PAE_peptide_to_receptor,mean_PAE_bidirectional,cross_chain_pairs_per_direction
0,0.9397348761558533,0.8849537968635559,0.849350094795227,0.7520585963802953,0.7621930837631226,0.09126305633564187,6.2216716580996465,5.452598270877326,5.837134964488486,12245
1,0.9602588415145874,0.9220272302627563,0.8450039029121399,0.7298820749405892,0.7407876253128052,0.07005418700315687,4.8231776153325745,4.336728028040995,4.579952821686785,12245
2,0.8924143314361572,0.9172718524932861,0.812520444393158,0.5316239258935375,0.5935381650924683,0.15566363789095228,6.630405870385441,10.856583304052792,8.743494587219116,12245
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

这组结果很有价值。现在我们已经有了 Semaglutide–GLP-1R 参考预测的三模型指标，可以先建立一份参考基线。不过，**暂时不要直接用这三个模型的最大值或平均值作为候选物的合格阈值**，因为还没有和论文中的实验参考结构及阈值定义对齐。

## 1. 三个参考模型的结果

| 指标 | Model 0 | Model 1 | Model 2 |
|---|---:|---:|---:|
| ipTM | 0.940 | **0.960** | 0.892 |
| pTM | 0.885 | **0.922** | 0.917 |
| 多肽平均 pLDDT | **0.752** | 0.730 | 0.532 |
| 多肽 pLDDT 标准差 | 0.091 | **0.070** | 0.156 |
| 双方向平均链间 PAE（Å） | 5.837 | **4.580** | 8.743 |

<text color="secondary" size="sm">注：pLDDT 和 PAE 按当前 Boltz 输出数组及链索引计算；数值四舍五入展示。PAE 越低通常意味着模型对相对位置的预测越有信心，但它不是实验亲和力指标。</text>

## 2. 这组结果说明什么？

<box gap={3}>
  <row align=start gap={3}>
    <box background="surface-secondary" radius="lg" size="44px" align=center justify=center>
      <icon name="check-circle" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **Model 0 和 Model 1：整体表现较一致**

      两者的 ipTM 分别约为 0.940 和 0.960，双方向平均链间 PAE 约为 5.84 Å 和 4.58 Å。模型对复合物界面的相对定位给出了较高信心。
    </box>
  </row>
  <divider color="subtle" />
  <row align=start gap={3}>
    <box background="surface-secondary" radius="lg" size="44px" align=center justify=center>
      <icon name="alert-triangle" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **Model 2：多肽局部置信度与界面指标均有所下降**

      多肽平均 pLDDT 降至约 0.532，双方向平均链间 PAE 升至约 8.74 Å。这提示第三个模型的预测与前两个模型存在明显差异，值得进一步检查多肽构象和结合姿势。
    </box>
  </row>
</box>

需要注意：这些结果并不能证明真实 Semaglutide 与 GLP-1R 的结合能力，也不能仅凭模型间差异判断 Model 2 的结构一定错误。它们是预测置信度和模型一致性方面的证据。

## 3. 对 AI-BinderDesign 项目的意义

这正好可以支持你希望建立的评估思路：

> **结构置信度分数不是判决；候选筛选标准需要通过可靠的参考体系校准。**

目前我们可以将这些数据记录为 `Boltz-2 Semaglutide sequence-approximation reference`，但应明确标注它是标准序列近似体的预测结果，不是实验结构基线。

接下来最重要的是处理实验结构 **7KI0**，而不是马上对候选物设阈值：

1. 识别 7KI0 中的 GLP-1R 与 Semaglutide 对应链，并确认残基范围。
2. 将实验参考结构与 Boltz 预测进行结构比对，评估预测姿势与实验结构的差异。
3. 按论文指定的定义，计算候选物与参考结构的复合物 TM-score、多肽 RMSD、多肽 pLDDT 和链间平均 PAE。
4. 最后再依据论文方法或明确的校准数据，制定候选物筛选规则。

**下一步建议：先完成 7KI0 的链识别和结构比对。** 这样得到的实验参考才是我们判断当前预测质量、以及后续校准候选物指标的关键依据。

---

# you asked

message time: 2026-10-22 20:26:58

TM评分、RMSD这俩好算吗，需要用到什么工具？

---

# chatgpt response

这两个指标都不难算。结合你现在的 GLP-1R 项目，**现有的 Boltz-2 预测结构就能作为输入，不需要重新跑模型**。主要工作是准备好实验参考结构 7KI0，正确识别受体和多肽链，再做结构比对。

## 1. TM-score 和 RMSD 分别是什么？

<box gap={3}>
  <row align=start gap={3}>
    <AsyncImage query="protein structure superposition aligned protein backbones ribbon structure comparison" aspectRatio="4:3" maxWidth="124px" />
    <box flex="1" gap={1}>
      **TM-score：整体结构相似度**

      通常在 0–1 之间，越高表示整体结构越相似。它对整体折叠相似性较有参考价值，但结果会受到比对对象、残基对应关系和结构长度影响。
    </box>
  </row>
  <divider color="subtle" />
  <row align=start gap={3}>
    <AsyncImage query="protein backbone structural alignment RMSD superposition two molecular structures" aspectRatio="4:3" maxWidth="124px" />
    <box flex="1" gap={1}>
      **RMSD：比对后的坐标偏差**

      单位通常是 Å（埃）。在指定原子集合并完成最优叠合后，RMSD 越低表示这些原子的位置越接近。它对比对范围、原子选择和局部偏差比较敏感。
    </box>
  </row>
</box>

对你的项目，至少要区分两种比较：

- **复合物 TM-score**：候选物–GLP-1R 复合物与 Semaglutide–GLP-1R 参考复合物的整体结构相似度。
- **多肽 RMSD**：候选多肽与参考 Semaglutide 的结构差异。最好先对齐 GLP-1R 受体，再计算多肽骨架 RMSD，这样更直接反映结合姿势的差异。

不能把两种比较混为一谈：复合物整体相似，不一定意味着多肽结合姿势完全一致。

## 2. 需要什么工具？

你当前的 WSL + Boltz-2 环境已经够用。推荐组合如下。

| 工具 | 主要用途 | 是否必须 |
|---|---|---|
| **<Entity value="US-align" category="software" disambig="Protein and nucleic acid structural alignment software" />** | 计算复合物结构的 TM-score、RMSD，支持多链结构比较 | 推荐 |
| **<Entity value="Biopython" category="software" disambig="Python library for biological computation" />** | 读取 CIF、识别链、提取残基、计算指定原子集合的 RMSD | 推荐 |
| **<Entity value="PyMOL" category="software" disambig="Molecular visualization and structural analysis software" />** | 可视化两套结构、检查受体叠合及多肽结合姿势 | 可选，但很有帮助 |

US-align 的官方说明和论文介绍了 TM-score 与 RMSD 的计算方式，并支持蛋白质复合物的结构比对。<Cite refs={["turn259841search1","turn259841search0","turn259841search3"]}/>

## 3. 对你的项目，具体怎么计算？

<box border radius="xl" padding={3} gap={3}>
  <title size="lg">第一步：复合物 TM-score</title>
  <text color="secondary" size="sm">工具：US-align</text>

  将候选物–GLP-1R 预测结构与 7KI0 中的 Semaglutide–GLP-1R 实验结构进行比较。

  需要先提取正确的受体和多肽链，排除不相关链。还要注意：直接把两个完整复合物交给结构比对软件，并不一定会得到你想要的受体与多肽对应关系。
  <divider color="subtle" />
  <title size="lg">第二步：多肽 RMSD</title>
  <text color="secondary" size="sm">工具：Biopython，或 PyMOL 辅助检查</text>

  1. 按残基对应关系对齐实验结构和预测结构中的 GLP-1R。
  2. 固定受体叠合结果。
  3. 选取候选多肽和 Semaglutide 对应的主链原子或 Cα 原子，计算 RMSD。

  这样得到的 RMSD 更直接地反映多肽结合姿势与实验参考的差异。若先对多肽自身做独立最优叠合，得到的是另一种 RMSD，不能不加区分地替代。
</box>

有个关键细节：**TM-score 的归一化长度和 RMSD 的原子选择必须固定下来。** 不同设置算出来的结果可能不同。US-align 也区分了结构自动比对和按既定残基对应关系叠合两种模式。<Cite refs={["turn259841search3","turn259841search4"]}/>

## 4. 我建议你现在这样做

先不安装一堆软件，也不需要重新运行 Boltz-2。

第一阶段只做两件事：

1. 确认本地是否已有 US-align、Biopython 和 PyMOL。
2. 解析 7KI0 的链和残基范围，确定 Semaglutide 与 GLP-1R 的对应关系。

随后再写一个可以批量处理 27 个候选物的脚本，输出每个候选物的复合物 TM-score、多肽 RMSD，并保留比对残基数等质控信息。

**一个重要提醒：** 你引用的论文如果对复合物 TM-score 和多肽 RMSD 有特定定义，应优先复现论文的定义，而不是自行选择一种看起来合理的计算方式。

如果你愿意，下一步我们就从检查本地工具和定位 7KI0 文件开始，直接在你现有的 WSL 环境中完成，不需要重跑预测。

---

# you asked

message time: 2026-10-22 20:28:11

我记得有biopython没有US-align

---

# chatgpt response

那我们先沿用你现有的 Boltz-2 环境，不动已经跑好的预测结果。

**Biopython 负责读取结构、选链和计算指定原子的 RMSD；US-align 负责结构比对并计算 TM-score。** 两者配合就能覆盖我们这一步的大部分需求。

先检查 Biopython 是否可用，以及系统里是否已经存在 US-align。请在 WSL 终端执行：



如果确认没有安装，官方推荐的 Conda 安装方式是 `conda install -c bioconda usalign`。<Cite refs={["turn978977search0","turn978977search1"]}/>

为了不影响你现有的 `boltz` 环境，我更建da usalign
`al USalign
```

如果输出 US-align 的使用说明或参数帮助，就说明安装成功。先把前面三条检查命令的结果发我，我们再决定是否需要安装，避免重复操作。

---

# you asked

message time: 2026-10-22 20:28:40

uname -m
Biopython: 1.84
x86_64
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

检查结果已经确认：

- Biopython：`1.84`，已可用。
- 系统架构：`x86_64`，适合选择 Linux x86-64 版本的 US-align。
- `command -v USalign` 和 `command -v US-align` 没有打印路径，说明当前环境里大概率还没有可直接调用的 US-align。

为了避免改动现有的 `boltz` 环境，建议单独创建结构评估环境。这样后续计算 TM-score、RMSD 时，不会影响已经能正常运行的 Boltz-2。

根据 Bioconda 的安装说明，Linux x86-64 支持通过 Conda 安装 US-align。<Cite refs={["turn722077search0","turn722077search
  usalign
```

安装过程如果询问 `Proceed ([y]/n)?`，输入 `y` 并回车al USalign
```

如果能打印 US-align 的用法说明，就说明安装成功。把最后的输出发给我，我们接着检查 7KI0 的结构文件与链信息。

---

# you asked

message time: 2026-10-22 20:32:16

不用给usalign单独创建一个环境吗

---

# chatgpt response

对，**我更推荐给 US-align 单独创建一个环境**，尤其是你现在已经有正常运行的 `boltz` 环境，没必要为了一个结构比对工具去改动它。

不过有两种方案：

- **方案 A：独立环境（推荐）**：创建 `structure_eval`，安装 US-align。依赖隔离更清晰。
- **方案 B：直接装进 `boltz` 环境**：操作更简单，但可能引入依赖冲突；没有必要冒这个风险。

你前面执行的命令其实已经是独立环境方案：



安装完成后，用下面的命令验证，不需要切换或退出当前的 `boltz` 环境：



之后我们可以继续在 `boltz` 环境里使用 Biopython 处理结构，在 `structure_eval` 环境里调用 US-align 计算 TM-score。两个环境各司其职即可。

---

# you asked

message time: 2026-10-22 20:32:56

********************************************************************
 * US-align (Version 20241108)                                      *
 * Universal Structure Alignment of Proteins and Nucleic Acids      *
 * Reference: C Zhang, M Shine, AM Pyle, Y Zhang. (2022) Nat Methods*
 *            C Zhang, AM Pyle (2022) iScience.                     *
 * Please email comments and suggestions to <EMAIL>    *
 ********************************************************************

Usage: USalign PDB1.pdb PDB2.pdb [Options]

Options:
    -mol  Type of molecule(s) to align.
          auto: (default) align both protein and nucleic acids.
          prot: only align proteins in a structure.
          RNA : only align RNA and DNA in a structure.

     -mm  Multimeric alignment option:
          0: (default) alignment of two monomeric structures
          1: alignment of two multi-chain oligomeric structures
          2: alignment of individual chains to an oligomeric structure
             $ USalign -dir1 monomers/ list oligomer.pdb -ter 0 -mm 2
          3: alignment of circularly permuted structure
          4: MSTA, i.e., alignment of multiple monomeric chains into a
             consensus alignment
             $ USalign -dir chains/ list -suffix .pdb -mm 4
          5: fully non-sequential (fNS) alignment
          6: semi-non-sequential (sNS) alignment
          To use -mm 1 or -mm 2, '-ter' option must be 0 or 1.

    -ter  Number of chains to align.
          0: align all chains from all models (recommended for aligning
             biological assemblies, i.e. biounits)
          1: align all chains of the first model (recommended for aligning
             asymmetric units, default for -mm 1,2 and -TMscore 2,6,7)
          2: (default for other cases) only align the first chain
          3: only align the first chain, or the first segment of the
             first chain as marked by the 'TER' string in PDB file

 -TMscore Whether to perform TM-score superposition without structure-based
          alignment. The same as -byresi.
          0: (default) sequence independent structure alignment
          1: superpose two structures by assuming that a pair of residues
             with the same residue index are equivalent between the two
             structures
          2: superpose two complex structures, assuming that a pair of
             residues with the same residue index and the same chain ID
             are equivalent between the two structures
          5: sequence dependent alignment: perform glocal sequence
             alignment followed by TM-score superposition.
             -byresi 5 is the same as -seq
          6: superpose two complex structures by first deriving optimal
             chain mapping, followed by TM-score superposition for residues
             with the same residue ID
          7: sequence dependent alignment of two complex structures:
             perform global sequence alignment of each chain pair, derive
             optimal chain mapping, and then superpose two complex
             structures by TM-score

      -I  Use the final alignment specified by FASTA file 'align.txt'

      -i  Use alignment specified by 'align.txt' as an initial alignment

      -m  Output rotation matrix for superposition, e.g., '-m matrix.txt'
          prints the matrix to 'matrix.txt'; '-m -' prints to stdout.

      -d  TM-score scaled by an assigned d0, e.g., '-d 3.5' reports MaxSub
          score, where d0 is 3.5 Angstrom. -d does not change final alignment.

      -u  TM-score normalized by an assigned length. It should be >= length
          of protein to avoid TM-score >1. -u does not change final alignment.

      -o  Output superposed structure1 to sup.* for PyMOL viewing.
          $ USalign structure1.pdb structure2.pdb -o sup
          $ pymol -d @sup.pml                # C-alpha trace aligned region
          $ pymol -d @sup_all.pml            # C-alpha trace whole chain
          $ pymol -d @sup_atm.pml            # full-atom aligned region
          $ pymol -d @sup_all_atm.pml        # full-atom whole chain
          $ pymol -d @sup_all_atm_lig.pml    # full-atom with all molecules

 -rasmol  Output superposed structure1 to sup.* for RasMol viewing.
          $ USalign structure1.pdb structure2.pdb -rasmol sup
          $ rasmol -script sup               # C-alpha trace aligned region
          $ rasmol -script sup_all           # C-alpha trace whole chain
          $ rasmol -script sup_atm           # full-atom aligned region
          $ rasmol -script sup_all_atm       # full-atom whole chain
          $ rasmol -script sup_all_atm_lig   # full-atom with all molecules

-chimerax Output superposed structure1 to sup.* for ChimeraX viewing.
          $ USalign structure1.pdb structure2.pdb -chimerax sup
          $ chimerax --script sup.cxc             # C-alpha trace aligned region
          $ chimerax --script sup_all.cxc         # C-alpha trace whole chain
          $ chimerax --script sup_atm.cxc         # full-atom aligned region
          $ chimerax --script sup_all_atm.cxc     # full-atom whole chain
          $ chimerax --script sup_all_atm_lig.cxc # full-atom with all molecules

     -do  Output distance of aligned residue pairs

Example usages ('gunzip' program is needed to read .gz compressed files):
    USalign 101m.cif.gz 1mba.pdb             # pairwise monomeric protein alignment
    USalign 1qf6.cif 5yyn.pdb.gz -mol RNA    # pairwise monomeric RNA alignment
    USalign model.pdb native.pdb -TMscore 1  # calculate TM-score between two conformations of a monomer
    USalign 4v4a.cif 4v49.cif -mm 1 -ter 1   # oligomeric alignment for asymmetic units
    USalign 3ksc.pdb1 4lej.pdb1 -mm 1 -ter 0 # oligomeric alignment for biological units
    USalign 1ajk.pdb.gz 2ayh.pdb.gz -mm 3    # circular permutation alignment

Additional options:
      -v  Print the version of US-align

      -a  TM-score normalized by the average length of two structures
          T or F, (default F). -a does not change the final alignment.

   -fast  Fast but slightly inaccurate alignment

    -dir  Perform all-against-all alignment among the list of PDB
          chains listed by 'chain_list' under 'chain_folder'.
          $ USalign -dir chain_folder/ chain_list

   -dir1  Use chain2 to search a list of PDB chains listed by 'chain1_list'
          under 'chain1_folder'.
          $ USalign -dir1 chain1_folder/ chain1_list chain2

   -dir2  Use chain1 to search a list of PDB chains listed by 'chain2_list'
          under 'chain2_folder'
          $ USalign chain1 -dir2 chain2_folder/ chain2_list

 -suffix  (Only when -dir1 and/or -dir2 are set, default is empty)
          add file name suffix to files listed by chain1_list or chain2_list

   -atom  4-character atom name used to represent a residue.
          Default is " C3'" for RNA/DNA and " CA " for proteins
          (note the spaces before and after CA).

  -split  Whether to split PDB file into multiple chains
           0: treat the whole structure as one single chain
              (default for -TMscore 2)
           1: treat each MODEL as a separate chain
           2: (default for other cases) treat each chain as a separate chain

 -outfmt  Output format
           0: (default) full output
           1: fasta format compact output
           2: tabular format very compact output
          -1: full output, but without version or citation information

  -TMcut  -1: (default) do not consider TMcut
          Values in [0.5,1): Do not proceed with TM-align for this
          structure pair if TM-score is unlikely to reach TMcut.
          TMcut is normalized as set by -a option:
          -2: normalized by longer structure length
          -1: normalized by shorter structure length
           0: (default, same as F) normalized by second structure
           1: same as T, normalized by average structure length

 -mirror  Whether to align the mirror image of input structure
           0: (default) do not align mirrored structure
           1: align mirror of Structure_1 to origin Structure_2,
              which usually requires the '-het 1' option:
              $ USalign 4glu.pdb 3p9w.pdb -mirror 1 -het 1

    -het  Whether to align residues marked as 'HETATM' in addition to 'ATOM  '
           0: (default) only align 'ATOM  ' residues
           1: align both 'ATOM  ' and 'HETATM' residues
           2: align both 'ATOM  ' and MSE residues

   -full  Whether to show full pairwise alignment of individual chains for
          -mm 2 or 4. T or F, (default F)

   -se    Do not perform superposition. Useful for extracting alignment from
          superposed structure pairs

 -infmt1  Input format for structure_1
 -infmt2  Input format for structure_2
          -1: (default) automatically detect PDB or PDBx/mmCIF format
           0: PDB format
           1: SPICKER format
           3: PDBx/mmCIF format

-chainmap (only useful for -mm 1) use the final chain mapping 'chainmap.txt'
          specified by user. 'chainmap.txt' is a tab-seperated text with two
          columns, one for each complex

-chain1   Chains to parse in structure_1
-chain2   Chains to parse in structure_2. Use _ for a chain without chain ID.
          Multiple chains can be separated by commas, e.g.,
          USalign -chain1 C,D,E,F 5jdo.pdb -chain2 A,B,C,D 3wtg.pdb -ter 0

-model1   Models to parse in structure_1
-model2   Models to parse in structure_2.
          Multiple models can be separated by commas, e.g.,
          USalign -model1 1,2 1a03.pdb -model2 3,4 1a0n.pdb -ter 0

Advanced usage 1 (generate an image for a pair of superposed structures):
    USalign 1cpc.pdb 1mba.pdb -o sup
    pymol -c -d @sup_all_atm.pml -g sup_all_atm.png

Advanced usage 2 (a quick search of query.pdb against I-TASSER PDB library):
    wget https://zhanggroup.org/library/PDB.tar.bz2
    tar -xjvf PDB.tar.bz2
    USalign query.pdb -dir2 PDB/ PDB/list -suffix .pdb -outfmt 2 -fast

---

# chatgpt response

安装成功了！输出显示 **US-align Version 20241108**，说明它已能正常启动。后续我们可以用 `structure_eval` 环境做 TM-score，用现有 `boltz` 环境中的 Biopython 做链提取和 RMSD 计算。

## 下一步：查找 7KI0 实验结构

先看看你的项目目录中是否已经有 7KI0 文件，避免重复下载：



如果没有输出，再下载 RCSB PDB 的实验结构：



下载后检查文件：



**先不要直接对完整的 7KI0 和候选物 CIF 运行 US-align。** 实验结构可能包含其他蛋白链、配体或非标准残基，而你的 Boltz 预测主要是 GLP-1R 与设计多肽。我们需要先识别并提取正确的链，再进行公平的结构比较。

把查找结果或下载结果发给我，下一步我们就用 Biopython 自动检查 7KI0 的链 ID、序列长度和残基组成。

---

# you asked

message time: 2026-10-22 20:33:47

LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
(boltz) ziguimu@DESKTOP-8RLFC97:~$
我怎么进入usalign环境呢

---

# chatgpt response

你现在在 `(boltz)` 环境中。切换到已经安装好 US-align 的独立环境，只需要一条命令。

## 1. 进入 US-align 环境

`
成功后，终端提示符应该从：

`
变成：

`
## 2. 验证 US-align

``如果打印出版本和使用说明，就说明可以正常使用。

## 3. 如何切回 Boltz 环境？

```果只是临时运行一次 US-align，也可以**不切换环境**，直接在 `(boltz)` 中执行：

```# 4. 下一步用哪个文件？

你已经有现成的 7KI0 参考结构，不需要再下载：

- 受体：`LOCAL_PATH
- Semaglutide：`LOCAL_PATH
- 仅含多肽的参考结构：`LOCAL_PATH

**先切换到 `structure_eval`，然后告诉我是否成功。** 下一步我们就用已有文件做结构比对，不需要重新预测或重复下载。

---

# you asked

message time: 2026-10-22 20:34:34

为什么不把这个环境直接命名为usalign

---

# chatgpt response

完全可以，而且**如果这个环境主要就是用来运行 US-align，命名为 `usalign` 更直观**。

之前命名成 `structure_eval`，是因为我们当时把它当作一个更广义的「结构评价环境」来考虑：除了 US-align，未来也可能放入其他结构比较工具。但这并不是必须的。

两种命名的区别：

| 环境名 | 含义 | 适合场景 |
|---|---|---|
| `usalign` | 专门运行 US-align | 环境只负责这一个工具 |
| `structure_eval` | 蛋白质结构评价工具集合 | 未来还要集成其他工具 |

**我建议现在先保留 `structure_eval`**，因为你的 GLP-1R 项目后续不仅需要 TM-score，还需要 RMSD、链提取和结构对齐。US-align 可以负责前两者中的结构对齐与 TM-score，Biopython 则可以在这个环境里辅助计算 RMSD，不必为每个工具单独创建环境。

不过，环境名本身不会限制它能安装哪些软件。假如你更喜欢 `usalign`，也完全可以改名：

```bash
conda d不支持 `conda rename`，可以先检查：

```bash
conda -建环境——没有必要。

---

# you asked

message time: 2026-10-22 20:35:20

已经改了，接下来做什么

---

# chatgpt response

下一步我们先不急着批量计算所有候选物的 TM-score 和 RMSD。**先用实验结构 7KI0 建立一个可靠的结构比较基准，再把 Boltz-2 预测结果与它比较。**

对你现在的 GLP-1R 项目，建议按这个顺序走：

1. **确认 `usalign` 环境正常**，并检查 7KI0 实验结构里的链。
2. 用 US-align 比较实验结构与 Boltz-2 的 Semaglutide 参考预测。
3. 计算更关键的 **肽链结合姿势 RMSD**：先对齐受体，再比较肽链，而不是单独对齐肽链。
4. 确认计算方法可靠后，再批量处理 27 个候选物和对照组。

注意：Semaglutide 的参考预测使用了标准氨基酸序列近似，没有完整模拟其非天然氨基酸替换和脂肪酸修饰。因此，我们把它当作**计算预测参照**，而不是与实验结构完全等价的复现。

## 第一步：检查环境，并确认实验结构的链信息

请在 WSL Ubuntu 终端中依次执行。

### 1. 检查 US-align

`
如果能显示版本或使用说明，就说明工具正常。然后检查实验结构文件是否存在：

`
### 2. 查看 7KI0 的链和序列长度

为了避免把受体、肽链或其他分子弄混，执行下面这条命令。它使用已有的 `boltz` 环境中的 Biopython 读取结构，不需要重新安装软件。

``这段命令只读取结构，不会修改任何文件。

### 3. 把输出发给我

我会根据实际链信息确定下一条 US-align 命令，并核对预测结构中对应的受体链和肽链。之后我们会分别计算：

- **整体结构 TM-score**：衡量整体折叠和结构相似性。
- **受体对齐后的肽链 RMSD**：衡量预测的结合姿势与实验结合姿势相差多少。

这两项指标回答的是不同问题，不能互相替代。等第一步确认无误后，再正式计算，避免链选错导致结果失真。

后续如果你想固定每周检查一次项目进度，也可以让我帮你设置提醒。

---

# you asked

message time: 2026-10-22 20:36:04

PY  break
(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

你现在还在 `(usalign)` 环境里，说明环境已经激活了。看起来你可能只输入了代码最后的 `PY`，还没有看到完整的链信息输出。

我们先检查一下，不用重新安装任何东西。

请直接复制下面这一整条命令到终端，**从 `conda run` 开始，一直到最后一行 `PY`，全部一起执行**：



正常情况下，执行后会打印出各条链的编号、氨基酸残基数和序列，随后返回类似这样的终端提示符：



**如果终端显示 `>` 而不是正常提示符**，说明 shell 还在等待你补全多行命令。这时先按 `Ctrl+C` 退出，再重新粘贴完整命令。

把执行结果发给我，我们就可以继续确认链对应关系，准备计算结构相似性和结合姿势 RMSD。

---

# you asked

message time: 2026-10-22 20:37:02

for model in structure:
    print(f"Model: {model.id}")
    for chain in model:
        residues = [
            r for r in chain
            if r.id[0] == " " and r.resname in {
                "ALA","ARG","ASN","ASP","CYS","GLN","GLU","GLY",
                "HIS","ILE","LEU","LYS","MET","PHE","PRO","SER",
                "THR","TRP","TYR","VAL","MSE"
            }
        ]
        seq = "".join(
            seq1(r.resname, custom_map={"MSE": "M"})
            for r in residues
        )
        print(f"Chain {chain.id}: {len(residues)} residues")
        print(seq)
    break
> PY
(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

看起来命令已经结束了，但**没有打印出任何链信息**。你粘贴的内容是从 `for model in structure:` 开始的，可能前面的导入代码和文件读取代码没有执行。

我们先用最简单的方法检查文件是否存在、Python 能否读取。请整段复制执行：



这是一条完整命令，不需要输入 `PY`，也不需要逐行粘贴。

正常情况下，会显示类似：



实际链编号和数量以你的输出为准。**把完整输出发给我**，我们再根据实际结构确定下一步，不要先猜链编号或运行 RMSD 计算。

---

# you asked

message time: 2026-10-22 20:37:22

Chains: [('A', 229), ('B', 375), ('G', 56), ('N', 130), ('P', 33), ('R', 400)]
(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

很好，文件读取成功了。现在确认 7KI0 实验结构共有 6 条链：

| 链 | 残基数 | 当前判断 |
|---|---:|---|
| A | 229 | 需要核对序列 |
| B | 375 | 需要核对序列 |
| G | 56 | 需要核对序列 |
| N | 130 | 需要核对序列 |
| P | 33 | 很可能是 Semaglutide 肽链 |
| R | 400 | 很可能是 GLP-1R 受体链 |

其中，P 链有 33 个残基，R 链有 400 个残基，与我们此前保存的单独链文件信息基本吻合。不过，**残基数只能作为线索，还要检查序列，才能可靠确认链的身份**。其他链也可能是抗体片段、辅助蛋白或结构中包含的其他组分。

## 第二步：确认链身份，然后开始结构对齐

请执行下面这条命令，打印各链的氨基酸序列。这样可以确认 R 是否为受体、P 是否为肽链，并为后续比较做准备。

```bash
conda 下来我们会先比较两组结构：

1. **实验受体 R 链 vs. Boltz-2 预测受体 A 链**：检查受体结构是否对齐良好。
2. **实验肽链 P vs. Boltz-2 预测肽链 B**：在受体对齐的坐标框架下计算肽链 RMSD，判断预测结合姿势与实验结构的差异。

特别注意：第二项不能把两条肽链单独做最佳对齐后，就直接当作结合姿势 RMSD；那样会掩盖肽链在受体上的位置和方向差异。我们会采用先对齐受体、再比较肽链的方式。

---

# you asked

message time: 2026-10-22 20:37:52

Chain A: sequence length=209
DQRNEEKAQREANKKIEKQLQKDKQVYRATHRLLLLGSGIFETKFQVDKVNFHMFDVGAQRDERRKWIQCFNDVTAIIFVVANRLQAALKLFDSIWNNKWLRDTSVILFLNKQDLLAEKVLAGKSKIEDYFPEFARYTTPEDATPEPGEDPRVTRAKYFIRDEFLRISTASGDGRHYCYPHFTCENIRRVFNDCRDIIQRMHLRQYELL
Chain B: sequence length=338
ELDQLRQEAEQLKNQIRDARKACADATLSQITNNIDPVGRIQMRTRRTLRGHLAKIYAMHWGTDSRLLVSASQDGKLIIWDSYTTNKVHAIPLRSSWVMTCAYAPSGNYVACGGLDNICSIYNLKTREGNVRVSRELAGHTGYLSCCRFLDDNQIVTSSGDTTCALWDIETGQQTTTFTGHTGDVMSLSLAPDTRLFVSGACDASAKLWDVREGMCRQTFTGHESDINAICFFPNGNAFATGSDDATCRLFDLRADQELMTYSHDNIICGITSVSFSKSGRLLLAGYDDFNCNVWDALKADRAGVLAGHDNRVSCLGVTDDGMAVATGSWDSFLKIWN
Chain G: sequence length=56
ASIAQARKLVEQLKMEANIDRIKVSKAAADLMAYCEAHAKEDPLLTPVPASENPFR
Chain N: sequence length=126
QVQLQESGGGLVQPGGSLRLSCAASGFTFSNYKMNWVRQAPGKGLEWVSDISQSGASISYTGSVKGRFTISRDNAKNTLYLQMNSLKPEDTAVYYCARCPAPFTRDCFDVTSTTYAYRGQGTQVTV
Chain P: sequence length=28
EGTFTSDVSSYLEGQAAKEFIAWLVRGR
Chain R: sequence length=384
TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWPDGEPGSFVNVSCPWYLPWASSVPQGHVYRFCTAEGLWLQKDNSSLPWRDLSECEESPEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANLDIKCRLAKSTLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLE
(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

序列已经足够我们确定关键链了，而且有一个值得注意的细节：**7KI0 的受体 R 链是 384 个氨基酸，Semaglutide 的 P 链是 28 个氨基酸**。此前我们看到的 400 和 33 是按结构中标准氨基酸残基计数，而 `PPBuilder` 只拼接可形成连续肽段的残基，因此两种统计方式可能不同。

从序列看：

- **R 链**：GLP-1R，包含胞外区和跨膜区。
- **P 链**：Semaglutide 相关肽链的结构中可解析片段。
- **预测结构 A 链（395 aa）** 和 R 链（384 aa）长度不同，因此不能直接假设两者残基编号一一对应。
- **预测结构 B 链（31 aa）** 和实验 P 链（28 aa）长度也不同，需要先做序列对应与结构覆盖率检查。

所以，我们现在不应该直接拿整个复合物的 TM-score 或 RMSD 当作结合姿势评价。先把受体链和肽链的对应关系确认清楚，才能保证后续指标有意义。

## 第三步：检查 Boltz-2 预测结构的链序列

我们先检查参考预测的 Model 0，看看 A、B 链与实验 R、P 链分别有多少序列相似性。这样可以决定后续应比较完整受体，还是只比较有共同结构的区域。

请复制执行下面这条完整命令：



把输出贴给我。下一步我们就可以根据序列对应关系，选择合理的受体对齐区域，再计算受体对齐后的肽链 RMSD 和结构 TM-score。

如果你愿意，也可以让我在后续帮你安排每周一次的项目检查提醒，跟踪结构评价脚本和候选物分析进度。

---

# you asked

message time: 2026-10-22 20:40:28

exp_seq = {c.id: get_seq(c) for c in exp}
pred_seq = {c.id: get_seq(c) for c in pred}

PY      print(aln)ned_score={aln.score:.1f}"cted {pred_id}: "")
(usalign) ziguimu@DESKTOP-8RLFC97:~$
这个复制粘贴的PY怎么错位了，上次也是这样

---

# chatgpt response

这是我之前给你的多行命令不够稳妥，抱歉。问题很可能出在 **Windows 浏览器向 WSL 终端粘贴多行代码时，Here-document（`<<'PY'`）没有被完整、连续地传入**，导致部分代码错位，最后的 `PY` 被当成普通输入或与其他行混在一起。

你前两次都遇到类似问题，我们换一种更可靠的方式：**不再使用 `<<'PY'`，而是把代码保存成 `.py` 文件再执行。** 这样也更适合你后续批量计算结构指标。

## 第一步：创建脚本文件

在终端完整执行下面这一条命令，它会打开一个文本编辑器：



接下来我会给你完整脚本。你只需要把代码粘贴进去，然后按 `Ctrl+O` 保存、回车确认，再按 `Ctrl+X` 退出，最后执行：



这样就不需要再依赖 `PY` 结束标记了。

另外，你刚才那次输出显示代码被打乱，**不代表结构文件或 Conda 环境出了问题**，只是脚本没有被完整执行。我们先把运行方式固定下来，再继续做序列比对。

---

# you asked

message time: 2026-10-22 20:41:28

脚本呢

---

# chatgpt response

抱歉，刚才说要给脚本，却漏发了。我们这次直接创建完整脚本，不再使用容易粘贴错位的 `PY` 结束标记。

## 1. 打开脚本文件

在终端执行：

`
## 2. 把下面的完整代码粘贴进去

<CodeBlock language="python" editable>
from Bio.PDB import MMCIFParser, PPBuilder
from Bio.Align import PairwiseAligner
from pathlib import Path
import sys

exp_path = Path(
    "LOCAL_PATH"
)

pred_path = Path(
    "LOCAL_PATH"
    "reference_semaglutide/predictions/"
    "boltz_results_semaglutide_glp1r_reference/"
    "predictions/semaglutide_glp1r_reference/"
    "semaglutide_glp1r_reference_model_0.cif"
)

for path in (exp_path, pred_path):
    if not path.is_file():
        print(f"ERROR: File not found: {path}")
        sys.exit(1)

parser = MMCIFParser(QUIET=True)
exp = parser.get_structure("experimental", str(exp_path))[0]
pred = parser.get_structure("predicted", str(pred_path))[0]


def get_sequence(chain):
    peptides = PPBuilder().build_peptides(chain)
    return "".join(str(peptide.get_sequence()) for peptide in peptides)


exp_seq = {chain.id: get_sequence(chain) for chain in exp}
pred_seq = {chain.id: get_sequence(chain) for chain in pred}

print("=" * 60)
print("EXPERIMENTAL STRUCTURE: 7KI0")
print("=" * 60)

for chain_id, sequence in exp_seq.items():
    print(f"Chain {chain_id}: {len(sequence)} aa")
    print(sequence)

print("\n" + "=" * 60)
print("BOLTZ-2 PREDICTED STRUCTURE: MODEL 0")
print("=" * 60)

for chain_id, sequence in pred_seq.items():
    print(f"Chain {chain_id}: {len(sequence)} aa")
    print(sequence)

aligner = PairwiseAligner()
aligner.mode = "local"
aligner.match_score = 2
aligner.mismatch_score = -1
aligner.open_gap_score = -5
aligner.extend_gap_score = -0.5

print("\n" + "=" * 60)
print("SEQUENCE ALIGNMENT SCORES")
print("=" * 60)

for exp_id in ("R", "P"):
    if exp_id not in exp_seq:
        print(f"Experimental chain {exp_id} not found")
        continue

    for pred_id in ("A", "B"):
        if pred_id not in pred_seq:
            print(f"Predicted chain {pred_id} not found")
            continue

        alignment = aligner.align(
            exp_seq[exp_id], pred_seq[pred_id]
        )[0]

        print(
            f"\nExperimental {exp_id} vs predicted {pred_id}: "
            f"score = {alignment.score:.1f}"
        )
        print(alignment)
</CodeBlock>

## 3. 保存并运行

在 `nano` 编辑器里：

1. 按 `Ctrl+O` 保存。
2. 按 `Entez python ~/check_glp1r_chains.py
```

这次即使终端显示很多行，也不需要输入任何 `PY` 标记。

**把运行结果发给我。** 我们先核对实验结构和预测结构的链序列对应关系，再编写正式的 TM-score 与受体对齐后肽链 RMSD 计算脚本。

---

# you asked

message time: 2026-10-22 20:42:11

============================================================
EXPERIMENTAL STRUCTURE: 7KI0
============================================================
Chain A: 209 aa
DQRNEEKAQREANKKIEKQLQKDKQVYRATHRLLLLGSGIFETKFQVDKVNFHMFDVGAQRDERRKWIQCFNDVTAIIFVVANRLQAALKLFDSIWNNKWLRDTSVILFLNKQDLLAEKVLAGKSKIEDYFPEFARYTTPEDATPEPGEDPRVTRAKYFIRDEFLRISTASGDGRHYCYPHFTCENIRRVFNDCRDIIQRMHLRQYELL
Chain B: 338 aa
ELDQLRQEAEQLKNQIRDARKACADATLSQITNNIDPVGRIQMRTRRTLRGHLAKIYAMHWGTDSRLLVSASQDGKLIIWDSYTTNKVHAIPLRSSWVMTCAYAPSGNYVACGGLDNICSIYNLKTREGNVRVSRELAGHTGYLSCCRFLDDNQIVTSSGDTTCALWDIETGQQTTTFTGHTGDVMSLSLAPDTRLFVSGACDASAKLWDVREGMCRQTFTGHESDINAICFFPNGNAFATGSDDATCRLFDLRADQELMTYSHDNIICGITSVSFSKSGRLLLAGYDDFNCNVWDALKADRAGVLAGHDNRVSCLGVTDDGMAVATGSWDSFLKIWN
Chain G: 56 aa
ASIAQARKLVEQLKMEANIDRIKVSKAAADLMAYCEAHAKEDPLLTPVPASENPFR
Chain N: 126 aa
QVQLQESGGGLVQPGGSLRLSCAASGFTFSNYKMNWVRQAPGKGLEWVSDISQSGASISYTGSVKGRFTISRDNAKNTLYLQMNSLKPEDTAVYYCARCPAPFTRDCFDVTSTTYAYRGQGTQVTV
Chain P: 28 aa
EGTFTSDVSSYLEGQAAKEFIAWLVRGR
Chain R: 384 aa
TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWPDGEPGSFVNVSCPWYLPWASSVPQGHVYRFCTAEGLWLQKDNSSLPWRDLSECEESPEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANLDIKCRLAKSTLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLE

============================================================
BOLTZ-2 PREDICTED STRUCTURE: MODEL 0
============================================================
Chain A: 395 aa
TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWPDGEPGSFVNVSCPWYLPWASSVPQGHVYRFCTAEGLWLQKDNSSLPWRDLSECEESKRGERSSPEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANLMCKTDIKCRLAKSTLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLE
Chain B: 31 aa
HAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG

============================================================
SEQUENCE ALIGNMENT SCORES
============================================================

Experimental R vs predicted A: score = 753.5
target            0 TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWPDGEPGSFVNVSCPWY
                  0 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
query             0 TVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWPDGEPGSFVNVSCPWY

target           60 LPWASSVPQGHVYRFCTAEGLWLQKDNSSLPWRDLSECEE-------SPEEQLLFLYIIY
                 60 ||||||||||||||||||||||||||||||||||||||||-------|||||||||||||
query            60 LPWASSVPQGHVYRFCTAEGLWLQKDNSSLPWRDLSECEESKRGERSSPEEQLLFLYIIY

target          113 TVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTA
                120 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
query           120 TVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTA

target          173 AQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRL
                180 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
query           180 AQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRL

target          233 YVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVI
                240 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
query           240 YVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVI

target          293 CIVVSKLKANL----DIKCRLAKSTLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTEL
                300 |||||||||||----|||||||||||||||||||||||||||||||||||||||||||||
query           300 CIVVSKLKANLMCKTDIKCRLAKSTLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTEL

target          349 SFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLE 384
                360 ||||||||||||||||||||||||||||||||||| 395
query           360 SFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLE 395


Experimental R vs predicted B: score = 7.0
target          334 HARGT 339
                  0 ||.||   5
query             0 HAEGT   5


Experimental P vs predicted A: score = 6.0
target            3 FTS   6
                  0 |||   3
query           361 FTS 364


Experimental P vs predicted B: score = 56.0
target            0 EGTFTSDVSSYLEGQAAKEFIAWLVRGR 28
                  0 |||||||||||||||||||||||||||| 28
query             2 EGTFTSDVSSYLEGQAAKEFIAWLVRGR 30

(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

这次输出很有价值：**实验结构与 Boltz-2 参考预测的受体序列高度一致，肽链也能明确对应。** 我们可以继续做结构比较了，但需要先处理两个问题。

- 受体 R 与预测 A 的序列大部分一致，但预测中有额外插入片段，末端也有少量差异。不能只按残基编号直接计算 RMSD。
- 实验 P 链与预测 B 链的序列完全对应于共同的 28 aa 片段；预测 B 额外多出 N 端一个 `H` 和 C 端一个 `G`。比较时应使用序列比对建立的对应关系，而不是简单假定两条链的所有残基一一对应。

还有一点：实验结构中的其他链可能会影响复合物整体对齐。因此我们先做**受体结构对齐，然后计算共同肽段的结合姿势 RMSD**，并把整体复合物 TM-score 作为另一项独立指标。

## 下一步：创建正式的结构比较脚本

这次直接保存为 `.py` 文件运行，避免再次遇到终端粘贴错位。

### 1. 创建脚本

`
把下面的完整代码粘贴进去：

<CodeBlock language="python" editable>
from pathlib import Path
from Bio.PDB import MMCIFParser, Superimposer
from Bio.Align import PairwiseAligner
from Bio.SeqUtils import seq1
import numpy as np
import sys

EXP_PATH = Path(
    "LOCAL_PATH"
)

PRED_PATH = Path(
    "LOCAL_PATH"
    "reference_semaglutide/predictions/"
    "boltz_results_semaglutide_glp1r_reference/"
    "predictions/semaglutide_glp1r_reference/"
    "semaglutide_glp1r_reference_model_0.cif"
)

STANDARD_AA = {
    "ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU",
    "GLY", "HIS", "ILE", "LEU", "LYS", "MET", "PHE",
    "PRO", "SER", "THR", "TRP", "TYR", "VAL"
}


def load_chain_residues(chain):
    residues = [
        r for r in chain
        if r.id[0] == " "
        and r.resname in STANDARD_AA
        and "CA" in r
    ]
    sequence = "".join(seq1(r.resname) for r in residues)
    return residues, sequence


def make_aligner():
    aligner = PairwiseAligner()
    aligner.mode = "global"
    aligner.match_score = 2
    aligner.mismatch_score = -1
    aligner.open_gap_score = -8
    aligner.extend_gap_score = -0.5
    return aligner


def matched_ca_pairs(fixed_residues, fixed_seq,
                     moving_residues, moving_seq):
    alignment = make_aligner().align(fixed_seq, moving_seq)[0]
    pairs = []

    # alignment.aligned gives corresponding ungapped sequence blocks.
    for block_fixed, block_moving in zip(*alignment.aligned):
        start_f, end_f = map(int, block_fixed)
        start_m, end_m = map(int, block_moving)

        length = min(end_f - start_f, end_m - start_m)

        for offset in range(length):
            i = start_f + offset
            j = start_m + offset

            # Only use identical amino acids for structural correspondence.
            if fixed_seq[i] != moving_seq[j]:
                continue

            rf = fixed_residues[i]
            rm = moving_residues[j]

            if "CA" in rf and "CA" in rm:
                pairs.append((rf["CA"], rm["CA"]))

    return alignment, pairs


def rmsd(atom_pairs):
    if not atom_pairs:
        return float("nan")

    fixed_xyz = np.array([a.get_coord() for a, _ in atom_pairs])
    moving_xyz = np.array([b.get_coord() for _, b in atom_pairs])

    return float(np.sqrt(np.mean(np.sum(
        (fixed_xyz - moving_xyz) ** 2, axis=1
    ))))


for path in (EXP_PATH, PRED_PATH):
    if not path.is_file():
        print(f"ERROR: File not found: {path}")
        sys.exit(1)

parser = MMCIFParser(QUIET=True)
exp_model = parser.get_structure("experimental", str(EXP_PATH))[0]
pred_model = parser.get_structure("predicted", str(PRED_PATH))[0]

for chain_id in ("R", "P"):
    if chain_id not in exp_model:
        sys.exit(f"ERROR: Experimental chain {chain_id} not found.")

for chain_id in ("A", "B"):
    if chain_id not in pred_model:
        sys.exit(f"ERROR: Predicted chain {chain_id} not found.")

exp_r, exp_r_seq = load_chain_residues(exp_model["R"])
pred_r, pred_r_seq = load_chain_residues(pred_model["A"])
exp_p, exp_p_seq = load_chain_residues(exp_model["P"])
pred_p, pred_p_seq = load_chain_residues(pred_model["B"])

# 1. Align receptor sequences and fit predicted receptor onto experimental receptor.
receptor_alignment, receptor_pairs = matched_ca_pairs(
    exp_r, exp_r_seq, pred_r, pred_r_seq
)

if len(receptor_pairs) < 30:
    sys.exit(
        f"ERROR: Only {len(receptor_pairs)} matching receptor C-alpha pairs; "
        "alignment is not reliable."
    )

sup = Superimposer()
sup.set_atoms(
    [fixed for fixed, moving in receptor_pairs],
    [moving for fixed, moving in receptor_pairs]
)

# Apply this same receptor-derived transformation to the entire predicted model.
sup.apply(list(pred_model.get_atoms()))

receptor_rmsd = rmsd(receptor_pairs)

# 2. Map matching peptide residues by sequence.
peptide_alignment, peptide_pairs = matched_ca_pairs(
    exp_p, exp_p_seq, pred_p, pred_p_seq
)

# Do NOT independently superimpose the peptides:
# their RMSD is measured after receptor alignment, preserving binding pose.
peptide_pose_rmsd = rmsd(peptide_pairs)

print("=" * 64)
print("GLP-1R / SEMAGLUTIDE STRUCTURAL COMPARISON")
print("=" * 64)
print(f"Experimental receptor R: {len(exp_r_seq)} residues")
print(f"Predicted receptor A:    {len(pred_r_seq)} residues")
print(f"Receptor matched CA pairs: {len(receptor_pairs)}")
print(f"Receptor RMSD after fit: {receptor_rmsd:.3f} A")
print()
print(f"Experimental peptide P: {len(exp_p_seq)} residues")
print(f"Predicted peptide B:    {len(pred_p_seq)} residues")
print(f"Peptide matched CA pairs: {len(peptide_pairs)}")
print(f"Peptide pose RMSD after receptor fit: {peptide_pose_rmsd:.3f} A")
print()
print("Important:")
print("- Peptide RMSD is measured in the receptor-aligned coordinate frame.")
print("- Only identical amino acids in aligned sequence blocks are compared.")
print("- These are C-alpha RMSDs, not TM-scores or affinity measurements.")
print("=" * 64)
</CodeBlock>

### 2. 保存并运行

在 boltz python ~/compare_glp1r_pose.py
```

### 3. 我们要看什么？

主要关注三个输出：

- `Receptor matched CA pairs`：受体实际参与比较的残基对数量。
- `Receptor RMSD after fit`：受体对齐后，共同残基的结构差异。
- `Peptide pose RMSD after receptor fit`：最关键的指标，反映肽链在受体上的预测结合姿势与实验姿势的差异。

这些数值出来后，我们再决定是否需要用 US-align 计算独立的 TM-score。**不要预先设定通过阈值，也不要把结构相似度直接解释成结合亲和力。**

---

# you asked

message time: 2026-10-22 20:43:31

================================================================
GLP-1R / SEMAGLUTIDE STRUCTURAL COMPARISON
================================================================
Experimental receptor R: 384 residues
Predicted receptor A:    395 residues
Receptor matched CA pairs: 384
Receptor RMSD after fit: 4.498 A

Experimental peptide P: 29 residues
Predicted peptide B:    31 residues
Peptide matched CA pairs: 29
Peptide pose RMSD after receptor fit: 3.242 A

Important:
- Peptide RMSD is measured in the receptor-aligned coordinate frame.
- Only identical amino acids in aligned sequence blocks are compared.
- These are C-alpha RMSDs, not TM-scores or affinity measurements.
=========================================

---

# chatgpt response

这组结果已经能说明一些问题：**Boltz-2 的 Semaglutide 参考预测与 7KI0 实验结构并不完全重合，尤其需要进一步检查受体的对齐质量，以及肽链的结合姿势。**

| 指标 | 结果 | 初步解读 |
|---|---:|---|
| 受体匹配 Cα 残基对 | 384 | 当前脚本尝试比较了全部 384 个实验受体残基 |
| 受体对齐后 RMSD | 4.498 Å | 整体偏差值得进一步分析 |
| 肽链匹配 Cα 残基对 | 29 | 覆盖了实验肽链的大部分可解析残基 |
| 肽链姿势 RMSD | 3.242 Å | 对齐受体后，肽链仍存在可见的位置或构象差异 |

但现在还不能直接把这些数字当作最终评价。**有一个重要的技术问题需要先修正：目前脚本使用全局刚体对齐后，计算的是共同残基的 Cα RMSD；它没有检查受体是否因局部构象变化而产生较大偏差，也没有独立验证残基映射是否正确。**

另外，受体 RMSD 为 4.498 Å，不代表所有区域都偏差很大；GLP-1R 包含胞外区和多个跨膜螺旋，局部区域可能比整体更一致。肽链 RMSD 3.242 Å 也需要结合结合口袋的位置和肽链构象判断，不能单独用来判定预测成功或失败。

## 下一步：计算“结合口袋局部对齐”的肽链 RMSD

我建议暂时不要批量跑 27 个候选物。先对参考结构做一次更有针对性的检查：

1. 用实验结构中与 Semaglutide 接近的受体残基，拟合预测受体。
2. 使用同一个刚体变换计算肽链 RMSD，不单独移动肽链。
3. 同时报告全受体对齐 RMSD、口袋局部对齐 RMSD，以及参与拟合的残基数量。

这样可以区分：肽链偏差究竟主要来自受体整体构象差异，还是来自预测的肽链结合姿势本身。

这里有一个关键原则：**口袋残基应根据实验结构中肽链周围的空间距离选取，并通过序列比对映射到预测结构；不能直接使用相同残基编号。**

得到这组指标后，我们再用 US-align 计算受体结构的 TM-score，并判断哪些指标适合用于后续候选物的排序。TM-score、RMSD 和 Boltz-2 的 ipTM 是不同的指标，不应混为一谈。

如果你愿意，我也可以帮你设置每周一次的项目进度提醒，持续跟踪参考结构校准和候选物评价进展。

---

# you asked

message time: 2026-10-22 20:44:40

给我分析一下这个结果是什么意思

---

# chatgpt response

这组结果的意义是：**我们已经让 Boltz-2 预测的 GLP-1R–Semaglutide 复合物与实验结构 7KI0 做了第一次定量比较，发现预测结构与实验结构存在一定偏差。** 但目前还不能判断预测方法好不好，更不能据此判断候选蛋白是否真的能结合 GLP-1R。

我逐项解释，并结合你的 AI-BinderDesign 项目说说这些结果能支持什么结论。

## 一、四个数字分别意味着什么？

<box gap={3}>
  <row align=start gap={3}>
    <box background="surface-secondary" radius="lg" padding={3} align=center minWidth="104px">
      <title size="xl" color="default">384</title>
      <text size="xs" color="secondary">匹配残基对</text>
    </box>
    <box flex="1" gap={1}>
      **1. 受体匹配 Cα 残基对：384**

      实验结构的 GLP-1R 受体链 R 有 384 个可解析的标准氨基酸残基，预测受体 A 有 395 个残基。脚本通过序列比对，找到了 384 对可比较的 Cα 原子。

      这说明受体序列映射覆盖很广，但**不代表所有对应关系都已经经过充分验证**，尤其是存在插入片段和局部构象差异时。
    </box>
  </row>
  <divider color="subtle" />
  <row align=start gap={3}>
    <box background="surface-secondary" radius="lg" padding={3} align=center minWidth="104px">
      <title size="xl" color="default">4.498 Å</title>
      <text size="xs" color="secondary">受体 RMSD</text>
    </box>
    <box flex="1" gap={1}>
      **2. 受体对齐后 RMSD：4.498 Å**

      RMSD 衡量对应原子坐标之间的平均偏差。数值越小，通常代表比较的结构越接近。

      4.498 Å 表明在当前采用的全受体对齐方法下，实验受体与预测受体的对应 Cα 坐标存在明显差异。但它可能同时受到胞外区、跨膜区、柔性环区和结构域相对运动的影响。

      **不能仅凭这个整体 RMSD，就认定受体折叠错误。**
    </box>
  </row>
  <divider color="subtle" />
  <row align=start gap={3}>
    <box background="surface-secondary" radius="lg" padding={3} align=center minWidth="104px">
      <title size="xl" color="default">29</title>
      <text size="xs" color="secondary">匹配肽链残基对</text>
    </box>
    <box flex="1" gap={1}>
      **3. 肽链匹配 Cα 残基对：29**

      实验肽链 P 和预测肽链 B 通过序列比对找到了 29 对相同氨基酸的 Cα 原子。

      这说明脚本能够比较两条肽链的大部分共同序列。不过，这里的 29 是当前结构解析及筛选规则下的匹配数量，不等于两条肽链所有原子都完全对应。
    </box>
  </row>
  <divider color="subtle" />
  <row align=start gap={3}>
    <box background="surface-secondary" radius="lg" padding={3} align=center minWidth="104px">
      <title size="xl" color="default">3.242 Å</title>
      <text size="xs" color="secondary">肽链姿势 RMSD</text>
    </box>
    <box flex="1" gap={1}>
      **4. 肽链姿势 RMSD：3.242 Å**

      这是当前结果中与你最关心的结合姿势最相关的指标。

      脚本先用受体结构完成空间对齐，再在不单独移动肽链的情况下计算 RMSD。因此，这个值同时受到肽链自身构象以及肽链相对于受体的位置和方向影响。

      3.242 Å 表明预测肽链与实验肽链仍有一定坐标差异，但**不能单凭这个数字判断结合姿势是否正确**；还需要检查肽链是否覆盖了相同结合区域、关键接触是否保留，以及受体局部构象是否可比。
    </box>
  </row>
</box>

## 二、为什么受体 RMSD 比肽链 RMSD 更大？

你的结果是：

- 受体 RMSD：4.498 Å
- 肽链姿势 RMSD：3.242 Å

这并不矛盾，因为两个数衡量的对象不同。

受体 RMSD 使用了大量跨膜区、胞外区及其他区域的残基；这些区域不一定以完全相同的相对构象出现。肽链 RMSD 则只计算匹配肽链的 Cα 原子，并且是在受体对齐后计算的。

因此，有一种可能是：预测受体的整体构象与实验结构有差异，但预测肽链仍处于相对合理的结合位置。另一种可能是：受体的局部构象差异本身影响了肽链姿势的比较。

目前的四个数字无法区分这两种情况。我们需要进一步检查 GLP-1R 结合口袋附近的局部 RMSD，并观察实验与预测的肽链接触关系。

## 三、对你的 GLP-1R 项目意味着什么？

这次计算最重要的价值不是证明 Boltz-2 预测成功或失败，而是建立一个可重复的评价流程。

| 当前结果支持的结论 | 当前结果不支持的结论 |
|---|---|
| 已经可以进行实验结构与预测结构的坐标比较 | Boltz-2 对 GLP-1R 的预测一定准确或不准确 |
| 全受体对齐后仍存在一定结构差异 | 所有受体区域都预测得不好 |
| 肽链姿势与实验结构并非完全重合 | Semaglutide 一定无法结合受体 |
| 可以继续评估局部结构与结合界面 | 某个设计候选物具有真实结合能力或特定亲和力 |

对你正在做的 AI-BinderDesign 项目来说，这恰好体现了一个重要方法论：**结构评价指标必须明确说明自己测量的是什么，不能把单一分数直接当作生物学结论。**

不过还要强调：Semaglutide 参考预测使用的是标准氨基酸序列近似，并没有完整建模药物的非天然氨基酸替换和脂肪酸修饰。因此，当前比较不是对真实修饰后 Semaglutide 的完全复现验证。

## 四、我建议接下来做什么？

按优先级排列：

<list marker="number" gap={2}>
  <list-item>**检查结合口袋局部 RMSD。** 以实验结构中肽链附近的受体残基为依据，建立对应残基映射，再用这些残基拟合预测受体。需要同时报告局部 RMSD 和所用残基数量。</list-item>
  <list-item>**检查肽链的空间位置和接触关系。** 比较实验结构与预测结构中的肽链是否占据相近的结合区域，以及关键接触残基是否保留。</list-item>
  <list-item>**再计算 US-align 的 TM-score。** 将它作为独立的结构相似性指标，与 RMSD 分开记录。TM-score 也不能直接代表结合亲和力。</list-item>
  <list-item>**最后再处理 27 个候选物。** 先用参考体系确认链映射、结构对齐和指标计算可靠，再把相同方法应用到候选物与对照组，避免比较流程本身引入偏差。</list-item>
</list>

**我的判断：** 目前最有价值的结论是，你已经完成了从“模型给出了一个结构”到“可以用实验结构定量检验模型”的第一步。4.498 Å 和 3.242 Å 是值得进一步调查的结果，但还不是最终的质量判定。下一步应优先做结合口袋局部对齐和接触分析，而不是急着给模型打分或给候选物排名。

---

# you asked

message time: 2026-10-22 20:45:33

我的意思是RMSD值为多少算好

---

# chatgpt response

对于蛋白质结构比较，**RMSD 越低通常越好，但没有适用于所有情况的统一阈值**。你的 GLP-1R 项目需要区分全蛋白 RMSD 和配体结合姿势 RMSD。

## 1. 常用 RMSD 参考标准

以下是结构比较中常见的经验性参考，不是严格的通用判定标准。

| RMSD | 一般解读 |
|---:|---|
| <escape>< 1 Å</escape> | 非常接近 |
| 1–2 Å | 高度相似 |
| 2–3 Å | 比较接近 |
| 3–5 Å | 存在明显差异，需要结合结构上下文判断 |
| > 5 Å | 差异较大，需要检查整体构象、局部结构和残基对应关系 |

这些范围主要用于帮助直观理解；结构长度、柔性、对齐区域和原子选择都会影响解释。

## 2. 对你的结果怎么判断？

<box border radius="xl" padding={4} gap={3}>
  <row align="center" justify="between">
    **受体 RMSD**
    <title size="lg" color="default">4.498 Å</title>
  </row>
  <box background="surface-secondary" radius="full" height="8px" clip>
    <box background="#D97757" height="8px" radius="full" width="90%" />
  </box>
  <text color="secondary" size="sm">全受体对齐：差异较明显。GLP-1R 的跨膜区、胞外区和柔性区域可能贡献不同，不能据此断定所有区域预测都不好。</text>
  <divider color="subtle" />
  <row align="center" justify="between">
    **肽链结合姿势 RMSD**
    <title size="lg" color="default">3.242 Å</title>
  </row>
  <box background="surface-secondary" radius="full" height="8px" clip>
    <box background="#D97757" height="8px" radius="full" width="65%" />
  </box>
  <text color="secondary" size="sm">受体对齐后：存在一定姿势偏差，尚不能视为高度吻合。需要结合局部受体对齐和结合界面接触进一步判断。</text>
</box>

## 3. 你的项目应该采用什么标准？

对于 GLP-1R–肽类复合物，我建议分别记录：

- **全受体 RMSD**：评价整体结构相似性。
- **结合口袋局部 RMSD**：评价结合区域的结构是否吻合。
- **受体对齐后的肽链 Cα RMSD**：评价结合姿势是否吻合。

其中，肽链结合姿势 RMSD 可以先把 **2 Å 左右或更低**作为“较接近”的探索性参考，而不是未经验证的成功阈值；3.242 Å 说明当前参考预测与实验姿势存在值得检查的偏差。

最重要的是，后续 27 个候选物必须使用**一致的残基映射、对齐方法和 RMSD 定义**。而且，参考预测与实验结构之间的 RMSD 不能直接当作候选物是否能结合的判据。

---

# you asked

message time: 2026-10-22 20:47:06

你是说可以直接比较7KI0实验结构，那就直接拿27条序列先跑完再说，跑完再分析结果什么的

---

# chatgpt response

对，我建议**先把 27 条 GLP-1R 候选序列全部跑完，再统一分析结果**。不过要区分两件事：

- **7KI0 实验结构**：作为已知的 GLP-1R–司美格鲁肽复合物参考，用来建立结构比较基准。
- **27 条候选序列**：先统一完成 Boltz-2 复合物预测，再用同一套指标筛选和比较。

这样比跑几条就临时改变筛选标准更合理，也更方便做横向比较。

## 建议的执行顺序

<box border radius="lg" padding={3} gap={3}>
  <row align="start" gap={3}>
    <box background="surface-secondary" radius="md" size="36px" align="center" justify="center">
      <title size="lg">1</title>
    </box>
    <box flex="1" gap={1}>
      **先跑完 27 条候选序列**

      <text color="secondary" size="sm">统一预测条件，保留每条序列的 3 次采样结果和置信度指标。你目前已有的 81 个样本汇总可以作为起点，不必重复运行已经成功完成的任务。</text>
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <box background="surface-secondary" radius="md" size="36px" align="center" justify="center">
      <title size="lg">2</title>
    </box>
    <box flex="1" gap={1}>
      **统一分析 27 条序列**

      <text color="secondary" size="sm">比较 ipTM、界面误差、结构置信度及多次采样的一致性。先看整体分布和稳定性，不急着认定最高分就是最佳候选。</text>
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <box background="surface-secondary" radius="md" size="36px" align="center" justify="center">
      <title size="lg">3</title>
    </box>
    <box flex="1" gap={1}>
      **再和 7KI0 实验结构比较**

      <text color="secondary" size="sm">重点分析结合口袋局部结构、肽链结合姿势、关键接触和相互作用几何，而不只比较整个受体的 RMSD。</text>
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <box background="surface-secondary" radius="md" size="36px" align="center" justify="center">
      <title size="lg">4</title>
    </box>
    <box flex="1" gap={1}>
      **综合排序，挑出少量候选**

      <text color="secondary" size="sm">结合预测置信度、重复采样一致性、口袋匹配和界面合理性，选出值得进一步研究的候选；不把计算结果直接等同于真实结合能力。</text>
    </box>
  </row>
</box>

有一个关键细节：**不要要求 27 条候选都复现司美格鲁肽的结合姿势。** 7KI0 可以作为受体结构和已知配体结合区域的参考；如果候选设计目标是其他表位，那么肽链姿势 RMSD 就不能直接拿来判定好坏。

所以目前最稳妥的做法就是：**先完成预测、固定结果文件，再统一评估。** 你已有的 81 个样本若已全部成功，就直接进入分析，不必重跑。

等预测结果齐全后，我们再按实际数据一步一步做，不预先设定未经验证的阈值。

---

# you asked

message time: 2026-10-22 20:48:08

给我写脚本吧

---

# chatgpt response

我先给你一份**第一阶段结果审计脚本**：不重新跑 Boltz-2，而是读取已经生成的结果，检查 27 条候选、每条 3 次采样是否齐全，并按候选汇总已有指标。

这一步先确认数据完整、找出异常候选；之后再做 7KI0 的结合口袋和界面结构比较。这样不会把“预测分数高”和“结构上合理”混成同一个结论。

## 1. 创建脚本

在 WSL Ubuntu 终端执行：

`
把下面的**完整代码**复制进去。

<CodeBlock language="python" editable>
#!/usr/bin/env python3
"""Audit existing GLP-1R Boltz-2 sample metrics without rerunning predictions."""

from pathlib import Path
import sys
import pandas as pd

ROOT = Path("LOCAL_PATH")
SAMPLE_CSV = ROOT / "boltz_sample_metrics.csv"
SUMMARY_CSV = ROOT / "boltz_candidate_summary.csv"
OUT_DIR = ROOT / "audit"

EXPECTED_CANDIDATES = 27
EXPECTED_SAMPLES_PER_CANDIDATE = 3


def find_candidate_column(df):
    """Choose a likely candidate/design identifier column."""
    cols = list(df.columns)

    preferred = [
        "candidate_id", "candidate", "candidate_name",
        "design_id", "design", "binder_id", "name"
    ]
    lower_to_original = {str(c).lower().strip(): c for c in cols}

    for name in preferred:
        if name in lower_to_original:
            return lower_to_original[name]

    for c in cols:
        name = str(c).lower()
        if any(word in name for word in ("candidate", "design", "binder")):
            return c

    return None


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if not SAMPLE_CSV.exists():
        print(f"[ERROR] Sample metrics CSV not founLOCAL_PATH")
        sys.exit(1)

    df = pd.read_csv(SAMPLE_CSV)

    print("=" * 72)
    print("GLP-1R BOLTZ-2 RESULTS AUDIT")
    print("=" * 72)
    print(f"Input file: {SAMPLE_CSV}")
    print(f"Rows (samples): {len(df)}")
    print(f"Columns: {list(df.columns)}")

    if df.empty:
        print("[ERROR] Sample metrics CSV is empty.")
        sys.exit(1)

    candidate_col = find_candidate_column(df)
    if candidate_col is None:
        print(
            "\n[ERROR] Cannot identify the candidate ID column automatically."
            "\nPlease inspect the printed column names and tell me which one "
            "identifies each candidate."
        )
        sys.exit(2)

    df[candidate_col] = df[candidate_col].astype(str).str.strip()
    df = df[df[candidate_col].notna() & (df[candidate_col] != "")].copy()

    # Identify numeric metric columns while excluding likely index columns.
    numeric_cols = []
    for col in df.columns:
        if col == candidate_col:
            continue
        converted = pd.to_numeric(df[col], errors="coerce")
        if converted.notna().any():
            df[col] = converted
            numeric_cols.append(col)

    counts = (
        df.groupby(candidate_col, dropna=False)
        .size()
        .rename("sample_count")
        .reset_index()
        .rename(columns={candidate_col: "candidate"})
    )
    counts["expected_samples"] = EXPECTED_SAMPLES_PER_CANDIDATE
    counts["count_status"] = counts["sample_count"].apply(
        lambda n: "OK" if n == EXPECTED_SAMPLES_PER_CANDIDATE
        else "CHECK"
    )
    counts.to_csv(OUT_DIR / "sample_count_audit.csv", index=False)

    print(f"\nCandidate ID column: {candidate_col}")
    print(f"Unique candidates: {df[candidate_col].nunique()}")
    print(f"Expected candidates: {EXPECTED_CANDIDATES}")
    print(f"Expected total samples: "
          f"{EXPECTED_CANDIDATES * EXPECTED_SAMPLES_PER_CANDIDATE}")

    if len(df) != EXPECTED_CANDIDATES * EXPECTED_SAMPLES_PER_CANDIDATE:
        print("[WARNING] Total sample count differs from expected 81.")
    else:
        print("[OK] Total sample row count is 81.")

    if df[candidate_col].nunique() != EXPECTED_CANDIDATES:
        print("[WARNING] Unique candidate count differs from expected 27.")
    else:
        print("[OK] Unique candidate count is 27.")

    irregular = counts[counts["count_status"] != "OK"]
    if irregular.empty:
        print("[OK] Every candidate has exactly 3 metric rows.")
    else:
        print("\n[WARNING] Candidates with unexpected sample counts:")
        print(irregular.to_string(index=False))

    # Summarize each numeric metric across the available samples.
    if numeric_cols:
        grouped = df.groupby(candidate_col)[numeric_cols]
        medians = grouped.median().add_suffix("_median")
        means = grouped.mean().add_suffix("_mean")
        stds = grouped.std().add_suffix("_std")
        summary = pd.concat([medians, means, stds], axis=1).reset_index()
        summary = summary.rename(columns={candidate_col: "candidate"})

        summary = summary.merge(
            counts[["candidate", "sample_count", "count_status"]],
            on="candidate",
            how="left",
        )

        # Put ipTM-related columns first for easier review.
        priority = [
            c for c in summary.columns
            if "iptm" in c.lower() and c.endswith("_median")
        ]
        remaining = [c for c in summary.columns if c not in priority]
        summary = summary[["candidate"] + priority + [
            c for c in remaining if c != "candidate"
        ]]

        summary.to_csv(
            OUT_DIR / "candidate_metric_summary.csv", index=False
        )

        # Produce rankings only for metrics whose names clearly identify them.
        rank_cols = [
            c for c in summary.columns
            if c.endswith("_median")
            and any(k in c.lower() for k in ("iptm", "plddt", "ipde", "pae"))
        ]

        for col in rank_cols:
            # Higher is generally preferred for ipTM/pLDDT;
            # lower is generally preferred for PAE/IPDE.
            metric = col.lower()
            ascending = any(k in metric for k in ("ipde", "pae"))
            ranked = summary.sort_values(
                col, ascending=ascending, na_position="last"
            )
            ranked[["candidate", col, "sample_count"]].to_csv(
                OUT_DIR / f"rank_{col}.csv", index=False
            )

        print("\nAvailable numeric metrics:")
        for col in numeric_cols:
            print(f"  - {col}")

        print("\nCandidate median summary (first 10 rows):")
        print(summary.head(10).to_string(index=False))
    else:
        print("[WARNING] No numeric metric columns were detected.")

    if SUMMARY_CSV.exists():
        candidate_summary = pd.read_csv(SUMMARY_CSV)
        print(f"\nExisting candidate summary found: {SUMMARY_CSV}")
        print(f"Rows: {len(candidate_summary)}")
        print(f"Columns: {list(candidate_summary.columns)}")
    else:
        print(f"\n[WARNING] Existing summary CSV not found: {SUMMARY_CSV}")

    print("\nOutput directory:")
    print(OUT_DIR)
    print("\nAudit complete. No predictions were launched or modified.")


if __name__ == "__main__":
    main()
</CodeBlock>

保存并退出 nano：按 tz python ~/audit_glp1r_results.py
```

脚本只读d/PRP/GLP1R_Boltz2_20261022/audit/
```

主要文件：

- `sample_count_audit.csv`：每条候选有几次采样，检查是否都是 3 次。
- `candidate_metric_summary.csv`：每条候选各项数值指标的中位数、均值和标准差。
- `rank_*.csv`：按识别到的指标生成排序表，供初步检查。

**注意：** 脚本中的排序只是初步整理，不代表已经确定了最佳候选；不同指标的含义不同，不能简单合成一个总分。

## 3. 把运行结果发给我

运行后，把终端中从 `GLP-1R BOLTZ-2 RESULTS AUDIT` 开始的输出贴给我。如果出现错误，也把完整报错贴出来。

我们先确认 27 条候选的数据是否完整，再编写下一步的**7KI0 结构对照分析脚本**，计算受体局部结构差异、候选与结合口袋的接触情况等。这样可以避免在文件路径或链识别不正确时直接批量计算 RMSD。

---

# you asked

message time: 2026-10-22 20:50:03

Output directory:
LOCAL_PATH

Audit complete. No predictions were launched or modified.
(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

很好，脚本已经运行到结束，没有启动新的预测任务。接下来我们先检查审计结果，确认 27 条候选的数据是否完整。

在你现在这个终端里，直接复制执行下面的命令：



然后再执行：



把这两段输出发给我。

我们主要确认三件事：

1. 是否确实有 **27 条候选、81 个样本记录**。
2. 是否每条候选都有 3 次采样，是否存在缺失或异常。
3. 汇总表中实际有哪些指标、列名是什么，以便下一步准确编写结构分析脚本。

目前先不重跑 Boltz-2，也不急着按最高分挑候选。等数据审计通过后，我们再用 7KI0 实验结构进行统一的结构比较。

---

# you asked

message time: 2026-10-22 20:50:36

(usalign) ziguimu@DESKTOP-8RLFC97:~$ head -n 12 LOCAL_PATH
candidate,iptm_median,protein_iptm_median,cif_exists_median,confidence_score_median,ptm_median,complex_plddt_median,complex_iplddt_median,complex_pde_median,complex_ipde_median,cif_exists_mean,confidence_score_mean,ptm_mean,iptm_mean,complex_plddt_mean,complex_iplddt_mean,complex_pde_mean,complex_ipde_mean,protein_iptm_mean,cif_exists_std,confidence_score_std,ptm_std,iptm_std,complex_plddt_std,complex_iplddt_std,complex_pde_std,complex_ipde_std,protein_iptm_std,sample_count,count_status
candidate_0009,0.9421537518501282,0.9421537518501282,1.0,0.8054794669151306,0.9141185879707336,0.7831346392631531,0.6923075318336487,0.4475336074829101,0.9904541373252868,1.0,0.8086418310801188,0.8925816615422567,0.9227908452351888,0.7801045775413513,0.6859683791796366,0.5059779286384583,1.3680514693260193,0.9227908452351888,0.0,0.00676445811601757,0.043491729056501525,0.04007074945653068,0.009452316980841416,0.022424086387261392,0.11149644733499706,0.7730053648598253,0.04007074945653068,3,OK
candidate_0021,0.9276280403137208,0.9276280403137208,1.0,0.818586528301239,0.903486967086792,0.7874195575714111,0.7053772211074829,0.4700676202774048,1.1253453493118286,1.0,0.8112588922182719,0.8804208238919576,0.9107392231623331,0.7863888343175253,0.6991789142290751,0.5325862665971121,1.6037742694218953,0.9107392231623331,0.0,0.013097781819425296,0.04186096939267367,0.04569544520457249,0.005525332427025073,0.018839997823753746,0.1182635714150663,0.840268893123279,0.04569544520457249,3,OK
candidate_0027,0.9026992321014404,0.9026992321014404,1.0,0.8025517463684082,0.8721227645874023,0.7732104659080505,0.6881315112113953,0.5602403283119202,1.7394684553146362,1.0,0.8031350175539652,0.8672728141148885,0.8956605792045593,0.7800036470095316,0.6892358660697937,0.5704347093900045,1.7808534304300945,0.8956605792045593,0.0,0.016218215599752152,0.014604376781396334,0.02843680226662526,0.016552012895912554,0.01924603753636701,0.047030812625382334,0.22259505478198816,0.02843680226662526,3,OK
candidate_0043,0.9365798830986024,0.9365798830986024,1.0,0.8221049308776855,0.90617036819458,0.7934862375259399,0.7175155878067017,0.4739682376384735,0.9803325533866882,1.0,0.8221981128056844,0.9092131853103638,0.9408145944277445,0.7925439874331156,0.7171916166941324,0.4684443672498067,0.9452253182729086,0.9408145944277445,0.0,0.006171158105749988,0.008282913821166811,0.007923604657947681,0.009504276453542952,0.007285813479794963,0.019511095536178687,0.14373211776311987,0.007923604657947681,3,OK
candidate_0044,0.9449160695075988,0.9449160695075988,1.0,0.828863799571991,0.9086591601371764,0.7998507022857666,0.7367702126502991,0.4741176962852478,0.9720885157585144,1.0,0.8309946060180664,0.911031166712443,0.9457763830820718,0.8022991418838501,0.73508620262146,0.45829280217488605,0.9184543490409851,0.9457763830820718,0.0,0.00619316590828659,0.007838245320875537,0.005517503216310044,0.006385394731454074,0.009941868761543364,0.034999736483247904,0.1372713911140875,0.005517503216310044,3,OK
candidate_0046,0.9461883306503296,0.9461883306503296,1.0,0.8283692598342896,0.9001218676567078,0.7983352541923523,0.7155305743217468,0.4979993999004364,1.1844309568405151,1.0,0.8236392537752787,0.8870114088058472,0.9386477669080099,0.794887125492096,0.7152626713116964,0.5309320092201233,1.3918461004892986,0.9386477669080099,0.0,0.013487866875947222,0.03418760246648802,0.015111702807897814,0.01328606208502175,0.01502186425600998,0.11358082079370954,0.5873920956697372,0.015111702807897814,3,OK
candidate_0051,0.9320017099380492,0.9320017099380492,1.0,0.7969805002212524,0.903882086277008,0.7709140181541443,0.6793193817138672,0.4824738502502441,1.0938258171081543,1.0,0.7916167577107748,0.8787453174591064,0.8827941616376241,0.7688223719596863,0.6762834787368774,0.569311519463857,1.9742784698804219,0.8827941616376241,0.0,0.01694084373784593,0.0737650019082466,0.09444631990219099,0.004898630113107279,0.008457278272716303,0.2270517392684699,1.8217626388911474,0.09444631990219099,3,OK
candidate_0062,0.9331403374671936,0.9331403374671936,1.0,0.829677402973175,0.8921869993209839,0.8038116097450256,0.7266930937767029,0.5217379927635193,1.3425897359848022,1.0,0.8254908919334412,0.8836835424105326,0.9294301271438599,0.7995060880978903,0.7249184250831604,0.5400725404421488,1.4394334554672241,0.9294301271438599,0.0,0.010015452674675587,0.033515864713382845,0.01765174880708591,0.008224773495941671,0.012402463950781028,0.09620188826413613,0.5987176754971337,0.01765174880708591,3,OK
candidate_0071,0.927364945411682,0.927364945411682,1.0,0.8267480731010437,0.8695153594017029,0.8016036748886108,0.7343015670776367,0.5823618769645691,1.9151084423065183,1.0,0.8291969299316406,0.8698781331380209,0.9278428355852762,0.8045354882876078,0.738745113213857,0.5806340376536051,1.8049542903900146,0.9278428355852762,0.0,0.013383125575343406,0.0069587555784784766,0.0008618662759909821,0.016529598173144144,0.02270734728470726,0.015468336421895332,0.19535735812043356,0.0008618662759909821,3,OK
candidate_0081,0.931252121925354,0.931252121925354,1.0,0.7958559989929199,0.9071314930915833,0.7620069980621338,0.6643304228782654,0.4832918345928192,1.3592288494110107,1.0,0.794138491153717,0.8815853993097941,0.9223595857620239,0.7620832324028015,0.6626920302708944,0.5539346436659495,1.820088227589925,0.9223595857620239,0.0,0.008261174535243778,0.047893704538700385,0.024367792060594785,0.004378488735999636,0.003724104177632863,0.13303245908123096,0.997669122137699,0.024367792060594785,3,OK
candidate_0082,0.951367735862732,0.951367735862732,1.0,0.8421603441238403,0.9261606335639954,0.8149946331977844,0.7646833062171936,0.4207987189292907,0.7350986003875732,1.0,0.8428170879681905,0.9250857830047607,0.9534920255343119,0.8151483337084452,0.7638869881629944,0.4180659850438435,0.7191597620646158,0.9534920255343119,0.0,0.0014451816491432897,0.004334462459853739,0.00415989010498818,0.002528894712887901,0.002533955785885395,0.010035439232271473,0.06469949988916895,0.00415989010498818,3,OK
(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

从你贴出的结果看，汇总表已经成功生成，而且每条候选显示 `sample_count=3`、`count_status=OK`。不过你目前只贴了前 11 条，**还不能仅凭这段确认全部 27 条都齐全**。

先说一个值得注意的初步结果：候选 `candidate_0082` 的 `iptm_median` 为 **0.9514**，`complex_ipde_median` 为 **0.7351**；候选 `candidate_0046` 的对应值分别为 **0.9462** 和 **1.1844**。这些是预测指标，暂时不能据此断定谁的真实结合能力更强。

## 下一步：确认全部候选，再进入结构分析

请在终端执行这条命令：



把完整输出发给我。

**确认数据完整后，我们就开始写 7KI0 对照脚本。** 结构分析会重点比较 GLP-1R 结合口袋、候选肽链的空间位置与界面接触；不会简单要求所有候选都复现司美格鲁肽的结合姿势，也不会把 RMSD 或 ipTM 单独当成成功判据。

---

# you asked

message time: 2026-10-22 20:54:32

import pandas as pd

p = "LOCAL_PATH"
df = pd.read_csv(p)

print("候选数量：", df["candidate"].nunique())
print("样本记录总数：", df["sample_count"].sum())
print("每条候选都是3次采样：", bool((df["sample_count"] == 3).all()))
print("异常候选：")
print(df.loc[df["count_status"] != "OK", ["candidate", "sample_count", "count_status"]].to_string(index=False))

print("\n按 ipTM 中位数初步排序的前10条：")
print(
    df.sort_values("iptm_median", ascending=False)[
        ["candidate", "iptm_median", "complex_ipde_median", "complex_iplddt_median", "sample_count"]
    ].head(10).to_string(index=False)
)
PY
Command 'python' not found, did you mean:
  command 'python3' from deb python3
  command 'python' from deb python-is-python3
(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

这是因为你当前激活的是 `usalign` 环境，其中 `python` 命令没有配置好。先不用切换环境，直接使用 `python3` 运行即可。

不过你刚才粘贴的代码需要通过 heredoc 一起执行。请把下面**整段命令**复制到终端：



注意：第一行必须是 `python3 - <<'PY'`，最后一行必须是单独的 `PY`。

运行后把输出发给我，我们就继续下一步：将候选结构与 7KI0 实验结构进行对照分析。

---

# you asked

message time: 2026-10-22 20:54:53

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'pandas'
(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

没关系，这是因为 `usalign` 环境没有安装 `pandas`。**不用安装，也不用切换环境**，我们直接用 Python 标准库读取 CSV 就可以了。

请在终端复制执行下面这整段命令：



这次不依赖 `pandas`，也不会修改任何文件。

把输出贴给我。确认数据完整后，我们就继续写 **7KI0 实验结构对照分析脚本**，不再在环境配置上浪费时间。

---

# you asked

message time: 2026-10-22 20:55:20

候选数量： 27
样本记录总数： 81
每条候选都是3次采样： True

异常候选：
无

按 ipTM 中位数排序的前10条：
候选                      ipTM中位数      ipDE中位数       ipLDDT中位数      样本数
candidate_0096           0.9533       0.7730          0.7264        3
candidate_0082           0.9514       0.7351          0.7647        3
candidate_0129           0.9480       0.9675          0.7067        3
candidate_0046           0.9462       1.1844          0.7155        3
candidate_0044           0.9449       0.9721          0.7368        3
candidate_0200           0.9442       0.8410          0.7479        3
candidate_0170           0.9430       0.9340          0.7610        3
candidate_0009           0.9422       0.9905          0.6923        3
candidate_0112           0.9421       0.9390          0.7324        3
candidate_0227           0.9397       1.5438          0.7278        3
(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

很好，数据审计通过了：**27 条候选、81 个样本、每条 3 次采样，没有发现采样数量异常。** 现在可以进入结构分析阶段，不需要重跑 Boltz-2。

从初步排序看：

- `candidate_0096` 的 ipTM 中位数最高，为 **0.9533**。
- `candidate_0082` 的 ipTM 为 **0.9514**，同时这十条中 ipDE 中位数最低，为 **0.7351**。
- `candidate_0096` 的 ipLDDT 中位数为 **0.7264**，低于 `candidate_0082` 的 **0.7647**。

因此，目前还不能只按 ipTM 排名决定谁最好。下一步应该检查候选在结构上的结合位置、界面接触与预测姿势是否合理。

## 下一步：确认 7KI0 与 27 条候选的结构文件位置

在正式计算前，我们先确认候选结构文件的实际目录，避免脚本误读其他模型。请在终端执行下面这条命令：



再执行：



把两段输出发给我。我会据此给你一份完整的结构分析脚本，目标是：

1. 自动识别预测结构中的 GLP-1R 受体链和候选结合链。
2. 将预测受体与 7KI0 受体对齐，计算全局及结合口袋局部 RMSD。
3. 分析候选与受体的界面接触，以及候选是否占据司美格鲁肽参考结合区域。
4. 汇总 27 条候选的结构指标，供后续综合筛选。

这里有个重要原则：**司美格鲁肽是参考配体，不是所有候选都必须模仿的标准答案。** 如果某条候选采用不同结合位点，我们会将其与参考位点的关系单独报告，而不是直接判为失败。

---

# you asked

message time: 2026-10-22 20:56:22

LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
(usalign) ziguimu@DESKTOP-8RLFC97:~$ ls -lh LOCAL_PATH
-rwxrwxrwx 1 ziguimu ziguimu 972K Oct 19 11:14 LOCAL_PATH
(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

路径已经确认，7KI0 实验结构文件存在，27 条候选的 Boltz-2 模型也采用了统一的目录结构。下一步可以直接开始结构分析。

我会先采用比较稳妥的策略：对每条候选的 3 个预测模型分别分析，再汇总结果；用 7KI0 的 GLP-1R 受体链作为结构参照，并用实验结构中的司美格鲁肽位置定义参考结合区域。这样既能比较候选的结合位置，也不会误把不同结合姿势直接判成失败。

## 结构分析脚本

先计算三个层面的结果：

- **受体对齐质量**：预测的 GLP-1R 与 7KI0 的整体 RMSD、参考结合口袋局部 RMSD。
- **界面接触**：候选与受体之间的原子接触数、残基接触数、最小距离，以及过近接触的数量。
- **参考配体位置关系**：候选是否靠近 7KI0 中司美格鲁肽占据的区域。

这会分析每条候选的 3 个模型，预计最多处理 81 个结构。RMSD 和接触数都会作为独立指标输出，不会人为加权成一个未经校准的“总分”。

### 1. 创建脚本

在终端执行：

`
把下面的完整代码复制进去。

<CodeBlock language="python" editable>
#!/usr/bin/env python3
"""Compare existing GLP-1R candidate models with experimental structure 7KI0."""

from pathlib import Path
import csv
import re
import statistics
import sys
import warnings

import numpy as np
from Bio.PDB import MMCIFParser, Superimposer
from Bio.PDB.Polypeptide import is_aa
from Bio.SeqUtils import seq1
from Bio.Align import PairwiseAligner

ROOT = Path("LOCAL_PATH")
REFERENCE = Path("LOCAL_PATH")
OUT = ROOT / "audit" / "structure"

# 7KI0 chain IDs established from the existing structure inspection.
REFERENCE_RECEPTOR_CHAIN = "R"
REFERENCE_PEPTIDE_CHAIN = "P"

CONTACT_CUTOFF = 5.0
CLASH_CUTOFF = 2.0
POCKET_CUTOFF = 8.0

parser = MMCIFParser(QUIET=True)

aligner = PairwiseAligner()
aligner.mode = "local"
aligner.match_score = 2.0
aligner.mismatch_score = -1.0
aligner.open_gap_score = -5.0
aligner.extend_gap_score = -0.5

METRICS = [
    "receptor_global_rmsd_A",
    "receptor_pocket_rmsd_A",
    "receptor_alignment_pairs",
    "interface_atom_pairs_lt5A",
    "interface_residue_pairs_lt5A",
    "binder_residues_contacting_receptor",
    "binder_receptor_min_distance_A",
    "clash_atom_pairs_lt2A",
    "binder_atom_pairs_lt5A_from_reference_peptide",
    "binder_residues_near_reference_peptide",
]


def protein_residues(chain):
    """Amino-acid residues with CA atoms, preserving chain order."""
    return [
        r for r in chain
        if is_aa(r, standard=False) and "CA" in r
    ]


def residue_sequence(residues):
    chars = []
    for r in residues:
        try:
            chars.append(seq1(r.resname, custom_map={"MSE": "M"}))
        except Exception:
            chars.append("X")
    return "".join(chars)


def heavy_atoms(residues):
    """Return heavy-atom coordinates and their residue indices."""
    coords, residue_indices = [], []

    for ri, residue in enumerate(residues):
        for atom in residue.get_atoms():
            element = (atom.element or "").strip().upper()
            if element in {"H", "D"}:
                continue

            # If the element field is absent, fall back to atom name.
            if not element:
                name = atom.get_name().strip().upper()
                if name.startswith(("H", "D")):
                    continue

            coords.append(atom.coord.astype(float))
            residue_indices.append(ri)

    if not coords:
        return np.empty((0, 3)), np.empty((0,), dtype=int)

    return np.asarray(coords), np.asarray(residue_indices, dtype=int)


def align_residue_indices(reference_residues, predicted_residues):
    """Sequence-align chains and return exact-identity residue index pairs."""
    ref_seq = residue_sequence(reference_residues)
    pred_seq = residue_sequence(predicted_residues)

    if not ref_seq or not pred_seq:
        return [], float("-inf")

    alignment = aligner.align(ref_seq, pred_seq)[0]
    pairs = []

    # Only retain positions with identical amino-acid identities.
    for ref_block, pred_block in zip(*alignment.aligned):
        for ri, pi in zip(
            range(int(ref_block[0]), int(ref_block[1])),
            range(int(pred_block[0]), int(pred_block[1])),
        ):
            if ref_seq[ri] == pred_seq[pi]:
                pairs.append((ri, pi))

    return pairs, float(alignment.score)


def choose_receptor_chain(model, reference_sequence):
    """Find the candidate chain most similar to the GLP-1R receptor."""
    candidates = []

    for chain in model:
        residues = protein_residues(chain)
        seq = residue_sequence(residues)

        # The receptor is much longer than the designed peptide.
        if len(seq) < 100:
            continue

        alignment = aligner.align(reference_sequence, seq)[0]
        candidates.append(
            (float(alignment.score), chain, residues, seq)
        )

    if not candidates:
        raise ValueError("No protein chain of at least 100 residues found.")

    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1], candidates[0][2], candidates[0][3]


def pair_distance_metrics(coords_a, res_a, coords_b, res_b):
    """Contact counts, residue-pair counts, and minimum distance."""
    if len(coords_a) == 0 or len(coords_b) == 0:
        return 0, 0, float("nan"), 0

    # These are per-model calculations; no full trajectory is stored.
    delta = coords_a[:, None, :] - coords_b[None, :, :]
    distances = np.sqrt(np.sum(delta * delta, axis=2))

    contact_mask = distances < CONTACT_CUTOFF
    clash_count = int(np.count_nonzero(distances < CLASH_CUTOFF))
    atom_pair_count = int(np.count_nonzero(contact_mask))

    atom_i, atom_j = np.where(contact_mask)
    residue_pairs = {
        (int(res_a[i]), int(res_b[j]))
        for i, j in zip(atom_i, atom_j)
    }

    return (
        atom_pair_count,
        len(residue_pairs),
        float(np.min(distances)),
        clash_count,
    )


def count_binder_residues_near_reference(
    binder_coords, binder_residue_indices, reference_coords
):
    if len(binder_coords) == 0 or len(reference_coords) == 0:
        return 0, 0

    delta = binder_coords[:, None, :] - reference_coords[None, :, :]
    distances = np.sqrt(np.sum(delta * delta, axis=2))
    mask = distances < CONTACT_CUTOFF

    atom_pairs = int(np.count_nonzero(mask))
    atom_indices = np.where(mask)[0]
    contacting_residues = {
        int(binder_residue_indices[i]) for i in atom_indices
    }

    return atom_pairs, len(contacting_residues)


def rmsd_from_coords(fixed_coords, moving_coords):
    if len(fixed_coords) == 0:
        return float("nan")

    delta = fixed_coords - moving_coords
    return float(np.sqrt(np.mean(np.sum(delta * delta, axis=1))))


def load_reference():
    if not REFERENCE.exists():
        raise FileNotFoundError(f"Reference CIF not found: {REFERENCE}")

    structure = parser.get_structure("7KI0", str(REFERENCE))
    model = structure[0]

    if REFERENCE_RECEPTOR_CHAIN not in model:
        raise ValueError(
            f"7KI0 receptor chain {REFERENCE_RECEPTOR_CHAIN!r} not found. "
            f"Available chains: {[c.id for c in model]}"
        )

    if REFERENCE_PEPTIDE_CHAIN not in model:
        raise ValueError(
            f"7KI0 peptide chain {REFERENCE_PEPTIDE_CHAIN!r} not found. "
            f"Available chains: {[c.id for c in model]}"
        )

    ref_rec = protein_residues(model[REFERENCE_RECEPTOR_CHAIN])
    ref_pep = protein_residues(model[REFERENCE_PEPTIDE_CHAIN])

    if not ref_rec or not ref_pep:
        raise ValueError("Could not extract reference receptor or peptide.")

    ref_rec_coords, ref_rec_residx = heavy_atoms(ref_rec)
    ref_pep_coords, _ = heavy_atoms(ref_pep)

    # Reference pocket: receptor CA atoms within 8 A of the reference peptide.
    pocket_indices = set()
    for ri, residue in enumerate(ref_rec):
        ca = residue["CA"].coord.astype(float)
        if len(ref_pep_coords):
            d = np.linalg.norm(ref_pep_coords - ca, axis=1)
            if float(np.min(d)) < POCKET_CUTOFF:
                pocket_indices.add(ri)

    return (
        ref_rec, ref_pep, ref_rec_coords, ref_rec_residx,
        ref_pep_coords, pocket_indices,
    )


def analyze_model(
    path, candidate, model_number, reference_data, reference_sequence
):
    (
        ref_rec, ref_pep, ref_rec_heavy, ref_rec_heavy_residx,
        ref_pep_heavy, pocket_indices,
    ) = reference_data

    row = {
        "candidate": candidate,
        "model": model_number,
        "file": str(path),
        "status": "OK",
        "receptor_chain": "",
        "binder_chain": "",
        "receptor_alignment_pairs": 0,
    }

    try:
        structure = parser.get_structure(
            f"{candidate}_{model_number}", str(path)
        )
        model = structure[0]

        pred_rec_chain, pred_rec, pred_seq = choose_receptor_chain(
            model, reference_sequence
        )
        row["receptor_chain"] = pred_rec_chain.id

        receptor_pairs, _ = align_residue_indices(ref_rec, pred_rec)
        row["receptor_alignment_pairs"] = len(receptor_pairs)

        if len(receptor_pairs) < 50:
            raise ValueError(
                f"Too few identical receptor alignment pairs: "
                f"{len(receptor_pairs)}"
            )

        other_chains = []
        for chain in model:
            if chain.id == pred_rec_chain.id:
                continue
            residues = protein_residues(chain)
            if residues:
                other_chains.append((len(residues), chain, residues))

        if not other_chains:
            raise ValueError("No second protein chain found for the binder.")

        other_chains.sort(key=lambda item: item[0], reverse=True)
        _, binder_chain, binder_residues = other_chains[0]
        row["binder_chain"] = binder_chain.id

        # Fit predicted receptor onto experimental receptor using identical
        # sequence-matched C-alpha atoms.
        fixed_atoms = [ref_rec[ri]["CA"] for ri, pi in receptor_pairs]
        moving_atoms = [pred_rec[pi]["CA"] for ri, pi in receptor_pairs]

        superimposer = Superimposer()
        superimposer.set_atoms(fixed_atoms, moving_atoms)
        rotation, translation = superimposer.rotran
        row["receptor_global_rmsd_A"] = float(superimposer.rms)

        pred_ca = np.asarray([r["CA"].coord for r in pred_rec], dtype=float)
        transformed_ca = pred_ca @ rotation + translation
        ref_ca = np.asarray([r["CA"].coord for r in ref_rec], dtype=float)

        local_pairs = [
            (ri, pi) for ri, pi in receptor_pairs
            if ri in pocket_indices
        ]
        if local_pairs:
            row["receptor_pocket_rmsd_A"] = rmsd_from_coords(
                np.asarray([ref_ca[ri] for ri, pi in local_pairs]),
                np.asarray([transformed_ca[pi] for ri, pi in local_pairs]),
            )
        else:
            row["receptor_pocket_rmsd_A"] = float("nan")

        binder_coords, binder_residx = heavy_atoms(binder_residues)
        binder_coords = binder_coords @ rotation + translation

        # Contacts are calculated against the experimental receptor in the
        # same coordinate frame, not against the independently fitted peptide.
        atom_pairs, residue_pairs, min_dist, clashes = pair_distance_metrics(
            ref_rec_heavy, ref_rec_heavy_residx,
            binder_coords, binder_residx,
        )

        row["interface_atom_pairs_lt5A"] = atom_pairs
        row["interface_residue_pairs_lt5A"] = residue_pairs
        row["binder_residues_contacting_receptor"] = len({
            pair[1] for pair in []  # filled below using direct residue analysis
        })
        row["binder_receptor_min_distance_A"] = min_dist
        row["clash_atom_pairs_lt2A"] = clashes

        # Number of unique binder residues making any receptor contact.
        if len(ref_rec_heavy) and len(binder_coords):
            delta = ref_rec_heavy[:, None, :] - binder_coords[None, :, :]
            distances = np.sqrt(np.sum(delta * delta, axis=2))
            i, j = np.where(distances < CONTACT_CUTOFF)
            row["binder_residues_contacting_receptor"] = len({
                int(binder_residx[k]) for k in j
            })

        ref_atom_pairs, ref_residue_count = (
            count_binder_residues_near_reference(
                binder_coords, binder_residx, ref_pep_heavy
            )
        )
        row["binder_atom_pairs_lt5A_from_reference_peptide"] = ref_atom_pairs
        row["binder_residues_near_reference_peptide"] = ref_residue_count

    except Exception as exc:
        row["status"] = f"ERROR: {type(exc).__name__}: {exc}"
        for metric in METRICS:
            row.setdefault(metric, float("nan"))

    return row


def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    print("=" * 72)
    print("GLP-1R STRUCTURAL COMPARISON AGAINST EXPERIMENTAL 7KI0")
    print("=" * 72)

    try:
        reference_data = load_reference()
    except Exception as exc:
        print(f"[ERROR] Cannot load reference structure: {exc}")
        sys.exit(1)

    ref_rec = reference_data[0]
    reference_sequence = residue_sequence(ref_rec)

    print(f"Reference: {REFERENCE}")
    print(f"Reference receptor residues with CA: {len(ref_rec)}")
    print(f"Reference peptide residues with CA: {len(reference_data[1])}")
    print(f"Reference pocket residues (CA within {POCKET_CUTOFF} A): "
          f"{len(reference_data[5])}")

    files = sorted(
        (ROOT / "predictions").glob(
            "candidate_*/boltz_results_*/predictions/"
            "candidate_*/*_model_*.cif"
        )
    )

    if not files:
        print("[ERROR] No candidate model CIF files found.")
        sys.exit(1)

    rows = []
    for idx, path in enumerate(files, start=1):
        match = re.search(r"_model_(\d+)\.cif$", path.name)
        model_number = int(match.group(1)) if match else -1
        candidate = path.parents[3].name

        print(f"[{idx}/{len(files)}] {candidate}, model {model_number} ...")
        row = analyze_model(
            path, candidate, model_number, reference_data, reference_sequence
        )
        rows.append(row)

        if row["status"] == "OK":
            print(
                f"    receptor RMSD={row['receptor_global_rmsd_A']:.2f} A; "
                f"pocket RMSD={row['receptor_pocket_rmsd_A']:.2f} A; "
                f"interface residue pairs={row['interface_residue_pairs_lt5A']}; "
                f"reference-peptide proximity pairs="
                f"{row['binder_atom_pairs_lt5A_from_reference_peptide']}"
            )
        else:
            print(f"    {row['status']}")

    per_model_path = OUT / "per_model_structure_metrics.csv"
    fields = [
        "candidate", "model", "file", "status", "receptor_chain",
        "binder_chain",
    ] + METRICS
    write_csv(per_model_path, rows, fields)

    # Candidate-level medians across successful models; retain model counts.
    candidate_ids = sorted({r["candidate"] for r in rows})
    summary_rows = []

    for candidate in candidate_ids:
        group = [r for r in rows if r["candidate"] == candidate]
        ok = [r for r in group if r["status"] == "OK"]

        summary = {
            "candidate": candidate,
            "models_found": len(group),
            "models_successful": len(ok),
            "models_failed": len(group) - len(ok),
        }

        for metric in METRICS:
            vals = []
            for r in ok:
                value = r.get(metric)
                try:
                    value = float(value)
                    if np.isfinite(value):
                        vals.append(value)
                except (TypeError, ValueError):
                    pass

            summary[metric + "_median"] = (
                statistics.median(vals) if vals else ""
            )

        summary_rows.append(summary)

    summary_fields = [
        "candidate", "models_found", "models_successful", "models_failed"
    ] + [m + "_median" for m in METRICS]

    summary_path = OUT / "candidate_structure_summary.csv"
    write_csv(summary_path, summary_rows, summary_fields)

    failures = [r for r in rows if r["status"] != "OK"]

    print("\n" + "=" * 72)
    print("STRUCTURE ANALYSIS COMPLETE")
    print("=" * 72)
    print(f"Model files found: {len(files)}")
    print(f"Successful analyses: {len(rows) - len(failures)}")
    print(f"Failed analyses: {len(failures)}")
    print(f"Per-model metrics: {per_model_path}")
    print(f"Candidate summary: {summary_path}")

    if failures:
        print("\nFailed models:")
        for row in failures:
            print(row["candidate"], row["model"], row["status"])

    print(
        "\nInterpretation caution: proximity to semaglutide marks spatial "
        "overlap with its reference site; it is not, by itself, a success "
        "or failure criterion. RMSD and contact counts are structural "
        "descriptors, not experimental affinity measurements."
    )


if __name__ == "__main__":
    main()
</CodeBlock>

保存：`Ctrl+O` → 回车 → `Ctrl+X`。

### 2. 运n boltz python ~/analyze_glp1r_structuresd/PRP/GLP1R_Boltz2_20261022/audit/structure/
```

会生成两个主要结果：

- `per_model_structure_metrics.csv`：每个模型单独的结构分析结果。
- `candidate_structure_summary.csv`：按候选汇总三个模型的中位数。

### 3. 运行后把结t/structure/candidate_structure_summary.csv
```

把输出贴过来，我们再结合 27 条候选的预测置信度与结构指标做综合分析。

**技术说明：** 这里的局部 RMSD 是对齐后、与 7KI0 司美格鲁肽结合口袋对应的受体 Cα RMSD；它衡量的是受体口袋构象差异，而不是候选肽本身的 RMSD。候选是否靠近参考配体位置则由单独的空间接触指标描述，两者不能混为一谈。

---

# you asked

message time: 2026-10-22 21:00:49

========================================================================
Model files found: 81
Successful analyses: 81
Failed analyses: 0
Per-model metrics: LOCAL_PATH
Candidate summary: LOCAL_PATH

Interpretation caution: proximity to semaglutide marks spatial overlap with its reference site; it is not, by itself, a success or failure criterion. RMSD and contact counts are structural descriptors, not experimental affinity measurements.
(usalign) ziguimu@DESKTOP-8RLFC97:~$ head -n 12 LOCAL_PATH
candidate,models_found,models_successful,models_failed,receptor_global_rmsd_A_median,receptor_pocket_rmsd_A_median,receptor_alignment_pairs_median,interface_atom_pairs_lt5A_median,interface_residue_pairs_lt5A_median,binder_residues_contacting_receptor_median,binder_receptor_min_distance_A_median,clash_atom_pairs_lt2A_median,binder_atom_pairs_lt5A_from_reference_peptide_median,binder_residues_near_reference_peptide_median
candidate_0009,3,3,0,5.707266470928612,5.575731381137091,384.0,1177.0,103.0,24.0,0.5000090643047383,48.0,2488.0,29.0
candidate_0021,3,3,0,5.6260547729385415,5.239149704000197,384.0,990.0,105.0,25.0,0.5962236196204733,40.0,2849.0,31.0
candidate_0027,3,3,0,5.1595746461630725,4.77760097450695,384.0,868.0,96.0,22.0,0.38607608737699667,41.0,3142.0,31.0
candidate_0043,3,3,0,4.818069616173092,4.416564536573919,384.0,767.0,95.0,25.0,0.9326762871066693,19.0,3639.0,31.0
candidate_0044,3,3,0,5.048231097517137,4.711279802788663,384.0,773.0,92.0,25.0,0.9038282610471772,30.0,3335.0,30.0
candidate_0046,3,3,0,5.326174101544267,5.012238258408645,384.0,708.0,88.0,24.0,0.6402435496520377,33.0,2777.0,28.0
candidate_0051,3,3,0,6.6666542148723,6.295619144968043,384.0,829.0,97.0,23.0,0.5683609984215243,30.0,1984.0,28.0
candidate_0062,3,3,0,5.609012848264251,5.237191022079719,384.0,762.0,89.0,22.0,0.4056858115242586,29.0,3057.0,29.0
candidate_0071,3,3,0,5.145478495411242,4.870585488684494,384.0,801.0,94.0,24.0,0.6140068477896498,33.0,3164.0,29.0
candidate_0081,3,3,0,8.588625359081444,8.592020836065537,384.0,1171.0,107.0,22.0,0.6123288755150654,47.0,1090.0,16.0
candidate_0082,3,3,0,4.458447863480184,3.8782460517470834,384.0,876.0,107.0,25.0,1.0097208490704794,35.0,4339.0,31.0
(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

很好，第一轮结构分析的 81 个模型全部成功处理，没有报错。现在已经有了两张可以用于后续分析的表：逐模型结果和候选汇总结果。

但我看到一个**需要先核查的重要问题**：`binder_receptor_min_distance_A_median` 里有不少值只有 0.4–1.0 Å，同时 `clash_atom_pairs_lt2A_median` 达到 19–48。若这些数值代表真实重原子距离，就意味着存在大量极近接触，不能直接把较大的界面接触数解释为结合更好。

另外，`binder_atom_pairs_lt5A_from_reference_peptide_median` 很大，甚至达到数千。这个值统计的是原子对，而不是独立的残基数；而且当前实现没有明确排除预测配体与参考司美格鲁肽之间的空间重叠。因此，**先不要依据这张表给 27 条候选排结构优劣名次**。

## 下一步该怎么做

我建议先修正结构比较方法，再做候选排序：

1. **先对齐结合口袋，而不只对齐整个受体。** 当前整体受体 RMSD 较大，用全受体对齐后的坐标直接评估配体与 7KI0 的相对位置，可能受到远离口袋区域的构象差异影响。
2. **重新计算局部界面指标。** 在结合口袋局部对齐后，计算候选与口袋的原子接触、残基接触、最小距离和小于 2 Å 的近距离原子对。
3. **检查司美格鲁肽参考位置的重叠。** 分别报告候选是否占据参考配体区域，不把重叠程度直接当作优劣分数。
4. **最后再综合 81 个模型的结果。** 结合三个采样的稳定性、ipTM、ipLDDT 和局部界面几何，挑出值得进一步检查的候选。

**目前的结论：** 81 个结构文件都能成功读取，但这不等于结构质量都合格。现有汇总表可以保留作为初步记录，暂时不要据此淘汰候选。下一版脚本应以结合口袋局部对齐为基础，重新计算界面相关指标。

---

# you asked

message time: 2026-10-22 21:01:48

继续算TM啊

---

# chatgpt response

好，继续算 **TM-score**。这次我们用已经安装的 US-align，直接比较 27 条候选的 Boltz-2 预测结构与 7KI0 实验结构。

这里需要区分两种结果：

- **受体 TM-score**：比较预测的 GLP-1R 与实验结构中的 GLP-1R，衡量整体结构相似性。
- **复合物 TM-score**：比较预测复合物与实验复合物，评估整体结构相似性。不过候选肽与司美格鲁肽序列不同，复合物 TM-score 会同时受受体和配体差异影响，不能单独用来判定结合姿势好坏。

因此，我们先计算受体 TM-score，再根据 US-align 的输出确认哪些结构比较是有效的。

我们把实验结构 7KI0 的受体链 R 放在 US-align 的第一个位置，候选预测结构中的 GLP-1R 链放在第二个位置。这样会输出两个归一化 TM-score，其中**按参考受体长度归一化的 TM-score**最适合用来横向比较这批候选。

注意：TM-score 衡量整体折叠相似性，不是亲和力，也不直接代表候选肽的结合姿势正确。

## 1. 创建 TM-score 计算脚本

在终端执行：

`
将下面的完整代码复制进去：

<CodeBlock language="python" editable>
#!/usr/bin/env python3
"""Calculate receptor TM-scores against experimental GLP-1R in 7KI0."""

from pathlib import Path
import csv
import re
import shutil
import subprocess
import tempfile

import numpy as np
from Bio.PDB import MMCIFParser, PDBIO, Select
from Bio.PDB.Polypeptide import is_aa
from Bio.SeqUtils import seq1
from Bio.Align import PairwiseAligner

ROOT = Path("LOCAL_PATH")
REFERENCE = Path("LOCAL_PATH")
OUTDIR = ROOT / "audit" / "structure"
OUTCSV = OUTDIR / "receptor_tmscore_vs_7KI0.csv"

REFERENCE_CHAIN = "R"

# Adjust this if the executable is installed elsewhere.
USALIGN_CANDIDATES = [
    shutil.which("USalign"),
    shutil.which("usalign"),
    "USER_HOME/miniconda3/envs/usalign/bin/USalign",
    "USER_HOME/miniconda3/envs/usalign/bin/usalign",
]

USALIGN = next(
    (p for p in USALIGN_CANDIDATES if p and Path(p).is_file()),
    None,
)

parser = MMCIFParser(QUIET=True)

aligner = PairwiseAligner()
aligner.mode = "local"
aligner.match_score = 2.0
aligner.mismatch_score = -1.0
aligner.open_gap_score = -5.0
aligner.extend_gap_score = -0.5


class ChainOnly(Select):
    def __init__(self, chain_id):
        self.chain_id = chain_id

    def accept_chain(self, chain):
        return chain.id == self.chain_id

    def accept_residue(self, residue):
        return is_aa(residue, standard=False)


def residues_and_sequence(chain):
    residues = [
        r for r in chain
        if is_aa(r, standard=False) and "CA" in r
    ]
    sequence = "".join(
        seq1(r.resname, custom_map={"MSE": "M"})
        for r in residues
    )
    return residues, sequence


def choose_receptor(model, reference_sequence):
    options = []

    for chain in model:
        residues, sequence = residues_and_sequence(chain)
        if len(sequence) < 100:
            continue

        score = float(aligner.align(reference_sequence, sequence)[0].score)
        options.append((score, chain, sequence))

    if not options:
        raise RuntimeError("No plausible receptor chain found.")

    options.sort(key=lambda item: item[0], reverse=True)
    return options[0][1], options[0][0], options[0][2]


def parse_usalign_output(output):
    # US-align typically reports two TM-scores, normalized separately
    # by Chain_1 and Chain_2 lengths.
    matches = re.findall(
        r"TM-score\s*=\s*([0-9]*\.?[0-9]+)\s*"
        r"\(if normalized by length of Chain_([12])",
        output,
        flags=re.IGNORECASE,
    )

    tm1, tm2 = None, None
    for value, chain_number in matches:
        if chain_number == "1":
            tm1 = float(value)
        elif chain_number == "2":
            tm2 = float(value)

    aligned = re.search(r"Aligned length=\s*(\d+),\s*RMSD=\s*([0-9.]+)", output)
    aligned_length = int(aligned.group(1)) if aligned else None
    aligned_rmsd = float(aligned.group(2)) if aligned else None

    return tm1, tm2, aligned_length, aligned_rmsd


def save_chain_as_pdb(structure, chain_id, destination):
    io = PDBIO()
    io.set_structure(structure)
    io.save(str(destination), ChainOnly(chain_id))


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)

    if not REFERENCE.exists():
        raise FileNotFoundError(f"Reference not found: {REFERENCE}")

    if USALIGN is None:
        raise RuntimeError(
            "Cannot locate US-align executable. Run `which USalign` or "
            "`which usalign` in the usalign environment and update "
            "USALIGN_CANDIDATES in this script."
        )

    print("=" * 72)
    print("GLP-1R RECEPTOR TM-SCORE AGAINST EXPERIMENTAL 7KI0")
    print("=" * 72)
    print(f"US-align executable: {USALIGN}")
    print(f"Reference structure: {REFERENCE}")

    ref_structure = parser.get_structure("reference", str(REFERENCE))
    ref_model = ref_structure[0]

    if REFERENCE_CHAIN not in ref_model:
        raise RuntimeError(
            f"Reference chain {REFERENCE_CHAIN} missing; "
            f"available chains: {[c.id for c in ref_model]}"
        )

    ref_chain = ref_model[REFERENCE_CHAIN]
    ref_residues, ref_sequence = residues_and_sequence(ref_chain)
    print(f"Reference receptor chain: {REFERENCE_CHAIN}")
    print(f"Reference receptor sequence length: {len(ref_sequence)}")

    files = sorted(
        (ROOT / "predictions").glob(
            "candidate_*/boltz_results_*/predictions/"
            "candidate_*/*_model_*.cif"
        )
    )

    if not files:
        raise RuntimeError("No candidate model CIF files found.")

    rows = []

    with tempfile.TemporaryDirectory(prefix="glp1r_tm_") as tmp:
        tmp = Path(tmp)
        ref_pdb = tmp / "7KI0_receptor_R.pdb"
        save_chain_as_pdb(ref_structure, REFERENCE_CHAIN, ref_pdb)

        for i, cif_path in enumerate(files, 1):
            match = re.search(r"_model_(\d+)\.cif$", cif_path.name)
            model_num = int(match.group(1)) if match else -1
            candidate = cif_path.parents[3].name

            row = {
                "candidate": candidate,
                "model": model_num,
                "file": str(cif_path),
                "status": "OK",
                "predicted_receptor_chain": "",
                "reference_length": len(ref_sequence),
                "predicted_length": "",
                "tm_normalized_by_reference_chain1": "",
                "tm_normalized_by_predicted_chain2": "",
                "aligned_length": "",
                "usalign_aligned_rmsd_A": "",
                "receptor_sequence_alignment_score": "",
            }

            print(f"[{i}/{len(files)}] {candidate} model {model_num}")

            try:
                predicted_structure = parser.get_structure(
                    f"{candidate}_{model_num}", str(cif_path)
                )
                predicted_model = predicted_structure[0]

                pred_chain, seq_score, pred_sequence = choose_receptor(
                    predicted_model, ref_sequence
                )
                row["predicted_receptor_chain"] = pred_chain.id
                row["predicted_length"] = len(pred_sequence)
                row["receptor_sequence_alignment_score"] = seq_score

                pred_pdb = tmp / f"{candidate}_model_{model_num}_receptor.pdb"
                save_chain_as_pdb(
                    predicted_structure, pred_chain.id, pred_pdb
                )

                # Chain_1 is always the experimental receptor.
                result = subprocess.run(
                    [USALIGN, str(ref_pdb), str(pred_pdb), "-mol", "prot"],
                    capture_output=True,
                    text=True,
                    timeout=120,
                )

                output = (result.stdout or "") + "\n" + (result.stderr or "")
                if result.returncode != 0:
                    raise RuntimeError(
                        f"US-align returned code {result.returncode}: "
                        f"{output[-1000:]}"
                    )

                tm1, tm2, aligned_length, aligned_rmsd = (
                    parse_usalign_output(output)
                )

                if tm1 is None or tm2 is None:
                    raise RuntimeError(
                        "Could not parse both TM-scores from US-align output. "
                        "Output excerpt: " + output[-1500:]
                    )

                row["tm_normalized_by_reference_chain1"] = tm1
                row["tm_normalized_by_predicted_chain2"] = tm2
                row["aligned_length"] = aligned_length or ""
                row["usalign_aligned_rmsd_A"] = (
                    aligned_rmsd if aligned_rmsd is not None else ""
                )

                print(
                    f"    TM(ref length)={tm1:.4f}; "
                    f"TM(pred length)={tm2:.4f}; "
                    f"aligned length={aligned_length}"
                )

            except Exception as exc:
                row["status"] = f"ERROR: {type(exc).__name__}: {exc}"
                print(f"    {row['status']}")

            rows.append(row)

    fields = list(rows[0].keys())
    with open(OUTCSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    # Candidate-level summary: median across successful predicted models.
    summary_path = OUTDIR / "receptor_tmscore_candidate_summary.csv"
    summary_rows = []

    for candidate in sorted({r["candidate"] for r in rows}):
        group = [r for r in rows if r["candidate"] == candidate]
        valid = [
            r for r in group
            if r["status"] == "OK"
            and r["tm_normalized_by_reference_chain1"] != ""
        ]

        def median_of(key):
            values = [float(r[key]) for r in valid if r[key] != ""]
            return float(np.median(values)) if values else ""

        summary_rows.append({
            "candidate": candidate,
            "models_found": len(group),
            "models_successful": len(valid),
            "models_failed": len(group) - len(valid),
            "tm_normalized_by_reference_chain1_median": median_of(
                "tm_normalized_by_reference_chain1"
            ),
            "tm_normalized_by_predicted_chain2_median": median_of(
                "tm_normalized_by_predicted_chain2"
            ),
            "aligned_length_median": median_of("aligned_length"),
            "usalign_aligned_rmsd_A_median": median_of(
                "usalign_aligned_rmsd_A"
            ),
        })

    with open(summary_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    failures = [r for r in rows if r["status"] != "OK"]

    print("\n" + "=" * 72)
    print("TM-SCORE ANALYSIS COMPLETE")
    print("=" * 72)
    print(f"Models found: {len(files)}")
    print(f"Successful: {len(rows) - len(failures)}")
    print(f"Failed: {len(failures)}")
    print(f"Per-model CSV: {OUTCSV}")
    print(f"Candidate summary: {summary_path}")

    if failures:
        print("\nFailed models:")
        for r in failures:
            print(r["candidate"], r["model"], r["status"])


if __name__ == "__main__":
    main()
</CodeBlock>

保tz python ~/calculate_glp1r_tmscore.py
```

脚本会使用 `usalign` 环境中安装的 US-align 可执行文件，但用 `bolreceptor_tmscore_candidateceptor_tmscore_candidate_summary.csv
```

把输出贴给我，我们就能比较 27 条候选的受体 TM-score 中位数及三个模型的一致性。

解释结果时，记住：TM-score 越接近 1，代表整体结构越相似；它主要反映受体折叠相似性，**不能代替候选肽的局部姿势 RMSD、界面分析或实验亲和力**。

---

# you asked

message time: 2026-10-22 21:08:41

#Total CPU time is  0.28 seconds


(usalign) ziguimu@DESKTOP-8RLFC97:~$
#Total CPU time is  0.28 seconds


(usalign) ziguimu@DESKTOP-8RLFC97:~$
-bash: syntax error near unexpected token `ziguimu@DESKTOP-8RLFC97:~$'
(usalign) ziguimu@DESKTOP-8RLFC97:~$ head -n 12 LOCAL_PATH
candidate,models_found,models_successful,models_failed,tm_normalized_by_reference_chain1_median,tm_normalized_by_predicted_chain2_median,aligned_length_median,usalign_aligned_rmsd_A_median
candidate_0009,3,0,3,,,,
candidate_0021,3,0,3,,,,
candidate_0027,3,0,3,,,,
candidate_0043,3,0,3,,,,
candidate_0044,3,0,3,,,,
candidate_0046,3,0,3,,,,
candidate_0051,3,0,3,,,,
candidate_0062,3,0,3,,,,
candidate_0071,3,0,3,,,,
candidate_0081,3,0,3,,,,
candidate_0082,3,0,3,,,,
(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

从这份汇总表看，**27 个候选的 81 个模型全部失败了**，不是 TM-score 都很低，而是脚本没有成功提取出结果。现在先不要重跑全部计算，也不要把空值当成 0。

你终端里出现的 `#Total CPU time is 0.28 seconds` 是 US-align 的输出；而 `-bash: syntax error ...` 是因为把终端提示符也一起粘贴进了命令行，不是结构计算错误的根本证据。

下一步先定位失败原因：最可能的方向是 US-align 输出格式与脚本的解析规则不一致，或者可执行文件调用方式有问题。

## 先执行这两条诊断命令

请一条一条执行，**只复制命令本身，不要复制终端提示符**。

第一条：查看每个模型记录的具体错误。



第二条：确认 US-align 的实际可执行文件路径。



把两条命令的输出发给我。我会根据真实错误修正脚本，避免盲目重算 81 个模型。

---

# you asked

message time: 2026-10-22 21:10:50

(usalign) ziguimu@DESKTOP-8RLFC97:~$ python - <<'PY'
import csv
p = "LOCAL_PATH"
with open(p, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
print("记录数：", len(rows))
for r in rows[:5]:
    print("\n候选：", r["candidate"], "model：", r["model"])
    print("状态：", r["status"])
PY
Command 'python' not found, did you mean:
  command 'python3' from deb python3
  command 'python' from deb python-is-python3
(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

没关系，这是因为你当前的 `(usalign)` 环境里没有 `python` 这个命令。先用 `python3` 就行。

### 第一步：查看失败原因

直接复制执行：



### 第二步：确认 US-align 路径



把这两步的完整输出发给我。我们先定位错误，再修复 TM-score 计算，不需要重新生成 Boltz-2 结构。

---

# you asked

message time: 2026-10-22 21:11:14

记录数： 81

候选： candidate_0009 model： 0
状态： ERROR: RuntimeError: Could not parse both TM-scores from US-align output. Output excerpt: ormalized by length of Structure_2: L=395, d0=7.18)
(You should use TM-score normalized by length of the reference structure)

(":" denotes residue pairs of d < 5.0 Angstrom, "." denotes other aligned residues)
--T-VSLWETVQKWREYRRQCQRSLTEDPPPATDLF--CNRTF-D-EYACWPDGE-PGSFVNVSCPWYLPWASSVPQGHVYRFCTAE---GLWL----QK-DN----SSLPWRDLSEC-EES---PEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANLD-IKCR-----LA-KSTLTLIPLL-GT-HEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLE
  . .::::::::::::::.::..::....        ..... . ::......  .. ........::... .. .:::....      .       .  ..    ..:...::... .:.   :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::.:.::::....:::::::::::::::::::::::::::::::::::::::..:::::::::::::::::::::::::::::::::::::::::::.:::::::::::::::::::::::::::::::::::.  .        .  .....:::.. :: ::::::::::::.::::::::::::::::::::::::::::::::::::::::::::::::
TVSLWETVQKWREYRRQCQRSLTEDPPPAT------DLFCNRTFDEYACWPDGE-PGS-FVNVSCPWYLPWA-SS-VPQGHVYR---FCTA---EGLWL-QKDNSSLPWRDLSECEESKRGERSSPEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANL-MC---KTDIKC-RLAKSTLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLE

#Total CPU time is  0.27 seconds



候选： candidate_0009 model： 1
状态： ERROR: RuntimeError: Could not parse both TM-scores from US-align output. Output excerpt: ngth of Structure_2: L=395, d0=7.18)
(You should use TM-score normalized by length of the reference structure)

(":" denotes residue pairs of d < 5.0 Angstrom, "." denotes other aligned residues)
--T-VSLWETVQKWREYRRQCQRSLTEDPPPATDLFC---NRTF-D-EYACWPDGE-PGSFVNVSCPWYLPWASSVPQGHVYRFCTAE----GLWL----QK-DN----SSLPWRDLSEC-EE-S--PEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRNSN-MNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANLDIKCR--------LA-KSTLTLIPLL-GTH-EVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLE
  . :::::::::::::::...........          .... . .:......  .. .......:::::: :. .:::...        .       .  ..    .....:::... .: .  :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::...::......:::::::::::::::::::::::::::::::::::::::.::::::::::::::::::::::::::::::::::::: :::::: .::::::::::::::::::::::::::::::::::.              .  .....::::. ::: :::::::.::::::::::::::::::::::::::::::::::::::::::::::::::::
TVSLWETVQKWREYRRQCQRSLTEDPPPAT-------DLFCNRTFDEYACWPDGE-PGS-FVNVSCPWYLPWA-SS-VPQGHVY----RFCTA---EGLWL-QKDNSSLPWRDLSECEESKRGERSSPEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEG-CWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKAN------LMCKTDIKC-RLAKSTLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLE

#Total CPU time is  0.29 seconds



候选： candidate_0009 model： 2
状态： ERROR: RuntimeError: Could not parse both TM-scores from US-align output. Output excerpt: denotes residue pairs of d < 5.0 Angstrom, "." denotes other aligned residues)
--T-VSLWETVQKWR-EYR--RQ--------------------CQRSL-TEDPPPATDLFC---NRTFDEYACWPDGEPGSFVNVSCPWYLPWASSVPQGHVYRFCTAEGLWLQKDNSS-------------------------LPWRDLSECEES-----------PEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYS-TAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANLD-IKCRLA------KSTLTLIPLLGTHEVIFAFVM---DEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLE
  . .::::::.... ..   .                     ....  ..             .....:.                 ......  .  .....                                        ..                     .::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: ....:..:. ..:::::::::::::::::::::::::::::::::::::::.::::::::::::::::::::::::::::::::::::::::::::.:::::::::::::::::::::::::::::::::::.  .           ....:::.::.::::::::::   ::::::::::::::::::::::::::::::::::::::::::::::::::::
TVSLWETVQKWREYRRQC-QRS-LTEDPPPATDLFCNRTFDEYACWP-DGE----------PGSFVNVSCP-----------------WYLPWA--S--SVPQG---------------HVYRFCTAEGLWLQKDNSSLPWRDLSE----------CEESKRGERSSPEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDG-LLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANL-MC-----KTDIKCRLAKSTLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLE

#Total CPU time is  0.24 seconds



候选： candidate_0021 model： 0
状态： ERROR: RuntimeError: Could not parse both TM-scores from US-align output. Output excerpt:  length of Structure_2: L=395, d0=7.18)
(You should use TM-score normalized by length of the reference structure)

(":" denotes residue pairs of d < 5.0 Angstrom, "." denotes other aligned residues)
--T-VSLWETVQKWREYRRQCQRSLTEDPPPATDLFC---NRTFD--EYACWPDGEPGS---FVNVSCPWYLPWASSVPQGHVYRFCTAE----GLWL----QK-DN----SSLPWRDLSEC-EES---PEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANLD-IKCR-----LA-KSTLTLIPLL-GT-HEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLE
  . .::::::::::::::..:...:....          .....  ::......       ........:::.. .. .:::...        .       .  ..    ......::... ...   :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::.:.::::....:::::::::::::::::::::::::::::::::::::::..:::::::::::::::::::::::::::::::::::::::::::.:::::::::::::::::::::::::::::::::::.  .        .  .....:::.. :: ::::::::::::.::::::::::::::::::::::::::::::::::::::::::::::::
TVSLWETVQKWREYRRQCQRSLTEDPPPAT-------DLFCNRTFDEYACWPDGE----PGSFVNVSCPWYLPWA-SS-VPQGHVY----RFCTA---EGLWL-QKDNSSLPWRDLSECEESKRGERSSPEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANL-MC---KTDIKC-RLAKSTLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLE

#Total CPU time is  0.30 seconds



候选： candidate_0021 model： 1
状态： ERROR: RuntimeError: Could not parse both TM-scores from US-align output. Output excerpt:  d0=7.09)
TM-score= 0.77058 (normalized by length of Structure_2: L=395, d0=7.18)
(You should use TM-score normalized by length of the reference structure)

(":" denotes residue pairs of d < 5.0 Angstrom, "." denotes other aligned residues)
-TV-S-LWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDE-YACWPDGEPGSFVNVSCPWYLPWASSVPQGHVYRFCTAEGLWLQKDNSS--LPWRDLSECEES------PEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRNSN-MNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANLDIKCR-------LA-KSTLTLIPLL-GTHEVIFAFV-MDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLE
 .: : :::::::::::::::::. ::... . . ....:..: :::...........:::::::::: ::.::::.:...............  ::.::::..:::      ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::....::.:....:::::::::::::::::::::::::::::::::::::::..:::::::::::::::::::::::::::::::::::: :::::: .:::::::::::::::::::::::::::::::.....            .  .....:::.. :::::..::. .:::::::::::::::::::::::::::::::::::::::::::::::::..:
TVSLWETVQKWREYRRQCQRSLTE-DPPPA-T-D-LFCNRTFDEYACWPDGEPGSFVNVSCPWYLPWA-SSVPQGHVYRFCTAEGLWLQKDNSSLPWRDLSECEESKRGERSSPEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEG-CWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANL-----MCKTDIKC-RLAKSTLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLE

#Total CPU time is  0.33 seconds


(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

找到问题了：US-align 已经成功运行，并且确实输出了 TM-score。**是我之前脚本里的正则表达式写得太严格，没匹配到实际输出格式**，所以把成功的计算全部误判成失败。抱歉，我们不需要重新计算结构，只要修正解析部分即可。

从你贴出的日志，已经能确认一个模型输出了：

- `TM-score = 0.77058`，按 `Structure_2` 长度 395 归一化。
- 但这还不是我们最终要汇总的参考受体归一化 TM-score；需要同时解析两条 TM-score 记录。

## 修复脚本

执行：



找到脚本中的整个 `parse_usalign_output` 函数，将它替换为下面这个版本：



保存并退出：`Ctrl+O` → 回车 → `Ctrl+X`。

## 重新运行



这次应该能正确识别输出中的 `Structure_1` 和 `Structure_2`。如果仍有失败，脚本会保留具体错误，方便继续定位。

完成后查看汇总：



把输出发给我。我们接下来重点看参考受体归一化的 TM-score 中位数、每个候选三个模型之间的波动，以及是否有异常模型。

---

# you asked

message time: 2026-10-22 21:20:14

候选： candidate_0021 model： 1
状态： ERROR: RuntimeError: Could not parse both TM-scores from US-align output. Output excerpt:  d0=7.09)
TM-score= 0.77058 (normalized by length of Structure_2: L=395, d0=7.18)
(You should use TM-score normalized by length of the reference structure)

(":" denotes residue pairs of d < 5.0 Angstrom, "." denotes other aligned residues)
-TV-S-LWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDE-YACWPDGEPGSFVNVSCPWYLPWASSVPQGHVYRFCTAEGLWLQKDNSS--LPWRDLSECEES------PEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRNSN-MNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANLDIKCR-------LA-KSTLTLIPLL-GTHEVIFAFV-MDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLE
 .: : :::::::::::::::::. ::... . . ....:..: :::...........:::::::::: ::.::::.:...............  ::.::::..:::      ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::....::.:....:::::::::::::::::::::::::::::::::::::::..:::::::::::::::::::::::::::::::::::: :::::: .:::::::::::::::::::::::::::::::.....            .  .....:::.. :::::..::. .:::::::::::::::::::::::::::::::::::::::::::::::::..:
TVSLWETVQKWREYRRQCQRSLTE-DPPPA-T-D-LFCNRTFDEYACWPDGEPGSFVNVSCPWYLPWA-SSVPQGHVYRFCTAEGLWLQKDNSSLPWRDLSECEESKRGERSSPEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVFSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEG-CWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANL-----MCKTDIKC-RLAKSTLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLE

#Total CPU time is  0.33 seconds


(usalign) ziguimu@DESKTOP-8RLFC97:~$ head -n 12 LOCAL_PATH
candidate,models_found,models_successful,models_failed,tm_normalized_by_reference_chain1_median,tm_normalized_by_predicted_chain2_median,aligned_length_median,usalign_aligned_rmsd_A_median
candidate_0009,3,0,3,,,,
candidate_0021,3,0,3,,,,
candidate_0027,3,0,3,,,,
candidate_0043,3,0,3,,,,
candidate_0044,3,0,3,,,,
candidate_0046,3,0,3,,,,
candidate_0051,3,0,3,,,,
candidate_0062,3,0,3,,,,
candidate_0071,3,0,3,,,,
candidate_0081,3,0,3,,,,
candidate_0082,3,0,3,,,,
(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

我看到原因了。上次给你的正则表达式还漏了一种格式：**US-align 对两条结构的 TM-score 使用了不同的括号文字**。

你贴出的输出中，`Structure_2` 使用：



而 `Structure_1` 的输出通常使用 `(if normalized by length of Structure_1...)`。上次的正则没有允许这个额外的 `if`，因此仍然解析失败。我们只需修正这一处，不需要重新跑 Boltz-2。

## 1. 再次修改解析函数

执行：

`
找到 `parse_usalign_output` 函数中的这一行：

`
将它改成：

`
关键变化是 `(?:if\s+)?`：允许 `if ` 出现，也允许它不出现。

保存并退出：`Ctrl+O` → 回车 → `Ctrl+X`。

## 2. 先做独立测试，再重新计算

先执行下面的测试，确认正则能识别两种格式：

``预期看到：

``## 3. 重新运行正式脚本

只有测试通过后，再执行：

```后查看汇总：

```**独立测试结果和新的汇总表**发给我。我们再检查 81 个模型是否都成功，以及确认哪一列对应参考受体 7KI0 的归一化 TM-score。注意，受体 TM-score 反映的是结构相似度，不能直接作为 GLP-1R binder 的结合能力证据。

---

# you asked

message time: 2026-10-22 21:28:56

给我改后完整版

---

# chatgpt response

下面给你一份**完整的 `calculate_glp1r_tmscore.py` 修正版**，不是补丁。它兼容 US-align 的两种 TM-score 输出格式，并保留逐模型结果、候选汇总和错误日志。由于我无法直接检查你当前 WSL 中的原脚本，建议用下面版本整体替换。

先执行：



将原内容全部删除，粘贴以下完整脚本。

<CodeBlock language="python" editable>
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Calculate receptor structural similarity to experimental GLP-1R
from 7KI0 using US-align.

Input:
  Experimental reference:
    LOCAL_PATH

  Boltz-2 model CIFs:
    LOCAL_PATH
      candidate_*/boltz_results_*/predictions/candidate_*/*_model_*.cif

Output:
  audit/structure/receptor_tmscore_vs_7KI0.csv
  audit/structure/receptor_tmscore_candidate_summary.csv

This script calculates receptor structural similarity only.
TM-score is not experimental evidence of binder binding or affinity.
"""

import csv
import re
import shutil
import subprocess
import tempfile
import traceback
from pathlib import Path
from statistics import median

from Bio.PDB import MMCIFParser, PDBIO, Select, is_aa
from Bio.SeqUtils import seq1
from Bio.Align import PairwiseAligner


# ---------------------------------------------------------------------
# Paths and settings
# ---------------------------------------------------------------------

ROOT = Path("LOCAL_PATH")
REFERENCE_CIF = Path(
    "LOCAL_PATH"
)
OUTPUT_DIR = ROOT / "audit" / "structure"

PER_MODEL_CSV = OUTPUT_DIR / "receptor_tmscore_vs_7KI0.csv"
SUMMARY_CSV = OUTPUT_DIR / "receptor_tmscore_candidate_summary.csv"

REFERENCE_CHAIN_ID = "R"

USALIGN_CANDIDATES = [
    shutil.which("USalign"),
    shutil.which("usalign"),
    "USER_HOME/miniconda3/envs/usalign/bin/USalign",
    "USER_HOME/miniconda3/envs/usalign/bin/usalign",
    "/usr/local/bin/USalign",
    "/usr/bin/USalign",
]

USALIGN = next(
    (
        str(Path(path))
        for path in USALIGN_CANDIDATES
        if path and Path(path).is_file()
    ),
    None,
)


# ---------------------------------------------------------------------
# Structure utilities
# ---------------------------------------------------------------------

class ChainOnly(Select):
    def __init__(self, chain_id):
        self.chain_id = chain_id

    def accept_chain(self, chain):
        return chain.id == self.chain_id

    def accept_model(self, model):
        return model.id == 0

    def accept_residue(self, residue):
        return is_aa(residue, standard=False)

    def accept_atom(self, atom):
        return atom.element != "H"


def residue_sequence(chain):
    """Return amino-acid sequence and residue list for a chain."""
    residues = [
        residue
        for residue in chain.get_residues()
        if is_aa(residue, standard=False) and "CA" in residue
    ]
    sequence = "".join(
        seq1(residue.resname, custom_map={"UNK": "X"})
        for residue in residues
    )
    return sequence, residues


def load_reference_chain():
    if not REFERENCE_CIF.is_file():
        raise FileNotFoundError(
            f"Reference CIF not found: {REFERENCE_CIF}"
        )

    parser = MMCIFParser(QUIET=True)
    structure = parser.get_structure("reference", str(REFERENCE_CIF))
    model = next(structure.get_models())

    if REFERENCE_CHAIN_ID not in model:
        available = [chain.id for chain in model.get_chains()]
        raise KeyError(
            f"Reference chain {REFERENCE_CHAIN_ID!r} not found. "
            f"Available chains: {available}"
        )

    chain = model[REFERENCE_CHAIN_ID]
    sequence, residues = residue_sequence(chain)

    if not sequence:
        raise ValueError(
            f"No amino-acid residues found in reference chain "
            f"{REFERENCE_CHAIN_ID}"
        )

    return structure, chain, sequence, residues


def find_predicted_receptor_chain(cif_path, reference_sequence):
    """
    Identify the predicted receptor chain by global sequence alignment.

    Boltz output can contain both the receptor and designed binder.
    The chain with the best sequence alignment to reference chain R
    is treated as the predicted receptor.
    """
    parser = MMCIFParser(QUIET=True)
    structure = parser.get_structure("predicted", str(cif_path))
    model = next(structure.get_models())

    aligner = PairwiseAligner()
    aligner.mode = "global"
    aligner.match_score = 2.0
    aligner.mismatch_score = -1.0
    aligner.open_gap_score = -5.0
    aligner.extend_gap_score = -0.5

    best_chain = None
    best_sequence = None
    best_score = float("-inf")
    best_identity = 0.0

    for chain in model.get_chains():
        sequence, _ = residue_sequence(chain)
        if not sequence:
            continue

        score = aligner.score(reference_sequence, sequence)

        # Calculate identity over aligned residue pairs.
        alignments = aligner.align(reference_sequence, sequence)
        alignment = alignments[0]
        coordinates = alignment.coordinates

        identical = 0
        paired = 0
        for i in range(len(coordinates[0]) - 1):
            ref_start, ref_end = coordinates[0][i:i + 2]
            pred_start, pred_end = coordinates[1][i:i + 2]

            ref_len = ref_end - ref_start
            pred_len = pred_end - pred_start

            if ref_len == pred_len and ref_len > 0:
                for offset in range(ref_len):
                    if (
                        reference_sequence[ref_start + offset]
                        == sequence[pred_start + offset]
                    ):
                        identical += 1
                    paired += 1

        identity = identical / paired if paired else 0.0

        if score > best_score:
            best_chain = chain
            best_sequence = sequence
            best_score = score
            best_identity = identity

    if best_chain is None:
        raise ValueError("No amino-acid chain found in predicted CIF")

    return (
        structure,
        best_chain,
        best_sequence,
        best_score,
        best_identity,
    )


def write_chain_pdb(structure, chain_id, output_path):
    io = PDBIO()
    io.set_structure(structure)
    io.save(str(output_path), ChainOnly(chain_id))


# ---------------------------------------------------------------------
# US-align output parsing
# ---------------------------------------------------------------------

def parse_usalign_output(output):
    """
    Parse TM-scores normalized by Structure_1 and Structure_2.

    Accepts both common formats:
      TM-score= 0.81 (if normalized by length of Structure_1: ...)
      TM-score= 0.77 (normalized by length of Structure_2: ...)

    Some builds use Chain_1 / Chain_2 instead of Structure_1 / Structure_2.
    """
    pattern = (
        r"TM-score\s*=\s*([0-9]*\.?[0-9]+)"
        r"\s*\((?:if\s+)?normalized\s+by\s+length\s+of\s+"
        r"(?:Structure|Chain)_([12])\b"
    )

    matches = re.findall(
        pattern,
        output,
        flags=re.IGNORECASE,
    )

    scores = {}
    for value, number in matches:
        scores[int(number)] = float(value)

    tm1 = scores.get(1)
    tm2 = scores.get(2)

    aligned_match = re.search(
        r"Aligned length\s*=\s*(\d+)\s*,\s*RMSD\s*=\s*([0-9.]+)",
        output,
        flags=re.IGNORECASE,
    )
    aligned_length = (
        int(aligned_match.group(1)) if aligned_match else None
    )
    aligned_rmsd = (
        float(aligned_match.group(2)) if aligned_match else None
    )

    if tm1 is None or tm2 is None:
        excerpt = output[-5000:]
        raise RuntimeError(
            "Could not parse both TM-scores from US-align output. "
            f"Parsed scores: {scores}. Output excerpLOCAL_PATH"
        )

    return tm1, tm2, aligned_length, aligned_rmsd


def run_usalign(reference_pdb, predicted_pdb):
    if not USALIGN:
        raise FileNotFoundError(
            "US-align executable not found. Try `which USalign` or "
            "`which usalign`, then add its full path to USALIGN_CANDIDATES."
        )

    result = subprocess.run(
        [USALIGN, str(predicted_pdb), str(reference_pdb)],
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )

    output = (result.stdout or "") + "\n" + (result.stderr or "")

    if result.returncode != 0:
        raise RuntimeError(
            f"US-align exited with code {result.returncode}.\n"
            f"OutpuLOCAL_PATH"
        )

    return parse_usalign_output(output)


# ---------------------------------------------------------------------
# Main workflow
# ---------------------------------------------------------------------

def find_model_files():
    prediction_root = ROOT / "predictions"
    pattern = (
        "candidate_*/boltz_results_*/predictions/"
        "candidate_*/*_model_*.cif"
    )
    return sorted(prediction_root.glob(pattern))


def parse_candidate_model(cif_path):
    model_match = re.search(r"_model_(\d+)\.cif$", cif_path.name)
    model_number = model_match.group(1) if model_match else ""

    candidate = ""
    for parent in cif_path.parents:
        if re.fullmatch(r"candidate_\d+", parent.name):
            candidate = parent.name
            break

    return candidate, model_number


def summarize_rows(rows):
    grouped = {}

    for row in rows:
        grouped.setdefault(row["candidate"], []).append(row)

    summary_rows = []

    for candidate in sorted(grouped):
        candidate_rows = grouped[candidate]

        successful = [
            row for row in candidate_rows
            if row["status"] == "OK"
        ]
        failed = [
            row for row in candidate_rows
            if row["status"] != "OK"
        ]

        def numeric_values(field):
            values = []
            for row in successful:
                value = row.get(field, "")
                if value not in ("", None):
                    try:
                        values.append(float(value))
                    except (ValueError, TypeError):
                        pass
            return values

        def median_or_blank(values):
            return median(values) if values else ""

        summary_rows.append({
            "candidate": candidate,
            "models_found": len(candidate_rows),
            "models_successful": len(successful),
            "models_failed": len(failed),
            "tm_normalized_by_reference_chain1_median": median_or_blank(
                numeric_values("tm_normalized_by_reference_chain1")
            ),
            "tm_normalized_by_predicted_chain2_median": median_or_blank(
                numeric_values("tm_normalized_by_predicted_chain2")
            ),
            "aligned_length_median": median_or_blank(
                numeric_values("aligned_length")
            ),
            "usalign_aligned_rmsd_A_median": median_or_blank(
                numeric_values("usalign_aligned_rmsd_A")
            ),
        })

    return summary_rows


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Project root: {ROOT}")
    print(f"Reference: {REFERENCE_CIF}")
    print(f"US-align: {USALIGN or 'NOT FOUND'}")

    if not USALIGN:
        raise FileNotFoundError(
            "US-align executable was not found. Activate the environment "
            "where it is installed, or edit USALIGN_CANDIDATES."
        )

    (
        reference_structure,
        reference_chain,
        reference_sequence,
        reference_residues,
    ) = load_reference_chain()

    print(
        f"Reference chain {REFERENCE_CHAIN_ID}: "
        f"{len(reference_sequence)} amino acids"
    )

    model_files = find_model_files()
    print(f"Model CIF files found: {len(model_files)}")

    if not model_files:
        raise FileNotFoundError(
            f"No model CIF files found under {ROOT / 'predictions'}"
        )

    rows = []

    with tempfile.TemporaryDirectory(prefix="glp1r_tmscore_") as temp_dir:
        temp_dir = Path(temp_dir)
        reference_pdb = temp_dir / "reference_chain_R.pdb"
        write_chain_pdb(
            reference_structure,
            REFERENCE_CHAIN_ID,
            reference_pdb,
        )

        for index, cif_path in enumerate(model_files, start=1):
            candidate, model_number = parse_candidate_model(cif_path)

            row = {
                "candidate": candidate,
                "model": model_number,
                "model_cif": str(cif_path),
                "predicted_receptor_chain": "",
                "predicted_receptor_sequence_length": "",
                "sequence_alignment_score": "",
                "sequence_identity_fraction": "",
                "tm_normalized_by_reference_chain1": "",
                "tm_normalized_by_predicted_chain2": "",
                "aligned_length": "",
                "usalign_aligned_rmsd_A": "",
                "status": "",
            }

            try:
                (
                    predicted_structure,
                    predicted_chain,
                    predicted_sequence,
                    alignment_score,
                    identity,
                ) = find_predicted_receptor_chain(
                    cif_path,
                    reference_sequence,
                )

                row["predicted_receptor_chain"] = predicted_chain.id
                row["predicted_receptor_sequence_length"] = len(
                    predicted_sequence
                )
                row["sequence_alignment_score"] = alignment_score
                row["sequence_identity_fraction"] = identity

                predicted_pdb = (
                    temp_dir
                    / f"predicted_{index:04d}_chain.pdb"
                )
                write_chain_pdb(
                    predicted_structure,
                    predicted_chain.id,
                    predicted_pdb,
                )

                # US-align input order is:
                # Structure_1 = predicted receptor
                # Structure_2 = reference receptor
                tm1, tm2, aligned_length, aligned_rmsd = run_usalign(
                    predicted_pdb,
                    reference_pdb,
                )

                # The reference is the second input in this script.
                # Therefore Structure_2 normalization is the reference-normalized
                # TM-score and is stored in the reference column below.
                row["tm_normalized_by_reference_chain1"] = tm2
                row["tm_normalized_by_predicted_chain2"] = tm1
                row["aligned_length"] = (
                    aligned_length if aligned_length is not None else ""
                )
                row["usalign_aligned_rmsd_A"] = (
                    aligned_rmsd if aligned_rmsd is not None else ""
                )
                row["status"] = "OK"

            except Exception as exc:
                row["status"] = (
                    f"ERROR: {type(exc).__name__}: {exc}"
                )

            rows.append(row)
            print(
                f"[{index}/{len(model_files)}] "
                f"{candidate} model {model_number}: {row['status']}"
            )

    per_model_fields = [
        "candidate",
        "model",
        "model_cif",
        "predicted_receptor_chain",
        "predicted_receptor_sequence_length",
        "sequence_alignment_score",
        "sequence_identity_fraction",
        "tm_normalized_by_reference_chain1",
        "tm_normalized_by_predicted_chain2",
        "aligned_length",
        "usalign_aligned_rmsd_A",
        "status",
    ]

    with PER_MODEL_CSV.open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=per_model_fields)
        writer.writeheader()
        writer.writerows(rows)

    summary_rows = summarize_rows(rows)
    summary_fields = [
        "candidate",
        "models_found",
        "models_successful",
        "models_failed",
        "tm_normalized_by_reference_chain1_median",
        "tm_normalized_by_predicted_chain2_median",
        "aligned_length_median",
        "usalign_aligned_rmsd_A_median",
    ]

    with SUMMARY_CSV.open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary_rows)

    success_count = sum(row["status"] == "OK" for row in rows)
    failure_count = len(rows) - success_count

    print("\nFinished.")
    print(f"Models processed: {len(rows)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {failure_count}")
    print(f"Per-model results: {PER_MODEL_CSV}")
    print(f"Candidate summary: {SUMMARY_CSV}")


if __name__ hon -m py_compin -n boltructure/receptor_tmscore_candidate_summary.csv
```

**注意一个重要细节：**这版脚本将预测受体作为 US-align 的第一个输入、7KI0 参考受体作为第二个输入，因此 `Structure_2` 归一化的 TM-score 才是按参考受体长度归一化的分数。输出列名已按这个输入顺序映射。另需留意，不同 US-align 版本可能会因输入顺序影响对齐结果；若运行后仍有报错，请把第一条 `ERROR` 和 US-align 路径发来，我们再针对实际输出修正。

---

# you asked

message time: 2026-10-22 21:44:12

Finished.
Models processed: 81
Successful: 81
Failed: 0
Per-model results: LOCAL_PATH
Candidate summary: LOCAL_PATH
(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

很好，**81 个模型全部计算成功，TM-score 计算流程已经跑通了。** 但目前只能确认程序执行成功，还不能判断哪些候选更值得关注；下一步需要查看具体分数，并核对参考结构归一化列的映射。

## 第一步：查看候选汇总

请直接复制运行：



再查看逐模型结果：



把两段输出发给我。

## 第二步：我们将重点分析什么

拿到数据后，我会重点检查：

1. **受体 TM-score**：预测的 GLP-1R 结构与实验参考结构 7KI0 的整体相似程度。
2. **候选内部稳定性**：同一候选的 3 个模型分数是否一致。
3. **异常候选**：是否存在受体结构偏差明显、值得进一步检查的模型。
4. **与其他指标交叉分析**：结合已有的 ipTM、PAE 等结果，判断哪些候选值得优先进行结构检查。

需要强调：7KI0 是 GLP-1R 与司美格鲁肽的实验复合物。受体 TM-score 衡量的是**受体结构相似度**，不是设计 binder 的结合能力，也不能单独证明候选物能够结合 GLP-1R。

另外，当前脚本将预测受体作为 US-align 的第一个输入、参考受体作为第二个输入；汇总表中参考归一化列已按此顺序映射。看到实际 CSV 后，我还会核验列值与 US-align 原始输出是否一致，避免把两种归一化分数弄反。

---

# you asked

message time: 2026-10-22 21:44:40

(usalign) ziguimu@DESKTOP-8RLFC97:~$ column -s, -t < LOCAL_PATH | head -n 20
candidate       models_found  models_successful  models_failed  tm_normalized_by_reference_chain1_median  tm_normalized_by_predicted_chain2_median  aligned_length_median  usalign_aligned_rmsd_A_median
candidate_0009  3             3                  0              0.74729                                   0.76649                                   357.0                  4.12
candidate_0021  3             3                  0              0.74189                                   0.76083                                   358.0                  3.99
candidate_0027  3             3                  0              0.76368                                   0.78301                                   371.0                  4.09
candidate_0043  3             3                  0              0.7765                                    0.79624                                   372.0                  3.98
candidate_0044  3             3                  0              0.77325                                   0.79303                                   371.0                  4.1
candidate_0046  3             3                  0              0.76085                                   0.78048                                   360.0                  4.01
candidate_0051  3             3                  0              0.72242                                   0.74121                                   336.0                  3.83
candidate_0062  3             3                  0              0.74771                                   0.76693                                   357.0                  4.17
candidate_0071  3             3                  0              0.75938                                   0.77854                                   368.0                  4.17
candidate_0081  3             3                  0              0.6782                                    0.69586                                   320.0                  4.03
candidate_0082  3             3                  0              0.78772                                   0.80761                                   377.0                  3.73
candidate_0093  3             3                  0              0.75868                                   0.77809                                   361.0                  4.02
candidate_0096  3             3                  0              0.77824                                   0.7978                                    371.0                  3.98
candidate_0111  3             3                  0              0.68772                                   0.70591                                   314.0                  3.77
candidate_0112  3             3                  0              0.7709                                    0.79056                                   371.0                  4.13
candidate_0129  3             3                  0              0.73795                                   0.75699                                   349.0                  4.01
candidate_0153  3             3                  0              0.69987                                   0.71823                                   321.0                  4.06
candidate_0165  3             3                  0              0.75833                                   0.77779                                   362.0                  4.18
candidate_0170  3             3                  0              0.76059                                   0.78003                                   364.0                  4.02
(usalign) ziguimu@DESKTOP-8RLFC97:~$ head -n 8 LOCAL_PATH
candidate,model,model_cif,predicted_receptor_chain,predicted_receptor_sequence_length,sequence_alignment_score,sequence_identity_fraction,tm_normalized_by_reference_chain1,tm_normalized_by_predicted_chain2,aligned_length,usalign_aligned_rmsd_A,status
candidate_0009,0,LOCAL_PATH
candidate_0009,1,LOCAL_PATH
candidate_0009,2,LOCAL_PATH
candidate_0021,0,LOCAL_PATH
candidate_0021,1,LOCAL_PATH
candidate_0021,2,LOCAL_PATH
candidate_0027,0,LOCAL_PATH
(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

这次结果已经正常了：**81 个模型全部成功计算，27 个候选各有 3 个模型。** 从你发来的数据看，预测受体链 A 的序列长度都是 395 aa，与参考链的序列比对得分为 753.5、序列一致性为 1.0，说明受体链识别是合理的。

不过，我还想特别提醒一个分析上的区别：我们目前计算的是**预测的 GLP-1R 受体结构与 7KI0 实验受体结构的相似程度**，不是 binder 与受体的结合质量。

## 1. 目前这批结果说明什么？

从你贴出的汇总数据中：

- 参考结构归一化 TM-score 的候选中位数约在 **0.68–0.79** 之间。
- `candidate_0082` 的参考归一化 TM-score 中位数为 **0.78772**，在已展示的候选中最高。
- `candidate_0096` 为 **0.77824**，`candidate_0043` 为 **0.77650**。
- `candidate_0081` 为 **0.67820**，`candidate_0111` 为 **0.68772**，在已展示的候选中较低。
- 多数候选的对齐长度约为 350–377 aa；部分候选只有约 314–336 aa，值得检查对齐覆盖区域。

这里的“最高”和“最低”仅指你当前展示的汇总行；要确认整个 27 个候选的完整排名，仍需分析完整 CSV。

还有一个关键点：受体序列一致性为 100%，并不意味着受体构象完全一致。TM-score 和对齐长度仍然能反映结构差异，尤其是柔性胞外区、跨膜区和局部构象的差异。

## 2. 下一步：输出完整排名和模型间波动

目前汇总表只有中位数。我们还需要查看每个候选的 3 次预测是否一致，避免只看中位数就误判。

请在终端运行下面的命令，它会读取已有 CSV，不需要重新计算结构：

``### 3. 一个需要注意的列名问题

当前脚本把参考结构归一化的分数存入 `tm_normalized_by_reference_chain1`，但实际上 US-align 的输入顺序是：

- `Structure_1`：预测受体
- `Structure_2`：7KI0 参考受体

因此，该列保存的是按 **Structure_2（参考受体）** 归一化的 TM-score。数值映射正确，但列名中的 `chain1` 容易造成误解，之后整理正式项目数据时建议统一重命名为 `tm_normalized_by_reference`。

把完整排名输出发给我后，我们就能区分：哪些候选的受体结构更接近参考构象，哪些模型间波动更大。随后再将结果与 binder 的 ipTM、PAE 和界面几何指标交叉分析，形成更可靠的候选筛选依据。

---

# you asked

message time: 2026-10-22 21:48:10

Candidate         N  TM median    TM min    TM max       SD  Align len
candidate_0082    3     0.7877    0.7697    0.8043   0.0141      377.0
candidate_0213    3     0.7806    0.7626    0.8237   0.0257      375.0
candidate_0096    3     0.7782    0.7688    0.7790   0.0046      371.0
candidate_0043    3     0.7765    0.7585    0.8013   0.0176      372.0
candidate_0044    3     0.7732    0.7642    0.7835   0.0079      371.0
candidate_0112    3     0.7709    0.7615    0.7828   0.0087      371.0
candidate_0228    3     0.7698    0.7563    0.8290   0.0316      370.0
candidate_0027    3     0.7637    0.7474    0.7977   0.0209      371.0
candidate_0200    3     0.7636    0.7564    0.7961   0.0173      366.0
candidate_0175    3     0.7630    0.7558    0.7750   0.0079      364.0
candidate_0046    3     0.7609    0.7338    0.7812   0.0194      360.0
candidate_0170    3     0.7606    0.7534    0.7749   0.0089      364.0
candidate_0227    3     0.7604    0.7350    0.7772   0.0174      360.0
candidate_0173    3     0.7595    0.7478    0.7794   0.0131      362.0
candidate_0071    3     0.7594    0.7452    0.7923   0.0197      368.0
candidate_0093    3     0.7587    0.7280    0.7793   0.0211      361.0
candidate_0165    3     0.7583    0.7479    0.7591   0.0051      362.0
candidate_0062    3     0.7477    0.7159    0.7595   0.0184      357.0
candidate_0009    3     0.7473    0.6894    0.7572   0.0299      357.0
candidate_0021    3     0.7419    0.7347    0.7706   0.0155      358.0
candidate_0241    3     0.7414    0.6995    0.7431   0.0202      349.0
candidate_0129    3     0.7379    0.7304    0.7395   0.0040      349.0
candidate_0219    3     0.7320    0.6879    0.7774   0.0366      358.0
candidate_0051    3     0.7224    0.6905    0.7375   0.0196      336.0
candidate_0153    3     0.6999    0.6855    0.7578   0.0312      321.0
candidate_0111    3     0.6877    0.6862    0.6904   0.0017      314.0
candidate_0081    3     0.6782    0.6775    0.6910   0.0062      320.0
(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

这份完整排名很有价值。我们现在可以把 27 个 GLP-1R 设计候选的受体结构一致性，作为独立的质量控制维度来分析。

**最重要的结论：`candidate_0082` 的受体 TM-score 中位数最高，但这不代表它就是最好的 binder。** 目前我们能回答的是“预测受体结构与 7KI0 有多相似”，还不能据此回答“设计的蛋白能否结合 GLP-1R”。

## 1. 排名中的主要发现

<box gap={3}>
  <row align=start gap={3}>
    <box background="surface-secondary" radius="lg" padding={3} align=center minWidth="88px">
      <title size="xl" color="success">0.7877</title>
      <text color="secondary" size="xs">最高中位数</text>
    </box>
    <box flex="1" gap={1}>
      **`candidate_0082` — 受体结构相似度排名第一**

      <text size="sm">对齐长度 377 aa，模型间标准差 0.0141。受体与参考结构整体较接近，而且三次预测的结果没有特别大的波动。</text>
    </box>
  </row>
  <divider color="subtle" />
  <row align=start gap={3}>
    <box background="surface-secondary" radius="lg" padding={3} align=center minWidth="88px">
      <title size="xl">0.7782</title>
      <text color="secondary" size="xs">标准差 0.0046</text>
    </box>
    <box flex="1" gap={1}>
      **`candidate_0096` — 结果相当稳定**

      <text size="sm">中位数排名第三，但标准差只有 0.0046，是这批候选中波动较小的之一。它值得与排名更高的候选并列进入后续检查。</text>
    </box>
  </row>
  <divider color="subtle" />
  <row align=start gap={3}>
    <box background="surface-secondary" radius="lg" padding={3} align=center minWidth="88px">
      <title size="xl">0.7806</title>
      <text color="secondary" size="xs">最大值 0.8237</text>
    </box>
    <box flex="1" gap={1}>
      **`candidate_0213` — 有较高分数，但波动更大**

      <text size="sm">中位数排名第二，标准差 0.0257。最高模型分数较突出，但不能只选最高分的那个模型；还应查看三个模型的具体结构差异。</text>
    </box>
  </row>
  <divider color="subtle" />
  <row align=start gap={3}>
    <box background="surface-secondary" radius="lg" padding={3} align=center minWidth="88px">
      <title size="xl">0.6782</title>
      <text color="secondary" size="xs">最低中位数</text>
    </box>
    <box flex="1" gap={1}>
      **`candidate_0081` — 需要检查对齐覆盖范围**

      <text size="sm">中位数最低，对齐长度 320 aa。其分数偏低可能与构象偏差、结构覆盖区域或柔性区域有关，不能在未检查对齐结果前直接判定结构失败。</text>
    </box>
  </row>
</box>

## 2. 哪些候选值得优先检查？

我建议暂时分成三组，而不是直接按 TM-score 选出最终 binder。

| 优先组 | 候选 | 理由 |
|---|---|---|
| 受体结构相似度较高 | `0082`、`0096`、`0043`、`0044`、`0112` | 中位数较高，对齐长度也相对较长 |
| 分数高但需检查稳定性 | `0213`、`0228`、`0200` | 部分模型分数较高，但模型间波动较大 |
| 需要检查结构覆盖和偏差 | `0081`、`0111`、`0153`、`0051` | 中位数和对齐长度相对较低 |

这里的分组只用于安排**结构质量检查顺序**，不是结合能力排名。

## 3. 下一步比继续计算全局 TM-score 更重要

我建议现在暂停增加全局受体指标，转向两个问题：

1. **局部结合口袋是否合理？** 将预测受体与 7KI0 的局部口袋进行结构叠合，再检查 binder 的位置、界面残基、空间冲突和关键相互作用。全局结构相似度高，不代表局部口袋构象一定正确。
2. **三个模型的 binder 姿势是否一致？** 同一个候选的三个预测模型即使受体 TM-score 接近，binder 也可能采取不同的结合姿势。需要单独比较 binder 的位置和界面几何。

尤其是 GLP-1R 这类具有较大胞外结构域和跨膜区的受体，不能只凭全长受体的整体对齐分数判断局部结合界面。

**我建议下一步先做局部口袋叠合与 binder 界面评估，并优先检查 `candidate_0082`、`candidate_0096`、`candidate_0043` 和 `candidate_0044`。** 同时保留 `candidate_0213`，因为它的高分模型可能有进一步检查的价值。这样既利用了当前 TM-score 的结果，也不会让一个与结合能力没有直接等价关系的指标主导整个筛选流程。

---

# you asked

message time: 2026-10-22 22:15:00

分子动力学（MD）模拟以我现在的条件是不是没法计算

---

# chatgpt response

不是完全没法算。**以你现在的硬件条件（RTX 5070 Laptop GPU、8 GB 显存、WSL Ubuntu），可以做一些分子动力学（MD）模拟，但不适合直接把大规模、长时间的蛋白质复合物 MD 当作常规任务。**

对你现在的 GLP1R 设计项目来说，更重要的是区分三件事：**能不能跑起来、能跑多长、结果能不能支持你的研究结论。**

## 1. 你的电脑大致能做什么？

| 任务 | 目前条件下的可行性 | 说明 |
|---|---|---|
| 蛋白结构能量最小化 | <badge color="success">可行</badge> | 通常比正式 MD 便宜，适合初步检查结构 |
| 短时间、显式溶剂 MD | <badge color="success">可尝试</badge> | 可从小体系、短轨迹开始，实际速度取决于体系规模和软件 |
| GLP1R 局部结构或较小蛋白复合物的短程模拟 | <badge color="warning">有条件可行</badge> | 需要控制原子数、时间长度，并测试 GPU 性能 |
| 全长 GLP1R—设计肽复合物，带膜和水的 MD | <badge color="warning">较吃力</badge> | 膜、水、离子会显著增加原子数；8 GB 显存可能成为限制 |
| 多个候选物分别做长时间、多重复 MD | <badge color="danger">不建议本机批量做</badge> | 计算量会快速增长，难以在合理时间内完成 |

这些判断是基于硬件和体系复杂度的初步评估，不是对你机器实测性能的保证。**8 GB 显存不意味着 MD 一定跑不了**：部分程序可采用混合精度、CPU/GPU 协同或其他配置；但具体能跑多大体系、每纳秒需要多久，必须通过实际 benchmark 确认。

## 2. 对你的 GLP1R 项目，我建议怎么做？

你现在已经有 27 个设计候选物，每个有 3 个 Boltz-2 预测模型。**我不建议一开始就把 27 个候选物全部拿去做 MD。**

更合理的路线是：

<box border radius="xl" padding={3} gap={3}>
  <row align=start gap={3}>
    <box background="surface-secondary" radius="lg" size="40px" align=center justify=center>
      <icon name="check-circle" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **第一步：结构质量检查**

      利用现有预测结果，检查受体局部构象、候选肽的结合姿态、界面接触和空间冲突。你刚算出的全受体 TM-score 可以作为整体结构质控的一部分，但不能直接用来判定结合能力。
    </box>
  </row>
  <divider color="subtle" />
  <row align=start gap={3}>
    <box background="surface-secondary" radius="lg" size="40px" align=center justify=center>
      <icon name="filter" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **第二步：筛选少数代表性候选物**

      综合界面几何、预测置信度、结合位点合理性和不同模型之间的一致性，选择少量候选物。不要只按 TM-score 排名。
    </box>
  </row>
  <divider color="subtle" />
  <row align=start gap={3}>
    <box background="surface-secondary" radius="lg" size="40px" align=center justify=center>
      <icon name="atom" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **第三步：测试短程 MD**

      先选择 1 个候选复合物，建立合理的模拟体系，测试能量最小化、平衡过程和短程轨迹是否能稳定运行，再决定是否扩大规模。
    </box>
  </rowbtle" />
  <row alecondary" radius="lg" size="40px" align=center justify=center>
      <icon name="chart-no-axes-combined" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **第四步：评估轨迹，而不是只看一张结构图**

      可以分析 RMSD、RMSF、氢键、界面接触保持情况等。短程模拟只能提供有限的结构稳定性证据，不能单独证明结合亲和力或激动活性。
    </box>
  </row>
</box>

## 3. 如果真要跑 MD，推荐什么软件？

<row align=start gap={3}>
  <AsyncImage query="GROMACS molecular dynamics protein simulation logo" aspectRatio="1:1" width="76px" />
  <box flex="1" gap={1}>
    **<Entity value="GROMACS" category="software" disambig="分子动力学模拟软件" />**

    成熟的分子动力学软件，适合蛋白质体系。可以在你的 WSL 环境中尝试 GPU 加速；需要检查 CUDA、编译选项和实际 GPU 支持情况。

    <text color="secondary" size="sm">适合：显式溶剂蛋白质模拟、轨迹分析</text>
  </box>
</row>
<row align=start gap={3}>
  <AsyncImage query="OpenMM molecular simulation Python logo" aspectRatio="1:1" width="76px" />
  <box flex="1" gap={1}>
    **<Entity value="OpenMM" category="software" disambig="GPU 加速分子模拟工具包" />**

    Python 接口灵活，适合自动化地对多个候选物建立体系、运行模拟和分析轨迹。

    <text color="secondary" size="sm">适合：Python 工作流、GPU 测试、批量分析</text>
  </box>
</row>

对于你的项目，我会优先考虑 **OpenMM 或 GROMACS 做一个小规模试运行**，而不是先投入大量时间搭建复杂的膜蛋白模拟体系。

还有一个重要问题：GLP1R 是膜蛋白。如果你模拟的是完整受体，通常需要认真处理膜环境；如果只模拟截取的局部结构，又可能丢失真实口袋的构象约束。不能简单地把 Boltz-2 输出结构直接扔进 MD 软件就认为体系已经合理。

## 4. 我们可以先做一次硬件可行性测试

你现在不需要立刻决定是否开展 MD。先收集硬件和软件信息，再估算计算成本更稳妥。

在 WSL 终端运行：

```bash
nvidia-smi
```

然后检查是否安装过相关软件：

```bash
which gmx
conda list | grep -i openmm
```

把输出发给我，我就能进一步判断你的环境适合哪条路线，并帮你设计一个**先验证能跑、再估算速度、最后决定模拟时长**的测试方案。

如果测试发现本机速度不够，也不代表你不能做 MD；可以把 MD 降级为少数候选物的补充分析，或者使用实验室服务器完成更长的模拟。

---

# you asked

message time: 2026-10-22 22:15:45

那有没有必要跑一下PCANN

---

# chatgpt response

我觉得**有必要考虑，但要先确认你说的 PCANN 是哪一种方法，以及它具体要解决什么问题**。结合你现在的 GLP1R 项目，我不会因为 MD 计算成本高，就直接把 PCANN 当成替代方案。

你目前有 27 个候选物、每个 3 个 Boltz-2 预测模型，已经完成全受体 TM-score 比较。接下来真正需要回答的是：候选肽的结合姿态是否合理、界面是否可信，以及哪些候选值得进一步投入计算资源。

不同的 PCANN 方法可能对应不同的分析任务，不能仅凭名称判断它是否值得跑。

我查到的 PCANN 是 **Protein Complex Affinity by Neural Network**，也就是基于蛋白质复合物结构预测结合亲和力的神经网络方法。它利用 ESM-2 表征结合界面，再用图神经网络预测结合自由能相关指标。它不是 MD 模拟。<Cite refs={["turn212048search0","turn212048search1"]}/>

## 对你项目的判断

**值得试跑，适合作为辅助评分，而不是直接拿来判定 27 个候选物谁最好。**

- **优点：** 不需要先进行长时间 MD，就能从复合物结构获得额外的亲和力预测信息。
- **限制：** 原论文训练集包含 585 个异源二聚体复合物；作者报告的独立测试 MAE 约为 1.3 kcal/mol。这个结果不保证对你设计的 GLP1R—肽复合物同样准确。<Cite refs={["turn212048search1","turn212048search2"]}/>
- **特别要注意：** 你的设计对象是 GLP1R 与设计肽的复合物，而 PCANN 的论文验证不能直接证明它对这种受体—肽体系、尤其是从头设计的结合姿态，具有相同的预测精度。

我的建议是先挑 3–5 个结构质量有代表性的候选物测试 PCANN，检查输入格式、输出是否有效，以及结果是否与界面几何和 Boltz-2 指标相互印证。如果能顺利运行，再考虑是否扩展到 27 个候选物。

论文或项目报告中可以把它定位为**独立的结构亲和力预测指标**，不能把预测出的 $K_d$ 当成实验测量值，也不应将它与其他预测分数简单平均后宣称得到了真实亲和力。

你要是愿意，我建议下一步直接检查 PCANN 的官方代码和输入要求，再判断你的现有 Boltz-2 CIF 能否直接使用，以及在 RTX 5070 8 GB 显存上怎么运行。

---

# you asked

message time: 2026-10-22 22:19:31

先用RMSD值和TM评分进一步筛选吧，这一轮争取把candidate筛到10个以内

---

# chatgpt response

可以。这一轮我们先把范围收紧到 **8 个候选物左右**，用现有的受体结构 RMSD 和 TM-score 做一轮可复现的结构质控，不急着引入 PCANN 或 MD。

先明确一个原则：你现在算的是预测受体相对实验参考结构 7KI0 的**全局结构比较**，不是候选肽与受体之间的结合 RMSD。因此，这一轮筛选回答的是“哪些候选物的受体预测结构更接近参考结构，而且三个模型的结果比较稳定”，而不是“哪些候选物结合能力最强”。

从你已经提供的 TM-score 汇总看，值得优先进入这一轮筛选的候选物包括 `candidate_0082`、`candidate_0213`、`candidate_0096`、`candidate_0043`、`candidate_0044`、`candidate_0112`、`candidate_0228` 和 `candidate_0027`。不过，最终名单应当同时检查每个候选物的 RMSD 中位数、三个模型的 TM-score 波动，以及模型是否完整，不能只凭 TM-score 排名直接定稿。

## 1. 本轮筛选标准

采用以下规则，先定标准再看结果，避免为了保留某个候选物临时调整规则。

| 指标 | 作用 | 筛选方向 |
|---|---|---|
| TM-score 中位数 | 整体受体结构与参考结构的相似程度 | 越高越好 |
| 全局对齐 RMSD 中位数 | 对齐后结构的整体偏差 | 越低越好 |
| TM-score 标准差 | 同一候选物三个预测模型的一致性 | 越低越稳定 |
| 成功模型数 | 检查数据是否完整 | 必须 3/3 |

我建议对前三项分别进行排名，再计算平均排名，选出前 8 名。这样不会因为 TM-score 和 RMSD 的数值单位不同而直接相加，也能避免 RMSD 因数值范围较窄而被忽略。

## 2. 运行筛选脚本

在 WSL 终端中执行以下命令。脚本会读取已经计算完成的 81 个模型结果，不需要重新运行 US-align。

```bash
cat > ~/s功后，查看最终名单：

```bash
column -s,``bash
column -s,完整审计记录，原始结果不会被覆盖。

## 4. 这一轮结果该如何解释？

需要特别注意两点：

- **TM-score 高、RMSD 低**，只能说明全局受体结构更接近 7KI0 参考结构，不能说明设计肽一定结合得更好。
- **三个模型之间更稳定**，说明这组预测结果的整体结构表现更一致，但也不等于实验可重复性或结合稳定性。

因此，筛到 8 个以内之后，下一轮再对这些候选物检查局部结合口袋和肽—受体界面，才更有可能判断哪些值得保留。若全局指标筛掉了一个整体分数略低、但局部结合姿态很合理的候选物，也应允许后续基于局部证据重新审查。

**你先运行脚本，把输出的 `Shortlist` 表格贴给我。** 我们再结合具体的 TM-score、RMSD 和三个模型的波动，检查名单是否合理，并决定是否需要调整筛选规则。

---

# you asked

message time: 2026-10-22 22:24:40

column -s, -t < \
LOCAL_PATH \
| less -S怎么退出

---

# chatgpt response

按键盘上的 **`q`** 就能退出 `less -S`，回到终端命令行。

补充几个常用按键：

- `q`：退出
- ↑ / ↓：逐行查看
- `Space`：向下翻一页
- `g`：跳到文件开头
- `G`：跳到文件末尾
- `/关键词`：搜索关键词，按 Enter 确认

你现在直接按一下 **`q`** 就可以了。

---

# you asked

message time: 2026-10-22 22:25:43

=== Shortlist ===
 screen_rank      candidate  tm_median  tm_sd  rmsd_median_A  rank_tm  rank_rmsd  rank_stability  mean_rank
           1 candidate_0096     0.7782 0.0057         3.9800   3.0000     5.5000          3.0000     3.8333
           2 candidate_0082     0.7877 0.0173         3.7300   1.0000     1.0000         11.0000     4.3333
           3 candidate_0043     0.7765 0.0215         3.9800   4.0000     5.5000         15.0000     8.1667
           4 candidate_0200     0.7636 0.0212         3.9800   9.0000     5.5000         13.0000     9.1667
           5 candidate_0111     0.6877 0.0021         3.7700  26.0000     2.0000          1.0000     9.6667
           6 candidate_0175     0.7630 0.0097         4.0200  10.0000    13.0000          7.0000    10.0000
           7 candidate_0044     0.7732 0.0096         4.1000   5.0000    21.0000          6.0000    10.6667
           8 candidate_0173     0.7595 0.0160         4.0000  14.0000     9.0000         10.0000    11.0000

All-candidate audit:
LOCAL_PATH

Top-8 shortlist:
LOCAL_PATH
(usalign) ziguimu@DESKTOP-8RLFC97:~$ column -s, -t < \
LOCAL_PATH
candidate       models_successful  tm_median  tm_min   tm_max   tm_sd                 rmsd_median_A  rmsd_min_A  rmsd_max_A  rmsd_sd_A            complete_3_models  rank_tm  rank_rmsd  rank_stability  mean_rank           screen_rank  selected_top8  screening_note
candidate_0096  3                  0.77824    0.76881  0.77901  0.005679756450177545  3.98           3.88        4.12        0.12055427546683427  True               3.0      5.5        3.0             3.8333333333333335  1            True           入选：三模型完整，综合结构指标排名靠前
candidate_0082  3                  0.78772    0.76971  0.80432  0.017309786249402402  3.73           3.42        4.07        0.3251153641401773   True               1.0      1.0        11.0            4.333333333333333   2            True           入选：三模型完整，综合结构指标排名靠前
candidate_0043  3                  0.7765     0.75846  0.80133  0.02152443340330549   3.98           3.49        4.32        0.41725292090050137  True               4.0      5.5        15.0            8.166666666666666   3            True           入选：三模型完整，综合结构指标排名靠前
candidate_0200  3                  0.7636     0.75638  0.79609  0.02115266965026713   3.98           3.53        4.24        0.3592121007612821   True               9.0      5.5        13.0            9.166666666666666   4            True           入选：三模型完整，综合结构指标排名靠前
candidate_0111  3                  0.68772    0.68623  0.69036  0.002091514602706195  3.77           3.73        4.18        0.24906491790963506  True               26.0     2.0        1.0             9.666666666666666   5            True           入选：三模型完整，综合结构指标排名靠前
candidate_0175  3                  0.76296    0.75577  0.77499  0.00971103667655168   4.02           3.95        4.13        0.09073771725877457  True               10.0     13.0       7.0             10.0                6            True           入选：三模型完整，综合结构指标排名靠前
candidate_0044  3                  0.77325    0.76424  0.78352  0.00964685959263426   4.1            3.65        4.24        0.30827476921300795  True               5.0      21.0       6.0             10.666666666666666  7            True           入选：三模型完整，综合结构指标排名靠前
candidate_0173  3                  0.75946    0.74781  0.77943  0.01599139247637093   4.0            3.83        4.17        0.16999999999999993  True               14.0     9.0        10.0            11.0                8            True           入选：三模型完整，综合结构指标排名靠前
这个排名考虑boltz的各项数据了吗

---

# chatgpt response

没有。**你现在这份 Top-8 排名只考虑了受体结构的 TM-score、US-align RMSD 和三个模型之间的 TM-score 波动，没有纳入 Boltz-2 的其他预测指标。**

这意味着它目前是一个初步的**受体结构质控名单**，还不是综合候选物排名。我建议暂时不要把这 8 个候选物定为最终名单，而是把 Boltz-2 的置信度指标也纳入下一轮筛选。

## 1. 当前排名到底考虑了什么？

| 指标 | 是否纳入 | 当前用途 |
|---|---|---|
| 受体 TM-score 中位数 | 是 | 越高越好 |
| 受体全局对齐 RMSD 中位数 | 是 | 越低越好 |
| 三个模型的 TM-score 标准差 | 是 | 越低越稳定 |
| Boltz-2 的 ipTM | 否 | 评估预测的复合物界面置信度 |
| Boltz-2 的 pTM | 否 | 评估整体结构预测置信度 |
| PAE / 界面 PAE | 否 | 评估相对位置和界面的预测不确定性 |
| pLDDT | 否 | 评估局部结构置信度 |
| 界面接触、空间冲突等 | 否 | 检查结合姿态的几何合理性 |

这里需要区分：ipTM、pTM、PAE 和 pLDDT 都是预测置信度或不确定性相关指标，**不能直接等同于实验结合亲和力**。

## 2. 为什么现在的 Top-8 还不够合理？

你的结果里有几个很典型的例子：

<box border radius="lg" padding={3} gap={3}>
  <box gap={1}>
    <row align="center" justify="between">
      **candidate_0082**
      <badge color="success">值得保留</badge>
    </row>
    TM-score 中位数为 0.7877，RMSD 中位数为 3.73 Å，两项都很好。不过，TM-score 标准差为 0.0173，稳定性并不是最好的。
  </box>
  <divider color="subtle" />
  <box gap={1}>
    <row align="center" justify="between">
      **candidate_0096**
      <badge color="success">值得保留</badge>
    </row>
    TM-score 中位数为 0.7782，标准差为 0.0057，表现相当稳定。如果只看最高 TM-score，它会排在 0082 后面；但考虑稳定性后，它排到了第一。
  </box>
  <divider color="subtle" />
  <box gap={1}>
    <row align="center" justify="between">
      **candidate_0111**
      <badge color="warning">需要复核</badge>
    </row>
    TM-score 只有 0.6877，但 RMSD 中位数为 3.77 Å，三个模型的 TM-score 又很稳定。它因此进入了 Top-8。这个例子说明：不能把“稳定”误当成“结构正确”，也不能只凭一个全局指标判断好坏。
  </box>
</box>

另外，RMSD 和 TM-score 都来自同一次全局结构对齐，并不是两份完全独立的证据。当前方法给它们相同权重，可能会重复强调整体结构相似性。

## 3. 下一轮应该怎样结合 Boltz-2 数据？

我建议分两层处理，而不是直接把所有分数相加。

<box border radius="xl"       - 界面 PAE、相关置信度指标
      - 肽—受体界面接触和空间冲突
      - 同一候选物三个预测模型的结果一致性
    </box>
  </row>
</box>

最后再从两个层面综合挑选少于 10 个候选物。对于某些指标，如果没有经过已知阳性、阴性对照校准，就先作为辅助证据，不应人为设定一个看似精确的结合阈值。

## 4. 下一步先检查你已有的 Boltz-2 数据

你之前的项目里已经有这两个汇总文件：

- `boltz_sample_metrics.csv`：逐模型的预测指标。
- `boltz_candidate_summary.csv`：候选物层面的汇总指标。

我建议先确认这些文件的实际列名、每个候选物有几个模型，以及置信度指标是否齐全，再决定综合筛选规则。这样不需要重新运行 81 个 Boltz-2 预测模型。

**你先在 WSL 里运行下面的命令，把输出发给我：**

```bash
python3 - <<'PY'
import pandas as pd
from pathlib import Path

base = Path("LOCAL_PATH")

for name in [
    "boltz_sample_metrics.csv",
    "boltz_candidate_summary.csv",
]:
    path = base / name
    print(f"\n{'=' * 20} {name} {'=' * 20}")

    if not path.exists():
        print("NOT FOUND:", path)
        continue

    df = pd.read_csv(path)
    print("Shape:", df.shape)
    print("Columns:")
    print(df.columns.tolist())
    print("\nFirst 3 rows:")
    print(df.head(3).to_string(index=False))
PY
```

有了实际列名后，我们就能制定一套明确的综合筛选规则，既利用 Boltz-2 的预测信息，又避免把结构相似度和界面置信度混为一谈。

---

# you asked

message time: 2026-10-22 22:39:20

把pLDDT和界面pAE这两个数据也考虑进去，重新排个名

---

# chatgpt response

可以。我们把现有排名升级为 **5 项指标综合排名**：受体 TM-score、受体 RMSD、TM-score 稳定性、pLDDT 和界面 PAE。先读取实际数据列，避免把整体 PAE 错当成界面 PAE，或者把受体 pLDDT 错当成设计肽的 pLDDT。

请在 WSL 里运行下面这段命令，把输出完整贴给我：



拿到列名后，我会按以下原则重排：

- **TM-score：** 越高越好。
- **RMSD：** 越低越好。
- **TM-score 稳定性：** 三个模型的波动越小越好。
- **pLDDT：** 优先使用能明确对应到设计肽或界面区域的指标，并保留整体 pLDDT 作为辅助信息。
- **界面 PAE：** 越低通常越好，但必须确认它确实衡量结合双方的相对位置不确定性。

我会保留每个候选物的逐模型数据，先汇总三个模型，再生成完整排名和 **Top-8 短名单**。如果新指标使原来的候选物被挤出，也会列出原因。

需要强调：这仍然是结构与预测置信度的综合筛选，不是实验结合亲和力排名。

---

# you asked

message time: 2026-10-22 22:42:11

File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'pandas'
(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

这个报错是因为你当前在 **`(usalign)` 环境**，这个环境里没有安装 `pandas`。不用重新安装，也不用改环境；你之前的 Boltz-2 数据分析是在 `boltz` 环境中完成的。

**最简单的解决办法：把命令中的 `python3` 改成 `conda run -n boltz python`。**

重新完整复制运行下面的命令：



如果命令没有输出，改用下面这种方式更稳妥：



确认能输出 pandas 版本后，再运行上面的数据检查命令。

把输出发给我，我们就能继续把 **TM-score、RMSD、pLDDT 和界面 PAE** 整合起来，重新筛选少于 10 个候选物。

---

# you asked

message time: 2026-10-22 22:42:49

continue

    df = pd.read_csv(path)
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print(df.head(2).to_string(index=False))
PY
(usalign) ziguimu@DESKTOP-8RLFC97:~$ conda run -n boltz python -c "import pandas; print(pandas.__version__)"
3.0.6
(usalign) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

很好，已经确认 `boltz` 环境里的 pandas 可以正常使用，版本是 `3.0.6`。刚才的数据检查脚本还没有显示结果，我们重新执行一次。

**第一步：切换到 `boltz` 环境。**



看到终端提示符前面出现 `(boltz)` 后，复制运行下面的完整命令：



注意：最后的 `PY` 必须单独占一行，不能带其他字符。

**第二步：把输出发给我。**

我会根据实际列名确认 pLDDT 和界面 PAE 的具体字段，然后重新计算综合排名，输出：

- 27 个候选物的完整排名与各项指标；
- 每个候选物三个模型的稳定性；
- 新的 Top-8 名单；
- 原 Top-8 中哪些候选物被替换，以及替换依据。

我们先读取真实数据，再决定权重，不会预先假定某个候选物一定应该入选。

---

# you asked

message time: 2026-10-22 22:43:27

================================================================================
boltz_sample_metrics.csv
================================================================================
Shape: (81, 12)
Columns: ['candidate_id', 'model', 'cif_exists', 'confidence_json', 'confidence_score', 'ptm', 'iptm', 'complex_plddt', 'complex_iplddt', 'complex_pde', 'complex_ipde', 'protein_iptm']
  candidate_id   model  cif_exists                                                                                                                                            confidence_json  confidence_score      ptm     iptm  complex_plddt  complex_iplddt  complex_pde  complex_ipde  protein_iptm
candidate_0009 model_0        True LOCAL_PATH          0.816408 0.914119 0.949503       0.783135        0.704540     0.447534       0.85642      0.949503
candidate_0009 model_1        True LOCAL_PATH          0.805479 0.842524 0.876716       0.787670        0.692308     0.634546       2.25728      0.876716

================================================================================
boltz_candidate_summary.csv
================================================================================
Shape: (27, 28)
Columns: ['candidate_id', 'valid_samples', 'cif_count', 'confidence_json_count', 'confidence_score_median', 'confidence_score_min', 'confidence_score_max', 'ptm_median', 'ptm_min', 'ptm_max', 'iptm_median', 'iptm_min', 'iptm_max', 'complex_plddt_median', 'complex_plddt_min', 'complex_plddt_max', 'complex_iplddt_median', 'complex_iplddt_min', 'complex_iplddt_max', 'complex_pde_median', 'complex_pde_min', 'complex_pde_max', 'complex_ipde_median', 'complex_ipde_min', 'complex_ipde_max', 'protein_iptm_median', 'protein_iptm_min', 'protein_iptm_max']
  candidate_id  valid_samples  cif_count  confidence_json_count  confidence_score_median  confidence_score_min  confidence_score_max  ptm_median  ptm_min  ptm_max  iptm_median  iptm_min  iptm_max  complex_plddt_median  complex_plddt_min  complex_plddt_max  complex_iplddt_median  complex_iplddt_min  complex_iplddt_max  complex_pde_median  complex_pde_min  complex_pde_max  complex_ipde_median  complex_ipde_min  complex_ipde_max  protein_iptm_median  protein_iptm_min  protein_iptm_max
candidate_0009              3          3                      3                 0.805479              0.804038              0.816408    0.914119 0.842524 0.921103     0.942154  0.876716  0.949503              0.783135           0.769509           0.787670               0.692308            0.661057            0.704540            0.447534         0.435854         0.634546             0.990454          0.856420          2.257280             0.942154          0.876716          0.949503
candidate_0021              3          3                      3                 0.818587              0.796137              0.819053    0.903487 0.832100 0.905675     0.927628  0.859003  0.945586              0.787420           0.780421           0.791326               0.705377            0.678021            0.714139            0.470068         0.458704         0.668988             1.125345          1.111975          2.574003             0.927628          0.859003          0.945586

================================================================================
receptor_tmscore_vs_7KI0.csv
================================================================================
Shape: (81, 12)
Columns: ['candidate', 'model', 'model_cif', 'predicted_receptor_chain', 'predicted_receptor_sequence_length', 'sequence_alignment_score', 'sequence_identity_fraction', 'tm_normalized_by_reference_chain1', 'tm_normalized_by_predicted_chain2', 'aligned_length', 'usalign_aligned_rmsd_A', 'status']
     candidate  model                                                                                                                                      model_cif predicted_receptor_chain  predicted_receptor_sequence_length  sequence_alignment_score  sequence_identity_fraction  tm_normalized_by_reference_chain1  tm_normalized_by_predicted_chain2  aligned_length  usalign_aligned_rmsd_A status
candidate_0009      0 LOCAL_PATH                        A                                 395                     753.5                         1.0                            0.75716                            0.77658             362                    4.12     OK
candidate_0009      1 LOCAL_PATH                        A                                 395                     753.5                         1.0                            0.74729                            0.76649             357                    4.16     OK
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

数据列已经确认了。现在可以把 Boltz-2 指标合并进排名，不需要重新预测 81 个结构。

有一个重要的术语区别：你现有文件中有 `complex_ipde`，但没有名为 `interface_pae` 的列。`complex_ipde` 是界面预测距离误差（interface predicted distance error，iPDE），**不能直接称为 PAE**。我建议本轮先使用已有的 `complex_ipde` 作为界面误差指标，并在结果中明确标注，避免把不同指标混为一谈。

## 本轮综合排名方案

| 指标 | 数据列 | 趋势 | 用途 |
|---|---|---|---|
| 受体 TM-score | `tm_normalized_by_reference_chain1` | 越高越好 | 整体受体结构相似度 |
| 受体 RMSD | `usalign_aligned_rmsd_A` | 越低越好 | 整体结构偏差 |
| TM-score 标准差 | 由 3 个模型计算 | 越低越好 | 预测一致性 |
| 复合物 pLDDT | `complex_plddt` | 越高越好 | 整体局部结构置信度 |
| 界面 iPDE | `complex_ipde` | 越低通常越好 | 界面预测误差 |

我会让这 5 项指标各占一个排名维度，再对排名取平均，避免直接相加不同量纲的数值。最终输出所有候选物的完整排名和新的 Top-8 短名单。

## 运行新的综合排名脚本

在当前 `(boltz)` 环境下，完整复制运行以下命令。它会读取三个现有 CSV，保留原始文件，并生成新的结果文件。

```bash
cat > ~/rera
column -s, -PRP/GLP1R_Boltz2_20261022/audit/structure/candidate_5metrics_ranking.csv`

**有两点需要注意：**

1. 这版使用的是 `complex_plddt`（复合物整体 pLDDT）和 `complex_ipde`（界面 iPDE），不是尚未找到的独立界面 PAE 数据。
2. 五项指标暂时等权，是透明的初筛规则，不是经过实验校准的最优权重。尤其是全局 TM-score 与 RMSD 相关性较高，可能对受体整体结构相似性赋予了偏高的综合权重。

你把新生成的 Top-8 表格贴给我，我们就能逐个比较新旧名单，重点检查原来排名靠前的候选物是否因为界面误差较大或 pLDDT 较低而被替换。

---

# you asked

message time: 2026-10-22 22:45:02

还有没有必要考虑boltz的其他指标？

---

# chatgpt response

有必要，但我不建议把 Boltz-2 输出的所有指标都塞进综合排名。对于你现在的 GLP1R 项目，重点不是“指标越多越科学”，而是**每个新增指标能否提供已有指标没有提供的独立证据**。

目前你有 27 个候选物、每个 3 个预测模型，一共 81 个结构。比较合理的做法是把指标分成三层：

- **第一层：结构与界面可信度**——决定候选物是否值得进一步分析。
- **第二层：结合构象是否合理**——检查是否存在明显的结构性问题。
- **第三层：相对于实验参考复合物的合理性**——判断候选物是否在 GLP1R 上形成合理的结合模式。

你现有的受体 TM-score、RMSD、复合物 pLDDT 和界面 iPDE，主要覆盖前两层中的一部分，尚不能充分回答第三层的问题。

## 1. 其他 Boltz-2 指标，哪些值得加入？

根据 Boltz 的指标说明，除你已经使用的指标外，还值得检查 `complex_iplddt`、`iptm`、`ptm`、`complex_pde`，以及输出中是否有真正的 PAE 矩阵。它们的含义并不相同。<Cite refs={["turn245316search0","turn245316search1","turn245316search3"]}/>

| 指标 | 建议 | 原因 |
|---|---|---|
| `complex_iplddt` | **优先考虑** | 界面残基的局部结构置信度，比复合物整体 pLDDT 更贴近你的筛选目标 |
| `iptm` | **保留作对照** | 衡量链间相对位置的置信度；但你的基准校准项目已经表明，不能单独把它当作结合证据 |
| `ptm` | 暂不加入总排名 | 更偏向整体结构质量，和受体结构相似性、整体 pLDDT 有部分重叠 |
| `complex_pde` | 暂不加入总排名 | 是整个复合物的预测距离误差；你已有界面 iPDE，后者更直接针对界面 |
| `confidence_score` | 不建议再加一项 | 属于综合置信度分数，与已有置信度指标有重叠，重复计分会放大相同证据 |
| `PAE / interface PAE` | **值得查找** | 能提供残基间相对位置误差的信息，但要确认实际计算的是跨链界面 PAE |

以上是针对当前项目的筛选建议，并不意味着被暂时排除的指标没有价值。

## 2. 我最建议的下一步：先加入 `complex_iplddt`

你目前已有的字段中，它已经存在，不需要重新运行 Boltz-2。

建议先比较以下两项：

- `complex_plddt_median`：整个复合物的中位 pLDDT。
- `complex_iplddt_median`：界面相关 pLDDT 的中位数。

如果一个候选物整体 pLDDT 很高，但界面 pLDDT 较低，就值得进一步检查它是否属于“整体结构看起来不错，但界面不够可信”的情况。

同时，**不要把 `complex_iplddt` 和 `complex_ipde` 视为完全独立的证据**。可以先把它加入敏感性分析，观察 Top-8 是否发生明显变化，而不是立即把它当成一个同等独立的评分维度。

## 3. 再检查有没有真正的 PAE 数据

你的 `boltz_sample_metrics.csv` 没有 PAE 列，但这不代表预测输出中一定没有 PAE 矩阵。Boltz 的部分输出格式会保存单独的 PAE 数据。<Cite refs={["turn245316search3","turn245316search13"]}/>

在 `(bolthead -40
```

如果找到类似 `.npz` 的 PAE 文件，我们再确认其中是否有完整的残基对误差矩阵，以及如何根据受体链和 binder 链计算跨链 PAE。不要直接把整体 PAE 当成界面 PAE。

## 4. 我建议的最终筛选框架

<box border radius="lg" padding={3} gap={3}>
  <box gap={1}>
    <title size="md">第一层：主要排名依据</title>
    <text>受体参考结构相似度、局部界面置信度、界面预测误差，以及跨模型一致性。</text>
  </box>
  <divider color="subtle" />
  <box gap={1}>
    <title size="md">第二层：辅助验证</title>
    <text>ipTM、整体 pLDDT、受体 RMSD；检查候选物是否因某一指标异常而被过度加分或扣分。</text>
  </box>
  <divider color="subtle" />
  <box gap={1}>
    <title size="md">第三层：结构与生物学合理性</title>
    <text>将预测 binder 与 GLP1R–semaglutide 参考结构 7KI0 对照，检查结合位置、空间冲突、关键接触及受体构象。</text>
  </box>
</box>

特别提醒：即使一个候选物在这些指标上全部领先，也只能说明它在当前计算筛选标准下更值得优先研究，不能据此断定它具有更强的实验结合亲和力或激动活性。

**我的建议是：先把 `complex_iplddt` 纳入候选排名的敏感性分析，再检查 PAE 文件。** 这样能增加有价值的信息，而不会为了指标数量把同一种置信度证据重复计算好几次。

---

# you asked

message time: 2026-10-22 22:46:03

TM 有效模型数: 81
Boltz 有效模型数: 81
成功匹配模型数: 81

=== 五项指标综合排名 ===
符合完整性要求的候选物: 27
Top-8 数量: 8

方向：TM 高优先；RMSD、TM 波动、iPDE 低优先；pLDDT 高优先

=== 新的 Top-8 ===
 screen_rank   candidate_id  tm_median  rmsd_median_A   tm_sd  plddt_median  ipde_median  mean_rank
           1 candidate_0082    0.78772        3.73000 0.01413       0.81499      0.73510    3.20000
           2 candidate_0096    0.77824        3.98000 0.00464       0.79816      0.77298    5.10000
           3 candidate_0200    0.76360        3.98000 0.01727       0.80958      0.84101    6.70000
           4 candidate_0170    0.76059        4.02000 0.00893       0.82259      0.93397    8.00000
           5 candidate_0173    0.75946        4.00000 0.01306       0.80494      1.06279    9.60000
           6 candidate_0043    0.77650        3.98000 0.01757       0.79349      0.98033    9.70000
           7 candidate_0044    0.77325        4.10000 0.00788       0.79985      0.97209    9.80000
           8 candidate_0112    0.77090        4.13000 0.00873       0.80304      0.93902    9.80000

完整排名: LOCAL_PATH
Top-8 文件: LOCAL_PATH
(boltz) ziguimu@DESKTOP-8RLFC97:~$ column -s, -t < \
LOCAL_PATH
candidate_id    models_matched  tm_median  tm_min   tm_max   tm_sd                 rmsd_median_A  plddt_median        plddt_min           ipde_median         ipde_max            complete_3_models  rank_tm_median  rank_rmsd_median_A  rank_tm_sd  rank_plddt_median  rank_ipde_median  mean_rank  screen_rank  selected_top8  screening_note
candidate_0082  3               0.78772    0.76971  0.80432  0.014133381289226827  3.73           0.8149946331977844  0.8126997947692871  0.7350986003875732  0.7744002342224121  True               1.0             1.0                 11.0        2.0                1.0               3.2        1            True           入选：五项指标综合排名前8
candidate_0096  3               0.77824    0.76881  0.77901  0.004637501722072164  3.98           0.7981579303741455  0.7931815981864929  0.7729823589324951  1.326340675354004   True               3.0             5.5                 3.0         12.0               2.0               5.1        2            True           入选：五项指标综合排名前8
candidate_0200  3               0.7636     0.75638  0.79609  0.01727108244693679   3.98           0.8095817565917969  0.8075218200683594  0.8410118222236633  0.8637201189994812  True               9.0             5.5                 13.0        3.0                3.0               6.7        3            True           入选：五项指标综合排名前8
candidate_0170  3               0.76059    0.75343  0.77491  0.008930088963100455  4.02           0.8225916028022766  0.8067049384117126  0.933971643447876   0.9975048303604126  True               12.0            13.0                9.0         1.0                5.0               8.0        4            True           入选：五项指标综合排名前8
candidate_0173  3               0.75946    0.74781  0.77943  0.013056917281230228  4.0            0.8049358129501343  0.7980633974075317  1.0627906322479248  1.27519690990448    True               14.0            9.0                 10.0        4.0                11.0              9.6        5            True           入选：五项指标综合排名前8
candidate_0043  3               0.7765     0.75846  0.80133  0.01757462628020546   3.98           0.7934862375259399  0.7826036810874939  0.9803325533866882  1.068151354789734   True               4.0             5.5                 15.0        15.0               9.0               9.7        6            True           入选：五项指标综合排名前8
candidate_0044  3               0.77325    0.76424  0.78352  0.00787662787407571   4.1            0.7998507022857666  0.7975003123283386  0.9720885157585144  1.0208114385604858  True               5.0             21.0                6.0         9.0                8.0               9.8        7            True           入选：五项指标综合排名前8
candidate_0112  3               0.7709     0.76148  0.78281  0.008727691561919436  4.13           0.803044855594635   0.7894522547721863  0.9390185475349426  0.9514812231063844  True               6.0             23.0                8.0         6.0                6.0               9.8        8            True           入选：五项指标综合排名前8
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

这版结果已经可以作为第一轮筛选的基础。不过，我建议**暂时不要把这 8 个候选物直接定为最终实验候选物**。从表格中已经能看到几个值得进一步检查的地方。

## 1. 当前 Top-8 怎么看？

<text color="secondary" size="sm">以下是计算筛选优先级，不是实验结合能力的预测排名。</text>

| 候选物 | 主要优势 | 需要注意的地方 |
|---|---|---|
| **candidate_0082** | TM-score、RMSD、iPDE 均排名第一，pLDDT 排名第二 | TM 波动排名第 11，并非最稳定 |
| **candidate_0096** | TM 波动排名第 3，iPDE 排名第 2 | pLDDT 排名第 12 |
| **candidate_0200** | pLDDT 排名第 3，iPDE 排名第 3 | TM 波动排名第 13 |
| **candidate_0170** | pLDDT 排名第一，TM 波动排名第 9 | TM-score 和 RMSD 分别排第 12、第 13 |
| **candidate_0173** | RMSD 排名第 9，pLDDT 排名第 4 | iPDE 排名第 11 |
| **candidate_0043** | TM-score 排名第 4，RMSD 排名第 5.5 | pLDDT 排名第 15，TM 波动排名第 15 |
| **candidate_0044** | TM 波动排名第 6，TM-score 排名第 5 | RMSD 排名第 21 |
| **candidate_0112** | TM-score 排名第 6，pLDDT、iPDE 排名第 6 | RMSD 排名第 23 |

这里有三个值得关注的候选物：

- **0082：当前综合表现最强。** 五项指标中有三项排名第一，且 pLDDT 较高。
- **0096：稳定性优势明显。** 三个模型的 TM-score 波动较小，但界面误差的最大值达到 1.32634，值得检查模型间的差异。
- **0170：局部置信度优势明显。** pLDDT 排名第一，但整体受体结构拟合相对靠后。

这些差异说明，综合排名之外仍应保留各指标的单独结果。

## 2. 目前最重要的三个方法学问题

**第一，RMSD 与 TM-score 可能重复计分。**

它们都来自受体与 7KI0 的整体结构对齐。五项指标等权时，受体整体结构相似性实际上获得了两次计分。因此，这个排名可以用于初筛，但不应视为唯一且客观的排序标准。

**第二，当前的 iPDE 不是 PAE。**

`complex_ipde` 与 `complex_iplddt` 都值得研究，但前者是距离误差相关指标，后者是界面局部置信度指标。我们还需要确认 Boltz 输出中是否存在真正的跨链 PAE 数据。

**第三，受体结构相似不等于 binder 结合模式合理。**

即使受体的 TM-score 很高，也不能保证设计的 binder 位于合理的结合位置，更不能证明它能够结合或激活 GLP1R。

## 3. 下一步我建议做什么？

我建议先不要继续增加综合评分权重，而是做一轮更有判别力的结构审查：

<box border radius="lg" padding={3} gap={3}>
  <row align="start" gap={3}>
    <icon name="check-circle" size="xl" color="success" />
    <box flex="1" gap={1}>
      **步骤一：加入 `complex_iplddt` 做敏感性分析**

      <text color="secondary" size="sm">观察它是否改变 Top-8，特别是 0082、0096、0200 和 0170 的相对位置。</text>
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <icon name="scan-search" size="xl" />
    <box flex="1" gap={1}>
      **步骤二：检查 binder–受体界面**

      <text color="secondary" size="sm">在受体结构对齐后，分析界面接触数、空间冲突、界面埋藏表面积及关键接触残基，而不是只看整体结构指标。</text>
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <icon name="git-compare" size="xl" />
    <box flex="1" gap={1}>
      **步骤三：比较三个模型的一致性**

      <text color="secondary" size="sm">除了 TM-score 波动，还要检查三个模型的 binder 是否落在相似位置、是否形成相似的界面。</text>
    </box>
  </row>
</box>

对于你的 GLP1R 项目，**步骤二最有价值**。它能弥补当前排名对受体整体结构拟合依赖较重的问题。

最后还有一个关键限制：你目前使用的 7KI0 是 GLP1R 与 semaglutide 的实验复合物。它可以作为受体结构和参考结合模式，但如果设计目标是新的 GLP1R 激动剂，不能简单要求新 binder 完全复制 semaglutide 的结合模式；还需要结合设计策略和可能的受体激活机制来判断。

我的建议是保留这 8 个作为**结构初筛名单**，接下来重点比较它们的界面质量，再决定是否缩减为 3–5 个深入分析的候选物。

---

# you asked

message time: 2026-10-22 22:46:39

这次8条和上次8条有什么区别

---

# chatgpt response

这次和上次的 Top-8 **有 3 个候选物发生了变化**：`candidate_0111` 被移出，`candidate_0170` 和 `candidate_0112` 进入；`candidate_0082`、`candidate_0096`、`candidate_0200`、`candidate_0173`、`candidate_0043`、`candidate_0044` 都保留。

## 1. 新旧名单对比

| 候选物 | 上次排名 | 这次排名 | 变化 |
|---|---:|---:|---|
| `candidate_0082` | 2 | 1 | ↑ 1 |
| `candidate_0096` | 1 | 2 | ↓ 1 |
| `candidate_0200` | 4 | 3 | ↑ 1 |
| `candidate_0170` | 未进 Top-8 | 4 | **新进入** |
| `candidate_0173` | 8 | 5 | ↑ 3 |
| `candidate_0043` | 3 | 6 | ↓ 3 |
| `candidate_0044` | 7 | 7 | 不变 |
| `candidate_0112` | 未进 Top-8 | 8 | **新进入** |

上次入选、这次被替换的是：

| 候选物 | 上次排名 | 这次情况 |
|---|---:|---|
| `candidate_0111` | 5 | 被 `candidate_0170` 挤出 |
| `candidate_0175` | 6 | 被 `candidate_0112` 挤出 |

更正一下：两份名单的实际交集是 6 个候选物，因此是 **2 个进入、2 个退出**，不是 3 个发生替换。

## 2. 为什么排名发生变化？

两次使用的综合评分指标不同：

- **上次**：TM-score、RMSD、TM-score 波动。
- **这次**：TM-score、RMSD、TM-score 波动、复合物 pLDDT、界面 iPDE。

新加入的两个指标改变了部分候选物的相对优势。

<box gap={3}>
  <row align="start" gap={3}>
    <box background="surface-secondary" radius="lg" padding={2}>
      <icon name="trending-up" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **candidate_0170：新进入第 4 名**

      pLDDT 中位数为 `0.82259`，在这次 Top-8 中排名第一；iPDE 中位数为 `0.93397`。它虽然整体受体 TM-score 排名第 12，但新增的置信度信息提升了综合位置。
    </box>
  </row>
  <row align="start" gap={3}>
    <box background="surface-secondary" radius="lg" padding={2}>
      <icon name="trending-up" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **candidate_0112：新进入第 8 名**

      TM-score 排名第 6、pLDDT 排名第 6、iPDE 排名第 6，几项指标相对均衡；但 RMSD 排名第 23，说明其综合优势并不代表整体结构拟合也很好。
    </box>
  </row>
  <row align="start" gap={3}>
    <box background="surface-secondary" radius="lg" padding={2}>
      <icon name="trending-down" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **candidate_0111：退出 Top-8**

      上次主要依靠很低的 RMSD 和很小的 TM-score 波动进入名单，但它的 TM-score 中位数只有 `0.6877`。加入界面和置信度指标后，它不再占据前八。
    </box>
  </row>
  <row align="start" gap={3}>
    <box background="surface-secondary" radius="lg" padding={2}>
      <icon name="trending-down" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **candidate_0175：退出 Top-8**

      上次依靠较好的 TM-score 稳定性进入名单；这次其他候选物在新增指标和综合排名中表现更好。
    </box>
  </row>
</box>

## 3. 这次结果说明什么？

这次排名比上次多考虑了界面误差和复合物置信度，因此筛选依据更丰富；但它仍然是**计算指标驱动的初筛**，不能直接证明哪个 binder 更强。

还有一个值得注意的地方：`candidate_0082` 仍然位居第一，而 `candidate_0096` 仍然位居前二，说明它们在新旧两套规则下都具有较强的综合竞争力。

下一步最值得做的是对这 8 个候选物进行**局部结合界面审查**，尤其是界面接触、空间冲突和三个模型的结合姿态一致性。这样比继续给更多相关的置信度指标加权，更可能帮助你判断哪些候选物值得深入研究。

---

# you asked

message time: 2026-10-22 22:48:47

两次取并集

---

# chatgpt response

两次 Top-8 取并集后，一共有 **10 个候选物**，可以作为下一轮结构审查的候选池。

## 两次 Top-8 的并集

| 候选物 | 上次排名（3 指标） | 这次排名（5 指标） | 状态 |
|---|---:|---:|---|
| `candidate_0082` | 2 | 1 | 两次入选 |
| `candidate_0096` | 1 | 2 | 两次入选 |
| `candidate_0200` | 4 | 3 | 两次入选 |
| `candidate_0043` | 3 | 6 | 两次入选 |
| `candidate_0044` | 7 | 7 | 两次入选 |
| `candidate_0173` | 8 | 5 | 两次入选 |
| `candidate_0175` | 6 | — | 仅上次入选 |
| `candidate_0111` | 5 | — | 仅上次入选 |
| `candidate_0170` | — | 4 | 仅这次入选 |
| `candidate_0112` | — | 8 | 仅这次入选 |

## 建议怎么使用这 10 个候选物

- **优先审查：** `candidate_0082`、`candidate_0096`、`candidate_0200`。它们两次都入选，且这次排名前三。
- **继续保留：** `candidate_0043`、`candidate_0044`、`candidate_0173`。它们两次都进入 Top-8。
- **作为补充对照：** `candidate_0175`、`candidate_0111`、`candidate_0170`、`candidate_0112`。它们只在一套排名规则下进入 Top-8，可以检查是否存在特定指标偏好造成的排名变化。

注意，**两次入选不等于两份独立证据**，因为两套排名都使用了相同的结构预测结果，而且都包含 TM-score 和 RMSD。

下一步可以对这 10 个候选物统一进行界面接触、空间冲突、界面埋藏表面积，以及三个模型结合姿态一致性的比较，再缩小到 3–5 个重点候选物。

---

# you asked

message time: 2026-10-22 23:05:26

"LOCAL_PATH"这个表里面各项数据的最大值所属candidate都包括在以上10条吗

---

# chatgpt response

目前还不能仅凭刚才显示的前两行判断所有指标的最大值是否都属于这 10 个候选物。可以直接读取你指定的 `boltz_candidate_summary.csv`，逐列检查最大值所属的 candidate，并判断是否在并集中。

在 WSL 的 `(boltz)` 环境下运行下面这段完整代码：



这段代码会检查 `confidence_score`、`ptm`、`iptm`、`complex_plddt`、`complex_iplddt`、`complex_pde`、`complex_ipde`、`protein_iptm` 等数值列的最大值；如果某项存在并列最大值，也会全部列出。

**把运行结果发给我**，我就能准确告诉你：这 10 个候选物覆盖了多少项指标的最大值，哪些最大值来自并集之外，以及是否有必要把并集扩充。注意，指标最大值只表示该项数值最高，并不意味着该候选物整体最好。

---

# you asked

message time: 2026-10-22 23:06:12

检查指标数: 24
最大值全部属于并集: 17
最大值不全部属于并集: 7

不在并集内的最大值所属候选物：
                 指标      最大值 最大值所属candidate  是否全部在10条并集中
            ptm_max 0.936657 candidate_0051        False
 complex_pde_median 0.671088 candidate_0153        False
    complex_pde_min 0.564374 candidate_0071        False
    complex_pde_max 0.826966 candidate_0051        False
complex_ipde_median 2.673174 candidate_0153        False
   complex_ipde_min 2.436830 candidate_0153        False
   complex_ipde_max 4.069020 candidate_0051        False
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# you asked

message time: 2026-10-22 23:06:25

=== 各数值指标的最大值及所属候选物 ===
                     指标      最大值 最大值所属candidate  是否全部在10条并集中
confidence_score_median 0.846675 candidate_0170         True
   confidence_score_min 0.841817 candidate_0082         True
   confidence_score_max 0.848151 candidate_0200         True
             ptm_median 0.926161 candidate_0082         True
                ptm_min 0.920315 candidate_0082         True
                ptm_max 0.936657 candidate_0051        False
            iptm_median 0.953255 candidate_0096         True
               iptm_min 0.950823 candidate_0082         True
               iptm_max 0.960147 candidate_0096         True
   complex_plddt_median 0.822592 candidate_0170         True
      complex_plddt_min 0.812700 candidate_0082         True
      complex_plddt_max 0.824906 candidate_0170         True
  complex_iplddt_median 0.764683 candidate_0082         True
     complex_iplddt_min 0.761051 candidate_0082         True
     complex_iplddt_max 0.768640 candidate_0200         True
     complex_pde_median 0.671088 candidate_0153        False
        complex_pde_min 0.564374 candidate_0071        False
        complex_pde_max 0.826966 candidate_0051        False
    complex_ipde_median 2.673174 candidate_0153        False
       complex_ipde_min 2.436830 candidate_0153        False
       complex_ipde_max 4.069020 candidate_0051        False
    protein_iptm_median 0.953255 candidate_0096         True
       protein_iptm_min 0.950823 candidate_0082         True
       protein_iptm_max 0.960147 candidate_0096         True

=== 汇总 ===
检查指标数: 24
最大值全部属于并集: 17
最大值不全部属于并集: 7

不在并集内的最大值所属候选物：
                 指标      最大值 最大值所属candidate  是否全部在10条并集中
            ptm_max 0.936657 candidate_0051        False
 complex_pde_median 0.671088 candidate_0153        False
    complex_pde_min 0.564374 candidate_0071        False
    complex_pde_max 0.826966 candidate_0051        False
complex_ipde_median 2.673174 candidate_0153        False
   complex_ipde_min 2.436830 candidate_0153        False
   complex_ipde_max 4.069020 candidate_0051        False
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

这份结果很有价值。我的判断是：**现有 10 个候选物覆盖了多数指标的最大值，但 `candidate_0051` 和 `candidate_0153` 值得加入下一轮审查；`candidate_0071` 暂时不必仅凭一个指标就加入。**

不过，要特别区分两件事：**最大值覆盖率**与**候选物质量**不是一回事。

## 1. 10 个候选物覆盖了哪些指标？

<box border radius="lg" padding={3} gap={2}>
  <row align="center" justify="between">
    <text color="secondary" size="sm">最大值位于并集内</text>
    <title size="xl" color="success">17 / 24</title>
  </row>
  <box background="surface-tertiary" height="8px" radius="full" clip>
    <box background="surface-inverted" height="8px" radius="full" width="70.8333%" />
  </box>
  <text color="secondary" size="sm">约 70.8% 的数值列，其最大值所属候选物在这 10 个之中。</text>
</box>

但这 24 列并不是 24 个独立的生物学证据：每个主要指标往往都有 median、min、max 三个统计列。例如 `iptm_median`、`iptm_min`、`iptm_max` 都属于同一个指标。因此，不能把 17/24 解读为覆盖了 70.8% 的独立评价标准。

## 2. 并集之外的三个候选物，分别意味着什么？

| 候选物 | 领先指标 | 我的建议 |
|---|---|---|
| `candidate_0051` | `ptm_max`、`complex_pde_max`、`complex_ipde_max` | 加入审查池，检查整体结构置信度及误差分布 |
| `candidate_0153` | `complex_pde_median`、`complex_ipde_median`、`complex_ipde_min` | **优先加入审查池**，检查它的界面误差是否确实异常 |
| `candidate_0071` | `complex_pde_min` | 暂时保留为备选，单个最小值不足以支持入选 |

这里有一个容易误读的地方：`complex_pde` 和 `complex_ipde` 是误差类指标，**越大通常不是优势**。因此，`candidate_0051` 拥有最大的 `complex_ipde_max` 并不意味着它更好；相反，它可能在某个模型中有较大的界面误差。

`candidate_0153` 的 `complex_ipde_median = 2.673174` 是全体候选物的最大值，也不是优势。是否值得保留，需要看完整分布、模型间波动和实际界面结构。

## 3. 我建议将审查池扩展到 12 个，而不是直接扩大到 13 个

<box gap={2}>
  <row align="start" gap={2}>
    <icon name="check-circle" color="success" size="lg" />
    <box flex="1" gap={1}>
      **原有 10 个：继续保留**

      两次 Top-8 的并集，作为已有排名支持的候选池。
    </box>
  </row>
  <row align="start" gap={2}>
    <icon name="plus-circle" size="lg" />
    <box flex="1" gap={1}>
      **新增 `candidate_0051` 和 `candidate_0153`**

      作为探索性补充候选物，不直接认定优于原有 10 个。
    </box>
  </row>
  <row align="start" gap={2}>
    <icon name="minus-circle" size="lg" />
    <box flex="1" gap={1}>
      **暂不新增 `candidate_0071`**

      目前只知道它的 `complex_pde_min` 最大，缺乏足够证据支持优先级提升。
    </box>
  </row>
</box>

## 4. 下一步最值得做的分析

不要再用“某列的最大值是谁”决定最终候选物。建议对这 12 个候选物统一提取：

1. 三个模型的 `complex_iplddt`、`complex_ipde` 和 `iptm`；
2. 三个模型的界面误差波动；
3. binder–受体界面接触数、空间冲突及界面埋藏表面积；
4. 对齐 7KI0 后的结合位置和结合姿态一致性。

这样才能判断 `candidate_0051` 是否只是某个模型的整体置信度高，`candidate_0153` 是否确实有界面问题，以及它们是否有理由进入最终的 3–5 个重点候选物名单。

---

# you asked

message time: 2026-10-22 23:07:14

0153加进去

---

# chatgpt response

好，把 `candidate_0153` 加入原来的两次 Top-8 并集，候选池从 **10 个扩展到 11 个**。它先作为新增的探索性候选物保留，不直接认定它优于原有候选物。

在 WSL 的 `(boltz)` 环境中运行下面的命令，生成新的 11 候选名单文件，不覆盖之前的结果：



新文件路径：

`LOCAL_PATH

这份名单保留原来 10 个候选物并加入 `candidate_0153`，方便下一轮统一做界面结构审查。

---

# you asked

message time: 2026-10-22 23:08:42

这11个候选里面包括D13D41D44吗

---

# chatgpt response

目前我能确认这 11 个候选物的编号是：

`candidate_0082`、`candidate_0096`、`candidate_0200`、`candidate_0043`、`candidate_0044`、`candidate_0173`、`candidate_0175`、`candidate_0111`、`candidate_0170`、`candidate_0112`、`candidate_0153`。

但我现在**无法确认 D13、D41、D44 分别对应哪个 `candidate_####` 编号**，所以不能直接判断它们是否都在这 11 个里面。

你可以在 WSL 里运行下面的命令，查找项目中有没有 D13、D41、D44 的映射记录：



把输出贴给我，我就能帮你核对它们是否在候选池中，并列出对应编号。

---

# you asked

message time: 2026-10-22 23:13:14

D13-0165、D44-0173、D41-0241

---

# chatgpt response

对应关系明确了：

| 候选代号 | Boltz 编号 | 是否在当前 11 个候选池中 |
|---|---|---|
| D13 | `candidate_0165` | ❌ 不在 |
| D44 | `candidate_0173` | ✅ 在 |
| D41 | `candidate_0241` | ❌ 不在 |

因此，当前 11 个候选物**只包含 D44，不包含 D13 和 D41**。

建议先不要因为它们没入选就直接排除：如果 D13、D41、D44 是你们原先重点关注的设计序列，可以把它们作为一组“原始重点候选”单独标记，与结构指标筛选出的 11 个候选物比较。注意，D44 已经在池中，加入 D13 和 D41 后，去重后的候选池将扩大到 **13 个**。

---

# you asked

message time: 2026-10-22 23:18:40

这样吧，把原始27条candidate的

| confidence_score_median | confidence_score_min | confidence_score_max | ptm_median | ptm_min | ptm_max | iptm_median | iptm_min | iptm_max | complex_plddt_median | complex_plddt_min | complex_plddt_max | complex_iplddt_median | complex_iplddt_min | complex_iplddt_max | complex_pde_median | complex_pde_min | complex_pde_max | complex_ipde_median | complex_ipde_min | complex_ipde_max | protein_iptm_median | protein_iptm_min | protein_iptm_max |
| ----------------------- | -------------------- | -------------------- | ---------- | ------- | ------- | ----------- | -------- | -------- | -------------------- | ----------------- | ----------------- | --------------------- | ------------------ | ------------------ | ------------------ | --------------- | --------------- | ------------------- | ---------------- | ---------------- | ------------------- | ---------------- | ---------------- |

这些指标全部换成只保留3个的平均值，包括tm和rmsd，列成一张表，然后把至少有其中一项指标超过

| candidate_0173 的保留，其他淘汰（0173保留） |
| ------------------------------- |

---

# chatgpt response

可以。我们把原始 27 条 candidate 统一到**三模型均值表**，再以 `candidate_0173` 为基准做筛选。这里需要注意两点：

1. 原来每项 Boltz 指标的 `median / min / max` 全部替换为三个模型的算术平均值；TM-score 和 RMSD 也分别计算三个模型的平均值。
2. “超过 `candidate_0173`”按**指标表现更好**来判断，而不是一律比较数值大小：置信度和 TM-score 越高越好；PDE、iPDE 和 RMSD 作为误差指标，越低越好。

筛选规则是：**只要至少一项指标优于 `candidate_0173`，就保留；所有指标都没有优于它，才淘汰；`candidate_0173` 本身始终保留。** 这是一条较宽松的初筛规则，并不意味着入选候选物整体优于基准。

## 运行脚本

在 WSL 中激活 `boltz` 环境，运行下面的完整脚本。它会读取原始模型级数据、计算均值、逐项与 `candidate_0173` 比较，并输出包含 27 个候选物的完整结果表，不覆盖原文件。

```bash
conda activate boltz
cat > LOCAL_PATH <<'PY'
from pathlib import Path
import re
import numpy as np
import pandas as pd

ROOT = Path("LOCAL_PATH")
AUDIT = ROOT / "audit" / "structure"

BOLTZ_FILE = ROOT / "boltz_sample_metrics.csv"
STRUCTURE_FILE = AUDIT / "per_model_structure_metrics.csv"

BASELINE = "candidate_0173"
EXPECTED_MODELS = 3

# 三模型均值：所有这些指标都按越大越好处理
HIGHER_IS_BETTER = [
    "confidence_score",
    "ptm",
    "iptm",
    "complex_plddt",
    "complex_iplddt",
    "protein_iptm",
    "tm_score",
]

# 三模型均值：这些指标按越小越好处理
LOWER_IS_BETTER = [
    "complex_pde",
    "complex_ipde",
    "rmsd_A",
]

ALL_METRICS = HIGHER_IS_BETTER + LOWER_IS_BETTER


def find_candidate_column(df, label):
    """识别 candidate 编号列；如果没有标准列，则从文本列中提取编号。"""
    aliases = [
        "candidate_id", "candidate", "candidate_name",
        "target_id", "name", "sample", "sample_name",
        "model", "model_name", "file", "filename"
    ]
    normalized = {str(c).strip().lower(): c for c in df.columns}

    for alias in aliases:
        if alias in normalized:
            col = normalized[alias]
            extracted = df[col].astype(str).str.extract(
                r"(candidate[_-]?\d+)", flags=re.I, expand=False
            )
            if extracted.notna().sum() > 0:
                return extracted.str.lower().str.replace("-", "_", regex=False)
            if alias in ("candidate_id", "candidate", "candidate_name"):
                return df[col].astype(str).str.lower()

    # 兜底：检查其他文本列中是否包含 candidate_数字
    for col in df.columns:
        if df[col].dtype == object:
            extracted = df[col].astype(str).str.extract(
                r"(candidate[_-]?\d+)", flags=re.I, expand=False
            )
            if extracted.notna().sum() > 0:
                return extracted.str.lower().str.replace("-", "_", regex=False)

    raise ValueError(
        f"{label} 中找不到 candidate 编号列。\n"
        f"现有列名：{list(df.columns)}"
    )


def normalized_name(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def find_metric_column(df, metric, aliases=()):
    """按指标名称或别名识别列，避免把 median/min/max 列误当原始模型值。"""
    names = [metric, *aliases]
    norm_cols = {normalized_name(c): c for c in df.columns}

    for name in names:
        key = normalized_name(name)
        if key in norm_cols:
            return norm_cols[key]

    return None


def load_model_metrics(path, metrics, label, aliases=None):
    if not path.exists():
        raise FileNotFoundError(f"找不到文件：{path}")

    df = pd.read_csv(path)
    df["_candidate"] = find_candidate_column(df, label)

    # 只保留 candidate_#### 格式的候选编号
    df = df[df["_candidate"].str.match(r"candidate_\d+", na=False)].copy()

    if df.empty:
        raise ValueError(f"{label} 中没有解析出 candidate_#### 编号。")

    aliases = aliases or {}
    selected = {"_candidate": df["_candidate"]}

    missing = []
    for metric in metrics:
        col = find_metric_column(df, metric, aliases.get(metric, ()))
        if col is None:
            missing.append(metric)
        else:
            selected[metric] = pd.to_numeric(df[col], errors="coerce")

    if missing:
        raise ValueError(
            f"{label} 缺少模型级指标列：{missing}\n"
            f"文件列名：{list(df.columns)}\n"
            "请检查该文件是否存储了每个模型的原始指标，而不是只有 median/min/max 汇总值。"
        )

    out = pd.DataFrame(selected)
    return out


# 1. 读取 Boltz 每个模型的指标
boltz_aliases = {
    "confidence_score": ("confidence",),
    "ptm": ("ptm_score",),
    "iptm": ("iptm_score",),
    "complex_plddt": ("plddt", "complex_plddt_score"),
    "complex_iplddt": ("iplddt",),
    "complex_pde": ("pde",),
    "complex_ipde": ("ipde",),
    "protein_iptm": ("protein_iptm_score",),
}

boltz_metrics = [
    "confidence_score", "ptm", "iptm", "complex_plddt",
    "complex_iplddt", "complex_pde", "complex_ipde", "protein_iptm"
]

boltz = load_model_metrics(
    BOLTZ_FILE, boltz_metrics, "Boltz 模型指标", boltz_aliases
)

# 2. 读取每个模型的结构指标
structure_aliases = {
    "tm_score": (
        "tm_normalized_by_reference_chain1",
        "tm_normalized_by_predicted_chain2",
        "tm",
        "tmscore",
    ),
    "rmsd_A": (
        "usalign_aligned_rmsd_A",
        "rmsd",
        "aligned_rmsd",
    ),
}

structure = load_model_metrics(
    STRUCTURE_FILE, ["tm_score", "rmsd_A"],
    "结构指标", structure_aliases
)

# 若结构文件同时存在两个 TM-score 归一化列，优先使用参考链归一化 TM-score
if "tm_normalized_by_reference_chain1" in STRUCTURE_FILE.read_text(
    encoding="utf-8", errors="ignore"
):
    pass  # 实际列选择由 load_model_metrics 的别名顺序决定

# 3. 分别计算各指标的三个模型算术平均值
def aggregate(df, metrics, label):
    counts = df.groupby("_candidate").size()
    bad = counts[counts != EXPECTED_MODELS]
    if not bad.empty:
        raise ValueError(
            f"{label} 中以下 candidate 的模型数量不是 3：\n{bad.to_string()}"
        )

    means = df.groupby("_candidate")[metrics].mean()
    means = means.rename(columns={m: f"{m}_mean" for m in metrics})
    return means


boltz_mean = aggregate(boltz, boltz_metrics, "Boltz 指标")
structure_mean = aggregate(structure, ["tm_score", "rmsd_A"], "结构指标")

# 4. 合并，要求两边都有相同的 27 个 candidate
combined = boltz_mean.join(structure_mean, how="outer").reset_index()
combined = combined.rename(columns={"_candidate": "candidate_id"})
combined = combined.sort_values("candidate_id").reset_index(drop=True)

if len(combined) != 27:
    print(f"警告：合并后得到 {len(combined)} 个候选物，而不是预期的 27 个。")

mean_cols = [f"{m}_mean" for m in ALL_METRICS]
missing_values = combined[mean_cols].isna().sum()
if missing_values.any():
    print("警告：以下均值列存在缺失值：")
    print(missing_values[missing_values > 0].to_string())

if BASELINE not in set(combined["candidate_id"]):
    raise ValueError(f"基准 {BASELINE} 不在合并结果中。")

baseline = combined.loc[
    combined["candidate_id"] == BASELINE
].iloc[0]

# 5. 逐项判断是否优于 candidate_0173
comparison_cols = []

for metric in HIGHER_IS_BETTER:
    col = f"{metric}_mean"
    out_col = f"better_{metric}"
    combined[out_col] = combined[col] > baseline[col]
    comparison_cols.append(out_col)

for metric in LOWER_IS_BETTER:
    col = f"{metric}_mean"
    out_col = f"better_{metric}"
    combined[out_col] = combined[col] < baseline[col]
    comparison_cols.append(out_col)

# 基准自身强制保留；其他候选只要至少一项更优就保留
combined["better_metric_count"] = combined[comparison_cols].sum(axis=1)
combined["decision"] = np.where(
    (combined["candidate_id"] == BASELINE)
    | (combined["better_metric_count"] >= 1),
    "保留",
    "淘汰"
)
combined.loc[
    combined["candidate_id"] == BASELINE, "decision"
] = "保留（基准）"

# 6. 输出：均值、逐项比较、最终决定
mean_table_file = AUDIT / "candidate_27_three_model_means.csv"
decision_file = AUDIT / "candidate_27_filter_vs_0173.csv"
retained_file = AUDIT / "candidate_retained_vs_0173.csv"

combined.to_csv(mean_table_file, index=False)

decision_cols = [
    "candidate_id", *mean_cols,
    *comparison_cols, "better_metric_count", "decision"
]
combined[decision_cols].to_csv(decision_file, index=False)

combined[combined["decision"].str.startswith("保留")].to_csv(
    retained_file, index=False
)

print("\n=== candidate_0173 三模型均值（筛选基准） ===")
print(baseline[mean_cols].to_string())

print("\n=== 27 个候选物筛选结果 ===")
print(
    combined[
        ["candidate_id", "better_metric_count", "decision"]
    ].to_string(index=False)
)

print("\n保留数量：", combined["decision"].str.startswith("保留").sum())
print("淘汰数量：", (combined["decision"] == "淘汰").sum())

print("\n输出文件：")
print(mean_table_file)
print(decision_file)
print(retained_file)
PY

python LOCAL_PATH
```

## 输出文件

运行成功后会生成三张 CSV：

- `candidate_27_three_model_means.csv`：27 个 candidate 的全部三模型均值。
- `candidate_27_filter_vs_0173.csv`：均值、逐项优于基准的判断、优于基准的指标数量和最终决定。
- `candidate_retained_vs_0173.csv`：只包含保留的候选物。

**重要检查：** 脚本要求模型级 CSV 中每个 candidate 恰好有 3 条记录。如果 `boltz_sample_metrics.csv` 或 `per_model_structure_metrics.csv` 的列名与实际情况不一致，脚本会报错并列出可用列名，不会静默地用旧的 median/min/max 代替三模型均值。

另外，TM-score 这里优先使用参考结构归一化的 `tm_normalized_by_reference_chain1`。如果你的结构文件同时包含两种 TM-score 归一化方式，建议统一使用这一列，避免混用不同归一化口径。

你运行后把终端输出贴过来，我可以继续核查保留名单是否合理，以及是否有候选物仅凭某一项指标略微优于基准而被保留。

---

# you asked

message time: 2026-10-22 23:20:23

raise ValueError(
ValueError: 结构指标 缺少模型级指标列：['tm_score', 'rmsd_A']
文件列名：['candidate', 'model', 'file', 'status', 'receptor_chain', 'binder_chain', 'receptor_global_rmsd_A', 'receptor_pocket_rmsd_A', 'receptor_alignment_pairs', 'interface_atom_pairs_lt5A', 'interface_residue_pairs_lt5A', 'binder_residues_contacting_receptor', 'binder_receptor_min_distance_A', 'clash_atom_pairs_lt2A', 'binder_atom_pairs_lt5A_from_reference_peptide', 'binder_residues_near_reference_peptide', '_candidate']
请检查该文件是否存储了每个模型的原始指标，而不是只有 median/min/max 汇总值。
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

这个报错说明：脚本读取到的 `per_model_structure_metrics.csv` **并没有保存 TM-score 和全局 RMSD 这两列**。它保存的是另一组结构指标，例如受体全局/口袋 RMSD、界面接触数、最小距离和 clash 数量。

所以不是 27 个 candidate 的数据一定有问题，而是我前一版脚本把两份不同用途的结构指标文件混在了一起。先不要修改或覆盖原始数据。

你之前计算的 TM-score 和全局 RMSD，应该来自另一个文件：

`LOCAL_PATH

我们需要改为读取这个文件，再确认它实际的列名和每个模型的记录数。

---

# chatgpt response

先在终端执行这条命令，确认 TM-score 文件确实存在、列名正确：



如果输出中包含以下两列：

- `tm_normalized_by_reference_chain1`
- `usalign_aligned_rmsd_A`

那么就可以修复脚本。打开原脚本：



找到文件路径定义，把：



改成：



保存后重新运行：



如果仍然报错，请把第一条命令输出的**列名、记录数和每个 candidate 的模型数统计**贴给我，我会根据实际数据修正，不再猜测列名。

---

# you asked

message time: 2026-10-22 23:22:02

记录数： 81

每个 candidate 的模型数：
3    27
Name: count, dtype: int64

前 3 行：
     candidate  model                                                                                                                                      model_cif predicted_receptor_chain  predicted_receptor_sequence_length  sequence_alignment_score  sequence_identity_fraction  tm_normalized_by_reference_chain1  tm_normalized_by_predicted_chain2  aligned_length  usalign_aligned_rmsd_A status
candidate_0009      0 LOCAL_PATH                        A                                 395                     753.5                         1.0                            0.75716                            0.77658             362                    4.12     OK
candidate_0009      1 LOCAL_PATH                        A                                 395                     753.5                         1.0                            0.74729                            0.76649             357                    4.16     OK
candidate_0009      2 LOCAL_PATH                        A                                 395                     753.5                         1.0                            0.68942                            0.70763             318                    3.95     OK
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

很好，TM-score 文件已经确认正常：**81 条模型记录，27 个 candidate，每个恰好 3 个模型**。参考归一化 TM-score 和全局 RMSD 的列名也已经明确，因此可以用正确的数据源计算均值。

你现在只需要把脚本中结构指标的文件路径和列名映射修正，不需要重新运行结构比对，也不需要重跑 Boltz 预测。

运行下面这段命令即可修改并重新运行：



脚本会使用：

- `tm_normalized_by_reference_chain1`：参考结构归一化 TM-score，越高越好。
- `usalign_aligned_rmsd_A`：全局比对 RMSD，越低越好。
- 原始 Boltz 模型指标：每个 candidate 的三个模型取算术平均值。

成功后请重点查看终端中的 **`candidate_0173` 三模型均值**、27 个候选物的保留/淘汰结果，以及输出文件路径。如果这次遇到新的报错，把完整报错贴过来；如果运行成功，把筛选结果贴过来，我再帮你检查规则是否正确执行。

---

# you asked

message time: 2026-10-22 23:22:35

=== 27 个候选物筛选结果 ===
  candidate_id  better_metric_count decision
candidate_0009                    0       淘汰
candidate_0021                    0       淘汰
candidate_0027                    2       保留
candidate_0043                    7       保留
candidate_0044                    8       保留
candidate_0046                    3       保留
candidate_0051                    1       保留
candidate_0062                    0       淘汰
candidate_0071                    3       保留
candidate_0081                    0       淘汰
candidate_0082                   10       保留
candidate_0093                    1       保留
candidate_0096                    7       保留
candidate_0111                    4       保留
candidate_0112                    7       保留
candidate_0129                    1       保留
candidate_0153                    1       保留
candidate_0165                    0       淘汰
candidate_0170                   10       保留
candidate_0173                    0   保留（基准）
candidate_0175                    1       保留
candidate_0200                   10       保留
candidate_0213                    2       保留
candidate_0219                    0       淘汰
candidate_0227                    3       保留
candidate_0228                    2       保留
candidate_0241                    0       淘汰

保留数量： 20
淘汰数量： 7

输出文件：
LOCAL_PATH
LOCAL_PATH
LOCAL_PATH
(boltz) ziguimu@DESKTOP-8RLFC97:~$

---

# chatgpt response

这次脚本运行成功。按照你设定的规则，原始 27 个候选物中，**20 个保留、7 个淘汰**。

## 1. 筛选结果

<box gap={2}>
  <grid columns={3} gap={2}>
    <grid-item>
      <box bsize="2xl" color="successdius="lg" padding={3} gap={1}>
        <text color="secondary" size="sm">淘汰</text>
        <title size="2xl" color="danger">7</title>
        <text size="xs">25.9%</text>
      </box>
    </grid-item>
  </grid>
</box>

### 保留的 20 个 candidate

```text
candidate_0027
candidate_0043
candidate_0044
candidate_0046
candidate_0051
candidate_0071
candidate_0082
candidate_0093
candidate_0096
candidate_0111
candidate_0112
candidate_0129
candidate_0153
candidate_0170
candidate_0173
candidate_0175
candidate_0200
candidate_0213
candidate_0227
candidate_0228
```

### 淘汰的 7 个 candidate

```text
candidate_0009
candidate_0021
candidate_0062
candidate_0081
candidate_0165
candidate_0219
candidate_0241
```

## 2. 对你之前关注的 D13、D41、D44 的影响

| 原始代号 | Candidate 编号 | 本轮结果 |
|---|---|---|
| D13 | `candidate_0165` | 淘汰 |
| D41 | `candidate_0241` | 淘汰 |
| D44 | `candidate_0173` | 保留（基准） |

D13 和 D41 在这轮规则下没有任何一项指标优于 `candidate_0173` 的三模型均值；D44 本身就是比较基准，所以强制保留。

## 3. 这里有一个重要的解释边界

`better_metric_count` 表示有多少项指标优于基准，不代表综合质量分数，也没有考虑指标之间的相关性。

例如：

- `candidate_0082`、`candidate_0170`、`candidate_0200`：各有 10 项指标优于基准，是本轮值得优先复核的对象。
- `candidate_0044`：有 8 项指标优于基准。
- `candidate_0051`、`candidate_0129`、`candidate_0153`、`candidate_0175`：仅有 1 项指标优于基准，属于较弱的边缘入选候选物。

**尤其要注意：** “至少一项优于基准”是宽松的筛选规则，20 个入选者不能直接理解为 20 个高质量 binder。它只是把候选物缩小到一个待进一步评估的集合。

## 4. 下一步建议

先保留这三份结果文件，不要覆盖原始数据：

- `candidate_27_three_model_means.csv`：27 个候选物的三模型均值。
- `candidate_27_filter_vs_0173.csv`：逐项比较与保留/淘汰判定。
- `candidate_retained_vs_0173.csv`：20 个入选候选物。

接下来更有价值的是对这 20 个候选物进一步比较**局部结合口袋、binder–受体接触、界面几何、空间冲突，以及与参考肽的空间关系**，而不是仅根据目前的 10 项优于基准数量继续排序。这样才能避免一个候选物只凭某项指标略微领先，就被误认为更值得实验验证。

---

# you asked

message time: 2026-10-22 23:24:17

# GLP-1RA 论文补充材料合并整理与复现审计

**论文：** *AI-Driven De Novo Design of Ultra Long-Acting GLP-1 Receptor Agonists*（Advanced Science, 2025；DOI: 10.1002/advs.202507044）  
**合并范围：** 用户在聊天中粘贴的 `sup-0001` 补充材料文字 + `advs71185-sup-0002-datafile.zip` 的源数据审计。  
**阅读原则：** 区分论文报告的方法、补充表/源数据中的记录、从表格复算出的数值，以及目前无法独立验证的结论。本文不是对论文全部实验的独立复现。

## A. 一页摘要

这篇工作采用计算设计与逐级实验验证相结合的流程，目标是从头设计 GLP-1 受体（GLP-1R）激动肽，并从候选物中筛选出具有功能活性、同时改善药代性质的分子。`sup-0001` 主要帮助理解设计与筛选流程、方法设置、序列/修饰信息及补充表；`sup-0002` 则提供 Figure 2–6 的部分 source data，以及 D13、D41、D44 和 Semaglutide 的 LC–MS/MS 定量汇总报告。

需要优先记住的事实：

1. 补充材料所述计算筛选链可概括为 **10,000 → 787 → 359 → 86 → 84 → 60**。这表示逐步过滤/推进的候选物数量，不应误写为 10,000 个分子都完成了后续实验。不同节点的具体筛选规则应以 `sup-0001` 对应的表格/方法说明为准。
2. 在 `sup-0002` 的 `Fig. 6` 表中，60 个候选物的 pull-down 记录为阳性 31 个；SPR 只有 13 个有记录，其中 6 个标为阳性；cAMP 只有 D13、D41、D44 三个候选物有记录。各实验分母不同，不能混用。
3. D13、D41、D44 的实验结果分属不同证据层次：SPR KD 是结合亲和力指标，cAMP EC50 是功能效力指标，PK 半衰期/AUC 是体内暴露与药代指标；三者不可互相替代。
4. D13、D41 的表列终末半衰期分别约为 Semaglutide 的 2.43 倍和 2.84 倍；D44 约为 0.51 倍。此结论仅是表中均值的算术比值，解释仍需结合给药剂量、动物实验设计和原文方法。
5. 现有补充材料可以支持部分流程审阅和源数据复算，但不足以独立重建所有 10,000 个生成候选物、完整逐条结构筛选记录、完整质谱仪器原始数据，或证明结构预测分数能普遍预测 GLP-1R 激动功能。

## B. sup-0001：方法、筛选流程与补充表

### B1. 计算设计与筛选流程

根据聊天中提供的 `sup-0001` 文字，论文方法涉及 ProteinMPNN、AlphaFold2、分子动力学（MD）以及系统发育/序列距离相关分析。整体是一个分阶段的候选生成与筛选流程，而不是单一模型一次性输出最终有效分子。

| 阶段计数 | 数量 | 阅读时应注意 |
|---|---:|---|
| 初始设计候选 | 10,000 | 生成起始规模；不代表全部进入实验 |
| 后续节点 1 | 787 | 论文筛选流程中的阶段性保留数量 |
| 后续节点 2 | 359 | 阶段性筛选结果 |
| 后续节点 3 | 86 | 阶段性筛选结果 |
| 后续节点 4 | 84 | 阶段性筛选结果 |
| 最终推进/送测候选 | 60 | 与 `sup-0002` 的 D02–D61 候选记录规模相对应 |

**计数口径提醒：** 聊天中整理 `sup-0001` 时还出现过 **1,443 与 787 不一致** 的数字。现阶段不应把两者自行合并成同一个节点，也不应擅自判定哪一个一定是错误。正式引用时要回到 `sup-0001` 对应的图、表或原文段落，记录每个数字对应的筛选步骤、候选集合与分母。上表将 10,000→787→359→86→84→60 作为当前工作流摘要，同时将 1,443/787 的冲突列为待核对项。

### B2. 方法组件应如何解释

- **ProteinMPNN：** 用于给定骨架/结构条件下的序列设计。它输出的是候选序列，不等于实验验证的结合剂或激动剂。
- **AlphaFold2：** 用于结构预测/结构相关筛选。预测结构和置信度指标可以帮助检查结构合理性，但本身不能证明真实结合亲和力或受体激动功能。
- **MD（分子动力学）：** 可用于观察模拟条件下结构随时间的行为。模拟稳定性不等于已测得的结合亲和力、受体激动效力或体内长效性；需同时考虑模拟设置、采样充分性和实验验证。
- **系统发育/序列距离分析：** 可描述候选序列与参考序列之间的差异/多样性；序列距离不应直接解释为功能距离。

这里的工具名是方法组件，不应被当作单独的“实验阳性判据”。具体参数、软件版本、阈值和每步筛选条件，应以补充方法及对应表格为准；没有完整的逐候选输出文件时，不声称已经独立复现所有筛选。

### B3. 补充表的用途与注意事项

聊天中提供的 `sup-0001` 内容涉及 **Table S1、S2–S5、S7–S9**。可按下列原则整理和引用：

- **Table S1：** 序列及化学修饰相关信息，是把计算设计序列与最终合成/测试分子对应起来的重要依据。不要只记录裸氨基酸序列；N 端 Aib、脂肪酸链及连接臂等修饰可能改变分子的药代性质和实验行为。
- **Tables S2–S5、S7–S9：** 应与其原始标题、列名、单位、脚注和正文引用一起解读。不能仅凭表号推断具体变量含义；若要把它们转为结构化数据，应保留原始表名、字段、单位、行号/候选 ID 和缺失状态。
- **缺失的表号或不连续编号：** 不代表内容缺失或实验没有进行，可能只是补充材料的编排方式。引用时使用原始表名，不自行重编号。

### B4. D13、D41、D44 序列与化学实体

`sup-0002` 中列出的生物合成肽序列（均 31 aa）：

- **D13：** `HAEGTFTSDVSSYLEEQAAKAFVERLKRGRG`
- **D41：** `HAEGTFTSDVSSYLEEQQVKQFVERLKRGRG`
- **D44：** `HAEGTFTSDVSRYLEEKAVKDFVERLKRGAG`

对应的化学合成形式包含 N 端 Aib 和赖氨酸侧链脂肪酸修饰：

- **D13：** `H-Aib-EGTFTSDVSSYLEEQAAK(AEEA-AEEA-γE-C20Diacid)AFVERLKRGRG-COOH`
- **D41：** `H-Aib-EGTFTSDVSSYLEEQQVK(AEEA-AEEA-γE-C20Diacid)QFVERLKRGRG-COOH`
- **D44：** `H-Aib-EGTFTSDVSRYLEEKAVK(AEEA-AEEA-γE-C20Diacid)DFVERLKRGAG-COOH`

因此，计算阶段的序列、用于表达/纯化的肽，以及用于 PK/功能实验的化学合成形式不一定是同一化学实体。做结构预测或模型评估时，必须明确输入序列是否包含非天然残基/修饰；普通蛋白质建模流程不能自动代表脂化后的真实分子。

### B5. 与 `sup-0002` 对接时要核查的事项

1. 将 `sup-0001` 中的筛选节点与 `sup-0002` `Fig. 6` 的 D02–D61 候选表逐项对齐，确保每个节点的分母、候选编号和状态定义一致。
2. 核对 1,443 与 787 的数字冲突：确认 1,443 是生成后某个早期集合、某种序列去重/过滤统计，还是另一版统计；在找到原始位置前标为“待核实”，不能静默改写。
3. 逐项记录方法阈值与对应输出字段；如果补充方法只给出筛选规则而未提供每个候选的完整预测结果，就只能描述流程，不能声称逐条复现。
4. 将结构筛选与实验验证分开记录：计算保留、pull-down 阳性、SPR 阳性、cAMP 激动、PK/PD 表现是不同状态，不要折叠成单一“成功/失败”标签。

---


## C. sup-0002：源数据与 PK 报告审计

**来源文件：** `advs71185-sup-0002-datafile.zip`  
**解包内容：** 4 份 PK LC–MS/MS 定量汇总报告 + `source data.xlsx`（7 个工作表）。

## 1. 核心结论

1. 该数据包明显超出一般 Supplementary Methods：它含有 Figure 2–6 的 source data，以及四个化合物的 LC–MS/MS 定量报告，可用来交叉核对论文图表。
2. 对 60 个送测候选物，`Fig. 6` 中 pull-down 记录为阳性的有 **31/60（51.7%）**。
3. SPR 并非对全部 60 个候选物进行：表中有结果的 13 个候选物中，6 个标为阳性、7 个标为阴性。不能把它写成 6/60。
4. cAMP 数据只覆盖 D13、D41、D44 三个候选物，三者均有阳性标记；这不能证明其他候选物均无激动活性，因为其他候选物没有该项数据。
5. D13、D41、D44 的药代数据提供了半衰期、Tmax、Cmax、AUC 和 MRT。D13 与 D41 的终末半衰期约为司美格鲁肽的 2.43 倍和 2.84 倍；D44 约为其 0.51 倍。
6. 该数据包支持复核“结合—功能—药代/药效”不同层次的证据，但不能单独证明模型结构预测可以可靠预测亲和力，也不能证明计算模型能够预测激动功能。

## 2. 文件清单与用途

| 文件/工作表 | 内容 | 可做的核查 |
|---|---|---|
| `source data.xlsx` → `Fig. 2_cAMP` | 四种肽的浓度-反应均值、SD 和报告的 EC50 | 复画浓度-反应曲线；检查 EC50 与正文/图注是否一致 |
| `Fig. 3 PK` | PK 汇总指标、浓度-时间均值与 SD | 重画 PK 曲线；复算比值和汇总指标 |
| `Fig. 4` | 血糖/药效相关源数据 | 按组别和时间整理后复画图；需先确认各块表格的列语义 |
| `Fig. 5` | 体重、体重变化、肝/脂肪指数、TC、LDL-C 等源数据 | 复画组间趋势；不要仅凭均值推断统计显著性 |
| `Fig. 6` | D02–D61 的 pull-down、SPR、cAMP、PK、PD 标记与 recovery | 重建候选物筛选漏斗，并保留各阶段实际分母 |
| `D13_D41_D44` | 序列、化学修饰、pull-down、SPR KD、cAMP EC50、PK/PD 指示 | 对照候选物的序列与实验结果 |
| `Phylogenetic distance` | GLP-1 与 D02–D61 的序列距离矩阵 | 研究序列多样性；不能直接当作功能相似性 |
| 4 份 `SI_The raw data of PK ...pdf` | MassLynx 定量汇总报告（每份约 31–32 页） | 检查标准曲线、QC、样本浓度和定量过程；并非完整仪器原始文件/色谱原始数据 |

## 3. 候选物筛选漏斗（由 source data.xlsx 重新计数）

`Fig. 6` 对 D02–D61 共 60 个候选物的阶段记录如下：

| 阶段 | 有该项记录的候选物 | 阳性 | 阴性 | 正确分母下的阳性比例 |
|---|---:|---:|---:|---:|
| Pull-down | 60 | 31 | 29 | 31/60 = **51.7%** |
| SPR | 13 | 6 | 7 | 6/13 = **46.2%** |
| cAMP | 3 | 3 | 0 | 3/3 = **100%（仅限被测的 3 个）** |
| PK 标记 | 3 | 2 | 1 | 2/3 = **66.7%（按表内标记）** |
| PD 标记 | 3 | 2 | 1 | 2/3 = **66.7%（按表内标记）** |

**解释限制：** 这些阶段是选择性推进的，不是对同一批 60 个分子逐一完成所有实验。cAMP 的 3/3 是经过前序筛选后进入功能检测的子集，不能作为全体候选物的功能命中率。`Fig. 6` 中 PK/PD 的 0/1 应按原表编码理解；在没有完整图注/实验判定定义前，不要把它自动解释为“没有进行实验”或“药代失败”。

## 4. D13、D41、D44 与司美格鲁肽：源数据关键值

### 4.1 cAMP 与 SPR

| 分子 | SPR KD（M，表格原值） | 换算 KD（µM） | cAMP EC50（nM，表格原值） | 说明 |
|---|---:|---:|---:|---|
| Semaglutide | 2.78×10⁻⁶ | 2.78 | 0.01940 | 参考分子 |
| D13 | 8.58×10⁻⁶ | 8.58 | 0.03577 | SPR KD 高于司美格鲁肽；EC50 也较高 |
| D41 | 5.19×10⁻⁶ | 5.19 | 0.01089 | 该组中表列 EC50 最低 |
| D44 | 6.78×10⁻⁶ | 6.78 | 0.01243 | EC50 较低，但后续 PK/PD 标记需结合原文解释 |

- **KD 与 EC50 不是同一个量。** KD 反映结合亲和力；EC50 反映特定 cAMP 实验条件下达到半最大响应所需浓度，不能互相替代。
- 这些数据中 D13/D41/D44 的 SPR KD 均高于司美格鲁肽的表列 KD，故不应概括为“亲和力强于司美格鲁肽”。
- 表格给出的 EC50 值很小（约 0.011–0.036 nM）。在正式引用前，建议逐一核对论文 Figure 2、图注和拟合方法中的单位及归一化定义。

### 4.2 PK 汇总（均值 ± SD）

| 指标 | D13 | D41 | D44 | Semaglutide |
|---|---:|---:|---:|---:|
| T1/2 (h) | 19.86 ± 1.55 | 23.16 ± 3.69 | 4.19 ± 0.37 | 8.17 ± 0.29 |
| Tmax (h) | 10.67 ± 2.31 | 12.00 ± 0.00 | 4.00 ± 0.00 | 8.00 ± 0.00 |
| Cmax (ng/mL) | 353.96 ± 41.90 | 294.13 ± 37.18 | 116.60 ± 20.36 | 329.82 ± 10.44 |
| AUC(0–t) (h·ng/mL) | 15939.88 ± 2952.53 | 15737.19 ± 822.42 | 1276.31 ± 139.04 | 7538.16 ± 75.63 |
| AUC(0–∞) (h·ng/mL) | 16134.37 ± 2750.68 | 15884.44 ± 889.05 | 1313.62 ± 140.46 | 7702.53 ± 95.62 |
| MRT(0–t) (h) | 32.02 ± 2.89 | 38.79 ± 1.15 | 7.69 ± 0.35 | 14.21 ± 0.23 |
| MRT(0–∞) (h) | 33.52 ± 1.60 | 40.30 ± 1.16 | 8.33 ± 0.40 | 15.18 ± 0.13 |

以表内均值计算，D13 与 D41 的 T1/2 分别约为司美格鲁肽的 **2.43×** 与 **2.84×**；D44 约为 **0.51×**。D13/D41 的 AUC(0–t) 约为司美格鲁肽的 **2.11×/2.09×**，但 AUC 受剂量、暴露和实验设计影响，不应单独等同于“长效性”。

## 5. 序列与化学修饰

三条候选物的生物合成肽序列（均为 31 aa）：

- **D13**：`HAEGTFTSDVSSYLEEQAAKAFVERLKRGRG`
- **D41**：`HAEGTFTSDVSSYLEEQQVKQFVERLKRGRG`
- **D44**：`HAEGTFTSDVSRYLEEKAVKDFVERLKRGAG`

化学合成形式均含 N 端 Aib 和赖氨酸侧链脂肪酸修饰：

- D13：`H-Aib-EGTFTSDVSSYLEEQAAK(AEEA-AEEA-γE-C20Diacid)AFVERLKRGRG-COOH`
- D41：`H-Aib-EGTFTSDVSSYLEEQQVK(AEEA-AEEA-γE-C20Diacid)QFVERLKRGRG-COOH`
- D44：`H-Aib-EGTFTSDVSRYLEEKAVK(AEEA-AEEA-γE-C20Diacid)DFVERLKRGAG-COOH`

注意：生物合成序列和化学合成肽不是完全相同的化学实体；分析时应把序列变体、Aib、脂肪酸连接臂和 C18/C20 修饰一并记录，不能只比较裸序列。

## 6. PK 原始报告的可核查范围

四份 PDF 是 MassLynx Quantify Compound Summary Report，而非完整原始仪器数据文件。报告包含校准曲线、标准品、QC 和样本定量记录。例如报告开头的校准相关系数约为：D13 r=0.998955、D41 r=0.995915、D44 r=0.996092、Semaglutide r=0.995914。**相关系数高不等于全部 QC/样本都自动合格**；应继续检查每份报告的 QC 偏差、超范围样本、缺失值、稀释/复测标记以及每只动物的时间点记录。

## 7. 可复现 / 不可复现边界

### 仅凭该数据包可做

- 重建 `Fig. 2` 和 `Fig. 3` 的均值±SD曲线（前提是按原始列和图注正确映射）。
- 复算 PK 汇总指标之间的倍数关系。
- 复核 60 个候选物在 pull-down、SPR、cAMP、PK、PD 各阶段的记录和分母。
- 对 D13/D41/D44 序列、脂肪酸修饰、KD、EC50、PK 指标做结构化汇总。
- 用序列距离矩阵分析候选物的序列多样性。

### 仅凭该数据包不能声称完成

- 从头复现 ProteinMPNN 的 10,000 条生成序列及每一步筛选：数据包未显示完整 10,000 条候选及逐条结构筛选结果。
- 从 PDF 汇总表重建全部 LC–MS/MS 仪器处理流程：需要原始色谱/质谱数据、完整分析方法和样本对应信息。
- 证明 AlphaFold/MD 指标能预测实验亲和力：需要候选级预测分数与实验标签的完整配对数据，并进行适当验证。
- 证明结构预测可以预测 GLP-1R 激动功能：cAMP 是功能实验；结合或结构相似本身不足以证明激动。
- 仅凭均值和 SD 判断统计显著性或独立重复数：需要实验设计、每只动物/每次实验的原始值和统计检验细节。

## 8. 与自己的 GLP1R 计算项目如何衔接

推荐把论文数据作为**公开实验参照和任务边界**，而不是直接当作自己模型的训练集或阈值来源：

1. 先把 D13/D41/D44 和 Semaglutide 作为已知实验参照，统一记录序列、修饰、SPR KD、cAMP EC50、PK 和 PD 标签。
2. 对结构模型只评估结构层面的量（构象相似、界面接触、界面置信度等），并明确这些量不能直接等同于 KD 或 cAMP 激动效力。
3. 若对公开数据做预测-实验比较，必须说明只有 3 个候选物具备 cAMP 标签、只有 13 个具备 SPR 标签；样本极小，不能据此训练或声称获得通用阈值。
4. 长江杯若只按实测亲和力评分，则应优先优化结合/亲和力相关的证据链；激动功能仍是独立的生物学问题，不应混成一个分数。
5. 在自己的仓库中保留来源、单位、原始列名、转换步骤和“不确定/未测”状态；缺失数据不得编码成阴性。

## 9. 建议的复现记录规范

每个分子一行，至少包含：`candidate_id`、裸肽序列、化学修饰、pull-down 标签、SPR 是否测试、SPR 标签、KD 原始值/单位、cAMP 是否测试、EC50 原始值/单位、PK 是否测试、T1/2、AUC、PD 是否测试、数据来源文件/工作表/行号、是否由自己重新计算、备注/不确定性。

**最重要的边界：** “未测试”必须与“测试为阴性”区分；“实验结合”必须与“受体激动”区分；“更长半衰期”必须与“更强亲和力”区分。


## D. 两份补充材料合并后的结论与证据边界

### D1. 可以较有把握地陈述

- 论文使用了分阶段的计算设计/筛选流程，计算筛选后有 60 个候选进入 `sup-0002` 中的候选物记录；但 1,443 与 787 的节点统计仍需回查原表/原文，正式报告中应保留该疑点。
- `sup-0002` 显示 60 个候选物中 31 个有 pull-down 阳性记录；SPR 仅 13 个有结果，6 个阳性；cAMP 仅 D13、D41、D44 三个候选物有记录。
- D13/D41/D44 的实验评价跨越结合、细胞功能和 PK/PD 等层面，不能把不同指标直接合并成一个“结合能力分数”。
- D13 与 D41 的表列半衰期高于 Semaglutide；D44 的表列半衰期低于 Semaglutide。该比较不能单独证明临床长效性或总体疗效优势。

### D2. 目前不能据此声称

- 已完整复现论文生成的全部 10,000 条序列、全部结构预测/MD 结果以及每一轮筛选的候选明细。
- AlphaFold2 置信度、MD 稳定性或序列距离已被证明可以普遍预测 GLP-1R 的结合亲和力或激动功能。
- pull-down 阳性等同于 SPR 强亲和力，或 SPR 结合等同于 cAMP 激动。
- cAMP 子集的 3/3 阳性可以代表全部候选物的激动命中率。
- 从 LC–MS/MS 汇总 PDF 单独重建完整的仪器原始色谱、样本处理和所有质量控制过程。
- 仅根据均值和标准差就得出统计显著性、可重复性或临床有效性结论。

### D3. 推荐的统一数据表结构

建议在科研仓库中建立一份主表，每个候选物一行，至少保留：

`candidate_id`, `design_stage`, `sequence_unmodified`, `sequence_chemical_form`, `modifications`, `ProteinMPNN_status`, `AlphaFold2_status`, `MD_status`, `pull_down_tested`, `pull_down_result`, `SPR_tested`, `SPR_result`, `KD_value`, `KD_unit`, `cAMP_tested`, `EC50_value`, `EC50_unit`, `PK_tested`, `half_life_value`, `AUC_value`, `PD_tested`, `source_document`, `source_table`, `source_row_or_page`, `value_type`（原始/换算/复算）, `uncertainty_notes`。

每一项状态应至少区分 `positive`、`negative`、`not tested/not reported`、`unclear`。缺失值不要编码成 0，也不要把未测试记作阴性。单位换算后的值要同时保留原始值和转换公式。

### D4. 对用户自己的 GLP-1R 计算项目的直接启示

1. 把该论文当作**公开实验参照与方法案例**，不要直接把小样本标签当作训练集或通用阈值。
2. 在自己的计算流程中分开记录结构合理性、界面/结合证据、受体激动功能和药代性质；每个阶段都要说明它实际支持哪类结论。
3. 如果要做预测指标与实验标签的比较，先建立候选级配对数据表，记录缺失机制与选择偏差；SPR/cAMP 子集数量很小，任何相关性都应标为探索性分析。
4. 在仓库里同时保存来源文件、原始字段、单位、转换脚本和人工核查备注，确保后续导师或合作者可以从结论追溯回数据。

**最终原则：** 计算筛选不是实验验证；结构置信度不是亲和力；结合不是激动；PK 暴露不是功能效力；“未测试”不是“阴性”。

根据这个材料总结一下D13D41D44体现出来的各项指标

---

# chatgpt response

根据你整理的 `sup-0001` 和 `sup-0002` 材料，D13、D41、D44 的表现需要从 **结合亲和力、细胞功能、药代动力学、药效表现和分子修饰** 五个方面理解。它们不是单纯比谁的结构分数更高，而是论文中经过实验评价的三个 GLP-1R 激动肽候选物。

## 一、三者核心指标对比

<text color="secondary" size="sm">数据来源：你提供的补充材料审计汇总。下表中的 KD、EC50、PK 数值均按原材料记录；半衰期倍数为根据表列均值复算。</text>

| 指标 | D13 | D41 | D44 | Semaglutide |
|---|---:|---:|---:|---:|
| SPR $K_D$（µM） | 8.58 | 5.19 | 6.78 | 2.78 |
| cAMP $EC_{50}$（nM） | 0.03577 | **0.01089** | 0.01243 | 0.01940 |
| 终末半衰期 $T_{1/2}$（h） | 19.86 ± 1.55 | **23.16 ± 3.69** | 4.19 ± 0.37 | 8.17 ± 0.29 |
| $T_{1/2}$ 相对倍数 | 2.43× | **2.84×** | 0.51× | 1.00× |
| $T_{\max}$（h） | 10.67 ± 2.31 | 12.00 ± 0.00 | 4.00 ± 0.00 | 8.00 ± 0.00 |
| $C_{\max}$（ng/mL） | **353.96 ± 41.90** | 294.13 ± 37.18 | 116.60 ± 20.36 | 329.82 ± 10.44 |
| AUC(0–t)（h·ng/mL） | **15939.88 ± 2952.53** | 15737.19 ± 822.42 | 1276.31 ± 139.04 | 7538.16 ± 75.63 |
| AUC(0–∞)（h·ng/mL） | **16134.37 ± 2750.68** | 15884.44 ± 889.05 | 1313.62 ± 140.46 | 7702.53 ± 95.62 |
| MRT(0–t)（h） | 32.02 ± 2.89 | **38.79 ± 1.15** | 7.69 ± 0.35 | 14.21 ± 0.23 |
| MRT(0–∞)（h） | 33.52 ± 1.60 | **40.30 ± 1.16** | 8.33 ± 0.40 | 15.18 ± 0.13 |

**先看整体：**

- **D13：** 半衰期明显延长，血浆暴露量较高，但 cAMP EC50 高于 Semaglutide。
- **D41：** 三者中表列 cAMP EC50 最低，半衰期最长，平均滞留时间也最长，是这三个候选物中功能效力与药代持续性表现较突出的分子。
- **D44：** 表列 cAMP EC50 较低，但半衰期和 AUC 都明显低于另外两者，药代持续性没有体现出同样优势。

## 二、结合亲和力：SPR $K_D$

SPR 测得的 $K_D$ 反映分子与受体的结合亲和力，通常在相同实验条件下，数值越低代表亲和力越强。

<box border radius="lg" padding={3} gap={3}>
  <title size="md">SPR 亲和力排序</title>
  <row align="center" gap={3}>
    <box width="56px">
      **D41**
    </box>
    <box flex="1" gap={1}>
      <box background="surface-tertiary" radius="md" height="10px" clip>
        <box background="#0D9488" height="10px" width="60.5%" radius="md" />
      </box>
      <text color="secondary" size="xs">5.19 µM</text>
    </box>
  </row>
  <row align="center" gap={3}>
    <box width="56px">
      **D44**
    </box>
    <box flex="1" gap={1}>
      <box background="surface-tertiary" radius="md" height="10px" clip>
        <box background="#0D9488" height="10px" width="79%" radius="md" />
      </box>
      <text color="secondary" size="xs">6.78 µM</text>
    </box>
  </row>
  <row align="center" gap={3}>
    <box width="56p

但三者的 KD 都高于 Semaglutide 的表列值。因此，不能根据这组数据声称 D13、D41 或 D44 的结合亲和力优于 Semaglutide。

## 三、细胞功能：cAMP $EC_{50}$

cAMP EC50 是功能效力指标，不是结合亲和力指标。按照表列数据，EC50 越低，达到半最大响应所需的浓度越低。

| 排名 | 分子 | EC50（nM） | 相对 Semaglutide |
|---|---|---:|---|
| 1 | D41 | **0.01089** | 更低 |
| 2 | D44 | 0.01243 | 更低 |
| 3 | Semaglutide | 0.01940 | 参考 |
| 4 | D13 | 0.03577 | 更高 |

D41 的 EC50 约为 Semaglutide 的 56.1%，D44 约为 64.1%，D13 约为 184.4%。

这说明在该 cAMP 实验的表列结果中，D41 和 D44 的 EC50 更低，而 D13 更高。不过，**EC50 更低并不自动意味着最大效应更高**；若要完整比较激动剂功能，还需要查看最大响应（$E_{\max}$）、实验条件和拟合方法。

此外，补充材料中只有这三个候选物具有 cAMP 记录，不能据此推断全部设计候选物的功能命中率。

## 四、药代动力学：半衰期、暴露量与滞留时间

<Chart content={{"chartType":"bar","meta":{"title":"终末半衰期比较","description":"表列均值；单位为小时。"},"xKey":"molecule","series":[{"dataKey":"half_life","label":"半衰期","valueSuffix":" h"}],"yAxisMin":0,"data":[{"molecule":"D13","half_life":19.86},{"molecule":"D41","half_life":23.16},{"molecule":"D44","half_life":4.19},{"molecule":"Semaglutide","half_life":8.17}]}} />

### D13：暴露量较高，持续时间延长

- 半衰期约为 Semaglutide 的 **2.43 倍**。
- AUC(0–t) 约为 Semaglutide 的 **2.11 倍**。
- Cmax 为 353.96 ng/mL，高于 Semaglutide 表列均值。
- MRT(0–∞) 为 33.52 h，约为 Semaglutide 的 2.21 倍。

### D41：半衰期和滞留时间最突出

- 半衰期约为 Semaglutide 的 **2.84 倍**。
- AUC(0–t) 约为 Semaglutide 的 **2.09 倍**。
- MRT(0–∞) 为 40.30 h，约为 Semaglutide 的 2.65 倍。
- 其 $T_{\max}$ 为 12 h，晚于 Semaglutide 的 8 h。

### D44：药代表现相对较弱

- 半衰期约为 Semaglutide 的 **0.51 倍**。
- AUC(0–t) 约为 Semaglutide 的 **16.9%**。
- Cmax 约为 Semaglutide 的 35.4%。
- MRT(0–∞) 约为 Semaglutide 的 54.9%。

因此，在这组表列 PK 数据中，D13 和 D41 的暴露与持续性更突出，D44 则没有表现出相同的药代优势。

需要注意：这些倍数是表列均值的算术比值，并非统计显著性检验结果；剂量、给药设计、动物实验条件都会影响解释，不能仅凭这些值断言临床长效性。

## 五、分子序列与化学修饰

三者均为 31 aa 的设计肽，并在化学合成形式中引入 N 端 Aib 和赖氨酸侧链脂肪酸修饰。

| 分子 | 生物合成肽序列 | 与其他候选物的特点 |
|---|---|---|
| D13 | `HAEGTFTSDVSSYLEEQAAKAFVERLKRGRG` | 与 D41 在多处序列位置不同 |
| D41 | `HAEGTFTSDVSSYLEEQQVKQFVERLKRGRG` | 与 D13 具有相近的序列骨架，但局部残基不同 |
| D44 | `HAEGTFTSDVSRYLEEKAVKDFVERLKRGAG` | 与 D13/D41 存在更多局部序列差异 |

三者的化学合成形式都包含：

- N 端 Aib；
- 赖氨酸侧链连接臂 `AEEA-AEEA-γE`；
- C20 二酸脂肪酸修饰；
- C 端羧基形式。

这些修饰与药代性质的设计有关，但仅凭三个候选物的结果，不能把半衰期差异归因于某一个单独残基或修饰。要识别因果关系，需要控制其他变量的成对比较或额外实验。

## 六、综合结论

<box border radius="lg" padding={3} gap={3}>
  <row align="start" gap={3}>
    <box background="surface-secondary" radius="lg" size="44px" align="center" justify="center">
      <icon name="activity" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **D41：综合表现最突出**

      <text color="secondary" size="sm">在这三个候选物中，表列 cAMP EC50 最低、SPR KD 最低、终末半衰期最长，且 MRT 最大。它是值得优先研究的候选物，但不能仅凭这些汇总指标认定其整体疗效最佳。</text>
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <box background="surface-secondary" radius="lg" size="44px" align="center" justify="center">
      <icon name="clock" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **D13：药代持续性突出**

      <text color="secondary" size="sm">半衰期和 AUC 均较高，但其表列 cAMP EC50 高于 Semaglutide，SPR KD 也是三者中最高的。它体现了药代优势与功能效力、结合亲和力并不一定同步。</text>
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <box background="surface-secondary" radius="lg" size="44px" align="center" justify="center">
      <icon name="flask-conical" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **D44：功能指标较好，但药代持续性较弱**

      <text color="secondary" size="sm">其表列 cAMP EC50 低于 Semaglutide，但半衰期、Cmax、AUC 和 MRT 均相对较低。说明功能效力指标较好并不意味着体内暴露或作用持续时间也更好。</text>
    </box>
  </row>
</box>

对你自己的 GLP1R 计算项目，最值得借鉴的是：**结合亲和力、受体激动功能与药代持续性必须分开评价。** Boltz 或 AlphaFold 的结构置信度、界面分数，即使表现很好，也不能直接替代 SPR KD、cAMP EC50 或体内 PK 数据。

以上比较严格依据你提供的补充材料审计摘要；我没有在本轮重新打开原始补充文件核对每个数值，因此正式引用前，建议再次核实 EC50 的单位、PK 给药条件和原文统计方法。

---

# you asked

message time: 2026-10-22 23:56:15

**WorkBuddy**

0173除外

筛选完成，结果如下：

## 结果：20 → 保留 2 / 删除 18

`candidate_retained_vs_0173.csv` 已就地删除 18 行，现剩：

| **候选**             | **状态**                                                     |
| :----------------- | :--------------------------------------------------------- |
| **candidate_0082** | 唯一全过门槛的候选（rmsd=3.74，10 项指标全超 0173）                         |
| **candidate_0173** | 按你“除外”的要求保留——它自身其实触了两条雷（tm=0.7622<0.77、rmsd=4>3.9），是基准所以豁免 |

被删的 18 个已另存 `candidate_retained_vs_0173_removed.csv`（同目录，带**删除原因**列，逐行标明触雷条件），原表可随时从此文件恢复。

## 各条件触发数（18 行内可重叠）

| **条件**                      | **触发** |
| :-------------------------- | :----- |
| rmsd_A_mean > 3.9           | **14** |
| tm_score_mean < 0.77        | 11     |
| iptm_mean < 0.9             | 6      |
| complex_plddt_mean < 0.79   | 6      |
| confidence_score_mean < 0.8 | 3      |

每行触雷项数：1 项 ×7、2 项 ×5、3 项 ×2、4 项 ×3、5 项 ×1——**rmsd>3.9 是主要杀手**（18 删 14 中招）。

## 两个值得注意的牺牲者

- **candidate_0200**：rmsd=3.9167，只超 3.9 红线 0.017——它和 0082 是仅有的两个 10 项全超 0173 的候选，这轮被 rmsd 卡掉；
- **candidate_0043**（rmsd=3.93）和 **candidate_0044**（3.9967）也都因 rmsd 出局。

如果觉得 3.9 卡太狠（0200 差 0.017 就能留），说一声我用放宽后的阈值重跑；校验已通过：保留行（除 0173）无一触雷、删除行全部触雷、总数守恒。

查看所有产物 (23)

这是我主观设定标准后筛选得到，最后其实只剩下0082这一条，所以我决定参考你之前列的top8，取`candidate_0082`

2

1

两次入选

`candidate_0096`

1

2

两次入选

`candidate_0200`

4

3

两次入选

`candidate_0043`

3

6

两次入选

`candidate_0044`

7

7

两次入选 这5条序列作为最终候选，你整理一个这5条序列的fasta文件，直接给我文本形式，我自己复制保存，然后你再对这5条序列和0173进行一个序列比对

---

# chatgpt response

我从你之前整理的 `GLP1R_representatives_24_plus_D13_D41_D44.fasta` 和代表序列文件中核对了候选序列。下面先给出 **5 条最终候选的 FASTA 文本**，再与 `candidate_0173`（D44 参考序列）进行逐位序列比对。<FileCite ref_id="turn8file1" />

## 一、5 条最终候选序列 FASTA

复制下面的全部内容，保存为 `GLP1R_final_5_candidates.fRLKRGAG
```

以上序列均为 **31 aa**。其中，`candidate_0082` 与 `candidate_0200` 属于同一序列簇；`candidate_0096` 与 `candidate_0043` 也属于同一序列簇。<FileCite ref_id="turn8file1" />

## 二、参考序列：candidate_0173

`candidate_0173` 对应你此EEKAVKDFVERLKRGAG
```

## 三、与 candidate_0173 的序列比对

所有序列长度相同，因此可以直接按氨基酸位置逐位比较，不需要插入缺口。

| 候选 | 长度 | 与 0173 相同的位点 | 差异位点数 | 序列一致性 |
|---|---:|---:|---:|---:|
| candidate_0044 | 31 aa | 29 | 2 | 93.5% |
| candidate_0082 | 31 aa | 28 | 3 | 90.3% |
| candidate_0096 | 31 aa | 28 | 3 | 90.3% |
| candidate_0200 | 31 aa | 28 | 3 | 90.3% |
| candidate_0043 | 31 aa | 27 | 4 | 87.1% |

### 1. 具体突变位点

以下位置均按序列从 N 端开始、从 1 计数。突变写法如 `D21Q`，表示参考序列第 21 位的 D（天冬氨酸）替换为 Q（谷氨酰胺）。

| 候选 | 相对于 0173 的氨基酸替换 |
|---|---|
| **candidate_0044** | D21A、E24D |
| **candidate_0082** | D21Q、K27R、A30G |
| **candidate_0096** | K17Q、D21A、E24D |
| **candidate_0200** | D21A、K27R、A30G |
| **candidate_0043** | K17Q、D21A、E24D、A30G |

### 2. 按参考序列位置展示差异

以 `candidate_0173` 为参照，五条候选的主要差异集中在第 17、21、24、27 和 30 位：

<box border radius="lg" padding={3} gap={3}>
  <title size="md">参考序列的关键位置</title>
  <text color="secondary" size="sm">位置： 17　21　24　27　30</text>
  <row align="center" gap={2}>
    <box width="104px">
      <text weight="medium">0173 参考</text>
    </box>
    <text> K　D　E　K　A</text>
  </row>
  <divider color="subtle" />
  {#each [{id:"0044",seq:"K　A　D　K　A",n:"2 个差异"},{id:"0082",seq:"K　Q　E　R　G",n:"3 个差异"},{id:"0096",seq:"Q　A　D　K　A",n:"3 个差异"},{id:"0200",seq:"K　A　E　R　G",n:"3 个差异"},{id:"0043",seq:"Q　A　D　K　G",n:"4 个差异"}] as item}
    <row align="center" gap={2}>
      <box width="104px">
        <text weight="medium">{item.id}</text>
      </box>
      <box flex="1">
        <text>{item.seq}</text>
      </box>
      <text color="secondary" size="xs">{item.n}</text>
    </row>
  {/each}
</box>

## 四、这次比对说明什么？

- **candidate_0044 与 0173 最接近**：仅有 2 个氨基酸替换，序列一致性为 93.5%。
- **candidate_0082 与 candidate_0200 很接近**：两者仅在第 21 位不同，分别为 Q 和 A；其余位置一致。
- **candidate_0096 与 candidate_0043 很接近**：两者仅在第 30 位不同，分别为 A 和 G。
- **candidate_0043 与 0173 的差异最多**：共有 4 个替换，但仍有 87.1% 的序列一致性。

**对后续实验的意义：** 这 5 条序列不是 5 个完全独立的设计，而是存在明显的序列相似性和局部突变关系。如果后续需要合成或实验验证，可以将它们视为一个小型候选变体集合，重点比较不同位点组合与实验表现之间的关系。

需要注意，序列一致性和突变数量只能描述序列关系，不能直接判断哪条序列的 GLP-1R 结合能力或激动活性更强。最终仍需结合结构分析和实验结果进行验证。

---

# you asked

message time: 2026-10-23 00:17:15

现在来建立第十一阶段的工作记录吧，这一阶段我们使用之前准备好的boltz体系（运行参数记得介绍一下，我看上一阶段记录里没提）完成了27条candidate的结构预测，获得了相关数据，随后又参照论文计算了TM评分和RMSD值，把所有数据汇总、排序、筛选，最后选出了5条最终序列，可能还要进一步进行亲和力预测，以上这些，你自行浏览对话记录进行补充，尽量详细一点，最后按照之前的工作记录风格，给我生成这次的文本，我自行复制保存

---

# chatgpt response

下面按之前《GLP1R_reproduction 工作记录》的风格整理为**第十一阶段工作记录**，可直接复制到原有 Markdown 文档末尾。

我会把已经完成的计算、使用的参数、指标定义、两种筛选思路、最终 5 条序列和下一步计划分别记录，并明确区分**计算结果、主观筛选标准和仍待验证的事项**。对于当前对话中没有明确核实的参数，不会擅自补成确定事实。

---

<

---

# you asked

message time: 2026-10-23 00:21:08

`--diffusion_samples`=3，seed=3你自己查对话记录查不到？我让你看对话记录你到底看了没？！

---

# chatgpt response

你说得对。这次是我没有把之前的对话记录查完整，就在工作记录里写“尚未核实”，把本来已经讨论并确定的参数遗漏了。这不是你没说清楚，是我没有做好记录追溯。对不起。

我刚刚重新检索了之前 GLP1R 项目的对话记录，找到了 **2026-10-22 关于 Boltz-2 运行体系的参数确认记录**。其中明确记录了以下设置：

| 参数 | 之前记录的值 |
|---|---:|
| `seed` | **27** |
| `recycling_steps` | **3** |
| `sampling_steps` | **200** |
| `step_scale` | **1.5** |
| `diffusion_samples` | **3** |
| `max_parallel_samples` | **1** |
| 受体 MSA | 优先使用 GLP1R 本地 MSA |
| 候选肽 MSA | `empty` |
| 候选数量 | 27 条 |
| 每条候选采样数 | 3 |
| 预期结构样本总数 | 81 |

这里有一个需要如实说明的差异：**我在之前找到的参数确认记录里查到的是 `seed=27`，而你刚才指出的是 `seed=3`。** 我不能为了迎合其中一个数字就直接覆盖另一个。`diffusion_samples=3` 是确定的；随机种子则应以正式批量运行命令或运行日志为准。当前找到的记录还提到，当时需要确认所用版本是否支持显式指定 seed，因此我还不能把 `seed=27` 直接断言为最终实际执行值。

我之前的记录至少应当先把已确认的参数完整写进去，而不是笼统地说“没有完整命令，所以不补写”。这确实是我的疏忽。

**第十一阶段工作记录的参数部分应改为：**

> 本阶段沿用此前准备好的 Boltz-2 运行体系，对 27 条 GLP1R 候选开展批量结构预测。此前讨论确定的运行参数包括 `recycling_steps=3`、`sampling_steps=200`、`step_scale=1.5`、`diffusion_samples=3` 和 `max_parallel_samples=1`。MSA 处理优先使用 GLP1R 受体的本地 MSA，候选肽的 MSA 设置为 `empty`。每条候选进行 3 个结构样本的采样，27 条候选共对应 81 个结构样本。随机种子的最终取值应以正式运行命令或日志为准；此前参数确认记录中出现的值为 `seed=27`，需与实际执行记录核对。上述设置用于统一候选的预测条件，后续将结合 Boltz-2 输出指标及相对于 7KI0 参考结构的 TM-score、RMSD 开展评价与筛选。

我也应该把之前的整份工作记录视为需要修订的版本，而不是只补一行参数就当作完成。尤其是运行参数、指标定义和筛选条件，都应该尽可能追溯到原对话与实际结果文件。

---

# you asked

message time: 2026-10-23 00:22:46

工作记录重写

---

# chatgpt response

你说得对，上一版工作记录没有把历史参数和实际筛选逻辑核实清楚。这次我按现有项目记录重写，明确区分**运行参数、计算结果、筛选决策和生物学验证**；没有依据的内容不补造。

WritingBlock>

---

# you asked

message time: 2026-10-23 00:25:10

你这写得太简略了，我让你浏览历史记录，详细补充，你听懂了吗！

---

# chatgpt response

听懂了。你要的不是把上一版工作记录扩写几段，而是**重新查阅之前的对话，把第十一阶段实际做过的工作按发生顺序恢复出来**：从 Boltz-2 参数和 27 条候选的预测，到模型数据提取、参考结构比对、TM-score/RMSD 计算、指标排序、筛选规则、最终五条序列，以及下一步亲和力预测的衔接。

我刚才重新检索了历史对话，找到了之前讨论过的几组具体信息，包括 81 个模型的结构评价、US-align 对 7KI0 的比对结果、三指标与五指标排序，以及司美格鲁肽参考结构的三模型数据。这些内容上一版确实遗漏了。

下面这版会按**实验过程、实际数据、筛选决策和未完成事项**详细整理；历史记录中没有明确证实的内容，我会标出来，不会伪装成已经完成的步骤。

WritingBlock>

以上版本补回了之前漏掉的 **7KI0 比对细节、TM-score 数值、三指标与五指标排序、81 个模型的处理背景、司美格鲁肽参考模型数据，以及 27 条预测与 20 条严格筛选对象之间的区别**。

还有一项我刻意没有编造：从 27 条候选缩小到 20 条的具体依据，以及 RMSD 脚本中所有原子和残基选择细节。现有历史检索结果没有完整提供这些信息，写成确定事实反而会污染你的实验记录。

---

# you asked

message time: 2026-10-23 13:08:23

Candidate summary:
  candidate_id  n_structures  pcann_avg_mean  pcann_avg_std  pcann_avg_min  pcann_avg_max
candidate_0043             3         -9.1200         0.2516          -9.28          -8.83
candidate_0044             3         -8.9433         0.1553          -9.07          -8.77
candidate_0082             3         -9.1100         0.1375          -9.23          -8.96
candidate_0096             3         -8.9733         0.2043          -9.12          -8.74
candidate_0173             3         -8.9600         0.2427          -9.16          -8.69
candidate_0200             3         -8.9700         0.0436          -9.00          -8.92
(pcann) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH
很好，这次 PCANN 批处理已经成功完成汇总。6 个候选物都各有 3 个 Boltz-2 结构，总计 18 个结构全部进入了统计结果。

1. 当前 PCANN 汇总结果
候选物

结构数

平均分

标准差

最低分

最高分

candidate_0043

3

-9.1200

0.2516

-9.28

-8.83

candidate_0082

3

-9.1100

0.1375

-9.23

-8.96

candidate_0044

3

-8.9433

0.1553

-9.07

-8.77

candidate_0173

3

-8.9600

0.2427

-9.16

-8.69

candidate_0200

3

-8.9700

0.0436

-9.00

-8.92

candidate_0096

3

-8.9733

0.2043

-9.12

-8.74

上表按平均分从数值较小到较大排列。这只是分数排序，不等同于已验证的结合能力排名。 需要先确认 PCANN 的输出分数方向，以及它在这批 GLP1R 复合物上的判别能力，才能赋予生物学解释。

2. 这组结果目前能说明什么？
数值排序靠前： candidate_0043（−9.1200）和 candidate_0082（−9.1100）非常接近，均值只差 0.0100，不能据此认为二者有明确差异。

三结构间最稳定： candidate_0200 的标准差最低，为 0.0436，说明这 3 个结构的 PCANN 分数较一致；但一致不代表预测一定准确。

结构间波动较大： candidate_0043 和 candidate_0173 的标准差分别为 0.2516 和 0.2427，提示其分数对不同预测结构更敏感，值得结合具体结构检查。

整体差异不大： 六个候选物的平均分从 −9.1200 到 −8.9433，跨度约 0.177。是否具有判别意义，目前还无法判断。

3. 下一步建议
先保留当前结果，不要仅凭 PCANN 均值筛掉候选物。建议把这份汇总与现有 Boltz-2 结构评价指标合并，逐个检查：

PCANN 分数与 Boltz-2 的 ipTM、界面几何等指标是否一致。

同一候选物的 3 个结构是否具有相似的结合姿态和界面。

候选物之间的分数差异，是否大于同一候选物不同结构带来的波动。

另外，PCANN 预测分数的方向和量纲仍需核对模型定义，所以现阶段应称为“PCANN 分数”，而不要直接称为结合自由能或 
K
d
K 
d
​
 。

如果你愿意，下一步我们可以直接对照 18 个结构的原始 PCANN 分数和 Boltz-2 评价结果，形成一张六个候选物的综合比较表。

这个分数怎么看
你这次得到的 PCANN 分数，最重要的是先分清楚两件事：分数在模型内部代表什么，以及它能不能用来判断 GLP1R 候选物谁更可能结合。

目前你得到的分数大约在 −8.69 到 −9.28 之间。不能仅凭负号就判断结合好，也不能直接把它当成实验结合自由能或 
K
d
K 
d
​
 。

1. 先看你这批结果
候选物

PCANN 平均分

三个结构的标准差

candidate_0043

−9.1200

0.2516

candidate_0082

−9.1100

0.1375

candidate_0200

−8.9700

0.0436

candidate_0096

−8.9733

0.2043

candidate_0173

−8.9600

0.2427

candidate_0044

−8.9433

0.1553

如果暂时只按数值从小到大排序，0043 和 0082 排在前面。但这只是数学排序，尚不能说它们的结合能力更强。

标准差反映的是三个结构所得分数的离散程度，不是预测准确率，也不是实验重复性。

2. 更关键的是：你的脚本实际上怎样定义这个分数？
在 PCANN 的 make_prediction() 中，模型输出经过了下面的换算：

R = 1.987204258e-03
T = 298
dg = output.item() * R * T

其中 
R
T
≈
0.592
 kcal/mol
RT≈0.592 kcal/mol。因此，你的 avg 不是模型未经处理的原始输出，而是代码将模型输出乘以 
R
T
RT 后得到的数值，再对 25 个模型的结果求平均。

这也意味着，需要核对 PCANN 模型的训练标签与输出定义，才能最终确认它是否严格对应预测结合自由能 
Δ
G
ΔG。不能只凭变量名 dg 就认定其物理含义已经得到验证。

如果模型定义确认它是结合自由能，那么通常：

Δ
G
ΔG 越负，预测结合在热力学上越有利。

Δ
G
ΔG 越接近零，预测结合的有利程度越低。

但预测自由能仍然不是实验测量值，也不能单凭它确认候选物会结合。

3. 你的候选物之间，差异到底有多大？
若暂时按上述自由能解释，最高与最低的候选物平均分相差约 
0.177
 kcal/mol
0.177 kcal/mol。在理想的热力学关系成立时，这只相当于约 1.35 倍的平衡常数差异。

相比之下，你每个候选物的三个结构之间，分数标准差约为 0.044–0.252。也就是说，候选物之间的均值差异很小，不能据此做强结论。

我建议下一步先查看 PCANN 的模型输出定义和训练标签，确认这个分数是否确实是 
Δ
G
ΔG。确认后，再决定排序方向和如何与 Boltz-2 的 ipTM、界面接触及几何指标联合筛选。

PCANN分数是越小越好吗
目前还不能无条件地说 PCANN 分数越小越好，但从你这批结果的计算方式看，如果模型输出确实代表结合自由能 
Δ
G
ΔG，那么通常是越负越好。

你的 PCANN 代码里有这一步：

dg = output.item() * R * T

其中 
R
×
T
≈
0.592
R×T≈0.592。这说明程序把模型原始输出乘以 
R
T
RT，并将结果命名为 dg。不过，变量名叫 dg 并不能单独证明训练标签的定义和模型输出方向正确对应结合自由能，还需要核对 PCANN 的训练标签。

按“数值越负越好”的暂定解释，你这批候选的排序如下：

候选

PCANN 平均分

暂定解读

candidate_0043

−9.1200

较好

candidate_0082

−9.1100

较好

candidate_0044

−8.9433

相对较弱

candidate_0173

−8.9600

相对较弱

candidate_0200

−8.9700

相对较弱

candidate_0096

−8.9733

相对较弱

注意，这些分数差距很小，而且每个候选只有 3 个结构。因此，暂时不能据此认定 candidate_0043 一定优于 candidate_0082，更不能直接断言其实际亲和力更强。

下一步最重要的是确认 PCANN 训练时的标签究竟是 ln(Kd)、结合自由能，还是其他亲和力指标。确认之后，才能最终确定分数方向。确认前，建议将它作为辅助排序指标，并结合 Boltz-2 的 ipTM、界面接触和结构合理性综合判断。


我又完成了以上序列的PCANN预测，也算是补全了亲和力相关的指标，这次论文复现工作也算是基本完结了，因为再往后就是湿实验验证了，而我暂时没有这个条件，所以这个项目就告一段落吧，我决定将candidate_0082、0096、0200、0043作为这个项目的最终成果，那么你现在可以完成最后一阶段（第十二阶段）的工作记录了，在这次记录里就叙述一下最后的PCANN流程，然后主要就是对本次项目的总结了，至于怎么总结你自由发挥，但是要尽量详细，我会把之前的所有工作记录都发给你，所以你先别急着生成文本，等我发完之后会提醒你的，以下是PCANN的相关记录：
========== Existing backups ==========
-rwxrwxrwx 1 ziguimu ziguimu 10197 Oct 23 12:22 examples/make_predictions/run_glp1r_pcann_batch.py.backup_20261023_122250
-rwxrwxrwx 1 ziguimu ziguimu 10197 Oct 23 09:32 examples/make_predictions/run_glp1r_pcann_batch.py.backup_20261023_093519
-rwxrwxrwx 1 ziguimu ziguimu 10197 Oct 23 09:29 examples/make_predictions/run_glp1r_pcann_batch.py.backup_20261023_093212
-rwxrwxrwx 1 ziguimu ziguimu 10140 Oct 23 09:22 examples/make_predictions/run_glp1r_pcann_batch.py.backup_20261023_092914

========== Relevant strings ==========
189:    # Stage 1: convert and validate all 18 structures.
234:        raise RuntimeError(f"Expected 18 structures; prepared {len(input_rows)}")
275:    output["pcann_label"] = output["pdb_id"].astype(str)
276:    output["pdb_id"] = output["pcann_label"].str.replace(r"_wt$", "", regex=True)
290:            output["candidate_id"].isna(), ["pcann_label", "pdb_id"]
297:        raise RuntimeError(f"Expected 18 prediction rows; got {len(output)}")
(pcann) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH
…
从你贴出的结果看，修改已经写入脚本：第 275–276 行保留了 PCANN 原始标签，并把末尾的 _wt 去掉用于匹配；第 297 行也已将预测结果数量检查从 15 条改成 18 条。

刚才报出的 AssertionError 是我写的自检条件有误：实际代码调用的是 output["pcann_label"].str.replace(...)，而自检却检查了 output["pdb_id"].str.replace。这是我的错误，不代表这次脚本修改失败，抱歉。

下一步先检查 Python 语法，再重新运行批处理。

在你当前的 (pcann) 终端中，按顺序执行以下命令。

1. 检查语法

python -m py_compile examples/make_predictions/run_glp1r_pcann_batch.py
echo "exit_code=$?"

如果输出 exit_code=0，说明语法检查通过。

2. 重新运行 18 个结构的批处理

PYTHONPATH=LOCAL_PATH \
python examples/make_predictions/run_glp1r_pcann_batch.py

这次重点观察两点：

是否成功将 c0082m0_wt 这类 PCANN 标签映射回 c0082m0，进而匹配到对应候选物。

是否成功写出 pcann_raw_18_structures.csv 和 candidate_summary.csv。

3. 运行结束后检查结果文件

ls -lh LOCAL_PATH

如果再次报错，请把从 ERROR 开始的完整 traceback 贴给我；如果成功，把终端最后 30 行和结果文件列表贴给我。暂时不要清理缓存，也不要修改其他 PCANN 文件。

ERROR: batch failed.
Traceback (most recent call last):
  File "LOCAL_PATH", line 330, in <module>
    main()
  File "LOCAL_PATH", line 313, in main
    summary["pcann_avg_mean"] = summary["pcann_avg_mean"].round(4)
  File "USER_HOME/miniconda3/envs/pcann/lib/python3.10/site-packages/pandas/core/series.py", line 2821, in round
    raise TypeError("Expected numeric dtype, got object instead.")
TypeError: Expected numeric dtype, got object instead.
(pcann) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH
这次已经越过了前面的候选映射错误，执行到了汇总阶段。当前异常发生在：

summary["pcann_avg_mean"] = summary["pcann_avg_mean"].round(4)

报错说明 pcann_avg_mean 这一列是 Pandas 的 object 类型，而不是数值类型。现在还不能直接断定是汇总逻辑错了，还是上游 avg 列被当作字符串读入或传递。 我们先检查实际数据和汇总代码，再针对原因修复，避免误改预测结果。

请先执行下面这组只读诊断命令。它会检查汇总代码、原始预测 CSV 的数据类型，以及 avg 列是否含有非数值内容。

cd LOCAL_PATH

echo "========== Summary code =========="
nl -ba examples/make_predictions/run_glp1r_pcann_batch.py | sed -n '285,325p'

echo
echo "========== Output files =========="
ls -lh LOCAL_PATH

echo
echo "========== Raw CSV diagnostics =========="
python - <<'PY'
from pathlib import Path
import pandas as pd

p = Path("LOCAL_PATH")
if not p.exists():
    print("RAW CSV DOES NOT EXIST")
else:
    df = pd.read_csv(p)
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    for col in ["pdb_id", "candidate_id", "avg", "pcann_avg", "pcann_avg_mean"]:
        if col in df.columns:
            print(f"\n--- {col} ---")
            print("dtype:", df[col].dtype)
            print("sample:", df[col].head(8).tolist())
            if col in ("avg", "pcann_avg", "pcann_avg_mean"):
                converted = pd.to_numeric(df[col], errors="coerce")
                print("non-numeric count:", int(converted.isna().sum()))
                if converted.isna().any():
                    print("non-numeric values:", df.loc[converted.isna(), col].tolist())
PY

把输出贴给我。这样我们可以确定应当在读取原始分数时转换类型，还是在计算候选物汇总后转换类型，而不是直接用 .round(4) 掩盖潜在的数据问题。

目前这个报错发生在汇总结果四舍五入阶段；它本身不代表 PCANN 模型推理失败。先确认原始 CSV 是否完整包含 18 条预测记录，再决定最小修复方案。

========== Summary code ==========
   285          mapping_df, on="pdb_id", how="left", validate="one_to_one"
   286      )
   287
   288      if output["candidate_id"].isna().any():
   289          unmatched = output.loc[
   290              output["candidate_id"].isna(), ["pcann_label", "pdb_id"]
   291          ].to_dict("records")
   292          raise RuntimeError(
   293              f"Some prediction rows could not be mapped to candidates: {unmatched}"
   294          )
   295
   296      if len(output) != 18:
   297          raise RuntimeError(f"Expected 18 prediction rows; got {len(output)}")
   298
   299      output.to_csv(RAW_CSV, index=False)
   300
   301      # Stage 4: summarize the three Boltz structures for each candidate.
   302      summary = (
   303          output.groupby("candidate_id", as_index=False)
   304          .agg(
   305              n_structures=("avg", "count"),
   306              pcann_avg_mean=("avg", "mean"),
   307              pcann_avg_std=("avg", "std"),
   308              pcann_avg_min=("avg", "min"),
   309              pcann_avg_max=("avg", "max"),
   310          )
   311      )
   312
   313      summary["pcann_avg_mean"] = summary["pcann_avg_mean"].round(4)
   314      summary["pcann_avg_std"] = summary["pcann_avg_std"].round(4)
   315      summary["pcann_avg_min"] = summary["pcann_avg_min"].round(4)
   316      summary["pcann_avg_max"] = summary["pcann_avg_max"].round(4)
   317
   318      summary.to_csv(SUMMARY_CSV, index=False)
   319
   320      print("\nBatch complete.")
   321      print(f"Structure checks: {CHECK_CSV}")
   322      print(f"Raw predictions:  {RAW_CSV}")
   323      print(f"Candidate summary:{SUMMARY_CSV}")
   324      print("\nCandidate summary:")
   325      print(summary.to_string(index=False))

========== Output files ==========
total 20K
drwxrwxrwx 1 ziguimu ziguimu 4.0K Oct 23 09:32 cache
-rwxrwxrwx 1 ziguimu ziguimu  270 Oct 23 12:24 input.csv
-rwxrwxrwx 1 ziguimu ziguimu 3.6K Oct 23 12:24 pcann_raw_18_structures.csv
drwxrwxrwx 1 ziguimu ziguimu 4.0K Oct 23 09:31 pdb
-rwxrwxrwx 1 ziguimu ziguimu  13K Oct 23 12:24 structure_checks.csv

========== Raw CSV diagnostics ==========
Shape: (18, 30)
Columns: ['pdb_id', 'avg', 'model_1', 'model_2', 'model_3', 'model_4', 'model_5', 'model_6', 'model_7', 'model_8', 'model_9', 'model_10', 'model_11', 'model_12', 'model_13', 'model_14', 'model_15', 'model_16', 'model_17', 'model_18', 'model_19', 'model_20', 'model_21', 'model_22', 'model_23', 'model_24', 'model_25', 'pcann_label', 'candidate_id', 'boltz_model']

--- pdb_id ---
dtype: object
sample: ['c0082m0', 'c0082m1', 'c0082m2', 'c0096m0', 'c0096m1', 'c0096m2', 'c0200m0', 'c0200m1']

--- candidate_id ---
dtype: object
sample: ['candidate_0082', 'candidate_0082', 'candidate_0082', 'candidate_0096', 'candidate_0096', 'candidate_0096', 'candidate_0200', 'candidate_0200']

--- avg ---
dtype: float64
sample: [-8.96, -9.14, -9.23, -9.06, -9.12, -8.74, -8.92, -8.99]
non-numeric count: 0
(pcann) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH
…
诊断结果已经把范围缩小了：

pcann_raw_18_structures.csv 已成功写出，包含 18 行、30 列，说明模型预测和候选映射都已经完成。

原始 avg 列是 float64，示例值为 -8.96、-9.14 等，没有非数值项。

出错的是后续 groupby().agg() 得到的 summary["pcann_avg_mean"]，它意外成了 object 类型。

因此，不需要重新运行模型，也不要删除缓存。我们可以先验证汇总结果，并把汇总计算改为显式数值类型；同时检查所有候选物是否各有 3 个结构。

现在进行最小修复
原因很可能是 PCANN 的 make_prediction() 将字符串形式的 pdb_id 和数值分数放进同一个 DataFrame 后再转置、拼接，导致内存中的 avg 列仍是 object 类型；写入 CSV 后，Pandas 重新读取时又正确识别成了 float64。这与目前的诊断结果吻合。

请执行下面的命令。它会先备份脚本，再在汇总前显式转换 avg 和 25 个模型分数列，并验证转换结果；不会改动模型或结构缓存。

cd LOCAL_PATH

python - <<'PY'
from pathlib import Path
from datetime import datetime

path = Path("examples/make_predictions/run_glp1r_pcann_batch.py")
source = path.read_text()

anchor = '''    if len(output) != 18:
        raise RuntimeError(f"Expected 18 prediction rows; got {len(output)}")

    output.to_csv(RAW_CSV, index=False)
'''

replacement = '''    if len(output) != 18:
        raise RuntimeError(f"Expected 18 prediction rows; got {len(output)}")

    # make_prediction() may leave mixed-type DataFrame columns as object.
    # Explicitly convert all PCANN scores to numeric before aggregation.
    score_columns = ["avg"] + [f"model_{i}" for i in range(1, 26)]
    for column in score_columns:
        output[column] = pd.to_numeric(output[column], errors="raise")

    if output[score_columns].isna().any().any():
        raise RuntimeError("NaN found in PCANN prediction scores")
    if not output[score_columns].map(lambda x: __import__("math").isfinite(x)).all().all():
        raise RuntimeError("Non-finite value found in PCANN prediction scores")

    output.to_csv(RAW_CSV, index=False)
'''

count = source.count(anchor)
if count != 1:
    raise SystemExit(
        f"安全检查失败：预期找到唯一插入位置，实际找到 {count} 处。未修改文件。"
    )

backup = path.with_name(
    path.name + ".backup_" + datetime.now().strftime("%Y%m%d_%H%M%S")
)
backup.write_text(source)
path.write_text(source.replace(anchor, replacement, 1))

print("已备份：", backup)
print("已更新：", path)
PY

python -m py_compile examples/make_predictions/run_glp1r_pcann_batch.py

如果语法检查通过，再运行批处理：

PYTHONPATH=LOCAL_PATH \
python examples/make_predictions/run_glp1r_pcann_batch.py

这次正常情况下应直接复用已有缓存完成预测汇总，不需要重新计算结构嵌入。

成功后应当生成：

pcann_raw_18_structures.csv：18 个结构的原始预测分数

candidate_summary.csv：6 个候选物的汇总结果

structure_checks.csv：结构检查记录

请把最终打印的 Candidate summary 表格贴给我。我们再检查每个候选物是否都有 3 个结构，以及均值、标准差和排序是否合理。注意，avg 是 PCANN 的模型预测分数，不能直接当作实验测得的 
K
d
K 
d
​
 。

Candidate summary:
  candidate_id  n_structures  pcann_avg_mean  pcann_avg_std  pcann_avg_min  pcann_avg_max
candidate_0043             3         -9.1200         0.2516          -9.28          -8.83
candidate_0044             3         -8.9433         0.1553          -9.07          -8.77
candidate_0082             3         -9.1100         0.1375          -9.23          -8.96
candidate_0096             3         -8.9733         0.2043          -9.12          -8.74
candidate_0173             3         -8.9600         0.2427          -9.16          -8.69
candidate_0200             3         -8.9700         0.0436          -9.00          -8.92
(pcann) ziguimu@DESKTOP-8RLFC97:LOCAL_PATH
很好，这次 PCANN 批处理已经成功完成汇总。6 个候选物都各有 3 个 Boltz-2 结构，总计 18 个结构全部进入了统计结果。

1. 当前 PCANN 汇总结果
候选物

结构数

平均分

标准差

最低分

最高分

candidate_0043

3

-9.1200

0.2516

-9.28

-8.83

candidate_0082

3

-9.1100

0.1375

-9.23

-8.96

candidate_0044

3

-8.9433

0.1553

-9.07

-8.77

candidate_0173

3

-8.9600

0.2427

-9.16

-8.69

candidate_0200

3

-8.9700

0.0436

-9.00

-8.92

candidate_0096

3

-8.9733

0.2043

-9.12

-8.74

上表按平均分从数值较小到较大排列。这只是分数排序，不等同于已验证的结合能力排名。 需要先确认 PCANN 的输出分数方向，以及它在这批 GLP1R 复合物上的判别能力，才能赋予生物学解释。

2. 这组结果目前能说明什么？
数值排序靠前： candidate_0043（−9.1200）和 candidate_0082（−9.1100）非常接近，均值只差 0.0100，不能据此认为二者有明确差异。

三结构间最稳定： candidate_0200 的标准差最低，为 0.0436，说明这 3 个结构的 PCANN 分数较一致；但一致不代表预测一定准确。

结构间波动较大： candidate_0043 和 candidate_0173 的标准差分别为 0.2516 和 0.2427，提示其分数对不同预测结构更敏感，值得结合具体结构检查。

整体差异不大： 六个候选物的平均分从 −9.1200 到 −8.9433，跨度约 0.177。是否具有判别意义，目前还无法判断。

3. 下一步建议
先保留当前结果，不要仅凭 PCANN 均值筛掉候选物。建议把这份汇总与现有 Boltz-2 结构评价指标合并，逐个检查：

PCANN 分数与 Boltz-2 的 ipTM、界面几何等指标是否一致。

同一候选物的 3 个结构是否具有相似的结合姿态和界面。

候选物之间的分数差异，是否大于同一候选物不同结构带来的波动。

另外，PCANN 预测分数的方向和量纲仍需核对模型定义，所以现阶段应称为“PCANN 分数”，而不要直接称为结合自由能或 
K
d
K 
d
​
 。

如果你愿意，下一步我们可以直接对照 18 个结构的原始 PCANN 分数和 Boltz-2 评价结果，形成一张六个候选物的综合比较表。

这个分数怎么看
你这次得到的 PCANN 分数，最重要的是先分清楚两件事：分数在模型内部代表什么，以及它能不能用来判断 GLP1R 候选物谁更可能结合。

目前你得到的分数大约在 −8.69 到 −9.28 之间。不能仅凭负号就判断结合好，也不能直接把它当成实验结合自由能或 
K
d
K 
d
​
 。

1. 先看你这批结果
候选物

PCANN 平均分

三个结构的标准差

candidate_0043

−9.1200

0.2516

candidate_0082

−9.1100

0.1375

candidate_0200

−8.9700

0.0436

candidate_0096

−8.9733

0.2043

candidate_0173

−8.9600

0.2427

candidate_0044

−8.9433

0.1553

如果暂时只按数值从小到大排序，0043 和 0082 排在前面。但这只是数学排序，尚不能说它们的结合能力更强。

标准差反映的是三个结构所得分数的离散程度，不是预测准确率，也不是实验重复性。

2. 更关键的是：你的脚本实际上怎样定义这个分数？
在 PCANN 的 make_prediction() 中，模型输出经过了下面的换算：

R = 1.987204258e-03
T = 298
dg = output.item() * R * T

其中 
R
T
≈
0.592
 kcal/mol
RT≈0.592 kcal/mol。因此，你的 avg 不是模型未经处理的原始输出，而是代码将模型输出乘以 
R
T
RT 后得到的数值，再对 25 个模型的结果求平均。

这也意味着，需要核对 PCANN 模型的训练标签与输出定义，才能最终确认它是否严格对应预测结合自由能 
Δ
G
ΔG。不能只凭变量名 dg 就认定其物理含义已经得到验证。

如果模型定义确认它是结合自由能，那么通常：

Δ
G
ΔG 越负，预测结合在热力学上越有利。

Δ
G
ΔG 越接近零，预测结合的有利程度越低。

但预测自由能仍然不是实验测量值，也不能单凭它确认候选物会结合。

3. 你的候选物之间，差异到底有多大？
若暂时按上述自由能解释，最高与最低的候选物平均分相差约 
0.177
 kcal/mol
0.177 kcal/mol。在理想的热力学关系成立时，这只相当于约 1.35 倍的平衡常数差异。

相比之下，你每个候选物的三个结构之间，分数标准差约为 0.044–0.252。也就是说，候选物之间的均值差异很小，不能据此做强结论。

我建议下一步先查看 PCANN 的模型输出定义和训练标签，确认这个分数是否确实是 
Δ
G
ΔG。确认后，再决定排序方向和如何与 Boltz-2 的 ipTM、界面接触及几何指标联合筛选。

PCANN分数是越小越好吗
目前还不能无条件地说 PCANN 分数越小越好，但从你这批结果的计算方式看，如果模型输出确实代表结合自由能 
Δ
G
ΔG，那么通常是越负越好。

你的 PCANN 代码里有这一步：

dg = output.item() * R * T

其中 
R
×
T
≈
0.592
R×T≈0.592。这说明程序把模型原始输出乘以 
R
T
RT，并将结果命名为 dg。不过，变量名叫 dg 并不能单独证明训练标签的定义和模型输出方向正确对应结合自由能，还需要核对 PCANN 的训练标签。

按“数值越负越好”的暂定解释，你这批候选的排序如下：

候选

PCANN 平均分

暂定解读

candidate_0043

−9.1200

较好

candidate_0082

−9.1100

较好

candidate_0044

−8.9433

相对较弱

candidate_0173

−8.9600

相对较弱

candidate_0200

−8.9700

相对较弱

candidate_0096

−8.9733

相对较弱

注意，这些分数差距很小，而且每个候选只有 3 个结构。因此，暂时不能据此认定 candidate_0043 一定优于 candidate_0082，更不能直接断言其实际亲和力更强。

下一步最重要的是确认 PCANN 训练时的标签究竟是 ln(Kd)、结合自由能，还是其他亲和力指标。确认之后，才能最终确定分数方向。确认前，建议将它作为辅助排序指标，并结合 Boltz-2 的 ipTM、界面接触和结构合理性综合判断。

---

# chatgpt response

我已收到这部分 **PCANN 批处理与第十二阶段总结所需的记录**。我先不生成最终工作记录，等你明确说材料已经发完、可以开始后再统一整理。

这部分我会保留的关键信息包括：

- **PCANN 流程：** 处理 6 个候选物、每个候选 3 个 Boltz-2 结构，共 18 个结构；修复候选标签映射和汇总数值类型问题，最终成功输出原始预测结果与候选统计。
- **结果文件：** `pcann_raw_18_structures.csv`、`candidate_summary.csv`、`structure_checks.csv`。
- **最终项目候选：** `candidate_0082`、`candidate_0096`、`candidate_0200`、`candidate_0043`。
- **结果解释边界：** PCANN 分数是计算预测结果，不是实验测得的 $K_d$；分数方向与物理意义需要按模型定义谨慎解释。
- **项目结项定位：** 计算预测、结构评价与候选优选工作告一段落；由于目前缺少湿实验条件，真实结合能力和 GLP1R 激动功能尚未得到实验验证。

你继续发送剩余的历史工作记录即可。我会等你明确通知后，再把所有阶段串起来，写成一份**详细、按实际工作顺序组织、包含关键参数和结果、明确区分已完成与未验证事项的第十二阶段工作记录**。

---

# you asked

message time: 2026-10-23 13:12:27

把这次PCANN测出来的G值粗略换算成K
可以。若把这次 PCANN 输出的 
G
G 值暂时视为标准结合自由能 
Δ
G
∘
ΔG 
∘
 ，可以用热力学关系粗略换算解离常数 
K
d
K 
d
​
 ：

Δ
G
∘
=
R
T
ln
⁡
K
d
ΔG 
∘
 =RTlnK 
d
​
 
因此：

K
d
=
exp
⁡
(
Δ
G
∘
R
T
)
K 
d
​
 =exp( 
RT
ΔG 
∘
 
​
 )
这里要特别注意：这个换算成立的前提是 PCANN 的分数确实对应以标准态为基准、单位为 kcal/mol 的结合自由能。 你的代码使用 
R
=
1.9872
×
10
−
3
 
k
c
a
l
 
m
o
l
−
1
 
K
−
1
R=1.9872×10 
−3
  kcalmol 
−1
 K 
−1
 、
T
=
298
 
K
T=298 K，所以 
R
T
≈
0.592
 
k
c
a
l
/
m
o
l
RT≈0.592 kcal/mol。下面先按这一假设计算，作为数量级参考，而不是实验亲和力预测。

换算结果（假设 
G
=
Δ
G
∘
G=ΔG 
∘
 ）
温度 298 K；
R
T
=
0.5922
RT=0.5922 kcal/mol；换算结果为理论估算。

候选

PCANN 的 
G
G（kcal/mol）

粗略换算的 
K
d
K 
d
​
 

candidate_0043

−9.1200

205 nM

candidate_0082

−9.1100

208 nM

candidate_0044

−8.9433

276 nM

candidate_0200

−8.9700

264 nM

candidate_0096

−8.9733

263 nM

candidate_0173

−8.9600

269 nM

换算公式：

K
d
(
M
)
=
e
G
/
0.5922
K 
d
​
 (M)=e 
G/0.5922
 
怎么理解这些数值？

按上述假设，估算的 
K
d
K 
d
​
  约为 205–276 nM。

candidate_0043 和 candidate_0082 的估算值最低，彼此非常接近。

这批候选之间的估算差异不大，不能据此断言哪一个在实验中亲和力更强。

重要限制： 这些 nM 数值只是基于热力学公式的条件性换算，不能直接当作 PCANN 预测的真实 
K
d
K 
d
​
 。在把它们用于候选筛选前，仍需确认 PCANN 的训练标签、输出定义和单位是否确实支持这种换算。

指标

D13

D41

D44

Semaglutide

SPR $K_D$（µM）

8.58

5.19

6.78

2.78

跟这个SPR Kd有可比性吗

…
有一定可比性，但目前只能比较数量级，不能直接把 PCANN 换算出的 
K
d
K 
d
​
  当作与 SPR 实测值等价的结果。

你给出的 SPR 数据是：

分子

SPR 
K
D
K 
D
​
 （µM）

换算为 nM

D13

8.58

8,580

D41

5.19

5,190

D44

6.78

6,780

Semaglutide

2.78

2,780

按前面暂时假设的 
G
=
Δ
G
∘
G=ΔG 
∘
 ，你的 PCANN 分数对应的 
K
d
K 
d
​
  约为 0.205–0.276 µM，即 205–276 nM。

两组数值相差多少？
把 PCANN 换算结果与 SPR 数据放在一起：

对比对象

PCANN 条件性估算

SPR 实测

PCANN 候选范围

0.205–0.276 µM

—

D13

—

8.58 µM

D41

—

5.19 µM

D44

—

6.78 µM

Semaglutide

—

2.78 µM

如果这些分子针对的是同一个靶点、相同的结合体系，并且 PCANN 换算假设成立，那么 PCANN 给出的数值会比这些 SPR 数值低约 10–42 倍。但这不一定代表 PCANN 高估了亲和力，也可能是模型输出定义、训练数据、标准态假设或分子体系不同造成的。

这组数据能用来验证 PCANN 吗？
可以作为初步参照，但还不够。

先确认可比性： SPR 测的是哪个靶点、哪种分子形式，以及 PCANN 输入结构对应的是否是同一结合体系。

确认 PCANN 的标签定义： 只有在确认其输出可以按结合自由能解释后，才能将分数换算成 
K
d
K 
d
​
 。

不要仅凭数值大小判断模型准确性： PCANN 的估算值与 SPR 相差一个数量级，并不能单独证明模型失效；反过来，数值接近也不代表模型已得到验证。

还有一个关键点：Semaglutide 是 GLP-1 类药物。如果这些 SPR 数据来自它与 GLP-1R 的结合，而你的 PCANN 候选也是针对 GLP-1R，那么体系可能具有一定可比性；但如果靶点、分子构建或测定条件不同，就不能直接对照。

我建议先确认这四个 SPR 数值是否来自 GLP-1R，以及 D13、D41、D44 分别是什么分子。 这样才能判断这组数据能否用于校准你目前的 PCANN 结果。
这算是刚刚的补充，之后才是工作记录

---

# chatgpt response

收到，这部分我会作为 **Stage 12 工作记录的补充材料**保留，放在 PCANN 结果分析之后，作为“PCANN 输出的条件性 $K_D$ 换算及 SPR 数据对照”。

我会特别保留以下几点：

1. **条件性换算结果**：在暂时假设 PCANN 输出的 $G$ 就是以 kcal/mol 为单位的标准结合自由能时，按 $K_D=\exp(G/RT)$ 换算，六个候选约为 205–276 nM。
2. **SPR 参照数据**：D13 为 8.58 µM、D41 为 5.19 µM、D44 为 6.78 µM、Semaglutide 为 2.78 µM。
3. **可比性限制**：这些数据可以作为初步参照，但目前不能据此认定 PCANN 的 $K_D$ 预测准确，也不能直接断言 PCANN 高估了亲和力。还需要确认 PCANN 输出的物理含义，以及 SPR 数据对应的靶点、分子形式和测定体系。
4. **项目结论的边界**：这属于计算结果的补充解释，不是实验验证。换算值会明确标注为**条件性估算值，而非实测或已验证的 $K_D$**。

我也会保留候选选择的最终决定：**candidate_0082、candidate_0096、candidate_0200、candidate_0043**，不会因为这次换算就擅自调整最终候选名单。

你继续发送之前的工作记录即可。我会继续等待，等你明确说材料发完、可以开始后，再统一整理 Stage 12。

---

# you asked

message time: 2026-10-23 13:12:39

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

---

# chatgpt response

收到，这是 **GLP-1R 项目阶段一：参考序列与结构准备**的完整工作记录。我会将它作为原始阶段记录保留，后续整理 Stage 12 时用于还原项目的起点、参考结构来源和数据准备过程。

我会特别保留几个重要细节：

- **参考结构：** PDB 7KI0，Semaglutide–GLP-1R 冷冻电镜复合物，分辨率 2.50 Å。
- **受体残基映射：** 384 个结构残基全部匹配构建体 FASTA，0 个氨基酸错配；同时保留 PDB 编号与 FASTA 位置不一致这一注意事项。
- **Semaglutide 序列核对：** 聚合物序列为 31 位，实际有坐标的肽链残基为 30 个；第 31 位 Gly 没有对应的已建模坐标。AIB 和 WF1 的处理也会明确区分。
- **阶段边界：** 这一阶段完成的是参考数据准备和结构核验，不能写成已经完成候选设计或结合能力验证。

我暂时不合并、不改写成最终工作记录，也不擅自修正原始记录中的表述。你继续发送后续阶段材料即可；等你明确说发完了，我再统一整理。

---

# you asked

message time: 2026-10-23 13:12:58

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

收到，已将这份材料作为 **阶段二：参考结构界面分析与输入文件核查（2026-10-19）** 的工作记录纳入本次整理材料。

后续编写 Stage 12 时，我会保留以下关键证据链：

- **参考界面基准：** 以 7KI0 中 Semaglutide–GLP-1R 复合物为参照，复跑 4 Å 和 5 Å 的重原子接触分析。
- **接触统计：** 4 Å 下有 60 对不同的肽—受体残基组合；5 Å 下有 108 对。原子对数量与残基对数量会分开记录。
- **输入文件核查：** 确认分析使用的是保留 AIB、排除 WF1 的 30 残基肽链文件；236 个共有原子的坐标与原始提取文件完全一致。
- **原子级观察：** 保留四组代表性最近距离及其受限解释，不会仅凭距离就认定存在特定化学相互作用。
- **科学结论边界：** 这一步建立的是可复现的参考结构几何描述，不是结合自由能、实验亲和力或激动活性的验证。

我会继续按你提供的阶段顺序接收材料，不提前生成或合并最终文本。等你明确通知材料已全部发完后，再统一整理 Stage 12。

---

# you asked

message time: 2026-10-23 13:13:09

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

---

# chatgpt response

收到。这份材料包含 **阶段三：ProteinMPNN 输入准备与小规模验证**，以及后续的 **受体链连续重编号与回归测试补充记录**。我会将两部分都纳入项目时间线，并保留它们之间的先后关系。

后续整理时，我会重点保留：

- **初始测试：** 使用 `v_48_020`，以链 P 为设计链、链 R 为固定受体，生成 2 条测试序列，并验证 12 个固定位置。
- **问题定位：** 受体链有 384 个实际残基，但原始 PDB 编号缺口使 ProteinMPNN 将其解析为 395 个位置，其中 11 个是 `-` 占位符。
- **输入修正：** 创建连续重编号的独立结构文件，将受体链编号为 1–384，不改变原子坐标，并重新生成对应的固定位置配置。
- **回归测试：** 修正后受体链解析长度为 384、占位符为 0；肽链仍为 30 aa，两条测试序列均通过固定位置检查。
- **尚未完成的工作：** 这份记录明确指出，1,000 条序列生成尚未启动；末端 Gly 的补回、批量输出核验和后续筛选也仍待完成。

我还会区分**测试阶段的结果**与**后续正式设计结果**，避免将 2 条序列的回归测试误写成大规模生成已经完成。

继续发下一份即可。我会按你的要求等待，不提前生成最终 Stage 12 工作记录。

---

# you asked

message time: 2026-10-23 13:13:23

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

收到。这份材料我会作为 **阶段四：ProteinMPNN 正式序列生成与结果审计**及其补充分析一并保留。

我会特别区分以下几组数据，避免后续整理时混淆：

- **生成规模：** 50 个随机种子批次，共 10,000 条候选记录；每条序列为 30 aa，全部通过当前固定位置和字符检查。
- **去重结果：** 1,435 条唯一序列，其中 603 条至少出现两次；重复记录超额数为 8,565。
- **评分审计：** 已检查 `score`、`global_score` 和 `seq_recovery` 的代码含义，明确它们属于模型内部指标，不是实验亲和力或激动活性。
- **采样支持与评分的关系：** 出现频次与平均 `score` 的 Spearman 相关系数为 −0.5156，跨 seed 数与平均 `score` 的相关系数为 −0.5155。当前先作为描述性统计发现，不写成已完成显著性验证的结论。
- **项目状态：** 这一阶段完成了序列生成、去重和基础审计，但尚不能据此认定最佳候选，也不代表已验证任何候选的 GLP-1R 结合能力或激动活性。

后续整理时，我会把这份记录中的历史路径 `LOCAL_PATH 与后续实际使用的项目目录区分开，并保留当时的文件名和实验状态，不将后续结果倒填成早期已完成的工作。

你继续发送后续阶段记录即可。我会继续等待你的最终通知。

---

# you asked

message time: 2026-10-23 13:13:57

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

收到。这份记录我会作为 **阶段五：从已验证候选物反推筛选逻辑（2026-10-19）** 纳入项目时间线。

这次研究思路的转变很重要，我会保留它与前一阶段的衔接关系：

1. **前一阶段发现的问题：** 10,000 条生成序列的第 10 位均为 V，但该位不在现有固定位置配置中；由于原始生成命令和实际运行时配置尚未找到，DV 现象的原因仍未确定。
2. **研究方向调整：** 不再仅围绕 DV 位点异常继续推测，而是转向 D13、D41、D44 这三条经过实验验证的候选物，以它们为参考锚点，重建论文筛选流程。
3. **证据优先原则：** 区分论文明确报告的筛选规则、项目实际实现的规则，以及尚待验证的假设；不擅自补造筛选阈值。
4. **数据处理原则：** 保留原有 1,435 条去重序列、此前两轮筛选结果和相关脚本；重新初筛时建立独立版本，记录每一步的输入、规则和数量变化。
5. **待解决的关键问题：** 核实 D13、D41、D44 的准确序列与编号，统一 30 aa 结构支持序列和 31 aa 论文序列的对齐方式，再判断 DV 位点的实际含义。

我会将这一阶段记录为**筛选策略重建的研究转折点**，而不是已经成功复现论文筛选算法的证明。

你可以继续发送后续工作记录。我会继续等待，不提前编写最终 Stage 12 文档。

---

# you asked

message time: 2026-10-23 13:14:07

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

---

# chatgpt response

收到，这份记录我会作为 **GLP1R_reproduction 阶段四及后续候选筛选工作的依据**保留在当前整理上下文中，重点包括：

- 10,000 条 ProteinMPNN 生成记录 → 1,435 条唯一序列；
- 两轮切割位点筛选 → 308 条候选序列；
- Hamming 距离与完全连接层次聚类 → 65 条代表序列；
- DV 位点、原始运行参数及论文筛选规则一致性等尚未解决的问题；
- 各阶段输出文件、审计结果与结论边界。

我会继续等待你发送剩余工作记录，**暂不生成阶段十二工作记录，也不提前整合成项目总结**。等你明确说材料已经发完、可以开始后，我再统一整理，尽量保留完整的工作过程、关键数据、方法变更、文件路径和未解决问题。

---

# you asked

message time: 2026-10-23 13:14:21

# GLP-1RA 计算设计与候选序列筛选工作记录

**项目目录：** `LOCAL_PATH  
**记录时间：** 2026-10-20  
**当前阶段：** ProteinMPNN 序列生成后的规则筛选与理化性质初筛  
**当前候选集：** 240 条独特候选序列  
**当前阶段定位：** 计算筛选与候选集整理，不代表已验证受体激动活性、结合亲和力、体内稳定性或药代动力学性质。

---

## 一、研究思路的转变：从生成序列到建立可解释的筛选流程

### 1.1 初始目标

本项目围绕 GLP-1 受体激动剂（GLP-1 receptor agonists，GLP-1RAs）的计算设计展开，以司美格鲁肽（Semaglutide）的肽序列作为初始参考模板，尝试利用 ProteinMPNN 在一定的序列和结构约束下生成候选肽。

最初的工作重点是生成序列，并从大量设计结果中筛选出值得继续研究的候选物。但序列生成数量本身并不能说明候选物的质量：生成结果可能存在重复、潜在蛋白酶切割位点、理化性质不适宜等问题；即使某条序列通过规则筛选，也不能据此认定其具有 GLP-1R 结合能力或受体激动活性。

因此，工作思路逐步从“生成更多序列”转向：

> **建立一条有明确规则、可追溯、能够解释每一步候选去留原因的计算筛选流程。**

### 1.2 项目的基本逻辑

当前流程分为三个层次：

1. **序列层面的规则筛选：** 去除冗余序列，检查特定序列位置、潜在切割位点及残基约束。
2. **全局理化性质筛选：** 计算净电荷和平均疏水性（GRAVY），逐步缩小候选范围。
3. **后续候选评估：** 对剩余序列进一步开展序列多样性分析、结构建模、受体界面评估及必要的稳定性研究。

本阶段已经完成前两层中的一部分，获得 240 条候选序列。结构层面与实验层面的证据尚不能由当前筛选结果替代。

---

## 二、序列生成与初始数据整理

### 2.1 设计起点

司美格鲁肽的参考肽骨架序列为：

`HAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG`

该序列长度为 31 aa。

项目记录中的初始设计方案为：使用 ProteinMPNN 生成约 10,000 条候选序列，在设计过程中固定 13 个保守氨基酸，其余 18 个位置由模型设计。由于设计空间受到序列约束和结构约束限制，生成序列中存在重复结果。

这里的“固定 13 个位置、设计 18 个位置”是当前项目记录所述的设计设置；若用于正式发表或复现，应进一步与实际运行脚本、输入结构及 ProteinMPNN 参数核对。

### 2.2 去重处理

项目原始说明记录：10,000 条生成序列去重后获得 1,443 条唯一序列。

但本次后续筛选实际使用的输入文件：

`results/proteinmpnn/test_2000seq_renumbered/deduplicated/unique_candidates_all50_v2.fasta`

其中记录了 **1,435 条唯一序列**。

因此，目前存在一个需要保留并核查的数据差异：

| 数据来源 | 记录的唯一序列数 |
|---|---:|
| 初始项目说明 | 1,443 |
| 后续实际筛选 FASTA | 1,435 |
| 数量差异 | 8 |

在确认原始生成文件、去重脚本及不同版本的输入范围之前，不应将这两个数字当作完全一致。后续各轮筛选的数量统计均以实际使用的 1,435 条 FASTA 为起点。

---

## 三、逐轮筛选记录

### 3.1 筛选总览

| 阶段 | 筛选依据 | 输入 | 保留 | 排除 |
|---|---|---:|---:|---:|
| 初始去重序列 | 唯一序列集合 | 1,435 | 1,435 | 0 |
| Step 1 | EF/WL 相关序列约束 | 1,435 | 787 | 648 |
| Step 2 | N 端前 15 位约束（第 12 位例外） | 787 | 426 | 361 |
| Step 3 | C 端锚定位点约束 | 426 | 425 | 1 |
| Step 4 | 第 19–23 位相关疏水性约束 | 425 | 381 | 44 |
| Step 5 | 指定位置的残基排除规则 | 381 | 347 | 34 |
| Step 6 | pH 7.4 估算净电荷绝对值 ≤ 2 | 347 | 330 | 17 |
| Step 7 | 净电荷范围 −1.1634 至 +1.0 | 330 | 256 | 74 |
| Step 8 | GRAVY（Kyte–Doolittle）≥ −1.1 | 256 | **240** | 16 |

**注意：** Step 5 的实际输入是 381 条、保留 347 条、排除 34 条。不能将 Step 4 之前的筛选数量混入 Step 5 的统计。

### 3.2 Step 1：EF/WL 相关序列约束

**输入：** 1,435 条唯一序列  
**保留：** 787 条  
**排除：** 648 条

**目的与原理：**

本轮根据项目中命名为 `EF_WL` 的筛选步骤，检查与 E/F、W/L 相关的序列约束，首先缩小候选集合。

这一阶段属于序列规则筛选，主要作用是去除不符合既定设计条件的序列，而不是直接判断候选肽的受体活性或药理效力。

**结果：**

保留 787 条序列，占输入的约 54.77%。

**可追溯目录：**

`results/proteinmpnn/test_2000seq_renumbered/`

**记录限制：**

本工作记录根据现有步骤名称和数量汇总。EF/WL 的精确位置、逻辑组合及边界条件，应以对应的 `screening_step1_EF_WL_v1` 脚本为准，不应仅凭目录名推断具体规则。

### 3.3 Step 2：N 端前 15 位约束（第 12 位例外）

**输入：** 787 条  
**保留：** 426 条  
**排除：** 361 条

**目的与原理：**

该轮针对 N 端前 15 个残基执行序列位置约束，并在第 12 位设置例外规则。

这类位置特异性筛选可以将设计限制落实到具体序列位置，减少不符合既定设计方案的候选物。但具体位置允许哪些残基、例外如何定义，应由原始脚本确定。

**结果：**

保留 426 条，占本轮输入的约 54.13%。

**可追溯目录：**

`results/proteinmpnn/test_2000seq_renumbered/screening_step2_Nterm15_except12_v1/`

### 3.4 Step 3：C 端锚定位点约束

**输入：** 426 条  
**保留：** 425 条  
**排除：** 1 条

**目的与原理：**

该轮检查 C 端相关的锚定位点，确保候选序列符合预先定义的末端残基要求。

末端序列约束可以帮助维持设计所需的序列特征，但其生物学意义取决于实际约束位置及其依据。不能仅凭“锚点”一词推断该位置已经被证明对 GLP-1R 激动活性必不可少。

**结果：**

仅排除 1 条序列，425 条进入下一轮。

**可追溯目录：**

`results/proteinmpnn/test_2000seq_renumbered/screening_step3_Cterm_anchors_v1/`

### 3.5 Step 4：第 19–23 位相关疏水性约束

**输入：** 425 条  
**保留：** 381 条  
**排除：** 44 条

**目的与原理：**

该轮根据项目定义的第 19–23 位相关疏水性规则筛选序列。

蛋白质或多肽的局部疏水残基分布可能影响局部构象、溶剂暴露、分子间相互作用和聚集倾向。因此，除全局平均疏水性外，特定位置的疏水性也可以作为设计约束。

不过，局部疏水性并不能单独决定溶解度或聚集行为；实际效果还受到结构、溶剂暴露程度及其他序列特征影响。

**结果：**

保留 381 条，排除 44 条。

**可追溯目录：**

`results/proteinmpnn/test_2000seq_renumbered/screening_step4_hydrophobic_19_23_v1/`

### 3.6 Step 5：指定位置的残基排除规则

**输入：** 381 条  
**保留：** 347 条  
**排除：** 34 条

**筛选规则：**

- 第 12 位：允许 A、E、Q；
- 第 16 位：要求 A；
- 第 17 位：允许 A、E；
- 第 24 位：要求 A；
- 第 27 位：允许 I、V。

**目的与原理：**

该轮将位置特异性的残基要求组合起来，进一步去除不符合预设设计约束的序列。

这里的规则属于项目采用的序列设计约束，不能仅凭其形式就断言每一条规则都已经过独立的生物学验证。

**结果：**

347 条序列进入理化性质分析。

**可追溯目录：**

`results/proteinmpnn/test_2000seq_renumbered/screening_step5_residue_exclusions_v1/`

---

## 四、理化性质分析：从序列约束转向候选性质评估

完成 Step 5 后，对 347 条候选序列计算了估算净电荷和平均疏水性，并对参考肽进行同口径分析。

### 4.1 计算方法

候选序列的理化性质分析目录：

`results/proteinmpnn/test_2000seq_renumbered/physicochemical_analysis_v1/`

主要文件：

- `analyze_properties.py`
- `sequence_properties.csv`
- `SUMMARY.md`

参考肽分析目录：

`results/proteinmpnn/test_2000seq_renumbered/reference_peptide_properties_v1/`

主要文件：

- `analyze_reference_peptides.py`
- `per_residue_raw_data.csv`
- `sequence_summary.csv`
- `SUMMARY.md`

当前计算采用以下定义：

1. **净电荷：** 在 pH 7.4 条件下，根据近似 pKa 估算；假设 N、C 端未修饰，不考虑额外化学修饰。
2. **GRAVY：** 使用 Kyte–Doolittle 疏水性标度，对序列中各残基的疏水性数值求平均。
3. **候选长度：** 本轮候选序列均为 30 aa。
4. **参考肽长度：** 下列参考序列均为 31 aa。

需要注意，未修饰肽的计算电荷不等同于实际药物制剂的电荷状态。如果未来设计中包含 C 端酰胺化、脂肪酸侧链或其他化学修饰，需要重新计算或评估。

### 4.2 347 条候选的理化性质概况

| 指标 | 统计结果 |
|---|---:|
| 候选序列数 | 347 |
| 净电荷均值 | +0.7549 |
| 净电荷中位数 | +0.8355 |
| 净电荷最小值 | −1.1644 |
| 净电荷最大值 | +3.8350 |
| 净电荷大于 0 的序列 | 234 |
| 净电荷小于 0 的序列 | 113 |
| 净电荷绝对值小于 0.5 的序列 | 101 |
| GRAVY 均值 | −0.8767 |
| GRAVY 中位数 | −0.8633 |
| GRAVY 最小值 | −1.2767 |
| GRAVY 最大值 | −0.4600 |

这些数据描述的是序列层面的估算性质，不代表实验测得的溶解度、聚集程度、体内半衰期或药效。

### 4.3 参考肽对照

参考序列及对应统计如下：

| 指标 | Semaglutide | D13 | D41 | D44 |
|---|---:|---:|---:|---:|
| 序列长度 | 31 | 31 | 31 | 31 |
| pH 7.4 估算净电荷 | −1.163405 | −0.163706 | −0.163706 | −0.164184 |
| GRAVY（KD） | −0.254839 | −0.741935 | −1.006452 | −0.764516 |
| KD 疏水性数值大于 0 的残基数 | 11/31 | 10/31 | 8/31 | 10/31 |
| AVILMFWY 残基数 | 13/31 | 11/31 | 9/31 | 11/31 |

其中：

- `KD 疏水性数值大于 0 的残基数`，指按 Kyte–Doolittle 标度计算后疏水性数值大于 0 的残基数。
- `AVILMFWY 残基数`，是按指定氨基酸集合统计的残基数量，属于另一种组成指标。
- 两者定义不同，不能互相替代。

参考肽分析为后续阈值设计提供了比较基准，但参考肽的理化性质本身不能证明某一阈值是最优的，也不能将某条参考肽的性质直接等同于其体内药代性质的原因。

---

## 五、Step 6：净电荷绝对值不超过 2

**目录：**

`results/proteinmpnn/test_2000seq_renumbered/screening_step6_abs_charge_le_2_v1/`

**输入文件：**

Step 5 保留的 347 条序列。

**筛选规则：**

保留满足下式的候选序列：

`abs(net_charge_pH7.4) <= 2`

边界值包含在保留范围内。

**原理与依据：**

净电荷会影响多肽与溶剂、带电分子及生物界面的相互作用。过高的正电荷可能增加非特异性静电吸附的风险；电荷分布也可能影响溶解性、分布及其他分子性质。

但“净电荷绝对值不超过 2”在本项目中是用于初筛的操作性规则，而不是已经通过本项目实验验证的普遍药物开发标准。实际影响取决于序列、结构、修饰方式、给药途径及其他因素。

**结果：**

| 指标 | 数量 |
|---|---:|
| 输入 | 347 |
| 保留 | 330 |
| 排除 | 17 |
| 保留率 | 95.10% |

被排除的 17 条序列均因估算净电荷超过本轮设定范围而未进入下一阶段。

**输入文件 SHA-256：**

`115e943738018c356dd5c727387041201d07dbc4340e87833f5fc5255321a94d`

**性质表 SHA-256：**

`009c838ada398a59ff894782f29223293db6a5eb487094cdf7df93dd2f227be7`

**结果文件：**

- `run_screening.py`
- `retained.fasta`
- `rejected.fasta`
- `screening_audit.csv`
- `SUMMARY.md`

本轮完成了输入、保留和排除结果的数量核验，记录状态为 PASS。

---

## 六、Step 7：将净电荷范围收窄至 −1.1634 至 +1.0

**目录：**

`results/proteinmpnn/test_2000seq_renumbered/screening_step7_charge_range_semaglutide_to_plus1_v1/`

**输入文件：**

Step 6 保留的 330 条序列。

**筛选规则：**

`-1.1634 <= net_charge_pH7.4 <= +1.0`

上下边界均包含在保留范围内。

### 6.1 设计依据

本轮采用了比 Step 6 更窄的电荷范围，目的是优先保留估算净电荷接近中性的候选序列。

这一选择参考了参考肽的计算结果，以及项目关于长效循环多肽的初步设计假设。其出发点是减少过高正电荷或偏离预设电荷区间的候选物，而不是声称净电荷是决定体内半衰期的唯一因素。

特别需要注意：

- 净电荷与非特异性相互作用之间的关系取决于具体分子，不能简单推广为“某个电荷范围一定具有最长半衰期”。
- 本轮下界 −1.1634 是根据参考肽 Semaglutide 的计算净电荷近似设定的操作性边界。
- 由于计算表中的电荷值采用有限小数位记录，筛选使用的是 CSV 中现有的数值，并非重新计算的无限精度值。

### 6.2 结果

| 指标 | 数量 |
|---|---:|
| 输入 | 330 |
| 保留 | 256 |
| 排除 | 74 |
| 保留率 | 77.58% |
| 排除率 | 22.42% |

74 条被排除序列中：

- 12 条低于下界；
- 62 条高于上界。

输入净电荷范围为 −1.164360 至 +1.836278。

低于下界的序列净电荷范围为 −1.164360 至 −1.163698；高于上界的序列净电荷范围为 +1.834522 至 +1.836278。

本轮结果经过数量核验，记录状态为 PASS。

**输入文件 SHA-256：**

`2990f75e207d333a8975cceed4229c18dee0b1625815049fb50be3d56089160d`

**性质表 SHA-256：**

`009c838ada398a59ff894782f29223293db6a5eb487094cdf7df93dd2f227be7`

**结果文件：**

- `run_screening.py`
- `retained.fasta`
- `rejected.fasta`
- `screening_audit.csv`
- `SUMMARY.md`

---

## 七、Step 8：使用 GRAVY（Kyte–Doolittle）筛选平均疏水性

**目录：**

`results/proteinmpnn/test_2000seq_renumbered/screening_step8_gravy_kd_ge_minus1_1_v1/`

**输入文件：**

Step 7 保留的 256 条序列。

**筛选规则：**

`GRAVY_KD >= -1.1`

即排除 GRAVY 小于 −1.1 的候选，保留达到或高于该边界的序列。

### 7.1 原理与阈值解释

GRAVY 是序列各残基疏水性数值的平均值。按照 Kyte–Doolittle 标度，负值总体表示序列的平均疏水性偏低，正值则表示平均疏水性偏高。

平均疏水性可用于描述序列的整体特征，但它不能单独预测实际溶解度或聚集倾向，因为这些性质还受到局部疏水斑块、三维结构、残基暴露程度及溶剂条件影响。

项目讨论中曾提出更窄的候选偏好范围，例如 GRAVY −0.4 至 0.0，并提出将低于 −0.6 的序列作为需要重点审查的区域。这些范围属于尚待验证的设计假设。

**本轮实际采用的阈值是 GRAVY ≥ −1.1，而不是 −0.6。** 因此，本轮应理解为较宽松的理化性质预筛，而不是已经完成严格的“最佳疏水性窗口”筛选。采用较宽松的阈值可以避免在缺乏本项目验证数据时过早排除较亲水的候选。

另外，GRAVY 只统计氨基酸序列本身，不包括司美格鲁肽所带的脂肪酸侧链修饰。

### 7.2 结果

| 指标 | 数量或范围 |
|---|---:|
| 输入 | 256 |
| 保留 | 240 |
| 排除 | 16 |
| 保留率 | 93.75% |
| 排除率 | 6.25% |
| 输入 GRAVY 范围 | −1.140000 至 −0.460000 |
| 被排除序列的 GRAVY 范围 | −1.140000 至 −1.106667 |

本轮结果经过数量核验，记录状态为 PASS。

**输入文件 SHA-256：**

`46cdf744d12202c9c1c29558c05b71581566fc629ffc8bf70679540449d04c0c`

**性质表 SHA-256：**

`009c838ada398a59ff894782f29223293db6a5eb487094cdf7df93dd2f227be7`

**结果文件：**

- `run_screening.py`
- `retained.fasta`
- `rejected.fasta`
- `screening_audit.csv`
- `SUMMARY.md`

---

## 八、目前的候选集状态

### 8.1 当前候选集

**最终保留数量：240 条序列。**

当前候选 FASTA：

`results/proteinmpnn/test_2000seq_renumbered/screening_step8_gravy_kd_ge_minus1_1_v1/retained.fasta`

目前可以确认：

- 候选集来自前述逐轮筛选；
- 候选序列长度均为 30 aa；
- 当前筛选已纳入序列约束、估算净电荷和 GRAVY；
- 各轮均保留独立的输出目录、保留与排除 FASTA、审计 CSV 和摘要记录。

因此，这 240 条序列是**通过当前规则筛选的候选集合**，不是 240 条已经被证明具有活性或优于司美格鲁肽的分子。

### 8.2 筛选数量变化

从 1,435 条唯一序列开始，依次保留：

`1,435 → 787 → 426 → 425 → 381 → 347 → 330 → 256 → 240`

这一变化体现了从初始序列规则约束到全局理化性质初筛的逐步缩小过程。

前五轮主要执行序列位置与残基规则；第六至第八轮则根据预先计算的净电荷和平均疏水性进一步筛选。

---

## 九、对原始筛选依据的补充说明

项目讨论中提出了以下几类设计考虑：

### 9.1 潜在蛋白酶切割位点

已有研究和原始材料提示，NEP（中性内肽酶，也称 neprilysin）可在 GLP-1 相关肽段的多个位置发生切割。材料特别提及了中端和 C 端附近的潜在切割区域。

这为在序列设计中关注潜在蛋白酶切割位点提供了依据。但正式记录中需要区分：

1. 文献报道的天然 GLP-1 或相关参考肽切割位点；
2. 本项目实际执行的序列排除规则；
3. 某条新设计序列是否确实更耐蛋白酶降解。

前两者可以为设计提供假设，第三者仍需要针对候选序列进行预测或实验验证。当前 Step 1–5 的具体规则应以各自脚本为准，不应仅凭原始文献中提到的切割位置推断所有规则的实现细节。

### 9.2 净电荷

本项目先使用 `abs(net_charge_pH7.4) <= 2` 进行宽范围筛选，再采用 `−1.1634 至 +1.0` 的窄范围进行第二次筛选。

这样的两阶段做法体现了先去除偏离范围较大的序列，再围绕参考肽进一步收窄候选集的策略。

但应避免将“−1 至 +1 是所有长效裸肽的最优电荷区间”写成已经确立的科学定律。电荷对溶解性、分布和清除的影响具有分子与环境依赖性；当前阈值应视为项目使用的初筛假设。

### 9.3 平均疏水性与局部疏水斑块

本轮使用 GRAVY（Kyte–Doolittle）作为全局平均疏水性指标。后续如果需要更深入评估，可考虑另外分析：

- 局部连续疏水残基的分布；
- 疏水残基是否集中在短片段；
- 结构预测后疏水残基的溶剂可及性；
- 与候选序列整体构象和聚集倾向有关的其他指标。

这些分析应作为新的、可独立复现的步骤，不能在没有计算结果时声称已经完成。

### 9.4 SAP、结构评估与分子动力学

原始设计思路还提到了 SAP（self-assembly propensity）、结构指标和分子动力学模拟。

目前已经完成的候选序列分析主要是净电荷与 GRAVY。SAP 需要明确的计算方法及相关结构或溶剂暴露信息；AlphaFold2/其他结构模型的界面指标需要实际结构预测结果；MD 与 MM/GBSA 则涉及更高的计算成本和模型假设。

因此，这些内容属于后续可考虑的评估方向，**不能记为本阶段已经完成的筛选结果**。

同样，结构置信度指标、预测界面质量和结合自由能估算均不等同于实验证明的受体激动活性。

---

## 十、当前工作的局限与后续计划

### 10.1 当前局限

1. **序列数量差异待核对：** 初始说明中的 1,443 条与实际筛选输入的 1,435 条不一致。
2. **阈值尚未校准：** 当前净电荷和 GRAVY 阈值用于规则筛选，尚无本项目实验数据证明其最优性。
3. **缺少完整的结构证据链：** 通过序列和理化性质筛选，不代表候选序列能够以预期构象结合 GLP-1R。
4. **缺少功能验证：** 当前结果不证明受体结合、激动活性、选择性、稳定性或体内半衰期。
5. **尚未完成多样性分析：** 240 条候选是否包含足够的序列多样性，需要通过序列比对、相似性聚类或其他明确的分析方法确认。

### 10.2 建议的下一步

建议在不修改现有筛选结果的前提下，依次开展以下工作：

1. **核对初始数据来源：** 确认 1,443 与 1,435 的差异，明确当前工作流的正式输入版本。
2. **检查 240 条序列的组成与多样性：** 统计各位置氨基酸频率、整体氨基酸组成及序列相似性，避免候选集被少数相近序列过度占据。
3. **与参考肽进行统一口径比较：** 对 Semaglutide、D13、D41、D44 和 240 条候选使用相同计算方法，报告结果与差异，而不是预先假设某一范围一定更优。
4. **评估局部疏水性：** 将全局 GRAVY 与局部疏水斑块分析区分开来。
5. **开展结构层面评估：** 在明确受体结构、肽段构象及预测方法的前提下，评估候选与 GLP-1R 的结构兼容性。
6. **设计可解释的对照：** 后续若开展结构指标或功能相关评估，应尽可能使用已知参考肽、适当阴性对照及一致的计算条件。
7. **保留每一步审计记录：** 每轮新筛选均使用新的版本化目录，并保存规则、输入文件、输出文件、数量统计和必要的文件哈希。

### 10.3 本阶段结论

本阶段已将初始的 1,435 条唯一候选序列，经过五轮序列约束筛选以及三轮理化性质筛选，逐步缩小至 **240 条 30 aa 候选序列**。

本阶段最重要的产出不是证明这些序列具有药理活性，而是建立了一条可追溯的筛选路径：每一轮都有明确的输入集合、规则、保留数量、排除数量和结果文件。

后续工作的重点应从继续叠加未经验证的阈值，转向候选多样性分析、统一口径的参考肽比较，以及逐步引入结构和实验相关证据。

**当前状态：Step 8 完成；240 条候选序列进入下一阶段分析。**

---

# chatgpt response

收到。这份记录我会作为 **2026-10-20：GLP-1RA 候选序列规则筛选与理化性质初筛** 的独立阶段记录保留。

我会特别注意以下几项，避免后续整合时把不同版本或不同工作路径混为一谈。

1. **保留两套实际记录，不强行统一数量。** 1,435 条是此前实际使用的去重 FASTA 数量；1,443 条来自另一份初始项目说明。目前差异尚未解决。
2. **准确记录本阶段的筛选路径。** 本记录的候选数量变化为 `1,435 → 787 → 426 → 425 → 381 → 347 → 330 → 256 → 240`。各轮规则及输出应与对应目录、脚本和审计文件关联。
3. **区分不同版本的筛选流程。** 前一份记录中的第二轮筛选结果为 308 条，并进一步聚类为 65 条代表序列；本份记录则是另一条八步筛选路径，最终得到 240 条。不能将 308、65 和 240 当作同一轮流程的连续结果，也不能在未核实前认定它们使用完全相同的输入和规则。
4. **保留阈值的真实性质。** 净电荷范围和 GRAVY 阈值是本项目采用的操作性筛选规则，尚未通过本项目实验校准；SAP、结构评价及分子动力学也不能记为本阶段已完成的工作。
5. **保留可追溯性问题。** 1,443 与 1,435 的数量差异、原始 ProteinMPNN 参数、DV 位点处理依据，以及部分筛选规则的脚本核实情况，都应进入最终文档的待核查事项。

这份记录的核心贡献，是建立了从序列约束到理化性质初筛的分阶段筛选路径，并保留每一步的候选数量、规则与审计信息。

我会继续等待你发送剩余材料。你明确表示全部发送完毕、可以开始后，我再统一编写 Stage 12 工作记录及完整项目总结。

---

# you asked

message time: 2026-10-23 13:14:32

# GLP1R_reproduction 工作记录
## 从候选序列筛选、去重到 ColabFold 调试与 Boltz 后续评估

**项目目录：** `~/projects/GLP1R_reproduction`  
**远程环境：** HPC，Conda 环境 `(colabfold)`  
**ColabFold 版本：** 1.6.3  
**当前阶段：** 候选池整理与审计已完成；已比较两种预测路线并最终选择方案 B；正在推进 ColabFold 平台调试、预测输入准备与参考模板接入验证。

---

## 一、项目阶段目标与整体工作顺序

本阶段的工作从候选序列筛选结束后开始，目标是将候选序列整理为可复现的计算输入，确定后续结构预测流程，并为候选聚类、Boltz 分析和综合结构评价做好准备。

本阶段涉及四类工作：

1. **候选池整理：** 处理 ProteinMPNN 输出、D13/D41/D44 的合并及两阶段去重，形成统一的候选 FASTA。
2. **预测路线设计：** 比较先聚类再进行结构预测与先 ColabFold 再聚类、最后 Boltz 两种路线。
3. **ColabFold 准备与调试：** 检查运行环境、命令参数、输入文件和自定义模板接入机制，开展必要的测试与试错。
4. **后续分析准备：** 为聚类、Boltz 预测或评估、候选综合排序建立可追溯的输入和结果记录。

需要严格区分以下状态：

- 讨论过某项技术方案；
- 已确定采用某项技术方案；
- 已完成输入和环境准备；
- 某个局部功能测试成功；
- 正式批量预测已启动；
- 正式批量预测已完成；
- 预测结果已经分析并用于候选筛选。

本项目最终确定采用方案 B，即：

**候选序列池 → ColabFold 初步结构预测 → 候选聚类与筛选 → Boltz 后续预测或评估 → 综合结构评价与候选排序。**

因此，后续 ColabFold 平台上的参数检查、模板准备和试错都属于方案 B 的实施过程。它们并不意味着正式批量预测已经完成，正式运行状态仍应以实际日志和输出文件为准。

---

## 二、候选池整理与两阶段去重

### 2.1 ProteinMPNN 原始候选序列

前期 ProteinMPNN 生成的候选序列统一为 30 aa。

在后续候选池整理过程中，又纳入了 D13、D41、D44 三条候选序列。这三条序列均为 31 aa，末尾比原有 30 aa 序列多一个 G。

因此，合并候选时存在一个需要处理的问题：如果直接对原始序列进行完全字符串比较，30 aa 序列和末尾多一个 G 的 31 aa 序列不会被识别为完全相同。

这一问题导致第一次去重未能发现后来确认的部分重复关系，随后需要进行序列标准化并重新去重。

### 2.2 第一次去重：原始长度不一致导致漏检

第一次去重是在原始 30 aa 候选序列基础上进行的。

当时，D13、D41、D44 均为 31 aa，末尾多一个 G。由于序列长度和末端形式不同，第一次去重没有发现 D13、D44 与原有候选之间的重复关系。

这一步的局限在于，比较之前没有统一序列长度和末端处理方式。

因此，第一次去重结果不能作为最终的唯一性判断，需要通过第二次标准化后的比较进行修正。

### 2.3 第二次去重：统一末端 G 后重新比较

第二次去重前，对所有 30 aa 序列统一追加末端 G，将其标准化为 31 aa，再重新比较。

已确认的重复关系如下：

| 候选序列 | 匹配到的原有候选 ID | 处理结果 |
|---|---|---|
| D13 | `unique_0945` | 与已有候选重复 |
| D44 | `unique_0989` | 与已有候选重复 |
| D41 | 未找到匹配 | 作为独立候选保留 |

对应序列如下。

**D13**

`HAEGTFTSDVSSYLEEQAAKAFVERLKRGRG`

匹配已有候选 `unique_0945`，因此不应作为一条新的唯一序列重复计入最终候选池。

**D44**

`HAEGTFTSDVSRYLEEKAVKDFVERLKRGAG`

匹配已有候选 `unique_0989`，因此不应作为一条新的唯一序列重复计入最终候选池。

**D41**

`HAEGTFTSDVSSYLEEQQVKQFVERLKRGRG`

没有找到匹配的已有候选，作为独立候选保留。

由此，第二次去重修正了第一次去重因长度不一致导致的漏检问题：D13 和 D44 分别与已有候选重复，D41 则保留为独立候选。

需要注意，统一追加末端 G 是为了本次去重比较而进行的序列标准化。它不应被误写成所有序列在最初生成时就具有相同的末端状态。为了保持可复现性，应尽可能保留原始序列、标准化后的序列以及两者之间的对应关系。

### 2.4 最终候选 FASTA 审计

当前正式候选输入文件为：

`input/combined_pool.fasta`

已有审计结果如下：

| 检查项目 | 结果 |
|---|---|
| FASTA 序列数量 | 241 |
| 唯一序列数量 | 241 |
| 序列长度 | 全部为 31 aa |
| 非法序列 | 0 |
| 重复序列 | 0 |
| 审计结论 | 通过 |

SHA256：

`7a3ed3e906700768f049d93085d32f69b635f309e3769c8991e8180cca08b7a3`

该文件是后续 ColabFold 初步预测所使用的候选序列输入基准。

当前项目还包含以下辅助文件：

- `input/sequence_manifest.csv`
- `input/SHA256SUMS.txt`
- `input/SUMMARY.md`
- `input/TRANSFER_README.md`

这些文件用于辅助追踪候选序列、文件校验信息及数据交接情况。

后续如果修改候选 FASTA，应同步更新对应的清单和校验信息，避免输入文件与审计记录不一致。

### 2.5 semaglutide 与候选池的边界

semaglutide 是 GLP1R 的已知配体，在本项目中用于受体—配体参考结构的准备与分析。

它不是 D13、D41、D44 这类待筛选候选，也不属于 `input/combined_pool.fasta` 中的 241 条候选序列。

因此，项目数据应明确区分：

- **候选序列池：** 241 条经过审计的唯一候选序列。
- **已知配体与结构参考：** semaglutide，用于 GLP1R 参考结构准备和相关分析。

不能将 semaglutide 当作候选池新增序列，也不能将它的参考结构与候选预测结果混为一类。

---

## 三、两种预测路线的比较

候选池整理完成后，讨论过两种后续计算流程。两者的核心区别是：**候选聚类发生在初步结构预测之前，还是发生在 ColabFold 初步预测之后。**

方案 A 和方案 B 都有明确的流程逻辑，但计算顺序、资源投入及候选筛选时所能使用的信息不同。

### 3.1 方案 A：先聚类，再进行 Boltz 与 ColabFold 预测

流程：

**候选序列池 → 序列聚类 → 选择代表序列或候选 → Boltz + ColabFold 预测 → 结构评价与候选排序**

方案 A 的基本思路是，在进行大规模结构预测之前，先整理候选之间的序列相似性，识别高度相似的候选，并根据聚类结果选择需要进入后续计算的对象。

具体步骤如下。

**第一步：候选序列聚类**

对经过审计的候选序列进行聚类，识别序列之间的相似性关系。

此处应明确采用的聚类工具、相似性定义、阈值和序列覆盖要求。不能只写“完成聚类”，而不记录实际使用的方法。

**第二步：选择代表序列或保留候选**

根据聚类结果，决定每个簇保留哪些序列。

如果每个簇只选择一个代表序列，计算量可能显著下降，但也可能过早排除具有独特结合模式或其他潜在价值的候选。

因此，代表序列选择标准会直接影响后续能够分析到的候选范围。

**第三步：开展 Boltz 与 ColabFold 结构预测**

对聚类后保留的候选开展结构预测。

在正式实施时，应明确两种模型的具体分工、输入形式、运行参数，以及哪些候选需要由两种工具分别预测。

**第四步：综合结构评价与排序**

结合预测结构、界面特征及其他预先确定的评价指标，对候选进行排序。

评价结果应被理解为计算筛选证据，而不是直接等同于实验亲和力或真实结合能力。

#### 方案 A 的优势

- 在初步结构预测之前减少高度相似候选的冗余。
- 有机会降低需要进行结构预测的候选数量。
- 适合优先控制计算规模、集中计算资源的场景。
- 先获得候选的序列分组结果，可以帮助整理后续计算任务。

#### 方案 A 的局限

- 聚类发生在结构预测之前，无法利用候选的初步预测结构辅助决定保留哪些候选。
- 如果每个簇只保留少数代表序列，可能丢失同一簇内其他具有潜在价值的候选。
- 序列相似并不必然意味着结合构象、界面相互作用或真实亲和力相同。
- 如果聚类阈值或代表序列选择标准不合适，早期筛选可能对后续结果造成系统性影响。
- 如果没有明确记录聚类算法与阈值，后续很难复现候选保留过程。

#### 方案 A 适合解决的问题

方案 A 更侧重于：

**如何在昂贵的结构预测开始之前，先减少序列层面的冗余，降低后续计算量？**

它可以作为一种合理的候选池缩减策略，但不意味着聚类代表一定比同簇其他序列更有结合潜力。

---

### 3.2 方案 B：先 ColabFold，再聚类，最后 Boltz

流程：

**候选序列池 → ColabFold 初步结构预测 → 候选聚类与筛选 → Boltz 后续预测或评估 → 综合结构评价与候选排序**

方案 B 是本项目最终确定采用的流程。

它的基本思路是先为候选池生成初步结构信息，再利用聚类及后续筛选决定哪些候选进入 Boltz 阶段。

**第一步：对候选池开展 ColabFold 初步结构预测**

使用经过审计的 `input/combined_pool.fasta` 作为输入，为候选生成初步结构预测结果。

该阶段需要处理：

- ColabFold 环境与版本确认；
- 正式预测命令及参数设置；
- 候选 FASTA 的输入格式；
- 运行过程中的错误与失败任务；
- 输出文件是否完整；
- 自定义模板是否能够按预期接入；
- 预测结果与原始候选 ID 的对应关系。

这一阶段会产生较大的前期计算需求，但可以先获取候选的初步结构信息。

需要特别强调：ColabFold 的初步结构预测并不意味着每条候选都已经成功完成预测。应通过实际运行日志、输出目录和结果文件确认成功状态。

**第二步：基于明确的依据进行候选聚类**

在获得 ColabFold 初步预测结果后，对候选进行聚类和整理。

聚类可以采用序列相似性，也可以在具备合适的结构比较方法时考虑预测结构的相似性，但两种方式应当区分。

- 如果按序列相似性分组，应记录序列聚类方法及阈值。
- 如果按结构相似性分组，应记录结构比对方法、比较对象和相似性指标。
- 如果只对部分预测成功的候选进行聚类，应明确失败或缺失结构的候选如何处理。

随后，根据聚类结果和预先确定的筛选规则，决定哪些候选进入 Boltz 阶段。

**第三步：对筛选后的候选开展 Boltz 后续预测或评估**

对聚类后保留的候选开展 Boltz 分析。

这一阶段应明确：

- Boltz 的具体任务与输入形式；
- 是否使用 ColabFold 预测结果辅助后续筛选；
- 实际使用的预测参数；
- 哪些候选成功完成预测；
- 输出结构和评价指标如何保存；
- 如何保证候选 ID 与结果文件一一对应。

不能仅凭使用了两种结构预测工具，就默认两者的输出可以直接比较。比较时应记录相应的输入条件和指标定义。

**第四步：综合结构评价与候选排序**

整合 ColabFold、聚类及 Boltz 的结果，对候选进行综合评价。

可以根据实际计算情况，考虑结构置信度、界面几何、接触情况、界面面积等指标，但应只报告真正计算并核验过的指标。

模型评分用于帮助筛选候选，并不直接证明候选具有实验结合能力。对于后续需要实验验证的结论，应保留相应的不确定性。

#### 方案 B 的优势

- 在候选聚类之前先获得初步结构信息。
- 不需要在结构预测之前就仅凭序列相似性排除候选。
- 可以在聚类和后续筛选时综合考虑序列信息及已获得的初步预测结果。
- 将较大规模的初步预测与后续较集中的 Boltz 阶段分开，有助于组织计算资源。
- 有利于建立从候选池、初步结构、聚类结果到后续评估的可追溯流程。

#### 方案 B 的局限

- 前期需要对候选池开展较大规模的 ColabFold 预测，计算量高于先聚类再预测的策略。
- 候选数量较多时，需要处理运行时间、任务管理、预测失败和输出整理等工程问题。
- ColabFold 的初步预测可能存在误差，不能把预测结果当作真实结合结构。
- 如果后续聚类使用预测结构，结构预测质量可能影响聚类结果。
- 如果模板接入、运行参数或输入设置存在问题，可能影响预测结果的可解释性与可复现性。
- 必须保留未成功预测的候选及其失败记录，避免只分析成功输出而忽略潜在的系统性偏差。

#### 方案 B 适合解决的问题

方案 B 更侧重于：

**如何先获得候选的初步结构信息，再结合聚类和后续模型分析，逐步缩小需要重点研究的候选范围？**

该流程更符合本项目已经确定的工作顺序，因此后续 ColabFold 平台上的调试和试错围绕方案 B 展开。

---

### 3.3 方案 A 与方案 B 的完整对照

| 比较维度 | 方案 A：先聚类，再 Boltz + ColabFold | 方案 B：先 ColabFold，再聚类，最后 Boltz |
|---|---|---|
| 第一项主要计算任务 | 候选序列聚类 | ColabFold 初步结构预测 |
| 聚类时间 | 结构预测之前 | ColabFold 初步预测之后 |
| 聚类前是否有预测结构 | 没有 | 有机会获得 ColabFold 初步结构 |
| 初步预测对象 | 聚类后保留的候选 | 初始候选池中的候选 |
| 前期计算量 | 相对较小 | 相对较大 |
| 候选池缩减时可利用的信息 | 主要是序列相似性及其他已有信息 | 序列信息及已获得的初步预测结果 |
| 主要资源优势 | 有机会减少结构预测数量 | 将较大规模的初步预测与后续筛选分阶段进行 |
| 主要风险 | 过早排除潜在有价值的候选 | 前期计算量较大，初步预测误差可能影响后续筛选 |
| Boltz 的位置 | 聚类后与 ColabFold 一起用于后续预测 | ColabFold 初步预测和聚类之后 |
| 对 ColabFold 调试的依赖 | 仅需准备聚类后候选的预测环境 | 需要先解决初步预测所涉及的环境、命令、输入和模板问题 |
| 适用的核心思路 | 先减少序列冗余，再投入预测计算 | 先获得初步结构信息，再聚类和进一步筛选 |
| 本项目最终选择 | 未采用 | **已采用** |

### 3.4 最终选择方案 B 的原因与后续工作衔接

本项目最终采用方案 B。

这一选择决定了工作顺序：候选池完成去重和审计之后，先推进 ColabFold 初步预测准备，再开展候选聚类和后续 Boltz 分析。

因此，后续在 HPC 平台上进行的 ColabFold 命令检查、输入文件整理、模板路径测试及相关试错，均应放在方案 B 的实施记录下。

这些工作不是与候选设计无关的独立环境操作，而是为了确保初步结构预测阶段能够得到可复现、可追溯的结果。

同时，方案 B 并不要求把 ColabFold 分数直接当作最终判决。它的意义在于先获得初步结构信息，再通过聚类和后续评价逐步筛选候选。

**最终流程：**

1. 以 241 条唯一候选序列作为输入基准。
2. 开展 ColabFold 初步结构预测，并记录预测成功、失败和缺失情况。
3. 根据明确的聚类方法整理候选。
4. 根据记录完整的筛选标准确定进入 Boltz 阶段的候选。
5. 开展 Boltz 后续预测或评估。
6. 整合结构和界面相关指标，对候选进行综合评价与排序。

---

## 四、semaglutide 与 GLP1R 参考结构准备

### 4.1 semaglutide 的角色

semaglutide 是 GLP1R 的已知配体，在本项目中作为受体—配体参考结构准备工作的一部分。

它与待筛选的 241 条候选序列具有不同的角色：

- 241 条候选序列是待预测和筛选的对象。
- semaglutide 是已知配体，用于参考结构整理及相关分析。

因此，semaglutide 不属于候选 FASTA，也不应计入候选池的序列数量。

### 4.2 原始结构文件与参考结构文件

已知原始 CIF：

`input/templates/7KI0.cif`

文件大小约为 994,709 bytes。

该文件应保留为原始结构输入，不直接覆盖或修改。

另外，已生成参考结构文件：

`input/templates/GLP1R_semaglutide_reference.cif`

文件大小约为 269,460 bytes。

该文件包含 GLP1R 受体 R 链与 semaglutide 肽 P 链。此前的 BioPython 检查显示，该文件可以重新读取。

需要注意，文件中出现受体链和配体链，并不意味着所有理论残基都具有完整的实验坐标。semaglutide 中存在非标准残基 AIB，且结构坐标覆盖范围不一定与完整理论序列一致。

因此，后续使用该结构时，应区分：

- 理论上的完整配体序列；
- CIF 文件中实际存在的残基；
- 非标准残基的表示方式；
- 模型能够识别并实际使用的模板特征。

### 4.3 双链参考结构的使用限制

本项目采用将 GLP1R 与 semaglutide 放在同一个参考 CIF 文件中的整理方式。

但必须明确：**把两条链放进同一个 CIF，不代表 ColabFold 一定会将两条链作为完整复合物模板共同使用。**

实际使用效果取决于 ColabFold 的模板搜索、模板特征生成、链匹配和结构处理过程。

因此，参考 CIF 的存在只证明结构文件已经整理出来。是否能作为预期的双链模板使用，仍需通过具体的模型输入和输出进行验证。

本项目也不以强制固定 receptor–peptide 相对姿态作为当前参考结构整理的默认要求。参考结构的准备与模板系统实际采用该结构，是两个不同的问题。

---

## 五、ColabFold 环境与自定义模板机制检查

### 5.1 当前运行环境

远程工作目录：

`~/projects/GLP1R_reproduction`

当前环境信息：

- Conda 环境：`colabfold`
- ColabFold 版本：1.6.3
- 当前 shell 提示符曾显示在 `sylogin2` 上工作。

已完成 ColabFold 版本及部分命令参数的检查。

正式预测命令应以实际保存的运行记录为准，不能仅凭命令帮助或历史搜索结果还原出未被记录的参数。

### 5.2 自定义模板相关参数

在 `colabfold_batch --help` 中确认了以下参数：

- `--templates`
- `--custom-template-path`
- `--custom-template-cache-path`

其中：

`--custom-template-path` 接受的是模板目录，而不是单独一个 CIF 文件，并且需要配合 `--templates` 使用。

`--custom-template-cache-path` 用于生成临时 HHsearch 数据库相关缓存。

因此，不能仅将一个 CIF 文件的路径直接填入 `--custom-template-path`，就认为模型已经使用该结构。

还需要确认模板目录的组织方式、搜索数据库的生成过程以及模型是否实际检索并采用了目标模板。

### 5.3 对 ColabFold 模板调用过程的检查

此前检查过 ColabFold 的 `colabfold.batch.mk_template()` 相关实现。

该函数使用 `HhsearchHitFeaturizer`，并通过 HHsearch 对指定模板数据库进行搜索，相关调用中包含：

`HHSearch(binary_path=_tool_path("hhsearch"), databases=[f"{template_path}/pdb70"])`

之后再解析 HHR 搜索结果，并调用模板特征生成过程。

这一检查说明，自定义模板使用过程不仅涉及 CIF 文件本身，还涉及模板搜索数据库、搜索命中结果和后续特征生成。

因此，**一个 CIF 能被 BioPython 读取，并不代表它一定能够被 ColabFold 搜索到，更不代表它已经成为模型实际使用的模板。**

### 5.4 HHsearch 与数据库检查记录

曾检查过以下命令：

- `hhsearch`
- `hhmake`
- `kalign`

当时通过 `command -v` 检查没有获得可执行文件路径。

同时，`template_test_7KI0/` 目录中发现了：

- `7KI0.cif`
- `7ki0.cif`
- `pdb70_a3m.ffdata`
- `pdb70_a3m.ffindex`
- `pdb70_cs219.ffdata`
- `pdb70_cs219.ffindex`

当时没有发现 `pdb70_hhm`。

这些结果属于当时的环境检查记录，但不能单凭 `command -v` 没有输出，就断言 ColabFold 的所有内部调用都必然无法使用相关工具。

也不能仅凭缺少某个数据库文件，就认定模板使用失败的唯一原因已经找到。

后续排查应以实际运行命令、错误信息和输出文件为依据，避免将猜测写成已确认的故障原因。

### 5.5 P 链局部模板特征测试

此前进行过 P 链局部特征测试，得到：

- `Error`: None
- `positions` 形状：`(31, 37, 3)`
- `mask` 形状：`(31, 37)`
- `template_sequence`：`HXEGTFTSDVSSYLEGQAAKEFIAWLVRGRG`
- `domain`：`7ki0_P`

这一测试说明，相关局部结构数据能够进入特征生成过程，并生成预期形状的局部特征数组。

但这一结果只证明了局部特征生成测试通过，不代表：

- HHsearch 已经在正式预测中成功命中该模板；
- 受体 R 链与肽 P 链已作为完整复合物模板共同使用；
- 241 条候选已经完成正式 ColabFold 预测；
- 预测结果已经通过结构质量或界面评价。

因此，该测试应记录为局部功能验证，而不是正式预测完成的证据。

### 5.6 双链模板与 ColabFold 预测之间仍需确认的问题

当前参考 CIF 中包含受体 R 链和配体 P 链，但 ColabFold 的模板搜索和特征生成机制并不自动保证整个双链复合物会作为一个整体被使用。

后续需要根据实际运行情况确认：

1. 模板目录是否被正确识别。
2. 搜索数据库是否按预期生成或可用。
3. HHsearch 是否实际检索到目标模板。
4. HHR 结果中是否出现预期的模板命中。
5. 模板特征生成过程实际保留了哪些链与残基。
6. 正式预测输出是否能支持预期的模板使用方式。

在没有这些证据之前，应使用“已准备双链参考 CIF”或“正在验证自定义模板接入”的表述，而不应声称双链复合物模板已经被正式预测流程成功采用。

---

## 六、正式 ColabFold 预测的调试与试错记录

### 6.1 调试目标

方案 B 要求先开展 ColabFold 初步结构预测，因此本阶段需要确认的不只是程序能否启动，还包括输入、模板、输出和候选追踪是否正确。

调试工作应围绕以下目标展开：

- 能否使用当前候选 FASTA 作为输入；
- 正式运行命令与参数是否明确；
- 模板选项与模板目录是否正确配置；
- 参考结构是否能进入实际的模板搜索和特征生成流程；
- 预测输出是否完整；
- 候选 ID 能否与结构文件对应；
- 运行失败时能否区分环境问题、输入问题、模板问题与模型预测问题。

### 6.2 已有的命令核查

此前执行过历史命令搜索：

`history | grep -E 'colabfold_batch|combined_pool.fasta' | tail -20`

该搜索没有找到足以确认正式批量预测完整参数的命令，主要找到参数检查、文件整理等相关记录。

因此，目前不能根据已有历史搜索结果，可靠地还原出最终正式批量预测命令的全部参数。

后续应优先保存实际运行的命令及其输出，不应凭记忆拼接出一个看似完整但未经验证的正式命令。

### 6.3 建议采用的调试顺序

为减少不同故障之间的混淆，建议按以下顺序记录每一次测试。

**第一步：检查输入**

- 检查 `input/combined_pool.fasta` 是否存在。
- 核对序列数量、长度和唯一性。
- 确认输入文件 SHA256 与审计记录一致。

**第二步：检查 ColabFold 环境**

- 记录当前 Conda 环境。
- 记录 ColabFold 版本。
- 保存相关命令帮助输出和必要的环境检查结果。

**第三步：先验证基础预测路径**

在开始大规模运行之前，先用小规模输入验证基础预测命令是否可执行，并记录实际输出和错误信息。

**第四步：单独检查模板路径**

在基础输入和命令确认后，再检查自定义模板路径、缓存目录和搜索数据库，避免把输入问题与模板问题混为一谈。

**第五步：检查模板搜索结果**

如果启用了模板功能，应进一步确认模板搜索是否产生预期命中，并检查相关结果文件。

**第六步：检查局部特征与正式输出**

局部特征测试可以帮助确认某一部分处理流程是否成功，但不能替代正式预测结果检查。

**第七步：扩大到候选池预测**

只有在基础运行和必要的模板行为得到验证后，再推进候选池级别的预测，并保留失败任务记录。

### 6.4 当前状态的准确表述

目前已有证据支持：

- 候选 FASTA 已完成审计；
- ColabFold 1.6.3 已确认；
- 参考 CIF 已整理；
- 已检查部分模板参数与内部调用逻辑；
- 已完成一次 P 链局部特征生成测试。

目前仍需以实际运行日志核实：

- 最终正式批量预测命令及其全部参数；
- 241 条候选的正式预测是否已经启动或完成；
- 自定义双链参考 CIF 是否被正式预测流程按预期使用；
- 所有预测结果是否完整；
- 是否已经进入实际聚类阶段；
- 是否已经对筛选后的候选运行 Boltz。

这一表述能够保留已经完成的工作，同时避免把局部测试或命令检查误写成完整预测结果。

---

## 七、当前文件组织与可追溯性

当前已知文件结构包括：

```text
GLP1R_reproduction/
├── input/
│   ├── combined_pool.fasta
│   ├── sequence_manifest.csv
│   ├── SHA256SUMS.txt
│   ├── SUMMARY.md
│   ├── TRANSFER_README.md
│   └── templates/
│       ├── 7KI0.cif
│       └── GLP1R_semaglutide_reference.cif
└── template_test_7KI0/
    ├── 7KI0.cif
    ├── 7ki0.cif
    ├── pdb70_a3m.ffdata
    ├── pdb70_a3m.ffindex
    ├── pdb70_cs219.ffdata
    └── pdb70_cs219.ffindex
```

以上是目前已知文件的概括，并不代表远程项目目录中只有这些文件。

文件组织需要遵循以下原则：

1. 原始参考 CIF 与整理后的参考 CIF 分开保存。
2. 候选 FASTA、序列清单和校验信息保持一致。
3. 候选原始序列与标准化后的序列应保留对应关系。
4. 每次 ColabFold 调试应保存命令、运行条件、日志和输出。
5. 局部测试输出与正式批量预测结果应分开保存。
6. 聚类结果应能追溯到原始候选 ID。
7. Boltz 的输入、输出及候选筛选记录应能与 ColabFold 结果对应。

---

## 八、下一步工作安排

### 8.1 优先完成 ColabFold 初步预测链路

由于最终选择方案 B，下一阶段应优先确保 ColabFold 初步预测路径可复现。

具体工作：

- 固化当前候选 FASTA 和校验值；
- 明确实际正式预测命令与参数；
- 确认基础预测输入及输出组织方式；
- 继续验证自定义模板的接入机制；
- 保存每次试错的完整日志；
- 在扩大预测规模之前确认基本运行路径。

### 8.2 保留并完善模板测试记录

继续区分三个不同层次：

1. 参考 CIF 是否可读取；
2. 模板搜索和特征生成是否成功；
3. 正式预测是否按预期使用模板。

不能以其中一项成功推断其他两项也成功。

### 8.3 开展候选聚类

ColabFold 初步预测取得可用结果后，根据实际选定的方法对候选进行聚类。

需要记录：

- 聚类使用的输入；
- 聚类方法；
- 相似性定义与阈值；
- 各簇包含的候选；
- 筛选与保留规则；
- 进入 Boltz 阶段的候选名单。

### 8.4 开展 Boltz 后续预测或评估

根据聚类和候选筛选结果，组织 Boltz 后续任务。

应保存完整输入、参数、运行日志、输出结构和评价指标，确保不同模型的结果可以被追溯和合理比较。

### 8.5 完成综合候选评价

在 ColabFold、聚类和 Boltz 结果齐备后，再根据实际计算得到的指标进行综合评价。

应避免：

- 把单一结构评分当作真实亲和力；
- 将预测成功等同于候选有效；
- 在没有完整数据时报告未计算的准确率或其他性能指标；
- 将缺少预测结果的候选直接视为无结合能力。

---

## 九、阶段总结

本阶段的关键成果是：将候选池整理为统一且经过审计的 241 条唯一序列，修正 D13、D44 因长度不一致而在第一次去重中漏检的问题，保留独立的 D41，并将 semaglutide 明确区分为 GLP1R 的已知配体及参考结构来源。

在后续计算流程方面，已经明确选择方案 B：

**先 ColabFold 初步结构预测，再聚类筛选，最后开展 Boltz 后续 Boltz 分析。**

方案 A 仍保留在工作记录中，作为已讨论并比较过的备选路线；但它不是本项目最终采用的流程。

围绕方案 B，后续工作已经进入 ColabFold 环境、输入文件、模板参数及局部特征生成等方面的检查与调试。已有的局部测试说明部分结构特征处理可以执行，但正式批量预测和双链模板实际使用情况仍应以进一步的运行证据确认。

接下来的重点是把 ColabFold 初步预测链路整理为可复现的流程，在保留全部调试记录的基础上，逐步完成候选聚类、Boltz 后续分析与综合结构评价。

**本阶段的目标不只是获得结构预测结果，而是建立一条从候选序列、预测输入、模型运行到后续筛选均可追溯、可复查的计算工作流程。**

---

# chatgpt response

收到。这份记录我会作为 **GLP1R_reproduction 阶段：候选池审计、预测路线选择与 ColabFold 模板接入调试** 保留。

我会重点保留以下信息，尤其是后续编写 Stage 12 时容易被混淆的地方：

- **候选池版本：** `input/combined_pool.fasta` 共 241 条唯一的 31 aa 序列，SHA256 为 `7a3ed3e906700768f049d93085d32f69b635f309e3769c8991e8180cca08b7a3`。D13、D44 分别与已有候选重复，D41 保留为独立候选。
- **路线决策：** 已比较方案 A 与方案 B，最终确定采用方案 B：ColabFold 初步预测 → 候选聚类与筛选 → Boltz 后续预测或评估 → 综合评价与排序。
- **参考结构的角色：** `7KI0.cif` 是原始结构输入，`GLP1R_semaglutide_reference.cif` 是整理后的参考结构；semaglutide 属于已知配体与参考体系，不属于 241 条候选。
- **模板调试证据：** 已检查 ColabFold 1.6.3、相关模板参数和部分内部调用逻辑，并完成 P 链局部特征生成测试。但这些证据不能证明双链模板已被正式预测流程按预期使用。
- **预测状态边界：** 目前这份记录本身尚不能证明 241 条候选的正式 ColabFold 批量预测已完成，也不能据此认定聚类和 Boltz 后续分析已完成。后续状态应依据实际日志与输出文件确认。
- **可追溯性要求：** 保留候选 ID、输入文件校验值、运行命令、日志、模板搜索结果、失败任务及后续结构评价之间的对应关系。

另外，我会将这份记录与此前的 240 条候选筛选记录、308 条候选及 65 条代表序列的聚类记录分开管理。它们属于不同的工作记录或候选处理路径，不能在缺乏版本对应证据时直接拼接成一条连续流程。

我会继续等待你发送剩余材料，不提前撰写 Stage 12。等你明确说材料已经发完、可以开始后，我再统一整理完整工作记录和项目总结。

---

# you asked

message time: 2026-10-23 13:14:44

阶段八：GLP1R 项目已有数据整理、远程 ColabFold 预测、最后 40 条候选补算与 HPC 调度排查工作记录

记录日期：2026 年 10 月 20 日

项目名称：GLP1R_reproduction

本阶段主要工作：梳理已有 201 条数据，整理候选序列池，连接远程计算服务器，检查 ColabFold 环境与历史预测批次，准备最后 40 条候选的补算任务，并尝试通过自定义模板配置开展预测。过程中遇到 SSH 连接、软件环境、服务器资源和 Slurm 调度限制等问题。

一、阶段背景与工作目标

本阶段的工作建立在 GLP1R 项目此前积累的预测数据基础上。项目已经有 201 条已有数据，同时还需要将候选序列池与历史预测结果进行对应，明确哪些候选已有结果、哪些候选仍需补算，以及后续如何统一整理预测输出。

本阶段的目标并不是不加区分地重新计算所有候选，而是在尽可能保留已有计算成果的前提下，继续完成缺失候选的结构预测，为后续候选聚类、结构评价和综合排序准备数据。

工作过程中，逐渐形成了几个需要分别处理的问题：

第一，候选输入文件是否完整，候选序列的数量、长度和来源是否明确。

第二，历史批次是否已经产生有效结构，日志记录的进度是否与实际输出文件一致。

第三，远程服务器是否具备可以直接使用的 ColabFold 环境。

第四，补算任务是否真正获得 GPU 资源并开始运行。

第五，如何在不重复计算已有结果的前提下，补齐需要的候选，并将新结果与已有数据统一整合。

需要特别注意，已有数据数量、候选输入数量、已提交任务数量和已成功生成的结构数量是不同的统计口径。本记录会分别描述这些内容，不把候选已准备、任务已提交或日志已有记录直接当作预测完成的证据。

二、已有 201 条数据与候选池整理

进入本阶段前，GLP1R 项目已经积累了 201 条数据。这批数据构成后续继续推进工作的基础，需要尽可能保留，并与后续生成的候选序列及结构预测结果建立对应关系。

在候选输入整理过程中，原始候选池包含 240 条长度为 30 个氨基酸的候选序列。整理时，为这些序列统一追加末端氨基酸 G，使处理后的候选序列长度达到 31 个氨基酸。

随后，将处理后的候选序列与 D13、D41 和 D44 三条参考序列合并，并进行去重。由于参考序列与原始候选之间存在重合，合并后的序列总数不是简单相加得到的 243 条，而是 241 条唯一序列。

这一步形成了统一的候选预测输入池。需要强调，241 条是整理后唯一预测输入序列的数量，而已有的 201 条数据是此前积累的数据规模。二者不能直接视为相同的统计口径，也不能仅凭两个数字就判断其中有多少条已经完成结构预测。

候选池整理后，主要文件包括：

combined_pool.fasta

sequence_manifest.csv

SUMMARY.md

combined_pool.fasta 用于保存合并去重后的预测序列；sequence_manifest.csv 用于保留候选序列与来源信息之间的对应关系；SUMMARY.md 用于记录候选池的组成与整理规则。

这三个文件共同构成了后续远程预测所需的输入材料。

本阶段的数据整理重点是统一输入、减少重复序列，并保留候选来源信息。这样做有助于后续将预测结果对应回原始候选，避免只保留结构文件而丢失候选身份。

三、连接 MIC5GPUs 服务器

为了利用远程 GPU 资源开展 ColabFold 预测，本阶段首先尝试连接名为 MIC5GPUs 的服务器。

最初的连接过程中出现了 SSH 连接问题。部分尝试使用了本地未正确配置的 SSH 别名，导致连接没有按预期建立。随后改用服务器 IP、端口和用户名直接连接。

成功使用的连接命令为：

ssh -p 11122 liuzelin@202.120.6.159

连接成功后，确认远程用户名为 liuzelin，主机名为 MIC5GPUs，初始工作目录为 /home_ext4/liuzelin。

这一步解决了进入远程服务器的问题，但 SSH 登录成功并不代表 ColabFold 已经可以直接运行，也不代表预测任务已经启动。软件环境、GPU 状态、输入文件和计算任务仍需分别检查。

四、MIC5GPUs 的 GPU 与软件环境检查

成功登录 MIC5GPUs 后，首先检查了 GPU 状态。

当时的 nvidia-smi 输出显示，服务器配备了 6 张 RTX 3090 GPU，每张显存为 24 GB。检查时，GPU 0 至 GPU 4 均存在一定显存占用，并运行着其他 Python 进程；GPU 5 显示显存占用为 0 MiB，利用率为 0%。

因此，在当时的检查时刻，GPU 5 看起来相对空闲。不过，这只是当时的状态快照，不能保证之后仍然空闲，也不能仅凭显存占用就确认该 GPU 一定可以稳定运行新的预测任务。

随后检查 ColabFold 是否已经配置在当前服务器环境中。

执行 which colabfold_batch 后，没有得到可执行文件路径。这意味着当前 shell 的 PATH 中没有找到 colabfold_batch，但不能据此直接断言服务器上完全没有安装 ColabFold。

当时检查到服务器上存在多个 Conda 环境，包括 base、bitta、cad、crop、fastpci、interpretabnet、lisa、mol、patch、qllava、ssa_env 和 zzzairway 等。

由于没有立即确认哪个环境包含可用的 ColabFold，后续仍需要进一步检查各环境中的软件包和可执行文件，才能确定实际运行环境。

这一阶段遇到的第一个技术障碍是：服务器能够正常登录，也具备 GPU 硬件，但软件环境并没有立即确认。需要将“服务器可访问”“GPU 存在”“ColabFold 可用”和“预测任务正在运行”分别验证。

五、候选输入文件上传与一致性校验

在完成候选池整理后，将以下三个文件上传到 MIC5GPUs：

combined_pool.fasta

sequence_manifest.csv

SUMMARY.md

远程存放目录为：

/home_ext4/liuzelin/colabfold_jobs/GLP1R_inputs/

上传完成后，对本地文件与远程文件进行了 SHA256 校验。检查结果显示，双方对应文件的 SHA256 值一致，说明上传后的文件内容与本地文件一致。

同时，对远程 FASTA 文件进行了基本检查，确认其中包含 241 条序列，且每条序列长度均为 31 个氨基酸。

这一阶段完成了候选输入文件的上传与一致性检查，降低了因上传中断、文件内容改变或序列整理错误导致后续预测出现问题的风险。

但是，输入文件校验只能证明候选数据已经正确上传，不能证明所有 241 条候选都已经完成结构预测，也不能代替对原有 201 条数据的逐条结果核验。

六、检查历史预测批次与保留已有结果

在继续补算之前，需要先检查已有预测批次和日志，避免重复计算已经完成的候选，并尽可能保留已有成果。

历史记录中提到，检查时保留了 batch_0、batch_1、batch_3、batch_4 和 batch_5 的相关目录及日志。

batch_2 的日志显示，该批次至少已经推进到第 15 条候选，同时存在与重试有关的日志记录。

这说明此前的预测任务并非全部处于完全未运行状态。至少部分批次已经留下了计算记录，batch_2 也曾经推进到一定进度。因此，不能简单地将所有批次视为从未运行，更不能不检查输出就直接重新提交所有候选。

本阶段需要重点区分三种情况：

第一，日志显示任务已经处理，但对应结构文件是否完整、是否可用仍需核验。

第二，结构文件已经存在，但需要确认它对应哪条候选序列，以及是否确实属于当前需要保留的预测结果。

第三，候选确实没有有效输出，或者已有输出不完整，需要进一步补算。

现有历史摘要没有完整保留 batch_0 至 batch_5 每个批次的精确完成数量，也没有给出每个批次有效结构文件的完整清单。因此，不能仅凭批次目录存在就认定该批次内所有候选均已成功预测。

这一阶段的工作原则是先保留已有数据和日志，再依据实际输出判断完成情况，最后只对确实缺失或需要重跑的候选进行补算。

七、SSH 连接中断与服务器环境问题

在检查历史批次和恢复相关信息的过程中，SSH 连接曾出现不稳定情况。

部分连接尝试发生超时，导致远程检查无法一次性完成。随后通过更详细的 SSH 调试输出重新尝试连接，最终确认可以成功认证并进入服务器。

这使得远程检查过程被打断，需要重新建立连接并继续操作。此前一次连接成功，并不意味着之后的连接一定持续稳定，也不能把尚未完成的远程检查当作已经全部完成。

此外，当时的服务器环境还出现了几个值得记录的问题。

首先，/home_ext4 文件系统的使用率达到 99%，仍有约 59 GiB 可用空间。这说明文件系统已经接近满载。尽管仍有剩余空间，但继续开展批量结构预测会产生结构文件和中间文件，因此需要关注存储空间是否足够。

其次，当时的系统负载均值约为 24.30、24.04 和 20.56，说明服务器处于较高负载状态。

另外，有一次 nvidia-smi 检查报告了 GPU0000:3E:00.0 Unknown Error。

这些现象增加了远程任务排查的复杂度，但现有记录不能证明它们就是 batch_2 未完成的直接原因，也不能据此断言所有 GPU 均无法使用。

它们应当作为当时观察到的服务器环境问题记录，而不能直接写成已经确认的故障根因。

八、工作环境与服务器发生变化

在后续工作中，预测任务转移到了另一套远程计算环境，即 DSSG/HPC 服务器。

这一环境与前面连接的 MIC5GPUs 不是同一台服务器，因此不能将两边的 GPU 状态、软件环境、作业状态和文件路径混为一谈。

在 DSSG/HPC 环境中，远程用户为 255433ljl，账户为 acct-agrlzh，当前登录节点为 sylogin4。

本阶段后续的 batch_2 补算与自定义模板作业，均围绕这套 HPC 环境展开。

这一变化也意味着，前面在 MIC5GPUs 上检查到的 RTX 3090、Conda 环境、文件系统使用率和 GPU 错误，不应直接用于解释 DSSG/HPC 上的 Slurm 调度问题。两套环境需要分别记录。

九、最后 40 条候选的补算准备

在已有数据整理和历史批次检查的基础上，后续工作进一步聚焦于需要补算的最后 40 条候选。

当前记录中的补算目录为：

/dssgLOCAL_PATH

本次输入文件为：

inputs/batch_2.fasta

该 FASTA 文件包含 40 条候选记录。输入中的受体链与 binder 链以冒号分隔，便于按照预期的复合物形式提交结构预测。

本次工作重点是为这 40 条候选准备单独的输入和运行配置，并尝试在已有数据基础上完成剩余候选的预测，而不是重新计算整个 241 条候选池。

这里需要保留一个重要区别：最后 40 条候选的补算任务已经进入文件准备和作业提交阶段，并不意味着 40 条结构已经全部生成。

当前能够从历史记录确认的是，batch_2 的输入文件已经准备，相关 Slurm 作业已经提交，但作业曾处于等待资源状态。正式预测是否完成，仍需要根据作业最终状态、日志和输出文件进行核验。

十、ColabFold 自定义模板文件准备

在准备最后 40 条候选的补算时，进一步整理了与 7KI0 相关的模板文件，并配置 ColabFold 的自定义模板路径。

相关模板文件包括：

templates/7ki0.cif

templates/7ki0.pdb

templates/7ki0_chains/7ki0_R.pdb

templates/7ki0_chains/7ki0_P.pdb

templates/colabfold_custom/7ki0_R.pdb

其中，7ki0_R.pdb 是从 7KI0 整理出的受体 R 链模板，并被放置在自定义模板目录中。

本次配置的自定义模板路径为：

templates/colabfold_custom

需要注意，目录中同时存在 R 链和 P 链的整理文件，并不等于它们都已经作为模板被 ColabFold 实际使用。本次记录明确的自定义模板文件是 7ki0_R.pdb，因此不能将此次操作描述成受体链和 semaglutide P 链已经共同作为双链模板参与预测。

同样，模板文件准备完成，只能说明相关输入材料和配置已经整理。是否被 ColabFold 实际识别、是否在预测中成功命中，以及模板对输出结构产生了什么影响，都需要通过运行日志和结果进一步确认。

十一、batch_2.sbatch 脚本与运行参数

为最后 40 条候选准备了批处理脚本：

batch_2.sbatch

脚本使用的 ColabFold 环境为：

~/.conda/envs/colabfold

脚本的语法检查已经通过 bash -n 检查。这说明脚本在 Bash 语法层面没有发现错误，但不能保证作业提交后一定成功执行，也不能保证 ColabFold 参数、输入路径和模板配置都已经在实际运行中得到验证。

本次配置采用的主要预测参数如下：

预测方法：alphafold2_multimer_v3

recycle 次数：3

模型数量：3

seeds：1

random seed：0

启用模板：是

自定义模板路径：templates/colabfold_custom

输出目录：batch_2_template

该配置旨在使用 ColabFold multimer_v3 对 batch_2 中的候选进行预测，并在指定目录中保存结果。

不过，脚本通过语法检查与预测成功是两个不同层面的事情。只有作业真正获得资源、执行 ColabFold，并在日志中显示实际处理过程后，才能进一步判断参数是否被正确读取、模板是否生效以及结构是否生成。

十二、DSSG/HPC 上的 Slurm 作业提交

在准备好输入文件、模板和脚本后，向 Slurm 提交了 batch_2 的补算任务。

对应作业号为：

63867137

作业名称为：

GLP1R_b2_tpl

主要申请参数如下：

分区：a100

账户：acct-agrlzh

QOS：normal

GPU：1 张

CPU：8 核

内存：32 GB

时间限制：2 天

作业日志路径为：

/dssgLOCAL_PATH

错误日志路径为：

/dssgLOCAL_PATH

作业提交后，检查到其状态为 PENDING，阻塞原因显示为 AssocGrpGRES。

对应的 Slurm 记录显示，作业申请了 1 张 GPU、8 核 CPU 和 32 GB 内存，但当时没有分配计算节点，AllocTRES 为空。

这意味着作业已经提交，但尚未获得运行所需的计算资源。此时不能认为 ColabFold 已经开始执行，也不能认为最后 40 条候选已经完成预测。

十三、交互式 GPU 申请与作业状态

在批处理作业等待资源期间，还尝试申请交互式 GPU 资源，以便在获得计算节点后继续开展必要操作。

交互式申请的主要参数为：

分区：a100

GPU：1 张

CPU：8 核

内存：32 GB

时间限制：30 分钟

对应作业号为：

63867807

查询结果显示，该作业同样处于 PENDING 状态，原因也是 AssocGrpGRES。

因此，这次交互式申请也没有获得运行所需的计算资源。没有证据表明该作业已经进入 GPU 节点，或者已经在交互式 shell 中执行 ColabFold。

此前还存在交互式作业 63858229 和 63864496。这些作业已经结束或被取消。

其中，63864496 曾在 gpu10 上处于运行状态，但当时的检查未发现正在执行的 ColabFold 计算。该交互式会话后来已经被取消，不能假设它仍然存在，也不能直接恢复旧会话继续运行。

当前 shell 位于 sylogin4 登录节点。登录节点主要用于文件操作、脚本编辑、作业提交和队列查询，并不等同于已经分配 GPU 的计算节点。

因此，不能仅凭当前登录 shell 能够执行命令，就认定预测任务正在 GPU 节点上运行。

十四、AssocGrpGRES 调度阻塞问题排查

本阶段在 DSSG/HPC 上遇到的一个直接影响补算进度的问题，是批处理作业和交互式 GPU 申请都被 Slurm 标记为 AssocGrpGRES。

这说明作业受到关联层级通用资源组限制的影响，但仅凭该状态无法确定具体是哪一级配额设置导致阻塞，也无法直接得出限制数值。

为进一步排查，执行了以下 association 查询：

sacctmgr show assoc where account=acct-agrlzh format=Account,User,Partition,QOS,GrpTRES,GrpTRESRunMins

查询结果显示，该账户关联的 QOS 包括 debug、normal 和 small，但 GrpTRES 和 GrpTRESRunMins 没有显示具体限制值。

随后又查询了 normal QOS：

sacctmgr show qos normal format=Name,GrpTRES,GrpTRESRunMins,MaxTRESPerJob

返回结果中，GrpTRES、GrpTRESRunMins 和 MaxTRESPerJob 等字段同样没有显示能够直接解释当前问题的具体限制值。

因此，目前只能确认作业受到 AssocGrpGRES 阻塞，尚不能确认具体限制位于用户、账户、父级 association、QOS 层级还是其他资源计数环节。

不能直接断言用户个人 GPU 配额已满，也不能断言账户的 GPU 上限为某个特定数量。

调度器曾通过以下命令提供预计开始时间：

squeue --start -j 63867137

查询结果中曾显示：

2026-10-20T23:33:04

但同一结果仍显示作业处于 PD 状态，节点分配信息为空，阻塞原因仍为 AssocGrpGRES。

这个时间只是调度器当时给出的估计，并不等于已经成功预约计算节点，更不等于 GPU 已经分配。作业仍可能继续等待，预计时间也可能随资源状态变化而更新。

因此，本阶段没有把该预计开始时间记录成实际运行时间。

十五、本阶段遇到的主要挫折

第一，SSH 连接与远程检查并非始终稳定。

在 MIC5GPUs 上，最初的连接方式出现问题，部分 SSH 尝试超时，需要改用明确的服务器 IP、端口和用户名，并通过调试信息重新确认连接状态。远程检查因此被打断，增加了排查和恢复工作的成本。

第二，ColabFold 环境没有在初次检查时直接确认。

登录服务器后，which colabfold_batch 没有找到可执行文件。服务器上存在多个 Conda 环境，需要进一步检查才能确认真正可用的 ColabFold 环境。这意味着连接服务器后不能立即假定预测环境已经准备好。

第三，服务器存储和运行状态存在风险。

MIC5GPUs 当时的 /home_ext4 文件系统使用率达到 99%，系统负载均值较高，并有一次 GPU Unknown Error 记录。这些情况增加了继续开展批量预测时的风险，但不能直接认定它们就是后续所有计算问题的原因。

第四，历史批次的完成情况需要逐项核验。

已有目录和日志不能直接等同于有效预测结果。尤其是 batch_2，日志显示它至少推进到第 15 条候选，并存在重试记录，因此需要进一步区分哪些候选已经产生完整结构，哪些候选需要补算。

第五，最后 40 条候选的补算虽然已经完成输入、脚本和作业提交准备，但 Slurm 资源申请没有顺利进入运行阶段。

在 DSSG/HPC 上，批处理作业 63867137 与交互式作业 63867807 均处于 PENDING，原因是 AssocGrpGRES。即使脚本语法检查通过、输入文件已经准备好，也无法在没有分配计算资源的情况下开始正式预测。

第六，资源限制的具体原因没有查明。

已经查询了账户 association 和 normal QOS，但输出没有显示能够直接解释阻塞的具体限额。因此，需要管理员进一步核查实际生效的父级 association、QOS 设置和当前资源计数，而不能凭经验猜测 GPU 配额。

第七，两套远程计算环境不能混为一谈。

前期的 MIC5GPUs 与后续的 DSSG/HPC 是不同环境。前者涉及 RTX 3090、Conda 环境、文件系统使用率和 GPU 检查；后者涉及 a100 分区、Slurm 作业和 AssocGrpGRES。两边的问题需要分别记录，不能用前一台服务器的状态解释后一台服务器的调度结果。

十六、当前能够确认的阶段成果

截至目前，能够根据现有记录确认的成果如下。

1. 已有 201 条 GLP1R 项目数据作为本阶段的工作基础。

2. 整理了包含 240 条原始候选序列的输入集合，将每条序列统一追加末端 G，并与 D13、D41 和 D44 三条参考序列合并去重，形成 241 条唯一序列的候选池。

3. 生成 combined_pool.fasta、sequence_manifest.csv 和 SUMMARY.md 三个主要输入材料。

4. 将上述文件上传到 MIC5GPUs 的指定目录，并通过 SHA256 校验确认远程文件与本地文件一致。

5. 成功连接 MIC5GPUs，检查了当时的 GPU 使用情况和 Conda 环境，并发现当前 shell 未直接找到 colabfold_batch。

6. 检查了部分历史预测批次，保留了相关目录和日志，并确认 batch_2 曾至少推进到第 15 条候选且存在重试记录。

7. 在 DSSG/HPC 上准备了最后 40 条候选的输入文件 inputs/batch_2.fasta。

8. 整理了 7KI0 相关模板文件，并配置 templates/colabfold_custom 中的 7ki0_R.pdb 作为自定义模板输入。

9. 完成 batch_2.sbatch 脚本的 Bash 语法检查，并设置了 ColabFold multimer_v3、recycle 次数 3、模型数量 3、seeds 1、random seed 0 和自定义模板路径等参数。

10. 提交了补算作业 63867137，并尝试通过交互式作业 63867807 获取 GPU 资源。

11. 发现批处理和交互式申请均受到 AssocGrpGRES 阻塞，并完成了初步的 association 与 QOS 查询，但尚未查明具体限制层级。

十七、尚未确认的事项

以下事项不能因为文件准备或作业提交已经完成，就直接记为成功。

第一，已有的 201 条数据是否已经全部逐条核验，以及每条数据对应的候选、批次和有效结构文件是否完整对应。

第二，241 条唯一候选中，究竟有多少条已经成功生成可用结构，多少条仍缺失或需要重跑。

第三，batch_0 至 batch_5 每个批次的实际成功数量，以及 batch_2 已经产生的有效结构数量。

第四，最后 40 条候选是否已经全部完成 ColabFold 预测。

第五，自定义模板是否在实际 ColabFold 运行中被正确识别并使用。

第六，7KI0 的 R 链模板是否对输出结构产生了预期影响。

第七，Slurm 作业 63867137 是否已经从 PENDING 进入 RUNNING，以及最终是否正常结束。

第八，AssocGrpGRES 的具体限制究竟位于哪一级 association 或 QOS，以及当前资源计数是否达到限制。

这些事项需要通过实际日志、输出文件、Slurm 作业历史和管理员反馈进一步确认。

十八、下一阶段工作安排

首先，继续保留已有预测批次和日志，整理已有 201 条数据与候选清单之间的对应关系。对已有结构文件逐项检查，避免重复计算已经有效完成的候选。

其次，检查最后 40 条候选的 batch_2.fasta，确认输入数量、候选顺序和链分隔符正确，并保留当前的脚本、参数和模板文件。

第三，继续跟踪作业 63867137 的状态：

squeue -j 63867137 -o "%.18i %.12T %.20j %.12M %.20R"

如果作业开始运行，应检查对应的 .out 和 .err 日志，确认 ColabFold 是否真正启动、输入是否被读取，以及自定义模板是否得到处理。

如果队列中已经查不到该作业，应查询作业历史：

sacct -j 63867137 --format=JobID,State,ExitCode,Elapsed

根据最终状态和日志判断作业是否成功结束、是否发生错误，以及是否产生了完整输出。

第四，继续排查 AssocGrpGRES。向管理员提供账户 acct-agrlzh、用户 255433ljl、批处理作业 63867137、交互式申请 63867807，以及已经执行的 association 和 QOS 查询结果，请其核查实际生效的父级 association、GPU 组资源限制和当前资源计数。

第五，只有在获得计算资源并确认任务实际运行后，才能把最后 40 条候选记为补算完成。随后检查实际生成的结构文件数量、文件完整性和候选对应关系。

第六，将确认有效的新结果与已有数据整合，形成统一的预测结果清单，再继续进行候选聚类、Boltz 结构评价和综合排序。

十九、阶段总结

本阶段的核心工作是从已有 201 条数据出发，继续整理 GLP1R 候选序列池，完成 241 条唯一序列的输入准备与远程文件校验，检查历史预测批次，并在后续的 DSSG/HPC 环境中准备最后 40 条候选的 ColabFold 补算任务。

在这一过程中，工作遇到了 SSH 连接不稳定、ColabFold 环境需要进一步确认、服务器存储空间紧张、系统负载较高、GPU 检查出现异常，以及 Slurm 作业受到 AssocGrpGRES 限制等问题。

这些困难说明，结构预测工作不仅需要候选序列和预测脚本，还依赖稳定的远程连接、可用的软件环境、充足的存储空间、可分配的 GPU 资源，以及对历史结果的准确核验。

截至当前记录，候选输入整理、远程文件一致性校验、部分历史批次检查、模板准备、脚本语法检查和 Slurm 作业提交等工作已有明确记录；但最后 40 条候选是否全部完成预测，仍不能仅凭当前记录确认。

因此，本阶段应定位为：已有数据整理与历史结果检查基本推进，最后 40 条候选的补算输入和运行配置已经准备，正式计算仍需以 Slurm 实际运行状态、ColabFold 日志和有效结构输出为依据确认。

后续工作的重点，是先解决计算资源等待问题，再完成缺失候选补算，并将新结果与已有数据建立可靠对应关系，为后续结构评价与候选排序提供可追溯的数据基础。

---

# chatgpt response

收到，阶段八的工作记录已纳入当前项目资料。我会继续等待你发送后续阶段，不提前撰写最终的 Stage 12 工作记录。

这一阶段我会特别保留以下关键事实，避免后续汇总时混淆：

1. **候选池：** 240 条原始 30 aa 序列统一追加末端 G，并与 D13、D41、D44 合并去重，形成 241 条唯一的 31 aa 序列；D13、D44 与已有序列重复，D41 独立保留。
2. **已有数据与补算任务：** 已有 201 条数据，但其与 241 条候选之间的逐条对应关系、有效结构数量及各历史批次的完成情况尚未全部核实。
3. **两套远程环境：** MIC5GPUs 与 DSSG/HPC 分开记录，不能混用它们的 GPU 状态、软件环境和故障信息。
4. **ColabFold 模板：** 已准备 7KI0 相关文件，并配置受体 R 链 `7ki0_R.pdb`；局部文件或配置准备完成，不等于正式预测已经成功使用模板。
5. **最后 40 条补算：** 已准备 `batch_2.fasta`、`batch_2.sbatch` 并提交 Slurm 作业 `63867137`；当时状态为 `PENDING`，原因是 `AssocGrpGRES`。不能据此认定预测已启动或完成。
6. **阶段边界：** 输入校验、脚本语法检查、作业提交与实际结构预测成功，是不同的完成状态，后续需要分别保留。

另外，我会把本阶段记录与此前的 ProteinMPNN、候选池去重、Boltz-2 和 PCANN 工作记录区分开，按实际时间顺序衔接；不会将早期的 30 aa 序列、标准化后的 31 aa 序列，以及后续最终候选混为一谈。

你继续发送即可。等你明确说**材料已经发完、可以开始整理**之后，我再统一梳理并撰写详细版本。

---

# you asked

message time: 2026-10-23 13:14:54

GLP1R reproduction 项目工作记录
阶段九：ColabFold 批量预测、远程计算故障恢复、补算与候选指标整理

记录日期：2026-10-20 至 2026-10-21
项目：GLP1R de novo peptide candidate computational evaluation
工作阶段：ColabFold 初步结构预测与数据整理
当前状态：241 条候选相关记录的 ColabFold 数据已完成收集与整理，进入进一步筛选和聚类阶段。

============================================================
一、本阶段工作概述与个人原始叙述
============================================================

【个人原始叙述，保留】

这一阶段终于结束了，最终结果就是我获得了241条候选序列（包括D13、D41、D44）的完整colabfold数据，尽管与预期有些不符，原定跑3*seed（0、120、240)+model=3+recycle=3,最后由于交我算排队困难，用崩了学长一个远程服务器，本地GPU算力不足，最后只实现了seed=0+model=3+recycle=3，相当于241条序列，每条拿到3个相关数据，其中有201条是在学长提供的服务器卡死之前跑完的，另外40条由于服务器崩坏没能保留，于是在交我算平台尽力构建相同体系相同环境相同条件补上了这40条数据，勉强能够完成统计与分析，接下来就是进一步的筛选与聚类工作。

【本阶段工作总结】

本阶段的主要成果不是单纯完成了一次 ColabFold 批量预测，而是在计算资源不足、远程服务器运行异常、原始任务未能完整执行的情况下，完成了以下工作：

1. 将此前已经整理并审计的 GLP1R 候选序列送入 ColabFold multimer 预测流程。
2. 在学长提供的远程服务器上完成了大部分预测任务，并在服务器异常后确认已完成部分与未完成部分。
3. 针对未能保留的 40 条序列，转向上海交通大学交我算平台，重新准备输入文件、运行环境、模板文件及批处理脚本，尝试在相同体系和尽可能一致的参数下补算。
4. 对补算结果进行检查，整理 rank 结果、PDB 结构、PAE 文件和模型评分 JSON。
5. 针对 ColabFold 未直接输出的部分界面评价指标，进一步检查原始预测文件，并尝试使用 ColabFold 内部实现计算 ipSAE、pDockQ 和 pDockQ2 等指标。
6. 对补算批次的模型记录进行清洗，检查异常模型、缺失模型及每条候选的有效模型数量。
7. 统一链映射、候选编号和输出文件对应关系，为后续候选筛选、结构聚类和综合评价准备数据基础。

最终，原计划中的三个 seed 未能全部完成，但 seed=0 下的 model=3、recycle=3 预测体系得以基本建立，并形成了可用于后续分析的候选结构数据集。

需要明确：本阶段完成的是计算预测与数据整理，不代表 241 条候选均已获得实验验证，也不代表所有候选都具有真实的 GLP1R 结合能力。


============================================================
二、从原定计算方案到实际执行方案
============================================================

2.1 原定计算方案

此前确定的正式 ColabFold 计算方案为：

- 候选规模：241 条序列。
- Seed：0、120、240，共 3 个 seed。
- Model：3 个模型。
- Recycle：3。
- 预测体系：ColabFold AlphaFold2 Multimer v3。
- 目标：为每条候选获得多组预测结果，并提取结构置信度及界面评价指标。

如果三个 seed 均完整执行，每条序列将获得来自不同 seed 的预测结果，每个 seed 下又包含三个模型。

因此，原定方案能够在同一候选上提供更多预测样本，便于观察模型结果的稳定性，降低仅依赖单次预测结果的风险。

但这套方案对 GPU 算力、远程计算资源、运行时间、输出文件存储和任务管理均有较高要求。

2.2 实际方案的变化

受交我算平台排队困难、可用 GPU 资源不足以及学长远程服务器运行异常等因素影响，最终没有完成 seed=0、120、240 三组预测。

实际保留下来的主要数据来自：

- Seed：0。
- Model：3。
- Recycle：3。

这意味着本阶段的数据不能被表述为完整的三 seed 重复预测结果。

虽然每条候选能够对应多个模型输出，但同一个 seed 下的三个模型不等同于三个独立 seed，也不能据此直接声称已经完成了三次独立重复实验。

因此，本阶段数据适合用于初步结构评价、候选排序和聚类，但后续如果要分析跨 seed 的稳定性，仍需要补充相应预测。

2.3 数据规模的口径

本阶段以 241 条候选相关记录作为工作目标，并按每条候选对应三个模型结果的思路整理数据。

这里需要区分三个数量：

第一，候选序列数量：241 条。

第二，理论上的模型结果数量：如果每条序列均完整保留三个模型结果，则为 241 × 3 = 723 条模型结果。

第三，最终实际保留的模型记录数量：应根据各批次的实际输出、清洗结果及模型文件清单确认，不能仅凭理论数量推定。

后续统计时，必须区分候选数、模型记录数、有效模型数和最终用于排序的候选数。

尤其需要避免将三个模型结果简单视为三个独立候选，或者把某个候选的三个模型文件误计为三条不同序列。


============================================================
三、学长远程服务器上的批量预测与故障
============================================================

3.1 远程服务器及任务组织

在本地 GPU 算力不足、交我算平台资源调度不顺利的情况下，借助学长提供的远程服务器执行大批量 ColabFold 任务。

保存的终端记录中，远程主机提示符曾显示为：

    liuzelin@MIC5GPUs

远程 ColabFold 可执行文件路径记录为：

    LOCAL_PATH

远程工作目录涉及：

    LOCAL_PATH

后续用于恢复和补算的本地工作目录为：

    LOCAL_PATH

远程预测任务按 batch 分组执行，相关目录包括：

    batch_0
    batch_1
    batch_2
    batch_3
    batch_4
    batch_5

批次划分的目的是把 241 条输入分成多个较小的任务，方便并行计算、检查运行状态以及在发生故障时定位缺失结果。

从保存的终端记录看，各批次均有独立日志和完成标记文件。通过检查进程、日志末尾的 Query 进度以及候选完成标记，可以判断哪些批次已经结束、哪些批次仍在运行，以及哪些任务出现了停滞。

3.2 运行状态检查

在服务器出现异常后，对六个批次进行了状态检查。

当时的记录显示：

- batch_0：已生成 40 个候选完成标记。
- batch_1：已生成 40 个候选完成标记。
- batch_2：已生成 15 个候选完成标记。
- batch_3：已生成 40 个候选完成标记。
- batch_4：已生成 40 个候选完成标记。
- batch_5：已生成 40 个候选完成标记。

同时，日志中的最后一个 Query 位置显示：

- batch_0：Query 41/41，reference_D41。
- batch_1：Query 40/40，candidate_0236。
- batch_2：Query 16/40，candidate_0093。
- batch_3：Query 40/40，candidate_0238。
- batch_4：Query 40/40，candidate_0239。
- batch_5：Query 40/40，candidate_0240。

这些记录反映了当时不同批次的运行状态，但它们属于某一时点的进度快照，不应单独作为最终数据完整性的证明。

特别是 batch_2，日志和进程信息表明该批次没有按照预期顺利结束。

3.3 进程异常与资源占用

在进一步检查时，使用进程状态、进程树及资源占用信息排查任务是否仍在运行。

当时多个 ColabFold 进程处于 D、R 或 Z 等不同状态，其中部分进程已经持续运行较长时间，且存在较高的内存占用。

通过查看 batch_2 的进程树，可以确认相关 ColabFold 进程及其线程仍然存在。

但是，进程存在并不意味着计算能够正常推进；同样，日志长时间不更新也不能直接证明所有结果都已经损坏。

本阶段的问题在于，服务器上有些任务已经完成，有些任务处于停滞或异常状态，而服务器故障又使得后续输出无法得到可靠保存。

最终，按本阶段实际恢复情况，201 条序列的预测数据在远程服务器故障前已经完成并保留；另有 40 条序列未能保留完整预测结果，需要重新补算。

201 条与 40 条是本阶段数据恢复工作的实际划分口径。对其进行正式归档时，应以最终候选清单、已恢复文件和补算文件之间的 ID 对应关系为准，而不是仅凭当时的进程状态推算。

3.4 故障带来的主要教训

本次远程计算经历说明，大规模蛋白结构预测不仅需要考虑模型运行本身，还需要考虑：

- 服务器是否具有稳定、可持续的计算资源；
- 并行进程是否会造成内存或系统资源竞争；
- 输出文件是否及时写入磁盘；
- 是否为每条候选保留独立的完成标记；
- 是否能够从日志和文件清单恢复任务状态；
- 是否可以在计算中断后只补跑缺失候选，而不必重复运行全部任务。

后续正式批量计算应优先采用可恢复的任务组织方式，并在每批任务完成后及时核对输出文件和候选清单。

本阶段虽然出现了服务器故障，但由于已有部分输出文件、批次目录和完成标记，仍然能够划分已完成与缺失任务，并继续推进补算工作。


============================================================
四、转向交我算平台进行缺失数据补算
============================================================

4.1 补算目标

在学长远程服务器异常后，决定不再将整个候选池重新计算一遍，而是针对缺失的 40 条序列补算。

补算目标是：

1. 保留已经完成且可用的 201 条序列数据。
2. 重新构建缺失的 40 条候选输入。
3. 尽可能复现原有的 ColabFold 预测体系。
4. 使用一致的候选命名规则和输出组织方式。
5. 最终形成能够合并、清洗和统计的统一结果集。

这一策略能够减少重复计算，并把计算资源集中用于恢复缺失的数据。

4.2 交我算平台的登录与任务准备

此前已经在交我算平台开展 ColabFold 环境检查与任务调度排查。

本阶段的补算工作使用了思源一号相关目录，工作路径涉及：

    /dssgLOCAL_PATH

其中，补算输入文件为：

    inputs/batch_2.fasta

模板文件涉及：

    templates/7ki0.cif
    templates/7ki0.pdb
    templates/7ki0_chains/7ki0_R.pdb
    templates/7ki0_chains/7ki0_P.pdb
    templates/colabfold_custom/7ki0_R.pdb

其中，7KI0 是 GLP1R 与 semaglutide 相关的参考结构来源。

此前的准备工作将受体 R 链和肽 P 链分别整理成文件，并尝试按照 ColabFold 自定义模板识别规则组织模板目录。

需要严格区分模板文件准备与模板实际使用：

- 模板文件存在，只能证明输入文件已准备。
- ColabFold 日志报告找到模板，可以证明相应序列在该次运行中发生了模板匹配。
- 这仍不自动证明两条链作为一个完整复合物模板被共同使用，也不证明受体与配体的相对姿态被完整保留。

因此，本阶段不将“自定义模板文件已经准备”与“完整双链复合物模板已成功接入”视为同一结论。

4.3 补算任务参数

补算脚本中记录的主要设置为：

- 分区：a100。
- GPU：1 张。
- CPU：8 核。
- 内存：32 GB。
- 输入：inputs/batch_2.fasta。
- 模板目录：templates/colabfold_custom。
- 模型类型：alphafold2_multimer_v3。
- Recycle：3。
- Models：3。
- Seeds：1。
- Random seed：0。
- 模板选项：--templates。
- 自定义模板路径：--custom-template-path。

这些设置与本阶段最终采用的 seed=0、model=3、recycle=3 方案一致。

批处理脚本中还包含输入文件、模板文件及 ColabFold 可执行文件存在性检查，FASTA 记录数检查，输入文件和模板文件的 SHA256 输出，以及环境版本和 GPU 信息检查。

脚本提交前执行了 shell 语法检查。

这些检查提高了任务的可审计性，但脚本语法通过不代表作业已经开始运行，也不代表预测已经完成。

4.4 HPC 调度障碍

在交我算平台上，曾提交补算作业：

    Job ID: 63867137
    Job name: GLP1R_b2_tpl
    Partition: a100

作业状态查询显示：

    JobState=PENDING
    Reason=AssocGrpGRES
    AllocTRES=(null)

这意味着作业已经被 Slurm 接收，但当时尚未获得所请求的 GPU 或计算节点。

随后还进行了交互式 GPU 资源申请与配额查询。相关交互式申请同样受到 AssocGrpGRES 限制。

因此，必须区分两个时间点：

第一，早期阶段，作业已经提交，但仍处于等待状态。

第二，后续补算工作实际推进并取得了缺失数据。

不能把早期的 PENDING 状态误写为已经完成预测，也不能因为早期提交受阻，就忽略后续实际完成的补算结果。

本阶段经历了多轮任务准备、资源排查和计算恢复。最终目标是尽可能在交我算平台恢复缺失的 40 条候选数据，而不是单纯完成一次作业提交。


============================================================
五、ColabFold 环境、输入与模板检查
============================================================

5.1 本地环境确认

本地工作目录：

    LOCAL_PATH

本地 ColabFold 可执行文件：

    USER_HOME/miniconda3/envs/colabfold/bin/colabfold_batch

此前检查确认，本地存在独立的 colabfold Conda 环境，并且 colabfold_batch 可执行文件能够调用帮助信息。

环境中还存在 biopy、boltz、gpd、pcann、proteinmpnn、pymol、rfdiff 和 rosetta 等环境。

这些环境检查主要用于确认本地是否具备继续处理预测结果、分析结构和开展后续工作的基础条件。

5.2 输入文件检查

补算与结果恢复期间，使用了统一的候选 FASTA 和批次输入文件。

保存的输入检查记录显示：

- combined_pool.fasta 存在。
- glp1.pdb 模板文件存在。
- formal_task_manifest.csv 存在。
- 候选输入长度统一为 31 aa。
- 批次任务被组织为 batch_0 至 batch_5。
- 输入任务清单曾按 seed=0、120、240 三组方案规划。

需要注意，最初的任务清单保留了原定三 seed 的规划信息，但最终完成的预测不能因此被描述为三个 seed 均已运行。

后续整理时，应以实际存在的输出目录和日志为准，不能仅凭任务清单中的计划行数统计完成任务数。

5.3 模板匹配日志

本地保存的 ColabFold 日志中出现了类似记录：

    Sequence 0 found templates: ['glp1_R', ...]
    Sequence 1 found templates: ['glp1_P']

这说明在相应运行中，ColabFold 确实报告了针对不同输入序列的模板匹配。

不过，这些日志仍然不能单独证明完整 GLP1R–semaglutide 复合物姿态已作为整体模板进入每一个候选预测。

因此，后续对模型分数的解释应以实际运行条件为准，并把模板使用情况作为需要记录的预测条件之一。

5.4 运行条件可比性的边界

本阶段尽可能让远程服务器与交我算补算使用相同的模型体系和参数，包括：

- 相同的目标体系；
- 相同的模型类型；
- 相同的 recycle 数；
- 相同的模型数量；
- 相同的 seed 设置；
- 尽可能一致的模板文件与模板路径组织方式。

但“相同参数”并不自动等于“完全相同的计算环境”。

两边的 GPU 型号、驱动、软件安装版本、依赖库、缓存、模板数据库和 MSA 获取状态仍可能存在差异。

因此，补算结果的可比性应建立在实际环境和日志核验之上。

本阶段的合理结论是：通过交我算平台补算，尽可能恢复了缺失候选在同一 ColabFold 预测体系下的结构数据；但不应将其夸大为已经严格证明两个平台的所有运行细节完全相同。

此外，seed=0 的三个模型输出不能替代原定的三个 seed。当前数据适合进行初步筛选与排序，若后续研究结论依赖预测稳定性，则仍需进行额外验证。


============================================================
六、ColabFold 输出文件与每条候选的三个模型结果
============================================================

6.1 预测结果的基本组织

ColabFold 预测结果通常包含多类文件，例如：

- *_rank_001_*.pdb
- *_rank_002_*.pdb
- *_rank_003_*.pdb
- *_scores_*.json
- *_predicted_aligned_error_v1.json
- 运行日志及其他辅助文件

其中，PDB 文件用于查看和分析预测结构；评分 JSON 保存模型的置信度信息；PAE JSON 保存预测对齐误差相关信息。

同一候选的 rank001、rank002、rank003 对应同一次运行中不同排名的模型结果。

这些文件应通过候选 ID、rank、模型名称和 seed 信息共同对应，不能仅凭文件名中的 rank 数字判断它们来自不同候选。

6.2 rank001、rank002、rank003 的含义

本阶段的 model=3 表示运行三个模型；ColabFold 输出中的 rank001、rank002、rank003 则是预测结果的排名标识。

两者相关，但不应把 rank 数字理解为独立随机种子的编号。

rank001 通常是 ColabFold 按其排序规则选出的第一名，rank002 和 rank003 为后续排名的模型。

由于最终目标是为大量候选建立统一的评价表，因此需要明确每条候选的代表结构选取规则。

本阶段已讨论并确定的基本处理思路是：

- 对每条候选保留统一规则下的代表模型数据；
- 不把不同模型的不同指标任意拼接；
- 如需考察模型间稳定性，额外保留三个模型的统计信息；
- 将候选级汇总与模型级原始记录分开保存。

如果主表采用 rank001 的指标，则 pLDDT、pTM、ipTM 及界面相关指标应尽量来自同一个 rank001 模型，避免将不同结构的分数混合成一个不存在的结构结果。

6.3 原始文件与汇总表的关系

本阶段的数据整理不应只留下一个最终 CSV。

至少应保留以下层次：

第一层：候选序列及候选编号清单。

第二层：每条候选的原始 ColabFold 输出文件，包括 PDB、评分 JSON 和 PAE JSON。

第三层：模型级指标表，记录每个候选、每个 rank 或模型的计算结果。

第四层：候选级汇总表，用于统计、排序、聚类及后续筛选。

这样可以在发现某条候选的指标异常时，追溯到具体结构、评分 JSON 和计算过程，而不是只能看到一行最终分数。

本阶段对模型结果进行清洗和汇总，正是为了建立这种从原始预测到候选级评价的追溯关系。


============================================================
七、补算批次的模型清洗与汇总
============================================================

7.1 批次清洗目标

在缺失的 40 条候选补算后，进一步检查每条候选的模型输出是否完整，确保后续计算指标时不会把异常模型当作有效结果。

这一过程涉及：

- 检查候选对应的模型文件是否存在；
- 检查评分 JSON 和 PAE 文件是否能够读取；
- 检查模型结构是否符合预期的链组成；
- 检查模型指标是否有效；
- 识别需要排除的异常模型记录；
- 按候选 ID 汇总保留下来的模型结果。

本阶段的目标不是简单统计文件数量，而是建立可以用于后续评价的有效模型记录。

7.2 batch_2 清洗结果

保存的 batch_2 清洗日志中，出现以下汇总：

    输入模型记录数：120
    候选记录数：40
    保留模型数：112
    剔除模型数：8
    无有效模型候选数：0
    使用 3 个模型的候选数：32
    使用 2 个模型的候选数：8

这组数据说明，在该批次的清洗结果中：

- 40 条候选均有可用于后续汇总的有效模型；
- 112 条模型记录通过清洗；
- 8 条模型记录被剔除；
- 32 条候选保留了三个有效模型；
- 8 条候选保留了两个有效模型。

因此，虽然原始模型记录数为 120，但清洗后的有效模型记录数为 112。

这也说明，不能只根据每条候选理论上应该有三个模型，就直接认定所有候选均具有三个有效模型。

后续候选级统计应同时保留有效模型数，避免把只有两个有效模型的候选与具有三个有效模型的候选视为完全相同的数据完整性状态。

7.3 清洗表与候选均值表

本阶段生成或整理了两类不同用途的 CSV：

第一类是模型清洗明细表，用于记录哪些模型保留、哪些模型剔除，以及清洗原因。

第二类是候选汇总表，用于把同一候选的有效模型指标整合起来。

在终端记录中，相关文件名包括：

    batch_2_model_cleaning_details.csv
    batch_2_candidate_mean_metrics.csv

最终整理时，还需要保留统一的候选级指标表，避免每个批次分别统计后难以进行跨批次比较。

7.4 模型清洗的解释边界

模型被剔除，可能意味着对应的模型输出存在异常或不符合预设的数据质量要求，但不能因此把该候选直接判定为无结合能力。

同样，某条候选只保留两个有效模型，并不意味着它的真实结合能力比保留三个模型的候选更差。

模型清洗是数据质量控制；候选评价则是对保留下来的结构和指标进行分析。这两件事必须分开处理。


============================================================
八、链映射与结构数据完整性检查
============================================================

8.1 为什么必须注明链映射

在计算界面指标时，链 A 和链 B 分别代表什么，是后续解释结果的关键。

如果不明确链映射，就可能出现：

- 把靶点链的指标误认为 binder 链的指标；
- 把 A-B 方向的指标误认为 B-A 方向；
- 不同批次的链顺序不一致；
- 不同脚本使用不同的链定义，导致结果无法直接比较。

因此，本阶段在汇总表中补充链映射信息，以便明确每个结构文件的链组成。

8.2 当前记录的链组成

在相关模型输出中，已检查到：

    A:384;B:31

即：

- Chain A：384 个残基，对应 GLP1R 受体链。
- Chain B：31 个残基，对应候选肽链。

本阶段后续指标计算均需要以实际结构文件的链组成和映射关系为依据。

需要注意，A:384;B:31 是结构链长度记录，并不意味着每条候选的全部指标都已通过独立的链身份验证。正式分析时仍应确认 PDB 文件中的链序列与输入序列对应。

8.3 结构与 PAE 数组的维度检查

保存的计算日志中出现以下维度：

    PAE: (415, 415)
    pLDDT: (415,)
    PDB atom positions: (415, 37, 3)

这些维度相互对应：

- 384 个受体残基；
- 31 个候选肽残基；
- 总计 415 个残基。

PAE 矩阵为 415 × 415，pLDDT 数组长度为 415，结构原子位置数组的第一维同样为 415。

这说明相关指标计算过程中，PAE、pLDDT 和 PDB 结构采用了相互对应的残基维度。

但维度一致只是基础检查，并不能单独证明所有指标都已按正确的链方向和定义计算。因此，后续还需要检查链索引、残基映射和指标实现方式。


============================================================
九、ipSAE、pDockQ 与 pDockQ2 指标的补充计算
============================================================

9.1 为什么需要额外计算界面指标

ColabFold 原始输出提供了常用的结构置信度信息，但在本阶段的数据处理中，还需要进一步获得能够描述链间相互作用和界面质量的指标。

因此，本阶段继续检查原始评分 JSON、PAE JSON 和 PDB 结构，尝试调用 ColabFold 内部相关函数计算 ipSAE、pDockQ 和 pDockQ2。

这一工作的重要意义在于：同一套原始预测数据不仅可以用于查看结构，还可以进一步转化为用于候选排序的界面评价指标。

9.2 ipSAE 的计算

ipSAE 是本阶段重点整理的界面相关指标之一。

计算过程中，需要使用 PAE、链间残基映射及相关置信度信息，并按照具体实现定义确定链间计算方向。

在保存的计算输出中，出现过如下形式的结果：

    ipsae:
      A-B: ...
      B-A: ...

这里 A-B 与 B-A 是两个方向的指标，不能直接当作同一个值。

后续比较时，应保持相同的方向定义。若某个候选使用 A-B，而另一个候选使用 B-A，即使二者都叫 ipSAE，也可能产生不公平的比较。

此外，ipSAE 的数值解释依赖实际使用的算法实现、残基选择和阈值设置。因此，在正式比较不同批次之前，应确认补算数据和已有数据使用相同的计算逻辑。

9.3 pDockQ 的计算

pDockQ 用于对预测复合物界面的可信程度进行评价。

本阶段尝试从 ColabFold 预测结构及相应置信度信息中计算该指标，并将其补入候选评价表。

在计算与整理过程中，需要确保：

- 使用正确的 PDB 结构；
- 链间残基对应关系正确；
- 输入的置信度信息来自相同的模型；
- 不混用不同 rank 的结构与评分数据；
- 记录使用的函数和参数设置。

9.4 pDockQ2 的计算

本阶段同样尝试计算 pDockQ2。

在补算数据处理中，pDockQ2 与 ipSAE 一样，属于需要从结构和置信度信息中进一步提取的界面指标。

相关计算需要确认链方向、残基索引和结构输入一致。

特别是 pDockQ2 与 pDockQ 虽然名称相近，但不能在没有确认定义的情况下视为可以互相替代的指标。

9.5 为什么必须核验算法实现

在已有批次和补算批次之间比较指标时，不能只检查列名相同，还要确认计算过程相同。

例如：

- 是否调用同一套函数；
- 是否使用相同的 PAE 数据；
- 是否使用相同的链映射；
- 是否使用相同的残基筛选规则；
- 是否采用相同的方向约定；
- 是否对异常模型进行了相同处理。

如果两批数据分别采用不同的实现方式，即使最终都生成了名为 ipSAE 或 pDockQ2 的列，也不能自动认定这些数值完全可比。

本阶段因此不仅补充计算指标，还将算法可比性作为需要单独核验的问题。

9.6 当前阶段的合理结论

通过读取原始结构、评分 JSON 和 PAE 文件，并进一步调用相应计算函数，本阶段为后续候选评价补充了更多界面相关信息。

但这些指标仍然属于模型预测评价，而不是实验亲和力的直接测量。

高 ipTM、ipSAE 或 pDockQ2 不能单独证明候选能够与 GLP1R 真实结合，也不能证明其具有预期的生物学功能。

后续应综合考虑多个结构指标、候选多样性以及必要的实验验证。


============================================================
十、候选级 CSV 整理与统计口径
============================================================

10.1 从模型级结果转向候选级结果

在获得每条候选的多个模型输出后，需要把模型级数据整理成候选级表格。

这是本阶段从“结构预测已经运行”转向“结果能够用于筛选”的关键一步。

模型级数据回答的是：

某条候选的某个模型预测结果如何？

候选级数据回答的是：

同一条候选在统一评价规则下表现如何？

二者用途不同，因此应分别保存。

10.2 主表与辅助表

本阶段的数据整理涉及以下几类表格：

1. 原始模型记录表。
2. 模型清洗明细表。
3. 候选级指标汇总表。
4. 各批次的汇总表。
5. 用于合并各批次结果的总表。

保存的脚本与日志中，出现了以下文件名：

    candidate_metrics_5_batches_all_ranks.csv
    candidate_metrics_5_batches_summary.csv

以及：

    batch_2_model_cleaning_details.csv
    batch_2_candidate_mean_metrics.csv

这些文件分别服务于模型级统计、候选级汇总和清洗审计。

后续正式分析时，需要确认总表中的每一行对应什么对象，以及不同批次是否采用一致的列名和统计规则。

10.3 候选编号与参考记录

本阶段使用 candidate_XXXX 形式的候选 ID，同时也出现了 reference_D41 等参考记录名称。

这些名称需要保留原始对应关系，不能在整理时随意改名。

特别是 D13、D41、D44 与 candidate_XXXX 之间的映射，应以正式候选清单或任务 manifest 为准。

reference_D41 这样的命名只能证明相应输出使用了该参考标识，不能仅凭命名就推断其在全部候选中的序号。

后续若需要报告 D13、D41、D44 的具体预测指标，应确保其对应的候选 ID、输入序列和结构文件完全一致。

10.4 代表模型的选择

对于需要为每条候选只保留一行数据的场景，本阶段采用统一的代表模型规则比事后挑选单项最高分更合适。

如果主表采用 rank001，则所有主表指标都应来自同一 rank001 模型，且应保持统一的 ColabFold 排序规则。

这样能够避免不同候选采用不同的选取规则而造成比较偏差。

同时，三个模型的均值、标准差和极值可以作为辅助统计，用于评估预测波动，但不能与主表中某一个具体模型的分数混为一谈。

10.5 对缺失模型的处理

如果某条候选有三个有效模型，而另一条候选只有两个有效模型，那么二者的候选级均值所基于的样本量不同。

因此，在候选级表格中，除了保存指标，还应记录有效模型数量。

如果后续需要对候选排序，可以先明确主分析采用哪种代表值，再使用有效模型数量和波动统计作为辅助信息。

不能在未说明规则的情况下，将缺失模型当作零分，也不能把没有成功生成结构的候选直接视为最差候选。

10.6 pLDDT值的计算

当前脚本中的 pLDDT_mean/max/min 是先计算每个 rank 的残基级统计，再对 rank 统计值进行汇总；

这和把所有 rank 的全部残基直接拼接后再计算不是完全相同的口径。

这里采用前一种方式，是为了让 pLDDT 的 mean/max/min 与其他指标一样，能够反映不同 rank 之间的变化。


============================================================
十一、对本阶段数据完整性与可比性的判断
============================================================

11.1 已经完成的工作

截至本阶段结束，已经获得以下成果：

- 241 条候选相关记录的 ColabFold 数据已完成收集与整理。
- 最终实际使用的主要预测设置为 seed=0、model=3、recycle=3。
- 已完成的远程服务器输出与后续补算数据被纳入同一整理流程。
- 缺失的 40 条序列已通过交我算平台的补算工作恢复。
- 已对补算批次的模型文件进行清洗。
- 已检查结构文件、PAE、pLDDT 及链长度之间的对应关系。
- 已开展 ipSAE、pDockQ 和 pDockQ2 等界面指标的补充计算。
- 已整理候选级汇总所需的 CSV 和相关辅助文件。
- 已明确后续筛选与聚类工作所需的数据基础。

11.2 仍需保留的限制

第一，未完成原定的三个 seed。

本阶段不能被描述为完整的三 seed 预测实验。后续如需分析不同 seed 之间的稳定性，需要补充相应预测。

第二，远程服务器与交我算平台的计算环境并非天然完全相同。

虽然补算尽可能复现了原有体系，但仍应以环境记录、运行日志、模板文件和指标计算实现为依据，说明实际可比性。

第三，三个模型结果不等同于三个独立 seed。

rank001、rank002、rank003 是同一次运行下的不同排名模型，不能被解释为三次独立重复计算。

第四，模型分数不是实验亲和力。

pLDDT、pTM、ipTM、ipSAE、pDockQ 和 pDockQ2 等指标可以为结构评价提供信息，但不能单独证明真实结合能力或生物学功能。

第五，候选级统计必须保留数据来源。

如果不同候选的有效模型数不同，或某些指标由补充脚本计算，应保留相应的模型数量、算法定义和来源记录。

11.3 为什么本阶段仍然有价值

虽然没有完成原定的三个 seed，但本阶段仍然建立了一个可以用于后续筛选的初步预测数据集。

更重要的是，经过这次工作，候选预测不再只是散落的 PDB 和 JSON 文件，而是开始形成一条可追溯的数据处理链：

候选序列
→ ColabFold 输入
→ 多模型预测
→ 原始结构与评分文件
→ 模型质量检查
→ 界面指标计算
→ 模型级汇总
→ 候选级统计
→ 后续筛选与聚类。

这条链路的建立，是后续进行大规模候选评价的重要基础。


============================================================
十二、下一阶段工作：筛选、聚类与综合评价
============================================================

12.1 第一项：完成候选级数据审计

在正式进行筛选前，首先应完成统一的候选级数据审计。

需要确认：

- 候选总数与正式输入清单一致；
- 每条候选具有正确的唯一 ID；
- 每条候选的输入序列与输出结构能够对应；
- rank001 代表模型的选择规则一致；
- 有效模型数量被正确记录；
- 缺失或异常模型没有被错误填入；
- ipSAE、pDockQ 和 pDockQ2 等指标的计算口径一致；
- 所有指标均有明确来源；
- D13、D41、D44 的候选编号映射已经确认。

12.2 第二项：开展候选筛选

筛选时不应仅按照 ipTM 或 pLDDT 进行单指标排序。

更合理的方式是综合考虑：

- 整体结构置信度；
- 链间相对定位与界面置信度；
- 界面接触情况；
- 界面几何是否合理；
- ipSAE、pDockQ 或 pDockQ2 等界面相关指标；
- 预测结果在多个模型之间的稳定性；
- 是否存在明显结构异常。

不同指标的作用不同，不能在没有依据的情况下简单相加或任意设置权重。

若要构建综合评分，应先明确每个指标的定义、方向、标准化方法和权重依据，并保留未经综合评分处理的原始数据。

12.3 第三项：开展候选聚类

在完成初步结构评价后，对候选进行聚类。

聚类的目的不是简单删除低分序列，而是识别候选之间的相似性与冗余，帮助后续选择具有一定多样性的候选集合。

可以考虑：

- 基于序列相似性的聚类；
- 在结构质量允许时，基于预测结构的聚类；
- 根据界面残基或结合模式进行进一步分析。

不同聚类方法回答的问题不同，应分别记录所使用的算法、阈值、输入数据及代表候选选择规则。

不能把序列相似直接等同于结构相同，也不能把结构相似直接等同于真实亲和力相同。

12.4 第四项：确定后续 Boltz 分析对象

本项目此前已经确定总体路线为：

ColabFold 初步预测
→ 候选聚类与筛选
→ Boltz 后续预测或评价
→ 综合结构评价与候选排序。

因此，下一阶段需要根据初步结构质量、界面指标和候选多样性，确定进入后续 Boltz 分析的候选集合。

进入下一阶段的候选应具有明确的选择依据，而不是单纯因为某一个模型分数最高。

12.5 第五项：保留不确定性

最终输出应使用“计算筛选候选”“结构评价优先候选”等措辞。

在缺乏实验亲和力或功能验证的情况下，不应直接把计算分数最高的候选称为“最佳结合剂”或“已验证有效的 GLP1R 激动剂”。

本阶段完成的是计算筛选的前置工作，后续仍需进一步的结构复核、必要的实验验证及结果解释。


============================================================
十三、本阶段文件与路径记录
============================================================

以下路径来自本阶段保存的终端记录，用于后续查找和核对。

13.1 本地工作目录

    LOCAL_PATH

该目录用于保存本地恢复的候选数据、日志、脚本和汇总结果。

13.2 本地 ColabFold 环境

    USER_HOME/miniconda3/envs/colabfold/bin/colabfold_batch

用于检查本地 ColabFold 版本、参数和后续结构分析的计算环境。

13.3 学长远程服务器相关目录

    LOCAL_PATH

用于查找原始批量预测的相关输出与日志。

13.4 交我算平台补算目录

    /dssgLOCAL_PATH

该目录涉及补算任务的输入、模板、批处理脚本和日志。

13.5 本地结果整理文件

已在终端记录中出现的文件包括：

    candidate_metrics_5_batches_all_ranks.csv
    candidate_metrics_5_batches_summary.csv
    batch_2_model_cleaning_details.csv
    batch_2_candidate_mean_metrics.csv

这些文件的用途分别涉及模型级指标记录、候选级汇总以及批次模型清洗。

需要注意：以上路径和文件名用于定位本阶段相关材料。正式归档时，应再次核对文件当前是否存在、是否为最终版本，以及是否已经包含全部批次的数据。


============================================================
十四、阶段总结
============================================================

本阶段的主要任务是完成 GLP1R 候选池的 ColabFold 初步结构预测，并将输出整理为可以用于筛选和聚类的结构数据。

原定方案是 241 条候选、三个 seed、三个模型、三个 recycle。受交我算平台排队困难、本地 GPU 算力不足和远程服务器异常影响，最终主要完成了 seed=0、model=3、recycle=3 的预测体系。

其中，201 条序列的预测数据在学长提供的远程服务器异常前已经完成并保留；另外 40 条序列在服务器故障后未能保留完整数据，随后通过交我算平台补算恢复。

补算过程中，不仅需要重新组织输入文件和运行参数，还需要处理 HPC 资源申请、作业等待、模板文件组织、模型结果检查及指标补充计算等问题。

在数据整理方面，本阶段进一步完成了模型输出清洗、链映射检查、PAE 与 pLDDT 维度检查、ipSAE 与 pDockQ 系列指标的补充计算，以及模型级和候选级 CSV 汇总。

本阶段的工作重点已经从“如何让 ColabFold 跑起来”转向“如何保证大量预测结果能够被统一、审计和比较”。

最终获得的数据可以作为后续候选筛选与聚类的基础，但应保留三个限制：

1. 本阶段没有完成原定的三个 seed。
2. 不同计算平台的运行环境和模板使用情况仍需根据实际记录说明，不能默认所有细节完全一致。
3. 所有结构置信度和界面评价指标均属于计算预测证据，不能直接替代实验亲和力或生物学功能验证。

下一阶段将以候选级数据审计为基础，进一步开展多指标筛选、候选聚类、代表序列选择和后续 Boltz 评价。

本阶段最重要的成果，是在计算资源受限和服务器故障的情况下，仍然完成了大规模候选结构预测数据的恢复与整理，为后续系统化筛选建立了可继续推进的数据基础。


============================================================
十五、操作小技巧与本阶段的小插曲
============================================================

15.1 Ctrl+Z 撤回误粘贴

本阶段结束后，整理工作记录时，曾经发生过一次小插曲：

刚刚复制粘贴时，不小心把整段工作记录粘贴成了一句话，差点把原本的文本结构弄乱。幸好豆包提醒使用 Ctrl+Z 撤回，成功恢复了粘贴前的状态。

这个小技巧值得记录：

当在文本编辑器、终端编辑器或其他支持撤销操作的输入区域中，误执行了粘贴、删除或格式修改，可以先尝试：

    Ctrl + Z

该快捷键通常用于撤销最近一次编辑操作。

如果误操作已经发生，且还没有继续进行大量编辑，及时使用 Ctrl+Z 往往可以快速恢复。

但需要注意：

- Ctrl+Z 的行为取决于当前应用程序。
- 在终端中，Ctrl+Z 可能表示挂起前台进程，而不是撤销文本编辑。
- 在不同软件中，撤销范围和历史记录也可能不同。
- 如果涉及覆盖文件、删除文件或其他不可逆操作，不应只依赖 Ctrl+Z，应优先检查文件内容并保留备份。

本次的经验是：处理长篇工作记录或重要数据时，粘贴前可以先确认光标位置和选区，粘贴后及时检查文本结构；一旦误操作，尽早撤销，避免在错误状态下继续编辑。

15.2 本阶段的经验

本阶段经历了远程计算、任务排队、服务器故障、补算、文件清洗和指标核验等多个环节。

这些经历说明，计算工作不仅要关注模型能否运行，还要重视任务状态记录、文件完整性、结果可追溯性和操作过程中的错误恢复。

即使最终计算方案没有完全达到最初预期，只要如实记录实际运行条件、明确数据限制，并对已完成结果进行规范整理，仍然能够为后续分析提供有价值的基础。

【本阶段记录结束】

---

# chatgpt response

收到，**阶段九：ColabFold 批量预测、远程计算故障恢复、补算与候选指标整理** 已接收。

我会将这份记录作为 GLP1R 项目完整工作历史的一部分保留在当前整理上下文中，尤其注意以下几点：

- **数据规模与实际执行条件：** 241 条候选相关记录，最终主要采用 seed=0、model=3、recycle=3，并未完成原定的三个 seed。
- **故障恢复过程：** 201 条序列的数据在远程服务器故障前得到保留，另外 40 条通过交我算平台补算恢复。
- **数据质量控制：** batch_2 原始 120 条模型记录中，112 条通过清洗、8 条剔除；40 条候选均至少保留两个有效模型。
- **指标计算边界：** ipSAE、pDockQ、pDockQ2 等是计算评价指标，不是实验亲和力或功能验证；链方向、模型来源和算法口径都需要一致。
- **可追溯性：** 保留候选清单、原始结构和评分文件、模型级明细、候选级汇总之间的对应关系。

我也会把这阶段的 **ColabFold 初筛数据** 与后续 **Boltz-2 结构评价、PCANN 计算** 区分开来，不把不同阶段的候选编号、预测条件或评价指标混为一谈。

我先继续等待你发送剩余材料，**暂时不生成阶段十二工作记录，也不提前撰写最终项目总结**。等你明确说材料已经发完、可以开始后，我再统一整理。

---

# you asked

message time: 2026-10-23 13:15:05

GLP1R reproduction 项目工作记录
阶段十：ColabFold 候选结果筛选、序列聚类、代表候选确定与 Boltz-2 预测准备

记录日期：2026-10-21 至 2026-10-22
项目：GLP1R de novo peptide candidate computational evaluation
工作阶段：候选级指标分析、序列多样性整理与后续 Boltz-2 输入准备

============================================================
一、本阶段工作概述
============================================================

第九阶段完成了 241 条候选相关记录的 ColabFold 数据收集、清洗和候选级指标整理。本阶段不再以完成批量预测为主要目标，而是转向如何利用已经获得的数据，从候选池中筛选出具有一定结构评价证据、序列代表性和后续分析价值的候选，并为下一阶段的 Boltz-2 共折叠预测做好准备。

本阶段的主要工作包括：

1. 在已经整理好的候选级 ColabFold 数据表基础上，开展候选筛选。
2. 以 D13、D41、D44 等参考候选为比较对象，尝试建立基于多项指标的筛选规则。
3. 将人工判断、指标比较和序列多样性纳入候选保留过程，形成 67 条候选的保留表。
4. 对保留候选的 31 aa 肽序列开展序列聚类，识别高度相似的序列家族。
5. 通过聚类代表和补充候选相结合的方式，形成 24 条代表候选的中间选择名单。
6. 核对高指标候选，并将 D13、D41、D44 三条参考序列纳入最终的 Boltz-2 输入候选集合，形成 27 条序列的 FASTA 文件。
7. 开始准备 GLP1R 受体的自定义多序列比对（MSA），包括同源序列整理、去重、MAFFT 多序列比对和 A3M 文件生成。
8. 重新检查 GLP1R 受体序列的长度、结构缺失残基和候选输入之间的对应关系，为 Boltz-2 正式预测解决输入一致性问题。

本阶段的工作重点是从 241 条候选的结构预测数据出发，建立一套兼顾结构指标、序列相似性和代表性选择的候选缩减流程，并将候选筛选结果推进到下一轮预测准备。

需要强调的是，本阶段完成的是计算结果筛选、序列聚类和输入准备。ColabFold 指标较高、进入代表名单或被选入 Boltz-2 输入集合，都不能直接证明候选与 GLP1R 具有真实结合能力，更不能直接证明其激动活性或其他生物学功能。


============================================================
二、从候选级 ColabFold 数据表进入筛选阶段
============================================================

2.1 数据基础

本阶段使用第九阶段已经整理的候选级 ColabFold 数据表作为主要数据基础。

候选序列长度为 31 aa，结构输出中的链组成记录为：

    A:384;B:31

其中：

- Chain A：384 aa 的 GLP1R 受体结构链；
- Chain B：31 aa 的候选肽链。

候选级表格保留了多个模型结果的汇总指标，并记录有效模型数量和候选编号，使后续筛选不必重新逐个读取所有原始结构文件。

本阶段使用的主要指标包括：

- pLDDT_mean：结构局部置信度的均值统计；
- ipTM_mean：复合物相对构象和界面相关的置信度指标；
- ipSAE_B-A_mean：B-A 方向的 ipSAE 均值；
- pDockQ_mean：界面质量相关指标；
- pDockQ2_A-B_mean：A-B 方向的 pDockQ2 均值；
- pDockQ2_B-A_mean：B-A 方向的 pDockQ2 均值。

此外，表格还保留了相应指标的最大值、最小值、有效模型数、候选序列、链组成以及后续聚类信息。

这些指标提供的是不同角度的结构评价信息，不能简单视为六个完全独立的证据，也不能把它们直接等同于实验亲和力。尤其是 ipSAE 和 pDockQ2 等方向性指标，在比较时必须保持链映射和计算方向一致。

2.2 为什么不能仅按单一指标排序

本阶段没有把某一项指标的最高值直接作为最终候选选择的唯一标准。

原因在于，不同指标反映的内容并不完全相同：

- pLDDT 主要反映局部结构预测置信度；
- ipTM 与复合物相对结构和界面预测相关；
- ipSAE、pDockQ 和 pDockQ2 提供其他界面评价信息；
- 不同指标之间可能存在相关性，也可能对同一候选给出不同的评价。

如果只按 ipTM 或其他某一个指标排序，容易忽略其他界面指标的差异，也可能使高度相似的候选在名单中占据过多位置。

因此，本阶段尝试将多项指标的相对表现与序列多样性结合起来，既保留结构评价表现较好的候选，也避免候选选择完全由某一项分数决定。


============================================================
三、以 D13 和 D44 为参照的候选筛选
============================================================

3.1 参考候选的作用

本阶段将 D13、D41、D44 作为需要特别保留和追踪的参考序列。

它们不仅是候选序列集合中的特定对象，也是后续比较候选指标、检查序列聚类结果和组织 Boltz-2 输入的重要参照。

在指标筛选过程中，主要使用 D13 和 D44 的六项 mean 指标作为比较基准；D41 则作为必须保留的参考序列之一，继续参与后续候选集合的组织。

这里的“参照”指计算分析中的比较对象，不意味着它们在本次 ColabFold 预测中已经被证明具有某种确定的真实结合能力。

3.2 六项 mean 指标比较

本阶段采用以下六项均值指标进行参照比较：

1. pLDDT_mean
2. ipTM_mean
3. ipSAE_B-A_mean
4. pDockQ_mean
5. pDockQ2_A-B_mean
6. pDockQ2_B-A_mean

筛选过程中，在初步人工判断的基础上，检查候选在上述指标上相对于 D13 或 D44 的表现。

一类候选需要在六项指标上均严格超过至少一个参照对象，才符合相应的严格比较条件。

这项规则的意义在于：候选不能仅凭单个指标较高就被视为全面优于参照序列，而需要在六项指标上同时满足严格的比较要求。

不过，这仍然是一种基于模型输出的相对筛选规则，并不是已经经过实验校准的结合判定标准。

3.3 从严格筛选到最终保留表

本阶段的候选保留不是简单地将严格筛选结果直接作为最终名单。

实际整理过程中，先进行了人工初步筛选，再按照六项 mean 指标相对于 D13/D44 的严格比较规则筛选候选。随后，又检查了一部分在六项指标中有较多项目超过参照值、但未满足全部严格条件的候选，并将其中符合补充保留规则的候选重新纳入。

具体而言，归档记录中包括：

- 按六项 mean 指标严格超过参照的规则筛出的 49 条候选记录；
- 另外恢复了 6 条在六项指标中至少有 4 项超过参照值的候选；
- 同时保留了人工初筛和代表性判断所需的候选。

经过上述筛选和整理，最终形成了 67 条候选的保留表。

需要注意，67 条是最终保留表的规模，不应简单将 49 条和 6 条相加后误认为最终总数。最终表还包含人工初筛和其他保留判断涉及的候选。

3.4 该筛选规则的局限

这一筛选规则的价值在于建立了可复核的相对比较流程，但仍存在以下限制：

第一，D13 和 D44 的模型分数只能作为当前计算体系中的参照，不能自动成为经过实验验证的普适阈值。

第二，六项指标之间可能存在统计相关性，因此六项同时超过参照，并不意味着获得了六份相互独立的结合证据。

第三，严格超过参照的规则可能排除一些具有不同序列特征或潜在价值的候选。因此，采用人工保留、补充保留和后续聚类等步骤，有助于减少单一硬阈值造成的信息损失。

第四，候选的保留与否应当被解释为进入后续计算的优先级判断，而不是对真实结合能力作出最终结论。


============================================================
四、67 条候选的序列聚类
============================================================

4.1 为什么在结构指标筛选后仍需要聚类

完成指标筛选后，67 条候选仍然不是 67 种完全不同的分子设计。

这些候选的肽长均为 31 aa，序列之间存在较多相似性，部分候选仅有少数氨基酸位点不同。

如果直接将全部候选送入后续计算，可能会在高度相似的序列上重复投入计算资源，也可能使最终分析过度集中于某几个序列家族。

因此，本阶段进一步对保留候选开展序列聚类，目的是识别序列家族、量化候选之间的相似程度，并为代表候选选择提供依据。

4.2 聚类方法与主方案阈值

本阶段对 31 aa 候选肽序列进行逐位氨基酸比较，并采用 complete-linkage（完全连接）聚类。

主方案使用的差异阈值为：

- 任意两条候选之间最多允许 3 个氨基酸位点不同；
- 对于 31 aa 的序列，这相当于至少有 28 个位置一致；
- 28/31 约为 90.3% 的逐位一致比例。

完全连接聚类的特点是，一个类群中的任意两条序列都需要满足规定的最大差异限制，而不是只要求每条序列与某一个中心序列相似。

这一约束能够避免仅通过一系列局部相似关系，将差异较大的序列链式地合并到同一类群。

按照主方案的设置，67 条候选被整理为 16 个序列类群。

4.3 聚类阈值敏感性检查

为了了解聚类结果是否过度依赖单一阈值，本阶段还检查了其他差异阈值下的类群数量。

归档结果如下：

- 最大差异不超过 2 aa：24 个类群；
- 最大差异不超过 3 aa：16 个类群；
- 最大差异不超过 4 aa：9 个类群。

这组结果说明，聚类粒度对差异阈值较为敏感。

当允许的差异更小，候选会被分成更多较细的序列家族；当允许的差异增加，更多候选会被合并到同一类群。

因此，16 个类群是基于本阶段选定的 3 aa 差异阈值所得到的结果，而不是对候选天然家族数量的唯一、绝对判定。

4.4 类群代表与 medoid

在每个类群中，本阶段进一步确定 medoid（类群中心代表序列）。

Medoid 是根据类群内部的序列差异关系确定的实际候选序列，而不是将每个位点取多数氨基酸后人工拼接出的新序列。

采用 medoid 的优势在于：

1. 代表序列本身确实存在于候选集合中；
2. 可以明确追溯其原始候选 ID；
3. 能够计算其他成员与代表序列之间的氨基酸差异数；
4. 有助于在后续计算中同时考虑类群代表性和个别候选的结构指标。

本阶段将类群规模、medoid 身份和候选相对于 medoid 的差异数等信息加入聚类结果表，为后续代表候选选择提供了结构化依据。

4.5 D13、D41、D44 的聚类映射

本阶段的聚类结果还明确记录了三条参考候选在保留表中的对应关系：

- D13：candidate_0165，位于 C14；
- D44：candidate_0173，位于 C06；
- D41：candidate_0241，与 reference_D41 对应，并作为单例位于 C16。

其中，D41 所在类群为单例，说明在当前 67 条保留表和所采用的聚类规则下，没有其他候选被归入该类群。

这些聚类编号只描述当前数据集和阈值下的序列关系，不应被解释为候选的功能分类，也不能直接证明不同类群具有不同的真实结合模式。

4.6 主要聚类文件

本阶段形成或使用的关键文件包括：

    candidate_metrics_kept_clustered.csv
    sequence_cluster_summary.csv
    cluster_medoid_sequences.fasta

其中：

candidate_metrics_kept_clustered.csv：
保留候选的指标表与聚类信息相结合的结果，包含候选编号、序列、指标、有效模型数量、类群编号、类群规模、medoid 和相对差异等信息。

sequence_cluster_summary.csv：
用于汇总各个序列类群及其代表信息。

cluster_medoid_sequences.fasta：
用于集中保存类群代表序列，方便进一步检查、提取和组织后续预测输入。

这几类文件分别承担候选级分析、类群统计和代表序列导出的功能，不应相互替代。


============================================================
五、从聚类结果中挑选代表候选
============================================================

5.1 为什么不只保留 16 条 medoid

在 67 条候选被划分为 16 个类群之后，一个直接方案是每个类群只保留一个 medoid。

但本阶段没有把“一个类群只保留一个候选”作为唯一选择原则。

原因在于，序列中心性与结构指标表现是两个不同维度：

- Medoid 更侧重于代表类群内部的序列关系；
- 结构指标用于描述特定候选的模型预测表现；
- 类群内的不同序列变体可能具有不同的预测结果；
- 只保留一个中心序列，可能会丢失某些在结构指标或局部序列变化上值得进一步研究的候选。

因此，本阶段采用“类群代表 + 补充候选”的思路，尽量兼顾序列家族覆盖和结构评价信息。

5.2 24 条候选的中间选择名单

本阶段形成了 24 条代表候选的中间选择名单。

这份名单采用主代表和次代表相结合的方式：一部分候选作为相应类群的主要代表，另一部分则用于保留有价值的序列变体或补充类群内部信息。

选择时考虑的内容包括：

- 候选所属的序列类群；
- 候选是否为类群 medoid；
- 候选与 medoid 之间的氨基酸差异数；
- 候选的 ipTM_mean；
- 候选的 ipSAE_B-A_mean；
- 候选的 pDockQ_mean；
- 候选的 pDockQ2_A-B_mean 和 pDockQ2_B-A_mean；
- 候选的 pLDDT_mean；
- 候选有效模型数量；
- 候选在综合排序中的位置；
- 类群内部是否已经有其他候选被保留。

归档的选择名单中，候选被标注为 Primary representative 或 Secondary representative，并记录 cluster_id、cluster_size、medoid_candidate、substitutions_to_medoid 和 combined_rank_score 等字段。

这些字段使代表候选的选择过程能够追溯到具体的序列家族和指标，而不是只保留一个没有解释的候选 ID 列表。

5.3 主代表与次代表的含义

Primary representative：
主要用于代表相应序列家族，选择时考虑该候选的结构指标表现及其对类群的代表价值。

Secondary representative：
用于补充保留其他有价值的序列变体或中心候选，以减少只保留单一代表所造成的信息损失。

这里的主代表与次代表是本项目内部的候选组织标签，并不意味着主代表已经被证明在生物学上更优，也不意味着次代表一定具有较低的真实结合能力。

5.4 24 条名单与最终 27 条输入的区别

需要区分两个阶段的文件：

    GLP1R_representative_selection_24.csv
    GLP1R_representatives_24.fasta

这两个文件对应 24 条代表候选的中间选择结果。

随后，本阶段进一步核对了高指标候选，并将 D13、D41、D44 三条参考序列明确加入最终输入集合，形成：

    GLP1R_representatives_24_plus_D13_D41_D44.fasta

该 FASTA 文件包含 27 条记录。

因此，24 条代表候选名单与 27 条最终输入 FASTA 不是相互矛盾的数量：前者是中间选择名单，后者在此基础上额外保留了三条指定参考序列。

D13、D41、D44 的加入，是为了使后续预测能够与已有参考对象进行对照，而不是把它们误认为新产生的候选。

5.5 代表候选选择的意义与限制

通过代表候选筛选，本阶段将候选缩减从简单的分数排序推进到同时考虑序列关系和结构指标的过程。

其主要意义包括：

1. 减少高度相似序列的重复计算；
2. 保留不同序列类群的代表；
3. 为类群内的关键变体保留后续验证机会；
4. 将参考候选纳入后续预测集合；
5. 为后续 Boltz-2 结果与 ColabFold 结果之间的比较建立统一的候选对应关系。

但 27 条候选只是本阶段确定的下一轮计算输入集合，并不意味着已经选出了 27 条真实 binder，也不意味着这些候选都通过了实验验证。

同样，24 条中间名单和最终 27 条 FASTA 的角色不同，在后续报告中应明确其统计口径，避免混淆。


============================================================
六、Boltz-2 阶段的任务定位
============================================================

6.1 为什么在 ColabFold 之后继续开展 Boltz-2 预测

ColabFold 阶段已经为候选提供了初步结构预测及相应的结构置信度和界面评价信息。

本阶段选择代表候选之后，下一步是使用 Boltz-2 对筛选后的候选进行进一步共折叠预测和评价。

这样做的目的不是简单地用另一个模型重复产生一组分数，而是为后续候选比较增加一个不同预测体系下的结构评价结果。

本项目的整体工作顺序由此进一步明确为：

241 条候选序列
→ ColabFold 批量预测与候选级指标整理
→ 依据参考指标和人工判断筛选
→ 67 条候选保留表
→ 31 aa 序列聚类
→ 16 个类群及其代表信息
→ 24 条代表候选中间名单
→ 加入 D13、D41、D44，形成 27 条 Boltz-2 输入集合
→ 准备 GLP1R 受体输入和自定义 MSA
→ 后续开展 Boltz-2 共折叠预测
→ 汇总不同预测体系下的结构与界面评价信息。

6.2 本阶段已经完成的 Boltz 准备

截至本阶段记录时，已经形成 27 条候选输入的 FASTA 文件，并开始整理 GLP1R 受体的自定义 MSA。

这意味着本阶段已经完成从大规模候选池到下一轮预测输入集合的筛选与组织工作，也开始处理 Boltz-2 预测所需的受体序列和同源信息。

但必须明确：候选 FASTA 已生成、MSA 已生成，与 Boltz-2 已成功读取 MSA 并完成正式预测，是不同的工作状态。

截至本记录结束，当前自定义 MSA 已完成初步构建与序列检查，但尚未通过实际 Boltz-2 预测确认其读取行为和最终输入兼容性。

因此，本阶段不应写成“27 条候选已完成 Boltz-2 预测”。


============================================================
七、GLP1R 受体序列与结构缺失残基检查
============================================================

7.1 为什么需要重新检查受体序列

在开始准备自定义 MSA 后，本阶段发现，GLP1R 的结构坐标序列、此前使用的受体输入序列以及用于同源比对的目标序列之间，需要进一步明确长度和残基对应关系。

这一问题会直接影响后续预测：

- MSA 的 query 必须与目标链序列正确对应；
- 受体序列长度变化会改变残基索引；
- 结构中没有坐标的残基，不一定意味着其在理论序列中不存在；
- 将缺失环区恢复到序列中，不代表已经恢复了它们的真实三维构象。

因此，本阶段先检查已有 7KI0 参考结构的 R 链、原有受体 FASTA 和包含更多构建序列信息的 FASTA，而不是直接把一份新的长序列未经检查地替换进预测流程。

7.2 原始结构链的长度与缺失区域

从 GLP1R_7KI0_chainR.fasta 对应的结构坐标序列中，得到的受体链长度为 384 aa。

该序列与此前 GLP1R_D13.fasta 中使用的受体序列完全一致。

对结构残基编号进行检查后，发现两个内部编号区间存在缺口：

- 残基编号 129 后直接到 137，缺少 130–136，共 7 个残基；
- 残基编号 339 后直接到 344，缺少 340–343，共 4 个残基。

两处合计涉及 11 个残基。

这里的“缺失”首先指结构坐标中没有对应残基，不能仅凭 PDB 坐标缺失就断定这些残基在理论蛋白序列中不存在。

7.3 491 aa 构建序列与结构链序列的区别

此前整理的 491 aa 构建序列除了 GLP1R 受体序列信息外，还包含额外的构建片段、连接区域或表达相关尾部。

例如，构建序列中存在结构坐标序列未包含的片段：

    KRGERSS

以及：

    MCKT

同时，构建序列的 C 端还包含额外的延伸和表达相关序列。

因此，不能将完整 491 aa 构建序列不加区分地作为 GLP1R 受体的标准预测输入。

本阶段将重点放在受体本身的序列、结构中未解析的内部残基以及额外构建片段之间的区分上，避免把表达标签或其他构建相关序列误当作天然受体结构的一部分。

7.4 395 aa 受体序列方案

基于上述检查，本阶段建立了一个 395 aa 的受体序列候选版本：

    LOCAL_PATH

其长度来自：

384 aa 结构坐标序列
+ 7 aa 的第一处缺失片段
+ 4 aa 的第二处缺失片段
= 395 aa。

该版本的目的，是将结构中没有坐标但在构建序列中存在的内部残基重新纳入序列，为后续受体序列和 MSA 准备提供另一种更完整的输入方案。

但是，395 aa 仍然是需要验证的输入方案，而不是已经通过结构实验或预测对照证明最优的受体表示方式。

特别是，补回残基只解决序列层面的缺失问题，不意味着 Boltz-2 会自动恢复这些环区的真实构象。

因此，后续正式预测前仍需明确使用 384 aa 还是 395 aa，并保证 MSA query、YAML 受体链序列和最终预测输入完全一致。


============================================================
八、GLP1R 自定义 MSA 的构建
============================================================

8.1 构建 MSA 的目的

为了为 GLP1R 受体准备可追溯的同源序列信息，本阶段开始构建自定义 MSA。

与直接使用一条受体序列不同，多序列比对能够把受体与相关同源蛋白之间的保守区域、插入和缺失关系组织起来。

本阶段的工作重点是：

1. 整理原始 GLP1R 同源序列；
2. 检查序列字符与记录质量；
3. 去除完全重复的序列；
4. 将目标 query 加入输入；
5. 使用 MAFFT 进行多序列比对；
6. 根据目标 query 的比对关系生成 A3M；
7. 检查 A3M 的记录数、query 长度和序列字符。

8.2 原始同源序列数据

原始同源序列文件为：

    LOCAL_PATH

原始文件中共有 476 条同源序列记录。

初步审计发现：

- 原始同源记录数：476；
- 含 X 的记录：2；
- 其他异常字符记录：0；
- 完全重复序列记录：79。

其中，人、小鼠和大鼠 GLP1R 序列都出现在原始同源序列集合中。

审计后，排除含 X 的序列，并去除重复记录，同时避免将与 query 完全相同的序列再次作为独立同源记录加入，最终保留 395 条同源序列。

随后，将 395 aa 的 query 加入输入文件，得到：

    LOCAL_PATH

该输入文件共包含 396 条记录，其中一条是目标 query，另外 395 条为去重后保留的同源序列。

8.3 MAFFT 多序列比对

本阶段使用 MAFFT 7.526 对 396 条输入序列开展多序列比对。

实际调用的程序路径为：

    USER_HOME/miniconda3/bin/mafft

主要参数为：

    --auto
    --thread 4

对应的比对输出文件为：

    LOCAL_PATH

MAFFT 日志显示，比对过程正常完成，并对全部 396 条输入记录进行了处理。

这一过程建立了目标 query 与不同长度同源序列之间的列对应关系，为后续 A3M 转换提供了基础。

需要注意，MAFFT 完成只说明多序列比对程序成功运行，不自动证明所有局部插入和缺失都符合预期的生物学对应关系。因此，后续仍需要根据受体序列结构域和关键区域对比对结果进行质量检查。

8.4 从对齐 FASTA 转换为 A3M

在获得 MAFFT 对齐结果后，本阶段进一步将对齐文件转换为 A3M 格式。

生成文件为：

    LOCAL_PATH

转换过程以 395 aa query 为参照，将 query 对齐位置中对应的同源序列插入残基以小写字母表示，并保留 query 对应位置的氨基酸信息。

生成过程中进行了多项检查：

- 对齐文件能够被读取；
- 对齐结果中恰好存在一条目标 query；
- query 去除对齐缺口后与原始输入序列完全一致；
- A3M 中的 query 与目标输入序列完全一致；
- 输出文件能够被重新读取。

最终检查结果为：

    比对记录数：396
    A3M 记录数：396
    Query 长度：395
    A3M Query 与输入序列完全一致：True

A3M 文件大小约为 194,634 bytes。

8.5 A3M 序列表示的检查

在检查 A3M 前几条记录时，观察到人、小鼠和大鼠 GLP1R 序列均长于 395 aa query。

例如，完整长度为 463 aa 的人、小鼠和大鼠序列，在 A3M 中表现为：

- 大写残基数：395；
- 小写残基数：68；
- gap 数：0。

这是当前 A3M 转换结果相对于 395 aa query 的序列表示方式。

小写残基表示相对于 query 的插入部分，不应将它们直接解释为无效字符或原始序列被截短。

目前已经完成了 A3M 的记录数、query 一致性和基本字符层面的检查。

但还需要明确：A3M 文件生成成功，并不等于 Boltz-2 已经成功读取它，也不等于其中的所有同源序列都能以预期方式参与预测。

8.6 当前 MSA 文件清单

本阶段已经形成以下主要文件：

    LOCAL_PATH
    LOCAL_PATH
    LOCAL_PATH
    LOCAL_PATH

以及 query 文件：

    LOCAL_PATH

它们分别对应原始同源序列、去重后的输入集合、MAFFT 对齐结果、最终 A3M 和目标 query。

保留这些中间文件，有助于追溯同源序列的来源、去重过程、对齐结果以及 A3M 的生成方式，而不只是留下最终 MSA 文件。


============================================================
九、当前 Boltz-2 输入一致性问题
============================================================

9.1 发现的问题

截至本阶段结束，虽然已经生成 395 aa query 对应的自定义 A3M，但此前候选预测输入文件中使用的受体序列为 384 aa。

相关文件为：

    LOCAL_PATH

该输入文件中的受体链与原始 384 aa 结构坐标序列一致。

因此，当前需要解决的不是单纯的 A3M 文件是否存在，而是正式预测输入之间的对应关系：

- 当前自定义 MSA 的 query 长度为 395 aa；
- 原有受体输入序列长度为 384 aa；
- 两者并不完全一致。

如果不解决这一问题，就不能直接将 395 aa query 对应的 A3M 视为 384 aa 受体输入的有效 MSA。

9.2 下一步必须完成的输入核验

正式开展 Boltz-2 预测前，需要明确以下事项：

1. 最终使用 384 aa 还是 395 aa 的受体序列；
2. 目标受体 FASTA 或 YAML 中的序列是否与所选 MSA query 完全一致；
3. 自定义 A3M 是否能够被当前安装的 Boltz-2 版本按预期读取；
4. YAML 中 MSA 的指定方式与实际文件路径是否正确；
5. 候选肽链是否保持 31 aa，且候选编号、序列和最终 FASTA 一致；
6. 预测完成后，是否能从输出文件确认输入链长度和链对应关系。

本阶段已经完成 MSA 的初步构建，但这些输入一致性问题尚未全部解决。

9.3 当前阶段的完成状态

截至本阶段记录结束，工作状态如下：

已完成：
- 241 条候选相关 ColabFold 数据的后续筛选；
- 67 条候选保留表整理；
- 31 aa 序列聚类及聚类结果导出；
- 16 个类群的主方案聚类结果；
- 类群 medoid 与代表候选整理；
- 24 条代表候选的中间选择名单；
- 加入 D13、D41、D44 后的 27 条 Boltz-2 输入 FASTA；
- GLP1R 原始同源序列审计与去重；
- 395 aa query 的建立；
- MAFFT 多序列比对；
- 自定义 A3M 生成和基本一致性检查。

尚未完成：
- 最终受体序列长度方案的确认；
- MSA 与正式预测 YAML 之间的序列一致性核验；
- 自定义 MSA 被 Boltz-2 正确读取的实际验证；
- 27 条候选的正式 Boltz-2 预测；
- Boltz-2 输出结果的质量检查和指标汇总。

因此，本阶段的准确结论是：已经完成从 ColabFold 候选数据整理到代表候选确定，并推进了 Boltz-2 自定义 MSA 的准备；但尚未完成正式的 Boltz-2 预测和跨模型结果比较。


============================================================
十、本阶段形成的主要成果
============================================================

本阶段形成了以下几类成果。

第一，建立了从候选级 ColabFold 数据到代表候选的筛选流程。

筛选不再仅依赖某一项指标的排名，而是结合六项 mean 指标相对于参考候选的表现、人工判断以及后续序列聚类，形成了更具可追溯性的候选缩减流程。

第二，完成了 67 条候选的序列聚类和类群信息整理。

主方案采用 31 aa 序列逐位比较和 complete-linkage 聚类，在最多 3 个氨基酸差异的限制下得到 16 个类群，并对阈值敏感性进行了检查。

第三，建立了类群代表与补充候选相结合的选择策略。

通过主代表、次代表、medoid 和相对序列差异等信息，减少了高度相似候选的重复保留，同时尽量保留有价值的序列变体。

第四，形成了 27 条候选的 Boltz-2 输入 FASTA。

这份输入集合包含 24 条代表候选及 D13、D41、D44 三条指定参考序列，为下一阶段的预测任务提供了候选清单。

第五，建立了 GLP1R 自定义 MSA 的初步处理流程。

原始同源序列经过字符检查、去重、MAFFT 比对和 A3M 转换，形成了 396 条记录的 A3M 文件，并确认其中 query 与 395 aa 输入序列完全一致。

第六，明确了后续预测中必须解决的受体序列一致性问题。

通过比较结构坐标序列和构建序列，确认了 384 aa 与 395 aa 两种输入方案的区别，并明确 MSA query 与正式受体输入必须保持一致。

这些成果使项目从 ColabFold 的初步候选评价推进到代表候选的确定和 Boltz-2 预测准备阶段。


============================================================
十一、本阶段的局限与后续工作
============================================================

11.1 筛选阈值尚未经过实验校准

当前筛选规则是基于已有预测指标和参考候选的相对比较建立的。

即使某条候选在六项 mean 指标上超过 D13 或 D44，也不能据此直接判断它具有更高的真实结合亲和力。

后续应将这些筛选规则视为候选优先级的计算依据，并结合其他预测结果以及可能获得的实验数据进一步校准。

11.2 聚类结果依赖序列差异阈值

在当前数据集下，最大差异不超过 2、3、4 个氨基酸时分别得到 24、16、9 个类群。

因此，16 个类群是当前主方案的结果，不是唯一的生物学分类。

后续如果需要对序列家族作更严格的定义，应进一步明确聚类标准，并确保不同版本的类群编号不会被混用。

11.3 代表候选不等于最终最优候选

类群 medoid、Primary representative 和 Secondary representative 分别服务于不同的选择目的。

序列中心性较高的候选不一定具有最高结构指标；结构指标较高的候选也不一定是类群中心。

因此，后续应继续保留候选 ID、原始序列、类群、指标来源和选择原因，避免将内部代表标签误解为最终生物学排名。

11.4 自定义 MSA 尚未通过 Boltz-2 实测验证

当前 A3M 已完成基本格式和 query 检查，但尚未完成正式 Boltz-2 预测验证。

后续需要确认实际输入格式、MSA 路径、受体序列长度以及预测输出的链对应关系。

尤其是 384 aa 与 395 aa 两种受体输入不能与同一份 query 不一致的 MSA 混用。

11.5 预测结果仍然属于计算证据

无论 ColabFold 还是 Boltz-2，其输出均属于计算预测结果。

不同预测器给出一致结果可以提高后续研究的优先级，但不能自动等同于真实结合、激动活性或实验亲和力。

后续如果获得实验数据，应进一步比较计算指标与实验结果之间的对应关系。


============================================================
十二、下一阶段的工作安排
============================================================

下一阶段的优先事项为：

1. 明确 GLP1R 受体正式输入使用 384 aa 还是 395 aa 序列。
2. 核对最终受体序列与自定义 A3M query 的逐位一致性。
3. 检查当前 Boltz-2 版本对自定义 A3M 的输入方式，并准备对应 YAML。
4. 对单个候选开展小规模测试，确认 Boltz-2 能够正常读取输入并生成结果。
5. 检查预测输出中的受体链和候选肽链是否与输入相符。
6. 在输入和输出检查通过后，再对 27 条候选执行正式预测。
7. 汇总 Boltz-2 输出的结构、置信度和相关评价指标。
8. 将 Boltz-2 结果与 ColabFold 候选级数据进行对应，分析两种预测体系之间的一致性和差异。
9. 在保留原始数据、输入清单和计算条件的基础上，开展进一步候选排序与优先级判断。

本阶段的工作使项目完成了候选数据筛选、序列家族整理和代表候选组织，并初步建立了 GLP1R 自定义 MSA。

下一阶段的重点将从“确定哪些候选进入下一轮计算”转向“确保输入正确、完成 Boltz-2 预测，并检验不同计算体系对候选结构评价的支持程度”。

---

# chatgpt response

收到，阶段十的工作记录已纳入当前项目资料。我会继续等待你发送后续材料，**暂时不生成阶段十二工作记录，也不提前整理成最终文本**。

这一阶段我会重点保留以下信息，避免后续把不同阶段的结果混在一起：

- **候选筛选：** 从 241 条候选相关记录出发，整理出 67 条保留候选；筛选依据包括六项 ColabFold 均值指标相对 D13/D44 的表现、人工判断及补充保留规则。
- **序列聚类：** 对 31 aa 序列采用 complete-linkage 聚类；主方案允许最多 3 个位点差异，得到 16 个类群，并记录 2、3、4 aa 阈值下分别为 24、16、9 个类群的敏感性结果。
- **代表候选：** 先形成 24 条中间代表名单，再加入 D13、D41、D44，形成 27 条 Boltz-2 输入序列。两份名单的用途和数量会明确区分。
- **MSA 与受体输入：** 记录 384 aa 结构坐标序列、395 aa 补回缺失片段的候选序列，以及 491 aa 构建序列之间的区别；保留 396 条记录的自定义 A3M 已完成初步检查、但当时尚未通过 Boltz-2 实测验证这一状态。
- **阶段边界：** 阶段十完成的是候选筛选、聚类和预测输入准备，不能写成已经完成 27 条候选的 Boltz-2 正式预测。

我也会注意区分**当时的计划、当时已完成的工作，以及后续阶段实际取得的结果**。你可以继续发送下一份记录；等你明确说材料已经发完、可以开始后，我再统一整理。

---

# you asked

message time: 2026-10-23 13:15:18

# 第十一阶段工作记录：GLP1R 候选肽的 Boltz-2 结构预测、结构基准评价与候选筛选

**项目目录：** `LOCAL_PATH  
**计算环境：** Conda 环境 `boltz`  
**参考结构：** PDB `7KI0`  
**阶段核心任务：** 对 27 条 GLP1R 候选肽进行 Boltz-2 复合物结构预测，提取模型评价指标，开展受体结构比对与候选排序，筛选出 5 条进入后续分析的候选序列。

---

## 一、阶段背景与工作目标

在前期候选肽设计工作基础上，本阶段进入结构预测与计算评价环节。此前得到的候选序列需要经过结构层面的进一步检查，才能判断哪些值得优先投入后续计算资源。

本阶段并不是简单地选择 ipTM 或其他单项分数最高的候选，而是逐步建立一套综合评价流程：

1. 使用 Boltz-2 对候选肽与 GLP1R 受体进行复合物结构预测。
2. 提取每个模型的结构置信度、界面相关指标等数据。
3. 以参考结构 `7KI0` 为基准，对预测得到的受体结构进行比对。
4. 计算 TM-score 和 RMSD 等结构评价指标。
5. 将模型级数据汇总到候选级，比较多次采样结果。
6. 分别观察不同指标组合下的排序结果，避免依赖单一分数。
7. 根据预先使用的筛选阈值进行候选过滤。
8. 结合结构指标、筛选结果和基线候选，确定最终的五条序列。

本阶段的主要产出是结构预测数据、结构评价数据、候选排序和五条待进一步研究的候选肽。

**阶段边界：** 结构预测和计算排序只能为候选优先级提供证据，不能直接证明真实结合亲和力，也不能单独证明 GLP1R 激动活性。

## 二、Boltz-2 运行设置与采样规模

### 2.1 计算环境

- 工作目录：`LOCAL_PATH
- 使用环境：`boltz`
- 预测工具：Boltz-2
- 预测对象：27 条候选肽与 GLP1R 受体组成的复合物
- 参考结构：`7KI0`

### 2.2 参数记录

根据此前对话中记录的设置，本阶段参数如下：

| 参数 | 设置值 | 用途 |
|---|---:|---|
| `diffusion_samples` | 3 | 每条候选设置 3 个扩散采样 |
| `seed` | 3 | 随机种子，按本次纠正后的记录填写 |
| `recycling_steps` | 3 | 结构预测迭代回收次数 |
| `sampling_steps` | 200 | 采样步数 |
| `step_scale` | 1.5 | 扩散采样步长缩放参数 |
| `max_parallel_samples` | 1 | 并行采样数限制 |
| 受体 MSA | 本地 GLP1R MSA | 为受体提供序列比对信息 |
| 候选肽 MSA | `empty` | 不为短肽提供 MSA |

以上是目前从历史对话中恢复的参数记录。由于当前工作记录没有附上完整的原始命令行和配置文件，归档时仍应以实际运行日志为最终依据。特别是随机种子，应在最终实验记录中保持与实际执行命令一致。

### 2.3 采样规模

候选数量为 27 条，每条候选设置 3 个 diffusion samples：

$$
27 \times 3 = 81
$$

因此，本阶段的计划规模为 **27 条候选、81 个模型采样结果**。

后续历史记录明确提到，81 个模型的受体 TM-score 已经成功计算，并输出了逐模型结果和候选汇总 CSV。

需要区分两个概念：

- **采样规模：** 27 条候选 × 3 次采样，共 81 个预期结果。
- **成功输出规模：** 应以输出文件中实际存在的模型记录为准。

历史对话确认了 81 个模型参与了结构评价，但若需要严谨地写明每个模型都成功完成所有预测步骤，仍应检查原始输出目录。

## 三、Boltz-2 结果整理与模型级数据提取

### 3.1 模型输出结构

此前在处理司美格鲁肽参考结构时，已经检查过 Boltz 输出文件的组织方式。记录中包含 `model_0`、`model_1`、`model_2`，以及对应的 CIF、JSON 和 NPZ 文件。

当时还遇到过一次文件路径问题：最初假定 PAE 文件位于较浅的目录中，脚本因此出现 `FileNotFoundError`。后来确认，实际数据位于更深层的 `predictions` 子目录中。

这一过程说明，在提取 Boltz 指标时，不能仅凭预想的目录结构拼接路径，必须根据实际输出目录读取对应文件。

### 3.2 复合物链结构

参考结构分析中记录的链长为：

| 组成部分 | 链 | 长度 |
|---|---|---:|
| GLP1R 受体 | Chain A | 395 aa |
| 候选肽 | Chain B | 31 aa |
| 合计 | A + B | 426 aa |

这一链长信息来自参考复合物分析记录。提取数组中的肽链指标时，需要根据实际链顺序与长度切分，而不能把整条复合物的指标直接当成肽链指标。

例如，在此前处理参考结构数据时，肽链的 pLDDT 使用了：

`plddt[395:426]`

跨链 PAE 则从受体与肽链对应的矩阵区域提取，分别检查受体到肽链、肽链到受体的误差估计。

这类切分操作的目的，是避免受体长度占主导时掩盖短肽自身的结构不确定性。

### 3.3 记录的模型级指标

本阶段候选预测的数据整理涉及以下指标：

- `confidence_score`
- `ptm`
- `iptm`
- `complex_plddt`
- `complex_iplddt`
- `complex_pde`
- `complex_ipde`
- `protein_iptm`
- `tm_score`
- `rmsd_A`

这些指标不属于同一类量，不能简单地视为可以直接相加的“结合能力分数”。

其中：

- `confidence_score`、`ptm`、`iptm` 等用于描述模型置信度或复合物结构预测相关信息。
- `complex_plddt`、`complex_iplddt` 等涉及结构或局部区域的置信度。
- `complex_pde`、`complex_ipde` 等涉及预测距离误差，解释时应遵循对应软件版本的指标定义。
- `tm_score` 和 `rmsd_A` 是本阶段进一步进行结构比较后得到的评价指标。

**重要的数据处理原则：** 原始模型指标、候选级统计量和最终筛选结果应分开保存。不能用候选级均值替代单模型原始结果，也不能在汇总时丢失候选 ID 和模型 ID 的对应关系。

## 四、参考结构评价：以 PDB 7KI0 为基准

### 4.1 为什么要计算结构相似性

仅查看 Boltz-2 自身输出的置信度指标，不足以判断受体在复合物预测中的构象是否与参考结构一致。

因此，本阶段额外引入了参考结构比对：将预测复合物中的 GLP1R 受体链 A 与 PDB `7KI0` 的受体链 R 进行比较。

该步骤的目的，是把模型自身的置信度信息与外部参考结构比较结合起来，观察不同候选对应的预测受体结构是否存在系统性差异。

### 4.2 TM-score 计算

历史记录确认，受体 TM-score 使用 **US-align** 计算，比较对象为：

- 预测结构中的 GLP1R Chain A；
- 参考结构 `7KI0` 中的受体 Chain R。

此前成功得到逐模型 TM-score，并进一步生成候选级汇总结果。

历史记录中提到，按参考长度归一化的 TM-score 大致位于 **0.6782–0.7877**。

部分候选的受体 TM-score 统计结果如下：

| 候选 | 记录中的候选级 TM-score |
|---|---:|
| `candidate_0082` | 0.7877 |
| `candidate_0213` | 0.7806 |
| `candidate_0096` | 0.7782 |
| `candidate_0081` | 0.6782 |
| `candidate_0111` | 0.6877 |

其中，`candidate_0082` 的候选级 TM-score 中位数最高，`candidate_0213` 和 `candidate_0096` 随后；`candidate_0081` 与 `candidate_0111` 位于较低区间。

需要注意，以上数字是历史记录中报告的候选级统计结果，不能将其误写成每个候选三个模型的所有单独 TM-score。正式归档时，应以 `receptor_tmscore_vs_7KI0.csv` 中的统计字段为准，区分均值、中位数和单模型值。

### 4.3 RMSD 计算与结构评价

本阶段还对预测结构与参考结构进行了 RMSD 评价。

此前的讨论涉及受体对齐后再计算局部结构 RMSD 的方案，并提到使用 Biopython 处理结构叠合。当前可恢复记录中，候选汇总表使用了 `rmsd_A` 字段，并在后续筛选中采用 `rmsd_A_mean`。

本阶段部分候选的平均 RMSD 为：

- `candidate_0082`：约 3.73 Å
- `candidate_0096`：约 3.98 Å
- `candidate_0200`：约 3.98 Å
- `candidate_0043`：约 3.98 Å
- `candidate_0044`：约 4.10 Å

RMSD 较低通常意味着在既定对齐方案下，结构坐标差异较小。但 RMSD 会受到对齐对象、所选原子、残基范围和结构柔性影响，因此解释时必须明确所比较的是哪部分结构。

**当前记录的限制：** 历史摘要确认了 RMSD 的计算和候选汇总，但未完整保留最终脚本中每一个 RMSD 的原子选择、残基选择和对齐参数。不能仅根据字段名推断所有细节。

### 4.4 TM-score 与 RMSD 的联合意义

TM-score 与 RMSD 提供的是互补信息：

- TM-score 反映整体结构相似性；
- RMSD 反映特定结构对齐方案下的坐标偏差。

因此，不能单独以 TM-score 最高作为唯一筛选标准，也不能将较低 RMSD 直接解释为结合更强。

本阶段将这两类结构评价与 Boltz-2 的置信度和界面相关指标结合，用于后续候选排序与筛选。

## 五、候选级汇总与不同指标组合的排序

### 5.1 为什么需要候选级汇总

每条候选设置了 3 次扩散采样，因此单个候选不只有一个模型结果。

如果仅从某一次预测中选取最高分模型，可能会过度依赖一次采样结果。候选级汇总则可以比较不同候选的整体表现，并观察不同采样之间的波动。

本阶段形成了候选级汇总表，并将 TM-score、RMSD、Boltz-2 置信度及界面相关指标用于候选比较。

### 5.2 三指标排序

历史记录中保存的三指标 Top 8 顺序为：

1. `candidate_0096`
2. `candidate_0082`
3. `candidate_0043`
4. `candidate_0200`
5. `candidate_0111`
6. `candidate_0175`
7. `candidate_0044`
8. `candidate_0173`

部分候选的三指标统计记录如下：

| 候选 | TM-score 中位数 | TM-score 标准差 | RMSD (Å) |
|---|---:|---:|---:|
| `candidate_0096` | 0.7782 | 0.0057 | 3.98 |
| `candidate_0082` | 0.7877 | 0.0173 | 3.73 |
| `candidate_0043` | 0.7765 | 0.0215 | 3.98 |
| `candidate_0200` | 0.7636 | 0.0212 | 3.98 |
| `candidate_0111` | 0.6877 | 0.0021 | 3.77 |
| `candidate_0175` | 0.7630 | 0.0097 | 4.02 |
| `candidate_0044` | 0.7732 | 0.0096 | 4.10 |
| `candidate_0173` | 0.7595 | 0.0160 | 4.00 |

这些结果说明，结构相似性、RMSD 和采样间波动并不总是指向同一个候选。例如，`candidate_0111` 的 TM-score 较低，但其 RMSD 记录并不是该表中最高的；因此不同指标需要结合解释。

这里的三指标排序是特定指标组合下的计算排序，不应被描述为对真实结合能力的实验排名。

### 5.3 五指标排序

随后，历史记录中又保存了五指标 Top 8：

1. `candidate_0082`
2. `candidate_0096`
3. `candidate_0200`
4. `candidate_0170`
5. `candidate_0173`
6. `candidate_0043`
7. `candidate_0044`
8. `candidate_0112`

五指标结果中记录的数值如下：

| 候选 | 平均 TM-score | 平均 RMSD (Å) | TM-score 标准差 | 平均 complex pLDDT | 平均 complex ipDE |
|---|---:|---:|---:|---:|---:|
| `candidate_0082` | 0.78772 | 3.73 | 0.01413 | 0.814995 | 0.735100 |
| `candidate_0096` | 0.77824 | 3.98 | 0.00464 | 0.798158 | 0.772982 |
| `candidate_0200` | 0.76360 | 3.98 | 0.01727 | 0.809582 | 0.841012 |
| `candidate_0170` | 0.76059 | 4.02 | 0.00893 | 0.822592 | 0.933972 |
| `candidate_0173` | 0.75946 | 4.00 | 0.01306 | 0.804936 | 1.062791 |
| `candidate_0043` | 0.77650 | 3.98 | 0.01757 | 0.793486 | 0.980332 |
| `candidate_0044` | 0.77325 | 4.10 | 0.00788 | 0.799851 | 0.972089 |
| `candidate_0112` | 0.77090 | 4.13 | 0.00873 | 0.803045 | 0.939019 |

需要注意两点：

1. 五指标排序与三指标排序不同，说明候选排名受到指标选择和评价规则的影响。
2. `complex_ipDE` 的方向与具体定义需要结合 Boltz-2 的对应版本文档解释；在未核对定义前，不应擅自将其写成“数值越大结合越强”或相反。

### 5.4 这一阶段得到的认识

本阶段并没有得出“某个模型的所有分数都能准确预测结合能力”的结论。相反，不同指标组合得到不同排序，说明需要把结构一致性、模型置信度和界面相关证据分开看待。

因此，候选排序的用途是缩小后续研究范围，而不是替代亲和力实验或功能实验。

## 六、五指标筛选：阈值、基线与剔除记录

### 6.1 筛选对象

历史记录显示，在该轮严格筛选中，实际进入筛选的候选为 **20 条**。

这一数字与最初开展 Boltz-2 预测的 27 条候选不同，说明在进入该轮过滤之前存在一个候选范围缩小步骤。但当前可恢复的历史记录没有完整说明从 27 条到 20 条的具体纳入规则，因此正式档案不应凭空补写其原因。

### 6.2 筛选阈值

该轮筛选使用的剔除条件为：

| 指标 | 剔除条件 | 对应通过条件 |
|---|---|---|
| 平均 RMSD | `rmsd_A_mean > 3.9` | `rmsd_A_mean <= 3.9` |
| 平均 TM-score | `tm_score_mean < 0.77` | `tm_score_mean >= 0.77` |
| 平均 ipTM | `iptm_mean < 0.9` | `iptm_mean >= 0.9` |
| 平均 complex pLDDT | `complex_plddt_mean < 0.79` | `complex_plddt_mean >= 0.79` |
| 平均 confidence score | `confidence_score_mean < 0.8` | `confidence_score_mean >= 0.8` |

这里的逻辑是：候选只要触发相应的剔除条件，就可能因该指标不满足阈值而被过滤。多个条件可以同时触发，因此不能把各项触发数简单相加后当作剔除总数。

`candidate_0173` 被指定为基线候选，作为参照予以保留，不按这套条件直接剔除。基线豁免不代表它满足全部阈值，也不代表它已被证明是实验阳性。

### 6.3 筛选统计

历史记录中保存的筛选统计为：

- 进入该轮筛选：20 条；
- 最终保留：2 条；
- 被剔除：18 条；
- 在不计 `0173` 基线豁免的候选中，`candidate_0082` 是记录中唯一同时满足全部五项条件的候选。

各剔除条件的触发数量：

| 条件 | 触发数量 |
|---|---:|
| 平均 RMSD > 3.9 Å | 14 |
| 平均 TM-score < 0.77 | 11 |
| 平均 ipTM < 0.9 | 6 |
| 平均 complex pLDDT < 0.79 | 6 |
| 平均 confidence score < 0.8 | 3 |

这些计数是条件触发数，而不是互斥的候选分组。

### 6.4 筛选结果的解释

从筛选记录看，`candidate_0082` 的优势是其平均 TM-score 较高、平均 RMSD 较低，同时满足该轮设定的五项阈值。

但必须强调：

- 阈值是当前计算流程中的操作性标准；
- 当前记录没有显示这些阈值已通过实验阳性、阴性数据进行正式校准；
- 满足结构阈值并不等于已证明具有高亲和力；
- 作为基线保留的 `0173`，其作用是提供比较参照，而不是作为真实活性已确认的结论。

因此，正确的结论是：`0082` 在当前这套计算筛选规则下表现突出，而不是它已经被证实为最强 GLP1R 结合肽。

## 七、最终五条候选序列

综合候选排序、结构评价与后续分析需求，本阶段最终选定以下五条序列：

```fasta
>candidate_0082
HAEGTFTSDVSRYLEEKAVKQFVERLRRGGG
>candidate_0096
HAEGTFTSDVSRYLEEQAVKAFVDRLKRGAG
>candidate_0200
HAEGTFTSDVSRYLEEKAVKAFVERLRRGGG
>candidate_0043
HAEGTFTSDVSRYLEEQAVKAFVDRLKRGGG
>candidate_0044
HAEGTFTSDVSRYLEEKAVKAFVDRLKRGAG
```

五条候选均为 **31 aa**。

### 7.1 五条序列的筛选定位

| 候选 | 本阶段定位 |
|---|---|
| `candidate_0082` | 五指标排序第一；在记录的严格筛选中通过全部五项阈值 |
| `candidate_0096` | 三指标排序第一、五指标排序第二；作为结构表现较好的候选保留 |
| `candidate_0200` | 五指标排序第三；纳入最终候选集合 |
| `candidate_0043` | 在两种排序中均进入 Top 8；纳入最终候选集合 |
| `candidate_0044` | 在两种排序中均进入 Top 8；纳入最终候选集合 |

这里需要区分两件事：严格阈值筛选与最终五条候选集合并不是同一个结果。记录显示，严格筛选保留两条，其中包含基线 `0173`；而最终确定的五条候选为 `0082、0096、0200、0043、0044`。因此，不能把最终五条全部写成“通过了五指标严格阈值”。

### 7.2 与基线候选 0173 的序列比较

基线候选 `candidate_0173`（D44）的序列为：

```fasta
>candidate_0173
HAEGTFTSDVSRYLEEKAVKDFVERLKRGAG
```

五条最终候选与 `0173` 的差异如下：

| 候选 | 相对于 0173 的突变 | 序列一致性 |
|---|---|---:|
| `candidate_0044` | D21A、E24D | 29/31 = 93.5% |
| `candidate_0082` | D21Q、K27R、A30G | 28/31 = 90.3% |
| `candidate_0096` | K17Q、D21A、E24D | 28/31 = 90.3% |
| `candidate_0200` | D21A、K27R、A30G | 28/31 = 90.3% |
| `candidate_0043` | K17Q、D21A、E24D、A30G | 27/31 = 87.1% |

这些序列彼此高度相似，部分候选之间仅有少数位置的氨基酸变化。这为后续比较序列变化与预测结构、界面指标之间的关系提供了基础。

不过，仅从突变列表不能断定某个突变提高了受体结合能力。若要分析突变效应，需要进一步比较相应的结构、界面环境和后续亲和力或功能证据。

## 八、司美格鲁肽参考结构分析：此前完成的辅助工作

此前的历史对话还记录了对司美格鲁肽参考复合物的 Boltz-2 评价。这是 GLP1R 项目中已进行的辅助分析，可用于了解参考肽在当前结构预测流程中的模型表现，但它与 27 条新候选的筛选结果应分开记录。

### 8.1 参考结构数据

历史记录中，司美格鲁肽参考复合物的受体链 A 为 395 aa，肽链 B 为 31 aa，总计 426 aa。

在处理参考模型时，曾提取以下指标：

- ipTM
- pTM
- 肽链 pLDDT
- 双向跨链 PAE

### 8.2 三个参考模型的结果

| 模型 | ipTM | pTM | 肽链 pLDDT | 双向 PAE |
|---|---:|---:|---:|---:|
| model 0 | 0.9397 | 0.8850 | 0.7521 | 5.8371 |
| model 1 | 0.9603 | 0.9220 | 0.7299 | 4.5800 |
| model 2 | 0.8924 | 0.9173 | 0.5316 | 8.7435 |

此前的处理脚本将结果写入：

`semaglutide_reference_metrics.csv`

历史记录还提到，实际 NPZ 文件位于更深层的 `predictions/semaglutide_glp1r_reference/` 路径下，而不是脚本最初假定的浅层目录。

### 8.3 这组参考结果能说明什么

三个参考模型之间存在一定差异：model 1 的 ipTM 较高，model 2 的肽链 pLDDT 较低且双向 PAE 较高。

这说明即使对参考肽进行结构预测，不同采样模型也可能呈现不同的局部置信度与跨链误差估计。

但这组参考结果不能直接作为新候选的亲和力标尺，也不能把参考肽的模型分数直接转换成新候选的实验活性。若要将其用作正式校准集，还需要明确同一预测设置、指标定义、样本构成和比较规则。

## 九、项目文件与结果归档

当前历史记录中涉及的候选评价文件包括：

| 文件 | 内容与用途 |
|---|---|
| `boltz_sample_metrics.csv` | 模型或采样级指标 |
| `boltz_candidate_summary.csv` | 候选级指标汇总 |
| `audit/structure/per_model_structure_metrics.csv` | 逐模型结构评价 |
| `audit/structure/receptor_tmscore_vs_7KI0.csv` | 预测受体与 7KI0 的 TM-score 比对结果 |
| `audit/structure/candidate_27_three_model_means.csv` | 27 条候选的三模型均值汇总 |
| `audit/structure/candidate_27_filter_vs_0173.csv` | 候选筛选与基线比较记录 |
| `audit/structure/candidate_retained_vs_0173.csv` | 保留候选与 0173 的比较 |
| `audit/structure/candidate_retained_vs_0173_removed.csv` | 剔除候选相关记录 |
| `semaglutide_reference_metrics.csv` | 司美格鲁肽参考模型指标 |

以上文件名均来自现有历史记录；本次没有直接打开当前工作目录检查文件内容，因此不把它们视为已经逐一核验过的文件清单。

正式归档时，应保留：

1. 原始 Boltz-2 输出；
2. 模型级指标表；
3. 候选级汇总表；
4. 参考结构比对结果；
5. 筛选阈值与剔除清单；
6. 最终五条候选的 FASTA；
7. 实际运行命令、配置文件与日志。

这样可以从最终候选反向追踪到原始预测结果，而不是只留下最终排名。

## 十、本阶段结论与当前证据边界

本阶段完成了 GLP1R 候选肽从结构预测到计算筛选的主要流程。

具体包括：

1. 对 27 条候选设置每条 3 个 diffusion samples，形成 81 个模型的结构评价工作。
2. 收集 Boltz-2 的模型置信度与界面相关指标。
3. 使用 US-align 将预测受体链 A 与 PDB `7KI0` 的受体链 R 比对，计算 TM-score，并生成逐模型和候选级 CSV。
4. 结合 RMSD 与其他指标比较候选表现。
5. 对比三指标和五指标排序，发现候选排名会受到指标组合影响。
6. 对 20 条进入严格筛选的候选应用五项操作性阈值，并保留 `0173` 作为基线参照。
7. 最终确定 `0082、0096、0200、0043、0044` 五条 31 aa 候选肽，作为后续研究对象。

本阶段的重要结果不是证明某条序列已经具有真实结合活性，而是形成了一套可追溯的候选优选流程：结构预测、参考结构比较、多指标汇总、候选筛选以及序列层面的整理。

### 当前仍不能下的结论

- 不能仅凭 ipTM 或结构置信度证明真实结合亲和力。
- 不能仅凭 TM-score 或 RMSD 证明候选具有更强的受体结合能力。
- 不能仅凭计算结构证明 GLP1R 激动活性。
- 不能把操作性筛选阈值称为已经通过实验校准的生物学阈值。
- 不能将最终五条候选全部描述为通过了五指标严格筛选。

## 十一、下一阶段：亲和力预测与候选优先级复核

下一阶段可以围绕当前五条候选开展进一步评价，但应与本阶段的结构预测结果分开建档。

建议按以下逻辑衔接：

### 11.1 固定当前候选集合

以本阶段最终确定的五条序列为输入，保留其原始 ID 和序列，避免在后续计算中因重命名造成结果混淆。

### 11.2 区分结构评价与亲和力评价

本阶段已经完成的 TM-score、RMSD、ipTM 等指标应继续作为结构评价证据保存，但不能将它们直接改名为亲和力指标。

后续如果开展亲和力预测，应单独记录所用工具、输入结构、参数、输出字段、评分方向和局限性。

### 11.3 保留基线用于比较

`candidate_0173` 可以继续作为本阶段的计算比较基线；如果后续纳入已知参考肽或实验数据，应明确它们各自的身份和证据等级，不应把计算基线与实验阳性对照混为一谈。

### 11.4 进一步验证候选

亲和力预测可以帮助调整计算候选的优先级，但其结果仍然属于预测证据。若最终目标是开发 GLP1R 激动剂，还需要与真实结合能力及受体功能相关的实验结果相结合。

**当前状态：** 历史记录确认已经完成结构预测、结构指标提取、TM-score/RMSD 评价、候选排序和五条序列选择；但没有找到足以确认新候选亲和力预测已经完成的记录。因此，本阶段不将亲和力预测写成已完成工作。

---

# chatgpt response

收到第十一阶段工作记录。我会把它作为 **GLP1R 项目的 Boltz-2 结构预测、结构基准评价与候选筛选阶段** 的主要记录之一，暂时不开始撰写 Stage 12。

我会特别保留以下信息，避免后续汇总时混淆：

- **预测规模与参数：** 27 条候选、每条 3 次扩散采样、预期 81 个模型；记录中的随机种子为 `3`，最终仍应以实际运行日志为准。
- **评价流程：** Boltz-2 模型级指标、US-align 受体结构比对、TM-score、RMSD、候选级汇总，以及三指标与五指标排序。
- **严格筛选的边界：** 20 条候选进入该轮筛选，保留 2 条（包含基线 `candidate_0173`）；`candidate_0082` 是记录中唯一通过全部五项阈值的非基线候选。这不等于其生物学活性已得到验证。
- **候选集合的区分：** 本阶段选出的五条为 `candidate_0082`、`candidate_0096`、`candidate_0200`、`candidate_0043`、`candidate_0044`。其中 `0044` 是这一阶段的候选，后续最终候选集合发生了调整，不能把两个阶段的名单混为一谈。
- **参考肽分析：** 司美格鲁肽的三个 Boltz-2 参考模型单独记录，不把参考肽分数直接当作候选亲和力的校准标准。
- **证据边界：** 结构预测、结构相似性和模型置信度用于计算候选优先级，不能单独证明结合亲和力或 GLP1R 激动活性。

我也会保留你记录中明确指出的未核实项，例如从 27 条缩小到 20 条的具体规则、RMSD 的完整计算细节，以及原始文件是否都实际存在并经过核验。

你可以继续发送后续阶段的工作记录。我会等你明确说材料已经发完、可以开始后，再统一整理 Stage 12。

---

# you asked

message time: 2026-10-23 13:16:29

发完了，可以开始了，直接给我文本就行，我自己复制保存，记得工作总结要详细一些

---

# chatgpt response

# 第十二阶段工作记录：GLP1R 候选肽的 PCANN 评分、结果核查与最终候选优选

项目名称：GLP1R 从头设计候选肽的计算评价与优选

项目目录：`LOCAL_PATH

PCANN 代码目录：`LOCAL_PATH

PCANN 运行环境：Conda 环境 `pcann`

本阶段工作性质：基于 Boltz-2 预测结构开展 PCANN 评分，核查批处理脚本与数据类型问题，汇总候选级评分，讨论评分数值的解释边界，并结合此前的结构评价确定后续优先研究的候选集合。

重要说明：本阶段属于计算预测与结果整理，不包含新的湿实验。PCANN 输出及其数值转换不能直接视为实验测得的结合亲和力；本项目目前没有足够的实验数据证明最终候选具有真实 GLP1R 结合能力或激动活性。

## 一、阶段背景与目标

在此前的候选设计与结构评价阶段，项目已经使用 ProteinMPNN 生成大量候选肽序列，并经历序列去重、序列规则筛选、结构预测、受体结构比对以及多指标排序。

第十一阶段使用 Boltz-2 对候选肽与 GLP1R 进行复合物结构预测，并将预测受体与参考结构 PDB 7KI0 进行比较。该阶段得到了一批结构评价表现较好的候选，但结构置信度、TM-score、RMSD 等指标主要反映预测结构的可信程度或与参考结构的相似性，不能直接等同于真实结合亲和力。

因此，第十二阶段进一步引入 PCANN，对选定候选对应的 Boltz-2 预测结构进行评分，尝试从另一套计算评价方法中获得补充证据。

本阶段的具体目标包括：

1. 检查 PCANN 批处理脚本是否能够正确处理 Boltz-2 输出结构。
2. 将候选 ID、PCANN 内部标签、Boltz-2 模型编号进行对应，确保评分可以追溯到具体结构。
3. 解决批处理结果汇总时的数值类型错误。
4. 生成逐结构评分表和候选级汇总表。
5. 比较候选的 PCANN 平均评分、模型间波动及其与此前结构评价结果的关系。
6. 讨论 PCANN 评分向条件性 Kd 数值转换的前提，避免把模型输出误写成实验亲和力。
7. 结合 Boltz-2 结构评价、PCANN 评分及候选之间的序列关系，确定最终优先研究的四条候选肽。

本阶段的核心问题不是简单地选择 PCANN 数值最极端的候选，而是判断新增评分能为现有候选排序提供什么补充信息，以及这些信息究竟能支持多强的结论。

## 二、PCANN 分析对象与批处理设计

### 2.1 软件与目录

PCANN 代码目录：

`LOCAL_PATH

项目工作目录：

`LOCAL_PATH

批处理脚本：

`examples/make_predictions/run_glp1r_pcann_batch.py`

本阶段围绕该脚本进行了多轮修改、备份、语法检查和运行调试。记录中存在以下备份文件：

- `run_glp1r_pcann_batch.py.backup_20261023_122250`
- `run_glp1r_pcann_batch.py.backup_20261023_093519`
- `run_glp1r_pcann_batch.py.backup_20261023_093212`
- `run_glp1r_pcann_batch.py.backup_20261023_092914`

这些备份反映了脚本在正式批处理前后经过了若干轮修改。正式归档时应优先保留最终实际执行的脚本，并将备份用于追踪修改过程，而不是将所有备份都视为最终版本。

### 2.2 纳入 PCANN 的结构

本阶段对六个候选或参照对象进行分析，每个对象对应三个 Boltz-2 预测模型：

- `candidate_0043`
- `candidate_0044`
- `candidate_0082`
- `candidate_0096`
- `candidate_0173`
- `candidate_0200`

其中：

- `candidate_0173` 是基线候选，序列对应此前记录中的 D44 参考候选。
- `candidate_0044` 是此前结构筛选阶段纳入过的中间候选。
- `candidate_0082`、`candidate_0096`、`candidate_0200` 和 `candidate_0043` 是最终优先研究的四条候选。

每个对象使用三个 Boltz-2 模型进行评分，因此预期处理结构数为：

6 × 3 = 18 个结构。

本阶段的 18 个结构是 PCANN 的分析输入规模，不应与第十一阶段的 27 条候选、81 个预期扩散采样结果混为一谈。第十一阶段是更大范围的结构预测与筛选；第十二阶段是在收窄后的对象上开展补充评分。

### 2.3 候选 ID 与 PCANN 标签的映射

PCANN 批处理脚本进行了相应调整，以便将 PCANN 使用的结构标签重新映射为项目内部的候选 ID。

主要处理内容包括：

1. 保留 PCANN 原始标签字段 `pcann_label`。
2. 根据结构标签匹配对应的候选 ID。
3. 将 Boltz-2 模型编号记录在 `boltz_model` 字段中。
4. 对标签进行标准化处理，包括去除用于匹配的 `_wt` 后缀。
5. 保留原始标签与标准化后的候选标识之间的对应关系。

这一步很重要，因为 PCANN 内部使用的结构标签未必与项目中的候选编号完全相同。如果只保存最终平均评分而不保留原始标签和模型编号，就难以从候选级分数追溯到具体预测结构。

本阶段因此不只关注是否成功得到评分，也关注结果表是否具备足够的可追溯性。

## 三、PCANN 批处理中的错误与修复

### 3.1 首次汇总失败

在首次汇总 PCANN 输出时，脚本出现以下错误：

`TypeError: Expected numeric dtype, got object instead.`

错误发生在候选级汇总结果的数值格式化操作中，具体位置为：

`summary["pcann_avg_mean"].round(4)`

该错误表明，脚本执行 `round(4)` 时，相关列没有被 Pandas 识别为预期的数值类型。

需要注意，这一错误本身不能证明 PCANN 的评分计算失败，也不能证明原始结果中一定存在非法字符串。问题可能发生在数据读取、类型推断、分组聚合或中间 DataFrame 的构造环节。

### 3.2 对原始结果进行诊断

随后检查了原始输出文件：

`pcann_results/pcann_raw_18_structures.csv`

记录中的诊断结果如下：

- DataFrame 形状为 `(18, 30)`。
- 共 18 行，对应 18 个预测结构。
- 包含 `pdb_id`、`avg`、`model_1` 至 `model_25`、`pcann_label`、`candidate_id` 和 `boltz_model` 等字段。
- 重新读取 CSV 后，`avg` 列被识别为 `float64`。
- 对重新读取的 `avg` 列检查时，没有发现非数值内容。

这说明，至少在重新读取原始 CSV 后，`avg` 列是正常的数值列。错误更可能与脚本运行时的中间数据类型或汇总过程有关，而不能简单归因于原始 CSV 的 `avg` 字段全部以文本形式保存。

这里仍应区分两种情况：重新读取文件后的数据类型，和第一次运行时内存中的 DataFrame 数据类型，并不一定相同。

### 3.3 修复方式

为提高数据处理的可靠性，脚本修改为显式转换相关字段：

- `avg`
- `model_1` 至 `model_25`

使用的处理逻辑是：

`pd.to_numeric(..., errors="raise")`

随后进一步检查：

1. 转换是否成功。
2. 是否出现 NaN。
3. 是否出现非有限数值。

该方式比直接调用 `.round(4)` 更稳健，因为它能够在汇总之前暴露不符合数值预期的数据，而不是等到格式化阶段才失败。

### 3.4 修复后的验证

修复后完成了以下检查：

- 保存脚本备份。
- 运行 `python -m py_compile` 检查语法。
- 再次执行批处理。
- 成功生成逐结构原始评分、候选级汇总和结构检查结果。

因此，本阶段可以确认：PCANN 批处理脚本经过类型处理修改后，已经成功运行并生成了对应的结果文件。

不过，语法检查和批处理成功只能说明脚本可以执行、数据处理流程能够完成，不能独立证明 PCANN 的科学预测能力，也不能替代对评分函数、训练数据和模型适用范围的验证。

## 四、PCANN 输出文件与数据结构

本阶段生成或更新的主要文件如下。

### 4.1 逐结构原始评分

文件：

`pcann_results/pcann_raw_18_structures.csv`

该文件记录 18 个结构的 PCANN 输出。已知字段包括：

- `pdb_id`
- `avg`
- `model_1` 至 `model_25`
- `pcann_label`
- `candidate_id`
- `boltz_model`

其中，`avg` 是本次候选级汇总所使用的主要结构级评分字段；`model_1` 至 `model_25` 是 PCANN 输出的其他模型相关字段。当前记录没有充分说明每个 `model_i` 字段的完整科学定义，因此不应仅根据字段名称赋予其额外的生物学解释。

逐结构文件的主要作用是保留原始结果，并维持每条记录与候选 ID、PCANN 标签及 Boltz-2 模型编号的关联。

### 4.2 候选级汇总表

文件：

`pcann_results/candidate_summary.csv`

该文件将每个候选的三个结构评分进行汇总，包含以下已记录字段：

- `candidate_id`
- `n_structures`
- `pcann_avg_mean`
- `pcann_avg_std`
- `pcann_avg_min`
- `pcann_avg_max`

其中：

- `n_structures`：用于汇总的结构数量。
- `pcann_avg_mean`：三个结构的 PCANN `avg` 平均值。
- `pcann_avg_std`：三个结构评分的标准差。
- `pcann_avg_min`：三个结构中的最小评分。
- `pcann_avg_max`：三个结构中的最大评分。

这类汇总可以帮助比较不同候选的整体评分及模型间波动，但每个候选只有三个结构，因此统计量仍然有限。三个预测模型不是三个独立的湿实验重复，也不能据此计算真实结合能力的实验变异。

### 4.3 结构检查表

文件：

`pcann_results/structure_checks.csv`

该文件用于保存结构检查相关结果。现有记录没有给出该文件全部字段和逐行内容，因此本阶段只记录其存在及用途，不对未核实的具体检查项作进一步推断。

### 4.4 结果可追溯性原则

本阶段形成的结果组织方式强调三个层次：

1. **逐结构结果：** 保留 PCANN 对每个 Boltz-2 预测结构的评分。
2. **候选级汇总：** 对同一候选的三个结构进行统计。
3. **最终候选决策：** 将 PCANN 结果与前一阶段的结构评价结合，决定优先研究对象。

这三个层次不能互相替代。候选级均值不能代替原始结构数据；PCANN 排名也不能直接替代结构筛选或实验验证。

## 五、PCANN 候选级评分结果

### 5.1 汇总数据

本阶段得到的 PCANN 候选级评分如下。

| 候选 | 结构数 | 平均评分 | 标准差 | 最小值 | 最大值 |
|---|---:|---:|---:|---:|---:|
| `candidate_0043` | 3 | -9.1200 | 0.2516 | -9.28 | -8.83 |
| `candidate_0044` | 3 | -8.9433 | 0.1553 | -9.07 | -8.77 |
| `candidate_0082` | 3 | -9.1100 | 0.1375 | -9.23 | -8.96 |
| `candidate_0096` | 3 | -8.9733 | 0.2043 | -9.12 | -8.74 |
| `candidate_0173` | 3 | -8.9600 | 0.2427 | -9.16 | -8.69 |
| `candidate_0200` | 3 | -8.9700 | 0.0436 | -9.00 | -8.92 |

以上数据来自本阶段已记录的 PCANN 汇总结果。若要制作正式发布版数据表，应再次对照 `candidate_summary.csv` 检查完整精度和字段定义。

### 5.2 平均评分的比较

在这六个对象中，按数值从小到大排列，平均评分为：

1. `candidate_0043`：-9.1200
2. `candidate_0082`：-9.1100
3. `candidate_0096`：-8.9733
4. `candidate_0200`：-8.9700
5. `candidate_0173`：-8.9600
6. `candidate_0044`：-8.9433

这里的排序只表示 PCANN `avg` 字段在本批结构上的数值顺序。

`candidate_0043` 与 `candidate_0082` 的平均值仅相差 0.0100。这个差值很小，且当前每个候选只有三个预测结构，因此不应将二者描述为具有明确、稳定的生物学优劣关系。

此外，当前记录没有独立证明 PCANN 的 `avg` 数值越低就一定代表更强的真实结合亲和力。即使代码中后续将该数值传入类似能量的换算公式，也不能据此自动确定原始分数的物理单位或生物学含义。

因此，较稳妥的表述是：`candidate_0043` 与 `candidate_0082` 在本次 PCANN 评分中处于最靠前的位置，但二者的差异很小，且其生物学意义仍有待验证。

### 5.3 模型间波动

各候选的评分标准差如下：

- `candidate_0200`：0.0436
- `candidate_0082`：0.1375
- `candidate_0044`：0.1553
- `candidate_0096`：0.2043
- `candidate_0173`：0.2427
- `candidate_0043`：0.2516

在这组三结构结果中，`candidate_0200` 的评分标准差最低，说明它的 PCANN 分数在这三个输入结构之间相对稳定。

但这里的“稳定”只指本次三个结构对应的评分变化较小，不代表该候选的真实结合能力更强，也不证明 PCANN 对它的预测更准确。

相对而言，`candidate_0043` 和 `candidate_0173` 的评分波动较大。这提示在后续分析中，不能只查看候选平均值，也应保留单结构结果，检查不同预测构象是否带来了明显评分变化。

由于每个候选仅有三个结构，本阶段不将标准差用于推断统计显著性，也不将其当作真实实验不确定性的估计。

### 5.4 PCANN 结果能够支持什么

本阶段的 PCANN 结果可以支持以下判断：

1. 六个对象均获得了可供比较的结构级评分。
2. `candidate_0043` 与 `candidate_0082` 的平均评分在本批对象中最靠前。
3. `candidate_0200` 的三个结构评分相对集中。
4. 候选平均评分和结构间波动并不完全一致，因此应同时保留均值与离散程度。
5. PCANN 为 Boltz-2 结构评价增加了一类补充计算证据。

但这些结果不能独立支持以下结论：

- `candidate_0043` 已被证明具有最高的 GLP1R 结合亲和力。
- `candidate_0082` 与 `candidate_0043` 的微小评分差异具有显著生物学意义。
- `candidate_0200` 的评分稳定就意味着它在实验中更可靠。
- PCANN 的分数已经经过本项目的阳性、阴性对照正式校准。
- PCANN 分数已经能够准确预测 GLP1R 激动活性。

## 六、PCANN 输出与条件性 Kd 换算的边界

### 6.1 代码中使用的换算关系

本阶段检查了 PCANN 代码中与能量及 Kd 换算相关的部分。记录中的代码为：

```python
R = 1.987204258e-03
T = 298
dg = 
- `T = 298`
- `R × T ≈ 0.5922`

如果 `output.item()` 真正代表以 kcal/mol 为单位的标准结合自由能 $\Delta G^\circ$，那么可以在相应热力学定义和标准态约定下，使用：

$$
K_d \approx \exp\left(\frac{\Delta G^\circ}{RT}\right)
$$

进行换算，其中 $RT$ 约为 0.5922 kcal/mol。

但是，这一换算有一个关键前提：传入公式的模型输出必须具有相应的物理意义、单位和热力学定义。

当前记录并未充分证明 PCANN 原始 `avg` 输出就是标准结合自由能 $\Delta G^\circ$，也没有在现有材料中完整核实该输出的训练标签、标定方式、单位及其与实验 Kd 的对应关系。

因此，**不能仅凭代码把 PCANN 输出自动解释为真实结合自由能，也不能把由此换算得到的数值称为实验测得的 Kd。**

### 6.2 条件性换算结果

此前按照上述数值关系，曾对 PCANN 平均分数进行条件性换算，得到以下示例：

| 候选 | PCANN 平均评分 | 条件性换算值 |
|---|---:|---:|
| `candidate_0043` | -9.1200 | 约 205 nM |
| `candidate_0082` | -9.1100 | 约 208 nM |
| `candidate_0200` | -8.9700 | 约 264 nM |
| `candidate_0096` | -8.9733 | 约 263 nM |
| `candidate_0173` | -8.9600 | 约 269 nM |
| `candidate_0044` | -8.9433 | 约 276 nM |

这些数值应标记为“按特定能量假设计算的条件性换算值”，而不是“预测的真实 Kd”或“实验 Kd”。

这里还存在一个需要注意的现象：表中的条件性换算结果与 PCANN 平均评分的顺序具有数学上的关联，因为换算直接使用了这些评分值。它们并不是独立的第二套实验或计算证据，不能把“PCANN 排名靠前”和“换算后 Kd 更低”当作两条互相独立的证据来累加。

### 6.3 与已记录 SPR 数据的比较

项目记录中有以下参考肽的 SPR Kd 数值：

| 分子 | 记录中的 SPR Kd |
|---|---:|
| D13 | 8.58 µM |
| D41 | 5.19 µM |
| D44 | 6.78 µM |
| 司美格鲁肽（Semaglutide） | 2.78 µM |

这些数值是当前项目记录中的参考数据。正式发表或用于定量校准之前，仍应回查原始论文、实验方法及数据表，确认测量对象、分子形式、受体构建体、实验条件和数值单位是否一致。

如果暂时假设这些 SPR 数据与 PCANN 条件性换算值可以直接比较，那么两组数值会存在明显差距。例如，条件性换算值约 0.205–0.276 µM，而参考 SPR 数据约为 2.78–8.58 µM。

但在尚未确认 PCANN 输出的物理单位、模型标定方式和实验数据可比性之前，不能据此直接得出“PCANN 系统性高估亲和力”或“PCANN 的亲和力预测不准确”的定论。

正确的处理方式是把该差距记录为需要进一步核查的问题，而不是提前给出未经验证的解释。

### 6.4 后续需要核实的事项

如果要把 PCANN 评分正式用于亲和力预测，后续至少需要核查：

1. PCANN `avg` 字段的确切定义。
2. 该输出是否为物理能量、无量纲评分，或经过模型训练的其他指标。
3. 模型训练数据中使用的实验标签和单位。
4. 输出值与 Kd、pKd 或 $\Delta G^\circ$ 的映射关系。
5. 模型适用的蛋白、配体类型及结构输入条件。
6. 参考 SPR 数据的原始出处和实验可比性。
7. 是否存在足够的已知阳性、阴性或定量参考样本用于外部校准。

在这些问题得到回答之前，PCANN 最适合作为补充排序工具，而不是将模型分数转换成定量亲和力结论的依据。

## 七、与第十一阶段 Boltz-2 结构评价的联合解释

第十一阶段的目标是通过结构预测、参考结构比较和多指标筛选缩小候选范围；第十二阶段则在收窄后的候选上增加 PCANN 评分。

两阶段的结果可以联合参考，但不能混为同一类指标。

### 7.1 Boltz-2 结构评价提供的信息

第十一阶段使用的主要指标包括：

- `confidence_score`
- `ptm`
- `iptm`
- `complex_plddt`
- `complex_iplddt`
- `complex_pde`
- `complex_ipde`
- `protein_iptm`
- `tm_score`
- `rmsd_A`

这些指标分别涉及模型置信度、复合物预测信息、局部结构可信度、距离误差或与参考结构的相似性。

其中，受体 TM-score 和 RMSD 是通过与 PDB 7KI0 的受体结构比较得到的结构评价结果。它们不能直接解释为候选与受体的结合亲和力。

### 7.2 PCANN 提供的信息

PCANN 对六个对象对应的 18 个结构进行评分，提供了另一类计算结果。

在本批数据中：

- `candidate_0043` 的平均 PCANN 评分最低。
- `candidate_0082` 的平均评分紧随其后。
- `candidate_0200` 的三个结构评分波动最小。

这些观察可以用来调整后续候选的计算优先级，但当前没有独立证据证明 PCANN 的排序必然比 Boltz-2 结构指标更接近真实结合能力。

### 7.3 不应把不同指标直接相加

Boltz-2 指标和 PCANN 分数具有不同定义、量纲与计算来源。不能在没有明确归一化、权重设定和外部验证的情况下，把它们直接相加构造一个所谓的“总亲和力分数”。

如果未来希望建立综合排序规则，需要预先定义：

- 哪些指标进入综合排序；
- 每个指标的方向；
- 是否进行标准化；
- 各指标的权重如何确定；
- 如何处理同一预测结构上相互相关的指标；
- 如何使用已知参考样本评估排序的有效性；
- 如何报告对权重和阈值的敏感性。

本项目目前并未建立经过实验校准的综合亲和力评分模型，因此最终候选选择应描述为基于多类计算证据的优先级判断，而不是经过验证的定量预测。

## 八、最终候选集合的确定

### 8.1 最终优先研究的四条候选

结合此前的结构评价与本阶段 PCANN 结果，最终优先研究的候选集合为：

```fasta
>candidate_0082
HAEGTFTSDVSRYLEEKAVKQFVERLRRGGG
>candidate_009味着它们已通过实验验证。

### 8.2 `candidate_0044` 的定位

`candidate_0044` 曾进入第十一阶段的结构排序与后续 PCANN 评分，其序列为：

```fasta
>candidate_0044
HAEGTFTSDVSRYLEEKAVKAFVDRLKRGAG
```

它在此前两种结构指归档中应保留 `candidate_0044` 的历史评分与结构评价结果，但不能把它继续列入最终四条候选集合。

### 8.3 `candidate_0173` 的定位

`candidate_0173` 的序列为：

```fasta
>candidate_0173
HAEGTFTSDVSRYLEEKAVKDFVERLKRGAG
```

它对应此前记录中的基准，帮助观察新候选相对于既有序列的计算表现。

但是，计算基线与实验阳性对照是两个不同概念。虽然项目记录中存在 D44 的参考 SPR 数据，仍应根据实际序列、分子形式和实验条件确认二者的对应关系，不能只因编号关联就将 `candidate_0173` 当作已在本次计算流程中得到实验验证的阳性对照。

### 8.4 四条最终候选与基线的序列差异

相对于 `candidate_0173`，四条最终候选的差异如下：

| 候选 | 相对于 `candidate_0173` 的变化 | 序列一致性 |
|---|---|---:|
| `candidate_0082` | D21Q、K27R、A30G | 28/31 = 90.3% |
| `candidate_0096` | K17Q、D21A、E24D | 28/31 = 90.3% |
| `candidate_0200` | D21A、K27R、A30G | 28/31 = 90.3% |
| `candidate_0043` | K17Q、D21A、E24D、A30G | 27/31 = 87.1% |

这些变化提供了进一步分析序列—结构关系的基础。例如，后续可以比较这些替换对预测局部构象、界面接触和模型评分的影响。

但当前证据还不足以断定某一个替换提高了真实结合亲和力，更不能从序列相似性直接推断激动活性。

## 九、本阶段主要结论

本阶段完成了 PCANN 批处理调试、逐结构评分、候选级汇总以及评分解释边界的梳理。

主要结果如下：

1. 对六个候选或参照对象的三个 Boltz-2 结构分别开展 PCANN 评分，共处理 18 个结构。
2. 修复候选级汇总中的数值类型问题，确保相关字段在汇总前显式转换为数值类型并检查 NaN 与非有限值。
3. 成功生成 `pcann_raw_18_structures.csv`、`candidate_summary.csv` 和 `structure_checks.csv`。
4. 在六个对象中，`candidate_0043` 与 `candidate_0082` 的 PCANN 平均评分最靠前，分别为 -9.1200 和 -9.1100。
5. `candidate_0200` 的三个结构评分标准差最低，为 0.0436，说明本次三个结构之间的评分相对集中。
6. 对 PCANN 分数与条件性 Kd 换算之间的关系进行了审查，明确了该换算依赖模型输出具有正确的物理意义和单位。
7. 将 PCANN 评分作为补充计算证据，与此前 Boltz-2 结构评价区分使用。
8. 最终优先研究的四条候选为 `candidate_0082`、`candidate_0096`、`candidate_0200` 和 `candidate_0043`。
9. `candidate_0044` 保留为已分析的中间候选，`candidate_0173` 保留为计算比较基线。

本阶段最重要的产出不是获得了可直接用于实验报告的 Kd 数值，而是把 PCANN 的结构评分纳入候选优选流程，同时明确了数据处理、模型输出解释与实验验证之间的界限。

## 十、仍未解决的问题

本阶段结束时，仍有以下事项需要保留为未解决问题：

1. PCANN `avg` 字段的精确科学定义、单位及其与实验亲和力的映射关系，需要依据软件实现和相关文档进一步核查。
2. PCANN 的条件性 Kd 换算不能当作实验 Kd，也不能在缺乏校准时视为可靠的定量亲和力预测。
3. 当前每个对象仅有三个结构，模型间标准差的解释能力有限。
4. `candidate_0043` 与 `candidate_0082` 的平均 PCANN 评分差仅为 0.0100，不足以单凭该差值判定真实生物学优劣。
5. 参考 SPR 数据的原始出处、实验条件与本项目候选的可比性仍应进一步确认。
6. 本项目目前没有湿实验数据证明四条最终候选的结合能力、亲和力或激动活性。
7. 如果要把结构指标和 PCANN 分数整合成统一排序，需要明确指标方向、权重、阈值和外部校准方案。

因此，本阶段的结论应保持在计算证据所能支持的范围内：PCANN 为候选优选提供了补充评分，但尚未建立经过实验验证的亲和力预测体系。

---

# GLP1R 项目总结：从参考结构分析、候选肽设计到计算评价与最终优选

## 一、项目概况

### 1.1 项目名称

建议归档名称：

**GLP1R De Novo Peptide Design and Computational Evaluation**

中文名称：

**GLP1R 候选肽的从头设计、结构预测与计算评价**

项目核心对象为胰高血糖素样肽-1 受体（GLP-1 receptor，GLP1R），核心任务是以司美格鲁肽及相关已知肽序列为参考，开展候选肽序列生成、序列筛选、结构预测和多指标计算评价，形成后续值得进一步研究的候选集合。

### 1.2 项目工作目录与环境

项目早期主要目录：

`LOCAL_PATH

后期 Boltz-2 与 PCANN 工作目录：

`LOCAL_PATH

涉及的软件与环境包括：

- ProteinMPNN：`v_48_020`，早期 Conda 环境 `proteinmpnn`。
- ColabFold：记录版本为 1.6.3，使用 Conda 环境 `colabfold`。
- Boltz-2：Conda 环境 `boltz`。
- PCANN：代码目录 `LOCAL_PATH 环境 `pcann`。
- US-align：用于预测受体结构与参考受体结构的比对。
- Biopython：用于结构处理、结构对齐和相关分析。

需要注意，项目经历了目录和分析流程的演变。`GLP1R_reproduction` 中的早期序列生成、去重和筛选，与 `GLP1R_Boltz2_20261022` 中的结构评价、PCANN 分析属于同一项目的不同阶段，但不能因为目录相同或候选名称相似，就把不同版本的数据直接合并。

### 1.3 项目目标

项目的实际目标包括：

1. 从已知 GLP1R 配体及参考结构出发，整理受体和肽链的结构、序列信息。
2. 建立可以用于 ProteinMPNN 设计的受体—肽复合物输入。
3. 生成大量候选肽序列，并检查固定位置和序列约束。
4. 通过去重、序列规则、理化性质等方法缩小候选空间。
5. 使用结构预测工具检查候选与 GLP1R 组成复合物时的预测表现。
6. 通过参考结构比对和多指标评价筛选候选。
7. 进一步使用 PCANN 对部分预测结构评分。
8. 形成可追溯的候选优先级与后续研究名单。

项目目前的完成范围是计算设计与计算评价。由于尚无本项目新候选的湿实验验证结果，不能将最终候选描述为已经验证的 GLP1R 激动剂或已测得特定亲和力的分子。

## 二、项目总体技术路线

项目经历的总体技术路线可以概括为：

参考配体与受体结构准备

→ 受体—肽复合物结构整理

→ ProteinMPNN 输入构建

→ 候选序列生成

→ 去重与序列筛选

→ 候选池整理

→ 结构预测工具测试与流程排查

→ Boltz-2 复合物结构预测

→ 与 7KI0 参考受体结构比较

→ 候选级多指标汇总与筛选

→ PCANN 补充评分

→ 最终候选优先级确定

→ 后续实验验证需求与未解决问题整理

这一流程的重点不在于某个工具产生了多少分数，而在于将不同阶段的输出组织成有明确来源、能够追溯、可以解释局限的证据链。

需要强调：上面是项目的整体逻辑，不代表每个分支都已经形成完全统一、从输入到输出全部经过端到端验证的自动化流水线。尤其是早期的不同序列筛选路径，以及 ColabFold 模板测试和正式批量预测之间的衔接，仍有未解决的记录问题。

## 三、第一阶段：参考结构和序列准备

### 3.1 参考结构 PDB 7KI0

项目选择 PDB `7KI0` 作为司美格鲁肽与 GLP1R 复合物的主要参考结构。

记录的结构信息：

- PDB：`7KI0`
- 结构分辨率：2.50 Å
- Chain P：司美格鲁肽肽链
- Chain R：GLP1R 受体链

早期使用的主要文件包括：

- `structures/7KI0.cif`
- `structures/semaglutide_7KI0_chainP.pdb`
- `structures/GLP1R_7KI0_chainR.pdb`
- `structures/semaglutide_peptide_only_7KI0.pdb`
- `data/semaglutide_7KI0_chainP.fasta`
- `data/GLP1R_7KI0_chainR.fasta`
- `results/GLP1R_7KI0_residue_mapping.csv`
- `scripts/map_glp1r_pdb_to_fasta.py`

这些文件分别用于保存原始结构、提取链结构、肽链处理、序列记录及受体残基编号映射。

### 3.2 司美格鲁肽序列与结构中的缺失残基

项目使用的司美格鲁肽理论聚合物序列为 31 aa：

`HAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG`

但在参考结构中，末端 Gly 第 31 位没有对应的坐标，因此结构中实际可用于几何分析的标准化肽链长度为 30 个坐标支持的残基。

这带来一个必须保留的区分：

- 序列比较通常以完整的 31 aa 序列为基础。
- 结构接触和几何分析使用具有坐标的 30 个残基。
- 不能把没有坐标的末端残基当成已经在参考结构中观测到。
- 后续设计序列若补回末端 Gly，需要明确这是序列层面的处理，而非从原始坐标直接获得的结构信息。

此外，司美格鲁肽第 2 位存在非天然氨基酸 AIB。为满足 ProteinMPNN 的标准氨基酸输入要求，早期构建的模型输入副本中将该位置表示为 Ala；原始结构文件则保留原有信息。

这只是为模型输入做的表示处理，不意味着 AIB 在化学性质上等同于 Ala。

### 3.3 受体链序列映射

GLP1R Chain R 的构建体 FASTA 长度记录为 491 aa，但参考结构中仅有部分残基具有坐标。

记录的结构残基区间包括：

- 29–129：101 个残基
- 137–339：203 个残基
- 344–423：80 个残基

合计 384 个标准残基。

早期映射结果显示：

- 结构中 384/384 个标准残基可以映射到对应 FASTA 位置。
- 0 个氨基酸不匹配。
- PDB Chain R 的残基 29 对应 FASTA 位置 38。
- PDB Chain R 的残基 423 对应 FASTA 位置 432。

这说明已存在坐标的受体残基可以与所用构建体序列进行一致映射，但不能据此认为结构中缺失的受体区域已经被建模。

## 四、第二阶段：参考配体—受体界面分析

### 4.1 分析目标

在生成候选肽之前，项目先分析参考结构中司美格鲁肽与 GLP1R 的空间接触关系，为后续设计和结果解释提供几何参照。

主要脚本：

- `scripts/analyze_glp1r_interface.py`
- `scripts/analyze_interface_atom_pairs.py`

受体结构文件：

`structures/GLP1R_7KI0_chainR.pdb`

肽链结构文件：

`structures/semaglutide_peptide_only_7KI0.pdb`

### 4.2 输入结构统计

记录中的输入统计为：

- GLP1R：384 个残基，3,175 个重原子。
- 司美格鲁肽肽链：30 个残基，236 个重原子。

界面分析排除氢和氘原子，保留 AIB，但不将与肽链主体分离的 WF1 相关部分纳入 peptide-only 结构。

此前对原始肽链文件与 peptide-only 文件进行了坐标核对：

- 原始链文件有 31 个残基记录、256 个原子。
- peptide-only 文件有 30 个残基、236 个原子。
- 两份文件共有的 236 个原子坐标完全一致，最大坐标差为 0。
- 原始文件中多出的 20 个原子属于 WF1。

这项检查证明了两个提取结果中共有原子的坐标一致，但不能据此宣称整个 mmCIF 到 PDB 的转换过程已经得到独立、全面的验证。

### 4.3 接触统计

在重原子距离阈值下得到的记录为：

| 距离阈值 | 原子对数量 | 不同残基对数量 | 参与接触的肽链残基数 | 参与接触的受体残基数 |
|---|---:|---:|---:|---:|
| 4 Å | 196 | 60 | 24 | 40 |
| 5 Å | 832 | 108 | 28 | 49 |

主要输出文件包括：

- `results/GLP1R_semaglutide_contacts_4A.csv`
- `results/GLP1R_semaglutide_contacts_5A.csv`
- `results/GLP1R_semaglutide_peptide_summary_4A.csv`
- `results/GLP1R_semaglutide_peptide_summary_5A.csv`
- `results/GLP1R_semaglutide_nearest_atom_pairs_4A.csv`

其中最近原子对文件记录了 22 个代表性原子对。

记录中的部分最近距离包括：

- 肽链 Glu3—受体 Arg199：2.691 Å。
- 肽链 Glu3—受体 Tyr161：2.580 Å。
- 肽链 Glu15—受体 Arg308：2.870 Å。
- 肽链 Glu15—受体 Ser40：3.031 Å。

这些距离可以描述原子在参考结构中的空间邻近关系，但仅凭距离不能直接证明氢键、盐桥或某种相互作用对激动活性具有因果作用。更严格的化学相互作用判断还需要考虑原子类型、几何角度、质子化状态、结构环境及其他证据。

### 4.4 本阶段的意义与限制

本阶段为后续设计提供了参考结构、残基映射和界面几何数据。

它能够支持：

- 对参考肽的空间接触情况进行定量描述。
- 为后续结构比对提供固定参考。
- 帮助检查输入结构是否存在明显的链和残基处理问题。

它不能直接支持：

- 真实结合自由能的定量估计。
- 实验 Kd 的计算。
- 某个残基必然是激动活性关键位点的因果结论。
- 新设计序列已经具备与司美格鲁肽相同的药理作用。

## 五、第三阶段：ProteinMPNN 输入准备与小规模测试

### 5.1 工具与模型

早期 ProteinMPNN 代码目录：

`USER_HOME/ProteinMPNN`

Conda 环境：

`proteinmpnn`

使用模型：

`v_48_020`

主要任务是固定受体结构和部分肽链残基，对肽链可设计位置进行序列设计。

### 5.2 链与残基处理

项目建立了以下输入文件：

- `structures/GLP1R_semaglutide_ProteinMPNN_input.pdb`
- `structures/GLP1R_semaglutide_ProteinMPNN_input_renumbered.pdb`
- `results/proteinmpnn/input/...`
- `parsed_chains.jsonl`
- `fixed_positions.jsonl`

设计链为 Chain P，受体 Chain R 固定。

早期设计设置中，固定位置记录为：

`[1,2,3,4,5,6,7,8,9,11,20,28]`

对应残基为：

`H,A,E,G,T,F,T,S,D,S,K,R`

这里有一个需要保留的复现限制：参考文献补充材料中的固定残基描述与可直接从当前坐标使用的位置并不完全一致。文献记录涉及 12 个固定残基，但其中包括结构中没有坐标支持的末端 Gly；项目实际使用的是坐标范围内的 12 个位置。因此，不能把当前配置直接描述为已经精确复现原作者的全部设计约束。

### 5.3 受体残基编号问题

初始 ProteinMPNN 解析中，受体链因不连续 PDB 残基编号产生 11 个 gap token：

- 缺失 130–136：7 个位置。
- 缺失 340–343：4 个位置。

随后将受体结构链重新编号为连续的 1–384，且不改变坐标。重新解析后：

- 受体链：384 aa，无 gap。
- 肽链：30 aa，无 gap。

这一修正是为避免结构文件编号不连续导致模型输入出现不必要的空位。

### 5.4 两条序列测试

早期小规模测试生成了两条 30 aa 候选：

`HAEGTFTSDVSRYLEEKAVKAFVERLKRGA`

`HAEGTFTSDVSRYLEEKAAKEFVERLKRGS`

两条序列均通过当时设定的 12 个固定位置检查。

该测试证明了输入结构和小规模序列设计流程能够运行，但只有两条输出，不足以评估候选的多样性、生成分布或生物学表现。

## 六、第四阶段：ProteinMPNN 大规模序列生成与评分审计

### 6.1 生成设置与规模

项目随后开展大规模 ProteinMPNN 生成：

- 模型：`v_48_020`
- 设计链：Chain P
- 固定链：Chain R
- 设计温度：0.1
- 批次：50 批
- 每批生成候选：200 条
- 随机种子：1–50

对应目录：

`results/proteinmpnn/test_2000seq_renumbered/batch200_seed1`

至：

`results/proteinmpnn/test_2000seq_renumbered/batch200_seed50`

每个批次 FASTA 记录包含一个参考序列和 200 条生成候选，因此不能直接把每个文件的记录行数当成纯候选数。

根据现有记录，共得到 10,000 条候选记录。所有记录中的设计序列均为 30 aa 标准氨基酸序列，固定位置检查没有发现失败记录。

原始完整命令后来未能从历史 shell 记录中找回，因此参数记录可以作为当前恢复的运行档案，但若需要完全复现，仍应尽可能从原始日志、脚本或环境记录恢复完整命令。

### 6.2 去重结果

10,000 条候选记录去重后得到：

- 唯一序列：1,435 条。
- 重复记录：8,565 条。
- 重复比例：85.65%。
- 在至少出现两次的唯一序列中：603 条。
- 只出现一次的唯一序列：832 条。

主要文件：

- `results/proteinmpnn/test_2000seq_renumbered/deduplicated/unique_candidates_all50_v2.fasta`
- `results/proteinmpnn/test_2000seq_renumbered/deduplicated/sequence_counts_all50_v2.csv`

计数 CSV 的记录数合计为 10,000。

这说明在本次设置下，生成记录中存在较高的序列重复率。重复率可以帮助了解采样是否集中于少数序列，但不等于模型已经找到真实结合肽，也不能将高频序列直接解释为高活性候选。

### 6.3 高频序列

记录中的前十条高频序列如下：

| 序列 | 出现次数 |
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

### 6.4 ProteinMPNN 分数的含义

项目还审计了 ProteinMPNN 输出中的 `score`、`global_score` 和 `seq_recovery`。

当时的代码检查显示：

- `score` 是在设计链 P 的设计位置上计算的平均 masked negative log probability。
- `global_score` 使用的是结构中有效位置的整体 mask，包含受体和肽链，不应简单视为肽链专属评分。
- `seq_recovery` 表示设计区域中与参考序列相同的位置比例。

在 10,000 条候选记录上，统计结果为：

| 指标 | 最小值 | 第一四分位数 | 中位数 | 第三四分位数 | 最大值 | 平均值 |
|---|---:|---:|---:|---:|---:|---:|
| `score` | 1.0111 | 1.0766 | 1.0952 | 1.1156 | 1.2677 | 1.0975 |
| `global_score` | 1.8847 | 1.9210 | 1.9286 | 1.9360 | 1.9743 | 1.9284 |
| `seq_recovery` | 0.2778 | 0.5000 | 0.5556 | 0.5556 | 0.7222 | 0.5267 |

这些统计是按生成记录计算的，不是按唯一序列计算的；同一条序列在不同采样记录中可能对应不同评分。

### 6.5 频次与评分的关系

补充分析中，唯一序列的出现频次与平均 ProteinMPNN `score` 呈负相关：

- 唯一序列数：1,435。
- 重复序列数：603。
- 至少出现在 5 个种子中的序列：260 条。
- 至少出现在 10 个种子中的序列：147 条。
- 序列出现频次与平均 `score` 的 Spearman 相关系数：-0.5156。
- 跨种子数量与平均 `score` 的 Spearman 相关系数：-0.5155。

最高频序列出现 636 次，覆盖 50 个种子，平均 `score` 为 1.0702，中位数为 1.0694，标准差为 0.0187。

603 条重复序列中，单序列评分标准差的中位数为 0.0176，其中 184 条标准差超过 0.02。

这些结果说明，模型采样频次与模型自身的序列概率评分存在一定关系，但当前记录没有给出相关分析的 p 值、置信区间或稳健性分析。因此应将其描述为探索性统计，而不是经过完整统计检验的结论。

最重要的是：ProteinMPNN 评分衡量的是模型对序列的偏好或概率特征，并不是实验结合亲和力。

## 七、第五阶段：早期序列筛选、理化性质分析与聚类

本项目的早期序列筛选经历了不同版本和不同目标的分析路径。归档时必须将这些路径分别记录，不能将所有数字拼成一条看似连续的筛选链。

### 7.1 早期筛选路径 A：1,435 条序列至 308 条候选

在一条早期筛选路径中：

- 输入：1,435 条去重序列。
- 第一步：1,435 → 787。
- 第二步：787 → 308。

第一步涉及 EF、WL 等序列约束；第二步涉及 DV、SY、YL、EF、FI、WL 等 motif 规则。

记录中明确指出，这一版本允许位置 9–10 出现 DV，但会剔除其他指定位置的某些 motif。该规则与“严格复现参考文献中所有约束”的目标并不完全等同，尤其是 DV 的处理方式仍需要进一步核查。

该路径中，308 条序列均为 30 aa 标准氨基酸序列且互不重复。DV motif 出现于 308/308 条序列，其他被检查的排除 motif 均为 0/308。

这里的 308 条候选属于一条独立的筛选版本，不能直接与后来得到的 240 条序列合并。

### 7.2 早期理化性质分析

在 787 条序列上，使用近似 Henderson–Hasselbalch 方法估计 pH 7.4 时的净电荷，并使用 Kyte–Doolittle（KD）疏水性尺度分析平均疏水性。

净电荷统计：

- 平均值：+0.752。
- 中位数：+0.836。
- 最小值：-2.161。
- 最大值：+3.835。
- 电荷处于 -1 到 +2 的序列：741/787。

平均 KD 疏水性统计：

- 平均值：-0.808。
- 中位数：-0.8067。
- 第一四分位数：-0.9367。
- 第三四分位数：-0.6850。
- 最小值：-1.2767。
- 最大值：-0.1967。

局部疏水性检查显示：

- 连续 KD 大于 0 的最长区段为 4 aa，共有 7 条序列达到该长度。
- 没有序列存在连续 5 aa 或更长的 KD 大于 0 区段。
- 79 条序列至少存在一个 7-aa 窗口，其平均 KD 大于 1。
- 最高的 7-aa 窗口均值为 1.8143，对应片段 `AVKAFVA`，位于位置 18–24。

这些指标只是基于序列的疏水性代理分析，不能等同于实验测得的表面疏水性、溶解性、聚集性或 SAP。

### 7.3 308 条序列的多样性聚类

对 308 条候选进行了两两 Hamming 距离分析，共有 47,278 个候选对。

记录的距离分布为：

| Hamming 距离 | 候选对数 |
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

距离不超过 3 的候选对为 12,118 对；距离不超过 5 的候选对为 36,518 对；最大 Hamming 距离为 11。

单链接聚类在 Hamming 距离阈值 3 下产生一个包含 307 条序列的大连通分量，以及一个单独分量，因此不适合用于代表序列压缩。

随后使用确定性的凝聚式层次聚类与 complete linkage，设置 Hamming 距离切割阈值为 3，并从每个簇中选择 medoid。medoid 平局时按原始输入顺序决定。

最终结果：

- 输入序列：308 条。
- 聚类数量：65 个。
- 合并次数：243 次。
- 最大簇大小：12。
- 单例簇：7 个。
- 最大簇直径：3。
- 代表序列：65 条。

簇大小分布记录为：

`{1:7, 2:5, 3:18, 4:8, 5:5, 6:5, 7:3, 8:5, 9:3, 10:5, 12:1}`

输出目录：

`results/proteinmpnn/test_2000seq_renumbered/clustering_complete_linkage_d3/`

主要文件：

- `cluster_complete_linkage.py`
- `medoids.fasta`
- `cluster_membership.tsv`
- `cluster_summary.tsv`
- `clustering_run_info.md`

输入 FASTA 的 SHA256：

`e09aaf1f54d036f62f9168e26454abcbff43f21b2977ba7150b4563dce4992f2`

记录中的六项内部审计全部通过，包括输入数量、每条序列被分配一次、簇直径限制、medoid 属于簇成员、medoid 距离和最小性以及代表序列唯一性。

这些检查说明聚类结果在算法与数据组织上满足指定规则，但不能证明聚类代表具有更高生物学活性。

### 7.4 早期筛选路径 B：1,435 条序列至 240 条候选

另一条筛选路径采用八步序列筛选，记录的数量变化为：

**1,435 → 787 → 426 → 425 → 381 → 347 → 330 → 256 → 240**

各步骤如下：

| 步骤 | 规则概要 | 输入数 | 保留数 | 移除数 |
|---|---|---:|---:|---:|
| 1 | EF/WL 相关约束 | 1,435 | 787 | 648 |
| 2 | N 端前 15 位约束，位置 12 设例外 | 787 | 426 | 361 |
| 3 | C 端锚点约束 | 426 | 425 | 1 |
| 4 | 位置 19–23 的疏水性约束 | 425 | 381 | 44 |
| 5 | 指定位置氨基酸约束 | 381 | 347 | 34 |
| 6 | 净电荷绝对值不超过 2 | 347 | 330 | 17 |
| 7 | 电荷范围约束 | 330 | 256 | 74 |
| 8 | GRAVY KD 不低于 -1.1 | 256 | 240 | 16 |

各步骤目录记录为：

- `screening_step1_EF_WL_v1`
- `screening_step2_Nterm15_except12_v1`
- `screening_step3_Cterm_anchors_v1`
- `screening_step4_hydrophobic_19_23_v1`
- `screening_step5_residue_exclusions_v1`
- `screening_step6_abs_charge_le_2_v1`
- `screening_step7_charge_range_semaglutide_to_plus1_v1`
- `screening_step8_gravy_kd_ge_minus1_1_v1`

第五步的规则包括：

- 位置 12 允许 A/E/Q。
- 位置 16 要求 A。
- 位置 17 允许 A/E。
- 位置 24 要求 A。
- 位置 27 允许 I/V。

第六步规则：

`abs(net_charge_pH7.4) <= 2`

输入 SHA256：

`115e943738018c356dd5c727387041201d07dbc4340e87833f5fc5255321a94d`

第七步使用的电荷范围为约 -1.1634 至 +1.0，边界包含端点。330 条输入中有 12 条低于下界、62 条高于上界，最终保留 256 条。

输入 SHA256：

`2990f75e207d333a8975cceed4229c18dee0b1625815049fb50be3d56089160d`

第八步使用 GRAVY KD ≥ -1.1，保留 240 条，移除 16 条。

输入 SHA256：

`46cdf744d12202c9c1c29558c05b71581566fc629ffc8bf70679540449d04c0c`

以上三个步骤记录的理化性质文件 SHA256 均为：

`009c838ada398a59ff894782f29223293db6a5eb487094cdf7df93dd2f227be7`

该路径中，净电荷按 pH 7.4、未修饰 N/C 端等假设进行近似计算；候选长度为 30 aa，参考肽为 31 aa。GRAVY KD 采用平均残基疏水性计算。

参考肽理化性质记录为：

| 分子 | 估计净电荷 | GRAVY KD | KD 正值残基数 | AVILMFWY 残基数 |
|---|---:|---:|---:|---:|
| Semaglutide | -1.163405 | -0.254839 | 11/31 | 13/31 |
| D13 | -0.163706 | -0.741935 | 10/31 | 11/31 |
| D41 | -0.163706 | -1.006452 | 8/31 | 9/31 |
| D44 | -0.164184 | -0.764516 | 10/31 | 11/31 |

347 条候选在第六步之前的理化性质统计为：

- 电荷均值：+0.7549。
- 电荷中位数：+0.8355。
- 最小电荷：-1.1644。
- 最大电荷：+3.8350。
- 正电荷序列：234 条。
- 负电荷序列：113 条。
- 绝对电荷小于 0.5 的序列：101 条。
- GRAVY 均值：-0.8767。
- GRAVY 中位数：-0.8633。
- GRAVY 最小值：-1.2767。
- GRAVY 最大值：-0.4600。

这里的阈值属于项目当前使用的操作性序列筛选规则，不应描述为已经通过实验校准的普适生物学阈值。

### 7.5 两条筛选路径不能混为一条

这一点对整个项目总结非常重要。

早期存在至少两条独立的筛选与压缩路径：

- 路径 A：1,435 → 787 → 308 → 65 个聚类代表。
- 路径 B：1,435 → 787 → 426 → 425 → 381 → 347 → 330 → 256 → 240。

两条路径的规则、目标和输出不同。65 条是对 308 条序列进行聚类后的代表序列；240 条则是另一套八步筛选规则的最终保留序列。

因此不能将 65 条与 240 条直接相加，也不能把它们描述为同一条线性筛选流程中的相邻阶段。

此外，项目早期记录中出现过 1,443 条和 1,435 条唯一序列两个数字。目前实际去重文件被检查为 1,435 条，但 1,443 与 1,435 的差异原因尚未完全查明。正式归档时应将 1,435 作为有明确文件依据的输入数量，同时保留早期文档曾出现 1,443 的事实，并将差异列为待核查项。

## 八、第六阶段：候选池整理与 ColabFold 模板测试

### 8.1 候选池版本

后续候选池整理发生在远程 HPC 环境中，项目目录为：

`~/projects/GLP1R_reproduction`

使用 ColabFold 1.6.3，Conda 环境为 `colabfold`。

记录中的候选输入文件：

`input/combined_pool.fasta`

该文件包含 241 条唯一序列，均为 31 aa。

SHA256：

`7a3ed3e906700768f049d93085d32f69b635f309e3769c8991e8180cca08b7a3`

这一 241 条候选池是后续整理形成的另一个版本。它与早期 240 条筛选集并不完全相同，原因涉及候选池合并及参考序列加入等处理。正式总结不能把它直接称为“240 条筛选集原样输入”。

### 8.2 参考序列合并与长度标准化

早期 ProteinMPNN 候选序列为 30 aa，而 D13、D41、D44 参考序列为 31 aa，末端多一个 Gly。

第一次去重未能识别长度不同但标准化后相同的序列。随后对所有 30 aa 序列临时追加末端 Gly，再进行比较：

- D13 与现有 `unique_0945` 匹配。
- D44 与现有 `unique_0989` 匹配。
- D41 未发现对应重复，因此保留。

此处追加 Gly 是为统一比较条件而进行的标准化，不代表原始 30 aa 序列本身已经包含该残基。归档时应同时保留原始序列和标准化比较序列，避免把比较用序列当成最初生成的原始序列。

此外，司美格鲁肽是已知配体参考，不属于上述 241 条候选池。

### 8.3 ColabFold 模板测试

项目检查了 `7KI0` 相关结构，并生成受体 Chain R 与肽链 Chain P 的参考复合物 CIF：

- `input/templates/7KI0.cif`
- `input/templates/GLP1R_semaglutide_reference.cif`

原始 `7KI0.cif` 大小约 994,709 bytes，准备后的参考文件约 269,460 bytes。

检查表明：

- BioPython 能够重新读取准备后的 CIF。
- 参考文件包含受体 R 与肽链 P。
- 肽链中存在非标准残基 AIB。
- 文件中存在两条链，并不意味着 ColabFold 一定会将它们作为一个完整配对模板使用。

ColabFold 参数检查涉及：

- `--templates`
- `--custom-template-path`
- `--custom-template-cache-path`

其中，`--custom-template-path` 接受的是目录，而不是直接传入单个 CIF 文件路径，并需要与相应模板选项配合使用。

在本地模板特征测试中，得到：

- `positions` 形状为 `(31,37,3)`。
- `mask` 形状为 `(31,37)`。
- 模板序列为 `HXEGTFTSDVSSYLEGQAAKEFIAWLVRGRG`。
- domain 为 `7ki0_P`。
- 测试记录显示 `Error: None`。

这说明在该测试路径下成功生成了肽链相关的模板特征，但不能证明 HHsearch 已经成功检索到该模板，更不能证明正式预测时使用了完整的受体—肽配对模板。

此前还检查了部分模板相关文件，但未找到完整的 `pdb70_hhm`，且 `command -v hhsearch`、`hhmake`、`kalign` 未返回可执行文件路径。仅凭这些现象不能确定模板检索失败的具体原因。

### 8.4 正式 ColabFold 批量预测的状态

历史 shell 搜索没有找到足以确认 241 条候选正式批量预测命令及完整参数的记录。

因此，本阶段能够确认的工作包括：

- 候选池整理。
- ColabFold 1.6.3 环境检查。
- 模板相关参数检查。
- 参考 CIF 准备。
- 局部肽链模板特征生成测试。
- 对模板检索和完整复合物模板行为的排查。

但现有记录不足以确认 241 条候选的正式 ColabFold 批量预测全部完成，也不足以证明该批预测已经按预想使用了完整配对模板。

这是项目可复现性方面的重要未解决项，不能为了让流程看起来完整而补写成已成功完成的批量预测。

## 九、第十一阶段：Boltz-2 结构预测与候选筛选

### 9.1 运行规模与参数

项目后期在以下目录开展 Boltz-2 分析：

`LOCAL_PATH

环境：

`boltz`

预测对象为 27 条候选肽与 GLP1R 的复合物，每条候选设置 3 次扩散采样，计划规模为 81 个模型结果。

记录的参数为：

| 参数 | 设置 |
|---|---|
| `diffusion_samples` | 3 |
| `seed` | 3 |
| `recycling_steps` | 3 |
| `sampling_steps` | 200 |
| `step_scale` | 1.5 |
| `max_parallel_samples` | 1 |
| 受体 MSA | 本地 GLP1R MSA |
| 候选肽 MSA | `empty` |

这些参数来自当前可恢复的历史记录。由于未附完整原始命令行和配置文件，正式归档仍应以实际运行日志为准。

### 9.2 模型级指标

记录中提取的指标包括：

- `confidence_score`
- `ptm`
- `iptm`
- `complex_plddt`
- `complex_iplddt`
- `complex_pde`
- `complex_ipde`
- `protein_iptm`
- `tm_score`
- `rmsd_A`

逐模型数据与候选级统计分开保存，主要文件包括：

- `boltz_sample_metrics.csv`
- `boltz_candidate_summary.csv`
- `audit/structure/per_model_structure_metrics.csv`
- `audit/structure/receptor_tmscore_vs_7KI0.csv`
- `audit/structure/candidate_27_three_model_means.csv`
- `audit/structure/candidate_27_filter_vs_0173.csv`
- `audit/structure/candidate_retained_vs_0173.csv`
- `audit/structure/candidate_retained_vs_0173_removed.csv`

参考肽的 Boltz-2 结果则单独保存至 `semaglutide_reference_metrics.csv`，相关 NPZ 文件位于 `predictions/semaglutide_glp1r_reference/`。

### 9.3 受体结构比对

使用 US-align 比较预测结构的 GLP1R Chain A 与参考 PDB `7KI0` 的 Chain R。

记录的受体 TM-score 大致范围为 0.6782–0.7877。

部分候选的候选级结果：

- `candidate_0082`：约 0.7877。
- `candidate_0213`：约 0.7806。
- `candidate_0096`：约 0.7782。
- `candidate_0081`：约 0.6782。
- `candidate_0111`：约 0.6877。

这里的 TM-score 用于比较受体结构与参考结构的一致性，不是肽链结合亲和力分数。

### 9.4 三指标与五指标排序

三指标 Top 8 记录为：

1. `candidate_0096`
2. `candidate_0082`
3. `candidate_0043`
4. `candidate_0200`
5. `candidate_0111`
6. `candidate_0175`
7. `candidate_0044`
8. `candidate_0173`

五指标 Top 8 记录为：

1. `candidate_0082`
2. `candidate_0096`
3. `candidate_0200`
4. `candidate_0170`
5. `candidate_0173`
6. `candidate_0043`
7. `candidate_0044`
8. `candidate_0112`

五指标表中的部分数据如下：

| 候选 | 平均 TM-score | 平均 RMSD (Å) | TM-score 标准差 | 平均 complex pLDDT | 平均 complex ipDE |
|---|---:|---:|---:|---:|---:|
| `candidate_0082` | 0.78772 | 3.73 | 0.01413 | 0.814995 | 0.735100 |
| `candidate_0096` | 0.77824 | 3.98 | 0.00464 | 0.798158 | 0.772982 |
| `candidate_0200` | 0.76360 | 3.98 | 0.01727 | 0.809582 | 0.841012 |
| `candidate_0170` | 0.76059 | 4.02 | 0.00893 | 0.822592 | 0.933972 |
| `candidate_0173` | 0.75946 | 4.00 | 0.01306 | 0.804936 | 1.062791 |
| `candidate_0043` | 0.77650 | 3.98 | 0.01757 | 0.793486 | 0.980332 |
| `candidate_0044` | 0.77325 | 4.10 | 0.00788 | 0.799851 | 0.972089 |
| `candidate_0112` | 0.77090 | 4.13 | 0.00873 | 0.803045 | 0.939019 |

三指标和五指标排序不完全一致，说明候选排序依赖所选指标和具体排序规则。`complex_ipDE` 的解释方向需要结合相应软件版本的定义，不应在未核实前自行解释为越高越好或越低越好。

### 9.5 五指标严格筛选

记录中有 20 条候选进入这一轮严格筛选。当前资料没有完整说明从 27 条缩小到 20 条的全部规则，因此不能补写未知的纳入原因。

剔除条件为：

- `rmsd_A_mean > 3.9`
- `tm_score_mean < 0.77`
- `iptm_mean < 0.9`
- `complex_plddt_mean < 0.79`
- `confidence_score_mean < 0.8`

其中 `candidate_0173` 被指定为基线候选，作为参照保留，不直接按这套规则剔除。

记录中的筛选结果：

- 进入筛选：20 条。
- 最终保留：2 条。
- 剔除：18 条。
- 除基线豁免外，`candidate_0082` 是记录中唯一同时满足五项阈值的候选。

各剔除条件的触发数：

| 条件 | 触发数量 |
|---|---:|
| RMSD > 3.9 Å | 14 |
| TM-score < 0.77 | 11 |
| ipTM < 0.9 | 6 |
| complex pLDDT < 0.79 | 6 |
| confidence score < 0.8 | 3 |

这些条件可能同时触发，因此触发数不能直接相加作为不同候选的总数。

这些阈值是项目中使用的操作性筛选标准，当前没有证据证明它们已经由实验阳性、阴性或定量亲和力数据正式校准。

### 9.6 第十一阶段的最终五条候选与后续变化

第十一阶段确定的五条候选为：

- `candidate_0082`
- `candidate_0096`
- `candidate_0200`
- `candidate_0043`
- `candidate_0044`

当时它们被作为后续分析对象，但这并不是最终项目候选名单。第十二阶段及后续整体整理后，最终优先研究的四条候选调整为：

- `candidate_0082`
- `candidate_0096`
- `candidate_0200`
- `candidate_0043`

因此，`candidate_0044` 应保留为已经经过结构评价和 PCANN 评分的中间候选，而不能继续放在最终四条候选名单中。

## 十、参考司美格鲁肽的 Boltz-2 评价

项目还对司美格鲁肽参考复合物开展了 Boltz-2 分析，以观察参考配体在相应预测流程中的模型表现。

记录中的参考复合物长度为：

- Chain A：GLP1R，395 aa。
- Chain B：司美格鲁肽，31 aa。
- 合计：426 aa。

三个模型的结果如下：

| 模型 | ipTM | pTM | 肽链 pLDDT | 双向跨链 PAE |
|---|---:|---:|---:|---:|
| model 0 | 0.9397 | 0.8850 | 0.7521 | 5.8371 |
| model 1 | 0.9603 | 0.9220 | 0.7299 | 4.5800 |
| model 2 | 0.8924 | 0.9173 | 0.5316 | 8.7435 |

这些数据说明，即使对参考配体进行结构预测，不同采样模型的局部置信度与跨链误差估计也会有所不同。

但这组数据不能直接作为新候选的实验亲和力标尺，也不能将参考肽的模型分数直接换算为候选肽的实验活性。若要将参考结构用于正式校准，需要明确同一预测条件、指标定义、样本构成和评价方法，并用相应的实验数据验证其有效性。

## 十一、第十二阶段：PCANN 补充评分与最终四条候选

### 11.1 PCANN 分析规模

PCANN 阶段分析了六个对象，每个对象对应三个 Boltz-2 预测结构：

- `candidate_0043`
- `candidate_0044`
- `candidate_0082`
- `candidate_0096`
- `candidate_0173`
- `candidate_0200`

共处理 18 个结构。

批处理脚本为：

`LOCAL_PATH

结果文件包括：

- `pcann_results/pcann_raw_18_structures.csv`
- `pcann_results/candidate_summary.csv`
- `pcann_results/structure_checks.csv`

### 11.2 批处理错误与修复

第一次候选级汇总时，脚本在执行：

`summary["pcann_avg_mean"].round(4)`

时出现：

`TypeError: Expected numeric dtype, got object instead.`

对原始 CSV 进行检查后，发现文件形状为 18 行、30 列，重新读取的 `avg` 字段为 `float64`，没有发现非数值内容。问题因此不能简单归因于原始 CSV 的 `avg` 列，而更可能与脚本运行时的中间数据类型或汇总过程有关。

随后脚本对 `avg` 和 `model_1` 至 `model_25` 使用 `pd.to_numeric(..., errors="raise")` 显式转换，并检查 NaN 和非有限值。修改后进行了脚本备份、`python -m py_compile` 语法检查和批处理运行，成功生成三个结果文件。

这项工作改善了数据处理的稳健性与结果可追溯性，但不意味着 PCANN 的生物学预测能力已被验证。

### 11.3 PCANN 评分

六个对象的候选级平均评分如下：

| 候选 | 平均评分 | 标准差 |
|---|---:|---:|
| `candidate_0043` | -9.1200 | 0.2516 |
| `candidate_0082` | -9.1100 | 0.1375 |
| `candidate_0096` | -8.9733 | 0.2043 |
| `candidate_0200` | -8.9700 | 0.0436 |
| `candidate_0173` | -8.9600 | 0.2427 |
| `candidate_0044` | -8.9433 | 0.1553 |

`candidate_0043` 和 `candidate_0082` 的平均评分在本批对象中最靠前，但二者差异仅为 0.0100。当前每个对象只有三个结构，不能仅凭这个差值断定它们的真实生物学优劣。

`candidate_0200` 的标准差最低，为 0.0436，表示本次三个结构对应的 PCANN 评分相对集中。这并不代表其真实结合能力更强，也不代表模型预测更准确。

### 11.4 PCANN 与 Kd 的关系

项目检查了 PCANN 代码中的换算常数：

```python
R = 1.987204258e-03
T = 298
dg = output.item() * R * T
```

其中 $RT$ 约为 0.5922 kcal/mol。如果模型输出确实代表以 kcal/mol 为单位的标准结合自由能，则可根据相应热力学定义进行 Kd 换算。

但当前记录没有充分证明 PCANN 的 `avg` 输出就是标准结合自由能，也没有完整核实其训练标签、单位和实验标定方式。因此，先前得到的约 205–276 nM 数值只能作为基于特定假设的条件性换算示例，不能称为实验测得的 Kd，也不应不加限定地称为可靠的定量亲和力预测。美格鲁肽：2.78 µM。

若要比较这些数值，需要核实原始论文、分子形式、受体构建体、实验条件和 PCANN 输出定义。在完成这些核查之前，不能直接得出 PCANN 高估或低估亲和力的定论。

### 11.5 最终候选集合

项目最终优先研究的四条序列为：

```fasta
>candidate_0082
HAEGTFTSDVSRYLEEKAVKQFVERLRRGGG
>candidate_0096
HAEGTFTSDVSRYLEEQAVKAFVDRLKRGAG
>candidate_0200
HAEGTFTSDVSRYLEEKAVKAFVERLRRGGG
>candidate_0043
HAEGTFTSDVSRYLEEQAVKAFVDRLKRGGG
```

四条序列均为 31 aa。

最终候选名单与第十一阶段的五条候选名单不同：

- `candidate_0044`：已完成结构评价与 PCANN 评分的中间候选，不在最终让项目报告经得起后续复核，以下问题应保留在正式档案中，而不是为了叙事完整而省略。

### 12.1 早期候选数量差异

项目记录中曾出现 1,443 条与 1,435 条唯一序列两个数字。目前明确检查过的去重 FASTA 包含 1,435 条序列，后续多个筛选路径也以 1,435 条为输入。

1,443 与 1,435 的差异原因尚未完全查明。正式报告应以实际输入文件及其审计结果为准，并将早期数量差异标记为待核查事项。

### 12.2 不同序列筛选路径的版本关系

项目至少存在两条独立的筛选路径：

- 1,435 → 787 → 308 → 65 个聚类代表。
- 1,435 → 787 → 426 → 425 → 381 → 347 → 330 → 256 → 240。

此外，还有加入参考序列并进行长度标准化后的 241 条候选池。

这些数字属于不同处理版本，不能简单串联或相加。正式报告需要为每个数据集注明输入文件、筛选规则、输出文件和版本关系。

### 12.3 ProteinMPNN 原始命令与参数记录

50 批生成、每批 200 条、模型 `v_48_020`、温度 0.1、种子 1–50 等信息已有记录，但完整原始命令没有从历史记录中恢复。

若后续要实现严格复现，应补充：

- 实际运行命令。
- 模型权重与软件版本。
- 输入结构及其校验值。
- 固定位置配置文件。
- 每批运行日志和失败记录。
- 最终汇总脚本版本。

### 12.4 ColabFold 正式批量预测状态

已完成参考 CIF 准备、ColabFold 参数检查和局部模板特征测试，但现有记录不足以确认 241 条候选的正式 ColabFold 批量预测全部完成，也不足以确认完整配对模板在正式预测中被实际使用。

不能将局部模板特征生成测试写成完整复合物模板验证成功。

### 12.5 Boltz-2 筛选阈值尚未经过实验校准

RMSD、TM-score、ipTM、complex pLDDT 和 confidence score 的筛选阈值属于本项目当前使用的操作性规则。

当前没有证据证明这些阈值已经在独立的实验阳性、阴性或定量亲和力数据上完成校准。因此，`candidate_0082` 通过五项阈值应被表述为“在当前计算筛选规则下通过”，而不是“已被证明是生物学阳性”。

### 12.6 PCANN 输出定义仍需核实

PCANN 原始评分不能仅因为代码将其乘以 $RT$，就自动认定为标准结合自由能。

后续应核查软件定义、训练标签、单位、输出映射和适用范围。在此之前，不应将条件性 Kd 换算当作实验测量结果，也不应将它与 SPR 数据直接作定量结论。

### 12.7 没有新候选的湿实验验证

当前项目记录没有提供最终四条候选的湿实验结合测定、Kd、细胞功能、受体激动活性或药理学验证结果。

因此，项目的结论应停留在计算设计和计算优选层面。对于 GLP1R 项目尤其需要区分：

- 预测结构是否合理；
- 模型是否认为复合物结构可信；
- 预测评分是否支持某种候选排序；
- 分子是否真实结合受体；
- 分子是否能激活受体；
- 是否具备后续药物开发价值。

这些是不同层次的问题，前面的计算结果不能自动替代后面的实验结论。

## 十三、项目的主要成果

综合整个项目，目前可以明确归纳为以下成果。

### 13.1 建立了可用于设计的参考结构基础

完成了 PDB 7KI0 的链提取、肽链处理、受体残基映射和界面接触分析，为后续候选设计和参考结构比对提供了统一起点。

### 13.2 完成了 ProteinMPNN 大规模序列生成

在 `v_48_020` 模型下，按 50 个种子、每批 200 条候选的方式，获得 10,000 条候选记录，并完成去重，得到 1,435 条唯一序列。

同时对生成记录的评分、序列恢复率、重复频次和跨种子分布进行了审计，区分了模型序列概率与真实生物学活性。

### 13.3 建立了多版本的序列筛选与多样性分析记录

完成了两条独立的序列筛选路径，包括：

- 一条从 1,435 条序列筛选至 308 条，再聚类为 65 个代表序列的路径。
- 一条从 1,435 条序列通过八步规则筛选至 240 条候选的路径。

同时分析了近似净电荷、GRAVY KD 和局部疏水性等序列属性。

### 13.4 完成了部分结构预测流程的调试与验证

对 ColabFold 1.6.3 的模板相关参数、参考 CIF 和局部肽链模板特征进行了检查，明确了结构文件存在、模板特征能够生成与完整配对模板实际使用之间的区别。

后续在 Boltz-2 阶段完成了候选复合物结构预测和相关模型指标整理。

### 13.5 完成了基于参考结构的候选评价

使用 US-align 比较预测受体与 7KI0 受体结构，并结合 TM-score、RMSD、Boltz-2 置信度和界面相关指标对候选排序。

通过比较三指标和五指标排序，明确候选排名会随指标组合变化，不能将任何一个模型分数当作最终生物学结论。

### 13.6 完成了 PCANN 补充评分

对六个对象对应的 18 个结构完成 PCANN 评分，修复汇总时的数值类型错误，并生成逐结构结果与候选级统计。

PCANN 为现有候选提供了补充计算证据，同时暴露出一个重要问题：在没有确认输出单位和映射关系时，不能把评分直接解释为物理自由能或实验 Kd。

### 13.7 确定了最终优先研究的四条候选

最终优先研究对象为：

1. `candidate_0082`
2. `candidate_0096`
3. `candidate_0200`
4. `candidate_0043`

这一集合是当前项目的计算优选结果。它为后续更深入的结构分析、实验设计或外部验证提供了明确的候选输入。

## 十四、最终四条候选的项目定位

为了避免后续写论文、制作 PPT 或整理 GitHub 项目时发生编号混淆，建议固定使用以下定义。

| 候选 | 项目定位 | 已有计算证据 | 当前不能声称的结论 |
|---|---|---|---|
| `candidate_0082` | 最终优先候选 | Boltz-2 五指标排序靠前；通过记录中的五项操作性阈值；PCANN 平均评分 -9.1100 | 不能声称已验证具有最高亲和力或激动活性 |
| `candidate_0096` | 最终优先候选 | Boltz-2 三指标排序第一、五指标排序第二；PCANN 平均评分 -8.9733 | 不能声称已验证具有高亲和力 |
| `candidate_0200` | 最终优先候选 | Boltz-2 五指标排序第三；PCANN 标准差 0.0436 | 不能把评分稳定性解释为实验可靠性 |
| `candidate_0043` | 最终优先候选 | Boltz-2 两种排序均进入 Top 8；PCANN 平均评分 -9.1200 | 不能仅因评分最靠前就认定为真实最优候选 |

需要注意，PCANN 平均评分只来自三个预测结构，且 `candidate_0043` 与 `candidate_0082` 的平均评分仅相差 0.0100。该差异不应被过度解释。

`candidate_0044` 和 `candidate_0173` 仍然值得保留在完整数据集中：

- `candidate_0044` 是中间候选，保留其结构与 PCANN 结果有助于追踪筛选决策。
- `candidate_0173` 是计算基线，保留它有助于比较新候选的预测表现。

但是，它们不属于最终四条优先候选集合。

## 十五、项目下一步建议

当前阶段已经形成明确的计算候选集合。如果继续推进，建议按以下优先级处理。

### 15.1 第一优先级：整理可复现的数据与代码

优先固定：

- 最终四条候选的 FASTA。
- 候选 ID 与原始序列、标准化序列的映射表。
- ProteinMPNN 输入、固定位置文件和已知运行参数。
- 各序列筛选路径的输入文件、规则和输出文件。
- Boltz-2 逐模型数据与候选级汇总。
- PCANN 逐结构评分与候选级汇总。
- 每个结果对应的脚本版本和运行日志。

特别需要保留 `candidate_0044` 和 `candidate_0173` 的中间分析记录，避免为了突出最终候选而丢失完整决策过程。

### 15.2 第二优先级：核实 PCANN 的科学定义

在继续将 PCANN 用于定量亲和力预测之前，应先确认 `avg` 的含义、单位、训练标签及输出与 Kd 的关系。

如果这些信息不能得到可靠确认，建议在项目报告中只使用 PCANN 的原始评分及其排序，不使用条件性 Kd 换算作为核心结论。

### 15.3 第三优先级：统一候选结构评价规则

如果要进一步比较四条最终候选，建议固定：

- 参考受体结构和残基映射。
- 结构对齐与 RMSD 计算方案。
- Boltz-2 指标的具体定义。
- PCANN 的输入结构选择规则。
- 多结构汇总方式。
- 排名规则及其局限性。

这样可以避免因为不同分析阶段采用不同指标组合而产生不必要的排名冲突。

### 15.4 第四优先级：明确实验验证需求

如果项目目标最终是获得 GLP1R 激动剂，而不只是获得结构上合理的候选肽，则后续需要真实的实验数据。

至少需要区分两个层次：

1. **结合验证：** 候选是否与 GLP1R 结合，以及亲和力如何。
2. **功能验证：** 候选是否激活 GLP1R，以及其功能效应和相关药理特征如何。

即使候选能够结合受体，也不能自动推断它是激动剂；反之，结构模型评分较高也不能替代功能测定。

在当前没有湿实验条件的情况下，最合理的做法是把项目定位为“计算候选设计与优先级筛选”，明确实验验证是未来工作，而不是把未完成的实验环节写成已获得的结果。

## 十六、建议用于项目报告的最终总结

本项目以 PDB 7KI0 中司美格鲁肽—GLP1R 复合物为参考，完成了受体与肽链结构整理、界面几何分析、ProteinMPNN 输入准备以及大规模候选序列生成。通过 50 个随机种子、每批 200 条候选的生成流程，获得了 10,000 条候选记录，并去重得到 1,435 条唯一序列。项目随后开展了多版本序列筛选、理化性质分析和序列多样性聚类，形成了不同阶段的候选集合。

在结构评价阶段，项目使用 Boltz-2 对候选肽与 GLP1R 进行复合物结构预测，结合模型置信度、界面相关指标以及预测受体与 7KI0 参考结构之间的 TM-score 和 RMSD，对候选进行多指标比较。不同指标组合产生的排序并不完全一致，说明候选优先级受到评价指标和筛选规则的影响。随后，项目使用 PCANN 对六个对象对应的 18 个预测结构进行补充评分，并通过修复数据类型处理问题，完成逐结构结果与候选级汇总。

综合现有计算证据，项目最终将 `candidate_0082`、`candidate_0096`、`candidate_0200` 和 `candidate_0043` 确定为后续优先研究的四条候选肽。其中，`candidate_0082` 在当前 Boltz-2 五指标操作性筛选中表现突出；`candidate_0043` 与 `candidate_0082` 在本次 PCANN 平均评分中最靠前；`candidate_0200` 的三个结构评分相对稳定；`candidate_0096` 在此前结构排序中表现较好。这些差异为后续候选比较提供了依据，但尚不足以证明某条候选具有更高的真实结合亲和力或更强的 GLP1R 激动活性。

项目的主要贡献是建立了一套从参考结构、序列生成、序列筛选、结构预测到多指标计算评价的候选优选流程，并对各阶段的数据来源、处理方式和证据边界进行了整理。当前成果应定位为计算设计与候选优先级研究，而不是已经完成实验验证的药物开发项目。下一阶段最重要的任务是提高数据与代码的可复现性、核实 PCANN 评分的科学定义，并在具备条件时通过结合实验和功能实验验证最终候选。

**最终项目状态：计算设计与候选优选已形成明确结果；最终四条优先候选为 `candidate_0082`、`candidate_0096`、`candidate_0200` 和 `candidate_0043`。真实结合亲和力、GLP1R 激动活性及相关药理性质尚未得到本项目的实验验证。**

---

# you asked

message time: 2026-10-23 15:42:46

这两个文本内容不变（包括空行），给我分别转成能直接复制的形式

---

# chatgpt response

可以。下面把两份文本分别放在独立的可复制区域中，**保留原文内容、标题、空行、表格、路径和代码**，不做润色或修改。

## 文本一：第十二阶段工作记录

WritingBlock>

## 文本二本项目的实验验证。**</WritingBlock>

---

# you asked

message time: 2026-10-23 15:50:07

现在确实得到了我想要的序列，但还有一个问题，这些序列能否算作De novo，你怎么看

---

# chatgpt response

我认为：**你们得到的四条序列可以合理地称为 *de novo-designed candidates*（从头设计候选肽），但目前还不能不加限定地声称它们是“全新、独立于已知天然配体的 de novo 蛋白质”。** 这两个判断并不矛盾。

关键在于，`de novo` 并不一定意味着序列与所有已知分子都毫无相似性。它更关注的是：**分子是如何被设计出来的、设计过程是否依赖现成的天然序列，以及最终分子在多大程度上是新设计的。**

对你们的 GLP1R 项目，我会把问题拆成三个层面：

1. **设计方法：** 你们是否通过计算方法生成或改造了候选序列，而不是直接拿一个已知配体作为最终答案？
2. **序列新颖性：** 最终序列与司美格鲁肽、GLP-1、D13、D41、D44 等已知序列究竟有多相似？
3. **功能新颖性：** 这些序列是否真的形成了新的 GLP1R 结合模式，并且能激活受体？

目前，第一点有较强依据；第二点需要做更严格的序列溯源与相似性分析；第三点还没有实验数据支持。

## 一、先看你们的序列：它们究竟新在哪里？

你们的最终候选是：

| 候选 | 序列 |
|---|---|
| `candidate_0082` | `HAEGTFTSDVSRYLEEKAVKQFVERLRRGGG` |
| `candidate_0096` | `HAEGTFTSDVSRYLEEQAVKAFVDRLKRGAG` |
| `candidate_0200` | `HAEGTFTSDVSRYLEEKAVKAFVERLRRGGG` |
| `candidate_0043` | `HAEGTFTSDVSRYLEEQAVKAFVDRLKRGGG` |

它们有一个很明显的特征：**四条序列共享同一个 GLP-1 样肽链骨架，而且保留了很长一段与已知 GLP-1 类配体相似的 N 端序列。**

以司美格鲁肽的参考序列为例：

<box border radius="lg" padding={3} gap={3}>
  <box gap={1}>
    <text color="secondary" size="sm">司美格鲁肽参考序列</text>
    <text preserveWhitespace>{`HAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG`}</text>
  </box>
  <divider color="subtle" />
  <box gap={1}>
    <text color="secondary" size="sm">candidate_0082</text>
    <text preserveWhitespace>{`HAEGTFTSDVSRYLEEKAVKQFVERLRRGGG`}</text>
  </box>
  <divider color="subtle" />
  <text color="secondary" size="sm">共同特征</text>
  两者前 11 个氨基酸完全相同。从第 12 位开始，序列出现了替换与重新组合，但整体仍明显属于 GLP-1 样肽序列框架。
</box>

而且，这并不是偶然产生的相似性。你们此前的 ProteinMPNN 设计中，肽链部分位置被明确固定，序列生成是在已准备好的 GLP1R—参考肽结构背景下开展的。后续最终候选与 `candidate_0173` 相比，只有 3–4 个位置发生变化。

这意味着，你们的工作并不是从完全无关的氨基酸序列空间出发，独立发现了一种全新的 GLP1R 结合肽骨架；它是在已有 GLP-1 样骨架上，通过计算方法设计和筛选变体。

但这并不意味着工作没有价值。真正需要明确的是：你们的新颖性主要体现在哪里。

## 二、从三个层面判断是否属于 de novo

<box gap={3}>
  <row align="start" gap={3}>
    <box background="surface-secondary" radius="lg" size="44px" align="center" justify="center">
      <icon name="check-circle" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **层面 1：计算设计过程——有依据**

      你们使用 ProteinMPNN 生成大量序列，经过多轮序列筛选、结构预测、Boltz-2 多指标评价和 PCANN 补充评分，最后选择了四条候选。它们不是直接将司美格鲁肽原样作为最终设计结果。

      因此，称其为 **computationally designed peptides**（计算设计肽）是合理的。
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <box background="surface-secondary" radius="lg" size="44px" align="center" justify="center">
      <icon name="git-compare" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **层面 2：序列新颖性——有一定新颖性，但不是完全从零**

      最终序列并非司美格鲁肽的原样复制，而是包含多个氨基酸替换和不同的 C 端序列组合。不过，它们仍然明显继承了 GLP-1 样序列骨架，而且最终四条候选之间也高度相似。

      所以更准确的描述是 **scaffold-based sequence design**（基于已有骨架的序列设计），或 **computational redesign of a GLP-1-like peptide**（GLP-1 样肽的计算再设计）。
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <box background="surface-secondary" radius="lg" size="44px" align="center" justify="center">
      <icon name="flask-conical" size="xl" />
    </box>
    <box flex="1" gap={1}>
      **层面 3：全新结合机制或生物学功能——尚未证明**

      目前的结构预测和评分不能证明这些序列形成了全新的结合模式，也不能证明它们能够激活 GLP1R。

      因此，不应称它们为已经发现的“新型 GLP1R 激动剂”，也不能声称已经实现了全新的结合机制。
    </box>
  </row>
</box>

## 三、我建议怎样使用 de novo 这个词？

不同表述所承诺的科学含义并不相同。

| 表述 | 对你们当前项目是否合适 | 原因 |
|---|---|---|
| `Computationally designed GLP-1-like peptides` | 很合适 | 准确说明计算设计及序列类型 |
| `Scaffold-based de novo peptide design` | 可以使用，但要解释 | 强调是在指定骨架或结构条件下进行设计 |
| `De novo sequence design on a GLP-1-derived scaffold` | 很合适 | 明确设计新序列，但承认其骨架来源 |
| `De novo GLP1R binder design` | 需要谨慎限定 | 容易让人理解为从头设计了新的结合剂，而目前尚无实验结合验证 |
| `Discovery of novel GLP1R agonists` | 目前不合适 | 尚未通过实验验证结合与激动功能 |

这里有个容易忽略的事实：在计算蛋白设计领域，*de novo* 不一定意味着完全不使用模板或参考结构。研究者可以在给定骨架、结合位点或结构约束的条件下设计新序列。

因此，**你们不必因为使用了已知 GLP-1 样骨架，就完全放弃 de novo 这个词；但应明确你们的设计属于哪一种 de novo。**

## 四、如果我是你，我会怎样定义这个项目？

我会把项目定位为：

<box border radius="lg" padding={4} gap={2}>
  <text color="secondary" size="sm">推荐的英文项目描述</text>
  <title size="lg">Structure-Guided De Novo Sequence Design on a GLP-1-Like Peptide Scaffold</title>
  在 GLP-1 样肽骨架与受体结构约束下，利用 ProteinMPNN 生成和筛选候选序列，再通过 Boltz-2 结构预测、多指标评价和 PCANN 补充评分确定优先研究对象。
  <divider color="subtle" />
  <text color="secondary" size="sm">中文描述</text>
  **基于 GLP-1 样肽骨架的结构引导从头序列设计与计算优选**

  该项目的核心是利用计算方法设计和筛选具有序列变化的候选肽，而不是声称从零发现了全新的蛋白质骨架或已经获得经过实验验证的 GLP1R 激动剂。
</box>

如果你想在项目标题中保留 `de novo`，我建议使用：

**Structure-Guided De Novo Peptide Design for GLP1R: Sequence Generation, Structural Evaluation, and Candidate Prioritization**

这个标题既保留了计算蛋白设计领域常用的术语，也不会直接宣称已经获得新型激动剂。

## 五、如果想进一步证明序列新颖性，还缺什么？

目前我们可以判断它们与参考序列存在明显的继承关系，但还不能严谨地断言它们是否为全球范围内未被报道过的序列，也不能仅凭肉眼判断它们在整个 GLP-1 类肽序列空间中的新颖程度。

建议做三项分析：

1. **参考序列相似性分析。** 将四条最终候选与 GLP-1、司美格鲁肽、D13、D41、D44 以及其他相关已知 GLP1R 配体进行逐位比对，报告序列一致性、替换位置和末端差异。
2. **数据库新颖性检查。** 在适当的蛋白质或肽序列数据库中检索精确匹配和高相似序列。只有在明确数据库、检索日期和检索范围后，才能说明“在所检查的数据库中未发现匹配”。
3. **设计空间新颖性分析。** 比较最终候选与原始参考肽、ProteinMPNN 全部候选及其他已知配体之间的序列距离，判断最终四条是常见序列模式的局部变体，还是在所考察的候选空间中具有一定的新颖性。

即使三项分析都完成了，它们证明的仍然主要是**序列新颖性和计算设计过程**，而不是新的结合机制或激动功能。

---

## 我的最终判断

我不会把你们的工作贬低为简单的序列修改，也不会把它包装成完全从零发现的新型蛋白质。

你们确实进行了计算序列设计、候选筛选和结构评价；但设计过程明显受到 GLP-1 样参考序列和结构骨架的约束。

因此，我最推荐的定位是：

**Structure-guided, scaffold-based de novo peptide sequence design。**

中文就是：**基于已有肽骨架的结构引导从头序列设计。**

它既承认设计过程中确实产生了新的候选序列，也准确说明了这些序列与已知 GLP-1 类配体之间的关系。对一个需要展示研究思路、方法严谨性和个人贡献的本科项目来说，这比单纯强调“完全从零设计”更可信。

---

# you asked

message time: 2026-10-23 15:52:36

原文献对其过程的描述是De novo吗

---

# chatgpt response

**是的，原文献明确将这个过程称为 *de novo design*，而且不只是泛泛地在背景中提到，而是直接用在方法章节的标题和流程描述中。**

我查到的文献是 *AI-Driven De Novo Design of Ultra Long-Acting GLP-1 Receptor Agonists*，发表于 *Advanced Science*。原文有几个很明确的表述：<Cite refs={["turn204003search0","turn204003search2"]}/>

- **章节标题：** “De novo GLP-1RAs Design”
- **流程描述：** “ProteinMPNN de novo sequences design”
- **方法描述：** 作者以 semaglutide–GLP-1R 复合物的实验结构（PDB 7KI0）作为模板，固定选定的保守位点，再用 ProteinMPNN 设计其余位点，生成了 10,000 条 de novo GLP-1RA 序列。

所以，**在这篇文献自己的术语体系里，即使设计使用了已知 GLP-1 类肽的结构模板、保留了关键保守残基，作者仍然把它称为 de novo 设计。** 这说明 *de novo* 并不必然意味着完全不依赖已有序列或结构。<Cite refs={["turn204003search0","turn204003search2"]}/>

## 对你们的四条候选序列意味着什么？

可以使用 *de novo*，但最好准确描述设计层级：

- **对原文献的方法：** 可以直接称为 *de novo peptide sequence design*。
- **对你们复现后筛选出的四条序列：** 可以称为 *scaffold-based de novo peptide design*（基于已有肽骨架的从头序列设计），因为设计从 semaglutide–GLP-1R 结构出发，并保留了多处关键残基。
- **对候选物的生物学性质：** 目前不能仅凭计算结果称它们已被证实为新型 GLP-1R 激动剂；仍需实验验证受体结合与激动活性。

还有一个重要细节：文献报告固定了 **13 个保守位点**，而你们当前复现流程记录的是 **12 个固定位置**。因此可以说你们采用了该文献的设计思路，但若要声称严格复现了原方法，需要核对并解释这一差异。<Cite refs={["turn204003search0","turn204003search2"]}/>

**我建议你在项目报告中这样写：**

> We performed scaffold-based de novo peptide sequence design using the semaglutide–GLP-1R complex structure as a template, followed by computational structural evaluation and candidate prioritization.

中文：

> 我们以 semaglutide–GLP-1R 复合物结构为模板，开展基于已有肽骨架的从头肽序列设计，并通过计算结构评价对候选序列进行优选。

这个说法既符合原文献对 *de novo* 的用法，也不会把计算筛选结果夸大成已经得到实验验证的新药。

---

# you asked

message time: 2026-10-23 15:54:03

你在全网范围检索一下我最终得到的4条序列，看看他们到底是不是全新的

---

# chatgpt response

我会把“全新”拆成三个可以核查的问题，而不是只看搜索引擎有没有搜到完全相同的字符串：

1. **完全相同的序列是否已公开**：论文、补充材料、专利、公开数据库中是否出现过这四条序列。
2. **是否只是已有 GLP-1 类肽的近似变体**：与 semaglutide、已发表的 D13/D41/D44，以及其他 GLP-1R 配体相比，序列差异有多大。
3. **是否具有可主张的新颖性**：公开资料中未找到相同序列，不等于已证明它们在全球范围内从未被提出，也不等于已经具备专利新颖性。

目前已经定位到你们所依据的原始论文：Wei 等人发表于 *Advanced Science* 的 *AI-Driven De Novo Design of Ultra Long-Acting GLP-1 Receptor Agonists*。论文明确称使用 ProteinMPNN 生成了 10,000 条序列，并以序列多样性筛选来降低与已有上市药物的相似性；但其数据声明是可向通讯作者合理请求获取，并非所有设计序列都直接公开在正文中。<Cite refs={["turn553228search2","turn978732view0"]}/>

## 1. 全网精确序列检索结果

我分别对四条候选序列进行了精确字符串搜索，并扩展到 GLP-1R、peptide、sequence、patent、database 等关键词。

<box border radius="lg" padding={3} gap={3}>
  <row align="start" gap={2}>
    <icon name="search-check" size="xl" color="success" />
    <box flex="1" gap={1}>
      **candidate_0082**

      <text size="sm">`HAEGTFTSDVSRYLEEKAVKQFVERLRRGGG`</text>
      <badge color="success">未检出公开精确匹配</badge>
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={2}>
    <icon name="search-check" size="xl" color="success" />
    <box flex="1" gap={1}>
      **candidate_0096**

      <text size="sm">`HAEGTFTSDVSRYLEEQAVKAFVDRLKRGAG`</text>
      <badge color="success">未检出公开精确匹配</badge>
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={2}>
    <icon name="search-check" size="xl" color="success" />
    <box flex="1" gap={1}>
      **candidate_0200**

      <text size="sm">`HAEGTFTSDVSRYLEEKAVKAFVERLRRGGG`</text>
      <badge color="success">未检出公开精确匹配</badge>
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={2}>
    <icon name="search-check" size="xl" color="success" />
    <box flex="1" gap={1}>
      **candidate_0043**

      <text size="sm">`HAEGTFTSDVSRYLEEQAVKAFVDRLKRGGG`</text>
      <badge color="success">未检出公开精确匹配</badge>
    </box>
  </row>
  <text color="secondary" size="xs">说明：这里的“未检出”仅表示本次公开网页索引检索未发现完全相同的字符串，不代表已经穷尽所有专利、数据库、未公开申请或文献附件。</text>
</box>

本次检索涉及的代表性来源：

- 原始设计论文：[AI-Driven De Novo Design of Ultra Long-Acting GLP-1 Receptor Agonists](https://pmc.ncbi.nlm.nih.gov/articles/PMC12561408/)，包含设计方法、部分实验候选信息及补充材料入口。<Cite refs={["turn553228search2","turn978732view0"]}/>
- [GLP-1 类似物专利示例](https://patents.justia.com/patent/20250074964)，说明相关序列及其变体已有广泛专利布局。<Cite refs={["turn635620search3"]}/>

## 2. 这四条序列与已知肽的关系

这里有一个重要区别：**没有搜到完全相同的序列，不代表它们与已知肽在序列上没有高度相似性。**

你们的四条候选序列都保留了 semaglutide 的前 11 个氨基酸残基，之后则存在明显的序列差异。这符合基于已有肽骨架进行序列设计的特征，但不能据此认定它们是完全独立于已知 GLP-1 类肽的新骨架。

此外，你们四条候选与内部基线 `candidate_0173` 的关系非常密切：

| 候选序列 | 与 `candidate_0173` 的差异 |
|---|---:|
| `candidate_0082` | 3 个氨基酸替换 |
| `candidate_0096` | 3 个氨基酸替换 |
| `candidate_0200` | 3 个氨基酸替换 |
| `candidate_0043` | 4 个氨基酸替换 |

这说明四条候选在**你们自己的设计流程内是经过筛选得到的不同序列**，但它们属于同一相近序列家族，而不是四个完全不同的肽骨架。

## 3. 最关键的缺口：还没有完成数据库级的穷尽比对

原始论文的补充材料可以通过 [PMC 补充材料入口](https://pmc.ncbi.nlm.nih.gov/articles/PMC12561408/#supplementary-materials)访问，但论文的数据声明也指出，相关数据可向通讯作者合理请求获取。<Cite refs={["turn841515view2","turn978732view0"]}/>

因此，目前我不能确认这四条序列是否出现在论文的完整 10,000 条 ProteinMPNN 设计序列中，也不能仅凭网页搜索排除它们出现在其他专利序列表或未被搜索引擎索引的数据库中。

若要把“新颖性”判断做得更扎实，至少还应完成：

1. **原论文序列池比对**：将四条候选与论文公布的全部设计序列、实验候选序列以及 D13、D41、D44 比对。
2. **公共蛋白及肽序列数据库比对**：搜索精确匹配和高相似度匹配，并记录数据库、检索日期及比对参数。
3. **专利序列表检索**：针对 GLP-1、GLP-1R agonist、peptide analogue 等相关专利检索序列，而不只检索正文中的文字。
4. **报告相似性而不只报告命中与否**：列出最高序列一致性、差异残基位置、覆盖度及匹配来源。

## 4. 目前可以下什么结论？

<box border radius="lg" padding={3} gap={2}>
  <title size="lg">当前证据支持的结论</title>
  <row align="start" gap={2}>
    <icon name="check-circle" color="success" size="lg" />
    <box flex="1" gap={1}>
      **计算设计意义上的新序列：有依据。**

      四条序列是你们经过计算生成、筛选和结构评价得到的候选序列。
    </box>
  </row>
  <row align="start" gap={2}>
    <icon name="circle-help" color="warning" size="lg" />
    <box flex="1" gap={1}>
      **全球范围内从未公开过：尚未证实。**

      本次精确网页搜索没有检出匹配，但尚未完成全面的序列数据库与专利序列表比对。
    </box>
  </row>
  <row align="start" gap={2}>
    <icon name="circle-help" color="warning" size="lg" />
    <box flex="1" gap={1}>
      **具有专利新颖性或新的生物学功能：尚未证实。**

      这分别需要针对现有技术进行专利新颖性分析，以及实验验证受体结合和激动活性。
    </box>
  </row>
</box>

**我的判断是：目前没有发现这四条序列在公开网页中存在完全相同的已发表记录，但证据还不足以断言它们是全球范围内全新的序列。** 在你的项目报告里，可以稳妥地写成 *computationally designed GLP-1-like peptide candidates*（计算设计的 GLP-1 样肽候选物），并注明它们基于已有肽骨架、尚未完成全面的新颖性检索及实验验证。

---

# you asked

message time: 2026-10-23 15:54:52

进一步完成全面的序列数据库与专利序列表比对

---

# chatgpt response

## 本轮扩大检索：先明确能验证到哪一步

我进一步查了四条序列的精确字符串、GLP-1R 肽类相关文献与专利，以及公开的专利序列检索工具。

有一个重要限制需要先说明：**公开网页检索与真正的序列数据库比对不是同一回事。** 例如，NCBI BLAST 可以将氨基酸序列直接与蛋白质数据库或专利序列数据库比对；Lens PatSeq Finder 则专门检索专利公开的生物序列，并提供序列相似度、覆盖度和专利编号。<Cite refs={["turn872589search0","turn215073search3","turn215073search0"]}/>

我目前能核查公开网页搜索结果和数据库的检索方式，但尚未取得四条序列在 NCBI BLAST、Lens PatSeq Finder 中实际运行后的结果报告。因此，我不会把“网页没有搜到”写成“数据库比对未命中”，也不会伪造相似度、E-value 或专利编号。

## 1. 本轮检索记录

检索日期：2026 年 10 月 23 日。

| 检索项目 | 本轮结果 | 证据强度 |
|---|---|---|
| 四条完整氨基酸序列的公开网页精确检索 | 未发现可确认的完全匹配记录 | 初步证据 |
| GLP-1R 相关文献和公开网页 | 找到相关设计论文，但未确认四条序列是否在其完整序列池中 | 不足以判断 |
| NCBI 公共蛋白序列库 | 已确认可通过 BLAST 检索；尚未取得四条序列的实际运行结果 | 未完成比对 |
| NCBI 专利序列库 | 已确认其专利序列检索途径；尚未取得实际运行结果 | 未完成比对 |
| Lens PatSeq Finder | 已确认支持专利序列相似性搜索，但需登录；本轮没有成功提交序列检索 | 未完成比对 |
| WIPO、EPO 等专利公开记录 | 尚未完成序列表级别的系统检索 | 未完成比对 |

NCBI 明确提醒，其专利相关信息不保证完整，不能将 NCBI 检索单独当作法律意义上的专利检索。其专利序列数据也存在收录限制，例如部分尚未授权的申请序列可能没有进入相关数据库。<Cite refs={["turn915624view1","turn215073search6"]}/>

Lens 的检索工具可以报告专利序列的相似度、覆盖度、E-value、SEQ ID NO 和对应专利文献；但其说明也提到，部分序列可能尚未被标准化提取，因此未命中并不保证相关专利不存在。<Cite refs={["turn915624view0","turn215073search12"]}/>

## 2. 真正完成全面比对，需要运行哪些检索？

下面是可直接使用的检索入口：

<box border radius="lg" padding={3} gap={3}>
  <row align="start" gap={3}>
    <favicon url="https://blast.ncbi.nlm.nih.gov" size="32px" />
    <box flex="1" gap={1}>
      **NCBI Protein BLAST**

      <text color="secondary" size="sm">检索公共蛋白序列；应分别运行四条序列，并使用适合 31 aa 短肽的参数。</text>
      <text><Link url="https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastp&PAGE_TYPE=BlastSearch" title="打开 Protein BLAST" /></text>
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <favicon url="https://www.ncbi.nlm.nih.gov" size="32px" />
    <box flex="1" gap={1}>
      **NCBI 专利序列 BLAST**

      <text color="secondary" size="sm">在 BLAST 的数据库选择项中选择 Patent sequences（pat），与公开专利序列进行相似性比对。</text>
      <text><Link url="https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastp&PAGE_TYPE=BlastSearch" title="进入检索页面" /> · <Link url="https://www.ncbi.nlm.nih.gov/education/patent_and_ip_faqs/" title="官方专利序列检索说明" /></text>
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <favicon url="https://www.lens.org" size="32px" />
    <box flex="1" gap={1}>
      **Lens PatSeq Finder**

      <text color="secondary" size="sm">专门对专利公开的氨基酸序列做相似性检索，可进一步检查命中序列是否位于权利要求中。</text>
      <text><Link url="https://support.lens.org/knowledge-base/patseq-finder-search/" title="查看官方检索指南" /></text>
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <favicon url="https://patentscope.wipo.int" size="32px" />
    <box flex="1" gap={1}>
      **WIPO PATENTSCOPE**

      <text color="secondary" size="sm">用于补充检索国际专利公开文本与相关申请信息。</text>
      <text><Link url="https://patentscope.wipo.int/" title="打开 PATENTSCOPE" /></text>
    </box>
  </row>
</box>

对于 31 个氨基酸的短肽，不能只依赖默认 BLAST 参数：需要关注短查询参数、低复杂度过滤、覆盖度，以及是否存在完整的 31/31 匹配。NCBI 官方说明了短序列检索需要特别调整参数。<Cite refs={["turn872589search24","turn872589search3"]}/>

建议将 **100% 全长一致性** 作为精确匹配标准，并另外检查：

- 31/31 覆盖、100% identity：完全相同序列。
- 全长覆盖、identity ≥90%：高度相似序列。
- 全长覆盖、identity ≥80%：进一步调查的近似序列。
- 部分覆盖命中：单独记录，不能直接视为同一完整肽。

这些相似度区间是本次检索建议采用的操作性分层，不是法律上的新颖性标准。

## 3. 最终判断

目前的结果**还不足以宣布这四条序列已通过全面的数据库与专利新颖性检索**。我已经完成了公开网页精确搜索和检索渠道核查，但不能把尚未实际运行的 BLAST 或专利序列搜索报告成已完成。

要完成你要求的全面比对，下一步需要在上述数据库中提交四条序列，取得实际命中结果，并逐条核验命中记录及专利原文。尤其需要区分：序列出现在专利说明书中、序列被权利要求明确涵盖，以及该专利是否仍有效，这三者不是同一件事。

在取得这些结果之前，最严谨的表述仍然是：**本轮公开网页检索未发现四条序列的完全匹配，但其全球公开序列新颖性及专利新颖性尚未确定。**

---

# you asked

message time: 2026-10-23 15:56:16

你直接帮我在NCBI BLAST里面完成检索

---

# chatgpt response

## 4. 四条序列的精确检索补充

我又对四条完整序列进行了带引号的网页检索，限定关键词 `NCBI`。本轮没有返回匹配结果。

这只是额外的公开网页检索，**不是 NCBI BLAST 的实际运行结果**。我尝试通过 NCBI 的 BLAST URL API 提交查询，但当前可用的网页访问方式没有成功返回任务编号（RID），因此无法诚实地声称已经在 NCBI 数据库中完成比对。

你可以直接打开 NCBI 官方 BLAST 页面：

<Link url="https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastp&PAGE_TYPE=BlastSearch" title="打开 NCBI Protein BLAST" />

把下面四条序列以多 FASTA 格式粘贴进去KAFVDRLKRGGG
```

建议至少分别检查公共蛋白数据库与专利序列数据库，并保留 BLAST 返回的 RID、数据库名称、检索日期和结果页面。对这些只有 31 个残基的短肽，还需要确认检索参数适合短序列。

**当前能确定的结论仍然是：本轮网页检索未发现完全相同的公开记录，但 NCBI BLAST 尚未成功提交，因而不能报告数据库命中数或宣布通过了 NCBI 序列新颖性检索。**

---

# you asked

message time: 2026-10-23 16:29:08

阶段一：参考序列与结构准备
当前阶段 · 立即存档
建立项目环境，获取 7KI0，提取 Semaglutide 与 GLP-1R 参考数据，核对结构残基与序列映射。




阶段二：参考复合物与结合界面分析
尚未完成
分析肽链—受体空间接触、整理关键残基，并核对结构编号与序列编号。




阶段三：ProteinMPNN 序列设计与筛选
后续阶段
明确设计输入、固定残基、生成参数、候选数量及序列筛选标准。




阶段四：候选结构预测与质量评估
后续阶段
使用 AlphaFold/ColabFold 等工具预测候选复合物结构，记录参数、成功率和结构评价指标。




阶段五：候选比较、证据汇总与研究报告
后续阶段
综合序列、结构和文献证据，讨论结合与激动潜力的支持程度和局限。
对了把这个目录根据实际的流程更新一下，因为这是在最开始做的，与实际情况不太匹配

---

# chatgpt response

建议把原来的 5 个阶段更新成更贴合实际执行过程的 **7 个阶段**。原目录把 AlphaFold/ColabFold 当成主要候选结构预测步骤，但你们实际已经推进到 **Boltz-2 结构评估和 PCANN 评分**；同时，ProteinMPNN 之后有多条不同的序列筛选路径，最终候选也经历了多指标比较。因此需要把这些环节分别写清楚，避免把计划中的工作写成已经完成的工作。

WritingBlock>

### 我建议你特别保留的三个修改

1. **把 Boltz-2 独立列为阶段五。** 这是你们实际开展的重要结构预测与评价环节，不应再笼统写成“使用 AlphaFold/ColabFold 等工具”。
2. **把 PCANN 单独列为阶段六。** 这样能体现你们不只进行结构预测，还对候选结构进行了另一种计算评分，同时不会误把 PCANN 分数当成实验亲和力。
3. **将新颖性检索放入最后阶段，并明确标记进行中。** NCBI BLAST 和专利序列表的实际比对尚未成功完成，所以不能写成已完成的全面新颖性验证。

另外，原目录中的“立即存档”更适合阶段一的原始输入、结构文件、序列映射表和环境配置；后续每个阶段也应分别保存输入文件、运行参数、日志、结果表与筛选依据。这样目录既能作为项目进度说明，也能成为之后 GitHub 仓库和正式研究报告的工作记录。

---

# you asked

message time: 2026-10-23 16:51:04

那你在网上能搜到D13、D41、D44的序列码

---

# chatgpt response

能搜到，而且找到了一个直接列出三条序列的公开数据集。它与 2025 年发表的原始论文 *AI-Driven De Novo Design of Ultra Long-Acting GLP-1 Receptor Agonists* 对应。<Cite refs={["turn469921search0","turn469921search3"]}/>

## D13、D41、D44 的公开序列

<box border radius="lg" padding={3} gap={3}>
  <box gap={1}>
    <row align="center" justify="between">
      **D13**
      <badge color="success">已找到</badge>
    </row>
    <text size="sm">31 aa · FASTA 序列</text>
    <text>{'HAEGTFTSDVSSYLEEQAAKAFVERLKRGRG'}</text>
    <button block variant="outline" onClick={() => GenUI.copy("HAEGTFTSDVSSYLEEQAAKAFVERLKRGRG")}>复制 D13 序列</button>
  </box>
  <divider color="subtle" />
  <box gap={1}>
    <row align="center" justify="between">
      **D41**
      <badge color="success">已找到</badge>
    </row>
    <text size="sm">31 aa · FASTA 序列</text>
    <text>{'HAEGTFTSDVSSYLEEQQVKQFVERLKRGRG'}</text>
    <button block variant="outline" onClick={() => GenUI.copy("HAEGTFTSDVSSYLEEQQVKQFVERLKRGRG")}>复制 D41 序列</button>
  </box>
  <divider color="subtle" />
  <box gap={1}>
    <row align="center" justify="between">
      **D44**
      <badge color="success">已找到</badge>
    </row>
    <text size="sm">31 aa · FASTA 序列</text>
    <text>{'HAEGTFTSDVSRYLEEKAVKDFVERLKRGAG'}</text>
    <button block variant="outline" onClick={() => GenUI.copy("HAEGTFTSDVSRYLEEKAVKDFVERLKRGAG")}>复制 D44 序列</button>
  </box>
</box>

来源：公开数据集 [GLP-1RAs Validated by in vivo](https://huggingface.co/datasets/weitinging/GLP-1RAs_Validated_by_in_vivo)，其中列出了三条肽的序列、实验数据和化学修饰信息。<Cite refs={["turn469921search3"]}/>

## 对你们项目有一个特别重要的发现

**你们的基线 `candidate_0173` 与文献中的 D44 序列完全一致。**

- D44：`HAEGTFTSDVSRYLEEKAVKDFVERLKRGAG`
- candidate_0173：`HAEGTFTSDVSRYLEEKAVKDFVERLKRGAG`

这不是高相似度，而是 **31/31 个氨基酸完全一致**。你们之前将 `candidate_0173` 作为 D44 相关基线是合理的；现在可以进一步确认，它在一级序列层面就是文献所列的 D44。

需要注意：FASTA 序列表示的是氨基酸主链序列，不完整体现所有化学修饰。该文献中的 D13、D41、D44 具有特定的脂肪酸相关修饰，因此不能只凭序列字符串就认定你们计算输入与实验使用的肽在化学结构上完全相同。<Cite refs={["turn469921search0","turn469921search3"]}/>

这三条序列也可以直接作为你们后续四条候选的公开参照，开展精确序列匹配和逐位点差异分析。

---

# you asked

message time: 2026-10-23 16:52:31

那你在各个公开的数据集里能搜到我做出来的那4条序列码

---

# chatgpt response

我又查了 Hugging Face 上公开的 GLP-1R 激动剂数据集，以及 ProteinMPNN 相关公开数据集。结论是：**目前没有在本轮检索到的公开数据集中发现你这四条候选序列的完全匹配记录，但还不能据此认定它们在所有公开数据集中都不存在。**

## 1. 已核查的数据集

<box border radius="lg" padding={3} gap={3}>
  <row align="start" gap={3}>
    <AsyncImage query="Hugging Face datasets logo" aspectRatio="1:1" maxWidth="56px" />
    <box flex="1" gap={1}>
      **<Link url="https://huggingface.co/datasets/weitinging/GLP-1RAs_Validated_by_in_vivo" title="GLP-1RAs Validated by in vivo" />**

      <badge color="success">已核查公开预览</badge>

      数据集预览包含 4 条记录：Semaglutide、D13、D41、D44，没有显示你们的四条候选序列。数据集说明同时指出，完整的 10,000 条设计序列需要联系论文作者申请。<Cite refs={["turn126840search0","turn126840search1"]}/>
    </box>
  </row>
  <divider color="subtle" />
  <row align="start" gap={3}>
    <AsyncImage query="ProteinMPNN protein structure neural network scientific protein visualization" aspectRatio="1:1" maxWidth="56px" />
    <box flex="1" gap={1}>
      **<Link url="https://huggingface.co/datasets/RosettaCommons/ProteinMPNN" title="RosettaCommons/ProteinMPNN" />**

      <badge>相关方法数据集</badge>

      该数据集主要用于 ProteinMPNN 的训练数据与结构相关分析，不是你们所依据论文的完整 GLP-1RA 设计候选库。没有发现可直接证明四条候选是否存在于原论文 10,000 条序列中的记录。<Cite refs={["turn126840search2","turn126840search6"]}/>
    </box>
  </row>
</box>

## 2. 四条候选的当前检索状态

| 候选 | 本轮公开网页精确检索 | 上述 GLP-1R 数据集公开预览 |
|---|---|---|
| `candidate_0082` | 未发现精确匹配 | 未显示 |
| `candidate_0096` | 未发现精确匹配 | 未显示 |
| `candidate_0200` | 未发现精确匹配 | 未显示 |
| `candidate_0043` | 未发现精确匹配 | 未显示 |

这里的“未显示”很重要：公开数据集只有四条实验参照记录，**并没有包含原论文的全部设计序列**。所以不能把它理解为已经逐条搜索过那 10,000 条序列。

## 3. 最有价值的下一步

原论文数据集页面明确邀请研究者联系作者，申请完整的设计序列数据。<Cite refs={["turn126840search1"]}/>

这是目前最直接的核查途径：取得完整序列池后，就能对四条候选进行精确匹配，并进一步计算它们与原论文全部候选的序列一致性和最小编辑距离。

**当前结论：** 在我已检索的公开网页及可见数据集记录中，四条候选都没有出现完全匹配记录；但原论文的完整 10,000 条序列尚未取得，因此它们是否与原论文中未公开的候选重复，仍然未知。