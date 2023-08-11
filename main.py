import sys
import os
from database_manager import DatabaseManager
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QWidget, QComboBox, QLineEdit, QAction, QMessageBox
from PyQt5.QtGui import QColor
from PyQt5.uic import loadUi

class DetailsWindow(QWidget):
    def __init__(self, details):
        super().__init__()
        layout = QVBoxLayout()
        table = QTableWidget()
        table.setRowCount(len(details))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Key", "Value"])
        for row, (key, value) in enumerate(details.items()):
            table.setItem(row, 0, QTableWidgetItem(str(key)))
            table.setItem(row, 1, QTableWidgetItem(str(value)))
        layout.addWidget(table)
        self.setLayout(layout)
        self.setWindowTitle('Details')
        self.show()

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.databases = []
        self.loadExistingDatabases()
        self.database_path = None
        self.db_manager = DatabaseManager(self)
        loadUi('myqtui.ui', self) # Load the UI file
        self.initUI()

    def reloadDatabases(self):
        self.databases = self.db_manager.getDatabases()  # Get the updated list of databases
        self.combo_db.clear()  # Clear the current items in the combo box
        self.combo_db.addItems(self.databases)

    def showDetails(self):
        button = self.sender()
        row = button.property('row')
        details = self.df.loc[row].to_dict()
        self.details_window = DetailsWindow(details)
    def loadExistingDatabases(self):  # Move this method to App class
        self.databases = [f for f in os.listdir() if f.endswith('.db')]

    def updateTable(self, df):
        self.df = df
        columns = ["Item Desc", "ASIN", "EAN", "COST", "TOTAL RETAIL", "CONDITION"]
        statuses = ["Not checked", "Not working", "Working", "Sold", "Sold with tax"]
        colors = [QColor("white"), QColor("red"), QColor("green"), QColor("blue"), QColor("violet")]
        self.table_widget.setRowCount(df.shape[0])
        self.table_widget.setColumnCount(len(columns) + 3)  # Increased by one for the new column
        self.table_widget.setHorizontalHeaderLabels(columns + ["STATUS", "Sold Price", "Details"])
        for row, item in df[columns].iterrows():
            for col, value in enumerate(item):
                self.table_widget.setItem(row, col, QTableWidgetItem(str(value)))
            status_value = self.df.loc[row, 'STATUS']
            if status_value is None:
                status_value = 'Not checked'
            status_combo = QComboBox()
            status_combo.addItems(statuses)
            status_combo.setCurrentIndex(statuses.index(status_value))
            status_combo.currentIndexChanged.connect(lambda index, r=row: self.updateStatus(r, index))
            self.table_widget.setCellWidget(row, len(columns), status_combo)
            self.updateStatus(row, statuses.index(status_value))
            button = QPushButton('Details', self)
            button.setProperty('row', row)
            button.clicked.connect(self.showDetails)
            self.table_widget.setCellWidget(row, len(columns) + 2, button)
            sold_price_edit = QLineEdit()
            sold_price_edit.setText(str(self.df.loc[row, 'SOLD PRICE'] if 'SOLD PRICE' in self.df.columns else ""))
            sold_price_edit.textChanged.connect(lambda text, r=row: self.updateSoldPrice(r, text))
            self.table_widget.setCellWidget(row, len(columns) + 1, sold_price_edit)

    def updateStatus(self, row, index):
        statuses = ["Not checked", "Not working", "Working", "Sold", "Sold with tax"]
        colors = [QColor("white"), QColor("red"), QColor("green"), QColor("blue"), QColor("violet")]
        self.df.loc[row, 'STATUS'] = statuses[index]
        for col in range(self.table_widget.columnCount() - 2):
            item = self.table_widget.item(row, col)
            if item is None:  # Check if the item is None and create it if necessary
                item = QTableWidgetItem()
                self.table_widget.setItem(row, col, item)
            item.setBackground(colors[index])

    def updateSoldPrice(self, row, text):
        self.df.loc[row, 'SOLD PRICE'] = text

    def initUI(self):
        self.table_widget = self.findChild(QTableWidget, 'tableWidget')

        self.button_open_csv = self.findChild(QAction, 'actionOpen_CSV')
        self.button_open_csv.triggered.connect(self.db_manager.openFile)

        self.button_open_db = self.findChild(QPushButton, 'pushButton_2')
        self.button_open_db.clicked.connect(self.db_manager.openExistingDB)

        self.combo_db = self.findChild(QComboBox, 'comboBox')
        self.combo_db.addItems(self.databases)

        self.button_save = self.findChild(QAction, 'actionSave_DB')
        self.button_save.triggered.connect(lambda: self.db_manager.saveToDB(self.df))

        self.button_reload_databases = self.findChild(QPushButton, 'pushButton')
        self.button_reload_databases.clicked.connect(self.reloadDatabases)

        self.button_delete_db = self.findChild(QPushButton, 'pushButton_3')
        self.button_delete_db.clicked.connect(self.db_manager.deleteSelectedDB)

        self.button_export_csv = self.findChild(QAction, 'actionExport_CSV')
        self.button_export_csv.triggered.connect(self.db_manager.exportToCSV)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()  # <-- Add this line
    sys.exit(app.exec_())
