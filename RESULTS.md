# CellScope | Results and interpretation

The following are **computed from the actual dataset** with `analysis.py`; no synthetic samples or estimated clinical outcomes are used.

- Total labeled image specimens: **569**.
- Benign: **357 (62.7%)**.
- Malignant: **212 (37.3%)**.
- Missing cells in included source features: **0**.

## Mean-radius comparison

| Diagnostic label | Samples | Mean radius | Median radius | Std. dev. |
|---|---:|---:|---:|---:|
| Benign | 357 | 12.147 | 12.200 | 1.781 |
| Malignant | 212 | 17.463 | 17.325 | 3.204 |

## What worked

- Loaded locally bundled public data without an API key.
- Verified 569 unique IDs, 30 features, diagnostic labels, and no missing values.
- Built group comparisons with unit tests and an interactive explorer.
- Created a visual preview using genuine dataset values.

## Interpretation and limitations

The malignant-labeled observations have a larger mean radius on average in this dataset. The scatter plot shows overlap: a single feature cannot be interpreted as a diagnosis. Because the sample was assembled for a specific diagnostic study, its label proportions **are not population cancer rates**. The data contain no time-series or patient demographic variables, so no changes over time or demographic claims are made.

## What I would improve next

1. Quantify feature separability with uncertainty intervals and multiple-testing awareness.
2. Add accessible plot annotations and clearer original measurement definitions.
3. Conduct a separately scoped, leakage-aware predictive modeling exercise with cross-validation; never frame model scores as clinical validity.
4. Invite domain experts to critique presentation and bias.
