from pathlib import Path
import csv
import numpy as np
from Bio.PDB import PDBParser
from Bio.SeqUtils import seq1

ROOT = Path(__file__).resolve().parent.parent

PEPTIDE_PDB = ROOT / "structures/semaglutide_peptide_only_7KI0.pdb"
RECEPTOR_PDB = ROOT / "structures/GLP1R_7KI0_chainR.pdb"
MAPPING_CSV = ROOT / "results/GLP1R_7KI0_residue_mapping.csv"
OUT_DIR = ROOT / "results"

CUTOFFS = (4.0, 5.0)


def get_residue_key(residue):
    """返回可用于唯一识别残基的编号信息。"""
    hetflag, resseq, icode = residue.id
    return (resseq, str(icode).strip())


def get_heavy_atoms(residue):
    """排除氢原子和氘原子。"""
    return [
        atom for atom in residue.get_atoms()
        if atom.element.strip().upper() not in {"H", "D"}
    ]


def residue_label(residue):
    resname = residue.resname.strip()
    try:
        aa = seq1(resname, custom_map={"AIB": "X"})
    except Exception:
        aa = "X"
    return f"{aa}{residue.id[1]}({resname})"


def load_mapping(path):
    mapping = {}
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            key = (
                int(row["pdb_residue_number"]),
                row["pdb_insertion_code"].strip(),
            )
            mapping[key] = {
                "fasta_position": int(row["fasta_position"]),
                "fasta_amino_acid": row["fasta_amino_acid"],
                "match": row["match"].strip().lower() == "true",
            }
    return mapping


