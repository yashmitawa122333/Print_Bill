import pandas as pd
import settings
from Models.TableModel import TableModel
from PyQt5 import QtWidgets
from Datamanager import send_data


class AvailableStockView(QtWidgets.QTableView):
    def __init__(self, ):
        super(AvailableStockView, self).__init__()
        self.client = send_data.MongoDBConnection(settings.MONGO_STRING)
        self.db = self.client.get_database(settings.DATABASE)
        self.collection = self.db['availablestock']
        self._data = None
        self._model = None
        self.init_UI()

    def init_UI(self):
        try:
            _data = self.collection.find({})
            data_list = []
            for document in _data:
                data_list.append(document)
            self._data = pd.DataFrame(data_list).drop(columns=['_id', 'Total Price'])
            self._data = self._data[self._data['Boxes'] != 0]
        except Exception as e:
            self._data = pd.DataFrame(columns=["Received By", "Bill Number", "Purchase Date",
                                               "Name", "Price", "Boxes", "Lot/Batch Number", "Expiry Date",
                                               "Total Price"])
            print(f"Connection Can't Establish :- Error {e}")

        self._model = TableModel(data=self._data)
        self.setModel(self._model)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)
        self.setMouseTracking(True)

    def refresh_model(self):
        self.init_UI()

    def addNewRowToModel(self, new_row_data):
        self._model.addRow(new_row_data)
