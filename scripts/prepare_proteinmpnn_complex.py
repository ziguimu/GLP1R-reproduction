from pathlib import Path
from Bio.PDB import PDBParser, PDBIO, Select

ROOT = Path("/mnt/d/PRP/GLP1R_reproduction")
RECEPTOR = ROOT / "structures/GLP1R_7KI0_chainR.pdb"
PEPTIDE = ROOT / "structures/semaglutide_peptide_only_7KI0.pdb"
OUTPUT = ROOT / "structures/GLP1R_semaglutide_ProteinMPNN_input.pdb"

parser = PDBParser(QUIET=True)
receptor = parser.get_structure("receptor", str(RECEPTOR))
peptide = parser.get_structure("peptide", str(PEPTIDE))

# Create a fresh structure using the receptor model, then add the peptide chain.
model = receptor[0]
peptide_chain = peptide[0]["P"].copy()

# ProteinMPNN's PDB parser reads ATOM records and standard amino-acid names.
# AIB is approximated as ALA in this model-only copy:
# rename AIB to ALA, retain N/CA/C/O, and map one beta-methyl carbon to CB.
for residue in peptide_chain:
    if residue.resname == "AIB":
        residue.resname = "ALA"

        # AIB has two beta-methyl carbon atoms (CB1/CB2).
        # Keep CB1 as the Ala CB; remove CB2 from this approximate input.
        if "CB1" in residue:
            atom = residue["CB1"].copy()
            atom.id = "CB"
            atom.name = "CB"
            atom.fullname = " CB "
            residue.detach_child("CB1")
            residue.add(atom)

        if "CB2" in residue:
            residue.detach_child("CB2")

        # Any remaining non-standard atom names are not needed for Ala.
        for atom_name in list(residue.child_dict):
            if atom_name not in {"N", "CA", "C", "O", "CB"}:
                residue.detach_child(atom_name)

model.add(peptide_chain)

class KeepProteinChains(Select):
    def accept_chain(self, chain):
        return chain.id in {"R", "P"}

    def accept_residue(self, residue):
        return residue.resname not in {"HOH", "WF1"}

io = PDBIO()
io.set_structure(receptor)
io.save(str(OUTPUT), KeepProteinChains())

# Validate output chain IDs and residue counts.
check = parser.get_structure("check", str(OUTPUT))
print("输出文件:", OUTPUT)
for chain in check[0]:
    residues = list(chain.get_residues())
    print(f"链 {chain.id}: {len(residues)} 个有坐标残基")
    if chain.id == "P":
        print("肽链残基名:", " ".join(r.resname for r in residues))
        print("AIB 是否仍存在:", any(r.resname == "AIB" for r in residues))
        print("末端残基:", residues[-1].resname, residues[-1].id)
print("说明：该文件将 AIB 近似映射为 ALA；未添加缺失的末端 Gly。")
