# Evaluation Metrics & Success Criteria

## Primary Metric

**MAE on log-price** (`ln(actual_worth)`), reported as its implied typical relative error: `e^MAE − 1`.

- Why: prices span ~6 orders of magnitude (median 1.36M, max 3.8B AED). Log-MAE behaves like a **percentage error**: equal weight to a 10% miss on a studio and a penthouse.
- An error of 0.20 in ln-space ≈ ±20% typical price error — directly interpretable by stakeholders.

## Secondary Metrics

| Metric | Role | Why | Limitation |
|---|---|---|---|
| Median Absolute Error (log → %) | Typical-case error, robustness check | Immune to outlier skew; shows what the "average property" experiences | Says nothing about worst cases |
| RMSE (log) | Large-miss detector (monitor only) | Penalizes big misses more than MAE | Still outlier-sensitive even in log space; never optimize blindly |
| MAPE (price) + MdAPE | Business-facing % error | Directly quotable ("predictions off by X%") | Undefined/explosive near-zero targets → report median form or apply a price floor |
| R² (log-price) | Variance-explained sanity check | Quick health signal vs constant/naive models | Not comparable across segments; ignores business cost of errors |
| `meter_sale_price` metrics per segment | Cross-check lens (issue #7) | Confirms model isn't gaming size effects | Derived from target — never primary |

**Absolute vs percentage:** percentage-type error (via log transform) wins — with a 5000× price range, absolute-AED metrics are dominated by the luxury tail and would rank models by how well they predict villas while ignoring studios.

## Outlier Impact

- Raw-price RMSE/MAE would be dictated by the extreme tail (max 3.8B AED ≈ 2800× median) → rejected as primary.
- Log transform tames but doesn't remove tails → additionally track **share of predictions with >50% relative error** ("catastrophic-miss rate"); a model must not win on average while failing catastrophically often.

## Initial Success Criteria (provisional until first baseline)

1. Validation log-MAE ≤ 0.20 (≈ ±20% typical relative error)
2. Beat naive baseline (area-median price/m² × area) by ≥ 25% on log-MAE
3. Median AE ≤ 0.15 (typical case better than the mean case)
4. No price-quintile segment with log-MAE > 0.35
5. Catastrophic-miss rate (>50% relative error) ≤ 5%
6. R² (log) ≥ 0.75 as sanity floor

## Segment-Level Reporting

Report log-MAE + MdAPE separately for:

- **Price quintiles** — guards against trading cheap-segment accuracy for luxury wins
- **Off-plan vs ready** — eligibility doc (§6) flags label staleness risk for off-plan
- **Property type** (unit/villa/land) and **top areas**

## Review Questions (brief)

- *Why primary over alternatives?* Percentage-like behaviour across a huge price range; RMSE overweights outliers, raw MAE overweights expensive homes, R² is diagnostic only.
- *Extreme prices?* Handled: log target for modeling, log-based metrics for scoring, plus explicit catastrophic-miss tracking.
- *Sensible penalty?* Yes — proportional-to-value penalties match buyer/seller reality; being wrong by 200k on a 2M flat matters like 20k on a 200k studio.
- *Could primary improve while business outcome worsens?* Yes — e.g., ignoring the cheapest segment; mitigated by criterion 4 and segment reporting.
- *Separate evaluation per range?* Yes — mandatory per above.
