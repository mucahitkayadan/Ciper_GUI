from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QUrl


class AlgorithmWindow(QMainWindow):
    def __init__(self):
        super(AlgorithmWindow, self).__init__()
        loadUi("ui/select_algorithm_window.ui", self)
        self.text_browser.setSource(QUrl.fromLocalFile("descriptions/caesar.html"))
        self.radio_buttons = [
            self.caesar_radio_button,
            self.substitution_radio_button,
            self.vigenere_radio_button,
            self.rail_fence_radio_button,
            self.rot13_radio_button
        ]
        self.html_elements = [
            'caesar', 'substitution', 'vigenere', 'rail_fence', 'rot13'
        ]
        for radio_button in self.radio_buttons:
            radio_button.toggled.connect(self.select_algorithm)

    def select_algorithm(self):
        for i, radio_button in enumerate(self.radio_buttons):
            if radio_button.isChecked():
                cipher_name = self.html_elements[i]
                file_path = "descriptions/" + cipher_name + ".html"
                self.text_browser.setSource(QUrl.fromLocalFile(file_path))
                break
