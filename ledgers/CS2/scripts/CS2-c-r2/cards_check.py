# Verifier scan of the CS2 L09-L11 cards: grade and basis fields, uniqueness, and the lesson each card names.
import json, sys, pathlib
root = pathlib.Path(sys.argv[1])
cards = json.loads((root / "course/modules/CS/CS2/cards.json").read_text(encoding="utf-8"))
s = [c for c in cards if c["lesson"] in ("L09", "L10", "L11")]
print("slice cards:", len(s), s[0]["id"], "to", s[-1]["id"])
print("no grade field:", [c["id"] for c in s if "grade" not in c])
print("non-T grade without cite or basis:", [c["id"] for c in s if c.get("grade") not in (None, "T") and not (c.get("basis") or c.get("cite"))])
print("ungraded cards whose back names a lab:", [c["id"] for c in s if "grade" not in c and "lab" in c["back"].lower()])
print("all ids unique:", len({c["id"] for c in cards}) == len(cards), "all fronts unique:", len({c["front"] for c in cards}) == len(cards))
