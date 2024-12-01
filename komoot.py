import json
import logging
import os
import re

from dotenv import find_dotenv, load_dotenv
from geojson import Feature, FeatureCollection, LineString
from kompy import KomootConnector

load_dotenv(find_dotenv())

LOGGER = logging.getLogger(__name__)

with open("urls.json") as f:
    urls = json.load(f)["urls"]

connector = KomootConnector(
    email=os.getenv("KOMOOT_MAIL"),
    password=os.getenv("KOMOOT_PASSWORD"),
)

routes = []
for url in urls:
    LOGGER.info(f"Reading {url}")
    tour_id = re.search(r"tour/(\d+)", url).group(1)
    share_token = re.search(r"share_token=([^&]+)", url).group(1)
    gpx = connector.get_tour_by_id(tour_id, share_token=share_token, object_type="gpx")

    for track in gpx.tracks:
        points = []
        for segment in track.segments:
            for point in segment.points:
                points.append([point.longitude, point.latitude])

        routes.append(
            Feature(
                geometry=LineString(points),
                properties={"name": track.name, "id": tour_id, "url": url},
            ),
        )

    LOGGER.info("Writing geojson")
    geojson = FeatureCollection(routes)
    with open("tileserver-data/routes.geojson", "w") as f:
        json.dump(geojson, f)
