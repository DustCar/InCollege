import sqlite3 as sql
import getpass as gp
import utility
import config

# SQLite database
userData = sql.connect(config.database)
UDCursor = userData.cursor()

# check if the table exists and if not create it
try:
  UDCursor.execute(
    "CREATE TABLE userData(Username, Password, FirstName, LastName, EmailFeat, SMSFeat, TargetAdFeat, Language)"
  )
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

  password = gp.getpass(prompt="Enter your desired password: ")
  if password == "c":
    return password

  # Checks if the password fits the character count
  isGoodLength = True
  if len(password) > 12:
    utility.printMessage("Password is greater than 12 characters")
    isGoodLength = False
  elif len(password) < 8:
    utility.printMessage("Password is less than 8 characters")
    isGoodLength = False

  hasCapital = utility.hasCapitalLetter(password)
  hasDigit = utility.hasDigit(password)
  hasSpecialChar = utility.hasSpecialCharacter(password)

  # Checks for Capital
  if not hasCapital:
    utility.printMessage("Password must include a capital letter")
    hasCapital = False

  # Checks for digit
  if not hasDigit:
    utility.printMessage("Password must include a digit")
    hasDigit = False

  # Checks for Special character
  if not hasSpecialChar:
    utility.printMessage("Password must include a special character")
    hasSpecialChar = False

  # If any requirement not met, try again
  if not (isGoodLength and hasCapital and hasDigit and hasSpecialChar):
    return passwordCreation()

  # If password meets all requirements, returns password
  confirmPass = gp.getpass(prompt="Confirm password: ")
  while (confirmPass != password):
    utility.printMessage("Passwords do not match.")
    confirmPass = gp.getpass(prompt="Confirm password: ")
  return confirmPass


# function to ensure unique first,last combo
def name():
  first = input("Enter your first name: ").capitalize()
  if first == "c":
    return [first, "c"]
  last = input("Enter your last name: ").capitalize()
  if last == "c":
    return ["c", last]
  # Checks if first,last pair already exists
  for users in UDCursor.execute(
      "SELECT FirstName,LastName FROM userData").fetchall():
    if first == users[0] and last == users[1]:
      utility.printMessage('The full name is already in use')
      return name()
  # if it doesn't, return name
  return [first, last]


# function to create a user account
def createAccount():
  """
  Creates a new account for the user
  """
  # checks if max number of accounts have been made
  if (len(UDCursor.execute("SELECT Username FROM userData").fetchall()) < 5):
    print("PASSWORD REQUIREMENTS\n----------------------------")
    print(
      "Between 8-12 Characters\nAt least 1 Capital Letter\nAt least 1 Digit\nAt least 1 Special Character"
    )
    print("----------------------------")
    utility.printMessage("To cancel, press 'c' at any time")

    username = usernameCreation()
    if username == "c":
      utility.clearConsole()
      return
    password = passwordCreation()
    if password == "c":
      utility.clearConsole()
      return
    fullName = name()
    firstName = fullName[0]
    lastName = fullName[1]
    if firstName == "c" or lastName == "c":
      utility.clearConsole()
      return

    UDCursor.execute(f"""
    INSERT INTO userData VALUES
      ('{username}', '{password}', '{firstName}', '{lastName}', 'ON', 'ON', 'ON', 'English')
    """)
    userData.commit()
    utility.clearConsole()
  else:
    utility.printMessage("Maximum amount of accounts have been made")
    utility.quickGoBack()


# function for creating an account
def createAcctPage():
  if config.currUser is not None:
    utility.printMessage("You are currently logged in!")
    utility.quickGoBack()
    return
  utility.pageTitle("Create An Account")
  createAccount()
  return


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
  for users, passwrds in UDCursor.execute(
      "SELECT Username, Password FROM userData").fetchall():
    if username == users and password == passwrds:
      return True
  return False


def update_user_language(language):
  query = f"UPDATE userData SET Language = '{language}' WHERE Username = '{config.currUser}'"
  UDCursor.execute(query)
  userData.commit()
  return

def toggleFeature(feature, toggle):
  query = f"UPDATE userData SET {feature} = '{toggle}' WHERE Username = '{config.currUser}'"
  UDCursor.execute(query)
  userData.commit()
  return
