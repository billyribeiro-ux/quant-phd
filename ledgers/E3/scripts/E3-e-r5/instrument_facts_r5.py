"""Facts about the twelve Lab 3 answers quoted on the project page (Exemplar B instrument paragraph), round 5.

Standard library only. Answers are copied from project.html Lab 3 (not from the twin).
"""

from fractions import Fraction as F

import importlib.util
import sys

PAGE_ANSWERS = """
(0, "B", [6200, -15100], ["9/10", "1/10"], [3300, -3000, -700], ["1/20", "7/20", "3/5"]),
(1, "B", [-9400, -10100, 19000], ["2/5", "3/10", "3/10"], [-12200, 17000, -1100], ["1/2", "1/4", "1/4"]),
(2, "A", [10700, -3400, -13400], ["7/10", "1/10", "1/5"], [-14900, -13600, 15200], ["9/20", "2/5", "3/20"]),
(3, "A", [18800, -12500], ["3/4", "1/4"], [16500, -17700], ["2/5", "3/5"]),
(4, "B", [-10700, -5600, -7300], ["1/2", "2/5", "1/10"], [-13800, -9700], ["1/4", "3/4"]),
(5, "B", [-11600, 7900, -12200], ["3/4", "1/10", "3/20"], [-12000, 11300], ["17/20", "3/20"]),
(6, "A", [-9900, 5400, -4200], ["1/2", "1/4", "1/4"], [-15300, 16100, 6800], ["1/4", "1/2", "1/4"]),
(7, "A", [600, -17500], ["3/5", "2/5"], [15800, -2600, -17600], ["2/5", "2/5", "1/5"]),
(8, "B", [-10400, 13800], ["9/10", "1/10"], [10400, 1800], ["1/20", "19/20"]),
(9, "B", [-17900, -12000, -3600], ["1/4", "1/4", "1/2"], [15600, 11600, -12200], ["3/10", "13/20", "1/20"]),
(10, "B", [17000, 1600], ["1/10", "9/10"], [-18700, 3800], ["7/20", "13/20"]),
(11, "B", [10400, -11300], ["2/5", "3/5"], [9300, 7200, -13200], ["1/2", "1/4", "1/4"]),
"""
answers = eval("[" + PAGE_ANSWERS + "]")  # trusted: literal copied from the page above
prizes = [x for a in answers for x in a[2] + a[4]]
print("prize min", min(prizes), "prize max", max(prizes))
print("prizes per lottery:", sorted({len(a[2]) for a in answers} | {len(a[4]) for a in answers}))
sums_ok = all(sum(F(p) for p in a[3]) == 1 and sum(F(p) for p in a[5]) == 1 for a in answers)
print("every lottery's probabilities sum to exactly 1:", sums_ok)
mixed = 0
for a in answers:
    ok = False
    for pr, qs in ((a[2], a[3]), (a[4], a[5])):
        g = any(x > 0 and F(p) > 0 for x, p in zip(pr, qs))
        l = any(x < 0 and F(p) > 0 for x, p in zip(pr, qs))
        ok = ok or (g and l)
    mixed += ok
print("pairs with a mixed-sign lottery:", mixed, "of", len(answers))
print("pair 0 A:", answers[0][2], answers[0][3], "B:", answers[0][4], answers[0][5])
print("pair 3 A:", answers[3][2], answers[3][3], "B:", answers[3][4], answers[3][5])
print("pair 3 both mixed:", all(any(x > 0 for x in pr) and any(x < 0 for x in pr) for pr in (answers[3][2], answers[3][4])))
print("pair ids:", [a[0] for a in answers])
