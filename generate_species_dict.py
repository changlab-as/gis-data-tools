import argparse
import csv
from pathlib import Path
from pprint import pformat

CSV_FILE = Path("species0717.csv")


def make_parser():
    parser = argparse.ArgumentParser(
        description="""Convert plant_names CSV file into a species dictionary,
        species.py"""
    )

    parser.add_argument(
        "-c",
        "--csv",
        required=True,
        help="direct path the plant_names csv",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="species.py",
        help="Output species python file (default: combined.kml)",
    )

    return parser


def make_key(species_name):
    """Generate a dictionary key from species_name."""

    parts = species_name.split()

    if len(parts) == 2:
        return f"{parts[0].lower()}_{parts[1].lower()}"

    # Fallback for N/A, sp., hybrids, etc.
    return species_name.lower().replace(" ", "_")


def make_code(number, species_name):
    """Convert number + species name -> '1_GT'."""

    parts = species_name.split()

    if len(parts) < 2:
        return None

    genus = parts[0][0].upper()
    species = parts[1][0].upper()

    return f"{number}_{genus}{species}"


def main():
    parser = make_parser()
    args = parser.parse_args()

    csv_file = Path(args.csv)
    output_file = Path(args.output)
    species_dict = {}

    with csv_file.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            number = row["number"].strip()
            species_name = row["species_name"].strip()

            key = make_key(species_name)
            code = make_code(number, species_name)

            if key in species_dict:
                raise ValueError(f"Duplicate key: {key}")

            species_dict[key] = {
                "number": number,
                "code": code,
                "species_name": species_name,
                "common_name_zh": row["common_name_zh"].strip(),
                "common_name_en": row["common_name_en"].strip(),
                "subfamily": row["subfamily"].strip(),
                "tribe_name": row["tribe_name"].strip(),
            }

    with output_file.open("w", encoding="utf-8") as f:
        f.write("# Auto-generated from species0717.csv\n")
        f.write("# Do not edit manually.\n\n")
        f.write("SPECIES = ")
        f.write(pformat(species_dict, sort_dicts=False, width=100))
        f.write("\n")


if __name__ == "__main__":
    main()
