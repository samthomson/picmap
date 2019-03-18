# picmap

picmap recursively scans a seed directory and builds up an index of files, noting their latitude/longitude exif tags if set. It then renders a map with a marker for each picture it has a location for.

## requires

- python 2
- pil
- picmap
- simplekml

[![picmap](https://github.com/samthomson/picmap/blob/master/sample.png?raw=trueg)](https://github.com/samthomson/picmap/blob/master/sample.png?raw=true)


## running

build the image:
`docker-compose build picmap`

replace `/home/sam/Dropbox/folder-to-map-into-picmap` in `docker-compose.yml` to a folder on your machine that will map to the seed folder within the container. This should contain the geotagged pictures you want rendered on a map. Pictures can be in nested folders.

bash into the container:
`docker-compose run picmap bash "picmap/run.sh"`

run script `python picmap/src/setup.py`
run script `python picmap/src/picmap.py`