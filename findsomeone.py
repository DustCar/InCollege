'''This file holds all functions dealing with the Find Someone function'''

import sqlite3 as sql
import utility
import config

cancelInput = False
inSystem = False

# Connect to SQL database
userData = sql.connect(config.database)
UDCursor = userData.cursor()

# function for taking input of names
def NameInput(typeName):
  global cancelInput
  
  cName = input(f"Enter {typeName} name of User: ")
  if (cName == 'c'):
    cancelInput = True
    return

  if utility.hasSpecialCharacter(cName):
    utility.printMessage("Special characters are not allowed!")
    NameInput(typeName)
    return
  elif len(cName) > 25:
    utility.printMessage(f"{typeName.capitalize()} name is too long! Try again.")
    NameInput(typeName)
    return
  else:
    return cName.capitalize()
    
  return

# function to search for student
def SearchStudent():
  global inSystem, cancelInput
  inSystem = False
  cancelInput = False
  
  utility.pageTitle("Search for another Student")
  utility.printMessage("To search for someone simply enter their first and last name. To cancel, press 'c' anytime")
  utility.printSeparator()

  if cancelInput is False:
    first = NameInput("first")
    utility.printSeparator()
  if cancelInput is False:
    last = NameInput("last")
    utility.printSeparator()

  for fnames, lnames in UDCursor.execute("SELECT FirstName, LastName FROM userData").fetchall():
    if first == fnames and last == lnames:
      inSystem = True

  if inSystem:
    utility.printMessage("They are a part of the inCollege system")
    if config.currUser == "None":
      return
    FindSomeonePage()
  else:
    utility.printMessage("They are not a part of the inCollege system yet")
    if config.currUser == "None":
      return
    FindSomeonePage()
  return

# main page for find someone functionality
def FindSomeonePage():
  
  utility.pageTitle("Find Someone")

  findMenuOptions = {
    "Search for a fellow Student": SearchStudent,
  }
  utility.printMenu(findMenuOptions)
  print(f"Press {len(findMenuOptions)+1} for Back.")

  choice = input("Input: ")
  if int(choice) == len(findMenuOptions)+1:
    return
  else:
    choiceNum = utility.choiceValidation(choice, findMenuOptions)
    utility.call(choiceNum, findMenuOptions)
  
  return