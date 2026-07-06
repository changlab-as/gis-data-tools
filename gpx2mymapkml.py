import argparse
import gpxpy
import simplekml
from pathlib import Path


def make_parser():
    parser = argparse.ArgumentParser(
        description="""Convert Garmin GPX (track + waypoints) to
        a single My Maps-friendly KML"""
    )

    parser.add_argument(
        "--track", "-t", required=True, help="Track GPX file"
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


def add_waypoints(folder, gpx):
    for wp in gpx.waypoints:
        desc_parts = []

        if wp.comment:
            desc_parts.append(f"Comment: {wp.comment}")

        description = "\n".join(desc_parts) if desc_parts else None

        folder.newpoint(
            name=wp.name or "Waypoint",
            coords=[(wp.longitude, wp.latitude)],
            description=description,
        )


def main():
    parser = make_parser()
    args = parser.parse_args()

    track_path = Path(args.track)
    wp_path = Path(args.waypoints)
    output_path = Path(args.output)

    gpx_tracks = parse_gpx(track_path)
    gpx_waypoints = parse_gpx(wp_path)

    kml = simplekml.Kml()

    # Single folder -- presenting single layer in My Maps
    folder = kml.newfolder(name="Survey Locations")

    add_tracks(folder, gpx_tracks)
    add_waypoints(folder, gpx_waypoints)

    kml.save(output_path)

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
