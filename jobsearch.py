import sqlite3 as sql
import utility
import main
import account

user = main.currUser
cancelPost = False

# Connect to SQL database
userData = sql.connect("User_Data.db")
UDCursor = userData.cursor()

# Create table for jobs if table does not exist
try:
  UDCursor.execute("""
                    CREATE TABLE IF NOT EXISTS jobsData (
                    Issuer VARCHAR(25), 
                    Title VARCHAR(100), 
                    Description TEXT, 
                    Employer VARCHAR(25), 
                    Location VARCHAR(255), 
                    Salary INT
                  );""")
  UDCursor.commit()
except:
  pass

# Checks if word has special key characters that may affect SQLite
def hasSpecialChar(word):
	specialCharacters = ['#', ';', '\\', '`']
	for character in word:
		if character in specialCharacters:
			return True
	return False

def confirmDetails():
  confirm = input("Confirm detail? (y or n): ")
  if confirm != 'y' or confirm != 'n':
    utility.printMessage("'y' or 'n' only.")
    confirmDetails()
  else:
    return confirm
  return
  
# Customized input for title (PostJob)
def titleInput():
  global cancelPost
  cTitle = input("Title of Job (type 'c' to cancel): ")
  if (cTitle == 'c'):
    cancelPost = True
    return

  if hasSpecialChar(cTitle):
    utility.printMessage("Special characters are not allowed!")
    titleInput()
  elif len(cTitle) > 100:
    utility.printMessage("Title is too long! Try again.")
    titleInput()

  print(f"Given title: {cTitle}")
  confirmation = confirmDetails()

  if confirmation == 'y':
    return cTitle
  elif confirmation == 'n':
    titleInput()
  return

# Customized input for description (PostJob)
def descInput():
  global cancelPost
  cDesc = input("Description of Job (type 'c' to cancel posting): ")
  if (cDesc == 'c'):
    cancelPost = True
    return

  if hasSpecialChar(cDesc):
    utility.printMessage("Special characters are not allowed!")
    descInput()

  print(f"Given description: {cDesc}")
  confirmation = confirmDetails()

  if confirmation == 'y':
    return cDesc
  elif confirmation == 'n':
    titleInput()
  return

# Customized input for employer name (PostJob)
def empInput():
  global cancelPost
  cEmployer = input("Employer for Job (type 'c' to cancel posting): ")
  if (cEmployer == 'c'):
    cancelPost = True
    return

  if account.hasSpecialCharacter(cEmployer):
    utility.printMessage("Special characters are not allowed!")
    empInput()
  elif len(cEmployer) > 25:
    utility.printMessage("Employer name is too long! Try again.")
    empInput()

  print(f"Given employer name: {cEmployer}")
  confirmation = confirmDetails()

  if confirmation == 'y':
    return cEmployer
  elif confirmation == 'n':
    empInput()
  return

# Customized input for location (PostJob)
def locInput():
  global cancelPost
  cLocation = input("Location of Job (type 'c' to cancel posting): ")
  if (cLocation == 'c'):
    cancelPost = True
    return

  if hasSpecialChar(cLocation):
    utility.printMessage("#, ;, \, ` characters are not allowed!")
    locInput()
  elif len(cLocation) > 255:
    utility.printMessage("Name of Location is too long! Try again.")
    locInput()

  print(f"Given location: {cLocation}")
  confirmation = confirmDetails()

  if confirmation == 'y':
    return cLocation
  elif confirmation == 'n':
    locInput()
  return
  
# Customized input for salary (PostJob)
def salInput():
  global cancelPost
  cSalary = input("Salary of Job (type 'c' to cancel posting): ")
  if (cSalary == 'c'):
    cancelPost = True
    return

  if not account.hasDigit(cSalary) or account.hasSpecialCharacter(cSalary):
    utility.printMessage("Only positive numbers allowed.")
    salInput()

  print(f"Given salary: {cSalary}")
  confirmation = confirmDetails()

  if confirmation == 'y':
    return cSalary
  elif confirmation == 'n':
    salInput()
  return

# Allows user to post a job if there is < 5 jobs currently saved
def PostJob():
  if (len(UDCursor.execute("SELECT Title FROM jobsData;")) > 5):
    utility.printMessage("Sorry, max amount of jobs already posted!")
    JobSearchPage()
    return
    
  utility.pageTitle("Post a Job")
  utility.printMessage("Please enter the required details.")

  if cancelPost is False:
    title = titleInput()
    description = descInput()
    employer = empInput()
    location = locInput()
    salary = salInput()
  else:
    JobSearchPage()

  
  return

# Page holding all options dealing with Job Searching
def JobSearchPage():
  global cancelPost
  cancelPost = False
  utility.pageTitle("Job Search")

  menuOptions = {
    "Search For Job": utility.construction,
    "Post a Job": PostJob,
    "Back": utility.construction,
  }

  utility.printMenu(menuOptions)

  choice = input("Input: ")
  choiceNum = utility.choiceValidation(choice)

  utility.call(choiceNum, menuOptions)
  return