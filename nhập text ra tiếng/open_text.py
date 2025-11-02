import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from giaodien_text import Ui_MainWindow
from xuly_text import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.lienketnutlenh()

    def lienketnutlenh(self):
        self.ui.pushnoi.clicked.connect(self.xulynoibo)
        self.ui.pushquit.clicked.connect(QApplication.quit)
    def xulynoibo(self):
        noi_dung = self.ui.lnetext.text()

        if not noi_dung.strip():
            QMessageBox.warning(self, "Lỗi nhập", "Vui lòng nhập nội dung cần đọc!")
            return
        try:
            phat_am_thanh(noi_dung)
            self.ui.lnetext.clear()
            self.ui.lnetext.setFocus()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi phát âm thanh", str(e))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
