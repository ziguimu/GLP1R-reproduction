from Bio.PDB import PDBParser
from Bio.SeqUtils import seq1
from Bio.Align import PairwiseAligner
from pathlib import Path

fasta_path = Path("data/GLP1R_7KI0_chainR.fasta")
pdb_path = Path("structures/GLP1R_7KI0_chainR.pdb")

fasta_lines = fasta_path.read_text().splitlines()
fasta_seq = "".join(
    line.strip() for line in fasta_lines
    if line.strip() and not line.startswith(">")
).upper()

structure = PDBParser(QUIET=True).get_structure("GLP1R", str(pdb_path))
chain = structure[0]["R"]

observed = []
for residue in chain.get_residues():
    if residue.id[0] == " ":
        aa = seq1(residue.resname)
        observed.append((residue.id[1], residue.id[2], aa))

pdb_seq = "".join(item[2] for item in observed)

aligner = PairwiseAligner()
aligner.mode = "global"
aligner.match_score = 2
aligner.mismatch_score = -1
aligner.open_gap_score = -5
aligner.extend_gap_score = -0.1

alignment = aligner.align(fasta_seq, pdb_seq)[0]
coords = alignment.coordinates

pairs = []
for k in range(coords.shape[1] - 1):
    f0, f1 = map(int, coords[0, k:k+2])
    p0, p1 = map(int, coords[1, k:k+2])

    # 只有两条序列都连续前进的区段才逐位对应
    if f1 > f0 and p1 > p0:
        for offset in range(min(f1 - f0, p1 - p0)):
            fasta_pos = f0 + offset + 1
            pdb_index = p0 + offset
            pdb_num, ins_code, aa = observed[pdb_index]
            pairs.append(
                (pdb_num, fasta_pos, aa, fasta_seq[fasta_pos - 1])
            )

print("FASTA sequence length:", len(fasta_seq))
print("Observed PDB sequence length:", len(pdb_seq))
print("Alignment score:", alignment.score)
print("Aligned residue pairs:", len(pairs))
print("Exact matches:", sum(a == b for _, _, a, b in pairs))

print("\nFirst 12 mappings: PDB residue -> FASTA position")
for pdb_num, fasta_pos, pdb_aa, fasta_aa in pairs[:12]:
    print(f"  {pdb_num} -> {fasta_pos}: {pdb_aa}/{fasta_aa}")

print("\nLast 12 mappings:")
for pdb_num, fasta_pos, pdb_aa, fasta_aa in pairs[-12:]:
    print(f"  {pdb_num} -> {fasta_pos}: {pdb_aa}/{fasta_aa}")

mismatches = [
    (pdb_num, fasta_pos, pdb_aa, fasta_aa)
    for pdb_num, fasta_pos, pdb_aa, fasta_aa in pairs
    if pdb_aa != fasta_aa
]
print("\nMismatched aligned pairs:", len(mismatches))
for row in mismatches[:20]:
    print(f"  PDB {row[0]} -> FASTA {row[1]}: {row[2]}/{row[3]}")
