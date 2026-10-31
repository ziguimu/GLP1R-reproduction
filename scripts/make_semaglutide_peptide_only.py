from Bio.PDB import MMCIFParser, PDBIO, Select
from pathlib import Path

source = "structures/7KI0.cif"
output = Path("structures/semaglutide_peptide_only_7KI0.pdb")

structure = MMCIFParser(QUIET=True).get_structure("7KI0", source)

class PeptideOnlySelect(Select):
    def accept_chain(self, chain):
        return chain.id == "P"

    def accept_residue(self, residue):
        # 保留链 P 中的氨基酸，包括非标准氨基酸 AIB；
        # 排除 WF1 脂肪链修饰基团和水分子。
        return residue.resname not in {"WF1", "HOH"} and residue.id[0] != "W"

io = PDBIO()
io.set_structure(structure)
io.save(str(output), PeptideOnlySelect())

print(f"Saved: {output}")

from Bio.PDB import PDBParser
check = PDBParser(QUIET=True).get_structure("peptide", str(output))
chain = check[0]["P"]
residues = list(chain.get_residues())

print("Chain:", chain.id)
print("Residue count:", len(residues))
print("Residues:", " ".join(r.resname for r in residues))
print("AIB retained:", any(r.resname == "AIB" for r in residues))
print("WF1 retained:", any(r.resname == "WF1" for r in residues))
