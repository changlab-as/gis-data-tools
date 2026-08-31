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
      <name>0430</name>
      <description>1_Grona_triflora, 6_Alysicarpus_vaginalis</description>
      <styleUrl>#icon-1899-0288D1</styleUrl>
      <Point>
        <coordinates>
          121.602414,25.083121,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>0431</name>
      <description>2_Grona_heterophylla, 1_Grona_triflora</description>
      <styleUrl>#icon-1899-0288D1</styleUrl>
      <Point>
        <coordinates>
          121.602327,25.082877,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>0432</name>
      <description>2_Grona_heterophylla</description>
      <styleUrl>#icon-1899-0288D1</styleUrl>
      <Point>
        <coordinates>
          121.602506,25.082634,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>0433</name>
      <description>X</description>
      <styleUrl>#icon-1899-0288D1</styleUrl>
      <Point>
        <coordinates>
          121.602868,25.082614,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>0434</name>
      <description>X</description>
      <styleUrl>#icon-1899-0288D1</styleUrl>
      <Point>
        <coordinates>
          121.603167,25.082674,0
        </coordinates>
      </Point>
    </Placemark>
    """

    return ET.fromstring(xml_text)


def test_parse_coordinates():
    """Test parse_coordinates function
    given a few pairs of coordinates, this function can correctly
    categorize them into lontitude and latitude pairs"""
