import pytest
import jobsearch, config
import sqlite3 as sql

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

"""
function to test the main page for jobsearch
"""
def test_JobSearchPage(capfd, monkeypatch):
  # tests that the page prints all options
  monkeypatch.setattr('builtins.input', lambda _: '3')
  result = jobsearch.JobSearchPage()
  out, err = capfd.readouterr()
  assert "Press 1 for Search for Job." in out
  assert "Press 2 for Post a Job." in out
  assert "Press 3 for Back."

  # test for searching for a job
  inputs = iter(['1', '1', '3'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = jobsearch.JobSearchPage()
  out, err = capfd.readouterr()
  assert "Under Construction." in out

  # test post job link
  inputs = iter(['2', 'c', '3'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = jobsearch.JobSearchPage()
  out, err = capfd.readouterr()
  assert "* Please enter the required details. *" in out

"""
functions that tests inputs for posting a job details. 
"""
def test_TitleInput(capfd, monkeypatch):
  # test correct input 
  inputs = iter(["Clean gym", 'y'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = jobsearch.TitleInput()
  out, err = capfd.readouterr()
  assert result == "Clean gym"

  # test incorrect inputs
  inputs = iter(["Clean gym;", 'c'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = jobsearch.TitleInput()
  out, err = capfd.readouterr()
  assert "Special characters are not allowed!" in out

  # long input
  jobsearch.cancelPost = False
  inputs = iter(["Cleangymaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 'c'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = jobsearch.TitleInput()
  out, err = capfd.readouterr()
  assert "Title is too long! Try again." in out

def test_DescInput(capfd, monkeypatch):
  # test correct input 
  jobsearch.cancelPost = False
  inputs = iter(["Clean gym at the right edge of the campus. Make sure to clean all benches, chairs, floors, and rims. Also clean the storage room and organize all of the items!", 'y'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = jobsearch.DescInput()
  out, err = capfd.readouterr()
  assert result == "Clean gym at the right edge of the campus. Make sure to clean all benches, chairs, floors, and rims. Also clean the storage room and organize all of the items!"

  # test incorrect inputs
  jobsearch.cancelPost = False
  inputs = iter(["Clean gym at the right edge of the campus. Make sure to clean all benches, chairs, floors, and rims; Also clean the storage room and organize all of the items;", 'c'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = jobsearch.DescInput()
  out, err = capfd.readouterr()
  assert "Special characters are not allowed!" in out

def test_EmpInput(capfd, monkeypatch):
  # test correct input 
  jobsearch.cancelPost = False
  inputs = iter(["John Doe", 'y'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = jobsearch.EmpInput()
  out, err = capfd.readouterr()
  assert result == "John Doe"

  # test incorrect inputs
  jobsearch.cancelPost = False
  inputs = iter(["Doe, John", 'c'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = jobsearch.EmpInput()
  out, err = capfd.readouterr()
  assert "Special characters are not allowed!" in out

def test_LocInput(capfd, monkeypatch):
  # test correct input 
  jobsearch.cancelPost = False
  inputs = iter(["Davenport, Florida 33837", 'y'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = jobsearch.LocInput()
  out, err = capfd.readouterr()
  assert result == "Davenport, Florida 33837"

  # test incorrect inputs
  jobsearch.cancelPost = False
  inputs = iter(["Davenport, Florida; 33837", 'c'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = jobsearch.LocInput()
  out, err = capfd.readouterr()
  assert "#, ;, \\, ` characters are not allowed!" in out

  jobsearch.cancelPost = False
  inputs = iter(["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 'c'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = jobsearch.LocInput()
  out, err = capfd.readouterr()
  assert "Name of Location is too long! Try again." in out

def test_SalInput(capfd, monkeypatch):
  # test correct input 
  jobsearch.cancelPost = False
  inputs = iter(["30000", 'y'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = jobsearch.SalInput()
  out, err = capfd.readouterr()
  assert result == 30000

  # test incorrect inputs
  jobsearch.cancelPost = False
  inputs = iter(["-30000", 'c'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = jobsearch.SalInput()
  out, err = capfd.readouterr()
  assert "Only positive numbers allowed." in out

def test_PostJob(capfd, monkeypatch, database):
  config.currUser = "user1"
  cursor = database.cursor()

  jobsearch.cancelPost = False
  inputs = iter(["Clean gym", 'y', "Clean gym at the right edge of the campus. Make sure to clean all benches, chairs, floors, and rims. Also clean the storage room and organize all of the items!", 'y', "John Doe", 'y', "Davenport, Florida 33837", 'y', "30000", 'y', '1'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = jobsearch.PostJob()
  out, err = capfd.readouterr()
  
  cursor.execute("DELETE FROM jobsData WHERE Issuer LIKE 'user%'")

  assert "Job successfully posted!" in out

# Run the tests
if __name__ == '__main__':
  pytest.main()