from PyQt5 import QtCore, QtGui, QtWidgets
import ScanFile

class MainFileWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(160, 50, 480, 420))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 30)
        self.verticalLayout.setObjectName("verticalLayout")

        self.Title = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Title.setEnabled(True)
        self.Title.setMinimumSize(QtCore.QSize(50, 50))
        self.Title.setAutoFillBackground(False)
        self.Title.setTextFormat(QtCore.Qt.MarkdownText)
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setObjectName("Title")
        self.verticalLayout.addWidget(self.Title)

        self.ScanFileButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.ScanFileButton.setMinimumSize(QtCore.QSize(0, 50))
        self.ScanFileButton.setObjectName("ScanFileButton")
        self.verticalLayout.addWidget(self.ScanFileButton)

        self.RecordWindowButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.RecordWindowButton.setMinimumSize(QtCore.QSize(0, 50))
        self.RecordWindowButton.setObjectName("RecordWindowButton")
        self.verticalLayout.addWidget(self.RecordWindowButton)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(660, 510, 83, 25))
        self.pushButton_2.setObjectName("pushButton_2")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Title.setText(_translate("MainWindow", "Cross Country Data Logger"))
        self.ScanFileButton.setText(_translate("MainWindow", "Scan File"))
        self.RecordWindowButton.setText(_translate("MainWindow", "Records"))
        self.pushButton_2.setText(_translate("MainWindow", "Accounts"))

    