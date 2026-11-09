# Verifier-written: dump slice cards (lesson L04-L06) with grade/basis, and flag ids changed since edbb7aa8.
import json, pathlib, subprocess
REPO = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyS5-E1-b")
cards = json.loads((REPO / "course/modules/E/E1/cards.json").read_text(encoding="utf-8"))
old = json.loads(subprocess.run(["git", "show", "edbb7aa8:course/modules/E/E1/cards.json"], cwd=REPO,
                                capture_output=True, text=True, check=True).stdout)
oldmap = {c["id"]: c for c in old}
print("total", len(cards), "ids unique", len({c['id'] for c in cards}))
for c in cards:
    if c["lesson"] in ("L04", "L05", "L06") or c["id"] in ("E1-c133", "E1-c143", "E1-c144", "E1-c145", "E1-c146", "E1-c147", "E1-c148", "E1-c153", "E1-c154", "E1-c155", "E1-c156"):
        changed = "CHANGED" if oldmap.get(c["id"]) != c else "same"
        print(f"== {c['id']} {c['lesson']} grade={c.get('grade')} basis={c.get('basis')} [{changed}]")
        print("  F:", c["front"])
        print("  B:", c["back"])
