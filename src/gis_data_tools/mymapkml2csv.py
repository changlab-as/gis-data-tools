import argparse
import csv
import logging
import xml.etree.ElementTree as ET
from pathlib import Path

logging.basicConfig(level=logging.INFO)


def make_parser():
    parser = argparse.ArgumentParser(
        description="Extract polygon centroids from KML (Google My Maps)"
    )
    parser.add_argument("--kml_path", "-k", help="Path to input KML file")
    parser.add_argument(
        "-o", "--output", default="output.csv", help="Output CSV path"
    )
    parser.add_argument(
        "--plant_names_csv",
        "-p",
        required=True,
        help="Required. The most recent plant_names csv sheet",
    )
    return parser


def parse_coordinates(coord_text: str) -> list[tuple[float, float]]:
    """
    Parse coordinate string into list of (lon, lat). Distinguish lat and lon by
    the pair's degrees, currently lat <= 90, lon > 90
    """
    coords = []

    for line in coord_text.strip().split():
        parts = line.split(",")

        a = float(parts[0])
        b = float(parts[1])

        # Detect format
        if abs(a) <= 90 and abs(b) > 90:
            # lat, lon
            lat, lon = a, b
        else:
            # lon, lat (standard KML)
            lon, lat = a, b

        coords.append((lon, lat))  # normalize

    return coords


def polygon_centroid(
    coords: list[tuple[float, float]],
) -> tuple[float | None, float, None]:
    """
    Calculate the central point of a polygon using its average of vertices
    """
    if not coords:
        return None, None

    lon_sum = sum(p[0] for p in coords)
    lat_sum = sum(p[1] for p in coords)

    n = len(coords)

    return lat_sum / n, lon_sum / n


def extract_polygons(kml_path: Path) -> list:
    """
    Loop through KML file and [arse polygon placemarks out of KML
    Process polygon centroids (use another function within this one)
    Return a list of dictionaries, each of which is a polygon's data
    """
    tree = ET.parse(kml_path)
    root = tree.getroot()

    ns = {"kml": "http://www.opengis.net/kml/2.2"}

    results = []

    for placemark in root.findall(".//kml:Placemark", ns):
        name_elem = placemark.find("kml:name", ns)
        description_elem = placemark.find("kml:description", ns)
        polygon = placemark.find(".//kml:Polygon", ns)

        if polygon is None:
            continue

        coord_elem = polygon.find(".//kml:coordinates", ns)
        if coord_elem is None:
            continue

        coords = parse_coordinates(coord_elem.text)
        lat, lon = polygon_centroid(coords)  # process polygon coords

        if lat is None or lon is None:
            continue

        results.append(
            {
                "survey_site": (
                    name_elem.text if name_elem is not None else ""
                ),
                "latitude": lat,
                "longitude": lon,
                "description": (
                    description_elem.text
                    if description_elem is not None
                    else ""
                ),
            }
        )

    return results


def write_csv(data: list, plant_names: Path, output_path: str | Path):
    """
    Read plant_names_csv and get most recent plant IDs
    Loop through each polygon and get its coords and description fields to
      create each polygon's row/record
    Write these rows into the new CSV output file
    """
    with open(plant_names, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        plant_fields = [row["plant_id"] for row in reader]

    fieldnames = ["survey_site", "coordinates", *plant_fields]

    rows = []

    for row in data:
        coord_str = f"{row['latitude']:.6f}, {row['longitude']:.6f}"
        csv_row = {
            "survey_site": row["survey_site"],
            "coordinates": coord_str,
        }
        for plant_id in plant_fields:
            if plant_id in row["description"]:
                csv_row[plant_id] = "T"
            else:
                csv_row[plant_id] = "F"
        rows.append(csv_row)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_MINIMAL,
        )

        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = make_parser()
    args = parser.parse_args()

    kml_path = Path(args.kml_path)

    if not kml_path.exists():
        logging.error(f"Error: no or incorrect KML file path ({kml_path})")
        return

    polygons = extract_polygons(kml_path)
    write_csv(polygons, args.plant_names_csv, args.output)

    logging.info(f"Extracted {len(polygons)} polygons to {args.output}")


if __name__ == "__main__":
    main()
