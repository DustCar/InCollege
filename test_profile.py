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
Title VARCHAR(50), 
University TEXT,
Major TEXT,
years_attended TEXT,
About TEXT,
Published INT, UNIQUE (User));
    CREATE TABLE IF NOT EXISTS Experiences(e_id integer primary key autoincrement,
User TEXT, 
Title VARCHAR(50),
Employer TEXT,
Date_started DATE,
Date_ended DATE,
Location TEXT,
Description TEXT);
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
  INSERT OR IGNORE INTO Profiles VALUES ('user1', '', 'University of South Florida', 'Computer Science', '', '', 0);""")
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
  INSERT OR IGNORE INTO Profiles VALUES ('user1', '', 'University of South Florida', 'Computer Science', '', '', 1);
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
  INSERT OR IGNORE INTO Profiles VALUES ('user1', '4th Year Computer Science student', 'University of South Florida', 'Computer Science', '', 'Aspiring game developer', 0);
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

def test_ManageTitle(capfd, monkeypatch, database):
  config.currUser = "user1"
  cursor = database.cursor()

  cursor.executescript("""DELETE FROM Profiles WHERE User LIKE 'user%';
  INSERT INTO Profiles (User, University, Major, Published)
VALUES ('user1', 'University of South Florida', 'Computer Science', 0);
  """)
  
  # test menu option is set to create when no title has been set
  inputs = iter(['1', '1', 'c', '7', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = profile.MyProfile()
  out, err = capfd.readouterr()
  assert "Press 1 for Create Your Profile Title." in out

  # test creating a new title
  inputs = iter(['1', '1', '3rd year Computer Science student', 'y', '7', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = profile.MyProfile()
  title = profile.getColumn("Title")
  out, err = capfd.readouterr()
  assert title == "3rd year Computer Science student"

  # test menu option changing title option to 'Edit' and change title
  inputs = iter(['1', '1', 'y', '3rd year Computer Science developer', 'y', '7', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = profile.MyProfile()
  title = profile.getColumn("Title")
  out, err = capfd.readouterr()
  assert "Press 1 for Edit Your Profile Title."
  assert title == "3rd year Computer Science developer"

  # test cancelling an edit
  inputs = iter(['1', '1', 'y', '3rd year Computer Engineering student', 'n', '7', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = profile.MyProfile()
  title = profile.getColumn("Title")
  out, err = capfd.readouterr()
  assert title == "3rd year Computer Science developer"

def test_ManageAbout(capfd, monkeypatch, database):
  config.currUser = "user1"
  cursor = database.cursor()

  cursor.executescript("""DELETE FROM Profiles WHERE User LIKE 'user%';
  INSERT INTO Profiles (User, University, Major, Published)
VALUES ('user1', 'University of South Florida', 'Computer Science', 0);
  """)
  
  # test menu option is set to create when no about me has been set
  inputs = iter(['1', '5', 'c', '7', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = profile.MyProfile()
  out, err = capfd.readouterr()
  assert "Press 5 for Create Your About me." in out

  # test creating a new title
  inputs = iter(['1', '5', 'Hello, my name is userone and I am a 3rd year computer science student at USF. I hope to become a future software developer at Tesla in a few years. I am very interested in the technology of the latest Tesla cars and hope to one day work on them myself.', 'y', '7', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = profile.MyProfile()
  about = profile.getColumn("About")
  out, err = capfd.readouterr()
  assert about == "Hello, my name is userone and I am a 3rd year computer science student at USF. I hope to become a future software developer at Tesla in a few years. I am very interested in the technology of the latest Tesla cars and hope to one day work on them myself."

  # test menu option changing title option to 'Edit' and change title
  inputs = iter(['1', '5', 'y', 'Hello, my name is userone and I am a computer science student at USF onto my last year for a Bachelors. I hope to be a software developer with the focus on EVs, or electric vehicles. I aspire to work on the latest systems for EVs and potentially create a new system for them.', 'y', '7', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = profile.MyProfile()
  about = profile.getColumn("About")
  out, err = capfd.readouterr()
  assert "Press 1 for Edit Your About me."
  assert about == "Hello, my name is userone and I am a computer science student at USF onto my last year for a Bachelors. I hope to be a software developer with the focus on EVs, or electric vehicles. I aspire to work on the latest systems for EVs and potentially create a new system for them."

  # test cancelling an edit
  inputs = iter(['1', '5', 'y', 'I think I\'ll just remove the about me section that I worked to create.', 'n', '7', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = profile.MyProfile()
  about = profile.getColumn("About")
  out, err = capfd.readouterr()
  assert about == "Hello, my name is userone and I am a computer science student at USF onto my last year for a Bachelors. I hope to be a software developer with the focus on EVs, or electric vehicles. I aspire to work on the latest systems for EVs and potentially create a new system for them."
  