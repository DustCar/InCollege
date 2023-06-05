import maskpass as mp
import sqlite3 as sql


# SQLite database
userData = sql.connect("User_Data.db")
UDCursor = userData.cursor()
UDCursor.execute("CREATE TABLE User_Data(Username, Password)")


def createAccount():
    """
    Creates a new account for the user
    """

    # checks if max number of accounts have been made
    if(len(UDCursor.execute("SELECT Username FROM User_Data").fetchall()) < 5):
        username = usernameCreation()
        password = passwordCreation() 

        UDCursor.execute(f"""
        INSERT INTO User_Data VALUES
            ({username}, {password})
        """)
    else:
        print("Maximum amount of accounts have been made")

def usernameCreation():
    """
    new username creation, verifies new username is unique
    """
    username = input("Enter your desired username: ")

    # Checks if username already exists
    for users in UDCursor.execute("SELECT Username FROM User_Data").fetchall():
        if username == users:
            print(f'The username "{username}" is already in use\n')
            return usernameCreation()
    return username
    
def passwordCreation():
    """
    Password creation function, calls itself if new user password does not
    meet the requiremnts
    """
    print("PASSWORD REQUIREMENTS\n----------------------------")
    print("Between 8-12 Characters\nAt least 1 Capital Letter\nAt least 1 Digit\nAt least 1 Special Character")
    print("----------------------------")

    password = input("Enter your desired Password: ")

    # Checks if the password fits the character count
    if len(password) > 12:
        print("Password is greater than 12 characters, try removing some characters!\n")
        return passwordCreation()
    elif len(password) < 8:
        print("Password is less than 8 characters, try adding some more characters!\n")
        return passwordCreation()

    # Checks for Capital
    if not hasCapitalLetter(password):
        print("Password must include a capital letter, try again\n")
        return passwordCreation()
    
    # Checks for digit
    if not hasDigit(password):
        print("Password must include a digit, try again\n")
        return passwordCreation()

    # Checks for Special character
    if not hasSpecialCharacter(password):
        print("Password must include a special character, try again\n")
        return passwordCreation()
    
    # If password meets all requirements, returns password
    return password

def hasCapitalLetter(password):
    """
    password: attempted new user password
    
    Checks for capital letters in new user password
    """
    for character in password:
        if character.isupper():
            return True
    return False

def hasDigit(password):
    """
    password: attempted new user password

    Checks for digits in new user password
    """
    for character in password:
        if character.isdigit():
            return True
    return False

def hasSpecialCharacter(password):
    """
    password: attempted new user password

    Checks for special characters in new user password
    """
    specialCharacters = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
    for character in password:
        if character in specialCharacters:
            return True
    return False

def login():
    """
    Verify user login information
    """

    print("USER LOGIN\n----------")

    username = input("USERNAME: ")
    password = mp.askpass(prompt="PASSWORD: ", mask="*")

    # Username and password verification
    if not userVerification(username, password):
        # Incorrect information
        print("Either Username or Password is incorrect\n")
        return login()
    

    # Login information is correct
    print('Login Success!\n')
    return 
    
def userVerification(username, password):
    """
    username: attempted username associated with attempted password
    password: attempted password

    verifies that inputted username and password both exists and are correct
    """
    for users, passwrds in UDCursor.execute("SELECT Username, Password FROM User_Data").fetchall():
        if username == users and password == passwrds:
            return True
    return False
    