# --- File: xulymonan2.py --- (Đã nâng cấp)
# Chứa toàn bộ logic xử lý, không tương tác trực tiếp với giao diện.

import unicodedata  # <-- Thêm thư viện để bỏ dấu
import re  # <-- Thêm thư viện Regex để làm sạch
import os  # <-- Thêm để tạo thư mục
import json  # <-- Thêm để ghi file JSONL
from datetime import datetime  # <-- Thêm để lấy ngày giờ

# ==========================================
# 1. CƠ SỞ DỮ LIỆU CỦA HỆ THỐNG
# ==========================================

# 1.1. BẢNG ĐỒNG NGHĨA (Đã rút gọn nhờ unicodedata)
# Giờ đây chỉ cần các từ KHÔNG DẤU
BANG_DONG_NGHIA = {
    # Nguyên liệu chính
    "thit lon": "thit_lon",
    "thit heo": "thit_lon",
    "lon": "thit_lon",
    "heo": "thit_lon",
    "pork": "thit_lon",

    "thit bo": "thit_bo",
    "bo": "thit_bo",
    "beef": "thit_bo",

    "thit ga": "thit_ga",
    "ga": "thit_ga",
    "chicken": "thit_ga",

    "ca": "ca",
    "fish": "ca",

    "trung": "trung",
    "egg": "trung",

    "luon": "luon",
    "vit": "vit",
    "de": "de",

    # Nguyên liệu phụ (đã rút gọn)
    "hanh": "hanh",
    "hanh la": "hanh",
    "toi": "toi",
    "ot": "ot",
    "gung": "gung",
    "khoai tay": "khoai_tay",
    "khoai": "khoai_tay",
    "ca rot": "ca_rot",
    "rau": "rau",
    "mam": "mam",
    "nuoc mam": "mam",
    "muoi": "muoi",
    "tieu": "tieu",
    "mi chinh": "mi_chinh",
    "bot ngot": "mi_chinh",
    "gia vi": "gia_vi",
    "bot nem": "gia_vi",
    "tuong ot": "gia_vi",
}

# 1.2. DANH MỤC NGUYÊN LIỆU CHUẨN
DANH_MUC_CHINH = {
    "thit_lon", "thit_bo", "thit_ga", "ca", "trung", "luon", "vit", "de"
}
DANH_MUC_PHU = {
    "hanh", "toi", "ot", "gung", "khoai_tay", "ca_rot", "rau",
    "mam", "muoi", "gia_vi", "tieu", "mi_chinh"
}

# 1.3. TÊN HIỂN THỊ (Vẫn như cũ)
TEN_HIEN_THI = {
    "thit_lon": "Thịt lợn",
    "thit_bo": "Thịt bò",
    "thit_ga": "Thịt gà",
    "ca": "Cá",
    "trung": "Trứng",
    "luon": "Lươn",
    "vit": "Vịt",
    "de": "Dê",
    "hanh": "Hành",
    "toi": "Tỏi",
    "ot": "Ớt",
    "gung": "Gừng",
    "khoai_tay": "Khoai tây",
    "ca_rot": "Cà rốt",
    "rau": "Rau",
    "mam": "Mắm",
    "muoi": "Muối",
    "gia_vi": "Gia vị",
    "tieu": "Tiêu",
    "mi_chinh": "Mì chính",
}

