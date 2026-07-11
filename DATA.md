# Data provenance

All data derive from a single public cohort. **No raw sequencing reads are redistributed here** —
only derived tables. Re-fetch raw data from ENA if needed.

## Source cohort

- **BioProject:** PRJEB37731 (European Nucleotide Archive)
- **Description:** Danish cohort, dense **daily** vaginal shotgun metagenomic sampling
- **Subjects:** 40
- **Access:** public

## Derived files in `data/`

| File | What it is | How produced |
|---|---|---|
| `cst_calls.csv` | Per-sample community state type (CST) via VALENCIA, plus next-day CST and 1-day transition labels; host covariates | Taxonomic profiling of shotgun reads → species relative abundance → VALENCIA nearest-centroid CST assignment |
| `modeling_dataset.parquet` / `.csv` | 967 consecutive day-pairs × 209 columns: CLR-transformed species abundances + covariates (contraception, age, BMI, menstrual-cycle day) + labels `y_transition`, `y_into_IV` | Assembled from `cst_calls.csv`; each day *t* paired with day *t+1* |
| `valencia_taxon_mapping.csv` | Mapping of pipeline taxa to VALENCIA reference taxa | VALENCIA reference alignment |

## Label definitions

- **`y_transition`** — 1 if the coarse CST changes from day *t* to *t+1* (n=967, 63.6% positive).
- **`y_into_IV`** — defined **only for non-dysbiotic baselines** (day *t* CST ≠ IV): 1 if day *t+1* is CST IV.
  n=698, 27.7% positive. Rows where today is already CST IV are excluded, so this measures genuine
  *new onset*, not persistence.

## Important caveats

- **Single cohort, no external validation.** Public vaginal metagenomics with linked longitudinal
  outcomes is scarce; generalisation is untested.
- **CST calls depend on the taxonomic pipeline.** VALENCIA concordance (93.1%) mitigates but does not
  remove this dependence.
- **Boundary noise.** A share of daily "transitions" reflects CST scoring-boundary flicker rather than
  true biological change; this caps how predictable day-to-day onset can be.
