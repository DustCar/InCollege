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


# function for input validation
def choiceValidation(usrInput):
  while (not usrInput.isnumeric() or len(usrInput) > 1):
    print("Invalid input.")
    usrInput = input("Input: ")
    
  inputNum = int(usrInput)
  return inputNum
  
