"""Round-14 SC1-a: print the locators behind the round-14 FAIL rows (hub reflection claim vs L06; key-results rows vs the
hypotheses of the lemmas they summarise)."""
import re

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE14-SC1-a/course/modules/SC/SC1/"

def lines(path):
    return open(ROOT + path, encoding="utf-8").read().splitlines()

def show(path, nums, width=220):
    L = lines(path)
    for n in nums:
        print(f"{path}:{n}: {re.sub(r'<[^>]+>', '', L[n - 1]).strip()[:width]}")

print("== hub claim vs L06 (path-level reflection)")
show("index.html", [33])
for pat in [r"path-level", r"fixed-time form", r"Proposition 2\.7"]:
    for n, l in enumerate(lines("L06.html"), 1):
        if re.search(pat, l):
            print(f"L06.html:{n} [{pat}]: {re.sub(r'<[^>]+>', '', l).strip()[:200]}")
            break
print("== key-results rows vs lemma hypotheses")
show("L01.html", [351])
show("L01.html", [102, 103, 104, 105, 106, 107])
show("L02.html", [459])
show("L02.html", [103, 104, 105, 106, 108])
show("../../../../course/modules/SC/SC1/L03.html".replace("../../../../course/modules/SC/SC1/", ""), [395])
show("L03.html", [76, 77, 88, 89, 90])
