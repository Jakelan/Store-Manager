from datetime import datetime
import os
import pandas as pd
from sqlalchemy import create_engine
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class DatabaseManager:
    def __init__(self, app):
        self.app = app
        self.current_db_name = ""
        self.engine = None  # Initialize the engine attribute to None


    def loadCSV(self, filePath):
        # Create a new database file with a unique name
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        db_name = f'Goosevs_{timestamp}.db'
        self.current_db_name = db_name
        df = pd.read_csv(filePath)
        df['rowid'] = df.index + 1
        df['STATUS'] = 'Not checked'
        df['TO PRINT'] = 'Not Ready'
        df['SOLD PRICE'] = ""  # Adding default SOLD PRICE column
        engine = create_engine(f'sqlite:///{db_name}')
        df.to_sql('store_data', engine, if_exists='fail', index=False)
        self.app.updateTable(df)
        self.app.updateStatusBar(self.current_db_name)
        self.app.loadExistingDatabases()   # Refresh the list of available database files

    def exportToCSV(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getSaveFileName(self.app, "Save CSV File", "", "CSV Files (*.csv);;All Files (*)",
                                                  options=options)
        if filePath:
            if not filePath.endswith('.csv'):
                filePath += '.csv'
            try:
                self.app.df.to_csv(filePath, index=False)
                print(f"Exported to {filePath}")
            except Exception as e:
                print(f"Could not export to CSV: {e}")

    def openFile(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self.app, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)",
                                                  options=options)
        if filePath:
            self.loadCSV(filePath)

    def loadExistingDatabases(self):
        self.databases = [f for f in os.listdir() if f.endswith('.db')]

    def openExistingDB(self, selected_db):
        selected_db = self.app.combo_db.currentText()
        if selected_db:
            # If there is an existing engine, dispose of it
            if self.engine:
                self.engine.dispose()
            self.current_db_name = os.path.basename(selected_db)
            self.database_path = selected_db
            self.engine = create_engine(f'sqlite:///{selected_db}')
            query = 'SELECT * FROM store_data'
            df = pd.read_sql(query, self.engine)
            if 'SOLD PRICE' not in df.columns:  # If SOLD PRICE column doesn't exist
                df['SOLD PRICE'] = ""  # Adding default SOLD PRICE column
            if 'TO PRINT' not in df.columns:  # If TO PRINT column doesn't exist
                df['TO PRINT'] = "Not Ready"  # Adding default TO PRINT column
            self.app.updateTable(df)
            self.app.updateStatusBar(self.current_db_name)
    def getCurrentDBName(self):
        return self.current_db_name
    def getDatabases(self):
        return [f for f in os.listdir() if f.endswith('.db')]

    def saveToDB(self, df):
        if self.database_path:  # Use the database_path argument instead of self.database_path
            engine = create_engine(f'sqlite:///{self.database_path}')
            df.to_sql('store_data', engine, if_exists='replace', index=False)  # Use the df argument instead of self.df
            print("Saved to database:", self.database_path)
        else:
            print("No database selected. Cannot save.")

    def deleteSelectedDB(self):
        selected_db = self.app.combo_db.currentText()
        if selected_db:
            response = QMessageBox.question(self.app, "Delete Database", f"Do you really want to delete {selected_db}?",
                                            QMessageBox.Yes | QMessageBox.No)
            if response == QMessageBox.Yes:
                # If there is an existing engine, dispose of it
                if self.engine:
                    self.engine.dispose()

                try:
                    os.remove(selected_db)
                    self.app.reloadDatabases()  # Refresh the combo box
                    print(f"Deleted {selected_db}")
                except Exception as e:
                    print(f"Could not delete {selected_db}: {e}")