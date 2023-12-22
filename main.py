from PyQt5.QtWidgets import QApplication, QStackedWidget
from welcome_screen import WelcomeScreen
import sys


class Main:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.widget = QStackedWidget()
        self.welcome = WelcomeScreen(self.widget)
        self.widget.addWidget(self.welcome)
        self.widget.setFixedHeight(800)
        self.widget.setFixedWidth(1200)
        self.widget.show()

    def run(self):
        try:
            sys.exit(self.app.exec_())
        except Exception as e:
            print("Exception:", e)
            print("Exiting")


if __name__ == "__main__":
    main = Main()
    main.run()
