import argparse
from datetime import datetime, timezone
import gpxpy
import simplekml
from pathlib import Path


def make_parser():
    parser = argparse.ArgumentParser(
        description="""match track point and waypoint GPX files using recorded
        time and coordinates. If update is selected, wpt gpx coordinates will 
        be updated to most recent track point coordinates
        """
    )
    parser.add_argument(
        "--update",
        "-u",
        required=False,
        help="update waypoint file's coords to match with trackpoint file",
    )
    parser.add_argument(
        "--track",
        "-t",
        required=True,
        help="Track GPX file",
    )
    parser.add_argument("--waypoints", "-w", required=True, help="Waypoints GPX file")
    parser.add_argument(
        "-o",
        "--output",
        default="updated_wpt.gpx",
        help="updated waypoint file (default: updated_wpt.gpx)",
    )
    return parser

def parse_gpx(path):
    with open(path, "r", encoding="utf-8") as f:
        return gpxpy.parse(f)


def main():
    """
    - find a waypoint's closest trackpoint using the time
    - calculate two points' distance
    - if distance is smaller than 5 meters, it is considered matched
    - if not, indicates how many track points are not matched, and return a list
      of waypoint's <name>
    """

    parser = make_parser()
    args = parser.parse_args()

    wp_path = Path(args.waypoints)
    trk_path = Path(args.track)
    output_path = Path(args.output)

    wp_gpx = parse_gpx(wp_path)
    trk_gpx = parse_gpx(trk_path)
    print(type(wp_gpx.waypoints[0].time))

    unmatched = []



    if args.update:
        """update waypoints' coordinates to closest trackpoints' coords"""


if __name__ == "__main__":
    main()
