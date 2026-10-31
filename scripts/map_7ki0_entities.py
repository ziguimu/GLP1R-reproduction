from Bio.PDB.MMCIF2Dict import MMCIF2Dict

c = MMCIF2Dict("structures/7KI0.cif")

seq_by_entity = {
    entity: seq.replace("\n", "").replace(" ", "")
    for entity, seq in zip(
        c["_entity_poly.entity_id"],
        c["_entity_poly.pdbx_seq_one_letter_code_can"]
    )
}

author_by_entity = dict(zip(
    c["_entity_poly.entity_id"],
    c["_entity_poly.pdbx_strand_id"]
))

print("label_chain | entity | author_chain | length")
for label, entity in zip(
    c["_struct_asym.id"],
    c["_struct_asym.entity_id"]
):
    if entity in seq_by_entity:
        seq = seq_by_entity[entity]
        print(
            f"{label:>11} | {entity:>6} | "
            f"{author_by_entity[entity]:>12} | {len(seq)}"
        )
