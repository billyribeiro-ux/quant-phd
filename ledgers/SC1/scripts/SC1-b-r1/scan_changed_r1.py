"""Scan the three changed slice-b lines (L05.html:375, index.html:33, cards.json SC1-c238) with the
check_pages BANNED list and a process-word list. Run: python -I scan_changed_r1.py <checkout>."""
import json
import re
import sys

ROOT = sys.argv[1]
sys.path.insert(0, ROOT + "/tools")
import check_pages as cp  # noqa: E402

PROCESS = r"\b(round|rounds?|verifier|ledger|fragment|fixer|ruling|delta|earlier|corrected|previous|fixed)\b"
SCOPE = r"\b(only|all|always|every|any|same|drives|exactly)\b"
texts = {
    "L05.html:375": open(ROOT + "/course/modules/SC/SC1/L05.html", encoding="utf-8").read().split("\n")[374],
    "index.html:33": open(ROOT + "/course/modules/SC/SC1/index.html", encoding="utf-8").read().split("\n")[32],
}
cards = json.load(open(ROOT + "/course/modules/SC/SC1/cards.json", encoding="utf-8"))
c238 = [c for c in cards if c["id"] == "SC1-c238"][0]
texts["cards SC1-c238"] = c238["front"] + " " + c238["back"]
for name, t in texts.items():
    banned = [p for p in cp.BANNED if re.search(p, t, re.I)]
    proc = re.findall(PROCESS, t, re.I)
    scope = re.findall(SCOPE, t, re.I)
    print(f"{name}: banned={banned} process={proc} scope={scope}")
