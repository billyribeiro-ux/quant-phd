"""Round-4 delta checks for M2 slice a (hub + L01-L06 + lab twins). Read-only; run from the checkout root with -I."""
import html
import json
import re
import subprocess

ROOT = "."
CARDS = "course/modules/M/M2/cards.json"
new = json.load(open(f"{ROOT}/{CARDS}", encoding="utf-8"))
old = {c["id"]: c for c in json.loads(subprocess.check_output(["git", "show", f"aa3c26c:{CARDS}"]))}
changed = sorted(c["id"] for c in new if c != old[c["id"]])
print("cards changed since aa3c26c:", changed)
print("cards L01-L06 changed:", [i for i in changed if int(i[-3:]) <= 74])
for c in new:
    if c["id"] == "M2-c066":
        print("M2-c066 back:", c["back"])
        print("M2-c066 hypotheses clause mentions f(a)=f(b):", "f(a) = f(b)" in c["back"].split("Then there")[0])
print("card count:", len(new), "dup ids:", len(new) - len({c["id"] for c in new}))
for lab in ["L01", "L02", "L03", "L04", "L05", "L06"]:
    src = open(f"{ROOT}/tests/labs/M2/lab-M2-{lab}-1.py", encoding="utf-8").read()
    page = open(f"{ROOT}/course/modules/M/M2/{lab}.html", encoding="utf-8").read()
    blocks = [html.unescape(re.sub(r"<[^>]+>", "", b)).strip() for b in re.findall(r"<pre[^>]*><code[^>]*>(.*?)</code></pre>", page, re.S)]
    print(lab, "embedded twin equals file:", any(b == src.strip() for b in blocks))
for n in (1, 2, 3, 4, 5, 6):
    pass
print("c055 check: 6*1.5*3.25**2 =", 6 * 1.5 * 3.25**2)
print("c056 check: p'(1.5)=5*1.5**4+3*1.5**2 =", 5 * 1.5**4 + 3 * 1.5**2)
print("c057 check: 29/49 =", 29 / 49)
print("c069 check: f(-1)=", (-1) ** 3 - 3 * (-1), " f(1)=", 1 - 3)
print("c066 check: 2/sqrt(3)=", 2 / 3**0.5, " 1/sqrt(3)=", 1 / 3**0.5)
