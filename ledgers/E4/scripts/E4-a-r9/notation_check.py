"""List every LaTeX command used in the E4 slice pages and its registry entry in notation/notation.json."""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
pages = [root / "course/modules/E/E4" / p for p in ("index.html", "L01.html", "L02.html", "L03.html")]
text = "\n".join(p.read_text(encoding="utf-8") for p in pages)
used = sorted(set(re.findall(r"\\[A-Za-z]+", text)))
reg = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))
macros = reg["macros"]
symbols = reg["symbols"]
print("macro entries:", len(macros) if hasattr(macros, "__len__") else type(macros))
blob_m = json.dumps(macros, ensure_ascii=False)
blob_s = json.dumps(symbols, ensure_ascii=False)
for cmd in used:
    name = cmd[1:]
    in_m = (f'"\\\\{name}"' in blob_m) or (f'"{cmd}"' in blob_m) or (f'\\\\{name}' in blob_m)
    in_s = (f"\\{name}" in blob_s) or (f'"{cmd}"' in blob_s)
    print(f"{cmd:12s} macro_registry={in_m} symbol_registry={in_s}")
