def tinh_Sn(n):
    S = 0
    for k in range(1,n+1):
        pheptinh = -1 / (k * (k + 1))
        S = S + pheptinh
    return f"S={round(S, 3)}-TẠ NHẬT ANH-K254060676"
def chung_minh(s):
    S =  1 / (s + 1) -1
    return f"S={round(S, 3)}-TẠ NHẬT ANH-K254060676"