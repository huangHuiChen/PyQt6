from PyQt6 import QtWidgets
import sqlalchemy
from ui_Controller import MainWindow_controller
import DB_conn
import qt_ui
import sys
import os

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow_controller()
    MainWindow.show()
    sys.exit(app.exec())