import server_communication


def log_in(dbConn):

	print("LOG IN")

	username = input("Enter Username: ")
	passw = input("Enter Password: ")

	if not dbConn.validate_user(username, user.hash_pass(passw)):
		print("Credentials not found, please try again.")
		return log_in(dbConn)

	print(f"Welcome, {username}")
	return username, passw


if __name__ == "__main__":
	start()