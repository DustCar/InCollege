import sqlite3 as sql
import profile, pytest, config

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
Title VARCHAR(25), 
University TEXT,
Major TEXT,
About TEXT,
Published INT, UNIQUE (User));
    CREATE TABLE IF NOT EXISTS Experiences(User TEXT, 
Title VARCHAR(25),
Employer TEXT,
Date_started DATE,
Date_ended DATE,
Location TEXT,
Description TEXT, UNIQUE (User));
  """)
  except:
    pass

  yield conn

	# Tear down the database after testing
  conn.close()

"""
function that tests if the myprofile page prints the correct options
"""
def test_MyProfile(capfd, monkeypatch, database):
  config.currUser = "user1"
  cursor = database.cursor()
  cursor.executescript("""
  DELETE FROM Profiles WHERE User LIKE 'user%';
  INSERT OR IGNORE INTO Profiles VALUES ('user1', '', 'University of South Florida', 'Computer Science', '', 0);""")
  # test page with user profile not published yet
  monkeypatch.setattr('builtins.input', lambda _: '4')
  result = profile.MyProfile()
  out, err = capfd.readouterr()
  assert "Press 1 for Create/Edit My Profile." in out
  assert "Press 2 for View My Profile." in out
  assert "Press 3 for Publish My Profile." in out
  assert "Press 4 for Back." in out

  # test page with user profile already published
  cursor.executescript("""
  DELETE FROM Profiles WHERE User LIKE 'user%';
  INSERT OR IGNORE INTO Profiles VALUES ('user1', '', 'University of South Florida', 'Computer Science', '', 1);
  """)
  monkeypatch.setattr('builtins.input', lambda _: '4')
  result = profile.MyProfile()
  out, err = capfd.readouterr()
  assert "Press 1 for Create/Edit My Profile." in out
  assert "Press 2 for View My Profile." in out
  assert "Press 3 for Unpublish My Profile." in out
  assert "Press 4 for Back." in out

"""
functions that tests some utility functions used in profile
"""
def test_getColumn(capfd, monkeypatch, database):
  config.currUser = "user1"
  cursor = database.cursor()
  cursor.executescript("""
  DELETE FROM Profiles WHERE User LIKE 'user%';
  INSERT OR IGNORE INTO Profiles VALUES ('user1', '4th Year Computer Science student', 'University of South Florida', 'Computer Science', 'Aspiring game developer', 0);
  """)
  # test getColumn with title
  result = profile.getColumn("Title")
  out, err = capfd.readouterr()
  assert result == "4th Year Computer Science student"
  
  # test getColumn with university
  result = profile.getColumn("University")
  out, err = capfd.readouterr()
  assert result == "University of South Florida"

  # test getColumn with major
  result = profile.getColumn("Major")
  out, err = capfd.readouterr()
  assert result == "Computer Science"

  # test getColumn with about
  result = profile.getColumn("About")
  out, err = capfd.readouterr()
  assert result == "Aspiring game developer"
  