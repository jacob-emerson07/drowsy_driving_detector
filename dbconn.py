import sqlite3 as sql
import pandas as pd

class DBConn:

	def __init__(self):
		self._connect_to_db()


	def __del__(self):
		self._close_conn()


	def user_exists(self, user):

		output = self.cur.execute(f"SELECT username from USERS WHERE username = '{user}'")

		try:
			usern = next(output)[0]
			if user == usern:
				return True

		except StopIteration:
			return False

		return False

	def add_user(self, user, h_passw):
		if not self.user_exists(user):

			self.cur.execute(f"INSERT INTO USERS VALUES (?, ?)", (user, h_passw))

			print(f"User Added: {user}")

			self.conn.commit()
		
		else:
			print("Username Taken")

	def validate_user(self, user, h_passw):
		if self.user_exists(user):
			x = self.cur.execute(f"SELECT hashPass from USERS WHERE username = '{user}'")
			
			try:
				if h_passw == next(x)[0]:
					return True
					
			except StopIteration:
					return False
		
		return False

	def add_trip(self, data):

		highest_index = self.cur.execute("SELECT MAX(tripID) FROM TRIPS")

		try:
			highest_index = next(highest_index)[0]
			if type(highest_index) != int:
				raise StopIteration
			next_index = highest_index + 1

		except StopIteration:
			next_index = 1

		self.cur.execute(f"INSERT INTO TRIPS VALUES(?,?,?,?,?,?)", (next_index, data[0], data[1], data[2], data[3], data[4]))
		self.conn.commit()

		
	def _connect_to_db(self):
		self.conn = sql.connect("exampledb.db")
		self.cur = self.conn.cursor()

	def _close_conn(self):
		self.conn.close()