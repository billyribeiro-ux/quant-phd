"""Round 18 prose scan of LX1 lesson pages: process words, banned strings, scope words, ellipses (outside code).

Usage (checkout root): .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r19/prose_scan_r18.py course/modules/LX/LX1/L01.html ...
"""
import html
import re
import sys

WORDS = re.compile(
    r"\b(build|builder|builders|round|rounds|verifier|verifiers|REQUESTS|unit report|TODO|TBD|lorem|"
    r"for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|"
    r"studies show|experts agree|it is well known|obviously|clearly|every|all|always|never|any|only|exactly|same|"
    r"drives|offsets|as much as|the first|the last|central banking|bubbles|panics)\b",
    re.I,
)
for path in sys.argv[1:]:
    t = open(path, encoding="utf-8").read()
    t = re.sub(r"<pre.*?</pre>", "", t, flags=re.S)
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    print(f"== {path}")
    for n, line in enumerate(t.split("\n"), 1):
        for mm in WORDS.finditer(line):
            s, e = max(0, mm.start() - 60), min(len(line), mm.end() + 60)
            print(f"  [{mm.group(0)}] ...{' '.join(line[s:e].split())}...")
    print("  ellipsis outside code:", len(re.findall(r"\.\.\.", t)))
