# Raw Dataset Audit: data.csv

## 1. Dataset Source & Provenance

| Field | Value |
|-------|-------|
| **File** | `data.csv` |
| **Source** | Dubai Land Department (DLD) — official government real estate transaction records |
| **Accessed via** | DLD REST API (https://dubailand.gov.ae) |
| **Load timestamp** | `2026-08-18T17:31:53.000Z` (embedded in `load_timestamp` column) |
| **Format** | CSV, UTF-8 encoded |
| **One row represents** | A single registered real estate transaction (sale, mortgage, or gift) in Dubai |

**Provenance notes:**

- The dataset contains official Dubai Land Department transaction records.
- Each transaction is uniquely identified by `transaction_id`.
- The `load_timestamp` column indicates when the data was fetched from the DLD API (same timestamp for all rows: `2026-08-18T17:31:53.000Z`), suggesting a single bulk download.
- No explicit dataset version or snapshot identifier beyond the load timestamp.

---

## 2. Dataset Size

| Metric | Value |
|--------|-------|
| **Total rows** | 883,781 |
| **Total columns** | 47 |
| **File size** | ~500 MB (approximate) |

---

## 3. Schema & Data Types

### 3.1 Column Reference

| # | Column Name | Type | Description | Empty % |
|---|-------------|------|-------------|---------|
| 0 | `actual_worth` | float | Transaction value in AED | 0.0% |
| 1 | `area_id` | int | Numeric area identifier | 0.0% |
| 2 | `area_name_ar` | str | Area name (Arabic) | 0.0% |
| 3 | `area_name_en` | str | Area name (English) | 0.0% |
| 4 | `building_name_ar` | str | Building name (Arabic) | 28.3% |
| 5 | `building_name_en` | str | Building name (English) | 28.3% |
| 6 | `has_parking` | bool/int | Parking availability flag | 0.0% |
| 7 | `instance_date` | str (YYYY-MM-DD) | Transaction registration date | 0.0% |
| 8 | `master_project_ar` | str | Master project/compound name (Arabic) | 13.4% |
| 9 | `master_project_en` | str | Master project/compound name (English) | 13.4% |
| 10 | `meter_rent_price` | float | Rental price per sqm | 97.9% |
| 11 | `meter_sale_price` | float | Sale price per sqm | 0.0% |
| 12 | `nearest_landmark_ar` | str | Nearest landmark (Arabic) | 20.5% |
| 13 | `nearest_landmark_en` | str | Nearest landmark (English) | 20.5% |
| 14 | `nearest_mall_ar` | str | Nearest mall (Arabic) | 32.1% |
| 15 | `nearest_mall_en` | str | Nearest mall (English) | 32.1% |
| 16 | `nearest_metro_ar` | str | Nearest metro station (Arabic) | 31.5% |
| 17 | `nearest_metro_en` | str | Nearest metro station (English) | 31.5% |
| 18 | `no_of_parties_role_1` | int | Number of parties (role 1) | 0.1% |
| 19 | `no_of_parties_role_2` | int | Number of parties (role 2) | 0.1% |
| 20 | `no_of_parties_role_3` | int | Number of parties (role 3) | 0.1% |
| 21 | `procedure_area` | float | Area in square meters | 0.0% |
| 22 | `procedure_id` | int | Transaction procedure code | 0.0% |
| 23 | `procedure_name_ar` | str | Transaction type (Arabic) | 0.0% |
| 24 | `procedure_name_en` | str | Transaction type (English) | 0.0% |
| 25 | `project_name_ar` | str | Project name (Arabic) | 26.4% |
| 26 | `project_name_en` | str | Project name (English) | 26.4% |
| 27 | `project_number` | float | Project registration number | 26.4% |
| 28 | `property_sub_type_ar` | str | Property sub-type (Arabic) | 19.6% |
| 29 | `property_sub_type_en` | str | Property sub-type (English) | 19.6% |
| 30 | `property_sub_type_id` | int | Property sub-type code | 19.6% |
| 31 | `property_type_ar` | str | Property type (Arabic) | 0.0% |
| 32 | `property_type_en` | str | Property type (English) | 0.0% |
| 33 | `property_type_id` | int | Property type code | 0.0% |
| 34 | `property_usage_ar` | str | Property usage (Arabic) | 0.0% |
| 35 | `property_usage_en` | str | Property usage (English) | 0.0% |
| 36 | `reg_type_ar` | str | Registration type (Arabic) | 0.0% |
| 37 | `reg_type_en` | str | Registration type (English) | 0.0% |
| 38 | `reg_type_id` | int | Registration type code | 0.0% |
| 39 | `rent_value` | float | Rental value (if applicable) | 97.9% |
| 40 | `rooms_ar` | str | Room configuration (Arabic) | 21.1% |
| 41 | `rooms_en` | str | Room configuration (English) | 21.1% |
| 42 | `transaction_id` | str | Unique transaction identifier | 0.0% |
| 43 | `trans_group_ar` | str | Transaction group (Arabic) | 0.0% |
| 44 | `trans_group_en` | str | Transaction group (English) | 0.0% |
| 45 | `trans_group_id` | int | Transaction group code | 0.0% |
| 46 | `load_timestamp` | str (ISO 8601) | Data load timestamp | 0.0% |

### 3.2 Duplicate Columns

The dataset carries **dual-language columns** for most categorical fields (Arabic + English). For analysis purposes, the English columns are primary. The Arabic columns are redundant unless Arabic text processing is needed.

---

## 4. Date Range

| Metric | Value |
|--------|-------|
| **Earliest transaction date** | 1416-07-02 (likely erroneous — Hijri calendar not converted) |
| **Latest transaction date** | 2026-08-17 |
| **Unique dates** | 6,386 |

### 4.1 Year Distribution

| Year | Count | Notes |
|------|-------|-------|
| 1416 | 1 | Likely a Hijri date misclassified as Gregorian |
| 1966–1974 | 5 | Pre-modern Dubai; likely data entry errors or legacy records |
| 1975–1997 | ~450 | Early era; very sparse |
| 1998–2006 | ~15,000 | Pre-boom period |
| 2007 | 7,367 | Start of first major boom |
| 2008 | 15,925 | Financial crisis onset |
| 2009 | 38,624 | Post-crisis spike (distressed sales?) |
| 2010–2012 | ~65,600 | Recovery period |
| 2013–2014 | ~74,400 | Second boom |
| 2015–2020 | ~174,400 | Steady state (incl. COVID year 2020: 24,721) |
| 2021–2023 | ~184,000 | Post-COVID recovery and boom |
| 2024 | 112,133 | Record year (partial — data through Aug 2026) |
| 2025 | 133,431 | Full year + partial 2026 |
| 2026 | 68,659 | Partial year (through Aug 17) |

**Observation:** Data volume has grown dramatically in recent years. The 2009 spike may reflect distressed transactions during the global financial crisis. Pre-1998 data is extremely sparse and may represent legacy/imported records.

---

## 5. Geographic Coverage

### 5.1 Areas

| Metric | Value |
|--------|-------|
| **Unique area names (English)** | 247 |
| **Unique area IDs** | See `area_id` field |

**Top 10 areas by transaction count:**

| Area | Transactions |
|------|-------------|
| Marsa Dubai (Dubai Marina) | 69,510 |
| Business Bay | 58,470 |
| Al Barsha South Fourth | 56,463 |
| Al Thanyah Fifth | 49,783 |
| Burj Khalifa | 36,728 |
| Jabal Ali First | 32,952 |
| Wadi Al Safa 5 | 31,933 |
| Al Warsan First | 29,523 |
| Al Hebiah Fourth | 23,954 |
| Madinat Al Mataar | 23,236 |

**Observation:** The dataset covers Dubai's major freehold and leasehold zones. Concentration is heavily in high-density residential areas (Marina, Business Bay, Burj Khalifa area).

### 5.2 Master Projects (Communities)

| Metric | Value |
|--------|-------|
| **Unique master projects** | 160 |

**Top 10 master projects:**

| Master Project | Transactions |
|----------------|-------------|
| Jumeirah Village Circle | 56,458 |
| Business Bay | 52,442 |
| Dubai Marina | 49,182 |
| DMCC Master Community | 41,465 |
| DownTown Dubai | 36,295 |
| International City Phase 1 | 28,762 |
| Palm Jumeirah | 22,122 |
| Dubai Sports City | 20,522 |
| Silicon Oasis | 17,538 |
| Al Furjan | 17,475 |

### 5.3 Nearest Metro Stations

| Metric | Value |
|--------|-------|
| **Unique metro stations** | ~100+ |
| **Missing metro data** | 31.5% of rows |

**Top metro stations:**

| Station | Transactions |
|---------|-------------|
| Burj Khalifa Dubai Mall Metro Station | 64,976 |
| Dubai Internet City | 59,116 |
| Business Bay Metro Station | 57,515 |
| Nakheel Metro Station | 51,961 |
| Damac Properties | 44,011 |

### 5.4 Nearest Malls

| Metric | Value |
|--------|-------|
| **Unique malls** | ~100+ |
| **Missing mall data** | 32.1% of rows |

---

## 6. Major Categorical Fields

### 6.1 Transaction Groups (`trans_group_en`)

| Transaction Group | Count | % |
|-------------------|-------|---|
| Sales | 677,015 | 76.6% |
| Mortgages | 173,760 | 19.7% |
| Gifts | 33,006 | 3.7% |

**Note:** Arabic labels: مبايعات (Sales), رهون (Mortgages), هبات (Gifts).

### 6.2 Property Usage (`property_usage_en`)

| Usage | Count | % |
|-------|-------|---|
| Residential | 735,453 | 83.2% |
| Commercial | 93,756 | 10.6% |
| Other | 23,849 | 2.7% |
| Hospitality | 22,153 | 2.5% |
| أخرى (Other) | 3,096 | 0.4% |
| Industrial | 2,460 | 0.3% |
| Multi-Use | 2,081 | 0.2% |
| Agricultural | 558 | 0.1% |
| Storage | 349 | 0.0% |
| Residential / Commercial | 26 | 0.0% |

**Note:** There is a duplicate "Other" category — one in English (`Other`) and one in Arabic (`أخرى`). These should likely be consolidated.

### 6.3 Property Types (`property_type_en`)

| Type | Count | % |
|------|-------|---|
| Unit | 633,666 | 71.7% |
| Villa | 153,701 | 17.4% |
| Land | 78,256 | 8.9% |
| Building | 18,158 | 2.1% |

### 6.4 Property Sub-Types (`property_sub_type_en`)

| Sub-Type | Count | % |
|----------|-------|---|
| Flat | 565,124 | 63.9% |
| Villa | 76,842 | 8.7% |
| Office | 36,512 | 4.1% |
| Hotel Apartment | 14,720 | 1.7% |
| Shop | 9,006 | 1.0% |
| Hotel Rooms | 7,399 | 0.8% |
| Workshop | 276 | 0.0% |
| Stacked Townhouses | 263 | 0.0% |
| Store | 158 | 0.0% |
| Building | 144 | 0.0% |
| Warehouse | 83 | 0.0% |
| Show Rooms | 32 | 0.0% |
| Clinic | 29 | 0.0% |
| Hotel | 23 | 0.0% |
| Sized Partition | 21 | 0.0% |
| Gymnasium | 15 | 0.0% |
| Parking | 1 | 0.0% |
| Nursery | 1 | 0.0% |
| Unit | 1 | 0.0% |
| *(missing)* | 173,131 | 19.6% |

**Note:** 19.6% of rows have missing `property_sub_type`, which correlates with mortgage/gift transactions where sub-type is not recorded.

### 6.5 Room Configuration (`rooms_en`)

| Rooms | Count | % |
|-------|-------|---|
| 1 B/R | 242,164 | 27.4% |
| 2 B/R | 166,831 | 18.9% |
| Studio | 127,581 | 14.4% |
| 3 B/R | 91,825 | 10.4% |
| 4 B/R | 30,501 | 3.5% |
| Office | 29,914 | 3.4% |
| 5 B/R | 3,730 | 0.4% |
| Shop | 3,427 | 0.4% |
| PENTHOUSE | 813 | 0.1% |
| Single Room | 421 | 0.0% |
| 6 B/R | 200 | 0.0% |
| Store | 158 | 0.0% |
| 7 B/R | 36 | 0.0% |
| GYM | 11 | 0.0% |
| 8 B/R | 3 | 0.0% |
| 9 B/R | 5 | 0.0% |
| 10 B/R | 1 | 0.0% |

**Note:** 21.1% of rows have missing room data (typically mortgage and gift transactions).

### 6.6 Registration Types (`reg_type_en`)

| Registration Type | Count | % |
|-------------------|-------|---|
| Existing Properties | 562,776 | 63.7% |
| Off-Plan Properties | 321,005 | 36.3% |

Identical distribution to `reg_type_en` — maps to Existing vs Off-Plan classification.

### 6.7 Procedures (`procedure_name_en`)

| Procedure | Count | % |
|-----------|-------|---|
| Sell - Pre registration | 309,401 | 35.0% |
| Sell | 255,008 | 28.9% |
| Mortgage Registration | 120,111 | 13.6% |
| Delayed Sell | 76,993 | 8.7% |
| Lease to Own Registration | 29,768 | 3.4% |
| Grant | 29,255 | 3.3% |
| Modify Mortgage | 11,160 | 1.3% |
| Delayed Mortgage | 9,870 | 1.1% |
| Sell Development | 6,449 | 0.7% |
| Development Registration | 6,309 | 0.7% |
| Lease Finance Registration | 4,011 | 0.5% |
| Lease to Own Registration Pre-Registration | 3,608 | 0.4% |
| Development Mortgage | 3,326 | 0.4% |
| Mortgage Pre-Registration | 3,139 | 0.4% |
| Development Registration Pre-Registration | 2,727 | 0.3% |
| Grant Pre-Registration | 1,900 | 0.2% |
| Mortgage Transfer | 1,648 | 0.2% |
| Sale On Payment Plan | 1,169 | 0.1% |
| Grant on Delayed Sell | 1,155 | 0.1% |
| Delayed Lease to Own Registration | 1,081 | 0.1% |
| *(+ 31 additional rare procedures)* | <1,000 each | <0.1% |

**Note:** There are 51 distinct procedure types. The top 2 (Sell - Pre registration + Sell) account for 63.9% of all transactions.

---

## 7. Target-Related Fields

| Field | Description | Relevance |
|-------|-------------|-----------|
| `actual_worth` | Transaction value in AED | **Primary target** (sale price) |
| `meter_sale_price` | Sale price per sqm | **Derived target** (price normalization) |
| `meter_rent_price` | Rent per sqm | Only populated for rental transactions (97.9% empty) |
| `rent_value` | Rental transaction value | Only populated for rental transactions (97.9% empty) |
| `procedure_area` | Property area in sqm | Key feature for price normalization |

### 7.1 `actual_worth` (Transaction Value)

| Statistic | Value |
|-----------|-------|
| Non-null count | 883,781 |
| Observed range | Sample: 684,999 – 1,732,880 AED |

### 7.2 `meter_sale_price` (Price per sqm)

| Statistic | Value |
|-----------|-------|
| Count | 883,781 |
| Min | 0.0 |
| Max | 34,995,777.3 |
| Mean | 15,423.90 |

**Observation:** The maximum value (35M AED/sqm) is extreme and likely represents a data quality issue or an ultra-luxury outlier. The minimum of 0.0 suggests zero-value or gifted transactions.

### 7.3 `procedure_area` (Property Area)

| Statistic | Value |
|-----------|-------|
| Count | 883,781 |
| Min | 0.02 sqm |
| Max | 342,103,430.8 sqm (likely error — 342 sq km!) |
| Mean | 1,315.0 sqm |

**Observation:** The maximum `procedure_area` of 342M sqm is clearly an error (larger than Dubai itself). This needs to be flagged as an outlier.

### 7.4 `rent_value` (Rental Transaction Value)

| Statistic | Value |
|-----------|-------|
| Count | 18,472 (only rental transactions) |
| Min | 9,467 AED |
| Max | 262,080,000 AED |
| Mean | 1,480,030 AED |

**Note:** Only 2.1% of rows have a `rent_value`. The max of 262M AED may be a data error or represent a large commercial lease.

---

## 8. Structural Inconsistencies & Issues

### 8.1 Erroneous Dates

- **1 record** has date `1416-07-02` — this is a **Hijri calendar date** (not Gregorian). The DLD API returns dates in Gregorian format, so this is either a data entry error or a legacy record.
- **Sparse pre-1998 data** (~450 records) — may represent imported legacy data or errors.

### 8.2 High-Empty Columns

| Column | Empty % | Impact |
|--------|---------|--------|
| `meter_rent_price` | 97.9% | Only populated for rental transactions |
| `rent_value` | 97.9% | Only populated for rental transactions |
| `building_name_en` | 28.3% | Missing for land plots and some transactions |
| `master_project_en` | 13.4% | Missing for standalone buildings |
| `nearest_mall_en` | 32.1% | Missing for remote areas |
| `nearest_metro_en` | 31.5% | Missing for areas far from metro |
| `nearest_landmark_en` | 20.5% | Missing for some areas |
| `rooms_en` | 21.1% | Missing for non-residential and some transactions |
| `property_sub_type_en` | 19.6% | Missing for mortgage/gift transactions |
| `project_name_en` | 26.4% | Missing for non-project properties |

### 8.3 Duplicate Language Columns

Every categorical field has Arabic + English duplicates. Only English columns are needed for analysis unless Arabic NLP is required.

### 8.4 Zero-Value & Extreme Outliers

- `meter_sale_price` has minimum of 0.0 — gifted transactions and zero-value transfers.
- `meter_sale_price` maximum of 34,995,777 AED/sqm — likely data error or extreme outlier.
- `procedure_area` maximum of 342,103,430 sqm — clearly erroneous (larger than Dubai).
- `rent_value` maximum of 262,080,000 AED — may be data error or large commercial lease.

### 8.5 Building Name Inconsistencies

Building names show inconsistent naming conventions:
- Some use all caps: `PRINCESS TOWER`, `ELITE RESIDENCE`
- Some use mixed case: `Marina Pinnacle`, `Seven City JLT`
- Some use Arabic transliteration: `بن غاطي تيتانيا`

### 8.6 Transaction ID Format

Transaction IDs follow pattern `{type_id}-{procedure_id}-{YYYY-MM}-{sequence}`:
- Example: `1-102-2025-128277`
- This is not a simple sequential ID and encodes transaction metadata.

---

## 9. Reproducible Dataset Summary

To regenerate this audit, run:

```bash
python scripts/audit_data.py
```

The script:
1. Reads `data.csv` using the `csv` module (no external dependencies)
2. Computes row/column counts, date range, empty value counts
3. Aggregates categorical distributions
4. Computes numeric statistics
5. Prints a formatted report to stdout

**Raw dataset remains unchanged** — the script is read-only.

---

## 10. Open Questions for Further Investigation

1. **What does one row actually represent?**
   - One registered transaction at the Dubai Land Department. A single property can appear in multiple rows (sold multiple times).

2. **Is the date range sufficient for our prediction problem?**
   - The bulk of data is from 2007–2026. Pre-2007 data is sparse (~22,000 rows) and may not be representative.

3. **Are there geographic areas with very little data?**
   - The long tail of the area distribution has many areas with <100 transactions. These may be too sparse for reliable modeling.

4. **What about the `rent_value` and `meter_rent_price` columns?**
   - These are 97.9% empty and only populated for rental transactions. If the prediction target is sale price, these columns are not useful.

5. **Should gifted and mortgage transactions be included?**
   - Gifts (3.7%) and mortgages (19.7%) have different price dynamics than sales. They may need separate handling or exclusion.

6. **How should off-plan vs existing properties be treated?**
   - Off-plan (36.3%) and existing (63.7%) properties have fundamentally different pricing. Separate models may be needed.

7. **What is the `1416-07-02` date?**
   - Likely a Hijri date that was not converted. Needs investigation to determine if it should be excluded.

8. **Are the extreme `meter_sale_price` values (up to 35M AED/sqm) valid?**
   - Need to investigate whether these represent real transactions or data errors.

---

## Appendix: Column Index Reference

```
 0: actual_worth          1: area_id
 2: area_name_ar          3: area_name_en
 4: building_name_ar      5: building_name_en
 6: has_parking           7: instance_date
 8: master_project_ar     9: master_project_en
10: meter_rent_price     11: meter_sale_price
12: nearest_landmark_ar  13: nearest_landmark_en
14: nearest_mall_ar      15: nearest_mall_en
16: nearest_metro_ar     17: nearest_metro_en
18: no_of_parties_role_1 19: no_of_parties_role_2
20: no_of_parties_role_3 21: procedure_area
22: procedure_id         23: procedure_name_ar
24: procedure_name_en    25: project_name_ar
26: project_name_en      27: project_number
28: property_sub_type_ar 29: property_sub_type_en
30: property_sub_type_id 31: property_type_ar
32: property_type_en     33: property_type_id
34: property_usage_ar    35: property_usage_en
36: reg_type_ar          37: reg_type_en
38: reg_type_id          39: rent_value
40: rooms_ar             41: rooms_en
42: transaction_id       43: trans_group_ar
44: trans_group_en       45: trans_group_id
46: load_timestamp
```
