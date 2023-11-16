import pandas as pd
from PyQt5 import QtWidgets, QtCore
from datetime import date
from Models.TableModel import TableModel
from Datamanager import send_receive_data
from datetime import datetime
import Bill_Print


def generate_invoice_number(prefix, year, current_invoice_number):
    formatted_year = str(year)[-2:]
    formatted_invoice_number = str(current_invoice_number).zfill(3)
    invoice_number = f"{prefix}-{formatted_year}-{formatted_invoice_number}"
    return invoice_number


class TableView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.total_value = None
        self._data = pd.DataFrame(columns=['Name', 'Quantity', 'Price', 'Date', 'Lot Number', 'Expiry Date'])
        self._model = TableModel(data=self._data)
        self.setModel(self._model)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)
        self.setMouseTracking(True)

    def add_item(self, df_line):
        self._data = self._data.append(df_line, ignore_index=True)
        self._model.addRow(df_line)

    def total_price(self):
        self._data["Price"] = pd.to_numeric(self._data["Price"])
        self._data["Quantity"] = pd.to_numeric(self._data["Quantity"])
        self.total_value = (self._data["Price"] * self._data["Quantity"]).sum()
        return str(self.total_value)

    def send_df(self):
        data = self._data.to_dict(orient='records')
        send_receive_data.send_many_data('Sales', self._data)  # send data to database
        return data

    def reset_data(self):
        self._data = pd.DataFrame(columns=['Name', 'Quantity', 'Price', 'Date', 'Lot Number', 'Expiry Date'])
        self._model = TableModel(data=self._data)
        self.setModel(self._model)
        self.reset()

    def delete_selected_item(self):
        selected_row = self.selectionModel().currentIndex().row()
        print(selected_row)
        self._model.removeRow(selected_row)


