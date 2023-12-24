from PyQt5.QtWidgets import QApplication, QStackedWidget, QDesktopWidget
from welcome_screen import WelcomeScreen
import sys
from PyQt5.QtGui import QIcon


class Main:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.screen = QDesktopWidget().screenGeometry()
        self.icon = QIcon("ui/img/icon.png")
        self.widget = QStackedWidget()
        self.welcome = WelcomeScreen(self.widget)
        self.widget.addWidget(self.welcome)

        self.widget.setMinimumSize(1200, 800)
        # self.widget.setMaximumSize(self.screen.width(), self.screen.height())
        # self.welcome.setGeometry(0, 0, self.screen.width(), self.screen.height())
        # self.widget.setGeometry(0, 0, self.screen.width(), self.screen.height())

        self.widget.setFixedHeight(800)
        self.widget.setFixedWidth(1200)
        self.widget.setWindowIcon(self.icon)
        self.widget.show()
        # self.center_widget()

    def center_widget(self):
        widget_geometry = self.widget.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        widget_geometry.moveCenter(screen_center)
        self.widget.move(widget_geometry.topLeft())

    def run(self):
        try:
            sys.exit(self.app.exec_())
        except Exception as e:
            print("Exception:", e)
            print("Exiting")


if __name__ == "__main__":
    main = Main()
    main.run()
