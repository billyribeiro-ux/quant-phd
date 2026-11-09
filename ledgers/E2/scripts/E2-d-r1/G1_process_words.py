# Scans the 8 changed E2 cards for process words (round, ruling, verifier, fixer, draft, TODO, verify...) as whole words.
import json, re, sys
from pathlib import Path
root = Path(sys.argv[1])
items = json.loads((root / "course/modules/E/E2/cards.json").read_text(encoding="utf-8"))
changed = {"E2-c025", "E2-c037", "E2-c051", "E2-c059", "E2-c060", "E2-c088", "E2-c105", "E2-c130"}
pat = re.compile(r"\b(round|rulings?|verifiers?|fixers?|builders?|drafts?|TODO|verif\w*|fixed|audit\w*|reviewers?|closing)\b", re.I)
for c in items:
    if c["id"] in changed:
        print(c["id"], "process-word hits:", pat.findall(c["front"] + " " + c["back"]))
