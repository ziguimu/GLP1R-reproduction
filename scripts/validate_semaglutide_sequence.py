from pathlib import Path
from Bio.PDB import PDBParser
from Bio.SeqUtils import seq1

lines = Path("data/semaglutide_7KI0_chainP.fasta").read_text().splitlines()
fasta = "".join(
    line.strip() for line in lines
    if line.strip() and not line.startswith(">")
).upper()

structure = PDBParser(QUIET=True).get_structure(
    "peptide", "structures/semaglutide_peptide_only_7KI0.pdb"
)
residues = list(structure[0]["P"].get_residues())

pdb_sequence = "".join(
    "A" if r.resname == "AIB" else seq1(r.resname)
    for r in residues
)

print("FASTA length:", len(fasta))
print("PDB residue count:", len(residues))
print("FASTA sequence:", fasta)
print("PDB sequence (AIB represented as A):", pdb_sequence)
print("Sequences match:", fasta == pdb_sequence)
print("PDB residues:", " ".join(
    f"{r.id[1]}:{r.resname}" for r in residues
))
