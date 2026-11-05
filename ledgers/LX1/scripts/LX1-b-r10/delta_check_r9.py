"""LX1-b round 9: arithmetic of the changed L03 solutions, the card delta, and the L03 card coverage of the 7 concepts.

Usage: python3 -I delta_check_r9.py <checkout>
Reads the checkout only; uses exact Fractions for the arithmetic.
"""

import json
import re
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

root = Path(sys.argv[1])

# M2 (L03.html:448): N_4 = N_0 - (V_4 - D), exact and with the rounded V_4 (1 084 166 cents).
N0, D = F(4_000_000), F(1_000_000)
V4_exact = F(1_000_000) / F(5_764_801, 6_250_000)  # P_4 = (49/50)^4 = 5 764 801 / 6 250 000
V4_rounded = F(1_084_166)
print("V4 exact", float(V4_exact))
print("M2 exact N4", float(N0 - (V4_exact - D)))
print("M2 with rounded V4: N0 - (V4r - D) =", N0 - (V4_rounded - D), "(claimed 3 915 834)")
assert N0 - (V4_rounded - D) == 3_915_834

# M3 (L03.html:455): L4 = V4 / N4 with exact and with rounded V4 and N4, four decimals.
N4_exact = N0 - (V4_exact - D)
L_exact = V4_exact / N4_exact
L_rounded = V4_rounded / F(3_915_834)
print("L4 exact", float(L_exact), "rounded4", round(float(L_exact), 4))
print("L4 from rounded V4 and N4", float(L_rounded), "rounded4", round(float(L_rounded), 4))
assert round(float(L_exact), 4) == round(float(L_rounded), 4) == 0.2769

# Card delta: the cards whose JSON changed between the round-8 pin and this pin, for L03/L04 only.
diff = subprocess.run(
    ["git", "diff", "-U0", "0dee921a", "00a84795", "--", "course/modules/LX/LX1/cards.json"],
    cwd=root,
    capture_output=True,
    text=True,
    check=True,
).stdout
cards = json.loads((root / "course/modules/LX/LX1/cards.json").read_text(encoding="utf-8"))
by_id = {c["id"]: c for c in cards}
l03l04 = sorted(cid for cid, c in by_id.items() if c["lesson"] in ("L03", "L04"))
print("L03/L04 cards now:", len(l03l04), l03l04[0], "to", l03l04[-1])
for cid in ("LX1-c031", "LX1-c061", "LX1-c067", "LX1-c077", "LX1-c079"):
    print(cid, "present" if cid in by_id else "absent", "(removed or added in round 9 delta)" if cid in diff else "")
assert "LX1-c077" not in by_id and "LX1-c079" in by_id

# Coverage of the 7 concepts by cards (plan section 9: one card per definition of the 7 concepts).
# Concepts defined on L03: credit-channel-depression, lender-of-last-resort. Each must have a definition card.
for needle in ("credit channel of a depression", "lender of last resort"):
    hits = [c["id"] for c in cards if c["lesson"] == "L03" and needle in c["front"].lower()]
    print("L03 definition card for", needle, "->", hits)
    assert hits

# Central bank (plain dfn, L03.html:390) has no card after the round-9 deletion of c077 (plan section 9 covers the 7 concepts only).
cb = [c["id"] for c in cards if "central bank" in c["front"].lower()]
print("cards naming 'central bank' in the front:", cb)

# L03 cards whose text names Proposition 3.2 parts: each should match the proposition (checked by reading in the ledger row).
for c in cards:
    if c["lesson"] == "L03" and "3.2" in c["front"]:
        print(c["id"], "|", c["front"][:90], "|", c["back"][:110])

page = (root / "course/modules/LX/LX1/L03.html").read_text(encoding="utf-8")
print("L03 dfn central bank present:", 'id="def-central-bank"' in page)
print("DELTA_CHECK PASS")
