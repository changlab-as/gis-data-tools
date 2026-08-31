import csv
import xml.etree.ElementTree as ET
import pytest
import gis_data_tools.mymapkml2csv as kml2csv


@pytest.fixture
def standard_kml_coords():
    return "121.602486,25.082335 121.5, 24.05"


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


def test_parse_coordinates():
    """Test parse_coordinates function
    given a few pairs of coordinates, this function can correctly
    categorize them into lontitude and latitude pairs"""
