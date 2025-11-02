import math
from logging import exception


def giai_pt_bac2(a: float, b: float, c: float):
        if a == 0:
            if b == 0:
                if c == 0:
                    return "Phương trình vô số nghiệm"
                else:
                    return "Phương trình vô nghiệm"
            else:
                x = -c / b
                return (x,)
        delta = b**2 - 4*a*c
        if delta < 0:
            return "Phương trình vô nghiệm"
        elif delta == 0:
            x = -b / (2*a)
            return f"nghiệm kép {x}"
        else:
            sqrt_delta = math.sqrt(delta)
            x1 = (-b + sqrt_delta) / (2*a)
            x2 = (-b - sqrt_delta) / (2*a)
            return f"2 nghiệm x1={x1} x2={x2}"

