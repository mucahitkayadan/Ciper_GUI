import random

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import QUrl

from engine.Cipher import Cipher
from html_files.game.sentences import sentences_list


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
        self.encryption_status = True
        self.attempt_number = 0
        self.shown_hint_number = 0
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
        self.initialize_game_window()
        for radio_button in self.radio_buttons:
            radio_button.toggled.connect(self.update_tabs)
        self.submit_button.clicked.connect(self.update_application)
        self.encrypt_button.clicked.connect(lambda: self.set_encryption_status(True))
        self.decrypt_button.clicked.connect(lambda: self.set_encryption_status(False))
        self.game_guess_button.clicked.connect(self.game)

    def update_tabs(self):
        self.update_description()
        self.update_algorithm()
        self.initialize_game_window()
        if self.substitution_radio_button.isChecked() or self.rot13_radio_button.isChecked():
            self.key_input.setReadOnly(True)
            self.key_input.setPlainText("")
        else:
            self.key_input.setReadOnly(False)

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

        if (not self.input_text or not self.key_text
            and not self.substitution_radio_button.isChecked()) \
                and not self.rot13_radio_button.isChecked():
            self.application_text_output.setTextColor(QColor.fromRgb(255, 0, 0))
            self.application_text_output.setPlainText("Please fill out text and key!")
            self.application_text_output.setTextColor(QColor.fromRgb(0, 0, 0))
            return

        if self.caesar_radio_button.isChecked():
            try:
                self.key_text = int(self.key_text)
                encrypted_text = self.cipher.caesar_cipher(
                    self.input_text, self.key_text, encrypt=self.encryption_status)
                self.application_text_output.setPlainText(encrypted_text)
            except ValueError:
                QMessageBox.critical(self, "Error", "Key must be an integer.", QMessageBox.Ok)
                return

        if self.vigenere_radio_button.isChecked():
            encrypted_text = self.cipher.vigenere_cipher(self.input_text, self.key_text, encrypt=self.encryption_status)
            self.application_text_output.setPlainText(encrypted_text)

        if self.substitution_radio_button.isChecked():
            # Define the substitution key
            substitution_key = {'A': 'Q', 'B': 'W', 'C': 'E', 'D': 'R', 'E': 'T',
                                'F': 'Y', 'G': 'U', 'H': 'I', 'I': 'O', 'J': 'P',
                                'K': 'A', 'L': 'S', 'M': 'D', 'N': 'F', 'O': 'G',
                                'P': 'H', 'Q': 'J', 'R': 'K', 'S': 'L', 'T': 'Z',
                                'U': 'X', 'V': 'C', 'W': 'V', 'X': 'B', 'Y': 'N', 'Z': 'M'}
            encrypted_text = self.cipher.substitution_cipher(
                self.input_text, substitution_key, encrypt=self.encryption_status)
            self.application_text_output.setPlainText(encrypted_text)

        if self.rot13_radio_button.isChecked():
            encrypted_text = self.cipher.rot13_cipher(self.input_text)
            self.application_text_output.setPlainText(encrypted_text)

        if self.rail_fence_radio_button.isChecked():
            try:
                self.key_text = int(self.key_text)
                encrypted_text = self.cipher.rail_fence_cipher(
                    self.input_text, self.key_text, encrypt=self.encryption_status)
                self.application_text_output.setPlainText(encrypted_text)
            except ValueError:
                QMessageBox.critical(self, "Error", "Key must be an integer.", QMessageBox.Ok)
                return

    def set_encryption_status(self, value):
        self.encryption_status = value

    def initialize_game_window(self):
        original_sentence = random.choice(sentences_list)
        encrypted_sentence = self.get_encrypted_sentence(original_sentence)
        self.game_output_text_edit.setPlainText(encrypted_sentence)

    def game(self):
        encrypted_sentence = self.game_output_text_edit.toPlainText()

        if encrypted_sentence != self.game_input_text_edit.toPlainText():
            self.attempt_number += 1
            self.attempt_label.setText("Attempt: " + str(self.attempt_number))
            QMessageBox.warning(self, "Error", "Wrong Guess.")

            if self.attempt_number % 3 == 0:
                hint_text = self.get_hint_text(encrypted_sentence)
                self.shown_hint_number += 1
                self.game_output_text_edit.setText(hint_text)

    def get_hint_text(self, encrypted_sentence):
        original_sentence = self.get_original_sentence(encrypted_sentence)
        original_words = original_sentence.split()
        encrypted_words = encrypted_sentence.split()
        hint_words = []
        for i, word in enumerate(encrypted_words):
            if len(word) > self.shown_hint_number:
                word_list = list(word)
                word_list[self.shown_hint_number] = ("<font color='green'>" +
                                                     original_words[i][self.shown_hint_number] + "</font>")
                hint_words.append("".join(word_list))
            else:
                hint_words.append(word)
        hint_text = " ".join(hint_words)

        return hint_text

    def get_encrypted_sentence(self, sentence):
        encrypted_sentence = sentence
        cipher_name = None
        for i, radio_button in enumerate(self.radio_buttons):
            if radio_button.isChecked():
                cipher_name = self.html_elements[i] + '_cipher'
        # Use getattr to get the method by name
        method_to_call = getattr(self.cipher, cipher_name, None)
        # Check if the method exists
        if method_to_call is not None and callable(method_to_call):
            encrypted_sentence = method_to_call(sentence, 1, encrypt=True)  # Call the method
        else:
            print(f"Method '{cipher_name}' not found in Cipher class")
        return encrypted_sentence

    def get_original_sentence(self, encrypted_sentence):
        cipher_name = None
        for i, radio_button in enumerate(self.radio_buttons):
            if radio_button.isChecked():
                cipher_name = self.html_elements[i] + '_cipher'
                break

        method_to_call = getattr(self.cipher, cipher_name, None)
        if method_to_call is not None and callable(method_to_call):
            original_sentence = method_to_call(encrypted_sentence, 1, encrypt=False)
        else:
            print(f"Method '{cipher_name}' not found in Cipher class")
            original_sentence = encrypted_sentence

        return original_sentence
