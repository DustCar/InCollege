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
    CREATE TABLE IF NOT EXISTS userData(Username TEXT, Password TEXT,
			FirstName TEXT,
			LastName TEXT,
      University TEXT,
      Major TEXT,
      EmailFeat TEXT,
      SMSFeat TEXT,
      TargetAdFeat TEXT,
      Language TEXT, UNIQUE (Username, FirstName, LastName));
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
  input  = iter(['2', 'c', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(input))
  result = friends.MyFriendsPage()
  out, err = capfd.readouterr()
  assert "Your current friends are:" in out

  # test that user gets sent to ShowMyPendingRequestsPage
  input  = iter(['3', 'c', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(input))
  result = friends.MyFriendsPage()
  out, err = capfd.readouterr()
  assert "Friend requests you've sent that have not been accepted yet:" in out
  assert "Friend requests you've received that you haven't accepted yet:" in out
  
"""
function to test all cases for sending a friend request
"""
def test_CanSendRequest(capfd, monkeypatch, database):
  # insert test users into user table
  config.currUser = "user1"
  cursor = database.cursor()

  cursor.executescript("""
  DELETE FROM FriendRequests WHERE Sender LIKE 'user%';
  DELETE FROM Friends WHERE User LIKE 'user%';
  INSERT INTO FriendRequests VALUES ('user1', 'user2');
  INSERT INTO FriendRequests VALUES ('user4', 'user1');
  INSERT INTO Friends VALUES ('user3', 'user1');
  INSERT INTO Friends VALUES ('user1', 'user3');
  INSERT OR IGNORE INTO userData VALUES ('user1', 'userpass@1', 'Useronef', 'Useronel', 'University of South Florida', 'Computer Science', 'ON', 'ON', 'ON', 'English');
  INSERT OR IGNORE INTO userData VALUES ('user2', 'userpass@2', 'Usertwof', 'Usertwol', 'University of North Florida', 'Computer Engineering', 'ON', 'ON', 'ON', 'English');
  INSERT OR IGNORE INTO userData VALUES ('user3', 'userpass@3', 'Userthreef', 'Userthreel', 'University of Florida', 'Accounting', 'ON', 'ON', 'ON', 'English');
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
  inputs = iter(['1', 'Usertwol', 'c', 'n', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = friends.SearchStudentPage()
  out, err = capfd.readouterr()
  assert "Matches Found: 1" in out
  assert "Usertwof Usertwol, University of North Florida, Computer Engineering" in out
  
  # test searching without any matches
  inputs = iter(['1', 'Userfourl', 'n', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = friends.SearchStudentPage()
  out, err = capfd.readouterr()
  assert "No Matches Found" in out

def test_RemoveFriend(capfd, monkeypatch, database):
  
  pass



# Run the tests
if __name__ == '__main__':
  pytest.main()