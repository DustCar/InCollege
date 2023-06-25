import pytest
import jobsearch

@pytest.fixture
def database():
  conn = sql.connect(config.database)
  cursor = conn.cursor()

	# Create a table for User_Data
  try:
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS userData(Username TEXT, Password TEXT,
			FirstName TEXT,
			LastName TEXT,
      University TEXT,
      Major TEXT,
      EmailFeat TEXT,
      SMSFeat TEXT,
      TargetAdFeat TEXT,
      Language TEXT, UNIQUE (Username, FirstName, LastName));
    CREATE TABLE IF NOT EXISTS jobsData (Issuer VARCHAR(25), 
      Title VARCHAR(100), 
      Description TEXT, 
      Employer VARCHAR(25), 
      Location VARCHAR(255), 
      Salary INT);
    """)
  except:
    pass

  yield conn

	# Tear down the database after testing
  conn.close()

def test_JobSearchPage(capfd, monkeypatch):
  pass

# Run the tests
if __name__ == '__main__':
  pytest.main()