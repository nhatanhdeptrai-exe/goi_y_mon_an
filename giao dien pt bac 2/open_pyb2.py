import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from giaodien import Ui_MainWindow
from xulyptb2 import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.lienketnutlenh()

    def lienketnutlenh(self):
        self.ui.pushtinh.clicked.connect(self.xulynoibo)
        self.ui.pushthoat.clicked.connect(QApplication.quit)

    def xulynoibo(self):
        try:
            a = int(self.ui.lnehsa.text())
            b = int(self.ui.lnehsb.text())
            c = int(self.ui.lnehsc.text())
            s = giai_pt_bac2(a, b, c)
            self.ui.lneinketqua.setText(s)

        except ValueError:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập số hợp lệ!")
            self.ui.lnehsa.clear()
            self.ui.lnehsb.clear()
            self.ui.lnehsc.clear()

        except Exception as e:
            QMessageBox.critical(self, "Lỗi không xác định", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
