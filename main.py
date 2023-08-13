import sys
import os
import fitz
from database_manager import DatabaseManager
from label_printer import generate_labels
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QComboBox, QLineEdit, QAction, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QColor, QImage, QPixmap
from PyQt5.uic import loadUi

# ASIN, CONDITION, TOTAL_RETAIL, COST

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
        print_statuses = ["Ready", "Not Ready"]
        statuses = ["Not checked", "Not working", "Working", "Sold", "Sold with tax"]
        colors = [QColor("white"), QColor("red"), QColor("green"), QColor("blue"), QColor("violet")]
        self.table_widget.setRowCount(df.shape[0])
        self.table_widget.setColumnCount(len(columns) + 4)  # Increased by two for the new column
        self.table_widget.setHorizontalHeaderLabels(columns + ["STATUS", "To Print", "Sold Price", "Details"])
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

            # "To Print" Column
            print_status_value = self.df.loc[row, 'TO PRINT'] if 'TO PRINT' in self.df.columns else "Not Ready"
            if print_status_value is None:
                print_status_value = 'Not Ready'
            print_status_combo = QComboBox()
            print_status_combo.addItems(print_statuses)
            print_status_combo.setCurrentIndex(print_statuses.index(print_status_value))
            print_status_combo.currentIndexChanged.connect(lambda index, r=row: self.updatePrintStatus(r, index))
            self.table_widget.setCellWidget(row, len(columns) + 1, print_status_combo)

            sold_price_edit = QLineEdit()
            sold_price_edit.setText(str(self.df.loc[row, 'SOLD PRICE'] if 'SOLD PRICE' in self.df.columns else ""))
            sold_price_edit.textChanged.connect(lambda text, r=row: self.updateSoldPrice(r, text))
            self.table_widget.setCellWidget(row, len(columns) + 2, sold_price_edit)  # Updated index for the new column

            button = QPushButton('Details', self)
            button.setProperty('row', row)
            button.clicked.connect(self.showDetails)
            self.table_widget.setCellWidget(row, len(columns) + 3, button)  # Updated index for the new column

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

    def updatePrintStatus(self, row, index):
        print_statuses = ["Ready", "Not Ready"]
        self.df.loc[row, 'TO PRINT'] = print_statuses[index]

    def updateSoldPrice(self, row, text):
        self.df.loc[row, 'SOLD PRICE'] = text

    def generateAndDisplayLabels(self):
        # Generate the labels PDF
        generate_labels(self.df)

        # Display the generated PDF in the graphicsView widget
        self.loadPDF('labels.pdf')

    def loadPDF(self, filename):
        # Read the PDF file using the fitz library
        pdf_document = fitz.open(filename)
        page = pdf_document.loadPage(0)
        image = page.getPixmap(matrix=fitz.Matrix(1, 1))
        qt_image = QImage(image.samples, image.width, image.height, image.stride, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)

        # Display the image in the QGraphicsView widget
        graphics_view = self.findChild(QGraphicsView, 'graphicsView')
        scene = QGraphicsScene()
        scene.addPixmap(pixmap)
        graphics_view.setScene(scene)

    def initUI(self):
        self.table_widget = self.findChild(QTableWidget, 'tableWidget')
        # self.tab_widget = self.findChild(QTabWidget, 'tab')

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

        self.button_make_labels = self.findChild(QPushButton, 'pushButton_4')
        self.button_make_labels.clicked.connect(self.generateAndDisplayLabels)

        self.button_export_csv = self.findChild(QAction, 'actionExport_CSV')
        self.button_export_csv.triggered.connect(self.db_manager.exportToCSV)

        self.status_bar = self.statusBar()

    def updateStatusBar(self, db_name):
        if db_name:
            self.status_bar.showMessage(f"Current DB: {db_name}")
        else:
            self.status_bar.clearMessage()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()  # <-- Add this line
    sys.exit(app.exec_())