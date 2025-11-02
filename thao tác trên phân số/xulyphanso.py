def cong(a,b,c,d):
    tu=a*d+b*c
    mau=b*d
    for i in range (tu,1,-1):
        if tu%i==0 and mau%i==0:
            tu=tu/i
            mau=mau/i
            break
    return f"{tu}/{mau}"
def tru(a,b,c,d):
    tu=a*d-b*c
    mau=b*d
    for i in range (tu,1,-1):
        if tu%i==0 and mau%i==0:
            tu=tu/i
            mau=mau/i
            break
    return f"{tu}/{mau}"
def nhan(a,b,c,d):
    tu=a*c
    mau=b*d
    for i in range (tu,1,-1):
        if tu%i==0 and mau%i==0:
            tu=tu/i
            mau=mau/i
            break
    return f"{tu}/{mau}"
def chia(a,b,c,d):
    tu=a*d
    mau=b*c
    for i in range (tu,1,-1):
        if tu%i==0 and mau%i==0:
            tu=tu/i
            mau=mau/i
            break
    return f"{tu}/{mau}"



