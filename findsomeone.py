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
  
  while True:
    cName = input(f"Enter {typeName} name of User: ")
    if (cName == 'c'):
      cancelInput = True
      break
  
    if cName.isalpha() == False:
      utility.printMessage("Only letters are allowed!")

      continue
    elif len(cName) > 25:
      utility.printMessage(f"{typeName.capitalize()} name is too long! Try again.")
      continue
    else:
      return cName.capitalize()
  return

# function to search for student
def SearchStudent():
  global inSystem, cancelInput
  inSystem = False
  cancelInput = False
  
  utility.pageTitle("Search for another Student")
  utility.printMessage("To search for someone, simply enter their first and last name. To cancel, press 'c' at any time")
  utility.printSeparator()

  if cancelInput is False:
    first = NameInput("first")
  if cancelInput is False:
    last = NameInput("last")
    utility.printSeparator()
    
  if cancelInput is True:
    utility.clearConsole()
    return

  for fnames, lnames in UDCursor.execute("SELECT FirstName, LastName FROM userData").fetchall():
    if first == fnames and last == lnames:
      inSystem = True

  if inSystem:
    utility.printMessage("They are a part of the inCollege system")
    if config.currUser is not None:
      utility.quickGoBack()
  else:
    utility.printMessage("They are not a part of the inCollege system yet")
    utility.quickGoBack()
  return

# main page for find someone functionality
def FindSomeonePage():
  while True:
    utility.pageTitle("Find Someone")
  
    findMenuOptions = {
      "Search for a fellow Student": SearchStudent,
    }
    utility.printMenu(findMenuOptions)
    print(f"Press {len(findMenuOptions)+1} for Back.")
  
    choice = input("Input: ")
    choiceNum = utility.choiceValidation(choice, findMenuOptions)
    
    if choiceNum == len(findMenuOptions)+1:
      utility.clearConsole()
      break
    else:
      utility.call(choiceNum, findMenuOptions)
  return