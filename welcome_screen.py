from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
from login_screen import LoginScreen
from create_account import CreateAccScreen


class WelcomeScreen(QDialog):
    def __init__(self, widget):
        super(WelcomeScreen, self).__init__()
        loadUi("ui/welcome_screen.ui", self)
        self.login.clicked.connect(self.go_to_login)
        self.create_button.clicked.connect(self.go_to_create)
        self.widget = widget

    def go_to_login(self):
        login = LoginScreen(self.widget)
        self.widget.addWidget(login)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def go_to_create(self):
        create = CreateAccScreen(self.widget)
        self.widget.addWidget(create)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
