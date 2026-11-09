"""FC1-a round 2: prose scans over the hub and L01-L03 (learner text only; <pre> code blocks and <script> removed).

Covers: banned phrases (BUILDER 1.3-1.4 and process words), ellipses, external references, data files,
math macros and single-letter symbols against notation/notation.json, strong scope words, concept dfn/link inventory,
and every mention of the unregistered or registry-only sources. Run from the checkout root.
"""

import json
import re
from collections import Counter
from pathlib import Path

PAGES = [
    "course/modules/FC/FC1/index.html",
    "course/modules/FC/FC1/L01.html",
    "course/modules/FC/FC1/L02.html",
    "course/modules/FC/FC1/L03.html",
]
BANNED = re.compile(
    r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|"
    r"important to note|studies show|experts agree|well known|obviously|clearly|builder|verifier|planner|"
    r"architect|ledger|REQUEST|checked directly|it can be shown",
    re.I,
)
SCOPE = re.compile(r"\b(every|all|always|never|any|across|drives|only)\b", re.I)
SOURCES = re.compile(r"McLeay|Mishkin|mishkin|Harris|harris", re.I)
notation = json.loads(Path("notation/notation.json").read_text(encoding="utf-8"))
registered_macros = set(notation["macros"])

for page in PAGES:
    raw = Path(page).read_text(encoding="utf-8")
    prose = re.sub(r"<pre><code.*?</code></pre>", "", raw, flags=re.S)
    prose = re.sub(r"<script.*?</script>", "", prose, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", prose)
    name = page.split("/")[-1]
    banned = [m.group(0) for m in BANNED.finditer(text)]
    ellipses = [text[max(0, m.start() - 40): m.end() + 10].replace("\n", " ") for m in re.finditer(r"\.\.\.|…", text)]
    external = re.findall(r"https?://|<img|<svg|<iframe|data-chart|data-files|assets/data", raw)
    sources = [text[max(0, m.start() - 30): m.end() + 30].replace("\n", " ") for m in SOURCES.finditer(text)]
    scope = Counter(m.group(0).lower() for m in SCOPE.finditer(text))
    math = [m.group(1) or m.group(2) or "" for m in re.finditer(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", prose, flags=re.S)]
    commands = Counter(c for s in math for c in re.findall(r"\\[A-Za-z]+", s))
    custom = sorted(c for c in commands if c not in registered_macros and c not in {
        "\\times", "\\ell", "\\sum", "\\rho", "\\le", "\\qquad", "\\text", "\\dots", "\\blacksquare", "\\ge",
        "\\frac", "\\ne", "\\to", "\\cdot", "\\varphi", "\\kappa", "\\ldots", "\\lambda", "\\prod", "\\in",
        "\\sigma", "\\pi", "\\ge", "\\le", "\\left", "\\right", "\\mid", "\\sqrt", "\\cdots", "\\mathrm", "\\dfrac",
    })
    letters = Counter(c for s in math for c in re.findall(r"(?<![\\A-Za-z])([A-Za-z])(?![A-Za-z])", s))
    registered_symbols = [s["symbol"] for s in notation["symbols"]]
    reg_hits = {sym: sum(s.count(sym.split(",")[0].strip(" \\^{}")) for s in math) for sym in ["T", "Q", "R_f"]}
    print(f"== {name}")
    print("banned/process hits:", banned)
    print("ellipses outside code:", ellipses)
    print("external/data/media markers:", external)
    print("source mentions:", sources)
    print("scope words (every/all/always/never/any/across/drives/only):", dict(scope))
    print("math segments:", len(math), "macros used not in registry (beyond standard KaTeX):", custom)
    print("single-letter symbols:", dict(sorted(letters.items())))
    print("registered-symbol hits (T, Q, R_f) inside math:", reg_hits, "registered:", registered_symbols)
    dfns = re.findall(r'<dfn id="([^"]+)" data-concept="([^"]+)"', raw)
    links = re.findall(r'class="concept" data-concept="([^"]+)"', raw)
    print("dfn with data-concept:", dfns)
    print("concept links:", links)
