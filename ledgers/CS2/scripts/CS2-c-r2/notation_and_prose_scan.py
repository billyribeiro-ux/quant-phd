"""Round-2: notation scan (registered symbols and macros in L09-L11 math) and process-word scan on visible text and card text."""

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
reg = json.loads((ROOT / "notation/notation.json").read_text(encoding="utf-8"))
macros = set(reg["macros"].keys())
registered_symbols = ["T", r"\Phi", r"\gamma_3", r"\gamma_4", r"R^\ast", r"R^{e\ast}", r"R_f", r"\mathbb{Q}"]
pages = ["L09", "L10", "L11"]
segments_total = 0
for page in pages:
    raw = (ROOT / f"course/modules/CS/CS2/{page}.html").read_text(encoding="utf-8")
    segs = [html.unescape(a or b) for a, b in re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", raw, re.S)]
    segments_total += len(segs)
    used_macros = sorted({m for s in segs for m in re.findall(r"\\[A-Za-z]+", s) if m in macros})
    sym_hits = sorted({sym for sym in registered_symbols for s in segs if sym in s})
    print(page, "math segments", len(segs), "| registered macros used:", used_macros, "| registered symbols used:", sym_hits)
print("total math segments:", segments_total)

pat = re.compile(r"\b(verifier|builder|audit|revised|round|TODO|placeholder|pending|unverified|lorem|tbd|fixme|we|I|my|our)\b", re.I)
cards = json.loads((ROOT / "course/modules/CS/CS2/cards.json").read_text(encoding="utf-8"))
for page in pages:
    raw = (ROOT / f"course/modules/CS/CS2/{page}.html").read_text(encoding="utf-8")
    t = re.sub(r'<pre><code class="language-python".*?</code></pre>', " ", raw, flags=re.S)
    t = re.sub(r'<pre class="expected".*?</pre>', " ", t, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", t))
    text = re.sub(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", " ", text, flags=re.S)  # math is checked by the notation scan
    hits = sorted({m.group(0) for m in pat.finditer(text)})
    print(page, "process-word hits in prose (math removed):", hits)
card_hits = []
for c in cards:
    if c["lesson"] in pages:
        s = re.sub(r"\\\((.*?)\\\)", " ", c["front"] + " " + c["back"])
        for m in pat.finditer(s):
            card_hits.append((c["id"], m.group(0)))
print("process-word hits in L09-L11 card text (math removed):", card_hits)
