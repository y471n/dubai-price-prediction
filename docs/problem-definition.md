# Problem Definition — Prediction Target & Unit

> **Issue:** [#7](https://github.com/y471n/dubai-price-prediction/issues/7) · **Phase:** 1 · **Status:** Draft for review
> **Evidence:** `notebooks/01-target-definition-recon.ipynb`

## What Are We Predicting?

The **total transaction price, in AED, of a residential property sale in Dubai**, at the point of registration with the Dubai Land Department (DLD).

This is a regression problem grounded in a real use case: estimating what a property will sell for given its characteristics and market context.

## What Does One Prediction Represent?

**One prediction = one completed sale transaction** — a single row in the DLD transactions register where `trans_group_en == "Sales"`, identified by `transaction_id` and dated by `instance_date`.

| Dataset fact | Value | Source |
|---|---|---|
| Total records in raw extract | 883,781 | recon notebook |
| Sale transactions (**our population**) | 677,015 | `trans_group_en` counts |
| Mortgages (excluded) | 173,760 | same |
| Gifts/transfers (excluded) | 33,006 | same |

Mortgages and gifts are excluded because their recorded amounts are not arm's-length sale prices; including them would corrupt the target's meaning.

## Target Variable & Unit

| Role | Variable | Unit |
|---|---|---|
| **Primary target** | `actual_worth` | AED (log-transformed at modeling time due to heavy right skew) |
| Secondary evaluation lens | `meter_sale_price` | AED/m² |
| Denominator / cross-check | `procedure_area` | m² |

## Why This Formulation?

1. **It answers the business question.** Stakeholders ask "what will this property sell for?", not "what is its price per square meter?" Total price is the decision-relevant quantity.
2. **The alternative is informationally identical.** We verified that `meter_sale_price ≈ actual_worth / procedure_area` within 1% for **100%** of the 677,015 sales rows — the per-m² column is derived from the other two. Since area (`procedure_area`) is known at prediction time, predicting either formulation recovers the other exactly. The choice is therefore representational, not informational.
3. **Log transform is mandatory, not optional.** Sales prices span from small studios to entire buildings: median 1.36M AED vs max 3.8B AED. Modeling log-price stabilizes this spread; evaluation on the log scale also naturally weights relative errors, which suits price estimation across segments.

Could price vs price/m² lead to materially different modeling behavior? In principle yes — per-unit targets change how area variance and segment heterogeneity express themselves — but here the algebraic equivalence means both parameterizations encode the same fit; differences reduce to error-weighting choices, which we control via metrics rather than target choice.

## Alternatives Considered

| Alternative | Verdict | Reason |
|---|---|---|
| Predict `meter_sale_price` directly | Rejected as primary | Information-equivalent to total price (100% consistency check above); retained as secondary metric for cross-segment comparability |
| Include mortgages/gifts to enlarge training data | Rejected | Their amounts are not sale prices; would poison the target |
| Restrict further (e.g., existing flats only) | Deferred | Valid-transaction criteria are issue #8's scope; this doc defines the outer boundary only |

## Assumptions & Open Questions

**Assumptions**
- `actual_worth` reflects true consideration paid at registration.
- `instance_date` approximates the transaction's market moment.
- One row = one property-level transaction (identity/repeat-sale analysis pending, #13).

**Open questions (tracked in later issues)**
- Off-plan vs existing-property split: same model or separate treatment? (#8)
- Extreme outliers: max area 342M m², max ppm 14.4M AED/m², 3 zero-price rows → data-entry artifacts? (#12)
- Untranslated category values in English columns (e.g., `أخرى` alongside `Other`, n=3,096) (#12/#14)
- Temporal coverage: bulk of data is ~2016–2026, but 2,924 rows (<0.4%) carry implausible dates (earliest parsed: year 1416 — Hijri/garbage artifacts) (#12)
- Train/validation/test strategy over time (#16–#18)

## Review Questions

- **Useful real-world problem?** Yes — price estimation at registration is actionable for buyers, sellers, and lenders.
- **Would another ML engineer interpret it the same way?** Yes — population, unit, and units are stated explicitly with counts; the equivalence proof removes ambiguity between price formulations.
- **Hidden assumptions?** Registration date ≈ valuation moment, and single-row-per-transaction identity — both flagged above for verification.
