from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QUrl

from engine.Cipher import Cipher


class AlgorithmWindow(QMainWindow):
    def __init__(self):
        super(AlgorithmWindow, self).__init__()
        loadUi("ui/select_algorithm_window.ui", self)
        self.description_text_browser.setSource(QUrl.fromLocalFile("html_files/descriptions/caesar.html"))
        self.algorithm_text_browser.setSource(QUrl.fromLocalFile("html_files/algorithms/caesar.html"))
        self.tabWidget.setCurrentIndex(0)
        self.cipher = Cipher
        self.input_text = None
        self.key_text = None
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
            radio_button.toggled.connect(self.update_tabs)
        self.submit_button.clicked.connect(self.update_application)

    def update_tabs(self):
        self.update_description()
        self.update_algorithm()

    def update_description(self):
        for i, radio_button in enumerate(self.radio_buttons):
            if radio_button.isChecked():
                cipher_name = self.html_elements[i]
                description_file_path = "html_files/descriptions/" + cipher_name + ".html"
                self.description_text_browser.setSource(QUrl.fromLocalFile(description_file_path))
                break

    def update_algorithm(self):
        for i, radio_button in enumerate(self.radio_buttons):
            if radio_button.isChecked():
                cipher_name = self.html_elements[i]
                algorithm_file_path = "html_files/algorithms/" + cipher_name + ".html"
                self.algorithm_text_browser.setSource(QUrl.fromLocalFile(algorithm_file_path))
                break

    def update_application(self):
        self.input_text = self.application_text_input.toPlainText()
        self.key_text = self.key_input.toPlainText()
        if not self.input_text or not self.key_text:
            self.application_text_output.setTextColor(QColor.fromRgb(255, 0, 0))
            self.application_text_output.setPlainText("Please fill out text and key!")
            self.application_text_output.setTextColor(QColor.fromRgb(0, 0, 0))
            return
        print(self.input_text)
        print(self.key_text)

        if self.caesar_radio_button.isChecked():
            encrypted_text = self.cipher.caesar_cipher(self.input_text, int(self.key_text), encrypt=True)
            self.application_text_output.setPlainText(encrypted_text)
