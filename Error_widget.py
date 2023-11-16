from PyQt5 import QtWidgets, QtGui, QtCore
import sys


class ErrorWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(ErrorWidget, self).__init__(parent)

        layout = QtWidgets.QHBoxLayout(self)
        self.plain_text = QtWidgets.QLabel(self)
        self.plain_text.setText('No Error in the App')
        layout.addWidget(self.plain_text)