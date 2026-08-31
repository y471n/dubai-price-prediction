# Raw Data Quality Audit

**Dataset:** `data/transactions_2026-08-18_17-35-18_0001.csv`  
**Total rows:** 883,781  
**Total columns:** 47  
**File size:** 540.60 MB  
**Generated:** 2026-08-31

## Executive Summary

The dataset is largely usable, but several quality issues require attention before modeling. The most severe issues are extreme numerical outliers and suspicious duplicate-like records that share every field except `transaction_id`.

## 1. Missing Values

| Column                                         |     Missing Count | Missing % |
| ---------------------------------------------- | ----------------: | --------: |
| `meter_rent_price`                             |           865,309 |    97.91% |
| `rent_value`                                   |           865,309 |    97.91% |
| `nearest_mall_en` / `nearest_mall_ar`          |           283,995 |    32.13% |
| `nearest_metro_en` / `nearest_metro_ar`        |           278,521 |    31.51% |
| `building_name_en` / `building_name_ar`        | 250,115 – 250,366 |   ~28.33% |
| `project_name_*` / `project_number`            |           233,503 |    26.42% |
| `rooms_en` / `rooms_ar`                        |           186,160 |    21.06% |
| `nearest_landmark_*`                           |           181,243 |    20.51% |
| `property_sub_type_*` / `property_sub_type_id` |           173,131 |    19.59% |
| `master_project_*`                             | 118,387 – 118,405 |   ~13.40% |
| `no_of_parties_role_*`                         |               500 |     0.06% |

**Why it matters:**  
`meter_rent_price` and `rent_value` are almost entirely missing because the dataset is dominated by sales transactions; these fields are only relevant for rentals. High missingness in building/project/rooms/landmark columns will limit feature engineering unless imputed or encoded as "unknown."

**Recommended action:**

- Treat rent fields as rental-only features and exclude or conditionally impute for sales rows.
- Encode high-missingness categorical columns with an "Unknown" category rather than dropping rows.

## 2. Duplicate Analysis

- **Exact duplicate rows:** 0
- **Duplicate `transaction_id` values:** 0
- **Rows identical in all columns except `transaction_id`:** 25,794 (2.92%)

**Why it matters:**  
No row is an exact duplicate, but ~2.9% of records are identical across every descriptive field except the transaction identifier. One sampled group contained 65 such rows.

**Recommended action:**  
Investigate whether these represent legitimate bulk registrations or data-entry artifacts. If artifacts, deduplicate before splitting into train/validation/test.

## 3. Invalid or Impossible Values

| Issue                                      |         Count | % of Dataset |
| ------------------------------------------ | ------------: | -----------: |
| `meter_sale_price <= 0`                    |             3 |     ~0.0003% |
| `procedure_area` extremely large (outlier) | see Section 4 |            — |
| `instance_date` before 1970                |             3 |     ~0.0003% |
| Negative prices / negative party counts    |             0 |           0% |
| Invalid `has_parking` values               |             0 |           0% |
| Date parse failures                        |             0 |           0% |

**Why it matters:**  
Only a handful of rows contain impossible values, but they can break model training or skew evaluation.

**Recommended action:**  
Remove or flag the 3 rows with non-positive prices and pre-1970 dates.

## 4. Suspicious Distributions & Extreme Outliers

| Column             |             Max Value | IQR Outliers | Outlier % |
| ------------------ | --------------------: | -----------: | --------: |
| `actual_worth`     |    13,786,936,424 AED |       75,229 |     8.51% |
| `procedure_area`   |    342,103,430.80 sqm |      132,650 |    15.01% |
| `meter_sale_price` | 34,995,777.30 AED/sqm |       33,652 |     3.81% |

Notable observations:

- The top `actual_worth` value (13.79 billion AED) appears multiple times, suggesting a cap or placeholder.
- Several rows have `procedure_area` of ~0.09 sqm with extremely high `meter_sale_price`, which is physically impossible.
- Outliers in `procedure_area` are the most common issue.

**Recommended action:**

- Cap or Winsorize extreme `actual_worth` and `meter_sale_price` values.
- Remove rows with `procedure_area` below a realistic minimum (e.g., < 5 sqm) or above a realistic maximum.
- Investigate the repeated 13.79 billion AED value with the data source.

## 5. Suspicious Categorical Values

| Column                 | Key Findings                                                                                 |
| ---------------------- | -------------------------------------------------------------------------------------------- |
| `trans_group_en`       | Sales dominate (677,015 / 76.6%), followed by Mortgages (173,760) and Gifts (33,006).        |
| `procedure_name_en`    | Top procedures are sales-related (`Sell - Pre registration`, `Sell`, `Delayed Sell`).        |
| `reg_type_en`          | Existing Properties (562,776) vs Off-Plan Properties (321,005).                              |
| `property_type_en`     | Unit (633,666), Villa (153,701), Land (78,256), Building (18,158).                           |
| `property_sub_type_en` | `NaN` is the second-largest group (173,131 / 19.6%).                                         |
| `rooms_en`             | `NaN` is the second-largest group (186,160 / 21.1%).                                         |
| `property_usage_en`    | Contains both `"Other"` (23,849) and `"أخرى"` (3,096) — same meaning, inconsistent encoding. |
| `area_name_en`         | Top areas are Marsa Dubai, Business Bay, Al Barsha South Fourth.                             |

**Recommended action:**

- Map `"أخرى"` → `"Other"` in `property_usage_en`.
- Add explicit `"Unknown"` category for high-missingness columns instead of leaving `NaN`.

## 6. Consistency Between Related Fields

| Check                                                 | Result                                                |
| ----------------------------------------------------- | ----------------------------------------------------- |
| `area_id` → `area_name_en`                            | Perfectly consistent (0 conflicts)                    |
| `property_type_en` → `property_sub_type_en`           | Unit has 18 sub-types; Building and Villa have 1 each |
| `actual_worth` vs `meter_sale_price × procedure_area` | Match for                                             |
