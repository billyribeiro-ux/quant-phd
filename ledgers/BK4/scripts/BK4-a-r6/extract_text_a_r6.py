"""Extract visible text per raw line of a BK4 page (slice a, round 6).

Usage: python3 -I extract_text_a_r6.py <html-file> > out.txt
Each output line is '<raw line number>\t<visible text of that line>'. Tags are removed, entities
decoded, MathJax delimiters kept. Lines with no visible text are skipped. Script/style content is dropped.
"""
import html
import re
import sys

path = sys.argv[1]
raw = open(path, encoding="utf-8").read().split("\n")
in_script = False
for n, line in enumerate(raw, 1):
    s = line
    if re.search(r"<script", s):
        in_script = True
    if in_script:
        if re.search(r"</script>", s):
            in_script = False
        continue
    s = re.sub(r"<style.*?</style>", "", s)
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"</?[a-zA-Z][^>]*>", "", s)
    s = html.unescape(s).strip()
    if s:
        print(f"{n}\t{s}")
