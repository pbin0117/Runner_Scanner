import sys
from PyQt5.QtWidgets import QApplication
from gui import Gui

app = QApplication(sys.argv)

win = Gui()


win.show()
sys.exit(app.exec_())