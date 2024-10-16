from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from select_algorithm_window import AlgorithmWindow
import sqlite3
import re
import logging

logger = logging.getLogger(__name__)


def is_valid_email(email: str) -> bool:
    """
    Validate if the given string is a valid email address.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.

    This function uses a regular expression pattern to check if the email
    follows a basic valid email format: username@domain.tld
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


class LoginScreen(QDialog):
    def __init__(self, widget):
        super(LoginScreen, self).__init__()
        loadUi("ui/login.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.login_function)
        self.widget = widget
        logger.debug("LoginScreen initialized")

    def login_function(self):
        logger.debug("Login function called")
        user = self.emailfield.text()
        password = self.passwordfield.text()

        if len(user) == 0 or len(password) == 0:
            self.error.setText("Please input all fields.")
            logger.warning("Empty login fields")
        elif not is_valid_email(user):
            self.error.setText("Please enter a valid email address.")
            logger.warning("Invalid email address entered")
        else:
            try:
                conn = sqlite3.connect("db/credentials.db")
                cur = conn.cursor()
                cur.execute('SELECT password FROM login_info WHERE email = ?', (user,))
                result = cur.fetchone()
                conn.close()
                if result is None or result[0] != password:
                    self.error.setText("Invalid username or password")
                    logger.warning("Invalid login attempt for user: %s", user)
                else:
                    self.error.setText("")
                    logger.info("User %s logged in successfully", user)
                    self.go_to_algorithm_window()
            except Exception as e:
                self.error.setText(f"Error: {str(e)}")
                logger.exception("Exception occurred during login")

    def go_to_algorithm_window(self):
        logger.debug("Navigating to AlgorithmWindow")
        select_algorithm = AlgorithmWindow()
        self.widget.addWidget(select_algorithm)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
