"""Round-28 part A: carry prefixes for PASS rows whose subject files are byte-identical since 47bac8d.

For each PASS row of part A: resolve the files its location and check name (S7 page, card, lab twin, tool, test, reference,
data); if every resolved file is byte-identical between 47bac8d and HEAD (git diff --quiet), the evidence is prefixed with
'Carried from round 27 (<files> byte-identical since 47bac8d):' unless it already starts with a 'Carried' or 'Covered' or
'Re-derived' prefix. Rows with no resolvable subject are listed and left as they are (their evidence is a command re-run
or a run recorded in the round-27 decision). Prints the counts.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
FRAG = ROOT / "ledgers/S7/data-tooling-A.json"
PATH = re.compile(r"(?<![\w/])((?:[\w\-.]+/)*[\w\-.]+\.(?:py|html|js|mjs|json|yaml|md|csv|txt|toml|css|yml|tex))(?![\w/])")
S7 = "course/modules/S/S7"
ALIAS = {"L01.html": f"{S7}/L01.html", "L02.html": f"{S7}/L02.html", "L03.html": f"{S7}/L03.html", "L04.html": f"{S7}/L04.html",
         "L05.html": f"{S7}/L05.html", "L06.html": f"{S7}/L06.html", "L07.html": f"{S7}/L07.html", "L08.html": f"{S7}/L08.html",
         "project.html": f"{S7}/project.html", "cards.json": f"{S7}/cards.json", "cards.js": f"{S7}/cards.json"}


def subjects(row: dict) -> list[str]:
    text = row["location"] + " " + row["check"]
    found: set[str] = set()
    for tok in PATH.findall(text):
        if tok in ALIAS:
            found.add(ALIAS[tok])
        elif "/" in tok and (ROOT / tok).exists():
            found.add(tok)
        elif "/" not in tok and (ROOT / tok).exists():
            found.add(tok)
        elif "/" not in tok:
            for cand in (f"{S7}/{tok}", f"tests/labs/S7/{tok}", f"tools/{tok}", f"tests/{tok}"):
                if (ROOT / cand).exists():
                    found.add(cand)
                    break
    if re.search(r"\bcards?\b", text):
        found.add(f"{S7}/cards.json")
    if re.search(r"registry|references\.json", text):
        found.add("references/references.json")
    return sorted(found)


frag = json.loads(FRAG.read_text(encoding="utf-8"))
carried, nosubj, changed = [], [], []
for row in frag["rows"]:
    if row["status"] != "PASS":
        continue
    ev = row["evidence"]
    if ev.startswith(("Covered by", "Re-derived", "Carried")):
        continue
    files = subjects(row)
    if not files:
        nosubj.append(row["id"])
        continue
    same = subprocess.run(["git", "diff", "--quiet", "47bac8d", "HEAD", "--", *files], cwd=ROOT).returncode == 0
    if not same:
        changed.append((row["id"], files))
        continue
    row["evidence"] = f"Carried from round 27 ({', '.join(files)} byte-identical since 47bac8d): " + ev
    carried.append(row["id"])
frag["rows"] = frag["rows"]
FRAG.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("carried prefix added:", len(carried))
print("PASS rows with no resolvable subject (kept as round-27 evidence):", len(nosubj), nosubj[:40])
print("PASS rows whose subject changed since 47bac8d (must re-derive):", changed)
