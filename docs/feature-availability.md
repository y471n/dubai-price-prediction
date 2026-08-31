# Feature Availability at Prediction Time (Just Before Registration)

Defines which features are known when buyer/seller agree on price but before DLD registration.
Use **Yes** features as predictors; exclude **No** and **⚠️** columns to avoid leakage.

| Column | Available? | Treatment | Reason |
|---|---|---|---|
| `actual_worth` | ❌ No | Drop / investigate | Target (total sale price). |
| `area_id` | ⚠️ Identifier | Drop | Use `area_name_en` instead. |
| `area_name_ar` | ⚠️ Redundant | Drop | Redundant with `area_name_en`. |
| `area_name_en` | ✅ Yes | Feature | Known at agreement time. |
| `building_name_ar` | ⚠️ Redundant | Drop | Redundant with `building_name_en`. |
| `building_name_en` | ✅ Yes | Feature | Known at agreement time. |
| `has_parking` | ✅ Yes | Feature | Known at agreement time. |
| `instance_date` | ✅ Yes | Feature | Registration date (known in advance). |
| `master_project_ar` | ⚠️ Redundant | Drop | Redundant with `master_project_en`. |
| `master_project_en` | ✅ Yes | Feature | Known at agreement time. |
| `meter_rent_price` | ❌ No | Drop initially | Rental price; may not be known/leaky. |
| `meter_sale_price` | ❌ No | Drop | Derived from target (`actual_worth`/`procedure_area`). |
| `nearest_landmark_ar` | ⚠️ Redundant | Drop | Redundant with `nearest_landmark_en`. |
| `nearest_landmark_en` | ✅ Yes | Feature | Known at agreement time. |
| `nearest_mall_ar` | ⚠️ Redundant | Drop | Redundant with `nearest_mall_en`. |
| `nearest_mall_en` | ✅ Yes | Feature | Known at agreement time. |
| `nearest_metro_ar` | ⚠️ Redundant | Drop | Redundant with `nearest_metro_en`. |
| `nearest_metro_en` | ✅ Yes | Feature | Known at agreement time. |
| `no_of_parties_role_1` | ❌ No | Drop | Admin info; unknown pre-agreement. |
| `no_of_parties_role_2` | ❌ No | Drop | Admin info; unknown pre-agreement. |
| `no_of_parties_role_3` | ❌ No | Drop | Admin info; unknown pre-agreement. |
| `procedure_id` | ⚠️ Identifier | Drop | Use `procedure_name_en` instead. |
| `procedure_name_ar` | ⚠️ Redundant | Drop | Redundant with `procedure_name_en`. |
| `procedure_name_en` | ✅ Yes | Feature | Agreed transaction type (e.g., Sell - Pre registration). |
| `project_name_ar` | ⚠️ Redundant | Drop | Redundant with `project_name_en`. |
| `project_name_en` | ✅ Yes | Feature | Known at agreement time. |
| `project_number` | ⚠️ Identifier | Drop | Use `project_name_en` instead. |
| `property_sub_type_ar` | ⚠️ Redundant | Drop | Redundant with `property_sub_type_en`. |
| `property_sub_type_en` | ✅ Yes | Feature | Known at agreement time. |
| `property_sub_type_id` | ⚠️ Identifier | Drop | Use `property_sub_type_en` instead. |
| `property_type_ar` | ⚠️ Redundant | Drop | Redundant with `property_type_en`. |
| `property_type_en` | ✅ Yes | Feature | Known at agreement time. |
| `property_type_id` | ⚠️ Identifier | Drop | Use `property_type_en` instead. |
| `property_usage_ar` | ⚠️ Redundant | Drop | Redundant with `property_usage_en`. |
| `property_usage_en` | ✅ Yes | Feature | Known at agreement time. |
| `reg_type_ar` | ⚠️ Redundant | Drop | Redundant with `reg_type_en`. |
| `reg_type_en` | ✅ Yes | Feature | Known at agreement time (Off-Plan/Existing). |
| `reg_type_id` | ⚠️ Identifier | Drop | Use `reg_type_en` instead. |
| `rent_value` | ❌ No | Drop initially | Rental value; may not be known/leaky. |
| `rooms_ar` | ⚠️ Redundant | Drop | Redundant with `rooms_en`. |
| `rooms_en` | ✅ Yes | Feature | Known at agreement time. |
| `transaction_id` | ⚠️ Identifier | Drop | Assigned at registration. |
| `trans_group_ar` | ⚠️ Redundant | Drop | Redundant with `trans_group_en`. |
| `trans_group_en` | ✅ Yes | Feature | Intent to sell (`Sales`). |
| `trans_group_id` | ⚠️ Identifier | Drop | Use `trans_group_en` instead. |
| `load_timestamp` | ❌ No | Drop | Ingestion timestamp (post-collection). |

## Guidance
- **Predictors**: Use all **Yes** columns (✅).
- **Exclude**: All **No** (❌), **⚠️ Identifier**, and **⚠️ Redundant** columns.
- **Target**: `actual_worth` (or `meter_sale_price` given known `procedure_area`).
- **Critical**: Split train/validation/test before any feature engineering to prevent leakage.
