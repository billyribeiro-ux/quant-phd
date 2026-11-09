"""PC3-b round 16: scan visible prose of L04-L06 for banned phrases, process words, scope words.

Usage: python -I ledgers/PC3/scripts/PC3-b-r16/prose_scan.py <repo-root>
Strips <script>, <style>, <pre> blocks and tags, splits into sentences, and prints every sentence that
contains a banned phrase, a process word or a scope word, with its line number in the source file.
"""
import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
PAGES = ["L04", "L05", "L06"]
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly"]
PROCESS = [r"\bbuild", r"\bbuilder", r"\bround\b", r"\bverifier", r"REQUESTS", r"unit report", r"\bverif"]
SCOPE = [r"\bonly\b", r"\ball\b", r"\balways\b", r"\bevery\b", r"\bany\b", r"\bsame\b", r"\bexactly\b", r"\bnever\b"]
ELLIPSIS = re.compile(r"\.\s?\.\s?\.")
for page in PAGES:
    path = root / "course/modules/PC/PC3" / f"{page}.html"
    raw = path.read_text(encoding="utf-8")
    # keep line numbers: blank out script/style/pre contents but keep newlines
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    s = re.sub(r"<script.*?</script>", blank, raw, flags=re.S)
    s = re.sub(r"<style.*?</style>", blank, s, flags=re.S)
    s = re.sub(r"<pre.*?</pre>", blank, s, flags=re.S)
    s = re.sub(r"<code class=\"language-python\".*?</code>", blank, s, flags=re.S)
    s = re.sub(r"<[^>]+>", lambda m: re.sub(r"[^\n]", " ", m.group(0)), s)
    s = html.unescape(s)
    # sentence split per line, keeping source line numbers
    counts = {"banned": 0, "process": 0, "ellipsis": 0}
    scope_hits = []
    for ln, line in enumerate(s.split("\n"), 1):
        if not line.strip():
            continue
        sentences = re.split(r"(?<=[.!?])\s+", line)
        for sent in sentences:
            low = sent.lower()
            for b in BANNED:
                if b.lower() in low:
                    counts["banned"] += 1
                    print(f"{page}:{ln} BANNED[{b}]: {sent.strip()[:220]}")
            for p in PROCESS:
                if re.search(p, sent, flags=re.I if p != "REQUESTS" else 0):
                    counts["process"] += 1
                    print(f"{page}:{ln} PROCESS[{p}]: {sent.strip()[:220]}")
            if ELLIPSIS.search(sent):
                counts["ellipsis"] += 1
                print(f"{page}:{ln} ELLIPSIS: {sent.strip()[:220]}")
            for sc in SCOPE:
                if re.search(sc, sent, flags=re.I):
                    scope_hits.append((ln, sc, sent.strip()[:260]))
    print(f"== {page} banned={counts['banned']} process={counts['process']} ellipsis={counts['ellipsis']} scope_sentences={len(scope_hits)}")
    for ln, sc, sent in scope_hits:
        print(f"{page}:{ln} SCOPE[{sc}]: {sent}")
