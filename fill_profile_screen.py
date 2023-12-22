from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QPixmap


class FillProfileScreen(QDialog):
    def __init__(self):
        super(FillProfileScreen, self).__init__()
        loadUi("ui/fill_profile.ui",self)
        self.image.setPixmap(QPixmap('ui/img/placeholder.png'))
