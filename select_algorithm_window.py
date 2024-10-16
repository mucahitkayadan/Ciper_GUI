import random
import logging

logger = logging.getLogger(__name__)

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
        logger.debug("update_application called")
        try:
            self.input_text = self.application_text_input.toPlainText()
            self.key_text = self.key_input.toPlainText()

            if (not self.input_text or not self.key_text
                and not self.substitution_radio_button.isChecked()) \
                    and not self.rot13_radio_button.isChecked():
                self.application_text_output.setTextColor(QColor.fromRgb(255, 0, 0))
                self.application_text_output.setPlainText("Please fill out text and key!")
                self.application_text_output.setTextColor(QColor.fromRgb(0, 0, 0))
                logger.warning("Text or key missing")
                return

            if self.caesar_radio_button.isChecked():
                try:
                    self.key_text = int(self.key_text)
                    encrypted_text = self.cipher.caesar_cipher(
                        self.input_text, self.key_text, encrypt=self.encryption_status)
                    self.application_text_output.setPlainText(encrypted_text)
                    logger.info("Caesar cipher applied")
                except ValueError:
                    QMessageBox.critical(self, "Error", "Key must be an integer.", QMessageBox.Ok)
                    logger.error("Key must be an integer")
                    return

            if self.vigenere_radio_button.isChecked():
                encrypted_text = self.cipher.vigenere_cipher(self.input_text, self.key_text, encrypt=self.encryption_status)
                self.application_text_output.setPlainText(encrypted_text)
                logger.info("Vigenère cipher applied")

        except Exception as e:
            logger.exception("Exception occurred in update_application")

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

    def apply_cipher(self, text, encrypt=True):
        selected_algorithm = self.get_selected_algorithm()
        method_to_call = getattr(Cipher, f"{selected_algorithm}_cipher")
        
        if selected_algorithm == 'rot13':
            return method_to_call(text)
        else:
            return method_to_call(text, 1, encrypt=encrypt)

    def get_encrypted_sentence(self, sentence):
        return self.apply_cipher(sentence, encrypt=True)

    def get_original_sentence(self, encrypted_sentence):
        return self.apply_cipher(encrypted_sentence, encrypt=False)

    def get_selected_algorithm(self):
        for i, radio_button in enumerate(self.radio_buttons):
            if radio_button.isChecked():
                return self.html_elements[i]
        return None
