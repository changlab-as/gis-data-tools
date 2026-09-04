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
def point_placemark_file(tmp_path):
    fp = tmp_path / "point_placemark.kml"

    xml_text = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
      <Document>
        <Placemark>
          <name>0621</name>
          <description>8_Arachis_pintoi</description>
          <styleUrl>#icon-1899-0288D1</styleUrl>
          <Point>
            <coordinates>
              121.59205,25.043945,0
            </coordinates>
          </Point>
        </Placemark>
      </Document>
    </kml>
    """
    fp.write_text(xml_text, encoding="utf-8")

    return fp


@pytest.fixture
def polygon_placemarks_file(tmp_path):
    fp = tmp_path / "polygon_placemarks.kml"

    xml_text = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
      <Document>
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
      </Document>
    </kml>
    """
    fp.write_text(xml_text, encoding="utf-8")

    return fp


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


def test_extract_empty_polygons(point_placemark_file):
    result = kml2csv.extract_polygons(point_placemark_file)

    assert result == []


def test_extract_polygons(polygon_placemarks_file):
    result = kml2csv.extract_polygons(polygon_placemarks_file)

    assert result == [
        {
            "survey_site": "polygon01",
            "latitude": 25.082407083333333,
            "longitude": 121.60279759999999,
            "description": "1_Grona_triflora",
        },
        {
            "survey_site": "polygon02",
            "latitude": 25.08238838,
            "longitude": 121.60252556,
            "description": "X",
        },
        {
            "survey_site": "polygon03",
            "latitude": 25.0824931,
            "longitude": 121.60249844,
            "description": "1_Grona_triflora, 2_Grona_heterophylla",
        },
    ]
