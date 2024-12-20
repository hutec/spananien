# Script to convert routes.geojson to routes.mbtiles using tippecanoe

docker run --rm \
    -v $PWD/tileserver-data:/data \
    locusq/tippecanoe:latest \
    tippecanoe --output=/data/spananien.mbtiles /data/routes.geojson -l strava -f