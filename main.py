"""This file contains the main code for InCollege,
including the different pages and relevant functions."""


# imports
import account, jobsearch, findsomeone, usefullinks, implinks, utility, friends
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
      "Create An Account": account.createAcctPage,
      "Video About InCollege": videoPage,
      "Find Someone": newUserFind,
      "Useful Links": usefullinks.UsefulLinksPage,
      "InCollege Important Links": implinks.ImportantLinksPage
    }

    utility.printSuccessStory()
    utility.printMenu(welcome)
    print(f"Press {len(welcome)+1} for Exit InCollege.")

    option = input("Input: ")
    optionNum = utility.choiceValidation(option, welcome)

    if optionNum == len(welcome) + 1:
      closeApp()
      break
    else:
      utility.call(optionNum, welcome)
  return


# function for log in page
def loginPage():
  utility.pageTitle("Log In")
  utility.printMessage("To cancel, press 'c' at any time")
  utility.printSeparator()

  usr = input("Username: ")
  if usr == "c":
    utility.clearConsole()
    return
  passwd = gp.getpass(prompt="Password: ")
  if passwd == "c":
    utility.clearConsole()
    return

  goodLogin = loginAuthorization(usr, passwd)
  if goodLogin:
    utility.clearConsole()
    utility.printMessage("You have successfully logged in")
    loggedin()
  return


# function for initial login info check
def loginAuthorization(usr, passwd):
  badUsr = len(usr) < minUsr or len(usr) > maxUsr
  badPasswd = len(passwd) < minPasswd or len(passwd) > maxPasswd

  incorrectInfo = account.login(usr, passwd)
  newUsr = usr
  
  while badUsr or badPasswd or incorrectInfo:
    utility.printMessage("Incorrect username/password, please try again")
    utility.pageTitle("Log In")
    utility.printMessage("To cancel, press 'c' at any time")
    newUsr = input("Username: ")
    if newUsr == "c":
      utility.clearConsole()
      return False
    newPasswd = gp.getpass(prompt="Password: ")
    if newPasswd == "c":
      utility.clearConsole()
      return False
    badUsr = len(newUsr) < minUsr or len(newUsr) > maxUsr
    badPasswd = len(newPasswd) < minPasswd or len(newPasswd) > maxPasswd
    incorrectInfo = account.login(newUsr, newPasswd)

  config.currUser = newUsr
  return True


# function for screen after logging in
def loggedin():
  global currUser

  # notify users they have pending requests when they log in
  friends.FriendRequestNotification()
  
  while True:
    utility.pageTitle("Home")
    utility.printMessage(f"Current user: {config.currUser}")
    utility.printSeparator()

    home = {
      "Job Search": jobsearch.JobSearchPage,
      "Find Someone": findsomeone.FindSomeonePage,
      "Learn a New Skill": learnSkill,
      "Useful Links": usefullinks.UsefulLinksPage,
      "InCollege Important Links": implinks.ImportantLinksPage,
      "My Friends": friends.MyFriendsPage
    }

    utility.printMenu(home)
    print(f"Press {len(home)+1} for Log Out.")

    option = input("Input: ")
    optionNum = utility.choiceValidation(option, home)

    if optionNum == len(home) + 1:
      config.currUser = None
      utility.clearConsole()
      break
    else:
      utility.call(optionNum, home)
  return


# function for exiting InCollege
def closeApp():
  utility.printMessage("Exited InCollege.")
  return

# function to learn a skill
def learnSkill():
  while True:
    utility.pageTitle("Learn a New Skill")
    skills = {
      "Skill1": utility.construction,
      "Skill2": utility.construction,
      "Skill3": utility.construction,
      "Skill4": utility.construction,
      "Skill5": utility.construction
    }

    utility.printMenu(skills)
    print(f"Press {len(skills)+1} for Back.")

    option = input("Input: ")
    optionNum = utility.choiceValidation(option, skills)

    if optionNum == len(skills) + 1:
      utility.clearConsole()
      break
    else:
      utility.call(optionNum, skills)
  return


# function for video page
def videoPage():
  utility.printMessage("Video is now playing")
  utility.quickGoBack()
  utility.clearConsole()
  return


# function for search specific to users not logged in
def newUserFind():
  findsomeone.SearchStudent()
  if findsomeone.inSystem == True:
    utility.printSeparator()
    utility.printMessage(
      "Would you like to join your friend in inCollege? Or have an account already?"
    )
    utility.printSeparator()

    shortMenu = {"Create an Account": account.createAcctPage, "Login": loginPage}
    utility.printMenu(shortMenu)
    print(f"Press {len(shortMenu)+1} for Back.")

    option = input("Input: ")
    optionNum = utility.choiceValidation(option, shortMenu)

    if optionNum == len(shortMenu) + 1:
      utility.clearConsole()
      return
    else:
      utility.call(optionNum, shortMenu)
  return


# call/open InCollege
if __name__ == "__main__":
  inCollege()
