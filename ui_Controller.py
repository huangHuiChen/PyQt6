from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import  QMessageBox, QFileDialog
from qt_ui import Ui_MainWindow
from datetime import datetime
import DB_conn
import os

class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):
        self.ui.timer.timeout.connect(self.show_Time)
        self.ui.timer.start(1000)

        self.ui.pushButton.clicked.connect(self.condute_point)
        self.ui.Btn_Cls.clicked.connect(self.sys_exit)

    def show_Time(self):
        #獲取系統時間
        time = QtCore.QDateTime.currentDateTime()
        display = time.toString('yyyy-MM-dd hh:mm:ss')
        self.ui.Ltime.setText(display)

    def condute_point(self):
        """
        計算金額
        需要資訊: 欄位1+起訖時間
        匯出: 檔案.xlsx
        """
        Obj_B = datetime.strptime(self.ui.date_B.text(), "%Y/%m/%d")
        Date_begin = Obj_B.strftime("%Y%m%d")
        Obj_E = datetime.strptime(self.ui.date_E.text(), "%Y/%m/%d")
        Date_end = Obj_E.strftime("%Y%m%d")
        cond = self.ui.CB_Comp.currentText()[0]

        if Obj_B.strftime("%m") != Obj_E.strftime("%m"):
            QMessageBox.warning(self, "Error", "禁止跨月查詢!")
            return

        fileDir = os.path.join(os.path.expanduser('~'), 'Downloads')   
        try:
            DB_conn.deal_date(int(Date_begin), int(Date_end), cond, fileDir)
            QMessageBox.information(self, "訊息", f'檔案已存於{fileDir}!')
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "Error", "發生錯誤!")
        
    def sys_exit(self):
        reply = QMessageBox.question(self, "訊息", "確認要離開?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        # 判斷使用者操作，關閉視窗
        if reply == QMessageBox.StandardButton.Yes:
            self.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow_controller()
    MainWindow.show()
    sys.exit(app.exec())
        