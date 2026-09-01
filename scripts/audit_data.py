#!/usr/bin/env python3
"""Reproducible dataset audit script for data.csv.

Run:
    python scripts/audit_data.py
"""

import csv
from collections import Counter
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data.csv"


def audit(path: Path = DATA_PATH) -> dict:
    """Profile data.csv and return a summary dict."""
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)

        rows = 0
        dates: list[str] = []
        empty_counts: dict[str, int] = {h: 0 for h in headers}
        areas_en: Counter = Counter()
        building_en: Counter = Counter()
        master_projects: Counter = Counter()
        nearest_metros: Counter = Counter()
        nearest_malls: Counter = Counter()
        nearest_landmarks: Counter = Counter()
        property_types: Counter = Counter()
        property_sub_types: Counter = Counter()
        property_usages: Counter = Counter()
        reg_types_en: Counter = Counter()
        rooms_en: Counter = Counter()
        trans_groups_en: Counter = Counter()
        procedures_en: Counter = Counter()
        rent_values: list[float] = []
        sale_prices: list[float] = []
        areas_list: list[str] = []
        procedure_areas: list[float] = []

        for row in reader:
            rows += 1

            # Column indices (0-based)
            # 0: actual_worth, 1: area_id, 2: area_name_ar, 3: area_name_en
            # 4: building_name_ar, 5: building_name_en, 6: has_parking
            # 7: instance_date, 8: master_project_ar, 9: master_project_en
            # 10: meter_rent_price, 11: meter_sale_price
            # 12: nearest_landmark_ar, 13: nearest_landmark_en
            # 14: nearest_mall_ar, 15: nearest_mall_en
            # 16: nearest_metro_ar, 17: nearest_metro_en
            # 18: no_of_parties_role_1, 19: no_of_parties_role_2, 20: no_of_parties_role_3
            # 21: procedure_area, 22: procedure_id, 23: procedure_name_ar, 24: procedure_name_en
            # 25: project_name_ar, 26: project_name_en, 27: project_number
            # 28: property_sub_type_ar, 29: property_sub_type_en, 30: property_sub_type_id
            # 31: property_type_ar, 32: property_type_en, 33: property_type_id
            # 34: property_usage_ar, 35: property_usage_en
            # 36: reg_type_ar, 37: reg_type_en, 38: reg_type_id
            # 39: rent_value, 40: rooms_ar, 41: rooms_en
            # 42: transaction_id, 43: trans_group_ar, 44: trans_group_en, 45: trans_group_id
            # 46: load_timestamp

            if row[7]:
                dates.append(row[7])
            if row[3]:
                areas_en[row[3]] += 1
                areas_list.append(row[3])
            if row[5]:
                building_en[row[5]] += 1
            if row[9]:
                master_projects[row[9]] += 1
            if row[17]:
                nearest_metros[row[17]] += 1
            if row[15]:
                nearest_malls[row[15]] += 1
            if row[13]:
                nearest_landmarks[row[13]] += 1
            if row[32]:
                property_types[row[32]] += 1
            if row[29]:
                property_sub_types[row[29]] += 1
            if row[35]:
                property_usages[row[35]] += 1
            if row[37]:
                reg_types_en[row[37]] += 1
            if row[41]:
                rooms_en[row[41]] += 1
            if row[44]:
                trans_groups_en[row[44]] += 1
            if row[24]:
                procedures_en[row[24]] += 1
            if row[39]:
                try:
                    rent_values.append(float(row[39]))
                except ValueError:
                    pass
            if row[11]:
                try:
                    sale_prices.append(float(row[11]))
                except ValueError:
                    pass
            if row[21]:
                try:
                    procedure_areas.append(float(row[21]))
                except ValueError:
                    pass

            for j, v in enumerate(row):
                if not v.strip():
                    empty_counts[headers[j]] += 1

    dates_sorted = sorted(dates)
    years = [d[:4] for d in dates if d]

    summary = {
        "file": str(path),
        "total_rows": rows,
        "total_columns": len(headers),
        "headers": headers,
        "date_range": {
            "earliest": dates_sorted[0] if dates_sorted else None,
            "latest": dates_sorted[-1] if dates_sorted else None,
            "unique_dates": len(set(dates)),
        },
        "year_distribution": dict(sorted(Counter(years).items())),
        "empty_counts": {h: c for h, c in empty_counts.items() if c > 0},
        "top_areas": areas_en.most_common(10),
        "unique_areas": len(areas_en),
        "top_buildings": building_en.most_common(10),
        "unique_buildings": len(building_en),
        "top_master_projects": master_projects.most_common(10),
        "unique_master_projects": len(master_projects),
        "nearest_metros": nearest_metros.most_common(10),
        "nearest_malls": nearest_malls.most_common(10),
        "property_types": property_types.most_common(),
        "property_sub_types": property_sub_types.most_common(),
        "property_usages": property_usages.most_common(),
        "reg_types_en": reg_types_en.most_common(),
        "rooms_en": rooms_en.most_common(),
        "trans_groups_en": trans_groups_en.most_common(),
        "procedures_en": procedures_en.most_common(),
        "rent_value_stats": {
            "count": len(rent_values),
            "min": min(rent_values) if rent_values else None,
            "max": max(rent_values) if rent_values else None,
            "mean": sum(rent_values) / len(rent_values) if rent_values else None,
        },
        "meter_sale_price_stats": {
            "count": len(sale_prices),
            "min": min(sale_prices) if sale_prices else None,
            "max": max(sale_prices) if sale_prices else None,
            "mean": sum(sale_prices) / len(sale_prices) if sale_prices else None,
        },
        "procedure_area_stats": {
            "count": len(procedure_areas),
            "min": min(procedure_areas) if procedure_areas else None,
            "max": max(procedure_areas) if procedure_areas else None,
            "mean": sum(procedure_areas) / len(procedure_areas) if procedure_areas else None,
        },
    }

    return summary


