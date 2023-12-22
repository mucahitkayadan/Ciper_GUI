from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from select_algorithm_window import AlgorithmWindow
import sqlite3
import re


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


class LoginScreen(QDialog):
    def __init__(self, widget):
        super(LoginScreen, self).__init__()
        loadUi("ui/login.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.login_function)
        self.widget = widget

    def login_function(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()

        if len(user) == 0 or len(password) == 0:
            self.error.setText("Please input all fields.")

        # elif not is_valid_email(user):
        #     self.error.setText("Please enter a valid email address.")

        else:
            conn = sqlite3.connect("db/credentials.db")
            cur = conn.cursor()
            query = 'SELECT password FROM login_info WHERE email =\'' + user + "\'"
            cur.execute(query)
            result = cur.fetchone()
            if result is None:
                self.error.setText("Invalid username or password")
            else:
                result_pass = result[0]
                if result_pass == password:
                    print("Successfully logged in.")
                    self.error.setText("")
                    self.go_to_algorithm_window()
                else:
                    self.error.setText("Invalid username or password")

    def go_to_algorithm_window(self):
        select_algorithm = AlgorithmWindow()
        self.widget.addWidget(select_algorithm)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
