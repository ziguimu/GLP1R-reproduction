from Bio.PDB import PDBParser

path = "structures/GLP1R_7KI0_chainR.pdb"
structure = PDBParser(QUIET=True).get_structure("GLP1R", path)
chain = structure[0]["R"]

residues = [
    r for r in chain.get_residues()
    if r.id[0] == " " and r.resname != "HOH"
]

numbers = [r.id[1] for r in residues]
segments = []
start = previous = numbers[0]

for n in numbers[1:]:
    if n != previous + 1:
        segments.append((start, previous))
        start = n
    previous = n
segments.append((start, previous))

print("Observed standard amino-acid residues:", len(residues))
print("Observed residue-number segments:")
for a, b in segments:
    print(f"  {a}-{b} ({b-a+1} residues)")
