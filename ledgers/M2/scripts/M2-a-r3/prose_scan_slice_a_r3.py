"""M2 slice a round 3: prose scan of index.html and L01-L06 (visible text and card text).

Counts banned phrases (BUILDER_RULES 1.3-1.4), scope words (VERIFIER_RULES 2.9 / rule 4), process words,
rhetorical questions outside prompts, and lists every sentence that contains a scope word, for reading.
Run: python -I ledgers/M2/scripts/M2-a-r3/prose_scan_slice_a_r3.py <checkout-root>
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
pages = ["index"] + [f"L{n:02d}" for n in range(1, 7)]
banned = [
    "TODO", "TBD", "lorem", "...", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
    "you can add more", "important to note", "studies show", "experts agree", "well known", "obviously", "clearly",
    "it can be shown", "it is easy", "trivially", "of course", "in practice", "it is clear",
]
scope = ["always", "every", "only", "all ", "any", "same", "drives", "exactly", "never", "small", "fast", "smooth",
         "most", "typically", "generally", "usually", "several", "each"]
process = ["builder", "verifier", "round ", "fragment", "architect", "ruling", "slice", "audit", "fixed", "revised",
           "rewritten", "regenerat", "fan-out", "orchestrat", "ledger"]


def visible_text(src: str) -> str:
    src = re.sub(r"<script.*?</script>", " ", src, flags=re.S)
    src = re.sub(r"<style.*?</style>", " ", src, flags=re.S)
    src = re.sub(r'<pre class="expected".*?</pre>', " ", src, flags=re.S)
    src = re.sub(r"<pre><code class=\"language-python\".*?</code></pre>", " ", src, flags=re.S)
    src = re.sub(r"<[^>]+>", " ", src)
    return html.unescape(src)


total = {"banned": 0, "scope": 0, "process": 0, "question": 0}
for pg in pages:
    text = visible_text((root / f"course/modules/M/M2/{pg}.html").read_text(encoding="utf-8"))
    low = text.lower()
    for w in banned:
        c = low.count(w.lower())
        if c:
            total["banned"] += c
            print(f"BANNED {pg}: {w!r} x{c}")
    for w in process:
        c = low.count(w.lower())
        if c:
            total["process"] += c
            print(f"PROCESS {pg}: {w!r} x{c}")
    # rhetorical / question sentences (any '?' outside code/prompts: prompts are inside quiz <p class="prompt">)
    raw = (root / f"course/modules/M/M2/{pg}.html").read_text(encoding="utf-8")
    raw_no_prompt = re.sub(r'<p class="prompt">.*?</p>', " ", raw, flags=re.S)
    raw_no_prompt = re.sub(r"<pre><code.*?</code></pre>", " ", raw_no_prompt, flags=re.S)
    qtext = visible_text(raw_no_prompt)
    for m in re.finditer(r"[^.!?\n]*\?", qtext):
        total["question"] += 1
        print(f"QUESTION {pg}: {m.group(0).strip()[:160]}")
    sentences = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text))
    for s in sentences:
        sl = " " + s.lower() + " "
        hits = [w.strip() for w in scope if (" " + w if not w.startswith(" ") else w) in sl or w.strip() in sl and w.endswith(" ") and w in sl]
        hits = [w for w in scope if re.search(r"\b" + re.escape(w.strip()) + r"\b", sl)]
        if hits:
            total["scope"] += 1
            print(f"SCOPE {pg}: [{','.join(sorted(set(hits)))}] {s.strip()[:220]}")

cards = json.loads((root / "course/modules/M/M2/cards.json").read_text(encoding="utf-8"))
slice_cards = [c for c in cards if c["lesson"] in {"L01", "L02", "L03", "L04", "L05", "L06"}]
for c in slice_cards:
    for field in ("front", "back"):
        low = c[field].lower()
        for w in banned:
            if w.lower() in low:
                print(f"BANNED card {c['id']} {field}: {w!r}")
        for w in process:
            if w in low:
                print(f"PROCESS card {c['id']} {field}: {w!r}")
print("TOTALS", total, "slice cards", len(slice_cards))
