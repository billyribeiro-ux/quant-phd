"""Round-3 claim checks (verifier D3, FC1-c). Read-only. Usage: claims_checks_r3.py <checkout root>.

Sections: (1) page code blocks vs lab twins (Lab 2 differs only by its blanks); (2) expected blocks vs twin output;
(3) T-graded cards against the data-grade attribute of the cited claim; (4) lesson text for the changed cards;
(5) the curriculum brief for FC1 against the page's scope sentence; (6) the FC1 hours arithmetic.
"""
import difflib
import html
import json
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
MOD = root / "course/modules/FC/FC1"
page = (MOD / "project.html").read_text(encoding="utf-8")


def text_of(path):
    raw = path.read_text(encoding="utf-8")
    t = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", " ", raw, flags=re.S)))
    return re.sub(r"\s+", " ", t)


print("== 1. page code vs twin")
labs = re.findall(r'<section class="lab[^"]*" id="(lab-FC1-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, flags=re.S)
for lid, code, exp in labs:
    code = html.unescape(code)
    twin = (root / "tests/labs/FC1" / f"{lid}.py").read_text(encoding="utf-8")
    if code.strip() == twin.strip():
        print(lid, "page code equals twin")
    else:
        diff = [l for l in difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm="", n=0)
                if l[:1] in "+-" and l[:3] not in ("+++", "---")]
        print(lid, "page code differs from twin in", len(diff), "lines:", diff)
print("== 2. expected block vs twin output (run here)")
for lid, _code, exp in labs:
    if lid.endswith("-2"):
        continue
    out = subprocess.run([str(root / ".venv/bin/python"), "-I", "-W", "error", str(root / "tests/labs/FC1" / f"{lid}.py")],
                         capture_output=True, text=True, check=True).stdout
    print(lid, "expected equals output:", html.unescape(exp).strip().splitlines() == out.strip().splitlines())

print("== 3. T-graded cards citing Proposition or Corollary: data-grade of the cited claim")
cards = json.loads((MOD / "cards.json").read_text(encoding="utf-8"))
n = 0
bad = []
for c in cards:
    if c.get("grade") != "T":
        continue
    m = re.search(r"(Proposition|Corollary) (\d+\.\d+)", c["back"])
    if not m:
        continue
    n += 1
    raw = (MOD / f"{c['lesson']}.html").read_text(encoding="utf-8")
    hit = re.search(r'<span class="block-title claim" data-grade="(\w)">' + re.escape(f"{m.group(1)} {m.group(2)}") + r"\b", raw)
    if not hit or hit.group(1) != "T":
        bad.append((c["id"], m.group(0)))
print("T cards citing a Proposition or Corollary:", n, "without a T claim:", bad)

print("== 4. lesson text for the changed or added cards")
snips = {
    "L02 Definition 1.1": ("L02.html", "Definition 1.1 (exchange-traded and over-the-counter)", 330),
    "L04 Definition 1.1 stop order": ("L04.html", "Stop order. It has a stop price", 330),
    "L04 Proposition 2.3": ("L04.html", "Proposition 2.3 (share conservation)", 200),
    "L04 no cancellations sentence": ("L04.html", "The model has no cancellations or modifications of resting orders.", 160),
    "L01 Proposition 4.1": ("L01.html", "Proposition 4.1 (equity absorbs the loss)", 260),
    "L01 Remark 4.2": ("L01.html", "Remark 4.2 (a test, not a legal rule)", 200),
    "L05 Section 2 consideration": ("L05.html", "its consideration is", 230),
}
for label, (f, key, n_chars) in snips.items():
    t = text_of(MOD / f)
    i = t.find(key)
    print(label, "::", t[i:i + n_chars] if i >= 0 else "NOT FOUND")

print("== 5. curriculum brief for FC1 and the page scope sentence")
brief = " ".join(
    "Represent a fixed-rate bond and a trade that settles later as dated cash-flow objects with a common interface, and test each against hand-computed examples. Futures, swaps and options follow in FC2.".split())
data = json.loads((root / "curriculum/curriculum.json").read_text(encoding="utf-8"))


def find_module(o):
    if isinstance(o, dict):
        if o.get("id") == "FC1":
            return o
        for v in o.values():
            r = find_module(v)
            if r:
                return r
    elif isinstance(o, list):
        for v in o:
            r = find_module(v)
            if r:
                return r
    return None


fc1 = find_module(data)
print("curriculum.json brief equals the expected sentence:", " ".join(fc1["project"]["brief"].split()) == brief)
print("page scope sentence present:", "Futures, swaps and options are not part of this project" in page)
print("FC1 hours in curriculum.json:", fc1["hours"])

print("== 6. hours arithmetic")
table = [1, 2, 5, 4, 2, 3, 3]
print("table components:", table, "sum:", sum(table), "page total: 20")
print("hub lessons 5 x 10 =", 5 * 10, "; hub project 20; sum", 5 * 10 + 20, "equals curriculum hours", fc1["hours"])
