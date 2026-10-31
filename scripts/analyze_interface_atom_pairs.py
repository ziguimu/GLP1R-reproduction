import csv
from pathlib import Path

import numpy as np
from Bio.PDB import PDBParser

ROOT = Path(".")
PEPTIDE_PDB = ROOT / "structures/semaglutide_peptide_only_7KI0.pdb"
RECEPTOR_PDB = ROOT / "structures/GLP1R_7KI0_chainR.pdb"
CONTACT_CSV = ROOT / "results/GLP1R_semaglutide_contacts_4A.csv"
MAPPING_CSV = ROOT / "results/GLP1R_7KI0_residue_mapping.csv"
OUTPUT_CSV = ROOT / "results/GLP1R_semaglutide_nearest_atom_pairs_4A.csv"

# 这些是肽链的 PDB 残基编号，不是肽序列位置
FOCUS_PEPTIDE_PDB_RESIDUES = {7, 9, 12, 21, 29}


def load_structure(path):
    parser = PDBParser(QUIET=True)
    return parser.get_structure(path.stem, str(path))[0]


def get_chain(model, chain_id):
    if chain_id not in model:
        raise ValueError(
            f"在结构中找不到链 {chain_id}；"
            f"实际链 ID 为：{list(model.child_dict.keys())}"
        )
    return model[chain_id]


def heavy_atoms(residue):
    """返回残基中的重原子，排除氢原子。"""
    result = []
    for atom in residue.get_atoms():
        element = (atom.element or "").strip().upper()
        name = atom.get_name().strip().upper()

        if element:
            is_hydrogen = element in {"H", "D"}
        else:
            is_hydrogen = name.startswith(("H", "D"))

        if not is_hydrogen:
            result.append(atom)

    return result


def residue_by_number(chain, residue_number):
    matches = [
        residue for residue in chain.get_residues()
        if residue.id[1] == residue_number
    ]
    if len(matches) != 1:
        raise ValueError(
            f"链 {chain.id} 中，残基编号 {residue_number} "
            f"匹配到 {len(matches)} 个残基，无法唯一确定。"
        )
    return matches[0]


def main():
    for path in [
        PEPTIDE_PDB, RECEPTOR_PDB, CONTACT_CSV, MAPPING_CSV
    ]:
        if not path.exists():
            raise FileNotFoundError(f"缺少输入文件：{path}")

    peptide_model = load_structure(PEPTIDE_PDB)
    receptor_model = load_structure(RECEPTOR_PDB)

    peptide_chain = get_chain(peptide_model, "P")
    receptor_chain = get_chain(receptor_model, "R")

    # 建立：受体 FASTA 位置 -> 受体 PDB 残基编号
    with MAPPING_CSV.open(newline="") as f:
        mapping_rows = list(csv.DictReader(f))

    fasta_to_pdb = {}
    for row in mapping_rows:
        fasta_pos = int(row["fasta_position"])
        pdb_num = int(row["pdb_residue_number"])
        fasta_to_pdb[fasta_pos] = pdb_num

    # 读取原有 4 Å 接触表，仅分析指定的肽残基
    with CONTACT_CSV.open(newline="") as f:
        contact_rows = list(csv.DictReader(f))

    unique_pairs = {}
    for row in contact_rows:
        pep_num = int(row["peptide_pdb_residue_number"])
        if pep_num not in FOCUS_PEPTIDE_PDB_RESIDUES:
            continue

        receptor_fasta_pos = int(row["receptor_fasta_position"])
        key = (pep_num, receptor_fasta_pos)
        unique_pairs[key] = row

    output_rows = []

    for (pep_num, receptor_fasta_pos), contact in sorted(unique_pairs.items()):
        receptor_pdb_num = fasta_to_pdb[receptor_fasta_pos]

        pep_res = residue_by_number(peptide_chain, pep_num)
        rec_res = residue_by_number(receptor_chain, receptor_pdb_num)

        pep_atoms = heavy_atoms(pep_res)
        rec_atoms = heavy_atoms(rec_res)

        if not pep_atoms or not rec_atoms:
            raise ValueError(
                f"残基缺少重原子：peptide PDB {pep_num}, "
                f"receptor PDB {receptor_pdb_num}"
            )

        # 搜索两个残基之间距离最短的重原子对
        best = None
        for pep_atom in pep_atoms:
            for rec_atom in rec_atoms:
                distance = float(
                    np.linalg.norm(pep_atom.coord - rec_atom.coord)
                )
                if best is None or distance < best[0]:
                    best = (distance, pep_atom, rec_atom)

        distance, pep_atom, rec_atom = best

        output_rows.append({
            "peptide_sequence_position": pep_num - 6,
            "peptide_pdb_residue_number": pep_num,
            "peptide_residue": contact["peptide_residue"],
            "peptide_atom": pep_atom.get_name(),
            "receptor_fasta_position": receptor_fasta_pos,
            "receptor_pdb_residue_number": receptor_pdb_num,
            "receptor_residue": contact["receptor_residue"],
            "receptor_atom": rec_atom.get_name(),
            "minimum_heavy_atom_distance_A": f"{distance:.3f}",
            "within_4A": distance <= 4.0,
        })

    fieldnames = [
        "peptide_sequence_position",
        "peptide_pdb_residue_number",
        "peptide_residue",
        "peptide_atom",
        "receptor_fasta_position",
        "receptor_pdb_residue_number",
        "receptor_residue",
        "receptor_atom",
        "minimum_heavy_atom_distance_A",
        "within_4A",
    ]

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"分析完成：{len(output_rows)} 个残基对")
    print(f"结果文件：{OUTPUT_CSV}")
    print()
    print(
        "肽序列位点 | 肽残基 | 肽原子 | 受体 FASTA 位点 | "
        "受体残基 | 受体原子 | 最短距离 (A)"
    )

    for row in output_rows:
        print(
            f'{row["peptide_sequence_position"]:>12} | '
            f'{row["peptide_residue"]:>8} | '
            f'{row["peptide_atom"]:>7} | '
            f'{row["receptor_fasta_position"]:>15} | '
            f'{row["receptor_residue"]:>8} | '
            f'{row["receptor_atom"]:>8} | '
            f'{row["minimum_heavy_atom_distance_A"]:>15}'
        )


if __name__ == "__main__":
    main()
