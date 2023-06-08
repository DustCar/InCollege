"""This file contains the main code for InCollege,
including the different pages and relevant functions."""

# imports
import account
import jobsearch
import utility
import getpass as gp

# global variables
minUsr = 1
maxUsr = 20
minPasswd = 8
maxPasswd = 12
currUser = None

# function for initial InCollege screen
def inCollege():
  utility.pageTitle("Welcome to InCollege!")

  welcome = {
    "Log In": loginPage,
    "Create An Account": createAcctPage,
    "Video About InCollege": videoPage,
    "Exit InCollege": closeApp
  }

  utility.printSuccessStory()
  utility.printMenu(welcome)

  option = input("Input: ")
  optionNum = utility.choiceValidation(option, welcome)

  utility.call(optionNum, welcome)
  return


# function for log in page
def loginPage():
  global currUser
  utility.pageTitle("Log In")

  usr = input("Username: ")
  passwd = gp.getpass(prompt="Password: ")

  goodLogin = loginAuthorization(usr, passwd)
  if goodLogin:
    utility.printMessage("You have successfully logged in")
    currUser = usr
    jobsearch.SetCurrUser(currUser)
    loggedin()
  return


# function for initial login info check
def loginAuthorization(usr, passwd):
  badUsr = len(usr) < minUsr or len(usr) > maxUsr
  badPasswd = len(passwd) < minPasswd or len(passwd) > maxPasswd

  incorrectInfo = account.login(usr, passwd)

  while badUsr or badPasswd or incorrectInfo:
    utility.printMessage("Incorrect username/password, please try again")
    leave = quitOption()
    if leave:
      exit(0)
    utility.pageTitle("Log In")
    newUsr = input("Username: ")
    newPasswd = gp.getpass(prompt="Password: ")
    badUsr = len(newUsr) < minUsr or len(newUsr) > maxUsr
    badPasswd = len(newPasswd) < minPasswd or len(newPasswd) > maxPasswd
    incorrectInfo = account.login(newUsr, newPasswd)
  return True


# function for screen after logging in
def loggedin():
  global currUser
  utility.pageTitle("Home")

  home = {
    "Job Search": jobSearch,
    "Find Someone": utility.construction,
    "Learn a New Skill": learnSkill,
    "Log Out": inCollege
  }

  utility.printMenu(home)

  option = input("Input: ")
  optionNum = utility.choiceValidation(option, home)

  if optionNum == 4:
    currUser = None
    jobsearch.SetCurrUser(currUser)

  utility.call(optionNum, home)
  return


# function to quit back to initial screen
def quitOption():
  end = input("Press Q to quit. Otherwise, press any key.\nInput: ")
  if end == 'q' or end == 'Q':
    inCollege()
    return 1
  return


# function for exiting InCollege
def closeApp():
  utility.printMessage("Exited InCollege.")
  exit(0)


# function for creating an account
def createAcctPage():
  utility.pageTitle("Create An Account")
  account.createAccount()
  inCollege()
  return

def jobSearch():
  jobsearch.JobSearchPage()
  loggedin()
  return

# function to learn a skill
def learnSkill():
  utility.pageTitle("Learn a New Skill")

  skills = {
    "Skill1": utility.construction,
    "Skill2": utility.construction,
    "Skill3": utility.construction,
    "Skill4": utility.construction,
    "Skill5": utility.construction,
    "Back": loggedin
  }

  utility.printMenu(skills)

  option = input("Input: ")
  optionNum = utility.choiceValidation(option, skills)

  utility.call(optionNum, skills)
  return


# function for video page
def videoPage():
  utility.printMessage("Video is now playing")
  return


# call/open InCollege
inCollege()
