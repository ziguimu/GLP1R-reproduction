from pathlib import Path
import re
import numpy as np
import pandas as pd

ROOT = Path("/mnt/d/PRP/GLP1R_Boltz2_20261022")
AUDIT = ROOT / "audit" / "structure"

BOLTZ_FILE = ROOT / "boltz_sample_metrics.csv"
STRUCTURE_FILE = AUDIT / "receptor_tmscore_vs_7KI0.csv"

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
