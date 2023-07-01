# this file handles the profile creation and editing

import utility, config
import sqlite3 as sql
import readline, re

# Connect to SQL database
userData = sql.connect(config.database)
UDCursor = userData.cursor()

# check if the table exists and if not create it
try:
  UDCursor.execute('''CREATE TABLE IF NOT EXISTS Profiles(
                             User TEXT,
                             Title VARCHAR(50), 
                             University TEXT,
                             Major TEXT,
                             years_attended TEXT,
                             About TEXT,
                             Published INT, UNIQUE (User)
                            )''')

  UDCursor.execute('''CREATE TABLE IF NOT EXISTS Experiences(
                              e_id integer primary key autoincrement,
                              User TEXT, 
                              Title VARCHAR(50),
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


# returns the number of experiences made by the user
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
  if profileTitle == "c":
    return 1
  if utility.hasSpecialCharacter(profileTitle):
    utility.printMessage(
      "Your profile title cannot contain any special characters.")
    print("\n")
    return 0
  elif len(profileTitle) > 50:
    utility.printMessage(
      "Your profile title cannot be longer than 50 characters.")
    print("\n")
    return 0
  elif len(profileTitle) < 5:
    utility.printMessage("Your profile title must be longer.")
    print("\n")
    return 0
  return 1


def ValidateYearsAttended(yearsAttended):
  if yearsAttended == "c":
    return 1
    
  if not re.search("\d{4}\-\d{4}", yearsAttended):
    utility.printMessage(
      "Invalid input. Make sure your input looks like yyyy-yyyy. ex: 2020-2024"
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


# this function contains the logic to give users ability to create or edit existing content in their profile based on the type (Title, About, etc. )
def ManageColumnData(type):
  curData = getColumn(type)

  if curData == None:

    if type == "years_attended":
      utility.pageTitle("Add your years Attended")
      profileData = input(
        "Enter your years attended as yyyy-yyyy. ex: 2020-2024: ")
    else:
      utility.pageTitle(f"Create Your {type}")
      profileData = input(f"Enter a profile {type}: ")

    if type == "Title":
      while not VerifyProfileTitle(profileData):
        profileData = input(f"Enter a profile {type}: ")

    elif type == "years_attended":
      while not ValidateYearsAttended(profileData):
        profileData = input("Enter your years attended as yyyy-yyyy: ")

    if profileData.lower() == "c":
      return

    if type == "years_attended":
      option = confirmDetails("\nSave your years attended? (y/n): ")
    else:
      option = confirmDetails(f"\nSave this {type}? (y/n): ")

    if option == "y":
      UDCursor.execute(f'''UPDATE Profiles
                        SET {type} = '{profileData}'
                        WHERE User = '{config.currUser}'
                        ''')
      userData.commit()

  else:
    if type == "years_attended":
      type = "years attended"

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
      print("\n")
      utility.printMessage(f"Your new {type}: {newData}")
      utility.printSeparator()

      confirm = confirmDetails("\nSave this edit? (y/n): ")
      if confirm == "y":
        if type == "years attended":
          type = "years_attended"

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


def ManageYearsAttended():
  ManageColumnData("years_attended")


def ManageExperiences():
  while True:
    utility.pageTitle("Manage Your Experiences")
    # adjust menu options based on number of experiences
    if getNumExperiences() < 3 and getNumExperiences() > 0:
      options = {
        "Add an experience": AddExperience,
        "Edit an Experience": EditExperience,
        "Remove an Experience": RemoveExperience
      }

    elif getNumExperiences() == 3:
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


def AddExperience():
  while True:
    # insert the username into Experiences Table
    utility.pageTitle("Add An Experience")
    utility.printMessage("Enter 'c' to leave and save your progress.")
    title = employer = dateStarted = dateEnded = location = description = ""

    title = input("Enter a title for your experience: ")
    if title == "c":
      title = ""
      break

    employer = input("Enter an employer: ")
    if employer == "c":
      employer = ""
      break

    dateStarted = input("Enter Date Started: ")
    if dateStarted == "c":
      dateStarted = ""
      break

    dateEnded = input("Enter Date Ended: ")
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


def ManageExperienceData(e_id, experience_content, type):
  utility.pageTitle(f"Edit the Experience {type}")
  curData = experience_content[type]
  type = type.replace("_", " ")
  utility.printMessage(f"Your current {type}: {curData}")
  choice = confirmDetails(f"Would you like to edit your {type}? (y/n): ")
  if choice == "y":
    newData = PrefillInput(f"Edit your {type}: ", curData)
    utility.clearConsole()
    utility.printMessage(f"Your new {type}: {newData}")
    confirmEdit = confirmDetails("Save this edit? (y/n): ")
    if confirmEdit == "y":
      type = type.replace(" ", "_")
      UDCursor.execute(f'''UPDATE Experiences
                    SET {type} = '{newData}'
                    WHERE User = '{config.currUser}' AND e_id = {e_id}
                    ''')
      userData.commit()


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
      while True:
        utility.clearConsole()
        utility.pageTitle("Edit This Experience")
        
        experience = UDCursor.execute(
          f"SELECT * FROM Experiences WHERE User = '{config.currUser}' AND e_id = {experienceID}"
        ).fetchone()

        experience_content = {
          "Title": experience[2],
          "Employer": experience[3],
          "Date_started": experience[4],
          "Date_ended": experience[5],
          "Location": experience[6],
          "Description": experience[7]
        }
        

        options = {
          "Edit Title": 1,
          "Edit Employer": 2,
          "Edit Date Started": 3,
          "Edit Date Ended": 4,
          "Edit Location": 5,
          "Edit Description": 6
        }
        utility.printMessage(f"You are editing the job titled: '{experience_content['Title']}'")
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
          ManageExperienceData(experienceID, experience_content,
                               "Date_started")
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
