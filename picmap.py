
import os
import sys
from os import listdir
from os.path import isfile, join
import sqlite3

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
	'''
	add to db, queue accordingly
	'''
	# add to files table
	cursor.execute('''INSERT OR IGNORE INTO files(file) VALUES(?)''', (s_path,))

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
			i_added += 1

	print ("added %i files", (i_added))



	"""
	for i in range(i_files):
		if(files[i].endswith(('.jpg', '.JPG', '.jpeg', '.JPEG'))):
			print ("file %s" % (files[i]))

			# if the file isn't in our index already get it's geo and add it
			the_id_of_the_row = None
			for row in cursor.execute("SELECT id FROM files WHERE file = ?", (files[i],):
				the_id_of_the_row = row[0]
			if the_id_of_the_row is None:
				cursor = sql.cursor()
				cursor.execute('''INSERT OR IGNORE INTO files(file) VALUES(?)''', files[i])
				print ("added file %s", files[i])
				the_id_of_the_row = cursor.lastrowid
			

	"""

	# persist and closee db
	db.commit()
	db.close()