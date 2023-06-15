"""This file contains all functions involving the Important Links page"""

import utility, config


def ImportantLinksPage():

  while True:
    utility.pageTitle("InCollege Important Links")

    impLinksOptions = {
      "A Copyright Notice": copyright_notice,
      "About": about,
      "Accessibility": accessibility,
      "User Agreement": user_agreement,
      "Privacy Policy": privacy_policy,
      "Cookie Policy": cookie_policy,
      "Copyright Policy": copyright_policy,
      "Brand Policy": brand_policy,
      "Languages": languages
    }
    utility.printMenu(impLinksOptions)
    print(f"Press {len(impLinksOptions)+1} for Back.")

    choice = input("Input: ")
    choiceNum = utility.choiceValidation(choice, impLinksOptions)
    if choiceNum == len(impLinksOptions) + 1:
      utility.clearConsole()
      break
    else:
      utility.call(choiceNum, impLinksOptions)

  return


def copyright_notice():
  utility.pageTitle("Copyright Notice")
  utility.printMessage("Copyright 2023 InCollege. All rights reserved.")
  utility.quickGoBack()
  return
    
  

def about():
  utility.pageTitle("About")
  print("""The Solution
  • InCollege is an online tool that has been designed exclusively for college students.
  • Allows students at different universities to connect, exchange information, and talk with each other.
  • Understands that everyone's looking for a first job and provides the tools that they need in order to be successful.
  • Students can use this tool while they are in college and then transition to LinkedIn once they get a job and leave school
    """)
  utility.quickGoBack()
  return

def accessibility():
  utility.pageTitle("Accessibility")
  utility.printMessage(
    "We aim to ensure that our services are accessible to all our users. If you encounter any accessibility issues, please contact us."
  )
  utility.quickGoBack()
  return

def user_agreement():
  utility.pageTitle("User Agreement")
  utility.printMessage(
    "Your agreement to our terms of use is required to use our service. Please read them carefully."
  )
  utility.quickGoBack()
  return

def privacy_policy():
  while True:
    utility.pageTitle("Privacy Policy")
    utility.printMessage(
      "We take your privacy seriously. Our policy details how we collect, use and protect your data."
    )
    # Needs configuration. Update: gives user a menu option to go to guest_controls or back, if they are signed in
    if config.currUser is not None:

      ppolicyMenu = {
        "Guest Controls": guest_controls
      }
      utility.printMenu(ppolicyMenu)
      print(f"Press {len(ppolicyMenu)+1} for Back.")

      choice = input("Input: ")
      choiceNum = utility.choiceValidation(choice, ppolicyMenu)
      if choiceNum == len(ppolicyMenu) + 1:
        utility.clearConsole()
        break
      else:
        utility.call(choiceNum, ppolicyMenu)
        
    else:
      utility.quickGoBack()
  return

def cookie_policy():
  utility.pageTitle("Cookie Policy")
  utility.printMessage(
    "We use cookies to improve your experience. By using our service, you agree to our cookie use."
  )
  utility.quickGoBack()
  return

def copyright_policy():
  utility.pageTitle("Copyright Policy")
  utility.printMessage(
    "We respect intellectual property rights and expect you to do the same.")
  utility.quickGoBack()
  return

def brand_policy():
  utility.pageTitle("Brand Policy")
  utility.printMessage("Our brand policy outlines the appropriate use of our brand assets.")
  utility.quickGoBack()
  return

# Will be called for privacy policy
def guest_controls():
  utility.pageTitle("Guest Controls")
  utility.printMessage(
    "As a guest, you have certain controls over your data and privacy settings. Please use them responsibly."
  )
  utility.quickGoBack()
  return

def languages():
  if config.currUser is None:
    utility.printMessage("To change Language settings, please log in.")
    return
    
  utility.pageTitle("Languages")
  utility.printMessage("Select your preferred language")
  
  print("Press 1 for English")
  print("Press 2 for Spanish")
  print("Press 3 for Back")

  while True:
    language_choice = input("Input: ")
  
    if language_choice == "1":
      #update_user_language('english')
      utility.printMessage("Your language has been set to English.")
      return
    elif language_choice == "2":
      #update_user_language('spanish')
      utility.printMessage("Your language has been set to Spanish.")
      return
    elif language_choice == "3":
      utility.clearConsole()
      break
    else:
      utility.printMessage("Invalid input. Select again.")
  return
