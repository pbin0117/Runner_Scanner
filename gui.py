# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6 + modified by me


from PyQt5 import QtCore, QtWidgets,  QtGui
from PyQt5.QtWidgets import QMainWindow

from ScanFile import ScanFileWindow
from MainWindow import MainFileWindow
from RecordsWindow import RecordsWindow

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
        self.recordsWindow = RecordsWindow()

        self.database = Database("Test")


        self.mainFileWindow.setupUi(self)
        self.mainFileWindow.ScanFileButton.clicked.connect(self.scanFileButtonFunc)
        self.mainFileWindow.RecordWindowButton.clicked.connect(self.recordFileButtonFunc)

        
        
    def scanFileButtonFunc(self):
        self.scanFileWindow.setupUi(self)
        self.scanFileWindow.submitButton.clicked.connect(self.submitted)

    def recordFileButtonFunc(self):
        self.recordsWindow.setupUi(self, self.database)
        self.recordsWindow.sheetSelect.currentTextChanged.connect(self.onNewWorksheet)
        self.recordsWindow.exitButton.clicked.connect(self.exitRecordScreen)
        self.recordsWindow.runnerSelectButton.clicked.connect(self.runnerRecordScreen)
        
    def submitted(self):
        googleSheets = self.scanFileWindow.sheetSelect.currentText()
        print(googleSheets)
        scanner = Scanner(self.scanFileWindow.imgfile)

        data = scanner.extract_records(p_display=True)
        self.database.addSheet(googleSheets, data) 

        self.database.worksheets[googleSheets].pasteSheet(data[2:], data[0], data[1], self.database)

        self.mainFileWindow.setupUi(self)
        self.mainFileWindow.ScanFileButton.clicked.connect(self.scanFileButtonFunc)
        self.mainFileWindow.RecordWindowButton.clicked.connect(self.recordFileButtonFunc)

    def onNewWorksheet(self):
        self.recordsWindow.populateTable(self.database)

    def exitRecordScreen(self):
        self.mainFileWindow.setupUi(self)
        self.mainFileWindow.ScanFileButton.clicked.connect(self.scanFileButtonFunc)
        self.mainFileWindow.RecordWindowButton.clicked.connect(self.recordFileButtonFunc)

    def runnerRecordScreen(self):
        self.recordsWindow.showRunnerSpecificWindow(self.database)
    

