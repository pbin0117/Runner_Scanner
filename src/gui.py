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

        self.setGeometry(200, 200, 800, 600) # setting the default size of the screen
        self.setWindowTitle("Cross Country Data Logger")  # title
        
        # initializing the three windows for future use
        self.mainFileWindow = MainFileWindow()
        self.scanFileWindow = ScanFileWindow()
        self.recordsWindow = RecordsWindow()
        
        # initializing the database 
        self.database = Database("Test")

        # sets the current window to MainFileWindow (the start up menu) + all the buttons
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
        # brings which GoogleSheet worksheet is selected
        googleSheets = self.scanFileWindow.sheetSelect.currentText()
        print(googleSheets)

        # have to check whether a valid image is uploaded or none at all
        try:
            # makes a local scanner object
            scanner = Scanner(self.scanFileWindow.imgfile)

            # scanner scans and extracts records
            data = scanner.extract_records(p_display=True)

            # create new local storage of the data
            self.database.addSheet(googleSheets, data) 

            # uploads it to Google Sheets Database
            self.database.worksheets[googleSheets].pasteSheet(data[2:], data[0], data[1], self.database)
        except:
            # usually when no image is submitted is the except called
            print("no image submitted!")

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
    

