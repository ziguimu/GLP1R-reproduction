from Bio.PDB import MMCIFParser, PDBIO, Select
from pathlib import Path

source = "structures/7KI0.cif"
out_dir = Path("structures")
structure = MMCIFParser(QUIET=True).get_structure("7KI0", source)

class ProteinChainSelect(Select):
    def __init__(self, chain_id):
        self.chain_id = chain_id

    def accept_chain(self, chain):
        return chain.id == self.chain_id

    def accept_residue(self, residue):
        # 保留标准残基以及 AIB 等非标准氨基酸；
        # 排除水分子和其他异源分子。
        return residue.resname != "HOH" and residue.id[0] != "W"

for chain_id, filename in [
    ("P", "semaglutide_7KI0_chainP.pdb"),
    ("R", "GLP1R_7KI0_chainR.pdb"),
]:
    io = PDBIO()
    io.set_structure(structure)
    output = out_dir / filename
    io.save(str(output), ProteinChainSelect(chain_id))
    print(f"Saved: {output}")
