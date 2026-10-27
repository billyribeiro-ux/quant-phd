"""Round-7 L01-L02 checks: expected-block vs lab output, hub links, card duplicates, banned words."""
import html, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(sys.argv[1])
AC2 = ROOT / "course/modules/AC/AC2"
PY = str(ROOT / ".venv/bin/python")


def expected_block(page: str) -> str:
    text = (AC2 / page).read_text(encoding="utf-8")
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    return html.unescape(m.group(1)).strip()


for page, twin in (("L02.html", "lab-AC2-L02-1.py"), ("L01.html", "lab-AC2-L01-1.py")):
    out = subprocess.run([PY, "-I", str(ROOT / "tests/labs/AC2" / twin)], capture_output=True, text=True).stdout.strip()
    exp = expected_block(page)
    print(page, "expected block equals twin stdout:", exp == out)

index = (AC2 / "index.html").read_text(encoding="utf-8")
hrefs = sorted(set(re.findall(r'href="([^"#]+)', index)))
bad = [h for h in hrefs if not h.startswith("http") and not (AC2 / h).resolve().exists()]
print("index relative hrefs", len(hrefs), "unresolved", bad)

cards = json.load(open(AC2 / "cards.json", encoding="utf-8"))
fronts = [c["front"].strip().lower() for c in cards]
print("cards", len(cards), "unique ids", len({c["id"] for c in cards}), "duplicate fronts", len(fronts) - len(set(fronts)))

for name in ("index.html", "L01.html", "L02.html"):
    t = (AC2 / name).read_text(encoding="utf-8")
    hits = re.findall(r"(?i)\b(builder|this build|build report|unit report|REQUESTS|roughly|historically|typically)\b", t)
    print(name, "process/banned words:", hits)
