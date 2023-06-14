"""This file contains all functions involving the Important Links page"""

import utility

def ImportantLinksPage():
  
  while True:
    utility.pageTitle("InCollege Important Links")

    impLinksOptions = {
      "A Copyright Notice": utility.construction,
      "About": utility.construction,
      "Accessibility": utility.construction,
      "User Agreement": utility.construction,
      "Privacy Policy": utility.construction,
      "Cookie Policy": utility.construction,
      "Copyright Policy": utility.construction,
      "Brand Policy": utility.construction,
    }
    utility.printMenu(impLinksOptions)
    print(f"Press {len(impLinksOptions)+1} for Back.")
    
    choice = input("Input: ")
    choiceNum = utility.choiceValidation(choice, impLinksOptions)
    if choiceNum == len(impLinksOptions)+1:
      break
    else:
      utility.call(choiceNum, impLinksOptions)
  
  return