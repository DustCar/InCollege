"""This file contains utility functions for InCollege main."""


# function to print the given title of a page
def pageTitle(title):
  print("----------")
  print(title)
  print("----------")
  return


# function to print a system message
def printMessage(message):
  print("* " + message + " *")
  return


# function to print message for incomplete pages
def construction():
  print("Under Construction.")
  return


# function for printing menu 
def printMenu(listOptions):
  numOptions = len(listOptions)
  for choice in range(1, numOptions+1):
    print(f"Press {choice} for {list(listOptions)[choice-1]}.")
  return

# function for selecting from menu 
def call(input, menu):
  for choice in menu:
    if input == list(menu.keys()).index(choice) + 1:
      menu[choice]()
      return


# function for menu selection validation
def choiceValidation(usrInput, menu):
  menuLength = len(menu)
  menuRange = range(1, menuLength + 1)
  
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
  isOneCharacter = (len(usrInput) == 1)
  if isNumeric:
    inRange = int(usrInput) in menuRange
  else:
    inRange = False
  if (isNumeric and isOneCharacter and inRange):
    return True
  else:
    return False