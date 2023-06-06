import sqlite3 as sql
import utility

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
			utility.printMessage(f'The username "{username}" is already in use')
			return
	return username

# function to enforce password criteria on new password
def passwordCreation():
	"""
	Password creation function, calls itself if new user password does not
	meet the requiremnts
	"""
	print("PASSWORD REQUIREMENTS\n----------------------------")
	print("Between 8-12 Characters\nAt least 1 Capital Letter\nAt least 1 Digit\nAt least 1 Special   Character")
	print("----------------------------")

	password = input("Enter your desired Password: ")

	# Checks if the password fits the character count
	if len(password) > 12:
		utility.printMessage("Password is greater than 12 characters, try removing some characters!")
		return
	elif len(password) < 8:
		utility.printMessage("Password is less than 8 characters, try adding some more characters!")
		return

	# Checks for Capital
	if not hasCapitalLetter(password):
		utility.printMessage("Password must include a capital letter, try again")
		return

	# Checks for digit
	if not hasDigit(password):
		utility.printMessage("Password must include a digit, try again")
		return

	# Checks for Special character
	if not hasSpecialCharacter(password):
		utility.printMessage("Password must include a special character, try again")
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
		utility.printMessage("Maximum amount of accounts have been made")


def login(username, password):
	"""
	Verify user login information
	"""

	# Username and password verification
  if not userVerification(username, password):
    # Incorrect information
    return True
  return False

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
