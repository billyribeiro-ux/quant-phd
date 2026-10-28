"""Round 23 AC4-a checks: twin stdout vs embedded expected block; card id/text scan for L01-L02 cards."""
import html, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(sys.argv[1])
pages = {"L01": "course/modules/AC/AC4/L01.html", "L02": "course/modules/AC/AC4/L02.html"}
for lab, page in pages.items():
    text = (ROOT / page).read_text(encoding="utf-8")
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(m.group(1)).strip().splitlines()
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/AC4/lab-AC4-{lab}-1.py")],
                         capture_output=True, text=True, timeout=60)
    got = run.stdout.strip().splitlines()
    print(f"{lab}: rc={run.returncode} stderr_bytes={len(run.stderr)} lines expected={len(expected)} got={len(got)} equal={expected == got}")

cards = json.loads((ROOT / "course/modules/AC/AC4/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards total", len(ids), "unique ids", len(set(ids)) == len(ids))
fronts = [c["front"] for c in cards]
print("duplicate fronts", len(fronts) - len(set(fronts)))
for c in cards:
    if c["lesson"] in ("L01", "L02") or c["id"] in ("AC4-c020", "AC4-c135"):
        if c["id"] in ("AC4-c020", "AC4-c135") or c["lesson"] in ("L01", "L02"):
            pass
print("L01/L02 card count", sum(1 for c in cards if c["lesson"] in ("L01", "L02")))
for c in cards:
    if c["id"] in ("AC4-c020", "AC4-c135"):
        print(json.dumps(c, ensure_ascii=False))
