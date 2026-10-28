"""Round-25 scan: every place in L04 that names Proposition 2.2, and the banned-phrase and process-word scan of L04 and L05."""
import re
import sys

ROOT = sys.argv[1]
L04 = open(f"{ROOT}/course/modules/M/M1/L04.html", encoding="utf-8").read().split("\n")
L05 = open(f"{ROOT}/course/modules/M/M1/L05.html", encoding="utf-8").read().split("\n")
named = [i for i, l in enumerate(L04, 1) if re.search(r"Propositions? 2\.2|Prop\. 2\.2|Prop 2\.2", l)]
print("L04 lines naming Proposition 2.2:", named)
line79 = L04[78]
print("L04 line 79 names:", re.findall(r"the [^,:]+(?:, [^,:]+)*", line79)[:1])
banned = [r"roughly half", r"about 6%", r"historically", r"\.\.\.", r"…", r"\bbuilder\b", r"\bbuild\b", r"\bround\b", r"\bverifier\b", r"REQUESTS", r"unit report"]
for name, lines in (("L04", L04), ("L05", L05)):
    for pat in banned:
        hits = [i for i, l in enumerate(lines, 1) if re.search(pat, l, re.I if pat != "REQUESTS" else 0)]
        print(name, repr(pat), hits)
