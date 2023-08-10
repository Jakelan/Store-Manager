# Store Management App

## Overview

The Store Management App is a desktop application developed in Python using the PyQt5 library. It offers an intuitive graphical user interface for managing store inventory. With features like loading data from CSV files, saving to SQLite databases, and modifying the status and sold price of items, it provides a comprehensive solution for small to medium-sized retail stores.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [Support](#support)
- [License](#license)

## Features

- **Load CSV Files**: Import inventory data from CSV files.
- **SQLite Database Support**: Open, create, and manage SQLite databases.
- **Status Management**: Modify the status of items (e.g., Not Checked, Working, Sold).
- **Edit Sold Prices**: Easily update the sold prices for individual items.
- **Detailed Views**: View detailed information about each item.
- **Save Functionality**: Save changes directly to the SQLite database.
- **Intuitive UI**: A user-friendly interface that's easy to navigate and use.

## Installation

### Prerequisites

Make sure you have Python 3.x installed along with the following libraries:

- PyQt5
- pandas
- sqlalchemy

You can install these libraries using pip:

```bash
pip install PyQt5 pandas sqlalchemy
```

### Running the Application

1. Clone the repository:

```bash
git clone https://github.com/Jakelan/Store-Manager.git
```

2. Navigate to the project directory:

```bash
cd goosevs-store
```

3. Run the main script:

```bash
python main.py
```

## Usage

1. **Open CSV**: Click the 'Open CSV' button to load a CSV file.
2. **Open Existing DB**: Select an existing SQLite database from the dropdown and click 'Open Existing DB.'
3. **Edit Records**: You can edit the status and sold price of items directly in the table.
4. **View Details**: Click 'Details' to see more information about an item.
5. **Save**: Click 'Save' to save any changes to the database.

## Screenshots

(You can insert images here to give users a visual idea of the application)

## Contributing

We welcome contributions from the community. Please read our [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## Support

If you encounter any issues or have questions about the application, please open an [issue](https://github.com/your-username/goosevs-store/issues) on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