class SellMedicine(QtWidgets.QDialog):
    onRefreshData1 = QtCore.pyqtSignal()
    onRefreshData2 = QtCore.pyqtSignal()

    def __init__(self, parent, palette):
        super(SellMedicine, self).__init__(parent=parent)
        self.setWindowTitle('Sell Medicine')
        self.setMinimumWidth(1000)
        self.names = send_receive_data.fetch_all_medicine_name('availablestock')

        # -------------------- Dark mode
        self.setPalette(palette)

        # -------------------- Layout
        self.Vertical_layout = QtWidgets.QVBoxLayout(self)

        # -------------------- Table view
        self.sell_table_view = TableView()

        # -------------------- Label for the input field
        self.label_name = QtWidgets.QLabel('Med Name *')
        self.label_quantity = QtWidgets.QLabel('Quantity *')
        self.label_price = QtWidgets.QLabel('Price *')
        self.label_lot = QtWidgets.QLabel('Lot/Batch Number *')
        self.label_date = QtWidgets.QLabel('Selling Date')
        self.label_gst = QtWidgets.QLabel('GST %')

        # -------------------- Total price label
        self.label_total_price = QtWidgets.QLabel()
        self.label_total = QtWidgets.QLabel("Price (ex GST):- ")

        # -------------------- error label in widget
        self.label_error_show = QtWidgets.QLabel()

        # -------------------- Input field for the table view
        self.lineedit_buyer_name = QtWidgets.QLineEdit()
        self.lineedit_name = QtWidgets.QLineEdit()
        self.lineedit_quantity = QtWidgets.QSpinBox()
        self.lineedit_quantity.setValue(0)
        self.lineedit_price = QtWidgets.QLineEdit()
        self.lineedit_lot = QtWidgets.QLineEdit()
        self.lineedit_date = QtWidgets.QDateEdit()

        # -------------------- set the gst True default
        self.lineedit_gst = QtWidgets.QRadioButton('GST ')
        self.lineedit_gst.setChecked(True)

        # -------------------- QCompleter
        # all_med_name = fetch_all_medicine_name()
        self.completer = QtWidgets.QCompleter(self.names)
        self.lineedit_name.setCompleter(self.completer)

        # -------------------- Adding itme to the cash/Credit QComboBox
        self.lineedit_cash_credit = QtWidgets.QComboBox()
        self.lineedit_cash_credit.addItems(['Cash', 'Credit'])

        # -------------------- set Placeholder for the selling date and buyer name
        self.lineedit_buyer_name.setPlaceholderText('Enter Buyer Name')

        # -------------------- Adding label and input field to the
        self.GridLayout = QtWidgets.QGridLayout()
        self.GridLayout.addWidget(self.label_name, 0, 1)
        self.GridLayout.addWidget(self.lineedit_name, 0, 2)
        self.GridLayout.addWidget(self.label_quantity, 0, 3)
        self.GridLayout.addWidget(self.lineedit_quantity, 0, 4)
        self.GridLayout.addWidget(self.label_price, 0, 5)
        self.GridLayout.addWidget(self.lineedit_price, 0, 6)
        self.GridLayout.addWidget(self.label_lot, 1, 1)
        self.GridLayout.addWidget(self.lineedit_lot, 1, 2)
        self.GridLayout.addWidget(self.label_total, 2, 1)
        self.GridLayout.addWidget(self.label_total_price, 2, 2)
        self.GridLayout.addWidget(self.lineedit_buyer_name, 3, 1)
        self.GridLayout.addWidget(self.lineedit_cash_credit, 3, 2)
        self.GridLayout.addWidget(self.lineedit_gst, 3, 4)
        self.GridLayout.addWidget(self.label_date, 3, 5)
        self.GridLayout.addWidget(self.lineedit_date, 3, 6)
        self.GridLayout.addWidget(self.label_error_show, 4, 1)

        # # -------------------- Date QCheckbox login
        self.lineedit_name.textChanged.connect(self.get_medicine_data)

        # ---------------------- set the today's date
        self.lineedit_date.setDate(date.today())

        # -------------------- Generating the invoice number
        self.invoice_number = generate_invoice_number("INV", year=datetime.year,
                                                      current_invoice_number=send_receive_data.
                                                      count_row_in_collection('bills'))

        # -------------------- Initialize the expiry date variable
        self.expiry_data = None

        # -------------------- Creating and adding the buttons
        self.button_add_item = QtWidgets.QPushButton('Add Item')
        self.button_add_item.setEnabled(False)
        self.button_add_item.clicked.connect(self.add_items)

        self.button_delete_item = QtWidgets.QPushButton('Delete Item')
        self.button_delete_item.clicked.connect(self.sell_table_view.delete_selected_item)

        self.button_print_bill = QtWidgets.QPushButton('Print Bill')
        self.button_print_bill.clicked.connect(self.print_bill)

        self.layout2 = QtWidgets.QHBoxLayout()
        self.layout2.addWidget(self.button_add_item)
        self.layout2.addWidget(self.button_delete_item)
        self.layout2.addStretch(1)
        self.layout2.addWidget(self.button_print_bill)

        # -------------------- Adding widget to the layout
        self.Vertical_layout.addWidget(self.sell_table_view, 5)
        self.Vertical_layout.addLayout(self.GridLayout, 3)
        self.Vertical_layout.addLayout(self.layout2, 2)
        self.Vertical_layout.setSpacing(20)

    # ---------------- getting the medicine data according to the name
    def get_medicine_data(self):
        try:
            if self.lineedit_name.text() in self.names:
                data = send_receive_data.fetch_one_data_line('availablestock', self.lineedit_name.text())
                if int(data['Boxes']) == 0:
                    self.button_add_item.setEnabled(False)
                    self.label_error_show.setText("Item Out Of Stocks")
                else:
                    self.lineedit_quantity.setRange(0, data['Boxes'])
                    self.lineedit_price.setText(str(data['Price']))
                    self.lineedit_lot.setText(data['Lot/Batch Number'])
                    self.expiry_data = data['Expiry Date']
                    self.lineedit_lot.setEnabled(False)
                    self.lineedit_price.setEnabled(False)
                    self.button_add_item.setEnabled(True)
                    print(data)
        except Exception as e:
            print(f"Data Not Found: Error - {e}")

    def add_items(self):
        # -------------------- Sending data to the selling table data
        data_dict = {
            'Name': str(self.lineedit_name.text()),
            'Quantity': self.lineedit_quantity.text(),
            'Price': 0 if self.lineedit_price.text() == ' ' else
            int(self.lineedit_price.text()) * 0 if self.lineedit_price == ' '
            else int(self.lineedit_price.text()),
            "Date": str(self.lineedit_date.dateTime().toPyDateTime()),
            'Lot Number': str(self.lineedit_lot.text()),
            'Expiry Date': self.expiry_data
        }
        self.sell_table_view.add_item(data_dict)
        send_receive_data.update_medicine_quantity(self.lineedit_name.text(), int(self.lineedit_quantity.text()))
        self.onRefreshData1.emit()
        self.lineedit_name.clear()
        self.lineedit_quantity.setValue(1)
        self.lineedit_price.setText('0')
        self.lineedit_lot.clear()
        self.lineedit_price.setEnabled(True)
        self.button_add_item.setEnabled(False)
        self.label_total_price.setText(self.sell_table_view.total_price())

    def print_bill(self):
        print(self.lineedit_buyer_name.text())
        try:
            if self.lineedit_buyer_name.text() == '':
                raise "Please Enter the buyer name"
            else:
                gst_amount = ((18 if self.lineedit_gst.isChecked() else 0) / 100) * int(
                    self.sell_table_view.total_price())
                print(gst_amount)
                bill_data = {
                    "_id": self.invoice_number,
                    "Buyer Name": self.lineedit_buyer_name.text(),
                    "Selling date": str(self.lineedit_date.dateTime().toPyDateTime()),
                    "GST": 18 if self.lineedit_gst.isChecked() else 0,
                    "Payment Type": self.lineedit_cash_credit.currentText(),
                    "Medicine Data": self.sell_table_view.send_df(),
                    "Total Price": int(self.sell_table_view.total_price())+gst_amount
                }
                send_receive_data.send_one_data('bills', bill_data)
                Bill_Print.generate_invoice(bill_data, self.invoice_number)
                self.sell_table_view.reset_data()
                self.label_total_price.setText('')
                self.lineedit_buyer_name.setText('')
                self.lineedit_gst.setChecked(True)
                self.onRefreshData2.emit()
        except:
            self.label_error_show.setText("Enter Buyer Name")
