'''
this file contains unit tests for the various
functions found in findsomeone.py
'''

import pytest, findsomeone
from unittest.mock import patch
import sqlite3 as sql

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

def test_NameInput(capfd, monkeypatch):
	# test that function capitalizes input
	monkeypatch.setattr('builtins.input', lambda _: "test")
	result = findsomeone.NameInput("first")
	assert result == "Test"

	# test that special characters get caught
	inputs = iter(["test!", "testing"])
	monkeypatch.setattr('builtins.input', lambda _: next(inputs))
	result = findsomeone.NameInput("first")
	out, err = capfd.readouterr()
	assert result == "Testing"
	assert "Special characters are not allowed!" in out

	# test that length of input is caught
	inputs = iter(["Thisiswaytoolognofanameandisusedtotestthelengthoftheinputischecked", "testing"])
	monkeypatch.setattr('builtins.input', lambda _: next(inputs))
	result = findsomeone.NameInput("first")
	out, err = capfd.readouterr()
	assert result == "Testing"
	assert "name is too long! Try again." in out

	# test that integer inputs dont break the code
	monkeypatch.setattr('builtins.input', lambda _: "1234")
	result = findsomeone.NameInput("first")
	assert result == "1234"

@patch("findsomeone.NameInput")
def test_SearchStudent(mock_name, capfd, database):
	# Test case for searching for a valid student in the database
	mock_name.return_value = "Test"
	cursor = database.cursor()
	sqlite_insert_query = """INSERT INTO userData
                          (Username, Password, FirstName, LastName)
                           VALUES
                          ('Test','Testing!123', 'Test', 'Test')"""
	cursor.execute(sqlite_insert_query)
	result = findsomeone.SearchStudent()
	out, err = capfd.readouterr()
	assert "They are a part of the inCollege system" in out

	# test case that a non existing student does not return that they are a part of the system
	mock_name.return_value = "Testing"
	result = findsomeone.SearchStudent()
	out, err = capfd.readouterr()
	assert "They are not a part of the inCollege system" in out


def test_FindSomeonePage(capfd, monkeypatch):
	# check that loop breaks when 2 is inputted

	monkeypatch.setattr('builtins.input', lambda _: "2")
	result = findsomeone.FindSomeonePage()
	assert result is None

	# input 1 for menu and test going back feature
	try:
		inputs = iter(["1", "2", "2"])
		monkeypatch.setattr('builtins.input', lambda _: next(inputs))
		result = findsomeone.FindSomeonePage()
	except StopIteration:
		out, err = capfd.readouterr()
		assert "Search for a fellow Student" in out


# Run the tests
if __name__ == '__main__':
	pytest.main()