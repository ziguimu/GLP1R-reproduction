from Bio.PDB import MMCIFParser

path = "structures/7KI0.cif"
structure = MMCIFParser(QUIET=True).get_structure("7KI0", path)
model = structure[0]

print("===== Parsed structure chains =====")
for chain in model:
    residues = list(chain.get_residues())
    standard = [r for r in residues if r.id[0] == " "]
    print(
        f"chain={chain.id!r} | "
        f"residues={len(residues)} | "
        f"standard_residues={len(standard)}"
    )
