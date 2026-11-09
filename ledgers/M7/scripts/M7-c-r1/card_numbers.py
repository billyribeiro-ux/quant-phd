import json, re, sys
from pathlib import Path
root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/M/M7/cards.json").read_text(encoding="utf-8"))
num = re.compile(r"\d+\.\d+|\d+")
for lesson in sorted({c["lesson"] for c in cards}):
    html = (root / f"course/modules/M/M7/{lesson}.html").read_text(encoding="utf-8")
    missing = []
    for c in cards:
        if c["lesson"] != lesson:
            continue
        for n in set(num.findall(c["back"])):
            if n not in html and len(n) > 1:
                missing.append((c["id"], n))
    print(lesson, "numbers (len>1) in back not found in lesson text:", missing if missing else "none")
