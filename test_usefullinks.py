import pytest
import usefullinks, generallinks

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

def test_UsefulLinksPage(capfd, monkeypatch):
  # test if necessary links are displayed
  monkeypatch.setattr('builtins.input', lambda _: '5')
  result = usefullinks.UsefulLinksPage()
  out, err = capfd.readouterr()
  assert "Press 1 for General." in out
  assert "Press 2 for Browse InCollege." in out
  assert "Press 3 for Business Solutions." in out
  assert "Press 4 for Directories." in out
  assert "Press 5 for Back." in out

  # test if General link goes to general page
  inputs = iter(['1', '8', '5'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = usefullinks.UsefulLinksPage()
  out, err = capfd.readouterr()
  assert "Press 1 for Sign Up." in out
  assert "Press 2 for Help Center." in out
  assert "Press 3 for About." in out
  assert "Press 4 for Press." in out
  assert "Press 5 for Blog." in out
  assert "Press 6 for Careers." in out
  assert "Press 7 for Developers." in out
  assert "Press 8 for Back." in out

  # test if next three links print under construction (will only test one to cover for all under construction functions)
  inputs = iter(['2', '1', '5'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = usefullinks.UsefulLinksPage()
  out, err = capfd.readouterr()
  assert "Under Construction." in out
  
# Run the tests
if __name__ == '__main__':
	pytest.main()