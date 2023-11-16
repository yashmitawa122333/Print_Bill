from PyQt5 import QtWidgets, QtCore, QtGui
from Dialogs.Add_medicine_database import AddMedicineDatabase
from Dialogs.Sell_medicine import SellMedicine
from Dialogs.all_bills import AllBills


class ButtonWidget(QtWidgets.QFrame):
    def __init__(self, parent, palette):
        super(ButtonWidget, self).__init__(parent)

        self.parent_palette = palette

        # -------------------- Connect dialog box
        self.add_medicine_dialog = AddMedicineDatabase(self, palette=self.parent_palette)
        self.sell_medicine_dialog = SellMedicine(self, palette=self.parent_palette)
        self.all_bills = AllBills(self, palette=self.parent_palette)
        # -------------------- Layout
        self.buttons_layout = QtWidgets.QVBoxLayout(self)
        self.layout1 = QtWidgets.QVBoxLayout()
        self.layout2 = QtWidgets.QVBoxLayout()

        # -------------------- Creating buttons
        self.add_medicine_to_database = QtWidgets.QPushButton()
        self.add_medicine_to_database.setText('Purchase')
        self.add_medicine_to_database.setMaximumWidth(200)
        self.sell_medicine = QtWidgets.QPushButton()
        self.sell_medicine.setText('Sell')
        self.sell_medicine.setMaximumWidth(200)
        self.bill_data = QtWidgets.QPushButton("Bill Data")
        self.bill_data.setMaximumWidth(200)
        self.credit_note = QtWidgets.QPushButton()
        self.credit_note.setText('Credit Note')
        self.credit_note.setMaximumWidth(200)
        self.debit_note = QtWidgets.QPushButton()
        self.debit_note.setText('Debit Note')
        self.debit_note.setMaximumWidth(200)

        # --------------- Connecting buttons to the dialog box
        self.add_medicine_to_database.clicked.connect(self.add_medicine_to_database_function)
        self.sell_medicine.clicked.connect(self.sell_medicine_function)
        self.bill_data.clicked.connect(self.all_bill_data)

        # --------------- Adding buttons to the widget
        self.layout1.addStretch(1)
        self.layout2.addStretch(1)
        self.layout1.addWidget(self.add_medicine_to_database)
        self.layout1.addWidget(self.sell_medicine)
        self.layout2.addWidget(self.bill_data)
        # self.layout2.addWidget(self.credit_note)
        # self.layout2.addWidget(self.debit_note)

        # --------------- Adding button layout to the button frame
        # self.buttons_layout.addLayout(self.layout1)
        self.buttons_layout.addLayout(self.layout1, 8)
        self.buttons_layout.addLayout(self.layout2, 2)

    def add_medicine_to_database_function(self):
        if self.add_medicine_dialog is not None:
            self.add_medicine_dialog.show()
        else:
            self.add_medicine_dialog = AddMedicineDatabase(self, palette=self.parent_palette)
            self.add_medicine_dialog.show()

    def sell_medicine_function(self):
        if self.sell_medicine_dialog is not None:
            self.sell_medicine_dialog.show()
        else:
            self.sell_medicine_dialog = SellMedicine(self, palette=self.parent_palette)
            self.sell_medicine_dialog.show()

    def all_bill_data(self):
        if self.all_bills is not None:
            self.all_bills.show()
        else:
            self.all_bills = AllBills(self, palette=self.parent_palette)
            self.all_bills.show()
