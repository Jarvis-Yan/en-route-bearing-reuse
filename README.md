# En Route Bearing Reuse

Supplementary material and saved-result analysis for **En Route Bearing Reuse for Complete Servicing of Radio Interference Sources**, by Jiarui Yan, Jie Lei, and Jingyi Xue.

## Supplement

- [Read Supplement S1](supplement/Supplement-S1.pdf)
- [LaTeX source](supplement/Supplement-S1.tex)
- [Version 1.0.0 release](https://github.com/Jarvis-Yan/en-route-bearing-reuse/releases/tag/v1.0.0)

S1 contains exact sensing-error definitions, geometric margins and recovery arguments, controller and adapted-control definitions, extended results, and technical provenance. Its references are self-contained. The accompanying main manuscript is being prepared for submission; this repository does not imply acceptance or publication by a conference.

## Reproduce the paired summaries

Use Python 3.12 (standard library only), from a downloaded or cloned copy:

```sh
python3 analysis/recompute.py
```

The script validates input checksums, recomputes gains from candidate and baseline times, includes every saved pair, and verifies the means, intervals, and faster/tied/slower counts against `analysis/expected-results.json`. Results are printed as JSON. It does not modify the inputs.

| Input | Comparison | Pairs | Mean reduction (%) | 95% seed-cluster interval (%) |
|---|---|---:|---:|---|
| `data/primary_check_pairs.csv` | Windowed reuse / immediate servicing | 840 | 5.103 | [4.558, 5.641] |
| `data/same_window_reuse_pairs.csv` | Reuse enabled / disabled at the same window | 840 | 6.421 | [5.861, 7.004] |
| `data/joint_reuse_pairs.csv` | Joint scheduling with / without reuse | 360 | 10.128 | [9.013, 11.245] |
| `data/joint_complete_pairs.csv` | Joint scheduling with reuse / immediate servicing | 360 | 13.636 | [12.488, 14.787] |

These files overlap in scenarios; their row counts must not be summed as independent samples. The primary and joint cohorts use 30 and 20 seed clusters, respectively. The first comparison was prespecified. The other three paired analyses are post hoc, and their intervals are descriptive and unadjusted for multiple comparisons. The primary and joint-reuse files also supply the paired task-time reductions plotted in Fig. 2 of the manuscript.

For each pair, the reduction is `100 * (1 - candidate_time / baseline_time)`. Reported means average the pair-level reductions, rather than computing a ratio of mean times. `data/protocol.json` records cluster order, random seeds, resampling counts, and input checksums. Resampling uses 10,000 draws of whole seed clusters; percentiles use linear interpolation.

## Data dictionary

| Column | Meaning |
|---|---|
| `key` | Scenario identifier within a comparison |
| `seed` | Master seed identifying the bootstrap cluster |
| `scenario` | Scenario-layout stratum; definitions are in S1 |
| `error` | Deterministic sensing-error model; definitions are in S1 |
| `candidate_time` | Candidate virtual task time, seconds |
| `baseline_time` | Baseline virtual task time, seconds |
| `gain_percent` | Pair-level task-time reduction, percent; negative means slower |
| `time_saved_seconds` | Baseline minus candidate virtual task time, seconds |

## Release scope and provenance

Version 1.0.0 publishes the supplement, four unmodified processed pair tables, their statistical configuration, and a standalone recomputation script. It supports verification of the four comparisons above. It does **not** contain the complete planner implementations, all 8,640 execution traces, or every extended-result input described in S1; it is not a full simulation-rerun package. No new simulations were run to produce this release. The script was adapted for standalone use from the retained paired-analysis workflow.

The task protocol and adopted completion and joint-scheduling mechanisms have external sources, documented in S1. Those sources are not presented as original contributions of this work. Original run-table hashes are recorded in `analysis/expected-results.json`; published CSV hashes are recorded separately, because processed pair tables differ from full run tables. Local filesystem paths and internal delivery records are excluded.

## Citation and rights

Cite this repository's versioned release using the metadata in [CITATION.cff](CITATION.cff). The release URL is a versioned GitHub record, not a DOI. `SHA256SUMS` identifies the published file contents.

The files are publicly accessible for inspection. No additional reuse license is granted by this release; rights in cited third-party materials remain with their respective owners.

## Build Supplement S1

In the `supplement` directory, run `pdflatex Supplement-S1.tex` twice using a standard TeX Live or MacTeX installation. The published PDF is provided for readers who do not have LaTeX installed.
