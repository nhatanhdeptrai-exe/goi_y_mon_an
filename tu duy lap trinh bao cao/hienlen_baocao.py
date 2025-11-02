import sys
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMessageBox
from giaodiennew import Ui_MainWindow
from xulymonan2 import xu_ly_gui, chuan_hoa_input, luu_nguyen_lieu_moi

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushtinh.clicked.connect(self.xu_ly_tim_kiem)

    def xu_ly_tim_kiem(self):
        # Lấy dữ liệu từ 2 ô nhập
        text_chinh = self.ui.nguyenlieuchinh.text()
        text_phu = self.ui.nguyenlieuphu.text()

        # Chuẩn hoá & lấy dữ liệu hiển thị
        tap_chinh, tap_phu, hien_chinh, hien_phu = chuan_hoa_input(text_chinh, text_phu)

        # Hiển thị lại phần đã nhận diện
        self.ui.hiennlchinh.setText(f"Nguyên liệu chính: {hien_chinh}")
        self.ui.hiennlphu.setText(f"Nguyên liệu phụ: {hien_phu}")

        # Kiểm tra nếu người dùng nhập nguyên liệu lạ
        if hien_chinh == "(trống)" and hien_phu == "(trống)":
            QMessageBox.warning(
                self,
                "Thông báo",
                "Rất chân thành xin lỗi nhưng nguyên liệu bạn nhập hiện không có trong danh sách."
            )
            # Ghi lại toàn bộ raw input để dev cải thiện sau
            luu_nguyen_lieu_moi("chinh", text_chinh, text_chinh)
            luu_nguyen_lieu_moi("phu", text_phu, text_phu)
            return

        # Gọi xử lý gợi ý món ăn
        ket_qua = xu_ly_gui(text_chinh, text_phu)

        # Đổ dữ liệu vào bảng
        self.ui.tablemonan.setRowCount(len(ket_qua["bang"]))
        for i, (ten, nguyen_lieu_chinh, nguyen_lieu_phu) in enumerate(ket_qua["bang"]):
            self.ui.tablemonan.setItem(i, 0, QtWidgets.QTableWidgetItem(ten))
            self.ui.tablemonan.setItem(i, 1, QtWidgets.QTableWidgetItem(nguyen_lieu_chinh))
            self.ui.tablemonan.setItem(i, 2, QtWidgets.QTableWidgetItem(nguyen_lieu_phu))

        # Căn giữa cột tên món ăn
        self.ui.tablemonan.resizeColumnsToContents()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
