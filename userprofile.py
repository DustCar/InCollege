# this file handles the profile creation and editing

import utility, config
import sqlite3 as sql
import account
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

  UDCursor.execute('''CREATE TABLE IF NOT EXISTS Educations(
                              edu_id integer primary key autoincrement,
                              User TEXT,
                              school TEXT,
                              degree TEXT,
                              years_attended TEXT)''')

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
      utility.printSeparator()
      continue
  return confirm


# this function returns a specific column of data from the profiles table
def getColumn(column):
  return UDCursor.execute(
    f"SELECT {column} FROM Profiles WHERE User = '{config.currUser}'"
  ).fetchone()[0]

# this function returns a specific column of data from the profiles table
def is_published(user):
  return UDCursor.execute(
    f"SELECT Published FROM Profiles WHERE User = '{user}'"
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
    # automatically unpublish profile if student does not meet all criteria
    if getColumn("Published") == 1:
      numEducation = len(UDCursor.execute(f"SELECT User FROM Educations WHERE User = '{config.currUser}'").fetchall())
      if getColumn("Title") == None or getColumn("About") == None or numEducation == 0:
        published = 0
        UDCursor.execute(f'''UPDATE Profiles
                            SET Published = {published}
                            WHERE User = '{config.currUser}'
                            ''')
        userData.commit()
    
    utility.pageTitle("Manage Your Profile")

    publishText = "Publish"

    if getColumn("Published") == 1:
      publishText = "Unpublish"

    options = {
      "Create/Edit My Profile": ManageProfile,
      "View My Profile": ViewProfileUser,
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
  profileTitle = profileTitle.strip()
  if profileTitle == "c":
    return 1
  if utility.hasSpecialCharacter(profileTitle):
    utility.printMessage("Your title cannot contain any special characters.")
    utility.printSeparator()
    return 0
  elif len(profileTitle) > config.maxTitleLen:
    utility.printMessage(
      f"Your title cannot be longer than {config.maxTitleLen} characters.")
    utility.printSeparator()
    return 0
  elif len(profileTitle) <= config.minTitleLen:
    utility.printMessage(
      f"Your title must be longer than {config.minTitleLen} characters.")
    utility.printSeparator()
    return 0
  return 1


def ValidateYearsAttended(yearsAttended):
  # if the user wants to cancel then exit the function
  yearsAttended = yearsAttended.strip()
  if yearsAttended == "c":
    return 1

  if not re.search(r"^\d{4}-{1}\d{4}$", yearsAttended):
    utility.printMessage(
      f"Invalid input. Make sure your input looks like yyyy-yyyy. ex: {date.today().year-4}-{date.today().year}."
    )
    return 0

  years = [int(i) for i in yearsAttended.split("-")]

  if abs(years[0] - years[1]) > 20:
    utility.printMessage("This date range is too big.")
    return 0

  return 1


def ValidateProfileAbout(about):
  about = about.strip()
  if about == "c":
    return 1

  if len(about) < 10:
    utility.printMessage("Add more characters to your about.")
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
    # if the user does not have any title, change text to create in menu
    if getColumn("Title") == None:
      titleText = "Create"

    # if the user does not have any about section, change text to create in menu
    if getColumn("About") == None:
      aboutText = "Create"

    options = {
      f"{titleText} Your Profile Title": ManageTitle,
      "Edit Current University": ManageUniversity,
      "Edit Current Major": ManageMajor,
      f"{aboutText} Your About me": ManageAbout,
      "Manage Education History": ManageEducationSection,
      "Manage Job Experiences": ManageExperiences
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


def get_education_column(column, education_id):
  result = UDCursor.execute(f"SELECT {column} FROM Educations WHERE User = '{config.currUser}' and edu_id = '{education_id}'").fetchone()

  if result is not None:
    return result[0]
  else:
    return None

# Updates Educations table
def update_education(edu_id, newData, type):
  type = type.replace(" ", "_")
  UDCursor.execute(f'''UPDATE Educations
                SET {type} = '{newData}'
                WHERE User = '{config.currUser}' AND edu_id = {edu_id}
                ''')
  userData.commit()

# degree type (high school, bachelors, masters, phd) (DONE)
def degree_type_entry(edu_id):
  """
  edu_id: the id of the education experience in the table

  alters the type of degree for a saved education experience
  """
  utility.pageTitle('Degree Type Management')
  utility.printMessage(f'Current Degree Type is: {get_education_column("degree", education_id=edu_id)}')
  print('H - High School\nB - Bachelors\nM - Masters\nD - Doctorate\nO - Other')
  degree_type = input('Edit the Type of Degree or "c" to cancel: ')

  # Checks degree type
  if degree_type.lower() == 'c':
    return
  elif degree_type.lower() == 'h':
    degree_type = 'High School Diploma'
  elif degree_type.lower() == 'b':
    degree_type = 'Bachelors Degree'
  elif degree_type.lower() == 'm':
    degree_type = 'Masters Degree'
  elif degree_type.lower() == 'd':
    degree_type = 'Doctorate Degree'
  elif degree_type.lower() == 'o':
    while True:
      degree_type = input('Enter the type of degree or "c" to cancel: ')

      if degree_type.lower() == 'c':
        return
      degree_type = degree_type.title()
      if confirmDetails(f'Do you confirm {degree_type} as the degree type?(y/n): ') == 'y':
        break
      else:
        utility.clearConsole()
        return degree_type_entry(edu_id)
  else:
    utility.clearConsole()
    utility.printMessage(f'"{degree_type}" is an Invalid input')
    return degree_type_entry(edu_id)

  update_education(edu_id=edu_id, newData=degree_type, type='degree')
    
  
# name of the university degree is obtained from (DONE)
def edu_university(edu_id):
  """
  edu_id: the id of the education experience in the table
  """

  utility.pageTitle('University Management')
  utility.printMessage(f'The Current name of the School is: {get_education_column("school", education_id=edu_id)}')
  university_name = input('Edit the name of the School or "c" to cancel: ')

  if university_name.lower() == 'c':
    return
  university_name = university_name.title()
  if confirmDetails(f'Do you confirm "{university_name}" as the name of the school? (y/n): ') == 'y':
    update_education(edu_id=edu_id, newData=university_name, type='school')
  else:
    return edu_university(edu_id)

# name of the university degree is obtained from (DONE)
def years_attended_education(edu_id):
  """
  edu_id: the id of the education experience in the table
  """

  utility.pageTitle('Years Attended Management')
  utility.printMessage(f'The Current years attended: {get_education_column("years_attended", education_id=edu_id)}')
  yearsAttended = input(f"Enter your years attended as yyyy-yyyy. ex: {date.today().year-4}-{date.today().year}: ")

  while not ValidateYearsAttended(yearsAttended):
    yearsAttended = input(f"Enter your years attended as yyyy-yyyy. ex: {date.today().year-4}-{date.today().year}: ")

  if yearsAttended.lower() == "c":
    return

  if confirmDetails(f'Do you confirm your years attended as {yearsAttended}? (y/n): ') == 'y':
    update_education(edu_id=edu_id, newData=yearsAttended, type="years_attended")
  else:
    return edu_university(edu_id)


# Add a new education experience
def add_education():
  """
  Adds a new education experience to the database
  """
  utility.pageTitle('Add Education Experience')

  utility.printMessage("To cancel, enter 'c' at any time")
  
  # Degree type
  print('H - High School\nB - Bachelors\nM - Masters\nD - Doctorate\nO - Other')
  degree_type = input('Enter the Type of Degree: ')

  # Checks degree type
  if degree_type.lower() == 'c':
    return
  elif degree_type.lower() == 'h':
    degree_type = 'High School Diploma'
  elif degree_type.lower() == 'b':
    degree_type = 'Bachelors Degree'
  elif degree_type.lower() == 'm':
    degree_type = 'Masters Degree'
  elif degree_type.lower() == 'd':
    degree_type = 'Doctorate Degree'
  elif degree_type.lower() == 'o':
    while True:
      degree_type = input('Enter the type of degree: ')

      if degree_type.lower() == 'c':
        return
      
      if confirmDetails(f'Do you confirm {degree_type} as the degree type?(y/n): ') == 'y':
        break
      else:
        utility.clearConsole()
        add_education()
  else:
    utility.clearConsole()
    utility.printMessage(f'"{degree_type}" is an Invalid input')
    return add_education()

  # degree university
  university_name = input('Enter the name of the School: ')

  if university_name.lower() == 'c':
    return

  university_name = university_name.title()

  yearsAttended = input(f"Enter your years attended as yyyy-yyyy. ex: {date.today().year-4}-{date.today().year}: ")

  while not ValidateYearsAttended(yearsAttended):
    yearsAttended = input(f"Enter your years attended as yyyy-yyyy. ex: {date.today().year-4}-{date.today().year}: ")

  if yearsAttended.lower() == "c":
    return

  # confirm all information
  utility.pageTitle('Confirm Education Details')
  print(f'Degree type: {degree_type}')
  print(f'School Name: {university_name}')
  print(f'Years Attended: {yearsAttended}')

  if confirmDetails('Is all this information correct?(y/n): ') == 'y':
    UDCursor.execute(f"""
    INSERT INTO Educations (User, school, degree, years_attended)
    VALUES (?,?,?,?)
    """, (config.currUser, university_name, degree_type, yearsAttended))
    userData.commit()
  else:
    add_education()

# remove education experience
def remove_education():
  """
  deletes an education experiece from the database  
  """
  utility.pageTitle("Remove An Education Experience")
  edu_experiences = UDCursor.execute(
    f"SELECT edu_id, degree, school FROM Educations WHERE User = '{config.currUser}'"
  ).fetchall()

  for i, edu_experience in enumerate(edu_experiences):
    print(f"Press {i+1} to delete {edu_experience[1]} at {edu_experience[2]}")

  print(f"Press {len(edu_experiences)+1} to go back")

  option = input("Input: ")
  optionNum = utility.choiceValidation(option, edu_experiences)

  if optionNum == len(edu_experiences) + 1:
    utility.clearConsole()
    return
  else:
    option = confirmDetails(
      "Are you sure you want to delete this Education experience? (y/n): ")

    if option == "y":
      UDCursor.execute(
        f"DELETE FROM Educations WHERE User = '{config.currUser}' AND edu_id = '{edu_experiences[optionNum-1][0]}'"
      )
      userData.commit()
      utility.printMessage("This Education experience has been deleted.")
      utility.quickGoBack()


def education_settings(edu_id):
  """
  edu_id: the id of the education experience in the table
  """

  while True:
    utility.clearConsole()
    utility.pageTitle(f'Manage {get_education_column("degree", edu_id)} at {get_education_column("school", edu_id)}')
    edu_options = {
      'Manage School Name' : 1,
      'Manage Degree type' : 1,
      'Manage years attended' : 1,
    }

    utility.printMenu(edu_options)
    print(f"Press {len(edu_options)+1} for Back.")

    option = input("Input: ")
    optionNum = utility.choiceValidation(option, edu_options)
    utility.clearConsole()
    if optionNum == len(edu_options) + 1:
      utility.clearConsole()
      break
    elif optionNum == 1:
      edu_university(edu_id)
    elif optionNum == 2:
      degree_type_entry(edu_id)
    elif optionNum == 3:
      years_attended_education(edu_id)
      
  return

# this function is the page that allows users to create, edit, or remove parts of their education history like school name, degree, and years attended
def ManageEducationSection():
  """
  manages the section containing all educations
  """
  utility.pageTitle("Manages Education Experience")
  edu_experiences = UDCursor.execute(
    f"SELECT edu_id, degree, school FROM Educations WHERE User = '{config.currUser}'"
  ).fetchall()

  for i, edu_experience in enumerate(edu_experiences):
    print(f"Press {i+1} to Manage {edu_experience[1]} at {edu_experience[2]}")

  if len(edu_experiences) > 0:
    print(f'Press {len(edu_experiences)+1} to add a new education experience'.title())
    print(f'Press {len(edu_experiences)+2} to remove an education experience'.title())
    print(f"Press {len(edu_experiences)+3} to go back".title())
  else :
    print(f'Press {len(edu_experiences)+1} to add a new education experience'.title())
    print(f"Press {len(edu_experiences)+2} to go back".title())
    
  option = input("Input: ")
  if int(option) == len(edu_experiences) + 1:
    utility.clearConsole()
    add_education()    
  elif int(option) == len(edu_experiences) + 2 and len(edu_experiences) > 0:
    utility.clearConsole()
    remove_education()
  elif int(option) == len(edu_experiences) + 2 and len(edu_experiences) == 0:
    utility.clearConsole()
    return
  elif int(option) == len(edu_experiences) + 3:
    utility.clearConsole()
    return
  elif int(option) > len(edu_experiences) or int(option) < 1:
    utility.clearConsole()
    utility.printMessage('Invalid input')
    return ManageEducationSection()
  else:
    education_settings(edu_experiences[int(option) - 1][0])

#this function will update the specified column in the profiles table with the data
def UpdateProfileData(profileData, type):
  type = type.replace(" ", "_")
  UDCursor.execute(f"""UPDATE Profiles
                        SET {type} = \"{profileData}\"
                        WHERE User = \"{config.currUser}\"
                        """)
  userData.commit()


# this function contains the logic to give users ability to create or edit existing content in their profile based on the type (Title, About, etc. )
def ManageColumnData(type):
  curData = getColumn(type)

  if curData == None:

    if type == "years_attended":
      utility.pageTitle("Add Your Years Attended")
      utility.printMessage("Enter 'c' to cancel anytime.")
      utility.printSeparator()
      profileData = input(
        f"Enter your years attended as yyyy-yyyy. ex: {date.today().year-4}-{date.today().year}: "
      )
    else:
      utility.pageTitle(f"Create Your {type}")
      utility.printMessage("Enter 'c' to cancel anytime.")
      utility.printSeparator()
      profileData = input(f"Enter a profile {type}: ")

    if type == "Title":
      while not VerifyProfileTitle(profileData):
        profileData = input(f"Enter a profile {type}: ")

    elif type == "years_attended":
      while not ValidateYearsAttended(profileData):
        profileData = input(
          f"Enter your years attended as yyyy-yyyy. ex. {date.today().year-4}-{date.today().year}: "
        )

    elif type == "About":
      while not ValidateProfileAbout(profileData):
        profileData = input(f"Enter a profile {type}: ")

    if profileData.lower() == "c":
      return

    # remove leading and trailing whitespaces
    profileData = profileData.strip()

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
      utility.printMessage("Enter 'c' to cancel anytime.")
      utility.printSeparator()

      if type == "University" or type == "Major":
        newData = PrefillInput(f"Edit your {type}: ", curData).title()

        if type == "University":
          while not account.ValidateUniversity(newData):
            newData = PrefillInput(f"Edit your {type}: ", curData).title()

        elif type == "Major":
          while not account.ValidateMajor(newData):
            newData = PrefillInput(f"Edit your {type}: ", curData).title()

      elif type == "Title":
        newData = PrefillInput(f"Edit your {type}: ", curData)
        while not VerifyProfileTitle(newData):
          newData = PrefillInput(f"Edit your {type}: ", curData)

      elif type == "years attended":
        newData = PrefillInput(f"Edit your {type}: ", curData)
        while not ValidateYearsAttended(newData):
          newData = PrefillInput(f"Edit your {type}: ", curData)

      elif type == "About":
        newData = PrefillInput(f"Edit your {type}: ", curData)
        while not ValidateProfileAbout(newData):
          newData = PrefillInput(f"Edit your {type}: ", curData)

      else:
        newData = PrefillInput(f"Edit your {type}: ", curData)

      if newData.lower() == "c":
        return

      newData = newData.strip()
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
  userinput = userinput.strip()
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


def ValidateExperienceEmployer(employer):
  employer = employer.strip()

  if employer.lower() == "c":
    return 1

  if utility.hasSpecialCharacter(employer):
    utility.printMessage(
      "You cannot include any special characters for your employer.")
    return 0

  if len(employer) < 2:
    utility.printMessage("Add more characters for your employer.")
    return 0

  return 1


def ValidateExperienceLocation(location):
  location = location.strip()
  specialCharacters = [
    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', '-', '.', '/', ':',
    ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}',
    '~'
  ]
  if location.lower() == "c":
    return 1

  if utility.hasSpecialCharacter(location):
    for char in location:
      if char in specialCharacters:
        utility.printMessage("You can only include the special character ,")
        return 0

  return 1


def ValidateExperienceDescription(description):
  description = description.strip()
  if description.lower == "c":
    return 1
  if len(description) < 5:
    utility.printMessage("Add more characters to your description.")
    return 0

  return 1


# this function will allow a user to add a new experience
def AddExperience():
  while True:
    # insert the username into Experiences Table
    utility.pageTitle("Add An Experience")
    utility.printMessage("Enter 'c' to leave and save your progress.")
    utility.printSeparator()
    title = employer = dateStarted = dateEnded = location = description = ""

    title = input("Enter a title for your experience: ")
    while not VerifyProfileTitle(title):
      title = input("Enter a title for your experience: ")

    if title == "c":
      return

    employer = input("Enter an employer: ")
    while not ValidateExperienceEmployer(employer):
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
    while not ValidateExperienceLocation(location):
      location = input("Enter a location: ")
    if location == "c":
      location = ""
      break

    description = input("Enter a description: ")
    while not ValidateExperienceDescription(description):
      description = input("Enter a description: ")
    if description == "c":
      description = ""
      break
    break

  # remove leading and trailing whitespaces
  title = title.strip()
  employer = employer.strip()
  dateStarted = dateStarted.strip()
  dateEnded = dateEnded.strip()
  location = location.strip()
  description = description.strip()

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

    if type == "Date started" or type == "Date ended":
      while not VerifyExperienceDate(newData):
        newData = input(f"Add your {type}: ")

    elif type == "Employer":
      while not ValidateExperienceEmployer(newData):
        newData = input(f"Add your {type}: ")

    elif type == "Location":
      while not ValidateExperienceLocation(newData):
        newData = input(f"Add your {type}: ")

    elif type == "Description":
      while not ValidateExperienceDescription(newData):
        newData = input(f"Add your {type}: ")

    if newData.lower() == "c":
      return

    newData = newData.strip()
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

      elif type == "Employer":
        while not ValidateExperienceEmployer(newData):
          newData = PrefillInput(f"Edit your {type}: ", curData)

      elif type == "Location":
        while not ValidateExperienceLocation(newData):
          newData = PrefillInput(f"Edit your {type}: ", curData)

      elif type == "Description":
        while not ValidateExperienceDescription(newData):
          newData = PrefillInput(f"Edit your {type}: ", curData)

      if newData.lower() == "c":
        return

      newData = newData.strip()
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
      f"SELECT Title, Employer, Date_started, Date_ended, Location, Description FROM Experiences WHERE User = '{config.currUser}' AND e_id = {experienceID}"
    ).fetchone()

    # store experience content retrieved from db into this dictionary
    experience_content = {
      "Title": experience[0],
      "Employer": experience[1],
      "Date_started": experience[2],
      "Date_ended": experience[3],
      "Location": experience[4],
      "Description": experience[5]
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


# this function will allow a user to publish or unpublish their profile so it can be viewed by friends of the user
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

  if getColumn("Title") == None or getColumn("About") == None or len(UDCursor.execute(
    f"SELECT User FROM Educations WHERE User = '{config.currUser}'"
  ).fetchall()) == 0:
    if getColumn("Title") == None:
      utility.printMessage("You cannot publish your profile without a title.")
    if getColumn("About") == None:
      utility.printMessage("You cannot publish your profile without an About.")
    if len(UDCursor.execute(
    f"SELECT User FROM Educations WHERE User = '{config.currUser}'"
  ).fetchall()) == 0:
      utility.printMessage("You must have at least one education history in your profile before you can publish.")
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
      userData.commit()
      if published == 0:
        utility.printMessage("You have unpublished your profile.")
      else:
        utility.printMessage("You have published your profile.")

      utility.quickGoBack()


def ViewProfileUser():
  ViewProfile(config.currUser)
  
# this function will allow a user to view their current profile
def ViewProfile(user_profile):
  print('  O\n--|--\n / \\\n-------')
  user, title, university, major, about, published = UDCursor.execute("SELECT * FROM Profiles WHERE User = ?", (user_profile,)).fetchone()
  first, last = UDCursor.execute("SELECT FirstName, LastName FROM userData WHERE Username = ?", (user_profile,)).fetchone()
  
  print(f"{first} {last}, {title}")
  print(f'{major} at {university}')
  print(f'------------------\nAbout\n------------------')
  print(about)
  print('------------------')

  UDCursor.execute("SELECT * FROM Educations WHERE User = ?", (user_profile,))
  educations = UDCursor.fetchall()

  if educations:
    print('Education:')

    for education in educations:
      edu_id, user, school, degree, years_attended = education        
      print('------------------')
      print(f"School name: {school}")
      print(f'Degree: {degree}')
      print(f'Years Attended: {years_attended}')
      print('------------------')

  UDCursor.execute("SELECT * FROM Experiences WHERE User = ?", (user_profile,))
  experiences = UDCursor.fetchall()

  if experiences:
    print('Experiences:')

    for experience in experiences:
      e_id, user, title, employer, date_started, date_ended, location, description = experience
      print('------------------')
      print(f'{title}, {employer}')
      print(location)
      print(f'{date_started} to {date_ended}\n')
      print(description)
      print('------------------')

  utility.quickGoBack()