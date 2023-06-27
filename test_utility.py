import utility
from unittest.mock import MagicMock
from unittest import mock
from unittest.mock import patch


#capture page title
def test_pageTitle(capfd):
    utility.pageTitle("Welcome")
    out, err = capfd.readouterr()
    assert out == "--------------------\nWelcome\n--------------------\n"


#capture output and assert Hello
def test_printMessage(capfd):
    utility.printMessage("Hello")
    out, err = capfd.readouterr()
    assert out == "* Hello *\n"


#Tests for Under Construction
def test_construction(capfd, monkeypatch):
    input = '1'
    monkeypatch.setattr('builtins.input', lambda _: input)
    result = utility.construction()
    out, err = capfd.readouterr()
    assert "Under Construction.\n" in out


# function for printing menu 
def test_printMenu(capfd):
    # Define a test menu
    test_menu = {"Option1": "Action1", "Option2": "Action2", "Option3": "Action3"}

    # Call the function with the test menu
    utility.printMenu(test_menu)

    # Use capfd to capture the output that was printed to the console
    out, err = capfd.readouterr()

    # Check that the menu options were printed correctly
    assert "Press 1 for Option1" in out
    assert "Press 2 for Option2" in out
    assert "Press 3 for Option3" in out


#capture page title
def test_printSeparator(capfd):
    utility.printSeparator()
    out, err = capfd.readouterr()
    assert out == "---\n"


# Test call function
def test_call(monkeypatch):
    # Create mock functions for each menu choice
    test_func1 = MagicMock()
    test_func2 = MagicMock()
    test_func3 = MagicMock()

    # Create the test menu
    test_menu = {"Option1": test_func1, "Option2": test_func2, "Option3": test_func3}

    # Call the call function with the choice to select Option1
    utility.call(1, test_menu)

    # Test that test_func1 was called
    test_func1.assert_called_once()

    # Call the call function with the choice to select Option2
    utility.call(2, test_menu)

    # Test that test_func2 was called
    test_func2.assert_called_once()

    # Call the call function with the choice to select Option3
    utility.call(3, test_menu)

    # Test that test_func3 was called
    test_func3.assert_called_once()


# test the clearConsole functoin
def test_clearConsole(capfd):
  print("Hello World")
  out, err = capfd.readouterr()
  assert out == "Hello World\n"
  utility.clearConsole()
  out, err = capfd.readouterr()
  assert out != "Hello World\n"


# Test choiceValidation function
def test_choiceValidation(monkeypatch):
    exMenu = {"Book" : "The Great Gatsby", 
              "Author" : "F. Scott Fitzgerald"}
  
    # Test with a valid numeric input
    response = utility.choiceValidation("1", exMenu)
    assert response == 1


# test inputValidation function
def test_inputValidation(capfd):
  # true case
  userEntered = '10'
  allowedRange = range(1, 15)
  result = utility.inputValidation(userEntered, allowedRange)
  assert result == True
  # false case
  userEntered = '5'
  allowedRange = range(1, 4)
  result = utility.inputValidation(userEntered, allowedRange)
  assert result == False


# test printSuccessStory function
def test_printSuccessStory(capfd):
  utility.printSuccessStory()
  out, err = capfd.readouterr()
  assert "Thanks to InCollege" in out
  assert "InCollege User" in out
  

# test hasCapitalLetter Function
def test_hasCapitalLetter():
	out = utility.hasCapitalLetter("Test")
	out1 = utility.hasCapitalLetter("test")
	assert out == True
	assert out1 == False
  

# test hasDigit Function
def test_hasDigit():
	out = utility.hasDigit("Test123")
	out1 = utility.hasDigit("test")
	assert out == True
	assert out1 == False


# test hasSpecialCharacter function
def test_hasSpecialCharacter():
	specialCharacters = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
	for char in specialCharacters:
		password = "test" + char
		out = utility.hasSpecialCharacter(password)
		assert out == True
	out = utility.hasSpecialCharacter("test")
	assert out == False


# test confirmDetails function
def test_confirmDetails(capfd, monkeypatch):
  inputs = iter(['3', 'h', 'y'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = utility.confirmDetails()
  out, err = capfd.readouterr()
  assert result == 'y'
  assert "'y' or 'n' only" in out


# test quickGoBack function
def test_quickGoBack(capfd, monkeypatch):
  inputs = iter(['2', 'g', '1'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
  result = utility.quickGoBack()
  out, err = capfd.readouterr()
  assert "Press 1 for Back" in out

