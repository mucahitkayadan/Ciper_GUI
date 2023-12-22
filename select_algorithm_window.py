from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
import sqlite3


class AlgorithmWindow(QMainWindow):
    def __init__(self):
        super(AlgorithmWindow, self).__init__()
        loadUi("ui/select_algorithm_window.ui", self)
        self.radio_buttons = [
            self.caesar_radio_button,
            self.substitution_radio_button,
            self.vigenere_radio_button,
            self.rail_fence_radio_button,
            self.rot13_radio_button
        ]
        for radio_button in self.radio_buttons:
            radio_button.toggled.connect(self.select_algorithm)

    def select_algorithm(self):
        conn = sqlite3.connect("db/credentials.db")
        cur = conn.cursor()
        query = "SELECT caesar, substitution, vigenere, rail_fence, rot13 FROM crypto_descriptions"
        cur.execute(query)
        results = cur.fetchone()

        for i, radio_button in enumerate(self.radio_buttons):
            if radio_button.isChecked():
                self.algo_title.setText(results[i])
                break

        conn.close()