def print_summary(summary: dict) -> None:
    """Pretty-print the audit summary."""
    print("=" * 60)
    print("DATASET AUDIT REPORT")
    print("=" * 60)
    print(f"\nFile: {summary['file']}")
    print(f"Total rows: {summary['total_rows']:,}")
    print(f"Total columns: {summary['total_columns']}")

    print(f"\n--- DATE RANGE ---")
    dr = summary["date_range"]
    print(f"Earliest: {dr['earliest']}")
    print(f"Latest: {dr['latest']}")
    print(f"Unique dates: {dr['unique_dates']:,}")

    print(f"\n--- YEAR DISTRIBUTION ---")
    for y, c in summary["year_distribution"].items():
        print(f"  {y}: {c:,}")

    print(f"\n--- EMPTY VALUE COUNTS ---")
    for h, c in summary["empty_counts"].items():
        pct = c / summary["total_rows"] * 100
        print(f"  {h}: {c:,} ({pct:.1f}%)")

    print(f"\n--- TOP 10 AREAS ({summary['unique_areas']} unique) ---")
    for area, count in summary["top_areas"]:
        print(f"  {area}: {count:,}")

    print(f"\n--- TOP 10 BUILDINGS ({summary['unique_buildings']} unique) ---")
    for b, count in summary["top_buildings"]:
        print(f"  {b}: {count:,}")

    print(f"\n--- TOP 10 MASTER PROJECTS ({summary['unique_master_projects']} unique) ---")
    for p, count in summary["top_master_projects"]:
        print(f"  {p}: {count:,}")

    print(f"\n--- PROPERTY TYPES ---")
    for t, c in summary["property_types"]:
        print(f"  {t}: {c:,}")

    print(f"\n--- PROPERTY SUB TYPES ---")
    for st, c in summary["property_sub_types"]:
        print(f"  {st}: {c:,}")

    print(f"\n--- PROPERTY USAGES ---")
    for u, c in summary["property_usages"]:
        print(f"  {u}: {c:,}")

    print(f"\n--- REGISTRATION TYPES (EN) ---")
    for r, c in summary["reg_types_en"]:
        print(f"  {r}: {c:,}")

    print(f"\n--- ROOM TYPES ---")
    for r, c in summary["rooms_en"]:
        print(f"  {r}: {c:,}")

    print(f"\n--- TRANSACTION GROUPS ---")
    for tg, c in summary["trans_groups_en"]:
        print(f"  {tg}: {c:,}")

    print(f"\n--- PROCEDURE NAMES ---")
    for p, c in summary["procedures_en"]:
        print(f"  {p}: {c:,}")

    print(f"\n--- RENT VALUE ---")
    rv = summary["rent_value_stats"]
    print(f"  Count: {rv['count']:,}")
    print(f"  Min: {rv['min']}")
    print(f"  Max: {rv['max']}")
    print(f"  Mean: {rv['mean']:.2f}")

    print(f"\n--- METER SALE PRICE ---")
    sp = summary["meter_sale_price_stats"]
    print(f"  Count: {sp['count']:,}")
    print(f"  Min: {sp['min']}")
    print(f"  Max: {sp['max']}")
    print(f"  Mean: {sp['mean']:.2f}")

    print(f"\n--- PROCEDURE AREA ---")
    pa = summary["procedure_area_stats"]
    print(f"  Count: {pa['count']:,}")
    print(f"  Min: {pa['min']}")
    print(f"  Max: {pa['max']}")
    print(f"  Mean: {pa['mean']:.2f}")


if __name__ == "__main__":
    summary = audit()
    print_summary(summary)
