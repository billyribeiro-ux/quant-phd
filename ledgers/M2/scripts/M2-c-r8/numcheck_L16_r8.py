import math
e = math.e
print("F_x(1,2) =", 4 + 2*e**2, " F_y(1,2) =", 1 + e**2, " e^2 =", e**2)
F = lambda x, y: x*x*y + math.exp(x*y)
print("F(2,1) =", F(2, 1), " 4+e^2 =", 4 + e**2)
grid = [(x, y) for x in (0.5, 1.0, 1.5, 2.0) for y in (-1.0, 0.0, 1.0)]
m = max(grid, key=lambda p: abs(F(*p)))
print("grid max |F| at", m, abs(F(*m)), "count", len(grid))
print("max |F_xxx| on grid = max |y^3 e^{xy}|:", max(abs(y**3*math.exp(x*y)) for x, y in grid))
print("F_y third derivative x^3 e^{xy} at (2,1) =", 8*e**2)
print("E1 truncation (1e-10/6)*e^2 =", 1e-10/6*e**2, " rounding delta/h, delta=2^-52*? half spacing in [8,16) =", 2.0**-53*8, "->", 2.0**-53*8/1e-5)
print("E3 F_xy = F_yx at (1,2) =", 2 + 3*e**2)
print("R3 truncation (1e-10/6)*20 =", 1e-10/6*20, " rounding 1e-15/1e-5 =", 1e-15/1e-5, " total", 1e-10/6*20 + 1e-10)
print("L16 Lab hypothesis rounding 1e-16*11.39/1e-5 =", 1e-16*(4+e**2)/1e-5)
