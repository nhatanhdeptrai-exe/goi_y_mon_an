# --- File: xulymonan2.py --- (Đã nâng cấp logic "Rau là chính")
# Chứa toàn bộ logic xử lý, không tương tác trực tiếp với giao diện.

import unicodedata
import re
import os
import json
from datetime import datetime

# ==========================================
# 1. CƠ SỞ DỮ LIỆU CỦA HỆ THỐNG
# ==========================================

# 1.1. BẢNG ĐỒNG NGHĨA
BANG_DONG_NGHIA = {
    # Nguyên liệu chính (Thịt)
    "thit lon": "thit_lon", "thit heo": "thit_lon", "lon": "thit_lon", "heo": "thit_lon", "pork": "thit_lon",
    "thit bo": "thit_bo", "bo": "thit_bo", "beef": "thit_bo",
    "thit ga": "thit_ga", "ga": "thit_ga", "chicken": "thit_ga",
    "ca": "ca", "fish": "ca",
    "trung": "trung", "egg": "trung",
    "luon": "luon", "vit": "vit", "de": "de",

    # Nguyên liệu chính (Rau/Củ) <-- THAY ĐỔI
    "rau": "rau",
    "rau cai": "rau_cai",  # <-- Thêm mới
    "khoai tay": "khoai_tay", "khoai": "khoai_tay",
    "ca rot": "ca_rot",

    # Nguyên liệu phụ (Gia vị)
    "hanh": "hanh", "hanh la": "hanh",
    "toi": "toi", "ot": "ot", "gung": "gung",
    "mam": "mam", "nuoc mam": "mam",
    "muoi": "muoi", "tieu": "tieu",
    "mi chinh": "mi_chinh", "bot ngot": "mi_chinh",
    "gia vi": "gia_vi", "bot nem": "gia_vi", "tuong ot": "gia_vi",
}

# 1.2. DANH MỤC NGUYÊN LIỆU CHUẨN (THAY ĐỔI)
DANH_MUC_CHINH = {
    # Thịt
    "thit_lon", "thit_bo", "thit_ga", "ca", "trung", "luon", "vit", "de",
    # Rau (Chuyển từ phụ lên chính)
    "rau", "khoai_tay", "ca_rot", "rau_cai"
}
DANH_MUC_PHU = {
    # Chỉ còn gia vị
    "hanh", "toi", "ot", "gung",
    "mam", "muoi", "gia_vi", "tieu", "mi_chinh"
}

# 1.3. TÊN HIỂN THỊ (THAY ĐỔI)
TEN_HIEN_THI = {
    "thit_lon": "Thịt lợn", "thit_bo": "Thịt bò", "thit_ga": "Thịt gà",
    "ca": "Cá", "trung": "Trứng", "luon": "Lươn", "vit": "Vịt", "de": "Dê",

    "rau": "Rau", "khoai_tay": "Khoai tây", "ca_rot": "Cà rốt", "rau_cai": "Rau cải",  # <-- Cập nhật

    "hanh": "Hành", "toi": "Tỏi", "ot": "Ớt", "gung": "Gừng",
    "mam": "Mắm", "muoi": "Muối", "gia_vi": "Gia vị", "tieu": "Tiêu", "mi_chinh": "Mì chính",
}

