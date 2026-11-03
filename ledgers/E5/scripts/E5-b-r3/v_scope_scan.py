"""List every prose sentence in L04-L06 that contains a scope word, so each can be read and checked."""
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1])
pat = re.compile(r"\b(every|all|always|never|any|only|exactly|drives|same|whatever|each|none|nothing|must)\b", re.I)
for L in ("L04", "L05", "L06"):
    raw = (ROOT / f"course/modules/E/E5/{L}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<pre.*?</pre>", " ", raw, flags=re.S)
    txt = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw)))
    sents = [s for s in re.split(r"(?<=[.!?])\s+", txt) if pat.search(s)]
    print(L, "sentences with scope words:", len(sents))
    for s in sents:
        print("  -", s[:200])
