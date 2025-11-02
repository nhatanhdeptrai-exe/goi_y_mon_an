# --- File: main.py ---
# File này dùng để khởi chạy ứng dụng

import sys

# Quan trọng: Phải dùng PyQt6 vì file giaodiennew.py được tạo bằng PyQt6
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox

# 1. Import lớp Ui_MainWindow từ file giao diện của bạn
from giaodiennew import Ui_MainWindow

# 2. Import file xử lý của bạn (dùng "as xuly" để gọi cho ngắn)
import xulymonan3 as xuly


class UngDungGoiYMonAn(QMainWindow):
    def __init__(self):
        super().__init__()

        # 3. Khởi tạo giao diện từ file "giaodiennew.py"
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Việc gọi self.ui.setupUi(self) đã tự động tải tất cả style
        # nên giao diện sẽ "y chang như trên qt designer"

        # Sửa lại tiêu đề cửa sổ cho đẹp
        self.setWindowTitle("Hệ thống gợi ý món ăn")
        self.ui.tablemonan.verticalHeader().setVisible(False)
        self.ui.pushtinh.clicked.connect(self.thuc_hien_tim_kiem)

    def thuc_hien_tim_kiem(self):
        """
        Hàm này là cầu nối: Lấy data từ UI -> Gọi file xử lý -> Đẩy data lên UI
        (ĐÃ CẬP NHẬT ĐỂ KHỚP VỚI GIAO DIỆN MỚI)
        """

        # --- BƯỚC 1: Lấy input từ giao diện ---
        # Lấy text từ "Nguyên liệu thịt" (dù widget tên là 'nguyenlieuchinh')
        input_thit_tu_ui = self.ui.nguyenlieuchinh.text()
        # Lấy text từ "Nguyên liệu rau" (dù widget tên là 'nguyenlieuphu')
        input_rau_tu_ui = self.ui.nguyenlieuphu.text()

        # --- BƯỚC 2: Gọi hàm xử lý từ file 'xulymonan3.py' ---
        # Gọi hàm với 2 biến mới, và hứng 4 giá trị trả về
        (thit_da_nhan_dien, rau_va_giavi_da_nhan_dien, danh_sach_goi_y, cac_tu_khong_biet) = xuly.tim_kiem_mon_an(
            input_thit_tu_ui,
            input_rau_tu_ui)

        # --- BƯỚC 3: Khối code kiểm tra tín hiệu và hành động ---
        if cac_tu_khong_biet:
            # 1. Hiện thông báo "Xin lỗi"
            QMessageBox.warning(self,
                                "Không nhận diện được",
                                "Xin lỗi vì hiện tại hệ thống chưa có dữ liệu về nguyên liệu của bạn.\n"
                                "Chúng tôi đã lưu lại những nguyên liệu này và sẽ bổ sung trong tương lai.")

            # 2. Xóa (clear) cả hai ô nhập
            self.ui.nguyenlieuchinh.clear()
            self.ui.nguyenlieuphu.clear()

            # 3. Focus (trỏ chuột) vào ô đầu tiên
            self.ui.nguyenlieuchinh.setFocus()

        # --- BƯỚC 4: Cập nhật kết quả lên giao diện ---
        # (Đây là phần quan trọng nhất bạn hỏi)

        # 4a. Cập nhật 2 label hiển thị với 2 biến kết quả mới
        # self.ui.hiennlchinh là label có text "Nguyên liệu thịt: "
        self.ui.hiennlchinh.setText(f"Nguyên liệu thịt: {thit_da_nhan_dien}")
        # self.ui.hiennlphu là label có text "Nguyên liệu rau: "
        self.ui.hiennlphu.setText(f"Nguyên liệu rau: {rau_va_giavi_da_nhan_dien}")

        # (Thêm code ép màu đen để phòng lỗi Dark Mode)
        self.ui.hiennlchinh.setStyleSheet("color: black;")
        self.ui.hiennlphu.setStyleSheet("color: black;")

        # 4b. Cập nhật dữ liệu vào bảng 'tablemonan'
        # Bảng này sẽ TỰ ĐỘNG CÓ CẢ MÓN THỊT VÀ RAU
        # vì 'danh_sach_goi_y' đã chứa cả hai
        self.ui.tablemonan.setRowCount(0)

        for row_index, mon_an in enumerate(danh_sach_goi_y):
            self.ui.tablemonan.insertRow(row_index)
            self.ui.tablemonan.setItem(row_index, 0, QTableWidgetItem(mon_an["ten"]))
            self.ui.tablemonan.setItem(row_index, 1, QTableWidgetItem(mon_an["chinh"]))
            self.ui.tablemonan.setItem(row_index, 2, QTableWidgetItem(mon_an["phu"]))


# --- Khối mã tiêu chuẩn để chạy ứng dụng PyQt6 ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UngDungGoiYMonAn()
    window.show()
    sys.exit(app.exec())