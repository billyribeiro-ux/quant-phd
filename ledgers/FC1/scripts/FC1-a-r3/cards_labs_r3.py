"""FC1-a round 3: lab equality (page code == twin, expected == twin output), card numbers in lesson, card duplicates."""
import difflib
import html
import itertools
import json
import re
import subprocess
import sys

ROOT = "course/modules/FC/FC1/"
PY = ".venv/bin/python"


def visible(src):
    src = re.sub(r"<script.*?</script>", " ", src, flags=re.S)
    src = re.sub(r"<[^>]+>", " ", src)
    return html.unescape(src)


def code_block(page_src):
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page_src, flags=re.S)
    return html.unescape(m.group(1))


def expected_block(page_src):
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page_src, flags=re.S)
    return html.unescape(m.group(1))


print("== lab equality")
for page, twin in [("L01", "tests/labs/FC1/lab-FC1-L01-1.py"), ("L02", "tests/labs/FC1/lab-FC1-L02-1.py"),
                   ("L03", "tests/labs/FC1/lab-FC1-L03-1.py")]:
    src = open(ROOT + page + ".html", encoding="utf-8").read()
    twin_src = open(twin, encoding="utf-8").read()
    code = code_block(src)
    code_norm = code.strip("\n")
    twin_norm = twin_src.strip("\n")
    print(page, "code equals twin (after stripping outer newlines):", code_norm == twin_norm,
          "| page code lines", code_norm.count("\n") + 1, "twin lines", twin_norm.count("\n") + 1)
    if code_norm != twin_norm:
        for line in difflib.unified_diff(twin_norm.splitlines(), code_norm.splitlines(), "twin", "page", lineterm=""):
            print("   ", line)
    res = subprocess.run([PY, "-I", "-W", "error", twin], capture_output=True, text=True)
    exp = expected_block(src)
    out = res.stdout
    print(page, "twin exit", res.returncode, "stderr", repr(res.stderr[:200]),
          "| expected block equals twin stdout:", exp.rstrip("\n") == out.rstrip("\n"))
    if exp.rstrip("\n") != out.rstrip("\n"):
        for line in difflib.unified_diff(out.rstrip("\n").splitlines(), exp.rstrip("\n").splitlines(), "twin", "expected", lineterm=""):
            print("   ", line)

print("== cards")
cards = json.load(open(ROOT + "cards.json", encoding="utf-8"))
pages = {p: visible(open(ROOT + p + ".html", encoding="utf-8").read()) for p in ["L01", "L02", "L03"]}
ids = [c["id"] for c in cards]
print("total cards", len(cards), "duplicate ids", len(ids) - len(set(ids)))
for c in cards:
    if c["lesson"] not in pages:
        continue
    if c.get("grade") == "C" and not c.get("basis"):
        print("C card without basis", c["id"])
    text = pages[c["lesson"]]
    nums = set(re.findall(r"\d[\d,]*\.?\d*", c["back"] + " " + c["front"]))
    missing = []
    for n in sorted(nums):
        n2 = n.rstrip(".")
        if n2.replace(",", "") in text.replace(",", "") or n2 in text:
            continue
        missing.append(n2)
    if missing:
        print("card", c["id"], "numbers not found in lesson text:", missing)
print("== near-duplicate card pairs (difflib ratio >= 0.55 on front+back), L01-L03")
sel = [c for c in cards if c["lesson"] in ("L01", "L02", "L03")]
pairs = []
for a, b in itertools.combinations(sel, 2):
    r = difflib.SequenceMatcher(None, a["front"] + " " + a["back"], b["front"] + " " + b["back"]).ratio()
    if r >= 0.55:
        pairs.append((round(r, 3), a["id"], b["id"]))
for p in sorted(pairs, reverse=True):
    print(p)
print("pairs:", len(pairs))
