# this file will contain the functions that manage the
# friends list for InCollege users

import utility, config, findsomeone
import sqlite3 as sql

# Connect to SQL database
userData = sql.connect(config.database)
UDCursor = userData.cursor()

def MyFriendsPage():
  while True:
    utility.pageTitle("Manage Your Current Friends")

    # menu options within "My Friends"
    options = {
      "Search For Students": SearchStudentPage,
      "Show My Network": ShowMyNetworkPage
    }

    utility.printMenu(options)
    print(f"Press {len(options)+1} for Back.")

    option = input("Input: ")
    optionNum = utility.choiceValidation(option, options)

    if optionNum == len(options) + 1:
      utility.clearConsole()
      break
    else:
      utility.call(optionNum, options)
  return

def SearchStudentPage():
  while True:
    # this helper function handles searching done by last name
    def SearchStudentLN():
      while True:
        utility.pageTitle("Search by Last name")
        utility.printMessage("Type 'c' to cancel the search and go back")
        utility.printSeparator()
        lastname = findsomeone.NameInput("last")

        # if input is c then exit loop
        if lastname is None:
          break

        # search for the users based on last name and store into list
        users = UDCursor.execute(f"SELECT Username, FirstName, LastName, University, Major FROM userData WHERE LastName = '{lastname}'").fetchall()
        if len(users) > 0:
          print("\n")
          utility.printMessage(f"Matches Found: {len(users)}")
          print("\n")
          for i, user in enumerate(users):
            print(f"{i+1}: {user[1]} {user[2]}, {user[3]}, {user[4]}\n")
        else:
          print("\n")
          utility.printMessage("No Matches Found")
          print("\n")

        option = input("Would you like to search again? (y/n): ")
        utility.clearConsole()
        if option == "y":
          continue
        else:
          break

    # this helper function handles searching done by university
    def SearchStudentU():
      while True:
        utility.pageTitle("Search by University")
        utility.printMessage("Type 'c' to cancel the search and go back")
        utility.printSeparator()
        university = input("Enter a university: ")
        university = university.lower()
        
        # if input is c then exit loop
        if university == "c":
          break

        # search for the users based on university and store into list
        users = UDCursor.execute(f"SELECT Username, FirstName, LastName, University, Major FROM userData WHERE LOWER(University) = '{university}'").fetchall()
        if len(users) > 0:
          print("\n")
          utility.printMessage(f"Matches Found: {len(users)}")
          print("\n")
          for i, user in enumerate(users):
            print(f"{i+1}: {user[1]} {user[2]}, {user[3]}, {user[4]}\n")
        else:
          print("\n")
          utility.printMessage("No Matches Found")
          print("\n")

        option = input("Would you like to search again? (y/n): ")
        utility.clearConsole()
        if option == "y":
          continue
        else:
          break

    # this helper function handles searching done by major
    def SearchStudentM():
      while True:
        utility.pageTitle("Search by Major")
        utility.printMessage("Type 'c' to cancel the search and go back")
        utility.printSeparator()
        major = input("Enter a major: ")
        major = major.lower()
        
        # if input is c then exit loop
        if major == "c":
          break

        # search for the users based on university and store into list
        users = UDCursor.execute(f"SELECT Username, FirstName, LastName, University, Major FROM userData WHERE LOWER(major) = '{major}'").fetchall()
        if len(users) > 0:
          print("\n")
          utility.printMessage(f"Matches Found: {len(users)}")
          print("\n")
          for i, user in enumerate(users):
            print(f"{i+1}: {user[1]} {user[2]}, {user[3]}, {user[4]}\n")
        else:
          print("\n")
          utility.printMessage("No Matches Found")
          print("\n")

        option = input("Would you like to search again? (y/n): ")
        utility.clearConsole()
        if option == "y":
          continue
        else:
          break

    utility.pageTitle("Search for friends in InCollege")

    # menu options within "My Friends"
    options = {
      "Search by Last Name": SearchStudentLN,
      "Search by University": SearchStudentU,
      "Search by Major": SearchStudentM
    }

    utility.printMenu(options)
    print(f"Press {len(options)+1} for Back.")

    option = input("Input: ")
    optionNum = utility.choiceValidation(option, options)

    if optionNum == len(options) + 1:
      utility.clearConsole()
      break
    else:
      utility.call(optionNum, options)
  return


def ShowMyNetworkPage():
  pass
