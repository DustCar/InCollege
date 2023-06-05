import maskpass as mp
import sqlite3 as sql

# SQLite database
userData = sql.connect("User_Data_Test.db")
UDCursor = userData.cursor()

# check if the table exists and if not create it
try:
	UDCursor.execute("CREATE TABLE User_Data(Username, Password)")
except:
	pass

# function to check if a string contains a capital letter
def hasCapitalLetter(password):
	"""
	password: attempted new user password

	Checks for capital letters in new user password
	"""
	for character in password:
		if character.isupper():
			return True
	return False

# function to check if a string has a digit
def hasDigit(password):
	"""
	password: attempted new user password

	Checks for digits in new user password
	"""
	for character in password:
		if character.isdigit():
			return True
	return False

#function to check if a string contains a special character
def hasSpecialCharacter(password):
	"""
	password: attempted new user password

	Checks for special characters in new user password
	"""
	specialCharacters = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
	for character in password:
		if character in specialCharacters:
			return True
	return False

# Create new username and verify it is unique
def usernameCreation():
	"""
	new username creation, verifies new username is unique
	"""
	username = input("Enter your desired username: ")

	# Checks if username already exists
	for users in UDCursor.execute("SELECT Username FROM User_Data").fetchall():
		if username == users[0]:
			print(f'The username "{username}" is already in use\n')
			return
	return username

# function to enforce password criteria on new password
def passwordCreation():
	"""
	Password creation function, calls itself if new user password does not
	meet the requiremnts
	"""
	print("PASSWORD REQUIREMENTS\n----------------------------")
	print("Between 8-12 Characters\nAt least 1 Capital Letter\nAt least 1 Digit\nAt least 1 Special Character")
	print("----------------------------")

	password = input("Enter your desired Password: ")

	# Checks if the password fits the character count
	if len(password) > 12:
		print("Password is greater than 12 characters, try removing some characters!\n")
		return
	elif len(password) < 8:
		print("Password is less than 8 characters, try adding some more characters!\n")
		return

	# Checks for Capital
	if not hasCapitalLetter(password):
		print("Password must include a capital letter, try again\n")
		return

	# Checks for digit
	if not hasDigit(password):
		print("Password must include a digit, try again\n")
		return

	# Checks for Special character
	if not hasSpecialCharacter(password):
		print("Password must include a special character, try again\n")
		return

	# If password meets all requirements, returns password
	return password

def createAccount():
	"""
	Creates a new account for the user
	"""
	# checks if max number of accounts have been made
	if(len(UDCursor.execute("SELECT Username FROM User_Data").fetchall()) < 5):
		username = usernameCreation()
		password = passwordCreation()

		UDCursor.execute(f"""
		INSERT INTO User_Data VALUES
			('{username}', '{password}')
		""")
		userData.commit()
	else:
		print("Maximum amount of accounts have been made")


def login():
	"""
	Verify user login information
	"""

	print("USER LOGIN\n----------")

	username = input("USERNAME: ")
	password = input("PASSWORD: ")

	# Username and password verification
	if not userVerification(username, password):
		# Incorrect information
		print("Either Username or Password is incorrect\n")
		return


	# Login information is correct
	print('Login Success!\n')
	return

def userVerification(username, password):
	"""
	username: attempted username associated with attempted password
	password: attempted password

	verifies that inputted username and password both exists and are correct
	"""
	for users, passwrds in UDCursor.execute("SELECT Username, Password FROM User_Data").fetchall():
		if username == users and password == passwrds:
			return True
	return False