# 1.4. DATABASE MÓN ĂN (Giữ nguyên logic của bạn)
DATABASE_MON_AN = [
    {
        "ten_mon": "Thịt lợn luộc",
        "nguyen_lieu_chinh_keys": ["thit_lon"],
        "nguyen_lieu_phu_keys": [],
        "tat_ca_nguyen_lieu_set": {"thit_lon"}
    },
    {
        "ten_mon": "Gà luộc",
        "nguyen_lieu_chinh_keys": ["thit_ga"],
        "nguyen_lieu_phu_keys": [],
        "tat_ca_nguyen_lieu_set": {"thit_ga"}
    },
    {
        "ten_mon": "Trứng luộc",
        "nguyen_lieu_chinh_keys": ["trung"],
        "nguyen_lieu_phu_keys": [],
        "tat_ca_nguyen_lieu_set": {"trung"}
    },
    {
        "ten_mon": "Thịt lợn rang",
        "nguyen_lieu_chinh_keys": ["thit_lon"],
        "nguyen_lieu_phu_keys": ["mam"],
        "tat_ca_nguyen_lieu_set": {"thit_lon", "mam"}
    },
    {
        "ten_mon": "Trứng chiên",
        "nguyen_lieu_chinh_keys": ["trung"],
        "nguyen_lieu_phu_keys": ["mam"],
        "tat_ca_nguyen_lieu_set": {"trung", "mam"}
    },
    {
        "ten_mon": "Cá rán",
        "nguyen_lieu_chinh_keys": ["ca"],
        "nguyen_lieu_phu_keys": ["muoi"],
        "tat_ca_nguyen_lieu_set": {"ca", "muoi"}
    },
    {
        "ten_mon": "Gà rang gừng",
        "nguyen_lieu_chinh_keys": ["thit_ga"],
        "nguyen_lieu_phu_keys": ["gung"],
        "tat_ca_nguyen_lieu_set": {"thit_ga", "gung"}
    },
    {
        "ten_mon": "Rau xào tỏi",
        "nguyen_lieu_chinh_keys": [],
        "nguyen_lieu_phu_keys": ["rau", "toi"],
        "tat_ca_nguyen_lieu_set": {"rau", "toi"}
    },
    {
        "ten_mon": "Trứng chiên hành",
        "nguyen_lieu_chinh_keys": ["trung"],
        "nguyen_lieu_phu_keys": ["hanh", "mam"],
        "tat_ca_nguyen_lieu_set": {"trung", "hanh", "mam"}
    },
    {
        "ten_mon": "Thịt lợn kho",
        "nguyen_lieu_chinh_keys": ["thit_lon"],
        "nguyen_lieu_phu_keys": ["mam", "muoi", "hanh"],
        "tat_ca_nguyen_lieu_set": {"thit_lon", "mam", "muoi", "hanh"}
    },
    {
        "ten_mon": "Gà luộc lá chanh",
        "nguyen_lieu_chinh_keys": ["thit_ga"],
        "nguyen_lieu_phu_keys": ["gung", "muoi"],
        "tat_ca_nguyen_lieu_set": {"thit_ga", "gung", "muoi"}
    },
    {
        "ten_mon": "Canh trứng cà rốt",
        "nguyen_lieu_chinh_keys": ["trung"],
        "nguyen_lieu_phu_keys": ["ca_rot", "hanh", "muoi"],
        "tat_ca_nguyen_lieu_set": {"trung", "ca_rot", "hanh", "muoi"}
    },
    {
        "ten_mon": "Thịt lợn kho tiêu",
        "nguyen_lieu_chinh_keys": ["thit_lon"],
        "nguyen_lieu_phu_keys": ["hanh", "toi", "ot", "mam", "muoi", "tieu"],
        "tat_ca_nguyen_lieu_set": {"thit_lon", "hanh", "toi", "ot", "mam", "muoi", "tieu"}
    },
    {
        "ten_mon": "Vịt kho gừng",
        "nguyen_lieu_chinh_keys": ["vit"],
        "nguyen_lieu_phu_keys": ["gung", "toi", "ot", "mam", "gia_vi"],
        "tat_ca_nguyen_lieu_set": {"vit", "gung", "toi", "ot", "mam", "gia_vi"}
    },
    {
        "ten_mon": "Bò xào khoai tây",
        "nguyen_lieu_chinh_keys": ["thit_bo"],
        "nguyen_lieu_phu_keys": ["khoai_tay", "toi", "hanh", "gia_vi"],
        "tat_ca_nguyen_lieu_set": {"thit_bo", "khoai_tay", "toi", "hanh", "gia_vi"}
    }
]

