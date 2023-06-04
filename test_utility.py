import utility
from unittest.mock import MagicMock

#capture page title
def test_pageTitle(capfd):
    utility.pageTitle("Welcome")
    out, err = capfd.readouterr()
    assert out == "----------\nWelcome\n----------\n"

#capture output and assert Hello
def test_printMessage(capfd):
    utility.printMessage("Hello")
    out, err = capfd.readouterr()
    assert out == "* Hello *\n"

#Tests for Under Construction
def test_construction(capfd):
    utility.construction()
    out, err = capfd.readouterr()
    assert out == "Under Construction.\n"

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


# Test choiceValidation function
def test_choiceValidation(monkeypatch):

    # Test with a valid numeric input
    response = utility.choiceValidation("1")
    assert response == 1
    



