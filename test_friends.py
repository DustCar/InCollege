import pytest
import config
from unittest import mock
from unittest.mock import patch
import friends
import sqlite3 as sql

# Define a fixture to set up and tear down the database for testing
@pytest.fixture
def database():
  conn = sql.connect(config.database)
  cursor = conn.cursor()

	# Create a table for User_Data
  try:
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Friends(User, Friend);
    CREATE TABLE IF NOT EXISTS FriendRequests(Sender, Receiver);
    CREATE TABLE IF NOT EXISTS userData(Username TEXT,
Password TEXT,
FirstName TEXT,
LastName TEXT,
EmailFeat TEXT,
SMSFeat TEXT,
TargetAdFeat TEXT,
Language TEXT, UNIQUE (Username, FirstName, LastName));
    CREATE TABLE IF NOT EXISTS Profiles(User TEXT,
Title VARCHAR(50), 
University TEXT,
Major TEXT,
About TEXT,
Published INT, UNIQUE (User));
    """)
  except:
    pass

  yield conn

	# Tear down the database after testing
  conn.close()

"""
function to test functionality of friends page menu and links
"""
def test_MyFriendsPage(capfd, monkeypatch):
  # test that MyFriendsPage prints out appropriate links
  input = '4'
  monkeypatch.setattr('builtins.input', lambda _: input)
  result = friends.MyFriendsPage()
  out, err = capfd.readouterr()
  assert "Search For Students" in out
  assert "Show My Network" in out
  assert "Show Pending Requests" in out
  assert "Back" in out

  # test that user gets sent to SearchStudentPage
  input  = iter(['1', '4', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(input))
  result = friends.MyFriendsPage()
  out, err = capfd.readouterr()
  assert "Search by Last Name" in out
  assert "Search by University" in out
  assert "Search by Major" in out
  assert "Back" in out

  # test that user gets sent to ShowMyNetworkPage
  input  = iter(['2', '3', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(input))
  result = friends.MyFriendsPage()
  out, err = capfd.readouterr()
  assert "Press 1 for View Friends Profiles.\nPress 2 for Remove Friends.\nPress 3 for Back." in out

  # test that user gets sent to ShowMyPendingRequestsPage
  input  = iter(['3', '1', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(input))
  result = friends.MyFriendsPage()
  out, err = capfd.readouterr()
  assert "Sent Friend Requests" in out
  assert "Received Friend Requests" in out
  
"""
function to test all cases for sending a friend request
"""
def test_CanSendRequest(capfd, monkeypatch, database):
  # insert test users into user table
  config.currUser = "user1"
  cursor = database.cursor()

  cursor.executescript("""
  INSERT INTO FriendRequests VALUES ('user1', 'user2');
  INSERT INTO FriendRequests VALUES ('user4', 'user1');
  INSERT INTO Friends VALUES ('user3', 'user1');
  INSERT INTO Friends VALUES ('user1', 'user3');
  INSERT OR IGNORE INTO userData VALUES ('user1', 'userpass@1', 'Useronef', 'Useronel', 'ON', 'ON', 'ON', 'English');
  INSERT OR IGNORE INTO Profiles VALUES ('user1', '', 'University of South Florida', 'Computer Science', '', 0);
  INSERT OR IGNORE INTO userData VALUES ('user2', 'userpass@2', 'Usertwof', 'Usertwol', 'ON', 'ON', 'ON', 'English');
  INSERT OR IGNORE INTO Profiles VALUES ('user2', '', 'University of North Florida', 'Computer Engineering', '', 0);
  INSERT OR IGNORE INTO userData VALUES ('user3', 'userpass@3', 'Userthreef', 'Userthreel', 'ON', 'ON', 'ON', 'English');
  INSERT OR IGNORE INTO Profiles VALUES ('user3', '', 'University of Florida', 'Accounting', '', 0);
  INSERT OR IGNORE INTO userData VALUES ('user4', 'userpass@4', 'Userfourf', 'Userfourl', 'ON', 'ON', 'ON', 'English');
  INSERT OR IGNORE INTO Profiles VALUES ('user4', '', 'Florida State University', 'Mechanical Engineering', '', 0);
  """)
  
  # test sending a request to ownself
  result = friends.CanSendRequest("user1")
  out, err = capfd.readouterr()
  assert result == False
  assert "You can't send a friend request to yourself." in out

  # test sending a request when a request was already sent
  result = friends.CanSendRequest("user2")
  out, err = capfd.readouterr()
  assert result == False
  assert "You have already sent a friend request to this user." in out

  # test sending a request when the user received a request already
  result = friends.CanSendRequest("user4")
  out, err = capfd.readouterr()
  assert result == False
  assert "This user has already sent you a friend request." in out

  # test sending a request when the user received a request already
  result = friends.CanSendRequest("user3")
  out, err = capfd.readouterr()
  assert result == False
  assert "You are already friends with this user." in out

"""
function to test search by functions
"""
def test_SearchStudentLN(capfd, monkeypatch, database):
  config.currUser = "user1"
  
  # test searching with a match
  inputs = iter(['Usertwol', 'c', 'n', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = friends.SearchStudentLN()
  out, err = capfd.readouterr()
  assert "Matches Found: 1" in out
  assert "Usertwof Usertwol, University of North Florida, Computer Engineering" in out
  
  # test searching without any matches
  inputs = iter(['Userfivel', 'n', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = friends.SearchStudentLN()
  out, err = capfd.readouterr()
  assert "No Matches Found" in out

  # test sending a request
  config.currUser = "user2"
  inputs = iter(['userthreel', '1', 'y', 'userthreel', '1', 'c', 'n'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = friends.SearchStudentLN()
  out, err = capfd.readouterr()
  assert "You have sent a friend request to user3" in out
  assert "You have already sent a friend request to this user." in out
  

def test_SearchStudentM(capfd, monkeypatch, database):
  config.currUser = "user1"
  
  # test searching with a match
  inputs = iter(['Accounting', 'c', 'n', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = friends.SearchStudentM()
  out, err = capfd.readouterr()
  assert "Matches Found: 1" in out
  assert "Userthreef Userthreel, University of Florida, Accounting" in out
  
  # test searching without any matches
  inputs = iter(['Business', 'n', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = friends.SearchStudentM()
  out, err = capfd.readouterr()
  assert "No Matches Found" in out

def test_SearchStudentU(capfd, monkeypatch, database):
  config.currUser = "user1"
  
  # test searching with a match
  inputs = iter(['University of North Florida', 'c', 'n', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = friends.SearchStudentU()
  out, err = capfd.readouterr()
  assert "Matches Found: 1" in out
  assert "Usertwof Usertwol, University of North Florida, Computer Engineering" in out
  
  # test searching without any matches
  inputs = iter(['University of Miami', 'n', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = friends.SearchStudentU()
  out, err = capfd.readouterr()
  assert "No Matches Found" in out

def test_ShowMyPendingRequestsPage(capfd, monkeypatch, database):
  config.currUser = "user1"

  # test if friend requests are showing
  inputs = iter(['c', '1'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = friends.ShowMyPendingRequestsPage()
  out, err = capfd.readouterr()
  assert "* Sent Friend Requests *\n---\n1: user2" in out
  assert "* Received Friend Requests *\n---\n1: user4" in out

  # test declining a friend request
  inputs = iter(['d1', 'c', '1'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = friends.ShowMyPendingRequestsPage()
  out, err = capfd.readouterr()
  assert "You have declined the friend request from user4." in out
  
  # test accepting a friend request
  config.currUser = "user2"
  inputs = iter(['1', '1'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = friends.ShowMyPendingRequestsPage()
  out, err = capfd.readouterr()
  assert "You are now friends with user1." in out

  # test showing no requests
  config.currUser = "user4"
  monkeypatch.setattr('builtins.input', lambda _: '1')
  result = friends.ShowMyPendingRequestsPage()
  out, err = capfd.readouterr()
  assert "You have no pending requests." in out
  assert "You have no incoming friend requests." in out


def test_RemoveFriend(capfd, monkeypatch, database):
  config.currUser = "user1"

  cursor = database.cursor()
  
  # test showing current friends, also covering ShowMyNetworkPage
  monkeypatch.setattr('builtins.input', lambda _: '1')
  result = friends.RemoveFriend()
  out, err = capfd.readouterr()
  assert "1. Userthreef Userthreel" in out
  assert "2. Usertwof Usertwol" in out

  # test removing a friend but cancelling
  inputs = iter(['1', 'n', '1'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = friends.RemoveFriend()
  out, err = capfd.readouterr()
  assert "Friend removal cancelled." in out

  # test removing a friend and confirming
  inputs = iter(['1', 'y', '1'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = friends.RemoveFriend()
  out, err = capfd.readouterr()
  cursor.executescript("""
  DELETE FROM FriendRequests WHERE Sender LIKE 'user%';
  DELETE FROM Friends WHERE User LIKE 'user%';
  DELETE FROM Profiles WHERE User LIKE 'user%';
  DELETE FROM userData WHERE Username LIKE 'user%';
  """)
  assert "Userthreef Userthreel has been removed from your friends list." in out
  



# Run the tests
if __name__ == '__main__':
  pytest.main()