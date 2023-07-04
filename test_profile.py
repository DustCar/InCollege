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
    CREATE TABLE IF NOT EXISTS userData(Username TEXT, Password TEXT, FirstName TEXT, LastName TEXT, 
EmailFeat TEXT, SMSFeat TEXT, TargetAdFeat TEXT,
Language TEXT, UNIQUE (Username, FirstName, LastName));
    CREATE TABLE IF NOT EXISTS Profiles(User TEXT,
Title VARCHAR(50), University TEXT, Major TEXT,
years_attended TEXT, About TEXT, Published INT, UNIQUE (User));
    CREATE TABLE IF NOT EXISTS Experiences(e_id integer primary key autoincrement, User TEXT, Title VARCHAR(50),
Employer TEXT, Date_started DATE, Date_ended DATE, Location TEXT, Description TEXT);
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
  INSERT OR IGNORE INTO Profiles VALUES ('user1', '', 'University Of South Florida', 'Computer Science', '', '', 0);""")
  # test page with user profile not published yet
  monkeypatch.setattr('builtins.input', lambda _: '4')
  profile.MyProfile()
  out, err = capfd.readouterr()
  assert "Press 1 for Create/Edit My Profile." in out
  assert "Press 2 for View My Profile." in out
  assert "Press 3 for Publish My Profile." in out
  assert "Press 4 for Back." in out

  # test page with user profile already published
  cursor.executescript("""
  DELETE FROM Profiles WHERE User LIKE 'user%';
  INSERT OR IGNORE INTO Profiles VALUES ('user1', '', 'University Of South Florida', 'Computer Science', '', '', 1);
  """)
  monkeypatch.setattr('builtins.input', lambda _: '4')
  profile.MyProfile()
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
  INSERT OR IGNORE INTO Profiles VALUES ('user1', '4th Year Computer Science student', 'University Of South Florida', 'Computer Science', '', 'Aspiring game developer', 0);
  """)
  # test getColumn with title
  result = profile.getColumn("Title")
  out, err = capfd.readouterr()
  assert result == "4th Year Computer Science student"
  
  # test getColumn with university
  result = profile.getColumn("University")
  out, err = capfd.readouterr()
  assert result == "University Of South Florida"

  # test getColumn with major
  result = profile.getColumn("Major")
  out, err = capfd.readouterr()
  assert result == "Computer Science"

  # test getColumn with about
  result = profile.getColumn("About")
  out, err = capfd.readouterr()
  assert result == "Aspiring game developer"

