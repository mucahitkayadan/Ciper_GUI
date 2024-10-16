from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QWidget
import sqlite3
from fill_profile_screen import FillProfileScreen
from login_screen import is_valid_email
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class CreateAccScreen(QDialog):
    """
    A dialog for creating a new user account.

    This class handles the user interface and logic for account creation,
    including email and password validation, and database interaction.
    """

    def __init__(self, widget: QWidget) -> None:
        """
        Initialize the CreateAccScreen.

        Args:
            widget (QWidget): The parent widget for this dialog.
        """
        super(CreateAccScreen, self).__init__()
        loadUi("ui/create_account.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup.clicked.connect(self.signup_function)
        self.widget = widget
        logger.debug("CreateAccScreen initialized")

    def signup_function(self) -> None:
        """
        Handle the signup process when the signup button is clicked.

        This method validates user input, creates a new account in the database,
        and navigates to the profile filling screen upon successful signup.
        """
        logger.debug("Signup function called")
        user: str = self.emailfield.text()
        password: str = self.passwordfield.text()
        confirm_password: str = self.confirmpasswordfield.text()

        if not is_valid_email(user):
            self.error.setText("Please enter a valid email address")
            logger.warning("Invalid email address entered")
        elif len(password) == 0 or len(confirm_password) == 0:
            self.error.setText("Please fill in all inputs.")
            logger.warning("Empty password fields")
        elif len(password) < 8 or len(password) > 15:
            self.error.setText("Password has to be between 8 and 15 characters.")
            logger.warning("Password length is not within the required range")
        elif password != confirm_password:
            self.error.setText("Passwords do not match.")
            logger.warning("Passwords do not match")
        else:
            try:
                conn: sqlite3.Connection = sqlite3.connect("db/credentials.db")
                cur: sqlite3.Cursor = conn.cursor()
                cur.execute('INSERT INTO login_info (email, password) VALUES (?, ?)', (user, password))
                conn.commit()
                conn.close()
                self.error.setText("Account created successfully.")
                logger.info("Account created successfully for user: %s", user)
                fill_profile: FillProfileScreen = FillProfileScreen()
                self.widget.addWidget(fill_profile)
                self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
            except sqlite3.IntegrityError:
                self.error.setText("Email already exists.")
                logger.error("IntegrityError: Email already exists for user: %s", user)
            except Exception as e:
                self.error.setText(f"Error: {str(e)}")
                logger.exception("Exception occurred during signup")
