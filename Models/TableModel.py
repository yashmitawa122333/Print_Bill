from PyQt5 import QtCore
import pandas as pd
import typing


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data: typing.Union[None, pd.DataFrame], parent=None):
        super(TableModel, self).__init__(parent=parent)
        self._data = data

    def rowCount(self, index=None):
        return self._data.shape[0]

    def columnCount(self, index=None):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self._data.columns[section])

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    # -------------- custom methods for add row -----------------
    def addRow(self, data_df: typing.Union[dict, pd.DataFrame]):
        if not isinstance(data_df, pd.DataFrame):
            data_df = pd.DataFrame([data_df], columns=self._data.columns)
        updated_df = pd.concat([data_df, self._data], ignore_index=True)
        self.beginResetModel()
        self._data = updated_df
        self.endResetModel()
