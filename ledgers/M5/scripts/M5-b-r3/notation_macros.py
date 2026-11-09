"""Backslash macros used on the slice pages, and the registered macro names (notation/notation.json)."""
import collections, json, re
from pathlib import Path
reg = json.loads(Path("notation/notation.json").read_text(encoding="utf-8"))
print("registered macros:", sorted(reg["macros"]))
for f in ("L05", "L06", "L07"):
    s = Path(f"course/modules/M/M5/{f}.html").read_text(encoding="utf-8")
    c = collections.Counter(re.findall(r"\\([A-Za-z]+)", s))
    print(f, dict(c.most_common()))
    print(f, "registered macros used:", {m: c[m[1:]] for m in reg["macros"] if c.get(m[1:])})
