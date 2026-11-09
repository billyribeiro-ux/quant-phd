"""Banned-phrase, ellipsis and process-word scan of hub and L01-L03 learner text (round 4)."""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "course/modules/E/E1"
banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "round", "verifier", "builder", "REQUEST", "unit report"]
for page in ["index.html", "L01.html", "L02.html", "L03.html"]:
    src = (root / page).read_text(encoding="utf-8")
    src = re.sub(r"<script.*?</script>|<style.*?</style>", " ", src, flags=re.S)
    src = re.sub(r"<pre.*?</pre>", " ", src, flags=re.S)  # code and expected blocks excluded
    text = re.sub(r"<[^>]+>", " ", src)
    for b in banned:
        for m in re.finditer(re.escape(b), text, flags=re.I):
            print(page, "BANNED/PROCESS hit:", repr(b), "...", re.sub(r"\s+", " ", text[max(0, m.start() - 50):m.end() + 50]))
    for m in re.finditer(r"\.\.\.", text):
        print(page, "ellipsis:", re.sub(r"\s+", " ", text[max(0, m.start() - 40):m.end() + 40]))
    print(page, "scanned", len(text), "chars of learner text")
