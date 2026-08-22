
criterias to be linked to sales predictions.



| Column                 | Include in model? | Treatment          | Reason                                                                      |
| ---------------------- | ----------------- | ------------------ | --------------------------------------------------------------------------- |
| `actual_worth`         | ❌                 | Drop / investigate | Potentially derived from transaction/property value → **high leakage risk** |
| `area_id`              | ❌                 | Drop               | Identifier; use `area_name_en` instead                                      |
| `area_name_en`         | ✅                 | Feature            | **Very important location feature**                                         |
| `building_name_en`     | ✅                 | Feature            | Building-specific pricing information                                       |
| `has_parking`          | ✅                 | Feature            | Can influence property value                                                |
| `instance_date`        | ✅                 | Feature            | **Very important**; captures market/time effects                            |
| `master_project_en`    | ✅                 | Feature            | Project/community information                                               |
| `meter_rent_price`     | ❌                 | Drop initially     | Rental price may introduce leakage depending on timing/source               |
| `meter_sale_price`     | 🎯 **TARGET**     | Target             | This is what you're predicting                                              |
| `nearest_landmark_en`  | ✅                 | Feature            | Location/accessibility                                                      |
| `nearest_mall_en`      | ✅                 | Feature            | Accessibility/amenity proxy                                                 |
| `nearest_metro_en`     | ✅                 | Feature            | Accessibility/location proxy                                                |
| `no_of_parties_role_1` | ❌                 | Drop               | Administrative transaction information                                      |
| `no_of_parties_role_2` | ❌                 | Drop               | Administrative transaction information                                      |
| `no_of_parties_role_3` | ❌                 | Drop               | Administrative transaction information                                      |
| `procedure_id`         | ❌                 | Drop               | Identifier                                                                  |
| `procedure_name_en`    | ⚠️                | Transform          | Useful mainly for identifying sale/off-plan type                            |
| `project_name_en`      | ✅                 | Feature            | **Very important**                                                          |
| `project_number`       | ❌                 | Drop               | Identifier for project                                                      |
| `property_sub_type_en` | ✅                 | Feature            | Studio, 1 B/R, 2 B/R, etc.                                                  |
| `property_sub_type_id` | ❌                 | Drop               | Identifier                                                                  |
| `property_type_en`     | ✅                 | Feature            | Flat, Villa, etc.                                                           |
| `property_type_id`     | ❌                 | Drop               | Identifier                                                                  |
| `property_usage_en`    | ✅/⚠️              | Filter + Feature   | Residential/commercial etc.; important for defining population              |
| `reg_type_en`          | ⚠️                | Investigate        | May contain transaction/registration meaning                                |
| `reg_type_id`          | ❌                 | Drop               | Identifier                                                                  |
| `rent_value`           | ❌                 | Drop initially     | Potential leakage / different target domain                                 |
| `rooms_en`             | ✅                 | Feature            | Number/type of rooms                                                        |
| `transaction_id`       | ❌                 | Validation only    | Useful for duplicate detection, not prediction                              |
| `trans_group_en`       | ⚠️                | Filter/validation  | Useful for identifying `Sales`                                              |
| `trans_group_id`       | ❌                 | Drop               | Identifier                                                                  |
| `load_timestamp`       | ❌                 | Drop               | Data ingestion timestamp; not property information                          |


