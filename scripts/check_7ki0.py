from Bio.PDB.MMCIF2Dict import MMCIF2Dict

cif = MMCIF2Dict("structures/7KI0.cif")

print("===== Chain mapping =====")
for chain, entity in zip(cif["_struct_asym.id"], cif["_struct_asym.entity_id"]):
    print(f"label chain {chain}: entity {entity}")

print("\n===== Polymer sequences =====")
for chain, seq in zip(
    cif["_entity_poly.pdbx_strand_id"],
    cif["_entity_poly.pdbx_seq_one_letter_code_can"]
):
    seq = seq.replace("\n", "").replace(" ", "")
    print(f"author chain(s)={chain}, length={len(seq)}, sequence={seq}")
