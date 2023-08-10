import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget, QComboBox, QLineEdit
from PyQt5.QtGui import QColor
import pandas as pd
from sqlalchemy import create_engine

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
        self.title = 'Store Management App'
        self.left = 100
        self.top = 100
        self.width = 1600
        self.height = 1200
        self.initUI()

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
        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(50, 50, 1200, 800)
        button = QPushButton('Open CSV', self)
        button.setToolTip('Click here to open a CSV file')
        button.move(50, 850)
        button.clicked.connect(self.openFile)

        button_db = QPushButton('Open Existing DB', self)
        button_db.setToolTip('Click here to open an existing database file')
        button_db.move(250, 850)
        button_db.clicked.connect(self.openExistingDB)

        self.combo_db = QComboBox(self)
        self.combo_db.addItems(self.databases)
        self.combo_db.move(400, 850)

        button_save = QPushButton('Save', self)
        button_save.setToolTip('Click here to save changes to the database')
        button_save.move(650, 850)
        button_save.clicked.connect(self.saveToDB)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def loadCSV(self, filePath):
        # Create a new database file with a unique name
        import uuid
        db_name = f'store_{uuid.uuid4().hex}.db'

        df = pd.read_csv(filePath)
        df['rowid'] = df.index + 1
        df['STATUS'] = 'Not checked'
        df['SOLD PRICE'] = ""  # Adding default SOLD PRICE column
        engine = create_engine(f'sqlite:///{db_name}')
        df.to_sql('store_data', engine, if_exists='fail', index=False)
        self.updateTable(df)
        self.loadExistingDatabases()  # Refresh the list of available database files

    def openFile(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if filePath:
            self.loadCSV(filePath)

    def showDetails(self):
        button = self.sender()
        row = button.property('row')
        details = self.df.loc[row].to_dict()
        self.details_window = DetailsWindow(details)

    def loadExistingDatabases(self):
        self.databases = [f for f in os.listdir() if f.endswith('.db')]

    def openExistingDB(self):
        selected_db = self.combo_db.currentText()
        if selected_db:
            self.database_path = selected_db
            engine = create_engine(f'sqlite:///{selected_db}')
            query = 'SELECT * FROM store_data'
            df = pd.read_sql(query, engine)
            if 'SOLD PRICE' not in df.columns:  # If SOLD PRICE column doesn't exist
                df['SOLD PRICE'] = ""  # Adding default SOLD PRICE column
            self.updateTable(df)

    def saveToDB(self):
        if self.database_path:
            engine = create_engine(f'sqlite:///{self.database_path}')
            self.df.to_sql('store_data', engine, if_exists='replace', index=False)
            print("Saved to database:", self.database_path)
        else:
            print("No database selected. Cannot save.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
