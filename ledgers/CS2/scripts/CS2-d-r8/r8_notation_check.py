"""Round 8: symbols used in project.html math spans and cards.json vs the notation registry (notation/notation.json)."""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
reg = json.loads((ROOT / "notation/notation.json").read_text(encoding="utf-8"))
items = reg if isinstance(reg, list) else reg.get("symbols", reg.get("entries", []))
print("registry entries:", len(items))
page = (ROOT / "course/modules/CS/CS2/project.html").read_text(encoding="utf-8")
spans = [html.unescape(a or b) for a, b in re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", page, re.S)]
print("math spans on project.html:", len(spans))
syms = sorted({t for m in spans for t in re.findall(r"\\[A-Za-z]+|[A-Za-z](?:_\w+)?|\^\\ast|\^\{[^}]*\}", m)})
print("symbols used on project.html:", syms)
reg_tokens = ["T", "\\Phi", "\\gamma_3", "\\gamma_4", "R^\\ast", "R^{e\\ast}", "R_f", "\\mathbb{Q}"]
print("registry tokens:", reg_tokens)
print("collisions on project.html:", [s for s in syms if s in reg_tokens])
cards = json.loads((ROOT / "course/modules/CS/CS2/cards.json").read_text(encoding="utf-8"))
hits = [c["id"] for c in cards if re.search(r"(?<![A-Za-z])T(?![A-Za-z])|\\Phi|gamma|R_f|R\^", c["front"] + c["back"])]
print("card hits on registry symbols:", hits)
