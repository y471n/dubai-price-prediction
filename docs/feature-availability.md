# Feature Availability at Prediction Time (Listing)

This document defines which features from the DLD transactions dataset are known at the moment a property is first listed for sale (prediction time). Features marked **Yes** are usable for predicting the eventual sale price. Features marked **No** are not known at listing and must be excluded to avoid leakage. Features marked **Ambiguous** may be partially known or require careful consideration.

| Column | Available at prediction time? | Treatment | Reason |
|---|---|---|---|
| `actual_worth` | ❌ No | Drop / investigate | Total sale price; unknown at listing and directly derived from the target (`meter_sale_price` × `procedure_area`). High leakage risk if used. |
| `area_id` | ⚠️ Identifier | Drop | Internal area code; the area name is known, but the ID adds no predictive value. |
| `area_name_ar` | ✅ Yes | Feature | Arabic area name; known at listing. |
| `area_name_en` | ✅ Yes | Feature | English area name; known at listing. |
| `building_name_ar` | ✅ Yes | Feature | Arabic building name; known at listing. |
| `building_name_en` | ✅ Yes | Feature | English building name; known at listing. |
| `has_parking` | ✅ Yes | Feature | Parking availability; known at listing. |
| `instance_date` | ❌ No | Drop | Date of transaction (sale); unknown at listing. Using it would leak the timing of the sale outcome. |
| `master_project_ar` | ✅ Yes | Feature | Arabic master project/community name; known at listing. |
| `master_project_en` | ✅ Yes | Feature | English master project/community name; known at listing. |
| `meter_rent_price` | ❌ No | Drop initially | Rental price per square meter; may not be known at listing for sale listings and could introduce leakage depending on timing/source. |
| `meter_sale_price` | 🎯 **TARGET** | Target | Price per square meter at sale; unknown at listing (this is what we are predicting). |
| `nearest_landmark_ar` | ✅ Yes | Feature | Arabic nearest landmark name; known at listing. |
| `nearest_landmark_en` | ✅ Yes | Feature | English nearest landmark name; known at listing. |
| `nearest_mall_ar` | ✅ Yes | Feature | Arabic nearest mall name; known at listing. |
| `nearest_mell_en` | ✅ Yes | Feature | English nearest mall name; known at listing. |
| `nearest_metro_ar` | ✅ Yes | Feature | Arabic nearest metro station name; known at listing. |
| `nearest_metro_en` | ✅ Yes | Feature | English nearest metro station name; known at listing. |
| `no_of_parties_role_1` | ❌ No | Drop | Administrative transaction information; unknown at listing. |
| `no_of_parties_role_2` | ❌ No | Drop | Administrative transaction information; unknown at listing. |
| `no_of_parties_role_3` | ❌ No | Drop | Administrative transaction information; unknown at listing. |
| `procedure_id` | ⚠️ Identifier | Drop | Internal procedure identifier; the procedure name is known. |
| `procedure_name_ar` | ✅ Yes | Feature | Arabic procedure name (e.g., Sell - Pre registration); known at listing (reflects the intended sale type). |
| `procedure_name_en` | ✅ Yes | Feature | English procedure name (e.g., Sell - Pre registration); known at listing (reflects the intended sale type). |
| `project_name_ar` | ✅ Yes | Feature | Arabic project name; known at listing. |
| `project_name_en` | ✅ Yes | Feature | English project name; known at listing. |
| `project_number` | ⚠️ Identifier | Drop | Internal project identifier; the project name is known. |
| `property_sub_type_ar` | ✅ Yes | Feature | Arabic property subtype (e.g., Studio); known at listing. |
| `property_sub_type_en` | ✅ Yes | Feature | English property subtype (e.g., Studio); known at listing. |
| `property_sub_type_id` | ⚠️ Identifier | Drop | Internal property subtype identifier; the subtype name is known. |
| `property_type_ar` | ✅ Yes | Feature | Arabic property type (e.g., شقه سكنيه); known at listing. |
| `property_type_en` | ✅ Yes | Feature | English property type (e.g., Flat); known at listing. |
| `property_type_id` | ⚠️ Identifier | Drop | Internal property type identifier; the type name is known. |
| `property_usage_ar` | ✅ Yes | Feature | Arabic property usage (e.g., سكني); known at listing. |
| `property_usage_en` | ✅ Yes | Feature | English property usage (e.g., Residential); known at listing. |
| `reg_type_ar` | ✅ Yes | Feature | Arabic registration type (e.g., على الخارطة); known at listing (off-plan vs existing). |
| `reg_type_en` | ✅ Yes | Feature | English registration type (e.g., Off-Plan Properties); known at listing (off-plan vs existing). |
| `reg_type_id` | ⚠️ Identifier | Drop | Internal registration type identifier; the type name is known. |
| `rent_value` | ❌ No | Drop initially | Rental value; not known at listing for sale listings and may introduce leakage. |
| `rooms_ar` | ✅ Yes | Feature | Arabic room count/type (e.g., استوديو); known at listing. |
| `rooms_en` | ✅ Yes | Feature | English room count/type (e.g., Studio); known at listing. |
| `transaction_id` | ⚠️ Identifier | Drop | Unique transaction identifier; unknown at listing (assigned after sale). |
| `trans_group_ar` | ✅ Yes | Feature | Arabic transaction group (e.g., مبايعات); known at listing (the intent is to sell, so `Sales` is expected). |
| `trans_group_en` | ✅ Yes | Feature | English transaction group (e.g., Sales); known at listing (the intent is to sell). |
| `trans_group_id` | ⚠️ Identifier | Drop | Internal transaction group identifier; the group name is known. |
| `load_timestamp` | ❌ No | Drop | Data ingestion timestamp; not known at listing (occurs after data collection). |

## Notes on Ambiguous Columns
- None of the columns above are marked as purely ambiguous; however, the usability of `trans_group_*` and `procedure_name_*` relies on the assumption that the seller’s intent at listing matches the eventual transaction type. If a listing is withdrawn or the transaction type changes (e.g., sale to gift), these features may become inaccurate. In practice, we treat them as known at listing because the dataset only includes completed sales, and we are modeling the subset of listings that result in a sale.

## Derived Features & Leakage Risks
- `actual_worth` is derived from `meter_sale_price` × `procedure_area`. Since `meter_sale_price` is the target, using `actual_worth` would leak the target.
- Any feature that combines known and unknown components (e.g., a price per square meter multiplied by an unknown area) must be avoided.
- Features like `meter_rent_price` and `rent_value` are excluded because their timing/source may not align with the prediction moment and could leak future rental market information.

## Recommendation
For modeling, use only the features marked **Yes** (✅) as input predictors. Exclude all **No** (❌) and **⚠️ Identifier** columns. The target is `meter_sale_price` (or equivalently `actual_worth` given known `procedure_area`). Ensure that any train/validation/test split is done before any feature engineering to prevent leakage from future sale information.
