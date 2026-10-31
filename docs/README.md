# GLP-1R Semaglutide ProteinMPNN Reproduction

## 1. Project purpose

This project reproduces and audits the sequence-design and candidate-screening stages associated with the paper:

*AI-Driven De Novo Design of Ultra Long-Acting GLP-1 Receptor Agonists*  
Advanced Science (2025). DOI: [10.1002/advs.202507044](https://doi.org/10.1002/advs.202507044)

The project records the structures, ProteinMPNN sequence-generation outputs, screening procedures, and intermediate results. Reproduction status and deviations from the published workflow should be documented explicitly.

## 2. Current workflow and verified counts

| Stage | Records | Status |
|---|---:|---|
| ProteinMPNN-generated candidates | 10,000 | Generated across 50 batches |
| Unique sequences after deduplication | 1,435 | Count and total records checked |
| First cleavage-site screening | 787 retained | 648 rejected |
| Second cleavage-site screening | 308 retained | 479 rejected |
| Final retained sequence set | 308 | Length, residue alphabet, uniqueness, and audit-table consistency checked |

These counts describe the current local workflow. They do not, by themselves, establish equivalence to every step of the published paper.

## 3. Important unresolved issue: DV at positions 9–10

All 10,000 generated candidates have valine (V) at sequence position 10, so the DV motif at positions 9–10 is present in all candidates.

The saved fixed-position configuration does not list position 10 as fixed. However, the original generation command and complete runtime configuration have not been recovered, so the actual runtime design mask has not been independently verified.

This observation is unresolved. It must not be presented as proof that DV is biologically conserved or that ProteinMPNN is malfunctioning. The current screening workflow allowed DV; strict reproduction of the paper's cleavage-site filtering requires separate review.

See `../logs/2026-10-19_DV_site_investigation.md` for the investigation record.

## 4. Directory guide

- `data/`: input data and derived data, as present in the project.
- `docs/`: project overview and methodological documentation.
- `logs/`: dated run records, investigation notes, and analysis records.
- `references/`: literature and reference materials.
- `results/`: generated outputs, screening results, and analyses.
- `scripts/`: scripts used for processing and analysis.
- `structures/`: structural input files.

Directory descriptions indicate intended roles; they do not imply that every directory currently contains files.

## 5. Key records

- `../logs/2026-10-19_proteinmpnn_generation.md`: ProteinMPNN generation record.
- `../logs/2026-10-19_DV_site_investigation.md`: DV-site investigation and unresolved questions.
- `../logs/2026-10-19_interface_analysis.md`: interface-analysis record.

The backup file `2026-10-19_interface_analysis.md.bak-20261019-131326` is retained as-is and is not treated as the current primary record.

## 6. Reproducibility principles

1. Preserve original generation outputs and source files.
2. Keep screening scripts, audit tables, and retained/rejected sequence sets traceable to one another.
3. Distinguish directly verified observations from working hypotheses and unresolved questions.
4. Record deviations from the published procedure rather than silently treating them as equivalent.
5. Do not claim biological activity, receptor agonism, binding affinity, or in-vivo performance from sequence generation and computational screening alone.
