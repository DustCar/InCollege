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
    """)
  except:
    pass

  yield conn

	# Tear down the database after testing
  conn.close()

def test_MyProfile(capfd, monkeypatch):
  pass