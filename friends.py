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
      "Show My Network": ShowMyNetworkPage,
      "Show Pending Requests": ShowMyPendingRequestsPage
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


#Before a user sends a request, these conditions must be met
def CanSendRequest(friendToAdd):
  # Check if the current user is trying to send a request to themselves
  if friendToAdd == config.currUser:
    print("You can't send a friend request to yourself.")
    return False

  # Check if the current user has already sent a request to the other user
  existing_request = UDCursor.execute(
    f"SELECT * FROM FriendRequests WHERE Sender = '{config.currUser}' AND Receiver = '{friendToAdd}'"
  ).fetchone()
  if existing_request is not None:
    print("You have already sent a friend request to this user.")
    return False

  # Check if the other user has already sent a request to the current user
  incoming_request = UDCursor.execute(
    f"SELECT * FROM FriendRequests WHERE Sender = '{friendToAdd}' AND Receiver = '{config.currUser}'"
  ).fetchone()
  if incoming_request is not None:
    print("This user has already sent you a friend request.")
    return False

  # Check if the two users are already friends
  existing_friendship = UDCursor.execute(
    f"SELECT * FROM Friends WHERE (User = '{config.currUser}' AND Friend = '{friendToAdd}') OR (User = '{friendToAdd}' AND Friend = '{config.currUser}')"
  ).fetchone()
  if existing_friendship is not None:
    print("You are already friends with this user.")
    return False

  # If none of the above conditions are met, the current user can send a request to the other user
  return True


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
        users = UDCursor.execute(
          f"SELECT Username, FirstName, LastName, University, Major FROM userData WHERE LastName = '{lastname}'"
        ).fetchall()
        if len(users) > 0:
          print("\n")
          utility.printMessage(f"Matches Found: {len(users)}")
          print("\n")
          for i, user in enumerate(users):
            print(f"{i+1}: {user[1]} {user[2]}, {user[3]}, {user[4]}\n")
        while True:
          friendNum = input(
            "Enter the number of the friend you would like to send a friend request to, or 'c' to cancel: "
          )
          if friendNum == 'c':
            break
          elif not friendNum.isdigit() or int(friendNum) < 1 or int(
              friendNum) > len(users):
            print("Invalid number. Please try again.")
          else:
            friendToAdd = users[int(friendNum) - 1][
              0]  # Get the username of the selected friend
            if CanSendRequest(friendToAdd):
              # Add the new friendship to the database
              UDCursor.execute(
                f"INSERT INTO FriendRequests VALUES ('{config.currUser}', '{friendToAdd}')"
              )
              userData.commit()
              print(f"You have sent a friend request to {friendToAdd}.")
              break
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
        users = UDCursor.execute(
          f"SELECT Username, FirstName, LastName, University, Major FROM userData WHERE LOWER(University) = '{university}'"
        ).fetchall()
        if len(users) > 0:
          print("\n")
          utility.printMessage(f"Matches Found: {len(users)}")
          print("\n")
          for i, user in enumerate(users):
            print(f"{i+1}: {user[1]} {user[2]}, {user[3]}, {user[4]}\n")
        while True:
          friendNum = input(
            "Enter the number of the friend you would like to send a friend request to, or 'c' to cancel: "
          )
          if friendNum == 'c':
            break
          elif not friendNum.isdigit() or int(friendNum) < 1 or int(
              friendNum) > len(users):
            print("Invalid number. Please try again.")
          else:
            friendToAdd = users[int(friendNum) - 1][
              0]  # Get the username of the selected friend
            if CanSendRequest(friendToAdd):
              # Add the new friendship to the database
              UDCursor.execute(
                f"INSERT INTO FriendRequests VALUES ('{config.currUser}', '{friendToAdd}')"
              )
              userData.commit()
              print(f"You have sent a friend request to {friendToAdd}.")
              break
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
        users = UDCursor.execute(
          f"SELECT Username, FirstName, LastName, University, Major FROM userData WHERE LOWER(major) = '{major}'"
        ).fetchall()
        if len(users) > 0:
          print("\n")
          utility.printMessage(f"Matches Found: {len(users)}")
          print("\n")
          for i, user in enumerate(users):
            print(f"{i+1}: {user[1]} {user[2]}, {user[3]}, {user[4]}\n")
        while True:
          friendNum = input(
            "Enter the number of the friend you would like to send a friend request to, or 'c' to cancel: "
          )
          if friendNum == 'c':
            break
          elif not friendNum.isdigit() or int(friendNum) < 1 or int(
              friendNum) > len(users):
            print("Invalid number. Please try again.")
          else:
            friendToAdd = users[int(friendNum) - 1][
              0]  # Get the username of the selected friend
            if CanSendRequest(friendToAdd):
              # Add the new friendship to the database
              UDCursor.execute(
                f"INSERT INTO FriendRequests VALUES ('{config.currUser}', '{friendToAdd}')"
              )
              userData.commit()
              print(f"You have sent a friend request to {friendToAdd}.")
              break
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


