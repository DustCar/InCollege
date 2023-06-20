"""This file contains utility functions for InCollege main."""

# imports
import textwrap
import os


# function to print the given title of a page
def pageTitle(title):
  print("--------------------")
  print(title)
  print("--------------------")
  return


# function to print a system message
def printMessage(message):
  print("* " + message + " *")
  return


# function to print message for incomplete pages
def construction():
  print("Under Construction.")
  quickGoBack()
  return


# function for printing menu
def printMenu(listOptions):
  numOptions = len(listOptions)
  for choice in range(1, numOptions + 1):
    print(f"Press {choice} for {list(listOptions)[choice-1]}.")
  return


# function for printing separator
def printSeparator():
  print("---")
  return


# function for selecting from menu
def call(input, menu):
  for choice in menu:
    if input == list(menu.keys()).index(choice) + 1:
      clearConsole()
      menu[choice]()
      clearConsole()
      return


# function to clear console
def clearConsole():
  """
  There are two ways to clear a console:
  - The cls command in Windows (nt)
  - The clear command in other OS
  
  This function should be called before and 
  after function calls to other pages UNLESS
  navigating through a menu using call() above
  since it currently already implements this.
  """
  if os.name == 'nt':
    os.system('cls')
  else:
    os.system('clear')


# function for menu selection validation
def choiceValidation(usrInput, menu):
  menuLength = len(menu)
  menuRange = range(1, menuLength + 2)

  isValid = inputValidation(usrInput, menuRange)

  while (not isValid):
    print("Invalid input.")
    usrInput = input("Input: ")
    isValid = inputValidation(usrInput, menuRange)
  inputNum = int(usrInput)
  return inputNum


# function for validating input
def inputValidation(usrInput, menuRange):
  isNumeric = usrInput.isnumeric()
  if isNumeric:
    inRange = int(usrInput) in menuRange
  else:
    inRange = False

  if (isNumeric and inRange):
    return True
  else:
    return False


# function for printing user success story
def printSuccessStory():
  userStory = """
          \"Thanks to InCollege, I got my dream job as a 
          college student! The app helped me to connect with 
          students like me, search for suitable jobs, personalize 
          my profile, and learn skills that make me valuable to 
          employers. With a streamlined application process, my 
          transition from student to jobholder was smooth sailing! 
          If you're in college and seeking employment, InCollege 
          is something you can't afford to miss.\""""
  story = textwrap.dedent(userStory).strip()
  print(story)
  print("\t - InCollege User \t\n")

# function to check if a string contains a capital letter
def hasCapitalLetter(password):
  """
  password: attempted new user password

  Checks for capital letters in new user password
  """
  for character in password:
    if character.isupper():
      return True
  return False

# function to check if a string has a digit
def hasDigit(password):
  """
  password: attempted new user password

  Checks for digits in new user password
  """
  for character in password:
    if character.isdigit():
      return True
  return False

#function to check if a string contains a special character
def hasSpecialCharacter(password):
  """
  password: attempted new user password

  Checks for special characters in new user password
  """
  specialCharacters = [
    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
    ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|',
    '}', '~'
  ]
  for character in password:
    if character in specialCharacters:
      return True
  return False

# function that recursively asks to confirm until 'y' or 'n' is typed
def confirmDetails():
  while True:
    confirm = input("Confirm? (y or n): ")
    if confirm == "y" or confirm == "n":
      break
    else:
      printMessage("'y' or 'n' only.")
      continue
  return confirm


def quickGoBack():
  printSeparator()
  print("Press 1 for Back")

  while True:
    usrInput = input("Input: ")
    if usrInput == "1":
      clearConsole()
      break
    else:
      printMessage("Invalid input. Select again.")
  return
