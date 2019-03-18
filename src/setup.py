# this script is responsible for creating the database and tables

import sqlite3
import os

if __name__ == '__main__':

	#create/open db connection	
	db = sqlite3.connect('./out/files_database')

	cursor = db.cursor()
	
	cursor.execute('''
		DROP TABLE IF EXISTS files;

	''')
	cursor.execute('''
		CREATE TABLE files(id INTEGER, file TINYTEXT PRIMARY KEY,
	                   lat REAL,
	                   lon REAL,
	                   hasgeo INTEGER)

	''')
	
	
	cursor.execute('''
		CREATE INDEX filepath_index ON files (file)
	''')
	

	db.commit()
	db.close()