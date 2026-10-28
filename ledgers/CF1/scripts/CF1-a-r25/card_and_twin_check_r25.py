"""Round-25 checks for CF1 slice a: card CF1-c110 against L01 line 446 and Remark 4.3, R3 recomputed, twins vs embedded output."""
import html
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
cards = json.loads((root / "course/modules/CF/CF1/cards.json").read_text())
c110 = next(c for c in cards if c["id"] == "CF1-c110")
print("c110 grade", c110["grade"], "basis", c110["basis"])
l01 = (root / "course/modules/CF/CF1/L01.html").read_text().splitlines()
print("L01 line 446 starts", l01[445].strip()[:60])
print("L01 line 466 grade", re.findall(r'data-grade="(\w)"', l01[465]))
print("R3 values", -1 + 1.05 / 1.06, -1 + 1.05 / 1.03)
for lesson, twin in (("L01", "lab-CF1-L01-1.py"), ("L02", "lab-CF1-L02-1.py")):
    src = (root / f"course/modules/CF/CF1/{lesson}.html").read_text()
    embedded = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    import subprocess
    out = subprocess.run([str(root / ".venv/bin/python"), "-I", "-W", "error", str(root / "tests/labs/CF1" / twin)],
                         capture_output=True, text=True).stdout
    print(lesson, "embedded blocks", len(embedded), "match", [html.unescape(re.sub("<[^>]+>", "", e)).strip() == out.strip() for e in embedded])
