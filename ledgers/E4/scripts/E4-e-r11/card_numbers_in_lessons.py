"""Round 11: every number (integer, decimal or fraction) written on a card's back must occur in its own lesson's
rendered text, or in the lesson's rendered lab output, or in the card's basis. Lessons are rendered from the current
HTML with html_to_text.py into a scratch directory. Prints each card with a number that does not occur, for review.
Run from the checkout root with -I."""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
cards = json.load(open("course/modules/E/E4/cards.json", encoding="utf-8"))
os.makedirs("scratch/r11", exist_ok=True)
text = {}
for L in ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09"]:
    out = subprocess.run([PY, "-I", os.path.join(HERE, "html_to_text.py"), f"course/modules/E/E4/{L}.html"],
                         capture_output=True, text=True, check=True).stdout
    text[L] = out
NUM = re.compile(r"(?<![A-Za-z_])\d+(?:[./]\d+)?(?:e-?\d+)?(?![A-Za-z_])")
norm = lambda s: s.replace(" ", "").replace("\\", "")
missing = []
checked = 0
for c in cards:
    L = c["lesson"]
    if L not in text:
        continue
    hay = norm(text[L] + "\n" + c.get("basis", ""))
    for num in sorted(set(NUM.findall(c["back"]))):
        checked += 1
        if num.replace(" ", "") not in hay and num not in ("0", "1", "2"):
            missing.append((c["id"], L, num))
print(f"numbers checked (excluding 0, 1, 2 which occur everywhere): {checked}")
for m in missing:
    print("NOT IN LESSON:", *m)
print(f"numbers not found in own lesson: {len(missing)}")
