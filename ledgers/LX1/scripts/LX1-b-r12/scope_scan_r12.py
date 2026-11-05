"""LX1-b round 12: list every scope word (every, all, never, any, only, same, exactly, the first, several, most, many,
always) in L03.html and L04.html prose (tags, code and math stripped as text), with its context, for checking against
a computation or an explicit hypothesis. Run: .venv/bin/python -I <this file> <checkout>
"""
import html
import re
import sys

root = sys.argv[1]
scope = r"\b(every|all|never|any|only|same|panics|many|several|most|always|the first|exactly)\b"
for name in ("L03", "L04"):
    raw = open(f"{root}/course/modules/LX/LX1/{name}.html", encoding="utf-8").read()
    t = re.sub(r"<pre[^>]*>.*?</pre>", "", raw, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = re.sub(r"\\\((.*?)\\\)", r" \1 ", t, flags=re.S)
    t = re.sub(r"\s+", " ", t)
    print("==", name)
    for m in re.finditer(scope, t, re.I):
        print(f"[{m.group(0)}] ...{t[max(0, m.start() - 110): m.end() + 70]}...")
