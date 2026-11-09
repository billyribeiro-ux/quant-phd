"""Round-3: re-check every printed Part C improvement (L08.html:311-320 / lab output) exactly, against X=8, Y=4."""
from fractions import Fraction as F
X, Y = 8, 4
printed = [
    ((1, 1), (F(6, 5), F(6, 7)), F(36, 35), F(748, 35)),
    ((2, 2), (F(5, 2), F(5, 3)), F(25, 6), F(77, 6)),
    ((3, 1), (F(18, 7), F(6, 5)), F(108, 35), F(76, 5)),
    ((3, 2), (F(27, 8), F(9, 5)), F(243, 40), F(407, 40)),
    ((4, 1), (F(3), F(3, 2)), F(9, 2), F(25, 2)),
    ((4, 3), (F(5), F(5, 2)), F(25, 2), F(9, 2)),
    ((5, 2), (F(37, 8), F(11, 5)), F(407, 40), F(243, 40)),
    ((5, 3), (F(38, 7), F(14, 5)), F(76, 5), F(108, 35)),
    ((6, 2), (F(11, 2), F(7, 3)), F(77, 6), F(25, 6)),
    ((7, 3), (F(34, 5), F(22, 7)), F(748, 35), F(36, 35)),
]
ok_all = True
for (x, y), (a, b), uA_new, uB_new in printed:
    uA0, uB0 = F(x) * y, F(X - x) * F(Y - y)
    uA1, uB1 = a * b, (X - a) * (Y - b)
    nonint = a.denominator != 1 or b.denominator != 1
    good = (uA1 == uA_new and uB1 == uB_new and uA1 > uA0 and uB1 > uB0 and nonint)
    ok_all &= good
    print((x, y), "old", (uA0, uB0), "new", (str(uA1), str(uB1)), "printed", (str(uA_new), str(uB_new)), "strict_both", uA1 > uA0 and uB1 > uB0, "noninteger", nonint, "ok", good)
print("all printed improvements verified:", ok_all)
