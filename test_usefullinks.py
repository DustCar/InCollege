import pytest
import usefullinks

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
# Run the tests
if __name__ == '__main__':
	pytest.main()