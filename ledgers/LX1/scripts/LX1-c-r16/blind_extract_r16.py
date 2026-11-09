"""Round-15 verifier (ruling 15): extract each exemplar's memo prose only.

Drops <aside class="annotation">, the verdict paragraph (class exemplar-verdict), and data-score(s)/data-level
attributes. Usage: python -I blind_extract_r16.py <checkout_root> > out/blind_prose_r16.txt
"""
import html
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1]).resolve()
src = (root / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
for ex in ("exemplar-a", "exemplar-b"):
    start = src.index(f'<article class="exemplar" id="{ex}"')
    end = src.index("</article>", start)
    body = src[start:end]
    body = re.sub(r'<aside class="annotation".*?</aside>', " ", body, flags=re.S)
    body = re.sub(r'<p class="exemplar-verdict".*?</p>', " ", body, flags=re.S)
    body = re.sub(r"<h[45][^>]*>.*?</h[45]>", lambda m: "\n[" + html.unescape(re.sub(r"<[^>]+>", "", m.group(0))) + "]\n", body, flags=re.S)
    passages = re.findall(r'<div class="memo-text">(.*?)</div>', body, flags=re.S)
    print(f"=== {ex}: {len(passages)} passages (memo prose only)")
    for i, p in enumerate(passages, 1):
        text = html.unescape(re.sub(r"<[^>]+>", " ", p))
        text = re.sub(r"\s+", " ", text).strip()
        print(f"--- passage {i}: {text}")
