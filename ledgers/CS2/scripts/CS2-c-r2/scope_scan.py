# Verifier scan: banned phrases and scope words in the CS2 L09-L11 pages and cards (prints each hit with context).
import re, sys, pathlib
root = pathlib.Path(sys.argv[1])
pat = re.compile(r"\b(roughly|historically|typically|usually|often|generally|most|about|only|all|always|every|any|never|same|drives?|offsets?|raises?|as much as|build|builder|verifier|round|REQUESTS?|unit report|left as an exercise|exercise|clearly|obviously|trivially)\b", re.I)
for name in ("L09.html", "L10.html", "L11.html", "cards.json"):
    text = (root / "course/modules/CS/CS2" / name).read_text(encoding="utf-8")
    text = re.sub(r"<[^>]+>", " ", text) if name.endswith(".html") else text
    for m in pat.finditer(text):
        s = max(0, m.start() - 60); e = min(len(text), m.end() + 40)
        print(f"{name}: [{m.group(0)}] ...{' '.join(text[s:e].split())}...")
