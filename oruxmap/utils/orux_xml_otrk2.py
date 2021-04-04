import pathlib
from oruxmap.utils.projection import BoundsWGS84

TEMPLATE_LAYER_BEGIN = """    <OruxTracker xmlns="http://oruxtracker.com/app/res/calibration" versionCode="2.1">
      <MapCalibration layers="false" layerLevel="{id}">
        <MapName><![CDATA[{map_name} {id:d}]]></MapName>
        <MapChunks xMax="{xMax}" yMax="{yMax}" datum="CH-1903:Swiss@WGS 1984:Global Definition" projection="(SUI) Swiss Grid" img_height="{TILE_SIZE}" img_width="{TILE_SIZE}" file_name="{map_name}" />
        <MapDimensions height="{height}" width="{width}" />
        <MapBounds minLat="{minLat:2.6f}" maxLat="{maxLat:2.6f}" minLon="{minLon:2.6f}" maxLon="{maxLon:2.6f}" />
        <CalibrationPoints>
"""

TEMPLATE_LAYER_END = """        </CalibrationPoints>
      </MapCalibration>
    </OruxTracker>
"""


TEMPLATE_MAIN_START = """<?xml version="1.0" encoding="UTF-8"?>
<OruxTracker xmlns="http://oruxtracker.com/app/res/calibration" versionCode="3.0">
  <MapCalibration layers="true" layerLevel="0">
    <MapName><![CDATA[{map_name}]]></MapName>
"""

TEMPLATE_MAIN_END = """  </MapCalibration>
</OruxTracker>"""

class OruxXmlOtrk2:
    def __init__(self, filename: pathlib.Path, map_name: str):
        assert isinstance(filename, pathlib.Path)
        assert isinstance(map_name, str)
        self.f = filename.open("w")
        self.f.write(TEMPLATE_MAIN_START.format(map_name=map_name))

    def write_layer(self, calib: BoundsWGS84, **params):
        assert isinstance(calib, BoundsWGS84)

        self.f.write(
            TEMPLATE_LAYER_BEGIN.format(**params)
        )

        for strPoint, lon, lat in (
            ("TL", calib.northWest.lon, calib.northWest.lat),
            ("BR", calib.southEast.lon, calib.southEast.lat),
            ("TR", calib.northEast.lon, calib.northEast.lat),
            ("BL", calib.southWest.lon, calib.southWest.lat),
        ):
            self.f.write(f'          <CalibrationPoint corner="{strPoint}" lon="{lon:2.6f}" lat="{lat:2.6f}" />\n')

        self.f.write(TEMPLATE_LAYER_END)

    def close(self):
        self.f.write(TEMPLATE_MAIN_END)
        self.f.close()
