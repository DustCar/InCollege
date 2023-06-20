# imports
import pytest
import generallinks, implinks, main
import utility, config
from unittest import mock
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
		CREATE TABLE userData(
			Username TEXT,
			Password TEXT,
			FirstName TEXT,
			LastName TEXT,
      EmailFeat TEXT,
      SMSFeat TEXT,
      TargetAdFeat TEXT,
      Language TEXT)
      """)
	except:
		pass

	yield conn

	# Tear down the database after testing
	conn.close()


""" 
function to test that the General link and
its sublinks are displaying the correct info
for a guest
"""
def test_generalGuest(capfd, monkeypatch):
  # test that General displays the appropriate links
  input = '8'
  monkeypatch.setattr('builtins.input', lambda _: input)
  result = generallinks.GeneralLinksPage()
  out, err = capfd.readouterr()
  assert "Sign Up" in out
  assert "Help Center" in out
  assert "About" in out
  assert "Press" in out
  assert "Blog" in out
  assert "Careers" in out
  assert "Developers" in out
  
  # test that Sign Up leads to the account creation page
  inputs = iter(['1', 'c', '8'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = generallinks.GeneralLinksPage()
  out, err = capfd.readouterr()
  assert "Create An Account" in out
  assert "PASSWORD REQUIREMENTS" in out

  # test that Help Center gives appropriate info
  inputs = iter(['2', '1', '8'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = generallinks.GeneralLinksPage()
  out, err = capfd.readouterr()
  assert "Help Center" in out
  assert "We're here to help" in out
  assert "Back" in out

  # test that About gives appropriate info
  inputs = iter(['3', '1', '8'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = generallinks.GeneralLinksPage()
  out, err = capfd.readouterr()
  assert "About" in out
  assert "In College: Welcome to In College"
  assert "Back" in out

  # test that Press gives appropriate info
  inputs = iter(['4', '1', '8'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = generallinks.GeneralLinksPage()
  out, err = capfd.readouterr()
  assert "Press" in out
  assert "In College Pressroom"
  assert "Back" in out

  # test that Blog gives appropriate info
  inputs = iter(['5', '1', '8'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = generallinks.GeneralLinksPage()
  out, err = capfd.readouterr()
  assert "Under Construction." in out
  assert "Back" in out

  # test that Careers gives appropriate info
  inputs = iter(['6', '1', '8'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = generallinks.GeneralLinksPage()
  out, err = capfd.readouterr()
  assert "Under Construction." in out
  assert "Back" in out

  # test that Developers gives appropriate info
  inputs = iter(['7', '1', '8'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = generallinks.GeneralLinksPage()
  out, err = capfd.readouterr()
  assert "Under Construction." in out
  assert "Back" in out


""" 
function to test that the General link and
its sublinks are displaying the correct info
for a signed-in user
"""
def test_generalUser(capfd, monkeypatch):
  # test that General displays the appropriate links
  input = '7'
  config.currUser = "UserName"
  monkeypatch.setattr('builtins.input', lambda _: input)
  result = generallinks.GeneralLinksPage()
  out, err = capfd.readouterr()
  assert "Help Center" in out
  assert "About" in out
  assert "Press" in out
  assert "Blog" in out
  assert "Careers" in out
  assert "Developers" in out

  # test that Help Center gives appropriate info
  inputs = iter(['1', '1', '7'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = generallinks.GeneralLinksPage()
  out, err = capfd.readouterr()
  assert "Help Center" in out
  assert "We're here to help" in out
  assert "Back" in out

  # test that About gives appropriate info
  inputs = iter(['2', '1', '7'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = generallinks.GeneralLinksPage()
  out, err = capfd.readouterr()
  assert "About" in out
  assert "In College: Welcome to In College"
  assert "Back" in out

  # test that Press gives appropriate info
  inputs = iter(['3', '1', '7'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = generallinks.GeneralLinksPage()
  out, err = capfd.readouterr()
  assert "Press" in out
  assert "In College Pressroom"
  assert "Back" in out

  # test that Blog gives appropriate info
  inputs = iter(['4', '1', '7'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = generallinks.GeneralLinksPage()
  out, err = capfd.readouterr()
  assert "Under Construction." in out
  assert "Back" in out

  # test that Careers gives appropriate info
  inputs = iter(['5', '1', '7'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = generallinks.GeneralLinksPage()
  out, err = capfd.readouterr()
  assert "Under Construction." in out
  assert "Back" in out

  # test that Developers gives appropriate info
  inputs = iter(['6', '1', '7'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = generallinks.GeneralLinksPage()
  out, err = capfd.readouterr()
  assert "Under Construction." in out
  assert "Back" in out


"""
function to test that Languages works correctly
for guests (users not signed-in)
"""
def test_languagesGuest(capfd, monkeypatch):
  input = '1'
  config.currUser = None
  monkeypatch.setattr('builtins.input', lambda _: input)
  result = implinks.languages()
  out, err = capfd.readouterr()
  assert "Languages" in out
  assert "Back" in out
  

"""
function to test that Languages works correctly
for signed-in users
"""
def test_languagesUser(capfd, monkeypatch, database):
  inputs = iter(['1', '1'])
  config.currUser = "Test"
  
  cursor = database.cursor()
  sqlite_insert_query = """
                        INSERT INTO userData(Username, Password, FirstName, LastName, EmailFeat, SMSFeat, TargetAdFeat, Language) 
                        VALUES('Test','Testing!123', 'Test', 'Test', 'ON', 'ON', 'ON', 'English')
                        """
  cursor.execute(sqlite_insert_query)
  
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  with mock.patch('implinks.UDCursor', return_value=cursor):
    result = implinks.languages()
  out, err = capfd.readouterr()
  assert "Languages" in out
  assert "Current Language" in out
  assert "Back" in out


"""
function to test that Guest Controls is offered
to signed-in users
"""
def test_privacyGuestControls(capfd, monkeypatch, database):
  inputs = iter(['2'])
  config.currUser = "Test"
  
  cursor = database.cursor()
  sqlite_insert_query = """
                        INSERT INTO userData(Username, Password, FirstName, LastName, EmailFeat, SMSFeat, TargetAdFeat, Language) 
                        VALUES('Test','Testing!123', 'Test', 'Test', 'ON', 'OFF', 'ON', 'English')
                        """
  cursor.execute(sqlite_insert_query)
  
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  with mock.patch('implinks.UDCursor', return_value=cursor):
    result = implinks.privacy_policy()
  out, err = capfd.readouterr()
  assert "Privacy Policy" in out
  assert "We take your privacy seriously" in out
  assert "Guest Controls" in out
  assert "Back" in out


"""
function to test the basic navigation of InCollege
"""
def test_navigation(capfd, monkeypatch):
  inputs = iter(['5', '5', '6', '10', '7'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = main.inCollege()
  out, err = capfd.readouterr()
  assert "Back"


# Run the tests
if __name__ == '__main__':
	pytest.main()
