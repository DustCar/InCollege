import sqlite3 as sql
import utility

# Connect to SQL database
userData = sql.connect("User_Data.db")
UDCursor = userData.cursor()

# Create table for jobs if table does not exist
try:
  UDCursor.execute("""
                    CREATE TABLE IF NOT EXISTS jobsData (
                    Issuer VARCHAR(25), 
                    Title VARCHAR(255), 
                    Description TEXT, 
                    Employer VARCHAR(25), 
                    Location VARCHAR(255), 
                    Salary INT
                  );""")
  UDCursor.commit()
except:
  pass

