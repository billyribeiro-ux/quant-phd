# Round-3: which embedded series have >= 3 tenors (L08 canon-break claim), and which pages declare data-files.
import json, re, sys
from pathlib import Path
root = Path(sys.argv[1])
m = json.loads((root / "course/assets/data/market/MANIFEST.json").read_text(encoding="utf-8"))
for i, ds in enumerate(m["datasets"]):
    print(i, ds.get("name", ds.get("id", "?")), ds.get("columns"))
tenor_like = [c for ds in m["datasets"] for c in ds.get("columns", []) if re.search(r"\d+y|_\d+|tenor", c, re.I)]
print("tenor-like columns:", tenor_like)
for p in ["L07.html", "L08.html", "L09.html"]:
    t = (root / "course/modules/M/M3" / p).read_text(encoding="utf-8")
    print(p, "data-files attributes:", re.findall(r'data-files="[^"]*"', t))