def main():
    for path in (PEPTIDE_PDB, RECEPTOR_PDB, MAPPING_CSV):
        if not path.exists():
            raise FileNotFoundError(f"Required file not found: {path}")

    parser = PDBParser(QUIET=True)
    peptide_structure = parser.get_structure("peptide", str(PEPTIDE_PDB))
    receptor_structure = parser.get_structure("receptor", str(RECEPTOR_PDB))

    peptide_residues = list(peptide_structure.get_residues())
    receptor_residues = list(receptor_structure.get_residues())
    mapping = load_mapping(MAPPING_CSV)

    # Collect heavy atoms while retaining the residue they belong to.
    peptide_atoms = []
    for residue in peptide_residues:
        for atom in get_heavy_atoms(residue):
            peptide_atoms.append((residue, atom))

    receptor_atoms = []
    for residue in receptor_residues:
        for atom in get_heavy_atoms(residue):
            receptor_atoms.append((residue, atom))

    peptide_xyz = np.array([atom.coord for _, atom in peptide_atoms])
    receptor_xyz = np.array([atom.coord for _, atom in receptor_atoms])

    if len(peptide_xyz) == 0 or len(receptor_xyz) == 0:
        raise ValueError("No heavy atoms found in one or both structures.")

    # Pairwise distances between peptide and receptor heavy atoms.
    distances = np.linalg.norm(
        peptide_xyz[:, None, :] - receptor_xyz[None, :, :],
        axis=2,
    )

    print("=== Input validation ===")
    print(f"Peptide residues: {len(peptide_residues)}")
    print(f"Peptide heavy atoms: {len(peptide_atoms)}")
    print(f"Receptor residues: {len(receptor_residues)}")
    print(f"Receptor heavy atoms: {len(receptor_atoms)}")
    print(f"Receptor residues mapped to FASTA: {len(mapping)}")
    print("Distance definition: minimum heavy-atom distance between residues")
    print()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for cutoff in CUTOFFS:
        atom_i, atom_j = np.where(distances <= cutoff)

        # Aggregate atom contacts by unique peptide/receptor residue pair.
        pair_data = {}
        for i, j in zip(atom_i, atom_j):
            pep_res, pep_atom = peptide_atoms[i]
            rec_res, rec_atom = receptor_atoms[j]

            pep_key = get_residue_key(pep_res)
            rec_key = get_residue_key(rec_res)
            pair_key = (pep_key, rec_key)

            distance = float(distances[i, j])
            if pair_key not in pair_data:
                pair_data[pair_key] = {
                    "peptide_residue": pep_res,
                    "receptor_residue": rec_res,
                    "atom_contact_count": 0,
                    "min_distance_A": distance,
                }

            pair_data[pair_key]["atom_contact_count"] += 1
            pair_data[pair_key]["min_distance_A"] = min(
                pair_data[pair_key]["min_distance_A"], distance
            )

        rows = []
        peptide_summary = {}

        for item in pair_data.values():
            pep_res = item["peptide_residue"]
            rec_res = item["receptor_residue"]
            pep_key = get_residue_key(pep_res)
            rec_key = get_residue_key(rec_res)

            rec_map = mapping.get(rec_key)
            if rec_map is None:
                fasta_position = ""
                fasta_aa = ""
                exact_match = ""
            else:
                fasta_position = rec_map["fasta_position"]
                fasta_aa = rec_map["fasta_amino_acid"]
                exact_match = rec_map["match"]

            rows.append({
                "cutoff_A": cutoff,
                "peptide_pdb_residue_number": pep_res.id[1],
                "peptide_residue": residue_label(pep_res),
                "receptor_pdb_chain": "R",
                "receptor_pdb_residue_number": rec_res.id[1],
                "receptor_residue": residue_label(rec_res),
                "receptor_fasta_position": fasta_position,
                "receptor_fasta_amino_acid": fasta_aa,
                "mapping_exact_match": exact_match,
                "atom_contact_count": item["atom_contact_count"],
                "minimum_heavy_atom_distance_A": round(
                    item["min_distance_A"], 3
                ),
            })

            if pep_key not in peptide_summary:
                peptide_summary[pep_key] = {
                    "residue": pep_res,
                    "receptor_keys": set(),
                    "atom_contact_count": 0,
                    "minimum_distance_A": item["min_distance_A"],
                }
            peptide_summary[pep_key]["receptor_keys"].add(rec_key)
            peptide_summary[pep_key]["atom_contact_count"] += (
                item["atom_contact_count"]
            )
            peptide_summary[pep_key]["minimum_distance_A"] = min(
                peptide_summary[pep_key]["minimum_distance_A"],
                item["min_distance_A"],
            )

        rows.sort(key=lambda r: (
            r["peptide_pdb_residue_number"],
            r["receptor_pdb_residue_number"],
        ))

        pair_path = OUT_DIR / f"GLP1R_semaglutide_contacts_{cutoff:g}A.csv"
        with pair_path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "cutoff_A",
                "peptide_pdb_residue_number",
                "peptide_residue",
                "receptor_pdb_chain",
                "receptor_pdb_residue_number",
                "receptor_residue",
                "receptor_fasta_position",
                "receptor_fasta_amino_acid",
                "mapping_exact_match",
                "atom_contact_count",
                "minimum_heavy_atom_distance_A",
            ])
            writer.writeheader()
            writer.writerows(rows)

        summary_path = OUT_DIR / f"GLP1R_semaglutide_peptide_summary_{cutoff:g}A.csv"
        with summary_path.open("w", newline="") as f:
            fields = [
                "cutoff_A",
                "peptide_pdb_residue_number",
                "peptide_residue",
                "number_of_receptor_residues_contacted",
                "atom_contact_count",
                "minimum_heavy_atom_distance_A",
            ]
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for pep_key, info in sorted(peptide_summary.items()):
                residue = info["residue"]
                writer.writerow({
                    "cutoff_A": cutoff,
                    "peptide_pdb_residue_number": residue.id[1],
                    "peptide_residue": residue_label(residue),
                    "number_of_receptor_residues_contacted": len(
                        info["receptor_keys"]
                    ),
                    "atom_contact_count": info["atom_contact_count"],
                    "minimum_heavy_atom_distance_A": round(
                        info["minimum_distance_A"], 3
                    ),
                })

        receptor_contacted = {
            key[1] for key in pair_data.keys()
        }
        peptide_contacted = {
            key[0] for key in pair_data.keys()
        }

        print(f"=== Cutoff: {cutoff:.1f} Å ===")
        print(f"Heavy-atom pairs within cutoff: {len(atom_i)}")
        print(f"Unique peptide–receptor residue pairs: {len(pair_data)}")
        print(f"Peptide residues with contacts: {len(peptide_contacted)}")
        print(f"Receptor residues with contacts: {len(receptor_contacted)}")
        print(f"Residue-pair table: {pair_path.relative_to(ROOT)}")
        print(f"Peptide summary: {summary_path.relative_to(ROOT)}")
        print()


if __name__ == "__main__":
    main()
