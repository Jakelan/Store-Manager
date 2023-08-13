# Database Manager for Store Items

## Overview

This application provides a graphical user interface for managing a store's inventory. Built with Python and PyQt5, it enables users to perform various database operations, such as importing data from CSV files, saving data to SQLite databases, managing different databases, and exporting data to CSV files.

The user can view item details, update statuses, and see sold prices for individual items within the application.

## Features

- Import data from CSV files.
- Export data to CSV files.
- Open existing SQLite databases.
- Save changes to the SQLite databases.
- View and edit the status of individual items.
- Delete selected databases.

## Prerequisites

You'll need the following packages installed:

- Python (3.x recommended)
- PyQt5
- pandas
- sqlalchemy

## Installation

You can install the required packages using pip:

    ```bash
    pip install PyQt5 pandas sqlalchemy
    ```

## Running the Application

1. Clone the repository:

    ```bash
    git clone https://github.com/Jakelan/Store-Manager.git
    ```

2. Navigate to the directory:

    ```bash
    cd your-repository
    ```

3. Run the `main.py` script:

    ```bash
    python main.py
    ```

The application window will open, and you can begin managing your databases.

## Usage

- **Open CSV**: Import a CSV file into a new database.
- **Open Existing DB**: Select an existing database from the dropdown.
- **Save DB**: Save changes to the selected database.
- **Export CSV**: Export the current table to a CSV file.
- **Delete DB**: Delete the selected database.

## License

[MIT License](LICENSE.md) or whatever license you prefer.

