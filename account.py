import sqlite3 as sql
import utility
import config

# SQLite database
userData = sql.connect(config.database)
UDCursor = userData.cursor()

# check if the table exists and if not create it
try:
  UDCursor.execute("CREATE TABLE userData(Username, Password, FirstName, LastName)")
except:
  pass


# Create new username and verify it is unique
def usernameCreation():
  """
  new username creation, verifies new username is unique
  """
  username = input("Enter your desired username: ")
  if username == "c":
    return username
  # Checks if username already exists
  for users in UDCursor.execute("SELECT Username FROM userData").fetchall():
    if username == users[0]:
      utility.printMessage(f'The username "{username}" is already in use')
      return usernameCreation()
  return username

# function to enforce password criteria on new password
def passwordCreation():
  """
  Password creation function, calls itself if new user password does not
  meet the requiremnts
  """

  password = input("Enter your desired password: ")
  if password == "c":
    return password

  # Checks if the password fits the character count
  if len(password) > 12:
    utility.printMessage("Password is greater than 12 characters, try removing some characters!")
    return passwordCreation()
  elif len(password) < 8:
    utility.printMessage("Password is less than 8 characters, try adding some more characters!")
    return passwordCreation()

  # Checks for Capital
  if not utility.hasCapitalLetter(password):
    utility.printMessage("Password must include a capital letter, try again")
    return passwordCreation()

  # Checks for digit
  if not utility.hasDigit(password):
    utility.printMessage("Password must include a digit, try again")
    return passwordCreation()

  # Checks for Special character
  if not utility.hasSpecialCharacter(password):
    utility.printMessage("Password must include a special character, try again")
    return passwordCreation()

  # If password meets all requirements, returns password
  return password


def createAccount():
  """
  Creates a new account for the user
  """
  # checks if max number of accounts have been made
  if(len(UDCursor.execute("SELECT Username FROM userData").fetchall()) < 5):
    print("PASSWORD REQUIREMENTS\n----------------------------")
    print("Between 8-12 Characters\nAt least 1 Capital Letter\nAt least 1 Digit\nAt least 1 Special Character")
    print("----------------------------")
    print("Enter 'c' to cancel")
    utility.printSeparator()
    
    username = usernameCreation()
    if username == "c":
      return
    password = passwordCreation()
    if password == "c":
      return
    firstName = input("Enter your first name: ").capitalize()
    lastName = input("Enter your last name: ").capitalize()


    UDCursor.execute(f"""
    INSERT INTO userData VALUES
      ('{username}', '{password}', '{firstName}', '{lastName}')
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
  for users, passwrds in UDCursor.execute("SELECT Username, Password FROM userData").fetchall():
    if username == users and password == passwrds:
      return True
  return False
