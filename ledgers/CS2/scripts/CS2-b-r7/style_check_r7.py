"""Word counts of why-it-matters paragraphs and banned-phrase scan for CS2 L05-L08 (BUILDER_RULES 1.3, 1.4, 4.2).

Usage: python -I this.py <checkout-root>
"""
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "you can add more",
          "left as an exercise", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "...", "…"]
for page in ["L05", "L06", "L07", "L08"]:
    text = (root / f"course/modules/CS/CS2/{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', text, re.S)
    plain = re.sub(r"<[^>]+>", "", m.group(1))
    print(page, "why-it-matters words:", len(plain.split()))
    for b in banned:
        for hit in re.finditer(re.escape(b), text, re.I):
            ln = text[: hit.start()].count("\n") + 1
            print("  BANNED-HIT", page, ln, repr(b))
    for w in ["builder", "verifier", "round ", "fan-out", "orchestrat", "draft"]:
        for hit in re.finditer(w, text, re.I):
            ln = text[: hit.start()].count("\n") + 1
            print("  PROCESS-HIT", page, ln, w)
print("scan done")
