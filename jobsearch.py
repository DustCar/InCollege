"""This file contains all functions relating to the Job Search option for logged in users"""

import sqlite3 as sql
import utility
import config

cancelPost = False

# Connect to SQL database
userData = sql.connect(config.database)
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
except:
  print("Error")
  pass
  
# Checks if word has special key characters that may affect SQLite
def HasSpecialChar(word):
	specialCharacters = ['#', ';', '\\', '`']
	for character in word:
		if character in specialCharacters:
			return True
	return False

# function that recursively asks to confirm until 'y' or 'n' is typed
def ConfirmDetails():
  while True:
    confirm = input("Confirm detail? (y or n): ")
    if confirm == "y" or confirm == "n":
      break
    else:
      utility.printMessage("'y' or 'n' only.")
      continue
  return confirm
  
# Customized input for title (PostJob)
def TitleInput():
  global cancelPost
  if cancelPost is True:
    return
  while True:
    cTitle = input("Title of Job: ")
    if (cTitle == 'c'):
      cancelPost = True
      break
  
    if HasSpecialChar(cTitle):
      utility.printMessage("Special characters are not allowed!")
      continue
    elif len(cTitle) > 50:
      utility.printMessage("Title is too long! Try again.")
      continue
  
    print(f"Given title: {cTitle}")
    confirmation = ConfirmDetails()
  
    if confirmation == 'y':
      return cTitle
    elif confirmation == 'n':
      utility.printSeparator()
      continue
  return

# Customized input for description (PostJob)
def DescInput():
  global cancelPost
  if cancelPost is True:
    return
  while True:
    cDesc = input("Description of Job: ")
    if (cDesc == 'c'):
      cancelPost = True
      break
  
    if HasSpecialChar(cDesc):
      utility.printMessage("Special characters are not allowed!")
      continue
  
    print(f"Given description: {cDesc}")
    confirmation = ConfirmDetails()
  
    if confirmation == 'y':
      return cDesc
    elif confirmation == 'n':
      continue
  return

# Customized input for employer name (PostJob)
def EmpInput():
  global cancelPost
  if cancelPost is True:
    return
  while True:
    cEmployer = input("Employer for Job: ")
    if (cEmployer == 'c'):
      cancelPost = True
      break
  
    if utility.hasSpecialCharacter(cEmployer):
      utility.printMessage("Special characters are not allowed!")
      continue
    elif len(cEmployer) > 25:
      utility.printMessage("Employer name is too long! Try again.")
      continue
  
    print(f"Given employer name: {cEmployer}")
    confirmation = ConfirmDetails()
  
    if confirmation == 'y':
      return cEmployer
    elif confirmation == 'n':
      continue
  return

# Customized input for location (PostJob)
def LocInput():
  global cancelPost
  if cancelPost is True:
    return
  while True:
    cLocation = input("Location of Job: ")
    if (cLocation == 'c'):
      cancelPost = True
      break
  
    if HasSpecialChar(cLocation):
      utility.printMessage("#, ;, \, ` characters are not allowed!")
      continue
    elif len(cLocation) > 255:
      utility.printMessage("Name of Location is too long! Try again.")
      continue
  
    print(f"Given location: {cLocation}")
    confirmation = ConfirmDetails()
  
    if confirmation == 'y':
      return cLocation
    elif confirmation == 'n':
      continue
  return
  
# Customized input for salary (PostJob)
def SalInput():
  global cancelPost
  if cancelPost is True:
    return
  while True:
    cSalary = input("Salary of Job: ")
    if (cSalary == 'c'):
      cancelPost = True
      break
  
    if not utility.hasDigit(cSalary) or utility.hasSpecialCharacter(cSalary):
      utility.printMessage("Only positive numbers allowed.")
      continue
  
    print(f"Given salary: {cSalary}")
    confirmation = ConfirmDetails()
  
    if confirmation == 'y':
      return int(cSalary)
    elif confirmation == 'n':
      continue
  return

# Allows user to post a job if there is < 5 jobs currently saved
def PostJob():
  global cancelPost
  
  if (len(UDCursor.execute("SELECT Title FROM jobsData").fetchall()) >= 5):
    utility.printMessage("Sorry, max amount of jobs already posted!")
    return
    
  utility.pageTitle("Post a Job")
  utility.printMessage("Please enter the required details.")
  utility.printMessage("If at any time you want to cancel the posting, enter 'c'")
  utility.printSeparator()

  # checks for cancel posting after every detail
  title = TitleInput()
  if cancelPost is False:
    utility.printSeparator()

  description = DescInput() 
  if cancelPost is False:
    utility.printSeparator()

  employer = EmpInput()
  if cancelPost is False:
    utility.printSeparator()

  location = LocInput()
  if cancelPost is False:
    utility.printSeparator()

  salary = SalInput()
  
  if cancelPost is True:
    return

  sqlStatement = """ INSERT INTO 
      jobsData(Issuer, Title, Description, Employer, Location, Salary)
      VALUES(?,?,?,?,?,?) """
  jobInfo = (config.currUser, title, description, employer, location, salary)
  
  UDCursor.execute(sqlStatement, jobInfo)
  userData.commit()

  utility.printMessage("Job successfully posted!")
  return

def JobSearchPage():
  global cancelPost
  while True:
    cancelPost = False
    utility.pageTitle("Job Search")
  
    jobsMenuOptions = {
      "Search for Job": utility.construction,
      "Post a Job": PostJob,
    }
  
    utility.printMenu(jobsMenuOptions)
    print(f"Press {len(jobsMenuOptions)+1} for Back.")
    
    choice = input("Input: ")
    if int(choice) == len(jobsMenuOptions)+1:
      break
    else:
      choiceNum = utility.choiceValidation(choice, jobsMenuOptions)
      utility.call(choiceNum, jobsMenuOptions)
  return