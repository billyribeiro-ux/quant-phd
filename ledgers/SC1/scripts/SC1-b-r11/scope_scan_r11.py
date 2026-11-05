"""List scope words (every, all, always, any, never, only, exactly, same, almost surely, converges, for all, each, must)
in the prose of L04-L06 with their line numbers. Standard library only. Run: python -I -W error scope_scan_r11.py"""
import re
from pathlib import Path

SC1 = Path("/Users/billyribeiro/.fanout/wt/verifyE11-SC1-b/course/modules/SC/SC1")
pat = re.compile(r"\b(every|all|always|any|never|only|exactly|same|almost surely|converges?|for all|each|must|cannot)\b", re.I)
for name in ("L04.html", "L05.html", "L06.html"):
    total = 0
    for n, line in enumerate((SC1 / name).read_text(encoding="utf-8").split("\n"), 1):
        if 'data-run' in line or line.lstrip().startswith('"""'):
            continue
        text = re.sub(r"<[^>]+>", " ", line)
        found = sorted({m.group(1).lower() for m in pat.finditer(text)})
        if found:
            total += 1
            print(name, n, found)
    print(name, "lines with scope words:", total)
