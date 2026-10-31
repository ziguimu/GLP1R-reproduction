from pathlib import Path
from collections import Counter
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import AlignIO

base = Path("/mnt/d/PRP/GLP1R_MSA")
raw_path = base / "glp1r_homologs_raw.fasta"
query_path = Path(
    "/mnt/d/PRP/GLP1R_reproduction/data/GLP1R_7KI0_chainR_395aa.fasta"
)

input_path = base / "glp1r_395aa_unique_input.fasta"
aligned_path = base / "glp1r_395aa_aligned.fasta"
a3m_path = base / "glp1r_395aa_custom.a3m"

allowed = set("ACDEFGHIKLMNPQRSTVWY")

query_records = list(SeqIO.parse(query_path, "fasta"))
if len(query_records) != 1:
    raise ValueError("Query FASTA 必须恰好包含一条序列。")

query = str(query_records[0].seq).upper()
if len(query) != 395 or set(query) - allowed:
    raise ValueError("Query 不是合法的 395 aa 标准氨基酸序列。")

raw_records = list(SeqIO.parse(raw_path, "fasta"))
if not raw_records:
    raise ValueError("原始同源序列文件为空。")

# 按序列去重；排除含未知或非标准字符的记录。
seen = {query}
unique_records = []
excluded_x = 0
excluded_other = 0
duplicate_count = 0

for rec in raw_records:
    seq = str(rec.seq).upper()

    if not seq:
        excluded_other += 1
        continue

    if "X" in seq:
        excluded_x += 1
        continue

    if set(seq) - allowed:
        excluded_other += 1
        continue

    if seq in seen:
        duplicate_count += 1
        continue

    seen.add(seq)
    # 使用原始 FASTA 的首字段作为简洁 ID。
    rid = rec.id.replace("|", "_")
    unique_records.append(SeqRecord(Seq(seq), id=rid, description=""))

# Query 放在最前，方便后续定位。
all_records = [
    SeqRecord(Seq(query), id="GLP1R_QUERY_395AA", description="")
] + unique_records

SeqIO.write(all_records, input_path, "fasta")

print("=== MSA 输入准备完成 ===")
print("原始同源记录:", len(raw_records))
print("含 X 排除:", excluded_x)
print("其他异常字符排除:", excluded_other)
print("重复记录排除:", duplicate_count)
print("保留的同源序列:", len(unique_records))
print("包括 query 的输入记录:", len(all_records))
print("Query 长度:", len(query))
print("输入文件:", input_path)
