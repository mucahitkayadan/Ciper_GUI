from PyQt5.QtWidgets import QApplication, QStackedWidget
from welcome_screen import WelcomeScreen
import sys
from PyQt5.QtGui import QIcon


class Main:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.icon = QIcon("ui/img/icon.png")
        self.widget = QStackedWidget()
        self.welcome = WelcomeScreen(self.widget)
        self.widget.addWidget(self.welcome)
        self.widget.setFixedHeight(800)
        self.widget.setFixedWidth(1200)
        self.widget.setWindowIcon(self.icon)
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