# 1.4. DATABASE MÓN ĂN (THAY ĐỔI)
DATABASE_MON_AN = [
    # Món thịt
    {"ten_mon": "Thịt lợn luộc", "nguyen_lieu_chinh_keys": ["thit_lon"], "nguyen_lieu_phu_keys": [],
     "tat_ca_nguyen_lieu_set": {"thit_lon"}},
    {"ten_mon": "Gà luộc", "nguyen_lieu_chinh_keys": ["thit_ga"], "nguyen_lieu_phu_keys": [],
     "tat_ca_nguyen_lieu_set": {"thit_ga"}},
    {"ten_mon": "Trứng luộc", "nguyen_lieu_chinh_keys": ["trung"], "nguyen_lieu_phu_keys": [],
     "tat_ca_nguyen_lieu_set": {"trung"}},
    {"ten_mon": "Thịt lợn rang", "nguyen_lieu_chinh_keys": ["thit_lon"], "nguyen_lieu_phu_keys": ["mam"],
     "tat_ca_nguyen_lieu_set": {"thit_lon", "mam"}},
    {"ten_mon": "Trứng chiên", "nguyen_lieu_chinh_keys": ["trung"], "nguyen_lieu_phu_keys": ["mam"],
     "tat_ca_nguyen_lieu_set": {"trung", "mam"}},
    {"ten_mon": "Cá rán", "nguyen_lieu_chinh_keys": ["ca"], "nguyen_lieu_phu_keys": ["muoi"],
     "tat_ca_nguyen_lieu_set": {"ca", "muoi"}},
    {"ten_mon": "Gà rang gừng", "nguyen_lieu_chinh_keys": ["thit_ga"], "nguyen_lieu_phu_keys": ["gung"],
     "tat_ca_nguyen_lieu_set": {"thit_ga", "gung"}},
    {"ten_mon": "Trứng chiên hành", "nguyen_lieu_chinh_keys": ["trung"], "nguyen_lieu_phu_keys": ["hanh", "mam"],
     "tat_ca_nguyen_lieu_set": {"trung", "hanh", "mam"}},
    {"ten_mon": "Thịt lợn kho", "nguyen_lieu_chinh_keys": ["thit_lon"], "nguyen_lieu_phu_keys": ["mam", "muoi", "hanh"],
     "tat_ca_nguyen_lieu_set": {"thit_lon", "mam", "muoi", "hanh"}},

    # Món rau (Rau là NL Chính)
    {
        "ten_mon": "Rau cải luộc",  # <-- Món mới
        "nguyen_lieu_chinh_keys": ["rau_cai"],
        "nguyen_lieu_phu_keys": ["muoi"],
        "tat_ca_nguyen_lieu_set": {"rau_cai", "muoi"}
    },
    {
        "ten_mon": "Rau xào tỏi",
        "nguyen_lieu_chinh_keys": ["rau"],  # <-- Chuyển "rau" lên chính
        "nguyen_lieu_phu_keys": ["toi"],
        "tat_ca_nguyen_lieu_set": {"rau", "toi"}
    },

    # Món kết hợp (Cả 2 đều là NL Chính)
    {
        "ten_mon": "Canh trứng cà rốt",
        "nguyen_lieu_chinh_keys": ["trung", "ca_rot"],  # <-- "ca_rot" là chính
        "nguyen_lieu_phu_keys": ["hanh", "muoi"],
        "tat_ca_nguyen_lieu_set": {"trung", "ca_rot", "hanh", "muoi"}
    },
    {
        "ten_mon": "Bò xào khoai tây",
        "nguyen_lieu_chinh_keys": ["thit_bo", "khoai_tay"],  # <-- "khoai_tay" là chính
        "nguyen_lieu_phu_keys": ["toi", "hanh", "gia_vi"],
        "tat_ca_nguyen_lieu_set": {"thit_bo", "khoai_tay", "toi", "hanh", "gia_vi"}
    },
]

# 1.5. Nơi lưu file log
TEP_NGUYEN_LIEU_MOI = "du_lieu/nguyen_lieu_moi.jsonl"


# ==========================================
# 2. CÁC HÀM XỬ LÝ (Giữ nguyên, không đổi)
# ==========================================

def _ghi_json_line(path, obj):
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    except Exception as e:
        pass


def luu_nguyen_lieu_moi(loai, raw, norm):
    if not (raw and norm):
        return
    rec = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "Nguyên liệu": loai,
        "raw": raw,
    }
    _ghi_json_line(TEP_NGUYEN_LIEU_MOI, rec)


def bo_dau(s):
    s_norm = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in s_norm if not unicodedata.combining(ch))


def chuan_hoa_tu(token):
    t = (token or "").strip().lower()
    t = bo_dau(t)
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return BANG_DONG_NGHIA.get(t, t)


def tach_danh_sach(chuoi):
    if not chuoi:
        return []
    return [m.strip() for m in chuoi.split(",") if m.strip()]


# ==========================================
# 3. HÀM CHÍNH GỌI TỪ GIAO DIỆN (THAY ĐỔI)
# ==========================================

