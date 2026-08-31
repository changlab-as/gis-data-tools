import csv
import xml.etree.ElementTree as ET
import pytest
import gis_data_tools.mymapkml2csv as kml2csv


@pytest.fixture
def standard_kml_coords():
    return "121.602486,25.082335 121.5,24.05"


@pytest.fixture
def lat_lon_coords():
    return "25.082335,121.602486 25.05,121.5"


@pytest.fixture
def polygon_coords():
    return [
        (121.6028516, 25.0820827),
        (121.6028798, 25.0821277),
        (121.6027939, 25.0821264),
        (121.6027859, 25.0820754),
        (121.6028516, 25.0820827),
    ]


@pytest.fixture
def polygon_placemarks():
    xml_text = """
    <Placemark>
      <name>polygon01</name>
      <description>1_Grona_triflora</description>
      <styleUrl>#poly-E65100-1200-77</styleUrl>
      <Polygon>
        <outerBoundaryIs>
          <LinearRing>
            <tessellate>1</tessellate>
            <coordinates>
              121.6028361,25.082438,0
              121.6027623,25.082449,0
              121.6027368,25.0823895,0
              121.6027703,25.082353,0
              121.602844,25.082375,0
              121.6028361,25.082438,0
            </coordinates>
          </LinearRing>
        </outerBoundaryIs>
      </Polygon>
    </Placemark>
    <Placemark>
      <name>polygon02</name>
      <description>X</description>
      <styleUrl>#poly-000000-1200-77</styleUrl>
      <Polygon>
        <outerBoundaryIs>
          <LinearRing>
            <tessellate>1</tessellate>
            <coordinates>
              121.6025583,25.0823609,0
              121.6025583,25.082446,0
              121.6024778,25.0824229,0
              121.6024751,25.0823512,0
              121.6025583,25.0823609,0
            </coordinates>
          </LinearRing>
        </outerBoundaryIs>
      </Polygon>
    </Placemark>
    <Placemark>
      <name>polygon03</name>
      <description>1_Grona_triflora, 2_Grona_heterophylla</description>
      <styleUrl>#poly-E65100-1200-77</styleUrl>
      <Polygon>
        <outerBoundaryIs>
          <LinearRing>
            <tessellate>1</tessellate>
            <coordinates>
              121.6025381,25.0824897,0
              121.6025207,25.0825383,0
              121.6024282,25.0825006,0
              121.6024671,25.0824472,0
              121.6025381,25.0824897,0
            </coordinates>
          </LinearRing>
        </outerBoundaryIs>
      </Polygon>
    </Placemark>
    """

    return ET.fromstring(xml_text)


@pytest.fixture
def plant_file(tmp_path):
    file = tmp_path / "plant.csv"

    file.write_text(
        """plant_id
        1_Grona_triflora
        2_Grona_heterophylla
        3_Medicago_lupulina""",
        encoding="utf-8",
    )
    return file


def test_parse_standard_kml_coords(standard_kml_coords):
    result = kml2csv.parse_coordinates(standard_kml_coords)

    assert result == [
        (121.602486, 25.082335),
        (121.5, 24.05),
    ]


def test_parse_lat_lon_coords(lat_lon_coords):
    result = kml2csv.parse_coordinates(lat_lon_coords)

    assert result == [
        (121.602486, 25.082335),
        (121.5, 25.05),
    ]


def test_parse_empty_coords():
    result = kml2csv.parse_coordinates("")

    assert result == []


def test_polygon_centroid(polygon_coords):
    result = kml2csv.polygon_centroid(polygon_coords)

    assert result == (25.08209898, 121.60283256)


def test_polygon_centroid_empty():
    lat, lon = kml2csv.polygon_centroid([])

    assert lat is None
    assert lon is None
