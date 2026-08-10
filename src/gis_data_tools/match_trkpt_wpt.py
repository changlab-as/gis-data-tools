import argparse
from datetime import datetime, timezone
import gpxpy
import gpxpy.geo
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)


def make_parser():
    parser = argparse.ArgumentParser(
        description="""Match trackpoint and waypoint GPX files using recorded
        time and coordinates. If a wpt's distance to the closest trkpt is
        over 5m, the wpt and trkpt are considered unmatched.
        If "update" is flagged (-u), a new gpx file will be created with the
        unmatched wpt's coordinated updated to the most recent trkpt's
        coordinates.
        """
    )
    parser.add_argument(
        "--update",
        "-u",
        action="store_true",
        help="update waypoint file's coords to match with trackpoint file",
    )
    parser.add_argument(
        "--track",
        "-t",
        required=True,
        help="Track GPX file",
    )
    parser.add_argument(
        "--waypoints", "-w", required=True, help="Waypoints GPX file"
    )
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


def get_trackpoints(trk_gpx):
    """Get all trackpoints from the GPX file into a list"""
    return [
        point
        for track in trk_gpx.tracks
        for segment in track.segments
        for point in segment.points
    ]


def find_closest_trackpoint(waypoint, trackpoints):
    """Iterate through trackpoints and find the closest one"""
    closest_trackpoint = None
    smallest_time_difference = None

    for trackpoint in trackpoints:
        time_difference = abs(trackpoint.time - waypoint.time)

        if (
            smallest_time_difference is None
            or time_difference < smallest_time_difference
        ):
            closest_trackpoint = trackpoint
            smallest_time_difference = time_difference

    return closest_trackpoint


def main():

    parser = make_parser()
    args = parser.parse_args()

    wp_path = Path(args.waypoints)
    trk_path = Path(args.track)
    output_path = Path(args.output)

    wp_gpx = parse_gpx(wp_path)
    trk_gpx = parse_gpx(trk_path)

    unmatched = []
    matched = []

    all_trkpts = get_trackpoints(trk_gpx)

    for wp in wp_gpx.waypoints:
        closest_trkpt = find_closest_trackpoint(wp, all_trkpts)
        distance = gpxpy.geo.distance(
            wp.latitude,
            wp.longitude,
            wp.elevation,
            closest_trkpt.latitude,
            closest_trkpt.longitude,
            closest_trkpt.elevation,
        )
        if distance > 5:
            unmatched.append(wp)
            logging.info(f"{wp.name} is unmatched")

            if args.update:
                # if update is flagged in the argument, wpt will be updated
                wp.latitude = closest_trkpt.latitude
                wp.longitude = closest_trkpt.longitude
                wp.elevation = closest_trkpt.elevation
        else:
            matched.append(wp)

    logging.info(f"""there are {len(unmatched)} unmatched waypoints
                     and {len(matched)} matched waypoints""")

    if args.update:
        """Create a new gpx file to update waypoints' coordinates
        to the closest trackpoints' coordinates"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(wp_gpx.to_xml())
            logging.info(
                f"{output_path} has been created! Waypoints updated."
            )


if __name__ == "__main__":
    main()
