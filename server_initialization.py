import sqlite3 as sql
import datetime

def initialize():
	conn = sql.connect("exampledb.db")

	cur = conn.cursor()

	cur.execute('''
					CREATE TABLE TRIPS
					(tripId integer PRIMARY KEY, username text, tripDate date, 
					 tripTime timestamp, tripLength integer, timesAlerted integer)
				''')

	cur.execute('''
					CREATE TABLE USERS
					(username text PRIMARY KEY, hashPass text)
				''')

	conn.close()

if __name__ == '__main__':
	initialize()

	print("DONE")