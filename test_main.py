import pytest, main
from unittest import mock
import sqlite3 as sql

'''
this file contains unit tests for the various
functions found in main.py
'''

# Define a fixture to set up and tear down the database for testing
@pytest.fixture
def database():
	conn = sql.connect("User_Data_Test.db")
	cursor = conn.cursor()

	# Create a table for User_Data
	try:
		cursor.execute("""
		CREATE TABLE userData (
			Username TEXT,
			Password TEXT,
			FirstName TEXT,
			LastName TEXT
		)
	""")
	except:
		pass

	yield conn

	# Tear down the database after testing
	conn.close()

# test the calling of the main function inCollege
@mock.patch('main.gp.getpass')
def test_inCollege(password, capfd, monkeypatch, database):
	# simulate the flow of logging in and accessing every menu option and going back
	# log in,
	password.return_value = "Testing!123"
	cursor = database.cursor()
	sqlite_insert_query = """INSERT INTO userData
                          (Username, Password, FirstName, LastName)
                           VALUES
                          ('Test','Testing!123', 'Test', 'Test')"""
	cursor.execute(sqlite_insert_query)

	inputs = iter(['1', 'Test', '1', '3', '2', '2', '3', '6', '4', '5'])
	monkeypatch.setattr('builtins.input', lambda _: next(inputs))
	result = main.inCollege()
	out, err = capfd.readouterr()
	assert "You have successfully logged in" in out
	assert "Job Search" in out
	assert "Find Someone" in out
	assert "Learn a New Skill" in out
	assert "* Exited InCollege. *" in out

	# test for find someone
	inputs = iter(['4', 'Test', 'Test', '3', '5'])
	monkeypatch.setattr('builtins.input', lambda _: next(inputs))
	result = main.inCollege()
	out, err = capfd.readouterr()
	assert "They are a part of the inCollege system" in out

	# test for not finding someone
	inputs = iter(['4', 'nouser', 'Test', '5'])
	monkeypatch.setattr('builtins.input', lambda _: next(inputs))
	result = main.inCollege()
	out, err = capfd.readouterr()
	assert "They are not a part of the inCollege system" in out


	# This test that video plays when selected
	'''inputs = iter(['3', '5'])
	monkeypatch.setattr('builtins.input', lambda _: next(inputs))
	result = main.inCollege()
	out, err = capfd.readouterr()
	assert "* Video is now playing *" in out'''

	#

# test the calling of the main function inCollege
@mock.patch('main.account.login')
def test_loginAuthorization(login, capfd, monkeypatch):
	# test for correct login credentials
	login.return_value = False
	result = main.loginAuthorization("Testing", "Testing!123")
	assert result == True

	# test for incorrect login credentials
	with pytest.raises(Exception):
		result = main.loginAuthorization("Tes", "Testing!123")
		out, err = capfd.readouterr
		assert "Incorrect username/password" in out

	# test for invalid username length
	with pytest.raises(Exception):
		result = main.loginAuthorization("", "Testing!123")
		out, err = capfd.readouterr
		assert "Incorrect username/password" in out

	# test for invalid password length
	with pytest.raises(Exception):
		result = main.loginAuthorization("Test", "Testing!1235678")
		out, err = capfd.readouterr
		assert "Incorrect username/password" in out

def test_closeApp(capfd, monkeypatch):
	result = main.closeApp()
	main.closeApp()
	out, err = capfd.readouterr()
	assert "Exited InCollege." in out

def test_newUserFind(capfd, monkeypatch):
	# test that user is in incollege system and user is asked to join
	inputs = iter(['Test', 'Test', '3'])
	monkeypatch.setattr('builtins.input', lambda _: next(inputs))
	main.newUserFind()
	out, err = capfd.readouterr()
	assert "Would you like to join your friend in inCollege? Or have an account already?" in out

	# test that function returns nothing indicating user was not found
	inputs = iter(['nouser', 'Test', '3'])
	monkeypatch.setattr('builtins.input', lambda _: next(inputs))
	result = main.newUserFind()
	out, err = capfd.readouterr()
	assert result is None

@mock.patch("main.config.currUser", "Test")
@mock.patch("jobsearch.JobSearchPage")
@mock.patch('main.gp.getpass')
def test_loggedin(mock_jobsearch, password, capfd, monkeypatch):
	mock_jobsearch.return_value = "called"
	password.return_value = "Testing!123"
	# Test that logged in menu prints as expected and
	# when logging out, curuser gets set to none
	inputs = iter(['4'])
	monkeypatch.setattr('builtins.input', lambda _: next(inputs))
	result = main.loggedin()
	out, err = capfd.readouterr()
	assert "Current user: Test" in out
	assert "Press 1 for Job Search." in out
	assert main.config.currUser == "None"

@mock.patch('account.gp.getpass')
def test_createAcctPage(password, capfd, monkeypatch):
	password.return_value = "Testing!123"
	# Test that existing username is returned
	inputs = iter(["Test", "c", "5"])
	monkeypatch.setattr('builtins.input', lambda _: next(inputs))
	main.createAcctPage()
	out, err = capfd.readouterr()
	assert 'The username "Test" is already in use *' in out

def test_learnSkill(capfd, monkeypatch):
	# Test that all the menu options work and show the appropriate message.
	inputs = iter(['1', '6'])
	monkeypatch.setattr('builtins.input', lambda _: next(inputs))
	result = main.learnSkill()
	out, err = capfd.readouterr()
	assert "Learn a New Skill" in out
	assert "Under Construction." in out

	inputs = iter(['2', '6'])
	monkeypatch.setattr('builtins.input', lambda _: next(inputs))
	result = main.learnSkill()
	out, err = capfd.readouterr()
	assert "Learn a New Skill" in out
	assert "Under Construction." in out

	inputs = iter(['3', '6'])
	monkeypatch.setattr('builtins.input', lambda _: next(inputs))
	result = main.learnSkill()
	out, err = capfd.readouterr()
	assert "Learn a New Skill" in out
	assert "Under Construction." in out

	inputs = iter(['4', '6'])
	monkeypatch.setattr('builtins.input', lambda _: next(inputs))
	result = main.learnSkill()
	out, err = capfd.readouterr()
	assert "Learn a New Skill" in out
	assert "Under Construction." in out

	inputs = iter(['5', '6'])
	monkeypatch.setattr('builtins.input', lambda _: next(inputs))
	result = main.learnSkill()
	out, err = capfd.readouterr()
	assert "Learn a New Skill" in out
	assert "Under Construction." in out


# Run the tests
if __name__ == '__main__':
	pytest.main()