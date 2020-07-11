import dbconn, user, tracker, time

def create_username(dbConn):
	username = input("Create a username: ")

	if not validate_new_username(dbConn, username):
		print("Username taken. Try another one.")
		return create_username(dbConn)

	return username

def validate_new_username(dbConn, username=None):

	if username == None:
		username = input("Type in your username: ")

	return not dbConn.user_exists(username)

def create_pass():
	passw = input("""Create a Password that:

        Has at least one number,
        Has at least one uppercase and one lowercase character,
        Has at least one special symbol, and
        Is between 6 to 20 characters long.

""")
	if not user.validate_new_pass(passw):
		print("Password didn't work, try again")
		return get_new_pass()
	
	return user.hash_pass(passw)

def get_user_type():
	user_type = input("New user? [Y/N]: ").upper()

	if user_type not in ["Y", "N"]:
		return get_user_type()

	return user_type

def make_new_user(dbConn):
	username = create_username(dbConn)
	passw = create_pass()

	dbConn.add_user(username, passw)

	return dbConn

def log_in(dbConn):

	print("LOG IN")

	username = input("Enter Username: ")
	passw = input("Enter Password: ")

	if not dbConn.validate_user(username, user.hash_pass(passw)):
		print("Credentials not found, please try again.")
		return log_in(dbConn)

	print(f"Welcome, {username}")
	return username, passw

def start():
	dbConn = dbconn.DBConn()

	user_type = get_user_type()

	if user_type == "Y":
		dbConn = make_new_user(dbConn)

	username, passw = log_in(dbConn)

	print("\nStarting to track, when you are done, press esc on the keyboard.")

	time.sleep(5)

	data = tracker.track()

	dbConn.add_trip([username] + data)

if __name__ == '__main__':
	start()