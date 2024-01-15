# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RecordsWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import database
from database import SheetRepeats, SheetTimeTrial

class RecordsWindow(object):
    def setupUi(self, MainWindow, database):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 130, 721, 421))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # ------------Start Vertical Layout (with the labels and buttons)------------------------------------
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.GoogleSheetLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.GoogleSheetLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.GoogleSheetLabel.setObjectName("GoogleSheetLabel")
        self.verticalLayout.addWidget(self.GoogleSheetLabel)

        self.sheetSelect = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.sheetSelect.setEditable(True)
        self.sheetSelect.setObjectName("sheetSelect")
        self.sheetSelect.addItem("Test")
        self.sheetSelect.addItem("One")
        self.sheetSelect.addItem("Two")
        self.verticalLayout.addWidget(self.sheetSelect)

        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)

        self.OrganizeLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.OrganizeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.OrganizeLabel.setObjectName("OrganizeLabel")
        self.verticalLayout.addWidget(self.OrganizeLabel)

        self.organizeSelect = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.organizeSelect.setEditable(False)
        self.organizeSelect.setObjectName("organizeSelect")
        self.organizeSelect.addItem("")
        self.organizeSelect.addItem("")
        self.organizeSelect.currentTextChanged.connect(self.organizeTable)
        self.verticalLayout.addWidget(self.organizeSelect)
        

        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)

        self.SearchRunnerLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.SearchRunnerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SearchRunnerLabel.setObjectName("SearchRunnerLabel")
        self.verticalLayout.addWidget(self.SearchRunnerLabel)

        self.runnerSelect = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.runnerSelect.setObjectName("runnerSelect")
        self.verticalLayout.addWidget(self.runnerSelect)

        for name in database.runners.names:
            self.runnerSelect.addItem(name)

        self.runnerSelectButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.runnerSelectButton.setObjectName("runnerSelectButton")
        self.verticalLayout.addWidget(self.runnerSelectButton)

        

        self.horizontalLayout.addLayout(self.verticalLayout)
        # ----------------------End Vertical Layout-------------------------------------------
        self.tableWidget = QtWidgets.QTableWidget(self.horizontalLayoutWidget)
        self.tableWidget.setMaximumSize(QtCore.QSize(550, 16777215))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.horizontalLayout.addWidget(self.tableWidget)

        self.populateTable(database)

        self.RecordsLabel = QtWidgets.QLabel(self.centralwidget)
        self.RecordsLabel.setGeometry(QtCore.QRect(30, 30, 271, 51))
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.RecordsLabel.setFont(font)
        self.RecordsLabel.setObjectName("RecordsLabel")

        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(660, 30, 83, 25))
        self.exitButton.setObjectName("exitButton")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.GoogleSheetLabel.setText(_translate("MainWindow", "GoogleSheet"))
        self.sheetSelect.setItemText(0, _translate("MainWindow", "Test"))
        self.sheetSelect.setItemText(1, _translate("MainWindow", "One"))
        self.sheetSelect.setItemText(2, _translate("MainWindow", "Two"))
        self.OrganizeLabel.setText(_translate("MainWindow", "Organize by:"))
        self.organizeSelect.setItemText(0, _translate("MainWindow", "Alphabetically (A-Z)"))
        self.organizeSelect.setItemText(1, _translate("MainWindow", "Average Time"))
        self.SearchRunnerLabel.setText(_translate("MainWindow", "Search Runner"))
        self.runnerSelectButton.setText(_translate("MainWindow", "Search"))
        self.exitButton.setText(_translate("MainWindow", "Exit"))
        self.RecordsLabel.setText(_translate("MainWindow", "Records"))

    def populateTable(self, database):
        sheet = self.sheetSelect.currentText()

        try:
            self.wks = database.worksheets[sheet] # select current worksheet
            self.wks.readSheet() # read the specific worksheet

            self.tableWidget.setRowCount(self.wks.numOfNames) # set number of rows according to number of runners

            self.tableWidget.setColumnCount(self.wks.numOfRecords + 2) # set number of columns according to number of records

            if (type(self.wks) == SheetRepeats):
                # write data into table
                for i, runner in enumerate(self.wks.data):
                    for j, records in enumerate(runner[0]):
                        self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(records))

                    self.tableWidget.setItem(i, len(runner[0]) + 1, QtWidgets.QTableWidgetItem(runner[1]))
            if (type(self.wks) == SheetTimeTrial):
                for i, runner in enumerate(self.wks.data):
                    self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(runner[0][0]))
                    self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(runner[0][1]))
                    self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(runner[1]))
        except:
            print("not available")

    def organizeTable(self):
        if self.wks == None:
            return
        
        organizeCrit = self.organizeSelect.currentText()

        match organizeCrit:
            case "Alphabetically (A-Z)":
                self.wks.sortByName()

            case "Average Time":
                self.wks.sortByAvgTime()
            case _:
                return
            
        for i, runner in enumerate(self.wks.data):
                for j, records in enumerate(runner[0]):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(records))




        

    
        

