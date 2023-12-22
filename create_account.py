from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
import sqlite3
from fill_profile_screen import FillProfileScreen
from login_screen import is_valid_email


class CreateAccScreen(QDialog):
    def __init__(self, widget):
        super(CreateAccScreen, self).__init__()
        loadUi("ui/create_account.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup.clicked.connect(self.signup_function)
        self.widget = widget

    def signup_function(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()
        confirm_password = self.confirmpasswordfield.text()
        if not is_valid_email(user):
            self.error.setText("Please enter a valid email address")
        elif len(password) == 0 or len(confirm_password) == 0:
            self.error.setText("Please fill in all inputs.")
        # elif len(password) < 8 or len(confirm_password) > 15:
        #     self.error.setText("Password has to be between 8 and 15 characters.")
        elif password != confirm_password:
            self.error.setText("Passwords do not match.")
        else:
            conn = sqlite3.connect("db/credentials.db")
            cur = conn.cursor()

            user_info = [user, password]
            cur.execute('INSERT INTO login_info (email, password) VALUES (?,?)', user_info)

            conn.commit()
            conn.close()

            fill_profile = FillProfileScreen()
            self.widget.addWidget(fill_profile)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
