"""Round-11: owner module of every data-concept linked on L04-L06, checked against the E4 closure (curriculum.json concepts)."""
import json
import re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE11-E4-b")
C = json.loads((ROOT / "curriculum/curriculum.json").read_text(encoding="utf-8"))["concepts"]
CLOSURE = {"E1", "E2", "E3", "M1", "M2", "M3", "M4", "M7", "P0.1", "E4"}
pairs = 0
bad = 0
for p in ["L04", "L05", "L06"]:
    t = (ROOT / f"course/modules/E/E4/{p}.html").read_text(encoding="utf-8")
    for cid in sorted(set(re.findall(r'data-concept="([^"]+)"', t))):
        pairs += 1
        mod = C.get(cid, {}).get("module")
        ok = mod in CLOSURE
        bad += 0 if ok else 1
        print(p, cid, mod, "OK" if ok else "OUT-OF-CLOSURE")
print("page-concept pairs", pairs, "out of closure", bad)
