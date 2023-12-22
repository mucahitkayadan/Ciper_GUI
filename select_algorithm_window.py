from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class AlgorithmWindow(QMainWindow):
    def __init__(self):
        super(AlgorithmWindow, self).__init__()
        loadUi("ui/select_algorithm_window.ui", self)
