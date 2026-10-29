"""Round-20 delta scans for AC1-d: changed lesson/project lines, banned phrases, process words, and cards that cite changed passages."""

import json
import re
import sys
from pathlib import Path

ROOT = Path("/tmp/verify20-AC1-d")
added = [line[1:] for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines() if line.startswith("+")]
print("added lines:", len(added))
banned = re.compile(r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|obviously|clearly|important to note|studies show|experts agree|well known|historically|roughly|about 6|\.\.\.|…", re.I)
process = re.compile(r"\bround\b|builder|verifier|verification|unit report|REQUEST", re.I)
print("banned hits:", sum(1 for line in added if banned.search(line)))
print("process-word hits:", sum(1 for line in added if process.search(line)))
cards = json.loads((ROOT / "course/modules/AC/AC1/cards.json").read_text(encoding="utf-8"))
print("cards:", len(cards))
cite = re.compile(r"Remark 2\.4|Remark 1\.5|Definition 1\.3|Remark 2\.5|ratio|SCU|dollar|forfeit|Definition 1\.2|Definition 1\.1|identity|articulat|integer cents|Lab 1|multiple of|balance|Section 1|Section 2", re.I)
hits = [c["id"] for c in cards if c["lesson"] in ("L04", "L05", "L06", "L07", "L08") and cite.search(c["front"] + " " + c["back"])]
print("cards citing changed-passage vocabulary (L04-L08):", len(hits))
print(" ".join(hits))
