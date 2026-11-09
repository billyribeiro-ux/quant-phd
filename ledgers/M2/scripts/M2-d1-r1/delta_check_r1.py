"""Round-1 delta checks for M2-d1 (pin 95f3f8cb vs base 4eb6788f). Run with python -I from the checkout root."""
import json
import re
import subprocess
import sys

BASE = "4eb6788f"
P = "course/modules/M/M2"


def git(rev, path):
    return subprocess.check_output(["git", "show", f"{rev}:{path}"]).decode("utf-8")


# 1. L19-L21 pages and twins byte-identical
same = subprocess.call(["git", "diff", "--quiet", BASE + "..HEAD", "--",
                        P + "/L19.html", P + "/L20.html", P + "/L21.html",
                        "tests/labs/M2/lab-M2-L19-1.py", "tests/labs/M2/lab-M2-L20-1.py",
                        "tests/labs/M2/lab-M2-L21-1.py"]) == 0
print("pages+twins L19-L21 byte-identical since base:", same)

# 2. cards: id sets, lessons, changed entries
new = json.loads(git("HEAD", P + "/cards.json"))
old = json.loads(git(BASE, P + "/cards.json"))
on = {c["id"]: c for c in old}
nn = {c["id"]: c for c in new}
sel_new = sorted(c["id"] for c in new if c["lesson"] in ("L19", "L20", "L21"))
sel_old = sorted(c["id"] for c in old if c["lesson"] in ("L19", "L20", "L21"))
print("L19-L21 card id sets equal:", sel_new == sel_old, len(sel_new))
print("changed L19-L21 entries:", [i for i in sel_new if nn[i] != on[i]])
print("L19-L21 entries changed text fields:", {i: [k for k in nn[i] if nn[i][k] != on[i].get(k)] for i in sel_new if nn[i] != on[i]})
print("cards total new/old:", len(new), len(old))
print("dup ids:", len(nn) != len(new), " dup fronts:", len({c['front'] for c in new}) != len(new))
print("c402/c403 present:", "M2-c402" in nn and "M2-c403" in nn)

# 3. c293 number and lab output
c293 = nn["M2-c293"]["back"]
lab = subprocess.check_output(["/bin/sh", "-c", "cat ledgers/M2/scripts/M2-d1-r1/twin_L19.out"]).decode()
m = re.search(r"f_xy = ([0-9.]+)", lab)
print("card c293 number:", re.search(r"is ([0-9.]+) \(Misconception", c293).group(1), " lab printed f_xy:", m.group(1))
L19 = git("HEAD", P + "/L19.html")
print("card number 2.148721 appears in L19.html:", "2.148721" in L19, "| lesson prints ~2.149:", "2.149" in L19)
print("e^0.5+0.5 =", round(2.718281828459045 ** 0.5 + 0.5, 6))

# 4. Assumption 2.1 in L06 (cited by L19 and c293) unchanged in substance
l06 = git("HEAD", P + "/L06.html")
print("L06 Assumption 2.1 is EVT:", "Assumption 2.1" in l06 and "extreme value theorem" in l06)

# 5. references entries for the two keys
R = json.loads(git("HEAD", "references/references.json"))
RO = json.loads(git(BASE, "references/references.json"))
for k in ("spivak2008calculus", "hubbard2015vector"):
    a = [e for e in R["entries"] if e.get("key") == k]
    b = [e for e in RO["entries"] if e.get("key") == k]
    print("registry", k, "identical:", a == b, "used_by:", a[0].get("used_by") if a else None)

# 6. hours
idx = git("HEAD", P + "/index.html")
print("hub split:", re.findall(r'data-hours-lessons="(\d+)"', idx), "sum lesson data-hours:",
      sum(float(re.search(r'data-hours="([0-9.]+)"', git("HEAD", f"{P}/L{i:02d}.html")).group(1)) for i in range(1, 25)))