#Handles Pending Friends


def ShowMyNetworkPage():
  #RemoveFriend shows all students and allows you to remove one
  RemoveFriend()
  pass


def ShowMyPendingRequestsPage():
  utility.pageTitle("Your Friend Requests")

  # query the database for requests sent by the current user
  sent_requests = UDCursor.execute(
    f"SELECT Receiver FROM FriendRequests WHERE Sender = '{config.currUser}'"
  ).fetchall()

  # query the database for requests received by the current user
  received_requests = UDCursor.execute(
    f"SELECT Sender FROM FriendRequests WHERE Receiver = '{config.currUser}'"
  ).fetchall()

  # print all sent requests
  print("Friend requests you've sent that have not been accepted yet:")
  if len(sent_requests) > 0:
    for i, request in enumerate(sent_requests):
      print(f"{i+1}: {request[0]}")
  else:
    print("You have no pending requests.")
  print("\n")

  # print all received requests
  print("Friend requests you've received that you haven't accepted yet:")
  if len(received_requests) > 0:
    for i, request in enumerate(received_requests):
      print(f"{i+1}: {request[0]}")

    while True:
      selection = input(
        "\nEnter the number of the friend request you'd like to accept, 'd' followed by the number to decline, or 'c' to cancel: "
      )
      if selection == 'c':
        break
      elif selection.startswith('d') and selection[1:].isdigit():
        selection_number = int(selection[1:])
        if selection_number < 1 or selection_number > len(received_requests):
          print("Invalid number. Please try again.")
        else:
          friendToDecline = received_requests[selection_number - 1][
            0]  # Get the username of the selected friend
          # Remove the friend request from the FriendRequests table
          UDCursor.execute(
            f"DELETE FROM FriendRequests WHERE Sender = '{friendToDecline}' AND Receiver = '{config.currUser}'"
          )
          userData.commit()
          print(
            f"You have declined the friend request from {friendToDecline}.")
      elif selection.isdigit():
        selection_number = int(selection)
        if selection_number < 1 or selection_number > len(received_requests):
          print("Invalid number. Please try again.")
        else:
          friendToAccept = received_requests[selection_number - 1][
            0]  # Get the username of the selected friend
          # Remove the friend request from the FriendRequests table
          UDCursor.execute(
            f"DELETE FROM FriendRequests WHERE Sender = '{friendToAccept}' AND Receiver = '{config.currUser}'"
          )
          # Add the new friendship to the Friends table for both users
          UDCursor.execute(
            f"INSERT INTO Friends VALUES ('{config.currUser}', '{friendToAccept}')"
          )
          UDCursor.execute(
            f"INSERT INTO Friends VALUES ('{friendToAccept}', '{config.currUser}')"
          )
          userData.commit()
          print(f"You are now friends with {friendToAccept}.")
          break
      else:
        print("Invalid input. Please try again.")
  else:
    print("You have no incoming friend requests.")
  print("\n")

  input("Press any key to return")
  utility.clearConsole()

#Function shows all friends, and allows you to remove one.
def RemoveFriend():
  # Query to get all current friends
  friends = UDCursor.execute(
    f"SELECT Friend FROM Friends WHERE User = '{config.currUser}'").fetchall()

  # Dictionary to map friends' usernames to their names
  friend_names = {}

  # Print all friends
  print("Your current friends are:")
  for i, friend in enumerate(friends):
    # Get the friend's first and last name from the userData table
    friend_info = UDCursor.execute(
      f"SELECT FirstName, LastName FROM userData WHERE Username = '{friend[0]}'"
    ).fetchone()
    friend_names[friend[0]] = f"{friend_info[0]} {friend_info[1]}"
    print(f"{i + 1}. {friend_names[friend[0]]}")

  # Ask user to select a friend to remove
  selected_friend = input(
    "Enter the number of the friend you want to remove or press 'c' to cancel: "
  )
  if selected_friend == 'c':
    return
  selected_friend = int(selected_friend) - 1
  friend_to_remove = friends[selected_friend][0]

  # Ask for confirmation
  confirmation = input(
    f"Are you sure you want to remove {friend_names[friend_to_remove]} from your friends list? (Y/N): "
  )

  # If confirmed, remove the friend
  if confirmation.lower() == 'y':
    UDCursor.execute(
      f"DELETE FROM Friends WHERE (User = '{config.currUser}' AND Friend = '{friend_to_remove}') OR (User = '{friend_to_remove}' AND Friend = '{config.currUser}')"
    )
    userData.commit()
    print(
      f"{friend_names[friend_to_remove]} has been removed from your friends list."
    )
  else:
    print("Friend removal cancelled.")
