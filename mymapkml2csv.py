import argparse
import csv
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_coordinates(coord_text):
    """
    Parse coordinate string into list of (lon, lat)

    Handles both:
    - KML standard: lon,lat[,alt]
    - Your case: lat,lon

    Auto-detects based on value range.
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


def polygon_centroid(coords):
    """
    Simple centroid (average of vertices)
    Works well for small polygons
    """
    if not coords:
        return None, None

    lon_sum = sum(p[0] for p in coords)
    lat_sum = sum(p[1] for p in coords)

    n = len(coords)

    return lat_sum / n, lon_sum / n


def extract_polygons(kml_path):
    tree = ET.parse(kml_path)
    root = tree.getroot()

    ns = {"kml": "http://www.opengis.net/kml/2.2"}

    results = []

    for placemark in root.findall(".//kml:Placemark", ns):
        name_elem = placemark.find("kml:name", ns)
        polygon = placemark.find(".//kml:Polygon", ns)

        if polygon is None:
            continue

        coord_elem = polygon.find(".//kml:coordinates", ns)
        if coord_elem is None:
            continue

        coords = parse_coordinates(coord_elem.text)
        lat, lon = polygon_centroid(coords)

        if lat is None or lon is None:
            continue

        results.append(
            {
                "survey_site": (
                    name_elem.text if name_elem is not None else ""
                ),
                "latitude": lat,
                "longitude": lon,
            }
        )

    return results


def write_csv(data, output_path):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "survey_site",
                "coordinates",
                "1_蠅翼草",
                "2_山螞蝗",
                "3_天藍苜蓿",
                "4_含羞草",
                "5_草木樨",
                "6_煉莢豆",
                "7_雞眼草",
                "8_蔓花生",
                "9_白三葉草",
                "10_假地豆",
                "11_穗花木藍",
                "12_胡枝子",
                "13_假山扁豆",
                "14_太陽麻",
                "15_鋪地蝙蝠草",
                "16_銀合歡",
                "17_倒卵葉木藍",
                "18_疑似一條根",
                "19_寬翼豆",
                "20_田菁",
            ],
            quoting=csv.QUOTE_MINIMAL,  # ensures quotes when needed
        )

        writer.writeheader()

        for row in data:
            coord_str = f"{row['latitude']:.6f}, {row['longitude']:.6f}"

            writer.writerow(
                {
                    "survey_site": row["survey_site"],
                    "coordinates": coord_str,
                }
            )


def main():

    parser = argparse.ArgumentParser(
        description="Extract polygon centroids from KML (Google My Maps)"
    )
    parser.add_argument("--kml_path", "-k", help="Path to input KML file")
    parser.add_argument(
        "-o", "--output", default="output.csv", help="Output CSV path"
    )

    args = parser.parse_args()

    kml_path = Path(args.kml_path)

    if not kml_path.exists():
        print(f"Error: file not found {kml_path}")
        return

    data = extract_polygons(kml_path)
    write_csv(data, args.output)

    print(f"Extracted {len(data)} polygons to {args.output}")


if __name__ == "__main__":
    main()
