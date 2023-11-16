from PyQt5 import QtWidgets
from datetime import date
from dateutil. relativedelta import relativedelta
from Datamanager import send_receive_data
from Views import DailySolds, AvailableStock
from datetime import date


class MainTableView(QtWidgets.QFrame):
    def __init__(self, parent):
        super(MainTableView, self).__init__(parent)
        # -------------------- Layouts
        self.VerticalLayout = QtWidgets.QVBoxLayout(self)
        self.HorizontalLayout = QtWidgets.QHBoxLayout()

        # -------------------- Table View and model and other think
        # ---------------- Calling the model class
        self.table = QtWidgets.QTabWidget()
        self.daily_sold_tab = DailySolds.DailySoldView()
        self.available_stock_tab = AvailableStock.AvailableStockView()
        self.table.addTab(self.daily_sold_tab, "Sales")
        self.table.addTab(self.available_stock_tab, "Pharmacy Database")

        # -------------------- Defining the buttons
        self.label_to = QtWidgets.QLabel('To :- ')
        self.label_from = QtWidgets.QLabel('From :- ')
        self.starting_date = QtWidgets.QDateEdit()
        self.starting_date.setDate(date.today() - relativedelta(months=3))
        self.ending_date = QtWidgets.QDateEdit()
        self.ending_date.setDate(date.today())

        self.HorizontalLayout.addWidget(self.label_to)
        self.HorizontalLayout.addWidget(self.starting_date)
        self.HorizontalLayout.addWidget(self.label_from)
        self.HorizontalLayout.addWidget(self.ending_date)
        self.HorizontalLayout.addStretch(1)

        self.button_get_data = QtWidgets.QPushButton('Get Data')
        self.button_get_data.clicked.connect(self.get_data)
        self.HorizontalLayout.addWidget(self.button_get_data)

        # -------------------- Adding Widget to the layouts
        self.VerticalLayout.addWidget(self.table)
        self.VerticalLayout.addLayout(self.HorizontalLayout)

    def get_data(self):
        send_receive_data.query_database('Sales', start_date=self.starting_date.dateTime().toPyDateTime(),
                                         end_date=self.ending_date.dateTime().toPyDateTime())
