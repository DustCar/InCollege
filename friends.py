# this file will contain the functions that manage the
# friends list for InCollege users

import utility, config
import sqlite3 as sql

# Connect to SQL database
userData = sql.connect(config.database)
UDCursor = userData.cursor()

# check if the table exists and if not create it
try:
  UDCursor.execute("CREATE TABLE Friends(User, Friend)")
  UDCursor.execute("CREATE TABLE FriendRequests(Sender, Receiver)")

except:
  pass


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
    utility.printMessage("You can't send a friend request to yourself.")
    return False

  # Check if the current user has already sent a request to the other user
  existing_request = UDCursor.execute(
    f"SELECT * FROM FriendRequests WHERE Sender = '{config.currUser}' AND Receiver = '{friendToAdd}'"
  ).fetchone()
  if existing_request is not None:
    utility.printMessage("You have already sent a friend request to this user.")
    return False

  # Check if the other user has already sent a request to the current user
  incoming_request = UDCursor.execute(
    f"SELECT * FROM FriendRequests WHERE Sender = '{friendToAdd}' AND Receiver = '{config.currUser}'"
  ).fetchone()
  if incoming_request is not None:
    utility.printMessage("This user has already sent you a friend request.")
    return False

  # Check if the two users are already friends
  existing_friendship = UDCursor.execute(
    f"SELECT * FROM Friends WHERE (User = '{config.currUser}' AND Friend = '{friendToAdd}') OR (User = '{friendToAdd}' AND Friend = '{config.currUser}')"
  ).fetchone()
  if existing_friendship is not None:
    utility.printMessage("You are already friends with this user.")
    return False

  # If none of the above conditions are met, the current user can send a request to the other user
  return True


# this function handles search by function
def SearchStudent(searchCritera):
  display = searchCritera
  
  if searchCritera == "LastName":
    display = "Last Name"
    
  while True:
    utility.pageTitle(f"Search by {display}")
    utility.printMessage("Type 'c' to cancel the search and go back")
    utility.printSeparator()
    userInput = input(f"Enter a {display} to search: ").lower()
      
    if userInput == "c":
      break

    # search for the users based on last name and store into list
    users = UDCursor.execute(
      f"SELECT Username, FirstName, LastName, University, Major FROM userData WHERE LOWER({searchCritera}) = '{userInput}'"
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
        utility.printSeparator()
        if friendNum == 'c':
          break
        elif not friendNum.isdigit() or int(friendNum) < 1 or int(
            friendNum) > len(users):
          print("Invalid number. Please try again.")
        else:
          friendToAdd = users[int(friendNum) -
                              1][0]  # Get the username of the selected friend
          if CanSendRequest(friendToAdd):
            # Add the new friendship to the database
            UDCursor.execute(
              f"INSERT INTO FriendRequests VALUES ('{config.currUser}', '{friendToAdd}')"
            )
            userData.commit()
            print(f"You have sent a friend request to {friendToAdd}.")
            break
        utility.printSeparator()
    else:
      print("\n")
      utility.printMessage("No Matches Found")
      print("\n")

    while True:
      option = input("\nWould you like to search again? (y/n): ").lower()
      if option == "y":
        break
      elif option == "n":
        return
      else:
        utility.printMessage("Invalid input. try again")
    
    utility.clearConsole()
    

# Search students by lastname
def SearchStudentLN():
  SearchStudent("LastName")

# Search students by University
def SearchStudentU():
  SearchStudent("University")

# Search students by major
def SearchStudentM():
  SearchStudent("Major")


def SearchStudentPage():
  while True:

    utility.pageTitle("Search for friends in InCollege")

    # menu options within search students page

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

def ShowSentRequests():
  # query the database for requests sent by the current user
  sent_requests = UDCursor.execute(
    f"SELECT Receiver FROM FriendRequests WHERE Sender = '{config.currUser}'"
  ).fetchall()

  # print all sent requests
  utility.printMessage("Sent Friend Requests")
  utility.printSeparator()
  
  if len(sent_requests) > 0:
    for i, request in enumerate(sent_requests):
      print(f"{i+1}: {request[0]}")
  else:
    print("You have no pending requests.")
  print("\n")

  
def ShowRecievedRequests():
  # query the database for requests received by the current user
  received_requests = UDCursor.execute(
    f"SELECT Sender FROM FriendRequests WHERE Receiver = '{config.currUser}'"
  ).fetchall()

    # print all received requests
  utility.printMessage("Recieved Friend Requests")
  utility.printSeparator()
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
          break
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

  utility.quickGoBack()
  utility.clearConsole()

def ShowMyPendingRequestsPage():
  utility.pageTitle("Your Friend Requests")
  print("\n")
  ShowSentRequests()
  ShowRecievedRequests()
    

#Function shows all friends, and allows you to remove one.
def RemoveFriend():
  # Query to get all current friends
  friends = UDCursor.execute(
    f"SELECT Friend FROM Friends WHERE User = '{config.currUser}'").fetchall()

  # check if they have any friends
  if len(friends) > 0:

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
      print(f"\n{i + 1}. {friend_names[friend[0]]}")
  
    # Ask user to select a friend to remove
    utility.printSeparator()
    selected_friend = input(
      f"\nEnter the number of the friend you want to remove or press {len(friends)+1} to go back: "
    )
    selected_friend = utility.choiceValidation(selected_friend, friends)
    
    if selected_friend == len(friends)+1:
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
      utility.printMessage(
        f"{friend_names[friend_to_remove]} has been removed from your friends list."
      )
      utility.quickGoBack()
      
    else:
      utility.printMessage("Friend removal cancelled.")
      utility.quickGoBack()

  else:
    utility.printMessage("You currently have no friends.")
    utility.quickGoBack()
  

# send a logged in user to pending request page if they have any pending requests
def FriendRequestNotification():
  # check if the user has any recieved requests
  received_requests = UDCursor.execute(
    f"SELECT Sender FROM FriendRequests WHERE Receiver = '{config.currUser}'"
  ).fetchall()

  if len(received_requests) > 0:
    utility.pageTitle("Your Friend Requests")
    print("\n")
    ShowRecievedRequests()