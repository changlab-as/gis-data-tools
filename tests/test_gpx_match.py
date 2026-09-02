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
            29,
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


@pytest.fixture
def waypoint_0m():
    return gpxpy.gpx.GPXWaypoint(
        latitude=25.0832406990,
        longitude=121.6025701538,
        elevation=20.1,
        time=datetime(2026, 7, 29, 0, 11, 29, tzinfo=timezone.utc),
    )


@pytest.fixture
def waypoint_5m():
    return gpxpy.gpx.GPXWaypoint(
        latitude=25.0832856984,
        longitude=121.6027333494,
        elevation=17.70,
        time=datetime(2026, 7, 29, 0, 12, 29, tzinfo=timezone.utc),
        name="5m",
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


@pytest.mark.parametrize(
    "waypoint_fixture, expected_index, expected_distance",
    [
        ("waypoint_0m", 0, 0.0),
        ("waypoint_5m", 6, 5.0),
        ("waypoint_0430", 6, 34.96),
        ("waypoint_0431", 7, 57.27),
    ],
)
def test_match_waypoint(
    request,
    trackpoints,
    waypoint_fixture,
    expected_index,
    expected_distance,
):
    waypoint = request.getfixturevalue(waypoint_fixture)

    closest, distance = match_trkpt_wpt.match_waypoint(
        waypoint,
        trackpoints,
    )

    assert closest is trackpoints[expected_index]
    assert distance == pytest.approx(expected_distance, abs=0.01)


# Functional tests
def test_main(
    tmp_path,
    monkeypatch,
    track_gpx,
    waypoint_0m,
    waypoint_5m,
    waypoint_0430,
):
    track_file = tmp_path / "track.gpx"
    waypoint_file = tmp_path / "waypoints.gpx"

    waypoint_gpx = gpxpy.gpx.GPX()
    waypoint_gpx.waypoints.extend(
        [
            waypoint_0m,
            waypoint_5m,
            waypoint_0430,
        ]
    )

    track_file.write_text(
        track_gpx.to_xml(),
        encoding="utf-8",
    )

    waypoint_file.write_text(
        waypoint_gpx.to_xml(),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "match_trkpt_wpt",
            "--track",
            str(track_file),
            "--waypoints",
            str(waypoint_file),
        ],
    )

    match_trkpt_wpt.main()


def test_main_update(
    tmp_path,
    monkeypatch,
    track_gpx,
    trackpoints,
    waypoint_0m,
    waypoint_5m,
    waypoint_0430,
):
    # Arrange
    track_file = tmp_path / "track.gpx"
    waypoint_file = tmp_path / "waypoints.gpx"
    output_file = tmp_path / "updated.gpx"

    waypoint_gpx = gpxpy.gpx.GPX()
    waypoint_gpx.waypoints.extend(
        [waypoint_0m, waypoint_5m, waypoint_0430]
    )

    track_file.write_text(track_gpx.to_xml(), encoding="utf-8")
    waypoint_file.write_text(waypoint_gpx.to_xml(), encoding="utf-8")

    # Act
    monkeypatch.setattr(
        "sys.argv",
        [
            "match_trkpt_wpt",
            "--track",
            str(track_file),
            "--waypoints",
            str(waypoint_file),
            "--update",
            "--output",
            str(output_file),
        ],
    )

    match_trkpt_wpt.main()

    # Assert
    assert output_file.exists()

    updated_gpx = gpxpy.parse(output_file.read_text(encoding="utf-8"))

    assert len(updated_gpx.waypoints) == 3

    updated_0430 = updated_gpx.waypoints[2]

    assert updated_0430.latitude == trackpoints[6].latitude
    assert updated_0430.longitude == trackpoints[6].longitude
    assert updated_0430.elevation == trackpoints[6].elevation
