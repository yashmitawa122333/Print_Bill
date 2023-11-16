from PyQt5 import QtWidgets, QtCore
from dateutil.relativedelta import relativedelta
from datetime import date
from Datamanager import send_receive_data
import settings


class AddMedicineDatabase(QtWidgets.QDialog):
    onAddingRow = QtCore.pyqtSignal(dict)

    def __init__(self, parent, palette):
        super(AddMedicineDatabase, self).__init__(parent)
        self.setWindowTitle('Add Item')
        self.setMinimumWidth(400)
        # ------------------- Dark mode
        self.setPalette(palette)

        # ------------------- Layout
        self.GridLayout = QtWidgets.QGridLayout()
        self.VerticalLayout = QtWidgets.QVBoxLayout()
        self.HorizontalLayout = QtWidgets.QHBoxLayout()

        # ------------------- All input field
        self.lineedit_company_name = QtWidgets.QLineEdit()
        self.lineedit_bill_number = QtWidgets.QLineEdit()
        self.lineedit_purchase_date = QtWidgets.QDateEdit()
        self.lineedit_name = QtWidgets.QLineEdit()

        self.lineedit_total_price = QtWidgets.QLineEdit()
        self.lineedit_lot = QtWidgets.QLineEdit()
        self.lineedit_expiry = QtWidgets.QDateEdit()
        self.lineedit_boxes = QtWidgets.QSpinBox()
        self.lineedit_boxes.setRange(0, 10000)

        # ------------------- Labels for all input field
        self.label_company_name = QtWidgets.QLabel('Received By ')
        self.label_bill_number = QtWidgets.QLabel('Bill Number ')
        self.label_purchase_date = QtWidgets.QLabel('Purchase Date ')
        self.label_name = QtWidgets.QLabel('Name ')
        self.label_price = QtWidgets.QLabel('Price/Box ')
        self.label_boxes = QtWidgets.QLabel('Boxes ')
        self.label_lot = QtWidgets.QLabel('Lot/Batch Number ')
        self.label_expiry = QtWidgets.QLabel('Expiry Date ')

        # -------------------- Adding label, input field
        self.GridLayout.addWidget(self.label_company_name, 0, 0)
        self.GridLayout.addWidget(self.lineedit_company_name, 0, 1)
        self.GridLayout.addWidget(self.label_bill_number, 1, 0)
        self.GridLayout.addWidget(self.lineedit_bill_number, 1, 1)
        self.GridLayout.addWidget(self.label_purchase_date, 2, 0)
        self.GridLayout.addWidget(self.lineedit_purchase_date, 2, 1)
        self.GridLayout.addWidget(self.label_name, 3, 0)
        self.GridLayout.addWidget(self.lineedit_name, 3, 1)
        self.GridLayout.addWidget(self.label_price, 4, 0)
        self.GridLayout.addWidget(self.lineedit_total_price, 4, 1)
        self.GridLayout.addWidget(self.label_boxes, 5, 0)
        self.GridLayout.addWidget(self.lineedit_boxes, 5, 1)
        self.GridLayout.addWidget(self.label_lot, 6, 0)
        self.GridLayout.addWidget(self.lineedit_lot, 6, 1)
        self.GridLayout.addWidget(self.label_expiry, 7, 0)
        self.GridLayout.addWidget(self.lineedit_expiry, 7, 1)

        # ------------------- Completer
        self.QCompleter = QtWidgets.QCompleter(settings.medicine_names)
        self.lineedit_name.setCompleter(self.QCompleter)
        # -------------------- Adding today date in the date input field
        today = date.today()
        self.lineedit_purchase_date.setDate(today)
        self.lineedit_expiry.setDate(today + relativedelta(months=6))

        # -------------------- Adding button to the horizontal layout
        self.add_medicine_button = QtWidgets.QPushButton()
        self.add_medicine_button.setText('Add Item')
        self.add_medicine_button.setMaximumWidth(200)

        self.add_medicine_button.clicked.connect(self.send_data_to_database)

        self.HorizontalLayout.addStretch()
        self.HorizontalLayout.addWidget(self.add_medicine_button)

        # -------------------- Adding layout and button to the horizontal layout
        self.VerticalLayout.addLayout(self.GridLayout)
        self.VerticalLayout.addLayout(self.HorizontalLayout)

        self.setLayout(self.VerticalLayout)

    def send_data_to_database(self):
        try:
            get_data = self.get_data_from_widget()
            send_receive_data.send_one_data('availablestock', get_data)
            # --------------- emitting signal to add the new row in the available dataset
            self.onAddingRow.emit(get_data)

        except Exception as e:
            print(f"Error in insertion of item : Error {e}")

    def get_data_from_widget(self):
        try:
            _add_item = {
                "Received By": str(self.lineedit_company_name.text()),
                "Bill Number": str(self.lineedit_bill_number.text()),
                "Purchase Date": str(self.lineedit_purchase_date.dateTime().toPyDateTime()),
                "Name": str(self.lineedit_name.text()),
                "Price": int(int(self.lineedit_total_price.text()) / int(self.lineedit_boxes.text())),
                "Boxes": int(self.lineedit_boxes.text()),
                "Lot/Batch Number": str(self.lineedit_lot.text()),
                "Expiry Date": str(self.lineedit_expiry.dateTime().toPyDateTime()),
                "Total Price": int(self.lineedit_total_price.text())
            }
            self.lineedit_company_name.clear()
            self.lineedit_bill_number.clear()
            self.lineedit_name.clear()
            self.lineedit_total_price.clear()
            self.lineedit_boxes.setValue(0)
            self.lineedit_lot.clear()
            return _add_item

        except Exception as e:
            print(f"No data in widget to upload : Error {e}")
            return None
