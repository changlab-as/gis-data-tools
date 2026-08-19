from datetime import datetime, timezone

import gpxpy
import pytest

import gis_data_tools.match_trkpt_wpt as match_trkpt_wpt


@pytest.fixture
def trackpoints():
    return [
        gpxpy.gpx.GPXTrackPoint(
            latitude=25.0832406990,
            longitude=121.6025701538,
            elevation=20.11,
            time=datetime(2026, 7, 29, 0, 11, 29, tzinfo=timezone.utc),
        ),
        gpxpy.gpx.GPXTrackPoint(
            latitude=25.0832093507,
            longitude=121.6025981493,
            elevation=19.60,
            time=datetime(2026, 7, 29, 0, 11, 39, tzinfo=timezone.utc),
        ),
        gpxpy.gpx.GPXTrackPoint(
            latitude=25.0831618253,
            longitude=121.6026286595,
            elevation=19.79,
            time=datetime(2026, 7, 29, 0, 11, 49, tzinfo=timezone.utc),
        ),
        gpxpy.gpx.GPXTrackPoint(
            latitude=25.0831303932,
            longitude=121.6026488598,
            elevation=19.26,
            time=datetime(2026, 7, 29, 0, 11, 59, tzinfo=timezone.utc),
        ),
        gpxpy.gpx.GPXTrackPoint(
            latitude=25.0830908306,
            longitude=121.6026596725,
            elevation=18.79,
            time=datetime(2026, 7, 29, 0, 12, 9, tzinfo=timezone.utc),
        ),
        gpxpy.gpx.GPXTrackPoint(
            latitude=25.0831651781,
            longitude=121.6026978940,
            elevation=18.84,
            time=datetime(2026, 7, 29, 0, 12, 19, tzinfo=timezone.utc),
        ),
        gpxpy.gpx.GPXTrackPoint(
            latitude=25.0832407828,
            longitude=121.6027333494,
            elevation=17.70,
            time=datetime(2026, 7, 29, 0, 12, 29, tzinfo=timezone.utc),
        ),
        gpxpy.gpx.GPXTrackPoint(
            latitude=25.0832418725,
            longitude=121.6027258895,
            elevation=19.04,
            time=datetime(2026, 7, 29, 0, 12, 39, tzinfo=timezone.utc),
        ),
    ]


@pytest.fixture
def track_gpx(trackpoints):
    gpx = gpxpy.gpx.GPX()

    track = gpxpy.gpx.GPXTrack()
    segment = gpxpy.gpx.GPXTrackSegment()

    segment.points.extend(trackpoints)
    track.segments.append(segment)
    gpx.tracks.append(track)

    return gpx


@pytest.fixture
def waypoint_0429():
    return gpxpy.gpx.GPXWaypoint(
        latitude=25.0832407828,
        longitude=121.6027333494,
        elevation=17.7,
        time=datetime(
            2026,
            7,
            29,
            0,
            10,
            00,
            tzinfo=timezone.utc,
        ),
        name="0429",
        comment="1,2",
        symbol="Flag, Blue",
    )


@pytest.fixture
def waypoint_0430():
    return gpxpy.gpx.GPXWaypoint(
        latitude=25.0831212569,
        longitude=121.6024137475,
        elevation=20.27,
        time=datetime(
            2026,
            7,
            29,
            0,
            12,
            27,
            tzinfo=timezone.utc,
        ),
        name="0430",
        comment="1,6",
        symbol="Flag, Blue",
    )


@pytest.fixture
def waypoint_0431():
    return gpxpy.gpx.GPXWaypoint(
        latitude=25.0828773435,
        longitude=121.6023270786,
        elevation=14.99,
        time=datetime(
            2026,
            7,
            29,
            0,
            20,
            1,
            tzinfo=timezone.utc,
        ),
        name="0431",
        comment="2,1",
        symbol="Flag, Blue",
    )


# Unit test
def test_get_trackpoints(track_gpx, trackpoints):
    """Test that get_trackpoints gets all trackpoints"""
    result = match_trkpt_wpt.get_trackpoints(track_gpx)

    assert result == trackpoints


@pytest.mark.parametrize(
    "waypoint_fixture, expected_index",
    [
        ("waypoint_0429", 0),
        ("waypoint_0430", 6),
        ("waypoint_0431", 7),
    ],
)
def test_find_closest_trackpoint(
    request, trackpoints, waypoint_fixture, expected_index
):
    """Test find_closest_trackpoint using waypoint fixture"""
    waypoint = request.getfixturevalue(waypoint_fixture)

    result = match_trkpt_wpt.find_closest_trackpoint(
        waypoint,
        trackpoints,
    )

    assert result is trackpoints[expected_index]


def test_find_closest_trackpoint_exact_time(trackpoints):
    """Test find_closest_trackpoint using exact time"""
    waypoint = gpxpy.gpx.GPXWaypoint(
        latitude=25.0832407828,
        longitude=121.6027333494,
        time=datetime(
            2026,
            7,
            29,
            0,
            12,
            29,
            tzinfo=timezone.utc,
        ),
    )

    result = match_trkpt_wpt.find_closest_trackpoint(
        waypoint,
        trackpoints,
    )

    assert result is trackpoints[6]


def test_find_closest_trackpoint_empty(waypoint_0429):
    result = match_trkpt_wpt.find_closest_trackpoint(
        waypoint_0429,
        [],
    )

    assert result is None
