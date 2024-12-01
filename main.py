import json
import logging
import os

import gpxpy
from geojson import Feature, FeatureCollection, LineString

LOGGER = logging.getLogger(__name__)


def main():
    routes = []
    for file in os.listdir("./routes"):
        if file.endswith(".gpx"):
            with open(os.path.join("./routes", file)) as gpx_file:
                LOGGER.info(f"Reading {file}")
                gpx = gpxpy.parse(gpx_file)
                for track in gpx.tracks:
                    points = []
                    for segment in track.segments:
                        for point in segment.points:
                            points.append([point.longitude, point.latitude])
                    routes.append(Feature(geometry=LineString(points)))

    LOGGER.info("Writing geojson")
    geojson = FeatureCollection(routes)
    with open("tileserver-data/routes.geojson", "w") as f:
        json.dump(geojson, f)


if __name__ == "__main__":
    main()
