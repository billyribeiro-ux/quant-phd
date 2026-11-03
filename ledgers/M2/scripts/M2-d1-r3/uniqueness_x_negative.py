"""L21 E3 scope check: for x > 0, F(x, .) = y^3 + x y - 1 has one real zero; for x = -3 it has three.

Usage: python -I uniqueness_x_negative.py. Counts sign changes of F(x, .) on a fine grid.
"""


def count_real_zeros(x: float) -> int:
    lo, hi, n = -4.0, 4.0, 400000
    zeros = 0
    prev = (lo**3 + x * lo - 1.0)
    for k in range(1, n + 1):
        y = lo + (hi - lo) * k / n
        cur = y**3 + x * y - 1.0
        if prev == 0.0 or prev * cur < 0.0:
            zeros += 1
        prev = cur
    return zeros


for x in (0.25, 2.0, -0.5, -3.0):
    print(f"x = {x:>5}: real zeros of y^3 + x*y - 1 on [-4, 4] = {count_real_zeros(x)}")
