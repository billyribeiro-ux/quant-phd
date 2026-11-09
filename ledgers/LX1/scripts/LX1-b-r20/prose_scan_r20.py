"""Round 20 prose scan of LX1 slice-b pages (L01, L03, L04): process words, banned strings, scope words, ellipses.

Math spans, code blocks and scripts are removed first; the rest is de-tagged and unescaped. Run from the checkout root:
.venv/bin/python -I ledgers/LX1/scripts/LX1-b-r20/prose_scan_r20.py course/modules/LX/LX1/L01.html ...
"""
import html
import re
import sys

WORDS = re.compile(
    r"\b(build|builder|builders|round|rounds|verifier|verifiers|REQUESTS|unit report|TODO|TBD|lorem|"
    r"for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|"
    r"studies show|experts agree|it is well known|obviously|clearly|every|all|always|never|any|only|exactly|same|"
    r"drives|offsets|as much as|the first|the last|central banking|bubbles|panics|proves|prove|shows)\b",
    re.I,
)
for path in sys.argv[1:]:
    t = open(path, encoding="utf-8").read()
    t = re.sub(r"<pre.*?</pre>", "", t, flags=re.S)
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S)
    t = re.sub(r"\\\((.*?)\\\)", " MATH ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    print(f"== {path}")
    hits = 0
    for n, line in enumerate(t.split("\n"), 1):
        for mm in WORDS.finditer(line):
            hits += 1
            s, e = max(0, mm.start() - 70), min(len(line), mm.end() + 60)
            print(f"  [{mm.group(0)}] ...{' '.join(line[s:e].split())}...")
    print("  scope/process hits:", hits)
    print("  ellipsis outside code/math:", len(re.findall(r"\.\.\.", t)), " banned-literal hits:",
          len(re.findall(r"\b(TODO|TBD|lorem|for brevity|details omitted|left as an exercise)\b", t)))
