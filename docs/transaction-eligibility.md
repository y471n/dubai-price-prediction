# Transaction Eligibility — Defining Valid Training Examples

> **Issue:** [#8](https://github.com/y471n/dubai-price-prediction/issues/8) · **Phase:** 1 · **Status:** Draft for review
> **Depends on:** [Problem Definition](problem-definition.md) (issue #7) — this document refines the population boundary that #7 left open.
> **Supersedes:** the scratch column-treatment draft previously kept at `phases/phase1/task7.md` (its feature-level decisions are now governed by `docs/problem-definition.md` and the upcoming data dictionary, issue #9).

## Evidence Provenance

This ticket requires rules "supported by analysis of the actual dataset". The pinned raw extract
(`data/transactions_2026-08-18_17-35-18_0001.csv`, 883,781 × 47) is no longer present in the working tree
(`data/` is gitignored), so quantification uses three evidence tiers, each labelled inline:

| Tag | Source | Dataset |
|---|---|---|
| **[V]** | Executed outputs of `notebooks/01-target-definition-recon.ipynb` | Pinned extract (883,781 rows) — authoritative |
| **[P]** | Figures already committed in `docs/problem-definition.md` (issue #7, reviewed) | Pinned extract |
| **[X]** | Fresh profiling of a newer official DLD export (`transactions-2026-08-19.csv`, 143,014 rows, Jan–Aug 2026, richer schema incl. `IS_OFFPLAN_EN`) | Same register, later window — cross-check & proportion estimates |
| **[A]** | Archived exploration notebooks (`archive/notebooks/exp4…`) run on an older 1.66M-row superset extract | Domain vocabulary only — counts NOT reused |

Rule-of-thumb: exact row counts for the pinned extract are given where **[V]/[P]** evidence exists;
where only **[X]** exists, we state the *proportion* observed on the newer window and mark the pinned-extract
count as *quantify-on-reload*. No raw data was modified at any point.

---

## 1. Recap: The Prediction Problem

From `docs/problem-definition.md`: we predict the **total registered consideration (AED) of an arm's-length
residential property sale in Dubai**, one prediction per DLD sale-transaction row. Issue #7 fixed the outer
boundary (`trans_group_en == "Sales"`); issue #8 must decide everything inside it — off-plan vs ready,
resales/transfers, lease-to-own lookalikes, zero-price rows, garbage dates, duplicates — and quantify each cut.

---

## 2. Transaction Types Present in the Dataset

### 2.1 Top level: `trans_group_en` [V]

| Group | Rows (pinned) | Share | Meaning |
|---|---:|---:|---|
| `Sales` | 677,015 | 76.6% | Sale/transfer of ownership against consideration ("مبايعات") |
| `Mortgages` | 173,760 | 19.7% | Loan registrations secured on property; value = debt, not price |
| `Gifts` | 33,006 | 3.7% | Grants/transfers without market consideration ("هبات", procedure `Grant`) |

Cross-check [X]: newer window shows Sales 75.6% / Mortgage 20.4% / Gifts 4.0% — proportions are stable over time,
so eligibility percentages derived from either tier generalise to future data.

### 2.2 Procedure vocabulary (`procedure_name_en`)

The full register uses 52 distinct procedures [A]. There is **no** `Cancel*`, `Reversal*` or similar value
anywhere in the vocabulary. Within the `Sales` group, the observed types and their meanings:

| Procedure (Sales group) | Share of sales [X] | Meaning |
|---|---:|---|
| `Sell - Pre registration` | 67.2% | Sale of an **off-plan** unit registered before completion (maps to `reg_type_en = Off-Plan Properties` [A]) |
| `Sale` / `Sell` | 23.1% | Sale of an **existing/ready** property (maps to `reg_type_en = Existing Properties` [A]) |
| `Delayed Sell` | 6.7% | Registration of a sale executed earlier but registered late; price is the agreed consideration, date is registration date |
| `Development Registration Pre-Registration` / `Development Registration` / `Sell Development` (+Delayed variants) | ~2.3% | Development-stage sales (land/building packages); same semantics as above within development context |
| `Lease to Own Registration` (+variants) | 0.40% | Rent-to-own finance arrangement — **not** a clean outright sale price |
| `Sale On Payment Plan` | 0.23% | Straight sale paid by instalments — genuine consideration |
| `Adding Land By Sell` | <0.01% | Aggregation sale adding land to a plot — genuine consideration |

### 2.3 Cancelled / invalid / suspicious transactions

- **Cancelled:** cannot exist in this extract by construction — the file is a register of *completed*
  registrations only, and the procedure vocabulary contains no cancellation type [A][X]. A cancelled deal simply
  never appears (or appears only via its eventual completion). This is a documented limitation, not a filter.
- **Invalid/incomplete:** no nulls exist in any of the three target-critical columns across all 883,781 rows [V].
  Incompleteness therefore lives in *feature* columns (e.g., `building_name_en` null for land parcels) — a Phase 2
  concern, not an eligibility one.
- **Suspicious:** handled explicitly by rules E2–E4 below (zero prices, impossible dates, lease-to-own pricing).

### 2.4 Registration type (`reg_type_en`)

Exactly two values matter for sales — `Off-Plan Properties` and `Existing Properties` [V sample, A] — and they
align 1:1 with pre-registration vs standard sell procedures [A]. This makes `reg_type_en` both a reliable
off-plan indicator and a candidate feature (see §5).

---

## 3. Valid Transaction Definition

> **A valid training example is a row that represents one arm's-length, completed sale of a residential property
> in Dubai, registered with the DLD, carrying a positive, internally consistent consideration (`actual_worth > 0`,
> consistent with `meter_sale_price × procedure_area`), dated within a plausible calendar window, identified by a
> unique `transaction_id`.**

Unpacking each clause:

1. **Arm's-length sale** — buyer and seller act independently; the recorded amount approximates market value.
   Excludes mortgages (debt amounts) and gifts/grants (nominal or family consideration).
2. **Completed registration** — the DLD register is our ground truth; pre-registration rows count because
   off-plan sale registration *is* the commercial event for ~two-thirds of Dubai transactions (§5).
3. **Residential property** — matches the population fixed in issue #7.
4. **Positive, consistent consideration** — required by the log-target formulation and by the identity
   `meter_sale_price ≈ actual_worth / procedure_area` verified on 100% of sales rows [V].
5. **Plausible date** — temporal features and time-based splits break if Hijri/garbage dates enter training.
6. **Unique transaction** — one physical transaction must not be double-counted; multi-unit portfolio rows are
   distinct examples (§6).

Everything else follows as an exclusion rule.

---

## 4. Exclusion Rules (with reasoning and impact)

Rules apply **in order**; impacts are not additive across overlapping rules. Percentages are relative to the
pinned extract's 883,781 rows unless stated.

### E1 — Keep only `trans_group_en == "Sales"`

- **Reasoning:** Mortgage rows record loan values (median-scale debt, not price); their inclusion would poison the
  target with a completely different generative process. Gift/grant rows are non-arm's-length by definition
  (inheritance, family transfers, developer incentives) — their recorded amounts, where present, do not answer
  "what will this property sell for?". Both groups also lack sale-consistent targets: the 100%-verified
  price/area identity was computed on Sales rows only [V].
- **Impact [V]:** excludes 206,766 rows (**23.39%**) → Mortgages 173,760 + Gifts 33,006. Keeps 677,015.
- **Leakage check:** none of the dropped groups carries information about future sale prices beyond what features
  already encode; dropping them removes noise rather than signal.

### E2 — Require a usable positive target: `actual_worth > 0` (and `procedure_area > 0`)

- **Reasoning:** a zero or non-positive price cannot be log-transformed and represents a data-entry artifact, not a
  market outcome. Verified facts: `actual_worth` has **zero nulls**, `meter_sale_price` has **exactly 3 zero
  values** dataset-wide [V]; the worth↔ppm↔area identity holds within 1% for **100%** of the 677,015 sales rows [V],
  so no partially-corrupted targets hide behind consistency failures.
- **Impact:** expected ≤3 sales rows (**≤0.0004%**). Whether all 3 zeros fall inside the Sales subset is unverified
  — flagged in §8. The `procedure_area > 0` clause currently excludes nothing (zero nulls/zeros area [V]) and is
  retained purely as a future-data guardrail.
- **Note:** extreme-but-positive prices (max 3.8B AED [V]) stay **in scope here**; outlier triage is issue #12's job.
  Eligibility ≠ outlier removal.

### E3 — Require a plausible `instance_date`

- **Reasoning:** `instance_date` drives temporal features, trend handling, and train/test splits. The extract
  contains ~2,924 rows (<0.4%) with implausible dates (earliest parsed year 1416 — Hijri-calendar or ingestion
  artifacts) [P]. Such rows cannot participate in any time-ordered validation without corrupting it.
- **Proposed operational rule:** parse strictly; drop rows whose parsed date falls outside `[2000-01-01, extract
  date]`. Dubai's modern freehold/registration regime makes pre-2000 sales negligible and methodologically
  incomparable (different market structure).
- **Impact:** ≤2,924 rows (**≤0.33%**) [P]; exact post-filter count to be confirmed on data reload.

### E4 — Exclude rent-to-own arrangements inside the Sales group

- **Reasoning:** `trans_group_en` alone does **not** guarantee an outright sale: procedures like
  `Lease to Own Registration` sit inside the Sales group [X] and record finance-arrangement values, not clean
  arm's-length considerations. Including them injects a small number of structurally different targets.
- **Operational rule:** exclude `procedure_name_en` starting with `Lease to Own`.
- **Impact [X]:** 0.40% of sales in the 2026 window (437/108,093); pinned-extract count *quantify-on-reload*
  (vocabulary confirmed present in older extracts [A]).

### E5 — Keep only `property_usage_en == "Residential"`

- **Reasoning:** issue #7 defined the target population as *residential* property. Commercial assets (offices,
  retail, warehouses) price on income multiples rather than the amenity/size dynamics residential models capture;
  mixing them degrades both segments. Usage is recorded on every row (no nulls [V]).
- **Impact [X]:** Commercial ≈ 3.2% of the register in the 2026 window; pinned-extract split *quantify-on-reload*.
- **Edge note:** `usage` values other than Residential/Commercial were not observed in either extract [V][X];
  any new value should be treated as *exclude-until-reviewed* under the data contract (issue #10).

### E6 — Drop exact duplicate `transaction_id` rows

- **Reasoning:** identity integrity — the valid-example definition says "one transaction". Exact ID collisions are
  ingestion artifacts. This must be sharply distinguished from legitimate multi-row transactions (§6).
- **Impact:** unknown on the pinned extract (uniqueness not yet asserted) — *quantify-on-reload*; the newer export
  showed 4,478 repeated `TRANSACTION_NUMBER`s, but inspection traced them to portfolio transactions with distinct
  units/prices per row [X], i.e., legitimate under §6, so the true duplicate rate is expected near zero.

---

## 5. Transfers, Resales, and Repeated Properties

**Decision: every qualifying sale row is its own example — resales are never deduplicated away.**

- A property selling in 2018 and again in 2024 contributes two *genuinely different* labels (market price at two
  moments). Removing repeats would discard exactly the temporal signal the model must learn, and repeat-sale pairs
  are valuable for later index/valuation work (tracked via issue #13).
- What looks like a "transfer" inside the Sales group is ordinary ownership transfer = the sale itself; there is no
  separate zero-priced transfer category once Gifts are excluded by E1.
- Portfolio/bulk transactions produce several rows sharing one transaction number (one row per unit, each with its
  own price and area) [X: 4,478 such rows ≈ 3.1% in the 2026 window]. Each row is a distinct property-level
  observation → keep all; collapsing them would fabricate aggregate prices. Only *exact* ID+content duplicates fall
  under E6.
- Repeat-sale leakage is a **split-strategy** problem (property grouping in train/test), deliberately deferred to
  issues #16–#18 — not solved here by deleting data.

## 6. Off-Plan Transactions

**Decision: include off-plan sales; carry `is_offplan` (from `reg_type_en`) as a feature.**

- **Scale:** off-plan pre-registrations are the majority of the market — 68.6% of 2026-window sales [X], and the
  archived exploration showed the same ordering [A]. Excluding them would discard roughly two-thirds of training
  data *and* most of the realistic production use case (buyers evaluate off-plan before completion).
- **Same prediction problem?** Yes with one caveat: an off-plan row records consideration at *registration*, which
  may precede completion by months-to-years, so its price embeds launch-era expectations while `instance_date`
  reflects registration time. That is precisely what we defined as predictable ("price at the point of
  registration", issue #7) — but the label can be *stale relative to the market* at `instance_date`. Ready sales
  don't have this gap. We mitigate by keeping the indicator feature so the model can learn segment-specific
  behaviour, and flag a possible future segmentation (separate models or interaction terms) if error analysis (post-
  baseline work) shows systematic off-plan bias.
- **Leakage assessment:** `reg_type_en`/procedure names describe the *nature of the transaction being predicted*,
  known at prediction time → safe as features. Nothing in the off-plan path exposes post-completion information.

---

## 7. Missing or Invalid Target Values

| Check | Result (pinned extract) | Action |
|---|---|---|
| `actual_worth` nulls | 0 / 883,781 [V] | Guardrail rule E2 anyway (future extracts may differ) |
| `actual_worth` ≤ 0 | ≤3 candidates via `meter_sale_price == 0` [V] | Exclude (E2) |
| Target consistency (ppm ↔ worth/area ±1%) | Holds for 100% of sales rows [V] | Add contract assertion (issue #10); violation → reject row |
| Extreme magnitudes | max 3.8B AED, max 14.45M AED/m² [V] | **Not an eligibility matter** → issue #12 outlier review |

Because the target is never missing and always self-consistent, E2 is nearly a no-op today — it exists to make the
contract explicit and future-proof, which is cheap insurance compared with silently training on corrupted labels
in a re-download.

---

## 8. Quantified Impact Summary

| Rule | Description | Affected rows (pinned) | % of raw | Evidence |
|---|---|---:|---:|---|
| E1 | Non-sale groups (Mortgages + Gifts) | 206,766 | 23.39% | [V] |
| E2 | Zero/non-positive target | ≤3 | ≤0.0004% | [V/P] |
| E3 | Implausible dates | ≤2,924 | ≤0.33% | [P] |
| E4 | Lease-to-own procedures | ~2,700 est. | ~0.40% of sales | [X] |
| E5 | Non-residential usage | ~21,700 est. | ~3.2% of register | [X] |
| E6 | Exact duplicate IDs | TBD | TBD | reload |

**Projected eligible pool:** ≈ 650k rows ≈ **96% of Sales**, ≈ **73–74% of the raw extract** (rough projection
combining [V] exclusions with [X] proportions; to be replaced by exact counts in the profiling pipeline).

The headline: eligibility filtering costs ~quarter of the raw data, almost entirely from E1, whose exclusion is
semantically mandatory. Every refinement *inside* Sales costs <4% combined — we are not throwing away useful
information to achieve a clean prediction problem.

---

## 9. Known Edge Cases & Unresolved Cases

| # | Case | Status / Handling |
|---|---|---|
| 1 | Are the 3 zero-price rows inside the Sales subset? | Unresolved [V gives dataset-wide count only]; E2 handles either way; confirm on reload |
| 2 | `Delayed Sell` price-date mismatch (contract earlier than registration) | Accepted: definition is "consideration at registration"; assumption documented; revisit if residual analysis flags it |
| 3 | `Sale On Payment Plan` | Included — genuine consideration; instalment structure invisible in data (acceptable) |
| 4 | Residential `Land` / `Building` parcels (~11.7%/8.6% of register overall [X]) | **Open question for reviewer:** they satisfy E1–E5 but have different feature availability (no building name/rooms). Default: include with `property_type_en` feature; revisit after baseline |
| 5 | Untranslated Arabic category leftovers (e.g., `أخرى`, n≈3,096 [P]) | Feature-hygiene issue (issues #12/#14), not eligibility — categories still describe real transactions |
| 6 | Cancellation visibility | Structurally absent from extract; if a future export adds cancel procedures, add E-rule then |
| 7 | Pinned CSV no longer on disk | All [X]-based numbers need re-confirmation when data is restored/re-downloaded; rules themselves are extract-independent |

## 10. Review Questions Answered

- **Does every included record represent the same prediction problem?** After E1–E5, yes: arm's-length, residential,
  registered consideration with a valid positive label and date. Residual heterogeneity (off-plan staleness, land
  parcels) is carried as features and flagged, not hidden.
- **Are we accidentally excluding useful information?** The only debatable cuts are Gifts (3.7%) and Lease-to-Own
  (0.4%) — both excluded for target-validity reasons, not convenience. Mortgages/Gifts could inform *features*
  someday (e.g., prior mortgage on unit) but never labels.
- **Could a transaction type introduce target leakage?** The dangerous direction is the reverse: including
  mortgage/gift amounts *as if* prices corrupts the target itself. Feature-side leakage from `trans_group`/
  `reg_type`/`procedure` fields is nil post-E1 since they're constant or prediction-time-known.
- **Assumptions about off-plan/resale?** (a) registered consideration ≈ market price even pre-completion; (b)
  `instance_date` is the label's market moment despite possible contract-date lag; (c) repeat sales are independent
  valid examples. All documented above with mitigation plans.
- **Would these rules hold for future data?** They are written as schema-level predicates (column-value tests),
  not row-specific patches; group/proportion stability between the 2016–26 and 2026 windows supports
  generalisation. Unknown future categories fail *closed* via E5's exclude-until-reviewed stance.

## 11. Acceptance Criteria Mapping

| Criterion | Where satisfied |
|---|---|
| Valid transaction definition is explicit | §3 |
| Inclusion/exclusion rules documented | §4 (E1–E6), §5, §6 |
| Rules supported by actual-data analysis | throughout, via provenance tags [V]/[P]/[X]/[A] |
| Impact of exclusions quantified | §8 |
| Ambiguous transaction types documented | §2.2, §9 |
| No data permanently modified | read-only analysis; raw `data/` untouched & gitignored |

## 12. Reproduction Notes

To re-confirm every number in this document when the raw extract is restored:
profile `trans_group_en`, `procedure_name_en` × `trans_group_en`, `reg_type_en`, `property_usage_en`,
null/zero counts for `actual_worth`/`meter_sale_price`/`procedure_area`, parsed `instance_date` range, and
`transaction_id` uniqueness — then replace every *est./TBD* cell in §8 with exact counts. Suggested home for that
script: the Phase 2 profiling pipeline (issues #12–#13), so eligibility metrics become monitored data-quality
tests rather than a one-off notebook.
