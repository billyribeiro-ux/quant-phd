"""Round 17 (BK4 slice c): numeric claims in the grader text. Usage: python -I numeric_probes_r17.py"""
import math
# 1. test_large_cent_shares_are_floored_in_integers (test_project.py:450-459)
R = 6_585_696_953_829_388
f1, f2 = 6_692_931_089_932_558, 585_467_024_498_971
D = f1 + f2
s1, s2 = R * f1 // D, R * f2 // D
left = R - s1 - s2
print("large-cent: D", D, "R<D", R < D, "share1", s1, "share2", s2, "leftover", left)
print("large-cent: page test wants 6055950114045320 and 529746839784068 ->", (s1 + (1 if left > 0 else 0), s2) == (6055950114045320, 529746839784068))
print("large-cent: R*f1 exceeds 2**53:", R * f1 > 2**53)
# 2. the float sentence in the message at test_project.py:697-699
print("float (2800/10000)*50 =", repr((2800 / 10000) * 50), " ceil =", math.ceil((2800 / 10000) * 50))
print("exact ceil index for 2800 bps over 50 scenarios =", -((-2800 * 50) // 10000))
# 3. the expected margin of that fixture (losses 1..50) is the index itself
print("margin for losses 1..50 at index 14 =", sorted(range(1, 51))[14 - 1])
# 4. the page's '(6666.67 to two places)' and 3333 claims at test_project.py:781-794 and page line 251
print("20000/3 =", round(20000 / 3, 2), "floor 20000//3 =", 20000 // 3)
print("10000*1//3 =", 10000 * 1 // 3)
