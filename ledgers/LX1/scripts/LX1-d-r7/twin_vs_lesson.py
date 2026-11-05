"""Round-7 check: every line of each lab twin's standalone output appears in the lesson's extracted text.

Whitespace runs are collapsed on both sides (the extraction collapses them). Usage:
python3 -I twin_vs_lesson.py <outdir with twin_L0x.txt> <lesson text dir>
"""
import re, sys

out, txt = sys.argv[1], sys.argv[2]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


for L in ("L01", "L02", "L03", "L04"):
    lesson = [norm(re.sub(r"^\[\d+\] ", "", ln.rstrip("\n"))) for ln in open(f"{txt}/{L}.txt", encoding="utf-8")]
    lesson_set = set(lesson)
    twin = [norm(ln) for ln in open(f"{out}/twin_{L}.txt", encoding="utf-8") if ln.strip() and not ln.startswith("exit ")]
    missing = [t for t in twin if t not in lesson_set]
    print(L, "twin lines", len(twin), "not verbatim in lesson text:", len(missing))
    for m in missing:
        print("   MISSING:", m)
