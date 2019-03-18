# picmap

picmap recursively scans a seed directory and builds up an index of files, noting their latitude/longitude exif tags if set. It then renders a map with a marker for each picture it has a location for.

## notes

Requires docker and docker-compose.

Makes use of:
- python 2
- pil
- mapnik
- simplekml

[![picmap](https://github.com/samthomson/picmap/blob/master/sample.png?raw=trueg)](https://github.com/samthomson/picmap/blob/master/sample.png?raw=true)


## running

build the image:
`docker-compose build picmap`

replace `/home/sam/Dropbox/folder-to-map-into-picmap` in `docker-compose.yml` to a folder on your machine that will map to the seed folder within the container. This should contain the geotagged pictures you want rendered on a map. Pictures can be in nested folders.

run the script:
`docker-compose run picmap bash "picmap/run.sh"`

it will then generate a map here: `./out/GPS_tracking_points.png`.