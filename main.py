"""This file contains the main code for InCollege,
including the different pages and relevant functions."""


# imports
import sqlite3
import utility


# global variables
minUsr = 1
maxUsr = 20
minPasswd = 8
maxPasswd = 12


# function for initial InCollege screen
def inCollege():
  utility.pageTitle("Welcome to InCollege!")
  
  welcome = {"Log In": login, 
             "Create An Account": createAcct, 
             "Exit InCollege": closeApp}
  
  utility.printMenu(welcome)
  
  option = input("Input: ")
  optionNum = utility.choiceValidation(option)

  utility.call(optionNum, welcome)
  return
  

# function for log in page
def login():
  utility.pageTitle("Log In")
  
  usr = input("Username: ")
  passwd = input("Password: ")
  loginAuthorization(usr, passwd)
  
  utility.printMessage("You have successfully logged in")
  loggedin()
  return


# function for authorizing login info -- INCOMPLETE
def loginAuthorization(usr, passwd):
  badUsr = len(usr) < minUsr or len(usr) > maxUsr
  badPasswd = len(passwd) < minPasswd or len(passwd) > maxPasswd
  
  while badUsr or badPasswd:
    utility.printMessage("Incorrect username/password, please try again")
    end = input("Press Q to quit. Otherwise, press any key.\nInput: ")
    if end == 'q' or end == 'Q':
      return
    utility.pageTitle("Log In")
    usr = input("Username: ")
    passwd = input("Password: ")
    badUsr = len(usr) < minUsr or len(usr) > maxUsr
    badPasswd = len(passwd) < minPasswd or len(passwd) > maxPasswd
  return


# function for screen after logging in
def loggedin():
  utility.pageTitle("Home")
  
  home = {"Job Search" : utility.construction,
          "Find Someone" : utility.construction,
          "Learn a New Skill" : learnSkill,
          "Log out" : inCollege}

  utility.printMenu(home)

  option = input("Input: ")
  optionNum = utility.choiceValidation(option)
  
  utility.call(optionNum, home)
  return


# function for exiting InCollege
def closeApp():
  utility.printMessage("Exited InCollege.")
  exit(0)
  

# function for creating an account -- INCOMPLETE
def createAcct():
  utility.pageTitle("Create An Account")
  return


# function to learn a skill
def learnSkill():
  utility.pageTitle("Learn a New Skill")
  
  skills = {"Skill1" : utility.construction,
            "Skill2" : utility.construction,
            "Skill3" : utility.construction,
            "Skill4" : utility.construction,
            "Skill5" : utility.construction,
            "Home" : loggedin}
  
  utility.printMenu(skills)

  option = input("Input: ")
  optionNum = utility.choiceValidation(option)
  
  utility.call(optionNum, skills)
  return


# call/open InCollege
inCollege()
