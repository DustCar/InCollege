import pytest, main
from unittest import mock

'''
this file contains unit tests for the various
functions found in main.py
'''

# test the calling of the main function inCollege
@mock.patch('main.gp.getpass')
def test_inCollege(password, capfd, monkeypatch):
	# these simulate the flow of logging in,
	# clicking learn a new skill, going back, and finding someone
	password.return_value = "Testing!123"
	inputs = iter(['1', 'Test', 'Testing!123', '3', '6', '2'])
	monkeypatch.setattr('builtins.input', lambda _: next(inputs))
	result = main.inCollege()
	out, err = capfd.readouterr()
	assert "You have successfully logged in" in out
	assert "Home" in out
	assert "Press 1 for Skill1." in out

# test the calling of the main function inCollege
@mock.patch('main.account.login')
def test_loginAuthorization(login, capfd, monkeypatch):
	# test for correct login credentials
	login.return_value = False
	result = main.loginAuthorization("Testing", "Testing!123")
	assert result == True

	# test for incorrect login credentials
	with pytest.raises(Exception):
		result = main.loginAuthorization("Tes", "Testing!123")
		out, err = capfd.readouterr
		assert "Incorrect username/password" in out

	# test for invalid username length
	with pytest.raises(Exception):
		result = main.loginAuthorization("", "Testing!123")
		out, err = capfd.readouterr
		assert "Incorrect username/password" in out

	# test for invalid password length
	with pytest.raises(Exception):
		result = main.loginAuthorization("Test", "Testing!1235678")
		out, err = capfd.readouterr
		assert "Incorrect username/password" in out

@mock.patch("main.inCollege")
def test_quitOption(mock_inCollege, capfd, monkeypatch):
	monkeypatch.setattr('builtins.input', lambda _: "q")
	result = main.quitOption()
	mock_inCollege.assert_called_once()

@mock.patch("main.inCollege")
def test_quitOption(mock_inCollege, capfd, monkeypatch):
	monkeypatch.setattr('builtins.input', lambda _: "W")
	result = main.quitOption()
	assert not mock_inCollege.called

def test_closeApp(capfd):
	try:
		main.closeApp()
	except SystemExit:
		out, err = capfd.readouterr()
		assert "Exited InCollege." in out



# Run the tests
if __name__ == '__main__':
	pytest.main()