"""Round-4 independent check: scope-word counts (visible prose, labs excluded) and single-letter math symbols in L04-L06."""
import html
import re
from pathlib import Path

WORDS = ["every", "all", "never", "any", "always", "only", "exactly", "same", "drives"]
for p in ["L04", "L05", "L06"]:
    raw = Path(f"course/modules/FC/FC2/{p}.html").read_text(encoding="utf-8")
    prose = re.sub(r'<section class="lab".*?</section>', " ", raw, flags=re.S)
    prose = re.sub(r"<[^>]+>", " ", prose)
    prose = html.unescape(prose).lower()
    counts = {w: len(re.findall(r"\b%s\b" % w, prose)) for w in WORDS}
    print(p, "scope words (prose, labs excluded):", counts)
    maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", raw, re.S)
    body = " ".join(m for pair in maths for m in pair if m)
    body = re.sub(r"\\(text|mathrm|operatorname|mathbb|mathcal|mathbf)\{[^}]*\}", " ", body)
    letters = sorted(set(re.findall(r"(?<![\\a-zA-Z])([A-Za-z])(?![a-zA-Z])", body)))
    print(p, "single-letter math symbols:", "".join(letters))
    print(p, "T as symbol (standalone T in math):", len(re.findall(r"(?<![\\a-zA-Z])T(?![a-zA-Z])", body)))
    print(p, "Phi/gamma/R^*/R^{e*}/Q occurrences:", len(re.findall(r"\\Phi|\\gamma|\\ast|R\^\{e|\\mathbb\{Q\}", body)))
