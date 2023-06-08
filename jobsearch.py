"""This file contains all functions relating to the Job Search option for logged in users"""

import sqlite3 as sql
import utility
import account

currUser = None
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
                  )""")
  userData.commit()
except:
  pass

def SetCurrUser(username):
  global currUser
  currUser = username
  return
  
# Checks if word has special key characters that may affect SQLite
def HasSpecialChar(word):
	specialCharacters = ['#', ';', '\\', '`']
	for character in word:
		if character in specialCharacters:
			return True
	return False

# function that recursively asks to confirm until 'y' or 'n' is typed
def ConfirmDetails():
  confirm = input("Confirm detail? (y or n): ")
  if confirm != 'y' or confirm != 'n':
    utility.printMessage("'y' or 'n' only.")
    ConfirmDetails()
  else:
    return confirm
  return
  
# Customized input for title (PostJob)
def TitleInput():
  global cancelPost
  
  cTitle = input("Title of Job (type 'c' to cancel): ")
  if (cTitle == 'c'):
    cancelPost = True
    return

  if HasSpecialChar(cTitle):
    utility.printMessage("Special characters are not allowed!")
    TitleInput()
  elif len(cTitle) > 100:
    utility.printMessage("Title is too long! Try again.")
    TitleInput()

  print(f"Given title: {cTitle}")
  confirmation = ConfirmDetails()

  if confirmation == 'y':
    return cTitle
  elif confirmation == 'n':
    TitleInput()
  return

# Customized input for description (PostJob)
def DescInput():
  global cancelPost
  
  cDesc = input("Description of Job (type 'c' to cancel posting): ")
  if (cDesc == 'c'):
    cancelPost = True
    return

  if HasSpecialChar(cDesc):
    utility.printMessage("Special characters are not allowed!")
    DescInput()

  print(f"Given description: {cDesc}")
  confirmation = ConfirmDetails()

  if confirmation == 'y':
    return cDesc
  elif confirmation == 'n':
    TitleInput()
  return

# Customized input for employer name (PostJob)
def EmpInput():
  global cancelPost
  
  cEmployer = input("Employer for Job (type 'c' to cancel posting): ")
  if (cEmployer == 'c'):
    cancelPost = True
    return

  if account.hasSpecialCharacter(cEmployer):
    utility.printMessage("Special characters are not allowed!")
    EmpInput()
  elif len(cEmployer) > 25:
    utility.printMessage("Employer name is too long! Try again.")
    EmpInput()

  print(f"Given employer name: {cEmployer}")
  confirmation = ConfirmDetails()

  if confirmation == 'y':
    return cEmployer
  elif confirmation == 'n':
    EmpInput()
  return

# Customized input for location (PostJob)
def LocInput():
  global cancelPost
  
  cLocation = input("Location of Job (type 'c' to cancel posting): ")
  if (cLocation == 'c'):
    cancelPost = True
    return

  if HasSpecialChar(cLocation):
    utility.printMessage("#, ;, \, ` characters are not allowed!")
    LocInput()
  elif len(cLocation) > 255:
    utility.printMessage("Name of Location is too long! Try again.")
    LocInput()

  print(f"Given location: {cLocation}")
  confirmation = ConfirmDetails()

  if confirmation == 'y':
    return cLocation
  elif confirmation == 'n':
    LocInput()
  return
  
# Customized input for salary (PostJob)
def SalInput():
  global cancelPost
  
  cSalary = input("Salary of Job (type 'c' to cancel posting): ")
  if (cSalary == 'c'):
    cancelPost = True
    return

  if not account.hasDigit(cSalary) or account.hasSpecialCharacter(cSalary):
    utility.printMessage("Only positive numbers allowed.")
    SalInput()

  print(f"Given salary: {cSalary}")
  confirmation = ConfirmDetails()

  if confirmation == 'y':
    return cSalary
  elif confirmation == 'n':
    SalInput()
  return

# Allows user to post a job if there is < 5 jobs currently saved
def PostJob():
  global currUser
  
  if (len(UDCursor.execute("SELECT Title FROM jobsData").fetchall()) > 5):
    utility.printMessage("Sorry, max amount of jobs already posted!")
    JobSearchPage()
    return
    
  utility.pageTitle("Post a Job")
  utility.printMessage("Please enter the required details.")

  if cancelPost is False:
    title = TitleInput()
  if cancelPost is False:
    description = DescInput()
  if cancelPost is False:  
    employer = EmpInput()
  if cancelPost is False:
    location = LocInput()
  if cancelPost is False:
    salary = SalInput()
  if cancelPost is True:
    JobSearchPage()

  sqlStatement = """ INSERT INTO 
      jobsData(Issuer, Title, Description, Employer, Location, Salary)
      VALUES(?,?,?,?,?,?) """
  jobInfo = (currUser, title, description, employer, location, salary)
  
  UDCursor.execute(sqlStatement, jobInfo)
  userData.commit()

  utility.printMessage("Job successfully posted!")
  JobSearchPage()
  return

def JobSearchPage():
  global cancelPost
  
  cancelPost = False
  utility.pageTitle("Job Search")

  menuOptions = {
    "Search For Job": utility.construction,
    "Post a Job": PostJob,
  }

  utility.printMenu(menuOptions)
  print("Press 3 for Back.")
  
  choice = input("Input: ")
  if int(choice) == 3:
    return
  else:
    choiceNum = utility.choiceValidation(choice)

  utility.call(choiceNum, menuOptions)
  return