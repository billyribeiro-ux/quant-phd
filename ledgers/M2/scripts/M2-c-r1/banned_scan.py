"""Verifier script (M2 slice c, round 1): banned-phrase and scope-word scan of L13-L18 visible text.

Prints each hit with its line number and a 90-character context, after stripping tags and math delimiters.
"""

import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1]) / "course/modules/M/M2"
pattern = re.compile(
    r"roughly|historically|important to note|clearly|obviously|can be shown|well known|studies show|"
    r"experts agree|beyond the scope|for brevity|left as an exercise|TODO|TBD|lorem|you can add|"
    r"builder|verifier|REQUEST|unit report|\.\.\.|…|\bround\b|typically|in practice|\bmost\b|"
    r"\balways\b|\bonly\b|\bevery\b|\ball\b|\bsame\b|\bdrives\b|\boffsets\b|\braises\b|\bsmall\b|\bfast\b|"
    r"\bsmooth\b|\bsimple\b|\bclearly\b|\bjust\b|\bnever\b",
    re.I,
)
for n in range(13, 19):
    text = (root / f"L{n:02d}.html").read_text(encoding="utf-8")
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    lines = text.split("\n")
    for ln, line in enumerate(lines, 1):
        for m in pattern.finditer(line):
            s = max(0, m.start() - 45)
            print(f"L{n:02d} line{ln}: ...{line[s:m.end() + 45].strip()}...  [{m.group(0)}]")
