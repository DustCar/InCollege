'''This file holds all functions dealing with the Find Someone function'''

import sqlite3 as sql
import utility
import config

cancel = False

# Connect to SQL database
userData = sql.connect("User_Data.db")
UDCursor = userData.cursor()

def FNameInput():
  
  return

def LNameInput():
  
  return

def SearchStudent():
  global cancel

  utility.pageTitle("Search for another Student")
  utility.printMessage("To search for someone simply enter their first and last name. To cancel, press 'c' anytime")
  utility.printSeparator()

  if cancel is False:
    first = FNameInput()
    utility.printSeparator()
  if cancel is False:
    last = LNameInput()
  
  
  return

def FindSomeonePage():

  utility.pageTitle("Find Someone")

  findMenuOptions = {
    "Search for a fellow Student": SearchStudent,
  }
  utility.printMenu(findMenuOptions)
  print(f"Press {len(findMenuOptions)+1} for Back.")
  
  
  return