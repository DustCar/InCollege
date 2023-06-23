import friends
import pytest
import utility, config
from unittest import mock
from unittest.mock import patch
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
      Language TEXT);
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

  # test that user gets sent to SearchStudentPage
  input  = iter(['2', 'c', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(input))
  result = friends.MyFriendsPage()
  out, err = capfd.readouterr()
  assert "Your current friends are:" in out

  # test that user gets sent to SearchStudentPage
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
  INSERT INTO FriendRequests VALUES ('user1', 'user2');
  INSERT INTO FriendRequests VALUES ('user4', 'user1');
  INSERT INTO Friends VALUES ('user3', 'user1');
  INSERT INTO Friends VALUES ('user1', 'user3');
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




# Run the tests
if __name__ == '__main__':
	pytest.main()