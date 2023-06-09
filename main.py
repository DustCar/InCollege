"""This file contains the main code for InCollege,
including the different pages and relevant functions."""

# imports
import account
import jobsearch
import findsomeone
import utility
import time
import config
import getpass as gp

# global variables
minUsr = 1
maxUsr = 20
minPasswd = 8
maxPasswd = 12

# function for initial InCollege screen
def inCollege():
  
  while True:
    utility.pageTitle("Welcome to InCollege!")
    welcome = {
      "Log In": loginPage,
      "Create An Account": createAcctPage,
      "Video About InCollege": videoPage,
      "Find Someone": newUserFind
    }
  
    utility.printSuccessStory()
    utility.printMenu(welcome)
    print(f"Press {len(welcome)+1} for Exit InCollege")
  
    option = input("Input: ")
    if int(option) == len(welcome)+1:
      closeApp()
      break
    else:
      optionNum = utility.choiceValidation(option, welcome)
      utility.call(optionNum, welcome)
  return


# function for log in page
def loginPage():
  utility.pageTitle("Log In")

  usr = input("Username: ")
  passwd = gp.getpass(prompt="Password: ")

  goodLogin = loginAuthorization(usr, passwd)
  if goodLogin:
    utility.printMessage("You have successfully logged in")
    config.currUser = usr
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
      return False
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
  while True:
    utility.pageTitle("Home")
    utility.printMessage(f"Current user: {config.currUser}")
  
    home = {
      "Job Search": jobsearch.JobSearchPage,
      "Find Someone": findsomeone.FindSomeonePage,
      "Learn a New Skill": learnSkill
    }
  
    utility.printMenu(home)
    print(f"Press {len(home)+1} for Log Out")
  
    option = input("Input: ")
    if int(option) == len(home)+1:
      config.currUser = "None"
      break
    else:
      optionNum = utility.choiceValidation(option, home)
      utility.call(optionNum, home)
  return


# function to quit back to initial screen
def quitOption():
  end = input("Press Q to quit. Otherwise, press any key.\nInput: ")
  if end == 'q' or end == 'Q':
    return 1
  return 0 


# function for exiting InCollege
def closeApp():
  utility.printMessage("Exited InCollege.")
  return


# function for creating an account
def createAcctPage():
  utility.pageTitle("Create An Account")
  account.createAccount()
  return

# function to call Job Search page
#def jobSearchMain():
  #jobsearch.JobSearchPage()
  #loggedin()

#def findSomeoneMain():
  #findsomeone.FindSomeonePage()
  #loggedin()

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
  time.sleep(5)
  return

# function for search specific to users not logged in
def newUserFind():
  findsomeone.SearchStudent()
  if findsomeone.inSystem == True:
    utility.printSeparator()
    utility.printMessage("Would you like to join your friend in inCollege? Or have an account already?")
    utility.printSeparator()
    
    shortMenu = {
      "Create an Account": createAcctPage,
      "Login": loginPage
    }
    utility.printMenu(shortMenu)
    print(f"Press {len(shortMenu)+1} for Back")

    option = input("Input: ")
    if int(option) == len(shortMenu)+1:
      return
    else:
      optionNum = utility.choiceValidation(option, shortMenu)
      utility.call(optionNum, shortMenu)
  return

# call/open InCollege
if __name__ == "__main__":
  inCollege()