import pandas as pd
from Models.TableModel import TableModel
from PyQt5 import QtWidgets
from Datamanager import send_receive_data


class DailySoldView(QtWidgets.QTableView):
    def __init__(self):
        super(DailySoldView, self).__init__()
        try:
            self._data = send_receive_data.fetch_all_data_lines('Sales').drop(columns=['_id'])
        except Exception as e:
            self._data = pd.DataFrame(columns=['Name', 'Quantity', 'Price', 'Date', 'Lot Number', 'Expiry Date'])
            print(f"Connection Can't Establish :- Error {e}")
        self._model = TableModel(data=self._data)
        self.setModel(self._model)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)
        self.setMouseTracking(True)

    def addNewDataToModel(self, new_data):
        self._model.addRow(new_data)

    def refreshData(self):
        try:
            self._data = send_receive_data.fetch_all_data_lines('Sales').drop(columns=['_id'])
        except Exception as e:
            self._data = pd.DataFrame(columns=['Name', 'Quantity', 'Price', 'Date', 'Lot Number', 'Expiry Date'])
            print("No Data Present In Sales")
        self._model = TableModel(data=self._data)
        self.setModel(self._model)
        self.reset()