"""
function that tests the create/edit title option
"""
def test_ManageTitle(capfd, monkeypatch, database):
  config.currUser = "user1"
  cursor = database.cursor()

  cursor.executescript("""DELETE FROM Profiles WHERE User LIKE 'user%';
  INSERT INTO Profiles (User, University, Major, Published)
VALUES ('user1', 'University Of South Florida', 'Computer Science', 0);
  """)
  
  # test menu option is set to create when no title has been set
  inputs = iter(['1', '1', 'c', '5', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  profile.MyProfile()
  out, err = capfd.readouterr()
  assert "Press 1 for Create Your Profile Title." in out

  # test creating a new title
  inputs = iter(['1', '1', '3rd year Computer Science student', 'y', '5', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  profile.MyProfile()
  title = profile.getColumn("Title")
  out, err = capfd.readouterr()
  assert title == "3rd year Computer Science student"

  # test menu option changing title option to 'Edit' and change title
  inputs = iter(['1', '1', 'y', '3rd year Computer Science developer', 'y', '5', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  profile.MyProfile()
  title = profile.getColumn("Title")
  out, err = capfd.readouterr()
  assert "Press 1 for Edit Your Profile Title."
  assert title == "3rd year Computer Science developer"

  # test cancelling an edit
  inputs = iter(['1', '1', 'y', '3rd year Computer Engineering student', 'n', '5', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  profile.MyProfile()
  title = profile.getColumn("Title")
  out, err = capfd.readouterr()
  assert title == "3rd year Computer Science developer"

"""
function that tests the create/edit the about me option
"""
def test_ManageAbout(capfd, monkeypatch, database):
  config.currUser = "user1"
  cursor = database.cursor()

  cursor.executescript("""DELETE FROM Profiles WHERE User LIKE 'user%';
  INSERT INTO Profiles (User, University, Major, Published)
VALUES ('user1', 'University Of South Florida', 'Computer Science', 0);
  """)
  
  # test menu option is set to create when no about me has been set
  inputs = iter(['1', '3', 'c', '5', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  profile.MyProfile()
  out, err = capfd.readouterr()
  assert "Press 3 for Create Your About me." in out

  # test creating a new title
  inputs = iter(['1', '3', 'Hello, my name is userone and I am a 3rd year computer science student at USF. I hope to become a future software developer at Tesla in a few years. I am very interested in the technology of the latest Tesla cars and hope to one day work on them myself.', 'y', '5', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  profile.MyProfile()
  about = profile.getColumn("About")
  out, err = capfd.readouterr()
  assert about == "Hello, my name is userone and I am a 3rd year computer science student at USF. I hope to become a future software developer at Tesla in a few years. I am very interested in the technology of the latest Tesla cars and hope to one day work on them myself."

  # test menu option changing title option to 'Edit' and change title
  inputs = iter(['1', '3', 'y', 'Hello, my name is userone and I am a computer science student at USF onto my last year for a Bachelors. I hope to be a software developer with the focus on EVs, or electric vehicles. I aspire to work on the latest systems for EVs and potentially create a new system for them.', 'y', '5', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  profile.MyProfile()
  about = profile.getColumn("About")
  out, err = capfd.readouterr()
  assert "Press 1 for Edit Your About me."
  assert about == "Hello, my name is userone and I am a computer science student at USF onto my last year for a Bachelors. I hope to be a software developer with the focus on EVs, or electric vehicles. I aspire to work on the latest systems for EVs and potentially create a new system for them."

  # test cancelling an edit
  inputs = iter(['1', '3', 'y', 'I think I\'ll just remove the about me section that I worked to create.', 'n', '5', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  profile.MyProfile()
  about = profile.getColumn("About")
  out, err = capfd.readouterr()
  assert about == "Hello, my name is userone and I am a computer science student at USF onto my last year for a Bachelors. I hope to be a software developer with the focus on EVs, or electric vehicles. I aspire to work on the latest systems for EVs and potentially create a new system for them."

"""
function that tests the edit university option
"""
def test_ManageUniversity(capfd, monkeypatch, database):
  config.currUser = "user1"
  cursor = database.cursor()

  cursor.executescript("""DELETE FROM Profiles WHERE User LIKE 'user%';
  INSERT INTO Profiles (User, University, Major, Published)
VALUES ('user1', 'University Of South Florida', 'Computer Science', 0);
  """)
  
  # test changing university
  inputs = iter(['1', '2', '1', 'y', 'University of Florida', 'y', '4', '5', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  profile.MyProfile()
  university = profile.getColumn("University")
  out, err = capfd.readouterr()
  assert university == "University Of Florida"

  # test changing university but then cancelling
  inputs = iter(['1', '2', '1', 'y', 'University of Miami', 'n', '4', '5', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  profile.MyProfile()
  university = profile.getColumn("University")
  out, err = capfd.readouterr()
  assert university == "University Of Florida"

"""
function that tests the edit major option
"""
def test_ManageMajor(capfd, monkeypatch, database):
  config.currUser = "user1"
  cursor = database.cursor()

  cursor.executescript("""DELETE FROM Profiles WHERE User LIKE 'user%';
  INSERT INTO Profiles (User, University, Major, Published)
VALUES ('user1', 'University of South Florida', 'Computer Science', 0);
  """)
  
  # test changing major
  inputs = iter(['1', '2', '2', 'y', 'Computer Engineering', 'y', '4', '5', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  profile.MyProfile()
  major = profile.getColumn("Major")
  out, err = capfd.readouterr()
  assert major == "Computer Engineering"

  # test changing major but then cancelling
  inputs = iter(['1', '2', '2', 'y', 'Accounting', 'n', '4', '5', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  profile.MyProfile()
  major = profile.getColumn("Major")
  out, err = capfd.readouterr()
  assert major == "Computer Engineering"

"""
function that tests functions dealing with experiences
"""
def test_ManageExperience(capfd, monkeypatch, database):
  config.currUser = "user1"
  cursor = database.cursor()

  cursor.executescript("""
  DELETE FROM Experiences WHERE User LIKE 'user%';
  """)

  # test menu with no experiences
  inputs = iter(['1', '4', '2', '5', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  profile.MyProfile()
  out, err = capfd.readouterr()
  assert "Press 1 for Add an experience.\nPress 2 for Back." in out

  # test adding title then cancelling (this test goes for all other options as well)
  inputs = iter(['1', '4', '1', 'Manager', 'c', '2', '1', '7', '2', '4', '5', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  profile.MyProfile()
  out, err = capfd.readouterr()
  assert "Press 1 for Add an experience.\nPress 2 for Edit an Experience.\nPress 3 for Remove an Experience." in out
  assert "Press 1 to edit experience titled: 'Manager'" in out
  assert "You are editing the job titled: 'Manager'" in out
  assert "Press 1 for Edit Title." in out

  # test editing title (this test goes for all other options as well)
  inputs = iter(['1', '4', '2', '1', '1', 'y', 'Cashier', 'y', '7', '2', '4', '5', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  profile.MyProfile()
  out, err = capfd.readouterr()
  assert "Press 1 to edit experience titled: 'Manager'" in out
  assert "You are editing the job titled: 'Manager'" in out
  assert "Press 1 for Edit Title." in out
  assert "You are editing the job titled: 'Cashier'" in out

  # test menu when three jobs are posted
  inputs = iter(['1', '4', '1', 'Stocker', 'c', '1', 'Software Maintenance', 'c', '3', '5', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  profile.MyProfile()
  out, err = capfd.readouterr()
  assert "Press 1 for Edit an Experience.\nPress 2 for Remove an Experience." in out

  # test removing an experience (when experiences are full)
  inputs = iter(['1', '4', '2', '3', 'y', '1', '4', '5', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  profile.MyProfile()
  out, err = capfd.readouterr()
  assert "This experience has been deleted." in out
  assert "Press 1 for Add an experience.\nPress 2 for Edit an Experience.\nPress 3 for Remove an Experience." in out

  # test if menu reverts after deleting all experiences
  inputs = iter(['1', '4', '3', '1', 'y', '1', '3', '1', 'y', '1', '2', '5', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  profile.MyProfile()
  out, err = capfd.readouterr()
  assert "This experience has been deleted." in out
  assert "Press 1 for Add an experience.\nPress 2 for Back." in out

  # test adding a full experience
  inputs = iter(['1', '4', '1', 'Software Maintenance', 'John Doe', '03-24-2021', '06-10-2022', 'Tampa, FL', 'Maintained software at Ubisoft including servers, account managing, and transactions.', '2', '1', '7', '2', '4', '5', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  profile.MyProfile()
  out, err = capfd.readouterr()
  assert "Press 1 for Edit Title.\nPress 2 for Edit Employer.\nPress 3 for Edit Date Started.\nPress 4 for Edit Date Ended.\nPress 5 for Edit Location.\nPress 6 for Edit Description." in out

  # test to see if previous test saved in db
  experience = cursor.execute("SELECT Title, Employer, Date_started, Date_ended, Location, Description FROM Experiences WHERE User = 'user1' AND Title = 'Software Maintenance';").fetchone()
  assert experience[0] == "Software Maintenance"
  assert experience[1] == "John Doe"
  assert experience[2] == "03-24-2021"
  assert experience[3] == "06-10-2022"
  assert experience[4] == "Tampa, FL"
  assert experience[5] == "Maintained software at Ubisoft including servers, account managing, and transactions."