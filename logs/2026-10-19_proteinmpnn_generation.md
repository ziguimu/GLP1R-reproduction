# GLP-1R ProteinMPNN Sequence Generation Record

Date: 2026-10-19
Project: GLP1R_reproduction
Stage: ProteinMPNN candidate sequence generation and validation

## 1. Input and design setup

- Reference complex: semaglutide-bound GLP-1R structure derived from PDB 7KI0.
- ProteinMPNN-compatible input: `GLP1R_semaglutide_ProteinMPNN_input_renumbered.pdb`.
- Model: `v_48_020`.
- Designed chain: P (peptide); fixed chain: R (receptor).
- Candidate peptide length in the generated FASTA files: 30 amino acids.
- Fixed peptide positions checked: 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 20, 28.
- All checked candidates matched the expected amino acids at these fixed positions.
- Full runtime parameters have not yet been independently verified from a preserved run command or log.

## 2. Generation and deduplication

- Batch folders inspected: `batch200_seed1` through `batch200_seed50`.
- Candidate records: 200 per batch, 10,000 total, excluding the first reference record in each FASTA.
- Unique sequences across all batches: 1,435.
- Duplicate excess records: 8,565 (85.65% of all candidate records).
- Per-batch unique sequence count: 104–130 out of 200.
- The original FASTA outputs and earlier deduplicated files were preserved.

## 3. Deduplicated outputs

- `results/proteinmpnn/test_2000seq_renumbered/deduplicated/unique_candidates_all50_v2.fasta`
- `results/proteinmpnn/test_2000seq_renumbered/deduplicated/sequence_counts_all50_v2.csv`

Validation of the deduplicated outputs:
- FASTA sequence count: 1,435.
- CSV row count: 1,435.
- Sum of CSV `count` values: 10,000.
- FASTA/CSV unique sequence consistency: passed.
- Fixed-position validation: passed.

## 4. Interpretation and limitations

- The generated sequences and their frequencies describe ProteinMPNN sampling output only.
- Repeated sequences indicate sampling concentration; they do not establish binding, receptor activation, potency, stability, or pharmacological activity.
- The high-frequency sequence patterns merit further analysis, but the cause of the observed distribution has not been established.
- The peptide structure contains 30 coordinate-supported residues, while the full polymer sequence contains 31 positions; these outputs remain 30 residues long. No missing residue was appended during deduplication.
- This record documents computational sequence generation and validation, not experimental validation.

## 5. Run metadata cross-check

- Checked FASTA headers for all 50 batch outputs.
- All 50 headers matched their expected seed number.
- All 50 headers reported model `v_48_020`, fixed chain `R`, and designed chain `P`.
- Candidate records show the sampling temperature marker `T=0.1`.
- The model identifier recorded in the FASTA header is `8907e6671bfbfc92303b5f79c4b5e6ce47cdef57`.
- This check validates output metadata, not every runtime argument. The original batch command or run script was not found; consistency of all parameters such as `num_seq_per_target` and `batch_size` remains unverified.
