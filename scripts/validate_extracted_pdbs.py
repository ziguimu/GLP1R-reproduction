from Bio.PDB import PDBParser
from pathlib import Path

parser = PDBParser(QUIET=True)

files = [
    Path("structures/semaglutide_7KI0_chainP.pdb"),
    Path("structures/GLP1R_7KI0_chainR.pdb"),
]

for path in files:
    structure = parser.get_structure(path.stem, str(path))
    chain = next(structure.get_models()).child_list[0]

    residues = list(chain.get_residues())
    protein_like = [
        r for r in residues
        if r.resname != "HOH"
    ]
    atom_count = sum(1 for _ in chain.get_atoms())
    residue_names = [r.resname for r in residues]

    print(f"\n===== {path.name} =====")
    print("Chain ID:", chain.id)
    print("Residue records:", len(residues))
    print("Residue names:", " ".join(residue_names))
    print("Atom count:", atom_count)
    print("Contains AIB:", "AIB" in residue_names)
    print("File size:", path.stat().st_size, "bytes")
