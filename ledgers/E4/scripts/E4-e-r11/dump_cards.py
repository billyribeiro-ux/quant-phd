"""Round 11: dump course/modules/E/E4/cards.json grouped by lesson (id, grade, front, back, basis). argv[1] = lesson or ALL."""
import json, sys
cards = json.load(open("course/modules/E/E4/cards.json", encoding="utf-8"))
want = sys.argv[1] if len(sys.argv) > 1 else "ALL"
for c in cards:
    if want in ("ALL", c["lesson"]):
        print(f'{c["id"]} [{c["lesson"]}] grade={c.get("grade")} basis={c.get("basis")!r}')
        print(f'  F: {c["front"]}')
        print(f'  B: {c["back"]}')
        if c.get("cite"):
            print(f'  cite: {c["cite"]}')
