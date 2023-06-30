# this file handles the profile creation and editing

import utility, config
import sqlite3 as sql
import readline

# Connect to SQL database
userData = sql.connect(config.database)
UDCursor = userData.cursor()

# check if the table exists and if not create it
try:
  UDCursor.execute('''CREATE TABLE IF NOT EXISTS Profiles(
                             User TEXT,
                             Title VARCHAR(25), 
                             University TEXT,
                             Major TEXT,
                             About TEXT,
                             Published INT
                            )''')
  
  UDCursor.execute('''CREATE TABLE IF NOT EXISTS Experiences(
                              User TEXT, 
                              Title VARCHAR(25),
                              Employer TEXT,
                              Date_started DATE,
                              Date_ended DATE,
                              Location TEXT,
                              Description TEXT
                              )''')

except:
  pass

# this function modifies the input function to start with some text that can be modified by the user
def PrefillInput(prompt, text):
    def hook():
        readline.insert_text(text)
        readline.redisplay()
    readline.set_pre_input_hook(hook)
    result = input(prompt)
    readline.set_pre_input_hook()
    return result

# this function is the same as the one in utility just with a parameter to dynamically change the confirmation message
def confirmDetails(prompt):
  while True:
    confirm = input(prompt)
    if confirm == "y" or confirm == "n":
      break
    else:
      utility.printMessage("'y' or 'n' only.")
      print("\n")
      continue
  return confirm

# this function returns a specific column of data from the profiles table
def getColumn(column):
  return UDCursor.execute(f"SELECT {column} FROM Profiles WHERE User = '{config.currUser}'").fetchone()[0]

# this function handles the My Profile page option
def MyProfile():
  while True:
    utility.pageTitle("Manage Your Profile")

    publishText = "Publish"

    if getColumn("Published") == 1:
      publishText = "Unpublish"

    options = {
      "Create/Edit My Profile": ManageProfile,
      "View My Profile": ViewProfile,
      f"{publishText} My Profile": PublishProfile
    }

    utility.printMenu(options)
    print(f"Press {len(options)+1} for Back.")

    option = input("Input: ")
    optionNum = utility.choiceValidation(option, options)

    if optionNum == len(options) + 1:
      utility.clearConsole()
      break
    else:
      utility.call(optionNum, options)
  return

# this function verifies that the inputted profile title fits the criteria
def VerifyProfileTitle(profileTitle):
  if utility.hasSpecialCharacter(profileTitle):
    utility.printMessage("Your profile title cannot contain any special characters.")
    print("\n")
    return 0
  elif len(profileTitle) > 25:
    utility.printMessage("Your profile title cannot be longer than 25 characters.")
    print("\n")
    return 0
  elif len(profileTitle) < 5:
    utility.printMessage("Your profile title must be longer")
    print("\n")
    return 0
  return 1

# this handles the create/edit profile options
def ManageProfile():
  while True:
    utility.pageTitle("Create/Edit Your Profile")
    utility.printMessage("Your progress can be saved on any incomplete section")
    titleText = "Edit"
    aboutText = "Edit"

    # if the user does not have any title, change text to create in menu
    if getColumn("Title") == None:
      titleText = "Create"

    # if the user does not have any about section, change text to create in menu
    if getColumn("About") == None:
      aboutText = "Create"

    options = {
      f"{titleText} Your Profile Title": ManageTitle,
      "Edit Your University": ManageUniversity,
      "Edit Your Major": ManageMajor,
      f"{aboutText} Your About me": ManageAbout,
    }

    utility.printMenu(options)
    print(f"Press {len(options)+1} for Back.")

    option = input("Input: ")
    optionNum = utility.choiceValidation(option, options)

    if optionNum == len(options) + 1:
      utility.clearConsole()
      break
    else:
      utility.call(optionNum, options)
  return

# this function contains the logic to give users ability to create or edit existing content in their profile based on the type (Title, About, etc. )
def ManageColumnData(type):
  if getColumn(type) == None:
    utility.pageTitle(f"Create Your {type}")
    profileData = input(f"Enter a profile {type}: ")

    if type == "Title":
      while not VerifyProfileTitle(profileData):
        profileData = input(f"Enter a profile {type}: ")
    
    option = confirmDetails(f"\nSave this {type}? (y/n): ")
    if option == "y":
      UDCursor.execute(f'''UPDATE Profiles
                        SET {type} = '{profileData}'
                        WHERE User = '{config.currUser}'
                        ''')
      userData.commit()
  
  else:
    utility.pageTitle(f"Edit Your {type}")
    curData = getColumn(type)
    utility.printMessage(f"Your current {type}: {curData}")
    utility.printSeparator()
    option = confirmDetails("Would you like to edit? (y/n): ")
    utility.printSeparator()
    if(option == "y"):
      utility.clearConsole()
      utility.pageTitle(f"Edit Your {type}")
      if type == "University" or type == "Major":
        newData = PrefillInput(f"Edit your {type}: ", curData).title()

      elif type == "Title":
        newData = PrefillInput(f"Edit your {type}: ", curData)
        while not VerifyProfileTitle(newData):
          newData = PrefillInput(f"Edit your {type}: ", curData)

      else:
        newData = PrefillInput(f"Edit your {type}: ", curData)
      utility.clearConsole()
      utility.pageTitle(f"Edit Your {type}")
      print("\n")
      utility.printMessage(f"Your new {type}: {newData}")
      utility.printSeparator()
      
      confirm = confirmDetails("\nSave this edit? (y/n): ")
      if confirm == "y":
        UDCursor.execute(f'''UPDATE Profiles
                          SET {type} = '{newData}'
                          WHERE User = '{config.currUser}'
                          ''')
        userData.commit()

# this function will allow a user to create a new title or edit an existing one
def ManageTitle():
  ManageColumnData("Title")
    
# this function allows a user to edit an already exising univeristy
def ManageUniversity():
  ManageColumnData("University")

# this function allows a user to edit an already exising univeristy
def ManageMajor():
  ManageColumnData("Major")

# this function allows a user to create or edit an about section
def ManageAbout():
  ManageColumnData("About")

def ManageExperiences():
  pass

# this function will allow a user to publish their profile so it can be viewed by friends of the user
def PublishProfile():
  if getColumn("Title") == None:
    utility.printMessage("You cannot publish your profile without a title.")
    utility.quickGoBack()

# this function will allow a user to view their current profile
def ViewProfile():
  pass