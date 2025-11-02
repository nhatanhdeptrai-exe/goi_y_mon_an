import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from giaodienpso import Ui_MainWindow
from xulyphanso import *  # nếu bạn đã có module xử lý

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.lienketnutlenh()

    def lienketnutlenh(self):
        # kết nối sự kiện click nút
        self.ui.pushtinh.clicked.connect(self.xulynoibo)
        self.ui.pushthoat.clicked.connect(QApplication.quit)

    def xulynoibo(self):
        try:
            a = int(self.ui.lnetua.text())
            b = int(self.ui.lnemaua.text())
            c = int(self.ui.lnetub.text())
            d = int(self.ui.lnemaub_2.text())
            if self.ui.cong.isChecked():
                s=cong(a,b,c,d)
                self.ui.lnekqtu.setText(s)
            if self.ui.tru.isChecked():
                s=tru(a,b,c,d)
                self.ui.lnekqtu.setText(s)
            if self.ui.nhan.isChecked():
                s=nhan(a,b,c,d)
                self.ui.lnekqtu.setText(s)
            if self.ui.chia.isChecked():
                s=chia(a,b,c,d)
                self.ui.lnekqtu.setText(s)

        except ValueError:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập số hợp lệ!")
            self.ui.lnetua.clear()
            self.ui.lnemaua.clear()
            self.ui.lnetub.clear()
            self.ui.lnemaub_2.clear()

        except Exception as e:
            QMessageBox.critical(self, "Lỗi không xác định", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
