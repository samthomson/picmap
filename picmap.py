
import os
import sys
from os import listdir
from os.path import isfile, join
import sqlite3

from get_lat_lon_exif_pil import *
import get_lat_lon_exif_pil

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

def process_new_file(s_path):
	# get geo
	o_image = Image.open(s_path)
	exif_data = get_exif_data(o_image)
	lat_lon = get_lat_lon(exif_data)

	lat = 1000
	lon = 1000

	lat = lat_lon[0]
	lon = lat_lon[1]

	"""
	try:
		lat = lat_lon[0]
		lon = lat_lon[1]
	except:
		lat = 1000
	else:
		lat = 1000
	"""

	"""
	if lat_lon[0] not None:
		lat = lat_lon[0]

	if lat_lon[1] not None:
		lon = lat_lon[1]
	"""

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

	print ("added %i files", (i_added))



	# persist and closee db
	db.commit()
	db.close()