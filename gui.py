# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6 + modified by me


from PyQt5 import QtCore, QtWidgets,  QtGui
from PyQt5.QtWidgets import QApplication,QMainWindow

from ScanFile import ScanFileWindow
from MainWindow import MainFileWindow
from database import Database
from scanner import Scanner

import sys


class Gui(QMainWindow):
    def __init__(self):
        super(Gui, self).__init__()

        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("weeeee")
        
        self.mainFileWindow = MainFileWindow()
        self.scanFileWindow = ScanFileWindow()


        self.mainFileWindow.setupUi(self)
        self.mainFileWindow.ScanFileButton.clicked.connect(self.scanFileButtonFunc)

        
        
    def scanFileButtonFunc(self):
        self.scanFileWindow.setupUi(self)
        self.scanFileWindow.submitButton.clicked.connect(self.submitted)

    def submitted(self):
        googleSheets = self.scanFileWindow.sheetSelect.currentText()
        print(googleSheets)
        database = Database("Test")
        scanner = Scanner(self.scanFileWindow.imgfile)

        data = scanner.extract_records(p_display=True)
        database.addSheet(googleSheets)

        database.worksheets[googleSheets].pasteSheet400(data)

        self.mainFileWindow.setupUi(self)
        self.mainFileWindow.ScanFileButton.clicked.connect(self.scanFileButtonFunc)
    

app = QApplication(sys.argv)

win = Gui()


win.show()
sys.exit(app.exec_())