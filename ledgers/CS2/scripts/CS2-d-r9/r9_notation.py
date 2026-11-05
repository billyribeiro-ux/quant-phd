"""Round-9 notation check for project.html (and cards.json backs): every math span's macros must be registered,
and every single-letter or subscripted symbol used on the page must not collide with a registered symbol meaning.
Prints the registry symbols, the macros used, and the distinct symbols found in math spans."""
import json
import re
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MOD = ROOT / "course" / "modules" / "CS" / "CS2"
nj = json.loads((ROOT / "notation" / "notation.json").read_text(encoding="utf-8"))
macros = set(nj["macros"])
symbols = nj.get("symbols", {})
print("registry macros:", sorted(macros))
print("registry symbols:", sorted(symbols) if isinstance(symbols, dict) else symbols)
page = (MOD / "project.html").read_text(encoding="utf-8")
spans = re.findall(r"\\\((.*?)\\\)", page, flags=re.S)
spans += re.findall(r"\$\$(.*?)\$\$", page, flags=re.S)
spans_html = [html.unescape(re.sub(r"<[^>]+>", "", s)) for s in spans]
print("math spans on project.html:", len(spans_html))
used_macros = sorted({m for s in spans_html for m in re.findall(r"\\[A-Za-z]+", s)})
print("macros used:", used_macros)
bad_macros = [m for m in used_macros if m not in macros and m not in ("\\frac", "\\dots", "\\cdots", "\\sum", "\\le", "\\ge", "\\ldots", "\\varepsilon", "\\delta", "\\lfloor", "\\rfloor", "\\lceil", "\\rceil", "\\text", "\\min", "\\max", "\\mathbb", "\\Phi", "\\phi", "\\log", "\\cdot", "\\in", "\\ne", "\\sqrt", "\\bar", "\\left", "\\right", "\\,", "\\;", "\\le", "\\to", "\\mathrm", "\\mathbf", "\\sim", "\\equiv", "\\infty", "\\mid")]
print("used macros not in registry and not plain TeX:", bad_macros)
letters = sorted({t for s in spans_html for t in re.findall(r"(?<![\\A-Za-z])([A-Za-z])(?![A-Za-z])", s)})
print("single-letter symbols in math spans:", letters)
