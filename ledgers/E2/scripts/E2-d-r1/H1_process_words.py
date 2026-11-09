# H1: process-word scan (ruling-independent list from the base script) over the three cards changed since 2a805c83,
# and over the whole cards.json as a secondary check.
import json, re, sys
from pathlib import Path
root = Path(sys.argv[1])
items = json.loads((root / "course/modules/E/E2/cards.json").read_text(encoding="utf-8"))
changed = {"E2-c102", "E2-c105", "E2-c136"}
pat = re.compile(r"\b(round|rulings?|verifiers?|fixers?|builders?|drafts?|TODO|verif\w*|fixed|audit\w*|reviewers?|closing|fixture|delta)\b", re.I)
allhits = []
for c in items:
    h = pat.findall(c["front"] + " " + c["back"])
    if h:
        allhits.append((c["id"], h))
    if c["id"] in changed:
        print(c["id"], "process-word hits:", h)
print("whole cards.json process-word hits:", allhits)
