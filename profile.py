# this file handles the profile creation and editing

import utility, config
import sqlite3 as sql
try:
  import readline
except ImportError:
  from pyreadline3 import Readline
  readline = Readline()
import re
from datetime import date, datetime

# Connect to SQL database
userData = sql.connect(config.database)
UDCursor = userData.cursor()

# check if the table exists and if not create it
try:
  UDCursor.execute(f'''CREATE TABLE IF NOT EXISTS Profiles(
                             User TEXT,
                             Title VARCHAR({config.maxTitleLen}), 
                             University TEXT,
                             Major TEXT,
                             years_attended TEXT,
                             About TEXT,
                             Published INT, UNIQUE (User)
                            )''')

  UDCursor.execute(f'''CREATE TABLE IF NOT EXISTS Experiences(
                              e_id integer primary key autoincrement,
                              User TEXT, 
                              Title VARCHAR({config.maxTitleLen}),
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
  return UDCursor.execute(
    f"SELECT {column} FROM Profiles WHERE User = '{config.currUser}'"
  ).fetchone()[0]


# returns the total number of experiences made by the user
def getNumExperiences():
  return len(
    UDCursor.execute(
      f"SELECT User FROM Experiences WHERE User = '{config.currUser}'").
    fetchall())


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
  # if the user wants to cancel then exit the function
  if profileTitle == "c":
    return 1
  if utility.hasSpecialCharacter(profileTitle):
    utility.printMessage("Your title cannot contain any special characters.")
    print("\n")
    return 0
  elif len(profileTitle) > config.maxTitleLen:
    utility.printMessage(f"Your title cannot be longer than {config.maxTitleLen} characters.")
    print("\n")
    return 0
  elif len(profileTitle) <= config.minTitleLen:
    utility.printMessage(f"Your title must be longer than {config.minTitleLen} characters.")
    print("\n")
    return 0
  return 1


def ValidateYearsAttended(yearsAttended):
  # if the user wants to cancel then exit the function
  if yearsAttended == "c":
    return 1

  if not re.search(r"\d{4}\-\d{4}", yearsAttended):
    utility.printMessage(
      f"Invalid input. Make sure your input looks like yyyy-yyyy. ex: {date.today().year-4}-{date.today().year}."
    )
    return 0
  return 1


# this handles the create/edit profile options
def ManageProfile():
  while True:
    utility.pageTitle("Create/Edit Your Profile")
    utility.printMessage(
      "Your progress can be saved on any incomplete section")
    titleText = "Edit"
    aboutText = "Edit"
    yearsAttendedText = "Edit"

    # if the user does not have any title, change text to create in menu
    if getColumn("Title") == None:
      titleText = "Create"

    # if the user does not have any about section, change text to create in menu
    if getColumn("About") == None:
      aboutText = "Create"

    if getColumn("years_attended") == None:
      yearsAttendedText = "Add"

    options = {
      f"{titleText} Your Profile Title": ManageTitle,
      "Edit Your University": ManageUniversity,
      "Edit Your Major": ManageMajor,
      f"{yearsAttendedText} Your Years Attended": ManageYearsAttended,
      f"{aboutText} Your About me": ManageAbout,
      "Manage Experiences": ManageExperiences
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


#this function will update the specified column in the profiles table with the data
def UpdateProfileData(profileData, type):
  type = type.replace(" ", "_")
  UDCursor.execute(f'''UPDATE Profiles
                        SET {type} = '{profileData}'
                        WHERE User = '{config.currUser}'
                        ''')
  userData.commit()


# this function contains the logic to give users ability to create or edit existing content in their profile based on the type (Title, About, etc. )
def ManageColumnData(type):
  curData = getColumn(type)

  if curData == None:

    if type == "years_attended":
      utility.pageTitle("Add Your Years Attended")
      profileData = input(
        f"Enter your years attended as yyyy-yyyy. ex: {date.today().year-4}-{date.today().year}: "
      )
    else:
      utility.pageTitle(f"Create Your {type}")
      profileData = input(f"Enter a profile {type}: ")

    if type == "Title":
      while not VerifyProfileTitle(profileData):
        profileData = input(f"Enter a profile {type}: ")

    elif type == "years_attended":
      while not ValidateYearsAttended(profileData):
        profileData = input(
          f"Enter your years attended as yyyy-yyyy. ex. {date.today().year-4}-{date.today().year}: "
        )

    if profileData.lower() == "c":
      return

    if type == "years_attended":
      option = confirmDetails("\nSave your years attended? (y/n): ")
    else:
      option = confirmDetails(f"\nSave this {type}? (y/n): ")

    if option == "y":
      UpdateProfileData(profileData, type)

  else:
    type = type.replace("_", " ")
    utility.pageTitle(f"Edit Your {type}")
    utility.printMessage(f"Your current {type}: {curData}")
    utility.printSeparator()
    option = confirmDetails("Would you like to edit? (y/n): ")
    utility.printSeparator()
    if (option == "y"):
      utility.clearConsole()
      utility.pageTitle(f"Edit Your {type}")

      if type == "University" or type == "Major":
        newData = PrefillInput(f"Edit your {type}: ", curData).title()

      elif type == "Title":
        newData = PrefillInput(f"Edit your {type}: ", curData)
        while not VerifyProfileTitle(newData):
          newData = PrefillInput(f"Edit your {type}: ", curData)

      elif type == "years attended":
        newData = PrefillInput(f"Edit your {type}: ", curData)
        while not ValidateYearsAttended(newData):
          newData = PrefillInput(f"Edit your {type}: ", curData)

      else:
        newData = PrefillInput(f"Edit your {type}: ", curData)

      if newData.lower() == "c":
        return

      utility.clearConsole()
      utility.pageTitle(f"Edit Your {type}")
      utility.printMessage(f"Your new {type}: {newData}")
      utility.printSeparator()

      confirm = confirmDetails("\nSave this edit? (y/n): ")
      if confirm == "y":
        UpdateProfileData(newData, type)


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


def ManageYearsAttended():
  ManageColumnData("years_attended")


# this function provides the menu options to add, edit, and remove experiences
def ManageExperiences():
  while True:
    utility.pageTitle("Manage Your Experiences")
    # adjust menu options based on number of experiences
    if getNumExperiences() < config.maxExperiences and getNumExperiences() > 0:
      options = {
        "Add an experience": AddExperience,
        "Edit an Experience": EditExperience,
        "Remove an Experience": RemoveExperience
      }

    elif getNumExperiences() == config.maxExperiences:
      options = {
        "Edit an Experience": EditExperience,
        "Remove an Experience": RemoveExperience
      }

    else:
      options = {
        "Add an experience": AddExperience,
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


def VerifyExperienceDate(userinput):
  # if the user wants to cancel then exit the function
  if userinput == "c":
    return 1

  try:
    datetime.strptime(userinput, '%m-%d-%Y')
    return 1
  except ValueError:
    utility.printMessage(
      f"Enter the date as (mm-dd-yyyy) ex. {date.today().strftime('%m-%d-%Y')}"
    )
    return 0


# this function will allow a user to add a new experience
def AddExperience():
  while True:
    # insert the username into Experiences Table
    utility.pageTitle("Add An Experience")
    utility.printMessage("Enter 'c' to leave and save your progress.")
    title = employer = dateStarted = dateEnded = location = description = ""

    title = input("Enter a title for your experience: ")
    while not VerifyProfileTitle(title):
      title = input("Enter a title for your experience: ")

    if title == "c":
      title = ""
      break

    employer = input("Enter an employer: ")
    if employer == "c":
      employer = ""
      break

    dateStarted = input(
      f"Enter Date Started as (mm-dd-yyyy) ex. {date.today().strftime('%m-%d-%Y')}: "
    )
    while not VerifyExperienceDate(dateStarted):
      dateStarted = input(
        f"Enter Date Started as (mm-dd-yyyy) ex. {date.today().strftime('%m-%d-%Y')}: "
      )

    if dateStarted == "c":
      dateStarted = ""
      break

    dateEnded = input(
      f"Enter Date Ended as (mm-dd-yyyy) ex. {date.today().strftime('%m-%d-%Y')}: "
    )
    while not VerifyExperienceDate(dateEnded):
      dateEnded = input(
        f"Enter Date Ended as (mm-dd-yyyy) ex. {date.today().strftime('%m-%d-%Y')}: "
      )

    if dateEnded == "c":
      dateEnded = ""
      break

    location = input("Enter a location: ")
    if location == "c":
      location = ""
      break

    description = input("Enter a description: ")
    if description == "c":
      description = ""
      break
    break

  UDCursor.execute(f"""
    INSERT INTO Experiences (User, Title, Employer, Date_started, Date_ended, Location, Description)
    VALUES ('{config.currUser}', '{title}', '{employer}', '{dateStarted}', '{dateEnded}', '{location}', '{description}')
    """)
  userData.commit()


# this will allow users to remove their current experiences
def RemoveExperience():
  utility.pageTitle("Remove An Experience")
  experiences = UDCursor.execute(
    f"SELECT e_id, Title FROM Experiences WHERE User = '{config.currUser}'"
  ).fetchall()

  for i, experience in enumerate(experiences):
    print(f"Press {i+1} to delete experience titled: '{experience[1]}'")

  print(f"Press {len(experiences)+1} to go back")

  option = input("Input: ")
  optionNum = utility.choiceValidation(option, experiences)

  if optionNum == len(experiences) + 1:
    utility.clearConsole()
    return
  else:
    option = confirmDetails(
      "Are you sure you want to delete this experience? (y/n): ")

    if option == "y":
      UDCursor.execute(
        f"DELETE FROM Experiences WHERE User = '{config.currUser}' AND e_id = '{experiences[optionNum-1][0]}'"
      )
      userData.commit()
      utility.printMessage("This experience has been deleted.")
      utility.quickGoBack()


# this will update the specified column in the specific experience row specified by the e_id and the type
def UpdateExperienceData(e_id, newData, type):
  type = type.replace(" ", "_")
  UDCursor.execute(f'''UPDATE Experiences
                SET {type} = '{newData}'
                WHERE User = '{config.currUser}' AND e_id = {e_id}
                ''')
  userData.commit()


# this function is similar to ManageColumnData in that it gets the current experience data for a column and prompts the user to edit or create new data for that column
def ManageExperienceData(e_id, experience_content, type):
  curData = experience_content[type]
  type = type.replace("_", " ")
  # if the content is empty prompt the user to add new content
  if curData == "":
    utility.pageTitle(f"Add the {type}")
    utility.printMessage("Press 'c' to cancel anytime.")
    newData = input(f"Add your {type}: ")

    if type == "Title":
      while not VerifyProfileTitle(newData):
        newData = input(f"Add your {type}: ")

    elif type == "Date started" or type == "Date ended":
      while not VerifyExperienceDate(newData):
        newData = input(f"Add your {type}: ")

    if newData.lower() == "c":
      return

    choice = confirmDetails("Save this change? (y/n): ")
    if choice == "y":
      UpdateExperienceData(e_id, newData, type)

  else:
    utility.pageTitle(f"Edit the {type}")
    utility.printMessage(f"Your current {type}: {curData}")
    choice = confirmDetails(f"Would you like to edit your {type}? (y/n): ")
    if choice == "y":
      utility.printMessage("Press 'c' to cancel anytime.")
      newData = PrefillInput(f"Edit your {type}: ", curData)
      if type == "Title":
        while not VerifyProfileTitle(newData):
          newData = PrefillInput(f"Edit your {type}: ", curData)

      elif type == "Date started" or type == "Date ended":
        while not VerifyExperienceDate(newData):
          newData = PrefillInput(f"Edit your {type}: ", curData)

      if newData.lower() == "c":
        return

      utility.clearConsole()
      utility.printMessage(f"Your new {type}: {newData}")
      confirmEdit = confirmDetails("Save this edit? (y/n): ")
      if confirmEdit == "y":
        UpdateExperienceData(e_id, newData, type)


# this is the edit experience page which lists all of the experiences started by a user that they can select to edit
def EditExperience():
  while True:
    utility.pageTitle("Edit An Experience")
    experiences = UDCursor.execute(
      f"SELECT e_id, Title FROM Experiences WHERE User = '{config.currUser}'"
    ).fetchall()

    for i, experience in enumerate(experiences):
      print(f"Press {i+1} to edit experience titled: '{experience[1]}'")

    print(f"Press {len(experiences)+1} to go back")

    option = input("Input: ")
    optionNum = utility.choiceValidation(option, experiences)

    if optionNum == len(experiences) + 1:
      utility.clearConsole()
      break
    else:
      # get the experience id selected by the user
      experienceID = experiences[optionNum - 1][0]
      EditSpecificExperiencePage(experienceID)


def EditSpecificExperiencePage(experienceID):
  while True:
    utility.clearConsole()
    utility.pageTitle("Edit This Experience")

    experience = UDCursor.execute(
      f"SELECT * FROM Experiences WHERE User = '{config.currUser}' AND e_id = {experienceID}"
    ).fetchone()

    # store experience content retrieved from db into this dictionary
    experience_content = {
      "Title": experience[2],
      "Employer": experience[3],
      "Date_started": experience[4],
      "Date_ended": experience[5],
      "Location": experience[6],
      "Description": experience[7]
    }

    titleText = "Edit"
    if experience_content["Title"] == "":
      titleText = "Add"
    employerText = "Edit"
    if experience_content["Employer"] == "":
      employerText = "Add"
    dateStartedText = "Edit"
    if experience_content["Date_started"] == "":
      dateStartedText = "Add"
    dateEndedText = "Edit"
    if experience_content["Date_ended"] == "":
      dateEndedText = "Add"
    locationText = "Edit"
    if experience_content["Location"] == "":
      locationText = "Add"
    descriptionText = "Edit"
    if experience_content["Description"] == "":
      descriptionText = "Add"

    # menu options that is displayed to the user
    options = {
      f"{titleText} Title": 1,
      f"{employerText} Employer": 2,
      f"{dateStartedText} Date Started": 3,
      f"{dateEndedText} Date Ended": 4,
      f"{locationText} Location": 5,
      f"{descriptionText} Description": 6
    }

    utility.printMessage(
      f"You are editing the job titled: '{experience_content['Title']}'")
    utility.printSeparator()
    utility.printMenu(options)
    print(f"Press {len(options)+1} to go back.")
    utility.printSeparator()

    option = input("Input: ")
    optionNum = utility.choiceValidation(option, experience_content)
    utility.clearConsole()

    if optionNum == len(experience_content) + 1:
      break
    elif optionNum == 1:
      ManageExperienceData(experienceID, experience_content, "Title")
    elif optionNum == 2:
      ManageExperienceData(experienceID, experience_content, "Employer")
    elif optionNum == 3:
      ManageExperienceData(experienceID, experience_content, "Date_started")
    elif optionNum == 4:
      ManageExperienceData(experienceID, experience_content, "Date_ended")
    elif optionNum == 5:
      ManageExperienceData(experienceID, experience_content, "Location")
    elif optionNum == 6:
      ManageExperienceData(experienceID, experience_content, "Description")


# this function will allow a user to publish their profile so it can be viewed by friends of the user
def PublishProfile():
  published = getColumn("Published")
  if published == 1:
    utility.pageTitle("Unpublish Your Profile")
    utility.printMessage("Unpublish your profile to hide it")
  else:
    utility.pageTitle("Publish your profile")
    utility.printMessage(
      "Publish your profile to make it visible to your friends")
  utility.printSeparator()

  if getColumn("Title") == None:
    utility.printMessage("You cannot publish your profile without a title.")
    utility.quickGoBack()
  else:
    if published == 1:
      choice = confirmDetails("Would you like to Unpublish? (y/n): ")
    else:
      choice = confirmDetails("Would you like to Publish? (y/n): ")

    if choice == "y":
      # XOR published with 1 to invert value
      published = published ^ 1

      UDCursor.execute(f'''UPDATE Profiles
                            SET Published = {published}
                            WHERE User = '{config.currUser}'
                            ''')
      if published == 0:
        utility.printMessage("You have unpublished your profile.")
      else:
        utility.printMessage("You have published your profile.")

      utility.quickGoBack()


# this function will allow a user to view their current profile
def ViewProfile():
  pass
