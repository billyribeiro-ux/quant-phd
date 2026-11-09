"""Round-2 quiz key check for M2 L13-L18: each quiz item's keyed option (data-correct) and numeric answers, with explanation presence.

Run: python -I quiz_keys_r2.py <checkout_root>
"""

import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "course/modules/M/M2"
for n in range(13, 19):
    src = (root / f"L{n}.html").read_text(encoding="utf-8")
    quiz = src[src.index('<section class="quiz"') :]
    items = re.split(r'<li class="item"', quiz)[1:]
    print(f"L{n}: items={len(items)}")
    for k, it in enumerate(items, 1):
        kind = re.search(r'data-kind="(\w+)"', it)
        ans = re.search(r'data-answer="([^"]*)"', it)
        opts = re.findall(r'<label class="option"( data-correct)?>(.*?)</label>', it, re.S)
        correct = [html.unescape(re.sub(r"<[^>]+>", "", o[1])).strip()[:70] for o in opts if o[0]]
        expl = re.search(r'class="explanation"', it) is not None
        print(f"  q{k} kind={kind.group(1) if kind else None} answer={ans.group(1) if ans else None} n_options={len(opts)} correct={correct} explanation={expl}")
