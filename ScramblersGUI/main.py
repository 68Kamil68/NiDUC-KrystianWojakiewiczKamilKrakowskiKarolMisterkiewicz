# This Python file uses the following encoding: utf-8
import sys
import os
from PySide2.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtWidgets

import tkinter as tk
from tkinter.filedialog import askopenfilename


SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        #QMainWindow.__init__(self)
        super(MainWindow, self).__init__()
        gui = uic.loadUi(os.path.join(SCRIPT_DIRECTORY, 'scramblergui.ui'), self)
        self.loadFileBtn.clicked.connect(self.buttonClicked)
        self.show()

    def buttonClicked(self):
        print("hahaahahah")
        root = tk.Tk()
        root.withdraw()

        file_path = askopenfilename()



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
