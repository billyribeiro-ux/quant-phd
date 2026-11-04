F1 = 6_692_931_089_932_558
F2 = 585_467_024_498_971
R = 6_585_696_953_829_388
pool = F1 + F2
s1 = R * F1 // pool
s2 = R * F2 // pool
left = R - s1 - s2
print("2**53 =", 2**53)
print("R*F1 =", R * F1, "exceeds 2**53:", R * F1 > 2**53)
print("R*F2 =", R * F2, "exceeds 2**53:", R * F2 > 2**53)
print("R > 2**53:", R > 2**53, "F1 > 2**53:", F1 > 2**53, "F2 > 2**53:", F2 > 2**53)
print("pool", pool, "R<pool", R < pool)
print("s1", s1, "s2", s2, "leftover", left)
print("want_survivors expected 6055950114045320, 529746839784068")
print("s1 + leftover?", s1 + (1 if left else 0), s2)
# float-based path for vc10 comparison
import math
f1 = int(R * (F1 / pool)); f2 = int(R * (F2 / pool))
print("float shares", f1, f2)