# 1.5. Nơi lưu file log (Nâng cấp)
TEP_NGUYEN_LIEU_MOI = "du_lieu/nguyen_lieu_moi.jsonl"


# ==========================================
# 2. CÁC HÀM XỬ LÝ (Nâng cấp từ file mẫu)
# ==========================================

# --- HÀM LƯU FILE JSONL (Nâng cấp) ---
def _ghi_json_line(path, obj):
    """Ghi 1 dòng JSONLines, tự tạo thư mục nếu cần."""
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    except Exception as e:
        pass  # Bỏ qua lỗi nếu không ghi được file


def luu_nguyen_lieu_moi(loai, raw, norm):
    """
    Lưu nguyên liệu lạ (không có trong vocab) để dev xem lại.
    - loai: 'chinh' hoặc 'phu'
    - raw : người dùng gõ (ví dụ: "Thịt Meow")
    - norm: sau chuẩn hoá (ví dụ: "thit meow")
    """
    if not (raw and norm):
        return
    rec = {
        "time": datetime.now().isoformat(timespec="seconds"),  # Thêm ngày giờ
        "Nguyên liệu": loai,
        "raw": raw,
    }
    _ghi_json_line(TEP_NGUYEN_LIEU_MOI, rec)


# --- HÀM CHUẨN HÓA (Nâng cấp) ---
def bo_dau(s):
    """Bỏ dấu tiếng Việt (ví dụ: "Thịt lợn" -> "Thit lon")."""
    s_norm = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in s_norm if not unicodedata.combining(ch))


def chuan_hoa_tu(token):
    """
    Hàm chuẩn hóa MỘT từ: Bỏ dấu, bỏ ký tự lạ, ánh xạ đồng nghĩa.
    Ví dụ: "Thịt lợn" -> "thit_lon"
    """
    t = (token or "").strip().lower()  # 1. Hạ chữ thường, bỏ None
    t = bo_dau(t)  # 2. Bỏ dấu ("thịt lợn" -> "thit lon")
    t = re.sub(r"[^a-z0-9\s]", " ", t)  # 3. Lọc ký tự lạ (chỉ giữ a-z, 0-9, space)
    t = re.sub(r"\s+", " ", t).strip()  # 4. Gom nhiều khoảng trắng về 1

    # 5. Ánh xạ qua bảng đồng nghĩa (đã rút gọn)
    return BANG_DONG_NGHIA.get(t, t)


def tach_danh_sach(chuoi):
    """Tách chuỗi theo dấu phẩy, bỏ các mục rỗng."""
    if not chuoi:
        return []
    return [m.strip() for m in chuoi.split(",") if m.strip()]


# ==========================================
# 3. HÀM CHÍNH GỌI TỪ GIAO DIỆN
# ==========================================

