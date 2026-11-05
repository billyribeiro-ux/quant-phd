"""Round-11 extra fixtures recomputed from the page's rules (repeated losses, zero losses, large cents, shuffles).

Usage: python -I fixtures_extra_r11.py   (stdlib only; exits 1 on a mismatch)
"""

import sys
from fractions import Fraction
from math import ceil

bad = 0


def margin_for(losses: list[int], t: int) -> int:
    return sorted(losses)[ceil(Fraction(t * len(losses), 10_000)) - 1]


def cover(losses: list[int], m: int) -> int:
    return 10_000 * sum(1 for x in losses if x <= m) // len(losses)


def eq(label: str, got: object, want: object) -> None:
    global bad
    ok = got == want
    bad += not ok
    print(("OK " if ok else "MISMATCH ") + f"{label}: got {got!r} want {want!r}")


eq("repeated losses [5,5,10,20] at 5000 -> 5", margin_for([5, 5, 10, 20], 5_000), 5)
eq("repeated losses [5,5,5,9,12] at 6000 -> 5", margin_for([5, 5, 5, 9, 12], 6_000), 5)
eq("zero loss [0,10,20,30] at 5000 -> 10", margin_for([0, 10, 20, 30], 5_000), 10)
eq("one scenario [7] at 1 and 10000 -> 7", (margin_for([7], 1), margin_for([7], 10_000)), (7, 7))
eq("smallest target [9,3,5] at 1 -> 3", margin_for([9, 3, 5], 1), 3)
eq("cover [5,5,10,20] at 5 -> 5000", cover([5, 5, 10, 20], 5), 5_000)
eq("cover [0,0,5,9] at 0 -> 5000", cover([0, 0, 5, 9], 0), 5_000)
eq("cover [50] at 50 -> 10000; [51] at 50 -> 0", (cover([50], 50), cover([51], 50)), (10_000, 0))
eq("cover [1,5,9] at 4 -> 3333 (floor)", cover([1, 5, 9], 4), 3_333)
eq("cover [1,2,9] at 2 -> 6666 (floor)", cover([1, 2, 9], 2), 6_666)
eq("cover divided first would give 0 for 1 of 3", (10_000 * (1 // 3)), 0)
# Large-cent share: residual R = loss, survivors 1 and 2 with funds F1, F2 (defaulter 3 with nothing).
F1, F2 = 6_692_931_089_932_558, 585_467_024_498_971
LOSS = 6_585_696_953_829_388
T = F1 + F2
s1, s2 = LOSS * F1 // T, LOSS * F2 // T
left = LOSS - s1 - s2  # the leftover cents, given one each to the first survivors with DF > 0 (member 1 first)
eq("large-cent leftover cents (floor shares sum short)", left, 1)
eq("large-cent survivor shares after leftover 1 and 2", (s1 + 1, s2), (6_055_950_114_045_320, 529_746_839_784_068))
eq("large-cent residual below pool", LOSS < T, True)
print("FIXTURES EXTRA", "FAIL" if bad else "PASS", bad)
sys.exit(1 if bad else 0)
