"""Print each quiz option of L04-L06 with its data-correct marker, so the key can be compared with the stated answer."""
import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
for lesson in ("L04", "L05", "L06"):
    s = (root / f"course/modules/E/E1/{lesson}.html").read_text(encoding="utf-8")
    quiz = s[s.index('<section class="quiz"'):]
    quiz = quiz[: quiz.index("</section>")]
    print("==", lesson, "options:", len(re.findall(r'<label class="option"', quiz)),
          "correct markers:", len(re.findall(r"data-correct", quiz)))
    for attrs, body in re.findall(r'<label class="option"([^>]*)>(.*?)</label>', quiz, re.S):
        text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", body))).strip()
        print(("*" if "data-correct" in attrs else "-"), text[:70])
