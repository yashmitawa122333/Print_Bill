from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import QtWidgets
from Datamanager import send_receive_data


class AllBills(QtWidgets.QDialog):
    def __init__(self, parent, palette):
        super(AllBills, self).__init__(parent)

        # ------------------- Dark mode
        self.setPalette(palette)

        self.setWindowTitle("Bill Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout(self)

        self.table_widget = QTableWidget(self)
        self.layout.addWidget(self.table_widget)
        self.table_widget.setColumnCount(4)  # Adjust column count

        # Set headers
        headers = ["Invoice Number", "Buyer Name", "Total Price", "Date"]
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setMouseTracking(True)
        self.table_widget.setAutoScroll(True)
        self.load_data()

    def load_data(self):
        bill_data = send_receive_data.fetch_all_data_lines('bills')
        self.table_widget.setRowCount(0)  # Clear existing rows
        for index, bill in bill_data.iterrows():
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(str(bill["_id"])))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(bill["Buyer Name"]))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(str(bill["Total Price"])))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(str(bill["Selling date"])))

            # # Add button to each row
            # button = QPushButton("Generate Invoice")
            # # button.clicked.connect(lambda _, row=row_position: generate_invoice(bill_data[row].to_dict(),
            #                                                                     # bill_data[row]['Buyer Name']))
            # button.clicked.connect(lambda _, row=row_position: print(bill_data[row].to_dict()))
            # self.table_widget.setCellWidget(row_position, 4, button)


