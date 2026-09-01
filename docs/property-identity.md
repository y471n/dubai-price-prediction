# Property & Transaction Identity

## Objective

Determine whether multiple records can represent the same property, how to identify individual properties and transactions, and what this means for modelling and train/test leakage prevention.

---

## 1. Transaction Identity

| Field | Status |
|-------|--------|
| **`transaction_id`** | Unique per row — **Yes** |
| **`transaction_id` missing** | **No** (0/883,781) |
| **Format** | `{type_id}-{procedure_id}-{YYYY-MM}-{sequence}` (e.g. `1-102-2025-128277`) |
| **Total transactions** | **883,781** |

Every row is a distinct registered transaction at the Dubai Land Department. `transaction_id` is the authoritative unique identifier for each record.

---

## 2. Property Identity

### 2.1 No Explicit Property Identifier Exists

The dataset contains **no single column** that uniquely identifies a property (e.g. no unit number, no title deed reference). This is a fundamental limitation of the DLD API data.

### 2.2 Candidate Fields

| Field | Unique Values | Missing % | Suitable as sole identifier? |
|-------|---------------|-----------|------------------------------|
| `area_id` | 247 | 0.0% | **No** — too few unique values |
| `area_name_en` | 247 | 0.0% | **No** — same as `area_id` |
| `building_name_en` | 4,952 | 28.3% | **No** — missing for Land, Villa, Building types |
| `project_number` | 3,292 | 26.4% | **No** — missing for non-project properties |
| `project_name_en` | 3,287 | 26.4% | **No** — same coverage as `project_number` |
| `master_project_en` | 160 | 13.4% | **No** — too few unique values |
| `property_sub_type_id` | 19 | 19.6% | **No** — low cardinality |
| `property_type_id` | 4 | 0.0% | **No** — only 4 values |
| `rooms_en` | 17 | 21.1% | **No** — low cardinality |
| `procedure_area` | 77,028 | 0.0% | **No** — multiple units share same area |
| `has_parking` | 2 | 0.0% | **No** — binary |
| `reg_type_en` | 2 | 0.0% | **No** — only Off-Plan/Existing |
| `meter_sale_price` | 583,136 | 0.0% | **No** — target/feature value, not an identifier |
| `meter_rent_price` | 16,048 | 97.9% | **No** — only populated for rentals |

### 2.3 Composite Key (Recommended)

No single field suffices. A **composite key** is required:

```
property_key = area_id + building_name_en + procedure_area + rooms_en
```

> **Note:** `meter_sale_price` and `meter_rent_price` are **not** identity fields. They are price-per-sqm **values** (features/target), not identifiers. They are not unique — the same `meter_sale_price` is shared across many distinct properties (e.g. 1,133 rows share 358.8 AED/sqm), and `meter_rent_price` is 97.9% missing (only present for rental transactions). Across multi-transaction properties, only 4.4% have a constant `meter_sale_price` and 6.2% a constant `meter_rent_price`, confirming these vary per transaction and cannot group properties.

| Metric | Value |
|--------|-------|
| Unique property groups | **261,859** |
| Full key (building + rooms present) | 162,760 properties (620,856 transactions) |
| Partial key (one missing) | 32,908 properties (89,575 transactions) |
| Degraded key (both missing) | 66,191 properties (173,350 transactions) |

---

## 3. Repeated Property Records

### 3.1 Transactions per Property

| Statistic | Value |
|-----------|-------|
| Mean | 3.38 |
| Median | 1 |
| P25 | 1 |
| P75 | 3 |
| P90 | 6 |
| P95 | 10 |
| P99 | 30 |
| Max | **2,767** |

### 3.2 Distribution

| Category | Properties | % of Total |
|----------|------------|------------|
| Exactly 1 transaction | 136,348 | 52.1% |
| >1 transaction | 125,511 | **47.9%** |
| >5 transactions | 30,804 | 11.8% |
| >10 transactions | 13,026 | 5.0% |
| >50 transactions | 1,066 | 0.4% |
| >100 transactions | 280 | 0.1% |

**84.6% of all rows** belong to properties with multiple transactions.

### 3.3 Properties with Unusually High Transaction Counts

