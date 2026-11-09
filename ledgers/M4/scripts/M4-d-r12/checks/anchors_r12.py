"""Verifier round 12: in-page anchors and local file links in project.html resolve."""
import re
from pathlib import Path
root = Path("course/modules/M/M4")
s = (root / "project.html").read_text(encoding="utf-8")
ids = set(re.findall(r'id="([^"]+)"', s))
anchors = re.findall(r'href="#([^"]+)"', s)
missing = sorted({a for a in anchors if a not in ids})
print("in-page anchors:", len(anchors), "missing:", missing)
files = re.findall(r'href="([^"#]+)', s)
local = [f for f in files if not f.startswith(("http", "mailto"))]
bad = [f for f in local if not (root / f).exists() and not (Path("course/modules/M") / f).exists()]
print("local links:", len(local), "missing files:", sorted(set(bad)))
hub = (root / "index.html").read_text(encoding="utf-8")
print("index.html#placement target present:", 'id="placement"' in hub)
