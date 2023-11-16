from PyQt5 import QtWidgets, QtGui, QtCore
from Error_widget import ErrorWidget
from Button_widget import ButtonWidget
from Table_widget import MainTableView
import sys
import pyautogui


class MainApplication(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainApplication, self).__init__(parent=parent)
        self.setWindowTitle('eMediInvoice')
        self.add_medicine_dialog = None
        self.sell_medicine_dialog = None
        self.darkPalette = None

        # --------------- Dark Mode
        self.dark_mode()

        # --------------- Full screen
        width, height = pyautogui.size()
        self.resize(width, height-100)  # todo:- Find the best solution for the lower error layout

        # --------------- Adding widget to the main window
        self.error_widget = ErrorWidget(self)
        self.button_widget = ButtonWidget(self, self.darkPalette)
        self.table_view = MainTableView(self)

        # --------------- connecting the pyqt signal from add medicine database widget to available stock table view
        self.button_widget.add_medicine_dialog.onAddingRow.connect(self.table_view.available_stock_tab.addNewRowToModel)
        self.button_widget.sell_medicine_dialog.onRefreshData2.connect(self.table_view.daily_sold_tab.refreshData)
        self.button_widget.sell_medicine_dialog.onRefreshData1.connect(self.table_view.available_stock_tab.refresh_model)
        # --------------- Adding widget to the button and the table splitter
        self.button_table_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.button_table_splitter.addWidget(self.table_view)
        self.button_table_splitter.addWidget(self.button_widget)
        self.button_table_splitter.setSizes([850, 120])

        # --------------- Adding Widget to the splitter
        self.main_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.main_splitter.addWidget(self.button_table_splitter)
        self.main_splitter.addWidget(self.error_widget)
        self.main_splitter.setSizes([700, 60])

        self.setCentralWidget(self.main_splitter)

    def dark_mode(self):
        self.darkPalette = QtGui.QPalette()
        self.darkPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
        self.darkPalette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
        self.darkPalette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtGui.QColor(127, 127, 127))
        self.darkPalette.setColor(QtGui.QPalette.Base, QtGui.QColor(42, 42, 42))
        self.darkPalette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(66, 66, 66))
        self.darkPalette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
        self.darkPalette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
        self.darkPalette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
        self.darkPalette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QColor(127, 127, 127))
        self.darkPalette.setColor(QtGui.QPalette.Dark, QtGui.QColor(35, 35, 35))
        self.darkPalette.setColor(QtGui.QPalette.Shadow, QtGui.QColor(20, 20, 20))
        self.darkPalette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        self.darkPalette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        self.darkPalette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtGui.QColor(127, 127, 127))
        self.darkPalette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
        self.darkPalette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
        self.darkPalette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
        self.darkPalette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, QtGui.QColor(80, 80, 80))
        self.darkPalette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.white)
        self.darkPalette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, QtGui.QColor(127, 127, 127))
        self.setPalette(self.darkPalette)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    medicineX = MainApplication()
    app.setStyle('Fusion')
    medicineX.show()
    sys.exit(app.exec_())
