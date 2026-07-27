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
    numbers = re.findall(r"\d+", comment)
    return ", ".join(
        plant_id_lookup.get(number, number) for number in numbers
    )


def main():
    parser = make_parser()
    args = parser.parse_args()
    """
    get wp_path
    kml
    folder
    if type = collection
        process waypoint, decription goes through directly
    if type = survey
        get track_path
        get species_path
        process track
        process waypoints, description number translates into species_id
    """
    wp_path = Path(args.waypoints)
    output_path = Path(args.output)

    kml = simplekml.Kml()

    # Single folder -- presenting single layer in My Maps
    folder = kml.newfolder(name="YYYY-MM-DD_FT0000")

    gpx_waypoints = parse_gpx(wp_path)

    if args.type == "collection":
        for wp in gpx_waypoints.waypoints:
            folder.newpoint(
                name=wp.name or "Waypoint",
                coords=[(wp.longitude, wp.latitude)],
                description=wp.comment,
            )

    elif args.type == "survey":
        plant_id_lookup = load_plant_id_lookup(args.plant_names_csv)

        track_path = Path(args.track)
        gpx_tracks = parse_gpx(track_path)
        add_tracks(folder, gpx_tracks)

        for wp in gpx_waypoints.waypoints:
            desc = create_desc(plant_id_lookup, wp.comment)
            folder.newpoint(
                name=wp.name or "Waypoint",
                coords=[(wp.longitude, wp.latitude)],
                description=desc,
            )

    kml.save(output_path)

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
