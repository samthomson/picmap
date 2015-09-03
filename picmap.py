
import os
import sys
from os import listdir
from os.path import isfile, join
import sqlite3

from get_lat_lon_exif_pil import *
import get_lat_lon_exif_pil

import mapnik
import simplekml

def get_files(s_base_dir):
	fileList = []

	for root, subFolders, files in os.walk(s_base_dir):
		for file in files:
			f = os.path.join(root,file)
			fileList.append(f)

	return fileList

def get_db_files(db_cursor):
	db_cursor.execute('''SELECT file FROM files''')

	data=db_cursor.fetchall()
	COLUMN = 0
	fileList=[elt[COLUMN] for elt in data]

	return fileList

def get_db_file_rows(db_cursor):
	db_cursor.execute('''SELECT lat, lon FROM files''')

	data=db_cursor.fetchall()

	return data

def process_new_file(s_path):
	# get geo
	o_image = Image.open(s_path)
	exif_data = get_exif_data(o_image)
	lat_lon = get_lat_lon(exif_data)

	lat = 1000
	lon = 1000

	lat = lat_lon[0]
	lon = lat_lon[1]

	# add to files table
	cursor.execute('''INSERT OR IGNORE INTO files(file,lat,lon, hasgeo) VALUES(?,?,?,?)''', (s_path, lat, lon, 1,))

if __name__ == '__main__':

	print ("\npicmap :)")

	# get a db connection
	db = sqlite3.connect('files_database')
	cursor = db.cursor()

	# get files from disk
	physical_files = get_files('seed')
	i_physical_files = len(physical_files)

	# get files from db
	db_files = get_db_files(cursor)

	i_added = 0


	for s_physical_file_path in physical_files:
		if s_physical_file_path not in db_files:
			# new file, get geo and add to db
			process_new_file(s_physical_file_path)

			# we found it
			i_added += 1

	print "added %i files" % (i_added)

	# persist 
	db.commit()

	# render
	db_files = get_db_file_rows(cursor)

	#closee db
	db.close()

	print "%i files found to render" % (len(db_files))


	kml = simplekml.Kml()

	for r_file in db_files:
		pnt = kml.newpoint()
		#pnt.coords = [(r_file[0], r_file[1])]
		pnt.coords = [(r_file[1], r_file[0])]
		pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'


	kml.save('kml_geo.kml')



	width_in_px = 8000
	height_in_px = width_in_px / 2
	mapfile = 'mapnik_style.xml'

	map_canvas = mapnik.Map(width_in_px, height_in_px)
	mapnik.load_map(map_canvas, mapfile)
	map_canvas.background = mapnik.Color('rgb(0,0,0,0)') # transparent

	# Create a symbolizer to draw the points
	style = mapnik.Style()
	rule = mapnik.Rule()
	point_symbolizer = mapnik.MarkersSymbolizer()
	point_symbolizer.allow_overlap = True
	point_symbolizer.opacity = 1.0 # semi-transparent
	rule.symbols.append(point_symbolizer)
	style.rules.append(rule)
	map_canvas.append_style('GPS_tracking_points', style)

	# Create a layer to hold the ponts
	layer = mapnik.Layer('GPS_tracking_points')
	layer.datasource = mapnik.Ogr(file="kml_geo.kml", layer_by_index=0)
	layer.styles.append('GPS_tracking_points')
	map_canvas.layers.append(layer)

	# Save the map
	map_canvas.zoom_all()
	mapnik.render_to_file(map_canvas, 'GPS_tracking_points.png', 'png')
