import pytest, account_testing
import sqlite3 as sql

'''
This file utilizes pytest to run unit tests for all of the
functions located in account_testing.py

account_testing.py is the exact same as account.py which
we are using in our main program besides utilizing a test
database for testing and the recursive calls to functions
are removed due to the pytest getting stuck in an
infinite recursive loop when testing the expected behavior
of fail test cases

to run the test cases type pytest -v test_account.py in your terminal

'''

# Define a fixture to set up and tear down the database for testing
@pytest.fixture
def database():
	conn = sql.connect("User_Data_Test.db")
	cursor = conn.cursor()

	# Create a table for User_Data
	try:
		cursor.execute("""
		CREATE TABLE User_Data (
			Username TEXT,
			Password TEXT
		)
	""")
	except:
		pass

	yield conn

	# Tear down the database after testing
	conn.close()


def test_usernameCreation(capfd, monkeypatch, database):
	# this will test is a unique username is inputted
	monkeypatch.setattr('builtins.input', lambda _: "test")
	result = account_testing.usernameCreation()
	assert result == "test"

	# get a username from the database to test with
	cursor = database.cursor()
	cursor.execute("SELECT Username FROM User_Data")
	user = cursor.fetchall()

	# if a username exists, test that the function returns
	# the username is taken by supplying the same username
	# as a mock input
	if user:
		monkeypatch.setattr('builtins.input', lambda _: user[0][0])
		result = account_testing.usernameCreation()
		out, err = capfd.readouterr()
		assert f'The username "{user[0][0]}" is already in use' in out

def test_passwordCreation(capfd, monkeypatch):
	# this will test if a password is too long
	monkeypatch.setattr('builtins.input', lambda _: "Testing!12345678")
	result = account_testing.passwordCreation()
	out, err = capfd.readouterr()
	assert "Password is greater than 12 characters, try removing some characters!" in out

	# this is a unit test for password not containing a special character
	monkeypatch.setattr('builtins.input', lambda _: "Testing123")
	result = account_testing.passwordCreation()
	out, err = capfd.readouterr()
	assert "Password must include a special character, try again\n" in out

	# this is a unit test for password not being long enough
	monkeypatch.setattr('builtins.input', lambda _: "Test")
	result = account_testing.passwordCreation()
	out, err = capfd.readouterr()
	assert "Password is less than 8 characters, try adding some more characters!\n" in out

	# this is a unit test for password not having capital letters
	monkeypatch.setattr('builtins.input', lambda _: "testing!123")
	result = account_testing.passwordCreation()
	out, err = capfd.readouterr()
	assert "Password must include a capital letter, try again\n" in out

	# this is a unit test for password not having a digit
	monkeypatch.setattr('builtins.input', lambda _: "Testing!")
	result = account_testing.passwordCreation()
	out, err = capfd.readouterr()
	assert "Password must include a digit, try again\n" in out

	# this is a unit test to test that all password criteria is met
	monkeypatch.setattr('builtins.input', lambda _: "Testing!123")
	result = account_testing.passwordCreation()
	assert result == "Testing!123"

def test_passwordCreation(capfd, monkeypatch):
	# this will test if a password is too long
	monkeypatch.setattr('builtins.input', lambda _: "Testing!12345678")
	result = account_testing.passwordCreation()
	out, err = capfd.readouterr()
	assert "Password is greater than 12 characters, try removing some characters!" in out

# Test case for creating a new account
def test_createAccount(monkeypatch, database):
	inputs = iter(['Test1', 'Testing!123'])
	monkeypatch.setattr('builtins.input', lambda _: next(inputs))
	result = account_testing.createAccount()

	# Check if the account was inserted into the database
	cursor = database.cursor()
	cursor.execute("SELECT COUNT(*) FROM User_Data")
	account_count = cursor.fetchone()[0]

	assert account_count >= 1

# Test case for reaching the maximum number of accounts
def test_createAccount_max_accounts(capfd, monkeypatch, database):
	# Insert 5 dummy accounts into the User_Data table
	cursor = database.cursor()
	cursor.executemany("INSERT INTO User_Data VALUES (?, ?)",
					   [("'user1'", "'Testing!123'"), ("'user2'", "'Testing!123'"), ("'user3'", "'Testing!123'"), ("'user4'", "'Testing!123'"), ("'user5'", "'Testing!123'")])

	# call the createAccount function to test if message is displayed
	inputs = iter(['Test1', 'Testing!123'])
	monkeypatch.setattr('builtins.input', lambda _: next(inputs))
	result = account_testing.createAccount()
	out, err = capfd.readouterr()
	assert "Maximum amount of accounts have been made" in out

def test_userVerification():
	# verify user credentials that exist in the db
	result = account_testing.userVerification("Test", "Testing!123")
	assert result == True

	# test case for incorrect username
	result = account_testing.userVerification("no_username", "Testing!123")
	assert result == False

	# test case for incorrect password
	result = account_testing.userVerification("Test", "testing324")
	assert result == False


# Run the tests
if __name__ == '__main__':
	pytest.main()
