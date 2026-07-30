import argparse
import gpxpy
import simplekml
from pathlib import Path
import csv
import re


def make_parser():
    parser = argparse.ArgumentParser(
        description="""Convert Garmin GPX to a single My Maps-friendly KML
        based on the type of event took place"""
    )
    parser.add_argument(
        "--type", "-ty", required=True, help="'survey' or 'collection'"
    )
    parser.add_argument(
        "--track",
        "-t",
        required=False,
        help="Track GPX file. Add it when it is a SURVEY event",
    )
    parser.add_argument(
        "--waypoints", "-w", required=True, help="Waypoints GPX file"
    )
    parser.add_argument(
        "-o",
        "--output",
        default="combined.kml",
        help="Output KML file (default: combined.kml)",
    )
    parser.add_argument(
        "--plant_names_csv",
        "-p",
        required=False,
        help="Add it when it is a SURVEY event",
    )
    return parser


def parse_gpx(path):
    with open(path, "r", encoding="utf-8") as f:
        return gpxpy.parse(f)


def add_tracks(folder, gpx):
    all_coords = []

    for track in gpx.tracks:
        for segment in track.segments:
            all_coords.extend(
                (p.longitude, p.latitude, p.elevation or 0)
                for p in segment.points
            )

    if all_coords:
        line = folder.newlinestring(name="Track", coords=all_coords)
        line.style.linestyle.width = 3
        line.style.linestyle.color = simplekml.Color.red


def load_plant_id_lookup(plant_names_csv):
    with open(plant_names_csv, encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return {
            row["number"].strip(): row["plant_id"].strip()
            for row in reader
        }


def create_desc(plant_id_lookup, comment: str | None) -> str:
    """Convert species numbers from a GPX <cmt> field into species codes"""
    if not comment:
        return ""

    tokens = re.findall(r"\d+|[A-Za-z]+", comment)

    return ", ".join(plant_id_lookup.get(token, token) for token in tokens)


def add_collection_waypoints(folder, waypoints):
    for wp in waypoints:
        folder.newpoint(
            name=wp.name or "Waypoint",
            coords=[(wp.longitude, wp.latitude)],
            description=wp.comment,
        )


def add_survey_waypoints(folder, waypoints, plant_id_lookup):
    for wp in waypoints:
        description = create_desc(
            plant_id_lookup,
            wp.comment,
        )

        folder.newpoint(
            name=wp.name or "Waypoint",
            coords=[(wp.longitude, wp.latitude)],
            description=description,
        )


def main():
    parser = make_parser()
    args = parser.parse_args()

    wp_path = Path(args.waypoints)
    output_path = Path(args.output)

    kml = simplekml.Kml()
    kml_folder = kml.newfolder(name="YYYY-MM-DD_FT0000")

    wp_gpx = parse_gpx(wp_path)

    if args.type == "collection":
        add_collection_waypoints(kml_folder, wp_gpx.waypoints)

    elif args.type == "survey":
        if not args.track or not args.plant_names_csv:
            parser.error(
                "--track and --plant_names_csv are required for survey"
            )
        plant_id_lookup = load_plant_id_lookup(args.plant_names_csv)

        track_gpx = parse_gpx(Path(args.track))
        add_tracks(kml_folder, track_gpx)

        add_survey_waypoints(
            kml_folder,
            wp_gpx.waypoints,
            plant_id_lookup,
        )

    kml.save(output_path)

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
