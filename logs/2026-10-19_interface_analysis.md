# GLP-1R Reference Interface Analysis

Date: 2026-10-19
Project: GLP1R_reproduction
Stage: Semaglutide-bound reference structure and interface analysis

## 1. Reference structure

- Structure: PDB 7KI0
- Receptor chain used: author chain R
- Peptide chain used: author chain P
- Peptide: semaglutide
- Receptor chain contains 384 observed standard residues.
- Receptor residue mapping: 384/384 observed residues mapped to the receptor FASTA.
- Peptide coordinate model contains 30 residues; the full polymer sequence contains 31 positions. The final Gly is present in the sequence record but has no coordinates in the extracted peptide structure.

## 2. Generated analysis files

- `results/GLP1R_7KI0_residue_mapping.csv`
- `results/GLP1R_semaglutide_contacts_4A.csv`
- `results/GLP1R_semaglutide_contacts_5A.csv`
- `results/GLP1R_semaglutide_peptide_summary_4A.csv`
- `results/GLP1R_semaglutide_peptide_summary_5A.csv`
- `results/GLP1R_semaglutide_nearest_atom_pairs_4A.csv`

Analysis scripts include:
- `scripts/analyze_glp1r_interface.py`
- `scripts/analyze_interface_atom_pairs.py`

## 3. Heavy-atom contact analysis

Using heavy-atom distance cutoffs:

- 4 Å: 196 heavy-atom pairs, 60 unique peptide–receptor residue pairs.
- 5 Å: 832 heavy-atom pairs, 108 unique peptide–receptor residue pairs.
- At 4 Å, 24 peptide residues and 40 receptor residues participate in contacts.

These are geometric contact counts, not binding-energy estimates or experimental activity measurements.

## 4. Example interface observations

Selected peptide positions and nearby receptor FASTA positions:

- Peptide position 1 (His): receptor positions 243, 246, 315, 318, 319 and 322.
- Peptide position 3 (Glu): receptor positions 161, 199, 397 and 400.
- Peptide position 6 (Phe): receptor positions 150, 153 and 157, among others.
- Peptide position 15 (Glu): receptor positions 39, 40, 41 and 308.
- Peptide position 23 (Ile): receptor positions 97–100.

Selected minimum heavy-atom distances:

- Peptide Glu position 3 OE1 – receptor Arg FASTA position 199 NH2: 2.691 Å.
- Peptide Glu position 15 OE1 – receptor Arg FASTA position 308 NE: 2.870 Å.
- Peptide Glu position 3 OE2 – receptor Tyr FASTA position 161 OH: 2.580 Å.
- Peptide Glu position 15 OE2 – receptor Ser FASTA position 40 OG: 3.031 Å.

These close contacts are candidates for further chemical-geometry inspection. Distance alone does not establish a hydrogen bond or salt bridge.

## 5. Current limitations

- Neither extracted structure contains explicit hydrogen atoms.
- Hydrogen-bond angles have not been evaluated.
- No binding free energy, experimental affinity, or agonist activity was calculated in this stage.
- Structural proximity does not prove that a residue is functionally essential.
- Peptide residue numbering in the PDB differs from peptide sequence position. For the analyzed peptide, sequence position = PDB author residue number - 6.
- Receptor positions reported as FASTA positions are mapped separately from receptor PDB residue numbers.

## 6. Interpretation

This stage establishes a reproducible geometric description of the semaglutide–GLP-1R reference interface. It provides a structural reference for later candidate design and comparison, but it does not by itself validate a new peptide's binding affinity or agonist function.

## 7. Next step

Review the reference interface and analysis scripts, then define a cautious candidate-comparison protocol before starting new sequence design. Preserve the distinction between structural plausibility and experimentally established agonism.

## 8. Input-file consistency check (2026-10-19)

Compared the two extracted peptide-chain files:

- `structures/semaglutide_7KI0_chainP.pdb`: 31 residue records, 256 atoms; includes `AIB` and `WF1`.
- `structures/semaglutide_peptide_only_7KI0.pdb`: 30 residue records, 236 atoms; includes `AIB` and excludes `WF1`.

The difference in residue and atom counts is consistent with the explicit `WF1` exclusion in `scripts/make_semaglutide_peptide_only.py`.

`scripts/analyze_glp1r_interface.py` explicitly uses:
- `structures/semaglutide_peptide_only_7KI0.pdb`
- `structures/GLP1R_7KI0_chainR.pdb`

The interface analysis was rerun successfully using these configured paths. The shared atoms' coordinates across the two peptide files have not yet been compared atom by atom. The two files should not be treated as interchangeable without further validation.

## 9. Shared-atom coordinate comparison (2026-10-19)

Compared atom identities using residue identifier, residue name, atom name, and element.

- Original chain-P file: 256 atoms.
- Peptide-only analysis file: 236 atoms.
- Shared atom keys: 236.
- Atoms only in the original file: 20.
- Atoms only in the peptide-only file: 0.
- Maximum coordinate difference among shared atoms: 0.000000 Å.
- Shared atoms differing by more than 0.001 Å: 0.

This confirms that all 236 atoms retained in the peptide-only file have matching coordinates in the original chain-P file. The 20 additional atoms in the original file are consistent with the previously identified `WF1` residue. This is a file-consistency check, not an independent validation of the biological interpretation of the reference structure.

## 10. Receptor residue mapping validation (2026-10-19)

Inspected `results/GLP1R_7KI0_residue_mapping.csv`.

- Total mapping records: 384.
- Exact amino-acid matches: 384.
- Amino-acid mismatches: 0.
- PDB residue-number range: 29–423.
- Receptor construct FASTA-position range: 38–432.

All records in the mapping table have matching amino-acid identities at the mapped positions. PDB residue numbering and construct FASTA numbering must remain distinct. The mapping should be used directly rather than assuming a constant numerical offset. This validation applies only to positions represented in the mapping table and does not establish complete coverage of the native receptor sequence.

## 11. Reference interface coverage at a 4 Å cutoff (2026-10-19)

Inspected `results/GLP1R_semaglutide_contacts_4A.csv`.

- Contact records: 60.
- Distinct peptide residues involved: 24.
- Distinct receptor PDB residues involved: 40.
- Distinct receptor construct FASTA positions involved: 40.
- Records with non-exact receptor mapping: 0.

The contact table records peptide–receptor residue pairs with heavy-atom contacts within the 4.0 Å cutoff. These records are geometric descriptors, not counts of hydrogen bonds, binding-energy contributions, or experimentally verified functional interactions.

The receptor FASTA positions represented in the table are:
39, 40, 41, 44, 48, 77, 78, 97, 98, 99, 100, 130, 132, 147, 150, 153, 157, 161, 199, 206, 210, 214, 219, 223, 239, 243, 246, 307, 308, 309, 315, 318, 319, 322, 381, 389, 393, 396, 397, 400.

## 12. Candidate-input inventory (2026-10-19)

Inspected project files to a maximum depth of four, excluding Git internals, the reference mmCIF file, and the results directory.

The inspected project currently contains:
- The 7KI0 reference structure and extracted receptor/peptide PDB files.
- Receptor and semaglutide FASTA files.
- Reference-interface analysis scripts and result tables.
- The existing interface-analysis log.

No candidate peptide sequence files or candidate predicted structures were found in the inspected file inventory.

This is an inventory of the inspected project directory, not proof that no candidate materials exist elsewhere on the computer or in external storage. Candidate comparison and ranking have not started.
