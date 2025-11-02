# xuly.py
# Chỉ có def + return; KHÔNG print.
# Các dòng "khó" có chú thích # để mày đọc hiểu nhanh.

import os, re, json, unicodedata
from datetime import datetime
from typing import Dict, Set, List, Tuple

# ======================
# 1) CHUẨN HOÁ TỪ VỰNG
# ======================

def bo_dau(s: str) -> str:
    """Bỏ dấu tiếng Việt."""
    # NFD tách chữ + dấu tổ hợp, rồi lọc ký tự "combining"
    s_norm = unicodedata.normalize("NFD", s)  # # 'thịt lợn' -> 'thịṭ lợn'
    return "".join(ch for ch in s_norm if not unicodedata.combining(ch))  # # -> 'thit lon'

def chuan_hoa_tu(token: str, bang_dong_nghia: Dict[str, str]) -> str:
    """Hạ chữ, bỏ dấu/ ký tự lạ, gom khoảng trắng, ánh xạ đồng nghĩa -> nhãn chuẩn."""
    t = (token or "").strip().lower()
    t = bo_dau(t)                                           # # 'Thịt Lợn' -> 'thit lon'
    t = re.sub(r"[^a-z0-9\s_]", " ", t)                     # # giữ a-z, số, space, '_' thôi
    t = re.sub(r"\s+", " ", t).strip()
    return bang_dong_nghia.get(t, t)                        # # nếu có trong bảng thì trả về nhãn chuẩn

def tach_ds(chuoi: str) -> List[str]:
    """Tách theo dấu phẩy thành list token, bỏ rỗng/ khoảng trắng thừa."""
    if not chuoi:
        return []
    return [m.strip() for m in chuoi.split(",") if m.strip()]

def hien_thi_vi(nhan: str) -> str:
    """Đổi nhãn chuẩn -> chữ tiếng Việt để hiển thị."""
    return HIEN_THI_VI.get(nhan, nhan.replace("_", " "))

# Bảng đồng nghĩa -> nhãn chuẩn
BANG_DONG_NGHIA: Dict[str, str] = {
    # thịt/chính
    "thit lon": "thit_lon", "thit heo": "thit_lon", "lon": "thit_lon", "heo": "thit_lon",
    "thit bo": "thit_bo", "bo": "thit_bo",
    "thit ga": "thit_ga", "ga": "thit_ga",
    "ca": "ca", "ca fish": "ca",
    "trung": "trung", "trung ga": "trung", "trung vit": "trung",
    "luon": "luon", "luoi con": "luon",  # ví dụ mở rộng
    "vit": "vit",
    "chim": "chim", "bo cau": "chim", "chim bo cau": "chim",
    "de": "de", "cuu": "cuu", "nai": "nai",

    # phụ
    "hanh": "hanh", "hanh tay": "hanh", "hanh la": "hanh",
    "toi": "toi",
    "ot": "ot",
    "gung": "gung",
    "gia vi": "gia_vi", "bot nem": "gia_vi", "hat nem": "gia_vi",
    "khoai tay": "khoai_tay",
    "ca rot": "ca_rot", "carot": "ca_rot",
    "rau": "rau", "rau xanh": "rau",
    "nuoc mam": "mam", "mam": "mam",
    "muoi": "muoi",
}

# Từ vựng hợp lệ (nhãn chuẩn)
VOCAB_CHINH: Set[str] = {"thit_lon", "thit_bo", "thit_ga", "ca", "trung", "luon", "vit", "chim", "de", "cuu", "nai"}
VOCAB_PHU:   Set[str] = {"hanh", "toi", "ot", "gung", "gia_vi", "khoai_tay", "ca_rot", "rau", "mam", "muoi"}

# Bản đồ hiển thị tiếng Việt (có dấu)
HIEN_THI_VI: Dict[str, str] = {
    "thit_lon": "thịt lợn", "thit_bo": "thịt bò", "thit_ga": "thịt gà",
    "ca": "cá", "trung": "trứng", "luon": "lươn", "vit": "vịt", "chim": "chim",
    "de": "dê", "cuu": "cừu", "nai": "nai",
    "hanh": "hành", "toi": "tỏi", "ot": "ớt", "gung": "gừng", "gia_vi": "gia vị",
    "khoai_tay": "khoai tây", "ca_rot": "cà rốt", "rau": "rau", "mam": "mắm", "muoi": "muối"
}