def tim_kiem_mon_an(input_nguyen_lieu_thit, input_nguyen_lieu_rau):  # <-- Đổi tên biến
    """
    Hàm chính được gọi từ giao diện.
    LOGIC THAY ĐỔI: Nhận 2 input "thịt" và "rau", coi cả 2 là NGUYÊN LIỆU CHÍNH.
    Gia vị (mắm, muối) nếu người dùng nhập vào 1 trong 2 ô, vẫn được coi là PHỤ.
    """

    # 1. Chuẩn bị
    tat_ca_nguyen_lieu_biet = DANH_MUC_CHINH.union(DANH_MUC_PHU)

    # 2. Xử lý chuẩn hóa và Ghi log
    ds_thit_raw = tach_danh_sach(input_nguyen_lieu_thit)
    ds_rau_raw = tach_danh_sach(input_nguyen_lieu_rau)

    chinh_da_chuan_hoa_THIT = set()  # <-- Set riêng cho thịt
    chinh_da_chuan_hoa_RAU = set()  # <-- Set riêng cho rau
    phu_da_chuan_hoa_CHUNG = set()  # <-- Set chung cho gia vị
    tat_ca_khong_biet = set()

    # Xử lý ô "thịt"
    for raw_token in ds_thit_raw:
        norm_token = chuan_hoa_tu(raw_token)
        if norm_token in DANH_MUC_CHINH:
            chinh_da_chuan_hoa_THIT.add(norm_token)  # Thêm vào set thịt
        elif norm_token in DANH_MUC_PHU:
            phu_da_chuan_hoa_CHUNG.add(norm_token)  # Nếu gõ "mắm" vào ô thịt
        elif norm_token:
            luu_nguyen_lieu_moi("thit_box", raw_token, norm_token)
            tat_ca_khong_biet.add(raw_token)

    # Xử lý ô "rau"
    for raw_token in ds_rau_raw:
        norm_token = chuan_hoa_tu(raw_token)
        if norm_token in DANH_MUC_CHINH:
            chinh_da_chuan_hoa_RAU.add(norm_token)  # Thêm vào set rau
        elif norm_token in DANH_MUC_PHU:
            phu_da_chuan_hoa_CHUNG.add(norm_token)  # Nếu gõ "tỏi" vào ô rau
        elif norm_token:
            luu_nguyen_lieu_moi("rau_box", raw_token, norm_token)
            tat_ca_khong_biet.add(raw_token)

    # 3. Tìm kiếm món ăn
    danh_sach_goi_y = []

    # Gộp cả 2 set rau và thịt lại thành 1 set NGUYÊN LIỆU CHÍNH TỔNG
    cac_mon_chinh_nguoi_dung_co = chinh_da_chuan_hoa_THIT.union(chinh_da_chuan_hoa_RAU)
    cac_mon_phu_nguoi_dung_co = phu_da_chuan_hoa_CHUNG

    for mon_an in DATABASE_MON_AN:
        set_chinh_yeu_cau = set(mon_an["nguyen_lieu_chinh_keys"])
        set_phu_yeu_cau = set(mon_an["nguyen_lieu_phu_keys"])

        la_mon_goi_y = False

        if cac_mon_chinh_nguoi_dung_co:
            if not cac_mon_chinh_nguoi_dung_co.isdisjoint(set_chinh_yeu_cau):
                la_mon_goi_y = True
        elif not cac_mon_chinh_nguoi_dung_co and cac_mon_phu_nguoi_dung_co:
            if not cac_mon_phu_nguoi_dung_co.isdisjoint(set_phu_yeu_cau):
                if not set_chinh_yeu_cau:
                    la_mon_goi_y = True

        if la_mon_goi_y:
            ten_nl_chinh = ", ".join([TEN_HIEN_THI.get(key, key) for key in mon_an["nguyen_lieu_chinh_keys"]])
            ten_nl_phu = ", ".join([TEN_HIEN_THI.get(key, key) for key in mon_an["nguyen_lieu_phu_keys"]])

            mon_an_tim_thay = {"ten": mon_an["ten_mon"], "chinh": ten_nl_chinh if ten_nl_chinh else "Không có",
                               "phu": ten_nl_phu if ten_nl_phu else "Không có"}
            danh_sach_goi_y.append(mon_an_tim_thay)

    # 4. Chuẩn bị chuỗi hiển thị cho 2 label (Thịt và Rau)

    # Chỉ thịt
    thit_nhan_dien_list = [TEN_HIEN_THI.get(key, key) for key in chinh_da_chuan_hoa_THIT]
    str_thit_nhan_dien = ", ".join(thit_nhan_dien_list)

    # Rau + Gia vị chung
    rau_nhan_dien_list = [TEN_HIEN_THI.get(key, key) for key in chinh_da_chuan_hoa_RAU]
    giavi_nhan_dien_list = [TEN_HIEN_THI.get(key, key) for key in phu_da_chuan_hoa_CHUNG]

    str_rau_va_giavi_nhan_dien = ", ".join(rau_nhan_dien_list + giavi_nhan_dien_list)

    # 5. Trả về kết quả
    # Trả về 2 chuỗi riêng biệt cho 2 label mới
    return (str_thit_nhan_dien, str_rau_va_giavi_nhan_dien, danh_sach_goi_y, tat_ca_khong_biet)