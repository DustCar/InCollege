"""This file contains all functions involving the General Links page"""

import utility, account


def GeneralLinksPage():
  """This function manages the display and user interaction for the General Links Page."""
  while True:
    utility.pageTitle("General Links")
    generalLinksOptions = {
      "Sign Up": account.createAcctPage,
      "Help Center": helpCenter,
      "About": about,
      "Press": press,
      "Blog": utility.construction,
      "Careers": utility.construction,
      "Developers": utility.construction,
    }
    utility.printMenu(generalLinksOptions)
    print(f"Press {len(generalLinksOptions)+1} for Back.")

    choice = input("Input: ")
    choiceNum = utility.choiceValidation(choice, generalLinksOptions)
    if choiceNum == len(generalLinksOptions) + 1:
      utility.clearConsole()
      break
    else:
      utility.call(choiceNum, generalLinksOptions)
  return


def helpCenter():
  """This function provides a placeholder response to the Help Center option."""
  print("We're here to help")


def about():
  """This function provides a brief description about InCollege."""
  print(
    "In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide"
  )


def press():
  """This function provides a placeholder response to the Press option."""
  print(
    "In College Pressroom: Stay on top of the latest news, updates, and reports"
  )


def blog():
  """This function calls the construction placeholder function for the Blog option."""
  utility.construction()


def careers():
  """This function calls the construction placeholder function for the Careers option."""
  utility.construction()


def developers():
  """This function calls the construction placeholder function for the Developers option."""
  utility.construction()
