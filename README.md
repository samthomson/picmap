# picmap

picmap recursively scans a seed directory and builds up an index of files, noting their latitude/longitude exif tags if set. It then renders a map with a marker for each picture it has a location for.

## requires

- python 2
- pil
- picmap
- simplekml

[![picmap](https://github.com/samthomson/picmap/blob/master/GPS_tracking_points.png?raw=trueg)](https://github.com/samthomson/picmap/blob/master/GPS_tracking_points.png?raw=true)


## running

build the image:
`docker-compose build picmap`

set a folder in docker-compose to map to seed.

bash into the container:
`docker-compose run picmap bash "picmap/run.sh"`

run script `python picmap/src/setup.py`
run script `python picmap/src/picmap.py`