# Nơi lưu nguyên liệu lạ (JSON Lines)
TEP_NGUYEN_LIEU_MOI = "du_lieu/nguyen_lieu_moi.jsonl"


# =====================================
# 2) LƯU NGUYÊN LIỆU LẠ ĐỂ CẢI THIỆN
# =====================================

def _ghi_json_line(path: str, obj: Dict[str, object]) -> None:
    """Ghi 1 dòng JSON (không print)."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)     # # tạo thư mục nếu chưa có
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")      # # JSONL: mỗi bản ghi 1 dòng

def luu_nguyen_lieu_moi(loai: str, raw: str) -> None:
    """
    loai: 'chinh' hoặc 'phu'.
    raw: người dùng gõ.
    norm: sau khi chuẩn hoá nhưng KHÔNG thuộc từ vựng hợp lệ.
    """
    if not norm:  # # rỗng thì bỏ qua
        return
    rec = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "loai": loai,                 # # 'chinh' / 'phu'
        "raw": raw,                   # # người dùng gõ
    }
    _ghi_json_line(TEP_NGUYEN_LIEU_MOI, rec)


# =======================
# 3) CHUẨN HOÁ INPUT GUI
# =======================

def chuan_hoa_input(text_chinh: str, text_phu: str) -> Tuple[Set[str], Set[str], str, str]:
    """
    Từ 2 chuỗi input -> (tap_chinh, tap_phu, hien_thi_chinh, hien_thi_phu).
    - Tự lưu nguyên liệu lạ vào JSONL.
    """
    ds_chinh_raw = tach_ds(text_chinh)
    ds_phu_raw   = tach_ds(text_phu)

    # Ánh xạ từng token -> norm
    ds_chinh_norm = [(t, chuan_hoa_tu(t, BANG_DONG_NGHIA)) for t in ds_chinh_raw]
    ds_phu_norm   = [(t, chuan_hoa_tu(t, BANG_DONG_NGHIA)) for t in ds_phu_raw]

    # Lưu những token KHÔNG thuộc vocab (để cải thiện về sau)
    for raw, norm in ds_chinh_norm:
        if norm and norm not in VOCAB_CHINH:
            luu_nguyen_lieu_moi("chinh", raw, norm)  # # ghi file JSONL
    for raw, norm in ds_phu_norm:
        if norm and norm not in VOCAB_PHU:
            luu_nguyen_lieu_moi("phu", raw, norm)

    # Lọc ra token hợp lệ (dùng set để loại trùng)
    tap_chinh = {norm for _, norm in ds_chinh_norm if norm in VOCAB_CHINH}
    tap_phu   = {norm for _, norm in ds_phu_norm   if norm in VOCAB_PHU}

    # Chuẩn text hiển thị cho label
    hien_thi_chinh = ", ".join(hien_thi_vi(t) for t in sorted(tap_chinh)) or "(trống)"
    hien_thi_phu   = ", ".join(hien_thi_vi(p) for p in sorted(tap_phu))   or "(trống)"

    return tap_chinh, tap_phu, hien_thi_chinh, hien_thi_phu


# ==================================
# 4) LUẬT/CÔNG THỨC GỢI Ý MÓN ĂN
# ==================================

CongThuc = Dict[str, object]  # # 'name': str, 'requires': set, 'optional': set

CONG_THUC_CO_SAN: List[CongThuc] = [
    {"name": "Thịt lợn kho",        "requires": {"thit_lon", "mam", "muoi"}, "optional": {"hanh", "toi", "ot", "gia_vi"}},
    {"name": "Thịt bò xào gừng",    "requires": {"thit_bo", "gung", "toi"},  "optional": {"hanh", "ot", "gia_vi", "rau"}},
    {"name": "Gà luộc",             "requires": {"thit_ga", "hanh"},         "optional": {"muoi", "gia_vi"}},
    {"name": "Vịt kho",             "requires": {"vit", "mam", "muoi"},      "optional": {"hanh", "toi", "ot", "gia_vi"}},
    {"name": "Cá chiên",            "requires": {"ca", "muoi"},              "optional": {"toi", "ot"}},
    {"name": "Trứng chiên hành",    "requires": {"trung", "hanh"},           "optional": {"muoi", "gia_vi"}},
    {"name": "Lươn om",             "requires": {"luon", "hanh", "toi"},     "optional": {"ot", "mam", "muoi"}},
    {"name": "Chim nướng",          "requires": {"chim", "muoi"},            "optional": {"toi", "ot", "hanh", "gia_vi"}},
    {"name": "Cừu hầm khoai & cà rốt", "requires": {"cuu", "khoai_tay", "ca_rot", "gia_vi"}, "optional": {"hanh", "toi"}},
    {"name": "Nai xào gừng",        "requires": {"nai", "gung", "toi"},      "optional": {"hanh", "ot"}},
    {"name": "Dê xào gừng",         "requires": {"de", "gung", "toi"},       "optional": {"hanh", "ot"}},
]

def tao_cong_thuc_dong(tap_chinh: Set[str], co_san: Set[str]) -> List[CongThuc]:
    """
    Sinh công thức động theo nguyên liệu có sẵn:
    - Có 'mam' + 'muoi'  -> gợi ý '<thịt> kho'
    - Có 'hanh'          -> gợi ý '<thịt> luộc'
    - Có 'gung' + 'toi'  -> gợi ý '<thịt> xào gừng'
    """
    ds: List[CongThuc] = []
    for m in tap_chinh:
        if {"mam", "muoi"}.issubset(co_san):
            ds.append({"name": f"{hien_thi_vi(m).capitalize()} kho", "requires": {m, "mam", "muoi"}, "optional": {"hanh", "toi", "ot", "gia_vi"}})
        if "hanh" in co_san:
            ds.append({"name": f"{hien_thi_vi(m).capitalize()} luộc", "requires": {m, "hanh"}, "optional": {"muoi", "gia_vi"}})
        if {"gung", "toi"}.issubset(co_san):
            ds.append({"name": f"{hien_thi_vi(m).capitalize()} xào gừng", "requires": {m, "gung", "toi"}, "optional": {"hanh", "ot", "gia_vi"}})
    return ds

def goi_y_mon(tap_chinh: Set[str], tap_phu: Set[str]) -> List[Tuple[str, List[str], List[str]]]:
    """
    Trả về list các dòng cho bảng:
    [(ten_mon, danh_sach_chinh_hien_thi, danh_sach_phu_hien_thi)]
    """
    co_san = tap_chinh | tap_phu
    luat: List[CongThuc] = CONG_THUC_CO_SAN + tao_cong_thuc_dong(tap_chinh, co_san)

    ket_qua_tam: List[Tuple[str, List[str], List[str], int]] = []  # # thêm 'score' để sort
    for r in luat:
        req = set(r["requires"])
        opt = set(r["optional"])
        if not req.issubset(co_san):
            continue  # # thiếu NL bắt buộc -> bỏ

        used = sorted(req | (opt & co_san))                         # # nguyên liệu thực sự dùng
        score = len(used)                                           # # khớp càng nhiều càng ưu tiên

        # Tách used thành 2 nhóm để đưa lên 2 cột của bảng
        ds_chinh = [hien_thi_vi(x) for x in used if x in VOCAB_CHINH]
        ds_phu   = [hien_thi_vi(x) for x in used if x in VOCAB_PHU]

        ket_qua_tam.append((r["name"], ds_chinh, ds_phu, score))

    # Sort: nhiều nguyên liệu khớp hơn đứng trước; nếu bằng nhau thì theo tên
    ket_qua_tam.sort(key=lambda t: (-t[3], t[0]))

    # Trả về đúng 3 thành phần cho bảng
    return [(ten, ds_c, ds_p) for (ten, ds_c, ds_p, _) in ket_qua_tam]


# =========================================
# 5) HÀM DÀNH CHO GUI (chỉ return, không print)
# =========================================

def xu_ly_gui(text_chinh: str, text_phu: str) -> Dict[str, object]:
    """
    Dành cho GUI gọi.
    Return:
        {
          'hien_thi_chinh': 'thịt lợn, gà',
          'hien_thi_phu'  : 'hành, ớt, rau',
          'bang'          : [(ten_mon, 'thịt lợn', 'hành, mắm, muối'), ...]
        }
    """
    tap_chinh, tap_phu, hien_chinh, hien_phu = chuan_hoa_input(text_chinh, text_phu)
    ds = goi_y_mon(tap_chinh, tap_phu)

    # Chuyển từng món thành 1 dòng “sẵn sàng đổ vào QTableWidget”
    bang: List[Tuple[str, str, str]] = []
    for ten, ds_c, ds_p in ds:
        bang.append((ten, ", ".join(ds_c), ", ".join(ds_p)))

    return {
        "hien_thi_chinh": hien_chinh,
        "hien_thi_phu": hien_phu,
        "bang": bang
    }
