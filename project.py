import json
import sys
from PyQt6.QtWidgets import QApplication

from interface import QueryWindowGUI

def main():
    # Generate the database instance and connection, modify the parameters as appropriate
    DB_NAME = 'tpch'
    DB_USER = 'postgres'
    DB_PASSWORD = 'postgres'
    DB_HOST = 'localhost'
    PORT = 5432
    
    # Start the GUI
    queryApp = QApplication([])
    queryWindow = QueryWindowGUI(DB_NAME, DB_USER, DB_PASSWORD,DB_HOST, PORT)
    queryWindow.show()
    
    # Allow User to quit from the GUI
    sys.exit(queryApp.exec())


if __name__ == '__main__':
    main()