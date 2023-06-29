# this file handles the profile creation and editing

import utility, config
import sqlite3 as sql


# Connect to SQL database
userData = sql.connect(config.database)
UDCursor = userData.cursor()

# check if the table exists and if not create it
try:
  UDCursor.execute('''CREATE TABLE IF NOT EXISTS Profiles(
                             User TEXT,
                             University TEXT,
                             Major TEXT,
                             Title VARCHAR(25), 
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

def MyProfile():
  while True:
    utility.pageTitle("Manage Your Profile")

    publishText = "Publish"

    if getColumn("Published") == 1:
      publishText = "Unpublish"

    # menu options within "My Friends"
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

def AskProfileTitle():
  while True:
    profileTitle = input("Enter your profile title: ")

    if utility.hasSpecialCharacter(profileTitle):
      utility.printMessage("Your profile title cannot contain any special characters.")
      continue
    elif len(profileTitle) > 25:
      utility.printMessage("Your profile title cannot be longer than 25 characters.")
      continue
    elif len(profileTitle) < 1:
      utility.printMessage("Your profile title must be longer")
      continue

    break
    
  return profileTitle

def getColumn(column):
  return UDCursor.execute(f"SELECT {column} FROM Profiles WHERE User = '{config.currUser}'").fetchone()[0]

def ManageProfile():
  while True:
    utility.pageTitle("Create/Edit Your Profile")

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

    
    
def ManageTitle():
  utility.pageTitle("Create/Edit Your Title")
  # check if user has a title for their profile
  if getColumn("Title") == None:
    profileTitle = AskProfileTitle()
    
    option = utility.confirmDetails()
    if option == "y":
      UDCursor.execute(f'''UPDATE Profiles
                        SET Title = '{profileTitle}'
                        WHERE User = '{config.currUser}'
                        ''')
      userData.commit()
  
  else:
    curTitle = getColumn("Title")
    utility.printMessage(f"Your current title: {curTitle}")
    option = input("would you like to edit? (y/n): ")
    if(option == "y"):
    
      profileTitle = AskProfileTitle()
      
      confirm = utility.confirmDetails()
      if confirm == "y":
        UDCursor.execute(f'''UPDATE Profiles
                          SET Title = '{profileTitle}'
                          WHERE User = '{config.currUser}'
                          ''')
        userData.commit()
    

def ManageUniversity():
  pass

def ManageMajor():
  pass

def ManageAbout():
  pass

def ViewProfile():
  pass

def PublishProfile():
  if getColumn("Title") == None:
    utility.printMessage("You cannot publish your profile without a title.")
    utility.quickGoBack()

  

  

