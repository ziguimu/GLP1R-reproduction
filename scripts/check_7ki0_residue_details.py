from Bio.PDB import MMCIFParser

structure = MMCIFParser(QUIET=True).get_structure(
    "7KI0", "structures/7KI0.cif"
)

for chain_id in ("P", "R"):
    chain = structure[0][chain_id]
    residues = list(chain.get_residues())
    standard = [r for r in residues if r.id[0] == " "]

    print(f"\n===== Chain {chain_id} =====")
    print("First 15 residues:")
    print([(r.id[1], r.resname) for r in residues[:15]])

    print("Last 15 residues:")
    print([(r.id[1], r.resname) for r in residues[-15:]])

    nonstandard = [
        (r.id, r.resname) for r in residues if r.id[0] != " "
    ]
    print("Non-standard/hetero records:", nonstandard[:20])

    numbers = sorted(r.id[1] for r in standard)
    gaps = [
        (a, b) for a, b in zip(numbers, numbers[1:])
        if b > a + 1
    ]
    print("Numbering gaps (first 20):", gaps[:20])
    print("Standard residue count:", len(standard))
