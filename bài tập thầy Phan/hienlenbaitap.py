import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from giaodienbaitap import Ui_giaodienbaitap
from xulybaitap import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_giaodienbaitap()
        self.ui.setupUi(self)
        self.lienketnutlenh()

    def lienketnutlenh(self):
        self.ui.pushtinh.clicked.connect(self.xulynoibo)
        self.ui.pushtinh_1.clicked.connect(self.xulynoibo1)
        self.ui.chung_minh.clicked.connect(self.hien_thong_bao)
        self.ui.pushthoat.clicked.connect(QApplication.quit)

    def xulynoibo(self):
        try:
            n = int(self.ui.nhapn.text())
            a=tinh_Sn(n)
            self.ui.inketqua.setText(a)

        except ValueError:
            QMessageBox.warning(self, "Lỗi nhập liệu", "n thì phải nhập số nhé!")
            self.ui.nhapn.clear()
            self.ui.nhapn.setFocus()

        except Exception as e:
            QMessageBox.critical(self, "Lỗi không xác định", str(e))
    def xulynoibo1(self):
        try:
            s = int(self.ui.nhaps.text())
            e=chung_minh(s)
            self.ui.inketqua_1.setText(e)

        except ValueError:
            QMessageBox.warning(self, "Lỗi nhập liệu", "n thì phải nhập số nhé!")
            self.ui.nhaps.clear()
            self.ui.nhaps.setFocus()

        except Exception as e:
            QMessageBox.critical(self, "Lỗi không xác định", str(e))

    def hien_thong_bao(self):
        QMessageBox.information(
            self,
            "CHỨNG MINH",
            "VỚI 2 SỐ N GIỐNG NHAU TA CÓ THỂ THẤY\nKẾT QUẢ CỦA 2 PHÉP TÍNH ĐỀU BẰNG NHAU")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
