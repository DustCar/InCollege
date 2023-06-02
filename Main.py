def createAccount():
    """
    Creates a new account for the user
    """

    username = input("Enter your username: ")
    password = passwordCreation()

    return username, password


def usernameCreation():
    """
    new username creation, verifies new username is unique
    """
    

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
