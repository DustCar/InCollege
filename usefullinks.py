"""This file contains all functions relating to the Useful Links section of InCollege"""

import utility, generallinks


def UsefulLinksPage():
  
  while True:
    utility.pageTitle("Useful Links")

    usefulLinksOptions = {
      "General": generallinks.GeneralLinksPage,
      "Browse InCollege": utility.construction,
      "Business Solutions": utility.construction,
      "Directories": utility.construction
    }
    utility.printMenu(usefulLinksOptions)
    print(f"Press {len(usefulLinksOptions)+1} for Back.")
    
    choice = input("Input: ")
    choiceNum = utility.choiceValidation(choice, usefulLinksOptions)
    if choiceNum == len(usefulLinksOptions)+1:
      utility.clearConsole()
      break
    else:
      utility.call(choiceNum, usefulLinksOptions)
  
  return