When `building_name_en` is **missing**, the composite key degrades and many different units are incorrectly grouped together. The top groups (>500 txns) all have missing building names:

| Txns | Area ID | Building | SqM | Rooms |
|------|---------|----------|-----|-------|
| 2,767 | 451 | *(missing)* | 144.0 | *(missing)* |
| 1,457 | 505 | *(missing)* | 112.2 | *(missing)* |
| 1,029 | 469 | *(missing)* | 174.0 | 3 B/R |
| 1,003 | 445 | *(missing)* | 600.0 | *(missing)* |
| 976 | 506 | *(missing)* | 144.0 | *(missing)* |

When `building_name_en` **is** present, the max drops to **449** (Torch Tower, Marsa Dubai). Even these high counts likely represent distinct units in the same building that happen to share the same area and room configuration.

**Conclusion:** High transaction counts are a **composite key collision artefact**, not evidence of a single property being transacted thousands of times.

---

## 4. Multiple Transactions per Property

### 4.1 Transaction Types

| Group | Count | % of Multi-Txn Rows |
|-------|-------|---------------------|
| Sales | 569,583 | 76.2% |
| Mortgages | 154,411 | 20.7% |
| Gifts | 23,439 | 3.1% |

### 4.2 Top Procedure Types

| Procedure | Count | % |
|-----------|-------|---|
| Sell - Pre registration | 255,617 | 34.2% |
| Sell | 224,398 | 30.0% |
| Mortgage Registration | 105,522 | 14.1% |
| Delayed Sell | 58,190 | 7.8% |
| Lease to Own Registration | 28,383 | 3.8% |
| Grant | 20,738 | 2.8% |

### 4.3 Time Between Consecutive Transactions

| Metric | Value |
|--------|-------|
| Median gap | **34 days** |
| Mean gap | 328 days |
| P25 | 2 days |
| P75 | 246 days |
| P90 | 968 days |
| <30 days between txns | **48.5%** of consecutive pairs |
| <7 days between txns | **32.5%** of consecutive pairs |

The high frequency of very short gaps (< 30 days) is explained by **pre-registration + registration pairs**: a "Sell - Pre registration" followed by a "Sell" for the same property within days.

---

## 5. Identifier Stability Over Time

| Metric | Value |
|--------|-------|
| Properties with >5 txns | 30,804 |
| Properties where key components vary across transactions | **0** |
| Properties with >10 txns spanning >10 years | 5,824 |
| Properties with >10 txns spanning >20 years | 201 |

The composite key is **stable within the dataset** — no property has its key components change across transactions. However, the key is an **approximation** (see Section 3.3).

---

## 6. Missing / Ambiguous Identifiers

### 6.0 Price Columns (`meter_sale_price`, `meter_rent_price`) — Not Identifiers

These are **derived price values**, excluded as identity fields:

| Field | Unique | Missing % | Why not an identifier |
|-------|--------|-----------|----------------------|
| `meter_sale_price` | 583,136 | 0.0% | Not unique (883,781 rows); same value shared across many properties (e.g. 358.8 AED/sqm × 1,133 rows). It is a **target/feature**, not an ID. |
| `meter_rent_price` | 16,048 | 97.9% | Only present for rental transactions; not usable for grouping. |

Across multi-transaction properties, only **4.4%** have a constant `meter_sale_price` and **6.2%** a constant `meter_rent_price` — both vary per transaction and therefore cannot group properties.


### 6.1 Missing `building_name_en` by Property Type

| Property Type | Total | Missing | % |
|---------------|-------|---------|---|
| Land | 78,256 | 78,256 | **100.0%** |
| Building | 18,158 | 18,158 | **100.0%** |
| Villa | 153,701 | 153,701 | **100.0%** |
| Unit | 633,666 | 0 | 0.0% |

`building_name_en` is only populated for **Unit** property types.

### 6.2 Missing `rooms_en` by Property Type

| Property Type | Total | Missing | % |
|---------------|-------|---------|---|
| Land | 78,256 | 78,256 | **100.0%** |
| Building | 18,158 | 18,158 | **100.0%** |
| Villa | 153,701 | 76,936 | **50.1%** |
| Unit | 633,666 | 12,810 | 2.0% |

