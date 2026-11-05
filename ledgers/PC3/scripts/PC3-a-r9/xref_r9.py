# Cross-reference scan for PC3 lessons L01-L03: every "Kind N" mention must name a block defined in that lesson
# (block titles are the <span class="block-title..."> elements). Mentions in lab code are excluded. Other-lesson refs
# are reported separately (they name a lesson number before the reference).
import re, sys, pathlib
root = pathlib.Path(sys.argv[1]) / "course/modules/PC/PC3"
KIND = r"(Definition|Assumption|Proposition|Theorem|Example|Remark)"
for page in ["L01", "L02", "L03"]:
    text = (root / f"{page}.html").read_text(encoding="utf-8")
    text = re.sub(r"<pre.*?</pre>", "", text, flags=re.S)
    titles = re.findall(r'<span class="block-title[^"]*"(?: data-grade="T")?>\s*' + KIND + r' (A?\d+(?:\.\d+)?)', text)
    defined = set(titles)
    refs = re.findall(r"\b" + KIND + r" (A?\d+(?:\.\d+)?)", re.sub(r"<[^>]+>", " ", text))
    missing = sorted(set(r for r in refs if r not in defined))
    print(page, "defined:", sorted(defined))
    print("  mentions not defined in this lesson:", missing)