def tim_kiem_mon_an(input_nguyen_lieu_chinh, input_nguyen_lieu_phu):
    """
    Hàm chính được gọi từ giao diện.
    Đã NÂNG CẤP để dùng các hàm chuẩn hóa và logging mới.
    """

    # 1. Chuẩn bị (Tập hợp tất cả từ vựng hệ thống biết)
    tat_ca_nguyen_lieu_biet = DANH_MUC_CHINH.union(DANH_MUC_PHU)

    # 2. Xử lý chuẩn hóa và Ghi log (Nâng cấp)
    # Tách chuỗi input thành các từ gốc
    ds_chinh_raw = tach_danh_sach(input_nguyen_lieu_chinh)
    ds_phu_raw = tach_danh_sach(input_nguyen_lieu_phu)

    # Chuẩn hóa, lọc từ không biết, và ghi log "âm thầm"
    chinh_da_chuan_hoa = set()
    phu_da_chuan_hoa = set()
    tat_ca_khong_biet = set()

    for raw_token in ds_chinh_raw:
        norm_token = chuan_hoa_tu(raw_token)  # Chạy hàm chuẩn hóa xịn
        if norm_token in tat_ca_nguyen_lieu_biet:
            chinh_da_chuan_hoa.add(norm_token)
        elif norm_token:  # Nếu token lạ và không rỗng
            luu_nguyen_lieu_moi("chinh", raw_token, norm_token)  # Âm thầm ghi log
            tat_ca_khong_biet.add(raw_token) #SỬA ĐI EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE

    for raw_token in ds_phu_raw:
        norm_token = chuan_hoa_tu(raw_token)  # Chạy hàm chuẩn hóa xịn
        if norm_token in tat_ca_nguyen_lieu_biet:
            phu_da_chuan_hoa.add(norm_token)
        elif norm_token:  # Nếu token lạ và không rỗng
            luu_nguyen_lieu_moi("phu", raw_token, norm_token)  # Âm thầm ghi log
            tat_ca_khong_biet.add(raw_token)

    # (Không cần gọi hàm luu_nguyen_lieu_khong_biet cũ nữa)

    # 3. Tìm kiếm món ăn (Giữ nguyên logic "isdisjoint" của bạn)
    danh_sach_goi_y = []
    cac_mon_chinh_nguoi_dung_co = chinh_da_chuan_hoa.intersection(DANH_MUC_CHINH)
    cac_mon_phu_nguoi_dung_co = phu_da_chuan_hoa.intersection(DANH_MUC_PHU)

    for mon_an in DATABASE_MON_AN:
        set_chinh_yeu_cau = set(mon_an["nguyen_lieu_chinh_keys"])
        set_phu_yeu_cau = set(mon_an["nguyen_lieu_phu_keys"])

        la_mon_goi_y = False

        if cac_mon_chinh_nguoi_dung_co:
            if not cac_mon_chinh_nguoi_dung_co.isdisjoint(set_chinh_yeu_cau): #EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
                la_mon_goi_y = True
        elif not cac_mon_chinh_nguoi_dung_co and cac_mon_phu_nguoi_dung_co:
            if not cac_mon_phu_nguoi_dung_co.isdisjoint(set_phu_yeu_cau):
                if not set_chinh_yeu_cau:
                    la_mon_goi_y = True

        if la_mon_goi_y:
            ten_nl_chinh = ", ".join([TEN_HIEN_THI.get(key, key) for key in mon_an["nguyen_lieu_chinh_keys"]])
            ten_nl_phu = ", ".join([TEN_HIEN_THI.get(key, key) for key in mon_an["nguyen_lieu_phu_keys"]])

            mon_an_tim_thay = {
                "ten": mon_an["ten_mon"],
                "chinh": ten_nl_chinh if ten_nl_chinh else "Không có",
                "phu": ten_nl_phu if ten_nl_phu else "Không có"
            }
            danh_sach_goi_y.append(mon_an_tim_thay)

    # 4. Chuẩn bị chuỗi hiển thị
    chinh_nhan_dien_list = [TEN_HIEN_THI.get(key, key) for key in chinh_da_chuan_hoa if key in DANH_MUC_CHINH]
    phu_nhan_dien_list = [TEN_HIEN_THI.get(key, key) for key in phu_da_chuan_hoa if key in DANH_MUC_PHU]

    str_chinh_nhan_dien = ", ".join(chinh_nhan_dien_list)
    str_phu_nhan_dien = ", ".join(phu_nhan_dien_list)

    # 5. Trả về kết quả (Vẫn 3 giá trị như cũ)
    # File hienlen_baocao2.py của bạn không cần sửa gì cả
    return (str_chinh_nhan_dien, str_phu_nhan_dien, danh_sach_goi_y, tat_ca_khong_biet)