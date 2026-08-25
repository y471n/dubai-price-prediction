# Feature Availability at Prediction Time (Just Before Registration)

This document defines which features from the DLD transactions dataset are known at the moment just before a property transaction is registered with the Dubai Land Department (DLD) (prediction time). At this moment, the buyer and seller have agreed on the price and all terms, but the registration has not yet occurred. Features marked **Yes** are usable for predicting the eventual sale price. Features marked **No** are not known at prediction time and must be excluded to avoid leakage or because they are the target. Features marked **⚠️ Identifier** are internal IDs where the descriptive name is known and should be used instead.

| Column | Available at prediction time? | Treatment | Reason |
|---|---|---|---|
| `actual_worth` | ❌ No | Drop / investigate | This is the target variable (total sale price). Known to parties but not available as a feature for prediction (would be direct leakage). |
| `area_id` | ⚠️ Identifier | Drop | Internal area code; the area name (`area_name_en`) is known. |
| `area_name_ar` | ✅ Yes | Feature | Arabic area name; known at prediction time. |
| `area_name_en` | ✅ Yes | Feature | English area name; known at prediction time. |
| `building_name_ar` | ✅ Yes | Feature | Arabic building name; known at prediction time. |
| `building_name_en` | ✅ Yes | Feature | English building name; known at prediction time. |
| `has_parking` | ✅ Yes | Feature | Parking availability; known at prediction time. |
| `instance_date` | ✅ Yes | Feature | Date of registration; known at prediction time (registration is scheduled in advance). Captures market/time effects. |
| `master_project_ar` | ✅ Yes | Feature | Arabic master project/community name; known at prediction time. |
| `master_project_en` | ✅ Yes | Feature | English master project/community name; known at prediction time. |
| `meter_rent_price` | ❌ No | Drop initially | Rental price per square meter; may not be known at prediction time for sale listings and could introduce leakage depending on timing/source. |
| `meter_sale_price` | ❌ No | Drop | Price per square meter at sale; derived from `actual_worth` / `procedure_area`. Since `actual_worth` is unknown, this is also unknown and cannot be used as a feature. It is an alternative target. |
| `nearest_landmark_ar` | ✅ Yes | Feature | Arabic nearest landmark name; known at prediction time. |
| `nearest_landmark_en` | ✅ Yes | Feature | English nearest landmark name; known at prediction time. |
| `nearest_mall_ar` | ✅ Yes | Feature | Arabic nearest mall name; known at prediction time. |
| `nearest_mall_en` | ✅ Yes | Feature | English nearest mall name; known at prediction time. |
| `nearest_metro_ar` | ✅ Yes | Feature | Arabic nearest metro station name; known at prediction time. |
| `nearest_metro_en` | ✅ Yes | Feature | English nearest metro station name; known at prediction time. |
| `no_of_parties_role_1` | ❌ No | Drop | Administrative transaction information; unknown at prediction time. |
| `no_of_parties_role_2` | ❌ No | Drop | Administrative transaction information; unknown at prediction time. |
| `no_of_parties_role_3` | ❌ No | Drop | Administrative transaction information; unknown at prediction time. |
| `procedure_id` | ⚠️ Identifier | Drop | Internal procedure identifier; the procedure name is known. |
| `procedure_name_ar` | ✅ Yes | Feature | Arabic procedure name (e.g., Sell - Pre registration); known at prediction time (reflects the agreed transaction type). |
| `procedure_name_en` | ✅ Yes | Feature | English procedure name (e.g., Sell - Pre registration); known at prediction time (reflects the agreed transaction type). |
| `project_name_ar` | ✅ Yes | Feature | Arabic project name; known at prediction time. |
| `project_name_en` | ✅ Yes | Feature | English project name; known at prediction time. |
| `project_number` | ⚠️ Identifier | Drop | Internal project identifier; the project name is known. |
| `property_sub_type_ar` | ✅ Yes | Feature | Arabic property subtype (e.g., Studio); known at prediction time. |
| `property_sub_type_en` | ✅ Yes | Feature | English property subtype (e.g., Studio); known at prediction time. |
| `property_sub_type_id` | ⚠️ Identifier | Drop | Internal property subtype identifier; the subtype name is known. |
| `property_type_ar` | ✅ Yes | Feature | Arabic property type (e.g., شقه سكنيه); known at prediction time. |
| `property_type_en` | ✅ Yes | Feature | English property type (e.g., Flat); known at prediction time. |
| `property_type_id` | ⚠️ Identifier | Drop | Internal property type identifier; the type name is known. |
| `property_usage_ar` | ✅ Yes | Feature | Arabic property usage (e.g., سكني); known at prediction time. |
| `property_usage_en` | ✅ Yes | Feature | English property usage (e.g., Residential); known at prediction time. |
| `reg_type_ar` | ✅ Yes | Feature | Arabic registration type (e.g., على الخارطة); known at prediction time (off-plan vs existing). |
| `reg_type_en` | ✅ Yes | Feature | English registration type (e.g., Off-Plan Properties); known at prediction time (off-plan vs existing). |
| `reg_type_id` | ⚠️ Identifier | Drop | Internal registration type identifier; the type name is known. |
| `rent_value` | ❌ No | Drop initially | Rental value; not known at prediction time for sale listings and may introduce leakage. |
| `rooms_ar` | ✅ Yes | Feature | Arabic room count/type (e.g., استوديو); known at prediction time. |
| `rooms_en` | ✅ Yes | Feature | English room count/type (e.g., Studio); known at prediction time. |
| `transaction_id` | ⚠️ Identifier | Drop | Unique transaction identifier; assigned at registration, unknown at prediction time. |
| `trans_group_ar` | ✅ Yes | Feature | Arabic transaction group (e.g., مبايعات); known at prediction time (the intent is to sell, so `Sales` is expected for sale rows). |
| `trans_group_en` | ✅ Yes | Feature | English transaction group (e.g., Sales); known at prediction time (the intent is to sell). |
| `trans_group_id` | ⚠️ Identifier | Drop | Internal transaction group identifier; the group name is known. |
| `load_timestamp` | ❌ No | Drop | Data ingestion timestamp; not known at prediction time (occurs after data collection). |

## Notes on Ambiguous Columns
- None of the columns above are marked as purely ambiguous; however, the usability of `trans_group_*` and `procedure_name_*` relies on the assumption that the seller’s intent at the time of agreement matches the eventual transaction type. If a deal falls through or the transaction type changes (e.g., sale to gift), these features may become inaccurate. In practice, we treat them as known at prediction time because the dataset only includes completed sales, and we are modeling the subset of agreements that result in a sale.

## Derived Features & Leakage Risks
- `actual_worth` is the target; using it as a feature would be leakage.
- `meter_sale_price` is derived from `actual_worth` and `procedure_area`. Since `actual_worth` is unknown, `meter_sale_price` is also unknown and cannot be used as a feature.
- Any feature that combines known and unknown components (e.g., a price per square meter multiplied by an unknown area) must be avoided.
- Features like `meter_rent_price` and `rent_value` are excluded because their timing/source may not align with the prediction moment and could leak future rental market information.

## Recommendation
For modeling, use only the features marked **Yes** (✅) as input predictors. Exclude all **No** (❌) and **⚠️ Identifier** columns. The target is `actual_worth` (total sale price in AED). Alternatively, you may predict `meter_sale_price` (price per square meter) given that `procedure_area` is known; the two targets are equivalent. Ensure that any train/validation/test split is done before any feature engineering to prevent leakage from future sale information.
