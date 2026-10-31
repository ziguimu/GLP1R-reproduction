from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from pathlib import Path

cif = MMCIF2Dict("structures/7KI0.cif")

seq_by_entity = dict(zip(
    cif["_entity_poly.entity_id"],
    cif["_entity_poly.pdbx_seq_one_letter_code_can"]
))
entity_by_label = dict(zip(
    cif["_struct_asym.id"],
    cif["_struct_asym.entity_id"]
))

# label chain E = Semaglutide；label chain F = GLP-1R
targets = {
    "E": ("semaglutide_7KI0_chainP", "Semaglutide peptide as recorded in PDB 7KI0"),
    "F": ("GLP1R_7KI0_chainR", "GLP-1 receptor construct as recorded in PDB 7KI0"),
}

out = Path("data")
out.mkdir(exist_ok=True)

for label, (name, description) in targets.items():
    entity = entity_by_label[label]
    seq = seq_by_entity[entity].replace("\n", "").replace(" ", "")
    path = out / f"{name}.fasta"
    path.write_text(f">{name} | {description}\n{seq}\n")
    print(f"{path}: {len(seq)} aa")
