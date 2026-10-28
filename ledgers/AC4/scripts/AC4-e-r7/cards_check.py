"""Check AC4 cards.json: structure, duplicate fronts/backs, banned phrases, and that each card number appears in its lesson."""
import json, re, sys, html, pathlib
ROOT = pathlib.Path(sys.argv[1]).resolve()
MOD = ROOT / "course/modules/AC/AC4"
cards = json.loads((MOD / "cards.json").read_text())
print("cards:", len(cards))
ids = [c["id"] for c in cards]
print("duplicate ids:", len(ids) - len(set(ids)))
need = {"id", "lesson", "front", "back"}
bad = [c["id"] for c in cards if not need <= set(c) or (c.get("grade") and c["grade"] not in "TCU")]
print("structure problems:", bad)
fronts = {}
backs = {}
for c in cards:
    fronts.setdefault(c["front"].strip().lower(), []).append(c["id"])
    backs.setdefault(c["back"].strip().lower(), []).append(c["id"])
print("duplicate fronts:", [v for v in fronts.values() if len(v) > 1])
print("duplicate backs:", [v for v in backs.values() if len(v) > 1])
banned = ["roughly half", "about 6%", "historically", "...", "…", "typically", "usually"]
for c in cards:
    for field in ("front", "back"):
        for b in banned:
            if b in c[field].lower():
                print("banned", c["id"], field, repr(b))
lesson_text = {}
num = re.compile(r"\d[\d,]*(?:\.\d+)?")
miss = []
for c in cards:
    L = c["lesson"]
    if L not in lesson_text:
        raw = (MOD / f"{L}.html").read_text()
        body = re.sub(r"<[^>]+>", " ", raw)
        lesson_text[L] = html.unescape(body)
    for n in num.findall(c["back"]):
        n2 = n.rstrip(",")
        if n2 and n2 not in lesson_text[L]:
            miss.append((c["id"], n2))
print("numbers in card back not found in lesson text:", miss)