### 6.3 Missing `building_name_en` by Transaction Group

| Group | Total | Missing | % |
|-------|-------|---------|---|
| Mortgages | 173,760 | 83,448 | **48.0%** |
| Gifts | 33,006 | 10,865 | 32.9% |
| Sales | 677,015 | 155,802 | 23.0% |

### 6.4 Missing `building_name_en` by Registration Type

| Reg Type | Total | Missing | % |
|----------|-------|---------|---|
| Existing Properties | 562,776 | 216,031 | 38.4% |
| Off-Plan Properties | 321,005 | 34,084 | 10.6% |

**Key insight:** Building names are systematically missing for Land, Villa, Building property types and for mortgage/gift transactions. This means **~28% of rows cannot be precisely identified** at the building level.

---

## 7. Train/Test Leakage Risk

Using a temporal split at 2024-01-01:

| Metric | Value |
|--------|-------|
| Train transactions (before 2024) | 569,557 |
| Test transactions (2024+) | 314,223 |
| Train unique properties | 174,324 |
| Test unique properties | 128,681 |
| **Overlapping properties** | **41,146 (32.0% of test properties)** |
| Train rows from overlapping properties | 277,623 |

**Yes — the same property can (and does) appear in both training and test data.** A previous transaction for a property can indirectly reveal its future price trajectory.

---

## 8. Summary Statistics

| Metric | Value |
|--------|-------|
| Total transactions | 883,781 |
| Unique properties (composite key) | 261,859 |
| Transactions per property (mean) | 3.38 |
| Transactions per property (median) | 1 |
| Properties with multiple transactions | 125,511 (47.9%) |
| Rows in multi-transaction properties | 747,433 (84.6%) |
| Max transactions for a single property | 2,767 (key collision artefact) |
| Max transactions (building known) | 449 |
| Missing building_name_en | 250,115 (28.3%) |
| Missing rooms_en | 186,160 (21.1%) |
| Both missing | 173,350 (19.6%) |

---

## 9. Recommended Grouping Strategy

### Property Key Construction

```python
def build_property_key(df):
    """Build approximate property identity key."""
    return (
        df['area_id'].astype(str) + '|' +
        df['building_name_en'].fillna('UNKNOWN') + '|' +
        df['procedure_area'].astype(str) + '|' +
        df['rooms_en'].fillna('UNKNOWN')
    )
```

### Key Degradation Handling

| Scenario | Key Components | Coverage |
|----------|---------------|----------|
| Full key | `area_id + building_name_en + procedure_area + rooms_en` | 70.3% |
| No building name | `area_id + procedure_area + rooms_en` | 10.1% |
| No rooms | `area_id + building_name_en + procedure_area` | 0.0% (all Units have building name) |
| Both missing | `area_id + area_name_en + procedure_area + property_type_en` | 19.6% |

### Downstream Recommendations

1. **Use composite key for grouping** — group transactions by `property_key` for any analysis that requires property-level aggregation.
2. **Temporal train/test split must exclude overlapping properties** — if a property appears in test, remove all its training transactions, or vice versa.
3. **Flag high-frequency properties** — properties with >10 transactions should be reviewed; those with >50 are almost certainly key collisions.
4. **Separate analysis by key quality** — results from full-key properties are more reliable than degraded-key properties.
5. **Do not treat the composite key as a true property identifier** — it is an approximation. Two different units in the same building with identical area and room count will be incorrectly merged.

---

## 10. Review Questions

| Question | Answer |
|----------|--------|
| Can the same property appear in both training and test data? | **Yes.** 32% of test properties also appear in training. |
| Could a previous transaction for a property indirectly reveal its future price? | **Yes.** Past transactions provide price history that correlates with future values. |
| What happens when the property identifier is missing? | ~28% of rows lack `building_name_en`, ~21% lack `rooms_en`. The key degrades to fewer components, increasing collision risk. |
| Is a property identifier truly stable over time? | **Yes within the dataset** — no key components change across transactions. But the key is an approximation, not a true ID. |
| Should repeated transactions be grouped during evaluation? | **Yes for property-level metrics.** Grouping prevents a single property with many transactions from dominating evaluation scores. |
