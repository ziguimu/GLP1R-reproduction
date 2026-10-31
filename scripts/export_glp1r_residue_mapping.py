import csv
from pathlib import Path
from Bio.PDB import PDBParser
from Bio.SeqUtils import seq1
from Bio.Align import PairwiseAligner

fasta_path = Path("data/GLP1R_7KI0_chainR.fasta")
pdb_path = Path("structures/GLP1R_7KI0_chainR.pdb")
output_path = Path("results/GLP1R_7KI0_residue_mapping.csv")

fasta_lines = fasta_path.read_text().splitlines()
fasta_seq = "".join(
    line.strip()
    for line in fasta_lines
    if line.strip() and not line.startswith(">")
).upper()

structure = PDBParser(QUIET=True).get_structure("GLP1R", str(pdb_path))
observed = [
    (r.id[1], r.id[2], seq1(r.resname))
    for r in structure[0]["R"].get_residues()
    if r.id[0] == " "
]
pdb_seq = "".join(item[2] for item in observed)

aligner = PairwiseAligner()
aligner.mode = "global"
aligner.match_score = 2
aligner.mismatch_score = -1
aligner.open_gap_score = -5
aligner.extend_gap_score = -0.1

alignment = aligner.align(fasta_seq, pdb_seq)[0]
coordinates = alignment.coordinates

rows = []
for k in range(coordinates.shape[1] - 1):
    f0, f1 = map(int, coordinates[0, k:k+2])
    p0, p1 = map(int, coordinates[1, k:k+2])

    if f1 > f0 and p1 > p0:
        for offset in range(min(f1 - f0, p1 - p0)):
            fasta_pos = f0 + offset + 1
            pdb_num, ins_code, pdb_aa = observed[p0 + offset]
            fasta_aa = fasta_seq[fasta_pos - 1]

            rows.append({
                "pdb_chain": "R",
                "pdb_residue_number": pdb_num,
                "pdb_insertion_code": ins_code.strip(),
                "fasta_position": fasta_pos,
                "pdb_amino_acid": pdb_aa,
                "fasta_amino_acid": fasta_aa,
                "match": pdb_aa == fasta_aa,
            })

with output_path.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("Saved:", output_path)
print("Rows:", len(rows))
print("Exact matches:", sum(row["match"] for row in rows))
print("Mismatches:", sum(not row["match"] for row in rows))
print("First mapping:", rows[0])
print("Last mapping:", rows[-1])
