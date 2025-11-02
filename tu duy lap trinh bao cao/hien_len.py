
# run_gui.py
# Hiển thị giao diện PyQt6 (giống Qt Designer) và gọi xử lý từ xulymonan2.py

from PyQt6 import QtWidgets, QtCore
from giaodiennew import Ui_MainWindow
import xulymonan2 as xl

# ---- Vá nhanh cho xulymonan2.luu_nguyen_lieu_moi (file gốc định nghĩa sai tham số) ----
# Hàm chuan_hoa_input() trong xulymonan2 gọi: luu_nguyen_lieu_moi(loai, raw, norm)
# nhưng bản gốc lại chỉ nhận (loai, raw) và còn dùng biến 'norm' chưa khai báo.
# Để tránh lỗi khi chạy GUI, ta "monkey patch" hàm này cho đúng chữ ký.
try:
    import inspect
    sig = inspect.signature(xl.luu_nguyen_lieu_moi)
    if len(sig.parameters) == 2:
        # Thay thế bằng phiên bản an toàn: nhận (loai, raw, norm=None) và ghi JSONL nếu cần.
        def _patched_luu_nguyen_lieu_moi(loai: str, raw: str, norm: str | None = None) -> None:
            try:
                if not (raw and norm):
                    return
                from datetime import datetime
                rec = {
                    "ts": datetime.now().isoformat(timespec="seconds"),
                    "loai": loai,
                    "raw": raw,
                    "norm": norm,
                }
                # Dùng helper sẵn có trong module để ghi JSON Lines
                xl._ghi_json_line(xl.TEP_NGUYEN_LIEU_MOI, rec)
            except Exception:
                # Không để giao diện bị crash vì bất cứ lỗi ghi file nào
                pass
        xl.luu_nguyen_lieu_moi = _patched_luu_nguyen_lieu_moi  # type: ignore[attr-defined]
except Exception:
    # Nếu vì lý do nào đó không vá được, cứ bỏ qua (GUI vẫn chạy, chỉ không log nguyên liệu lạ)
    pass


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Giữ giao diện nhìn "y chang" Designer: dùng chính widget/styling từ .ui đã chuyển
        # Tinh chỉnh nhỏ cho bảng: ẩn số thứ tự hàng và khóa edit
        self.ui.tablemonan.verticalHeader().setVisible(False)
        self.ui.tablemonan.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.tablemonan.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)

        # Sự kiện bấm nút và nhấn Enter trong ô nhập
        self.ui.pushtinh.clicked.connect(self.handle_search)
        self.ui.nguyenlieuchinh.returnPressed.connect(self.ui.pushtinh.click)
        self.ui.nguyenlieuphu.returnPressed.connect(self.ui.pushtinh.click)

    def handle_search(self):
        text_chinh = self.ui.nguyenlieuchinh.text()
        text_phu   = self.ui.nguyenlieuphu.text()

        # Gọi xử lý từ xulymonan2.py
        try:
            result = xl.xu_ly_gui(text_chinh, text_phu)
        except Exception as e:
            # Phòng lỗi ngoài ý muốn: vẫn không để app sập
            result = {"hien_thi_chinh": "(lỗi xử lý)", "hien_thi_phu": "(lỗi xử lý)", "bang": []}

        # Cập nhật 2 label trong GroupBox "NGUYÊN LIỆU ĐÃ NHẬN DIỆN"
        self.ui.hiennlchinh.setText(f"Nguyên liệu chính: {result['hien_thi_chinh']}")
        self.ui.hiennlphu.setText(f"Nguyên liệu phụ: {result['hien_thi_phu']}")

        # Đổ dữ liệu vào bảng (không có cột 'thứ tự')
        rows = len(result["bang"])
        self.ui.tablemonan.setRowCount(rows)

        for r, row_tuple in enumerate(result["bang"]):
            for c, value in enumerate(row_tuple):  # (Tên món, NL chính, NL phụ)
                item = QtWidgets.QTableWidgetItem(value)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.ui.tablemonan.setItem(r, c, item)

        # Tự resize cho vừa đẹp
        self.ui.tablemonan.resizeColumnsToContents()
        self.ui.tablemonan.horizontalHeader().setStretchLastSection(True)


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
