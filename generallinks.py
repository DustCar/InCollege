"""This file contains all functions involving the General Links page"""

import utility, account, config


def GeneralLinksPage():
  while True:
    utility.pageTitle("General Links")
    if config.currUser is None:
      generalLinksOptions = {
        "Sign Up": account.createAcctPage,
        "Help Center": helpCenter,
        "About": about,
        "Press": press,
        "Blog": utility.construction,
        "Careers": utility.construction,
        "Developers": utility.construction,
      }
    else:
      generalLinksOptions = {
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

  utility.pageTitle("Help Center")
  utility.printMessage("We're here to help")
  utility.quickGoBack()
  return


def about():

  utility.pageTitle("About")
  utility.printMessage(
    "In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide"
  )
  utility.quickGoBack()
  return


def press():

  utility.pageTitle("Press")
  utility.printMessage(
    "In College Pressroom: Stay on top of the latest news, updates, and reports"
  )
  utility.quickGoBack()
  return


def blog():
  utility.pageTitle("Blog")
  utility.construction()
  return


def careers():
  utility.pageTitle("Careers")
  utility.construction()
  return


def developers():
  utility.pageTitle("Developers")
  utility.construction()
  return
