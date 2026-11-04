"""LX1-a r1: banned-phrase, process-word, scope-word and why-it-matters word-count scan over hub, L01, L02 (tags stripped, math kept)."""
import html, re, sys
FILES = ["course/modules/LX/LX1/index.html", "course/modules/LX/LX1/L01.html", "course/modules/LX/LX1/L02.html"]
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "...", "…"]
PROCESS = [r"\bbuild(er)?s?\b", r"\bverif(y|ier|ied|ication)\b", r"\bround\b", r"\brounds? \d", r"REQUEST", r"unit report",
           r"\bLX1 ledger\b", r"\bfixer\b", r"\bplanner\b", r"\bplan\b"]
SCOPE = [r"\bevery\b", r"\ball\b", r"\balways\b", r"\bnever\b", r"\bany\b", r"\bsame\b", r"\bdrives?\b", r"\bexactly\b",
         r"\bonly\b", r"\bmost\b", r"\busual\b", r"\bthe first\b", r"\bthe last\b", r"\bbubbles?\b", r"\bpanics?\b"]
for f in FILES:
    raw = open(f, encoding="utf-8").read()
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    body = re.sub(r'<pre class="expected".*?</pre>', " ", body, flags=re.S)
    body = re.sub(r"<pre><code class=\"language-python\".*?</code></pre>", " ", body, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    text = re.sub(r"\s+", " ", text)
    print("== FILE", f, "chars", len(text))
    for b in BANNED:
        for m in re.finditer(re.escape(b), text):
            print("BANNED", repr(b), "...", text[max(0, m.start()-80): m.end()+60])
    for p in PROCESS:
        for m in re.finditer(p, text):
            print("PROCESS", p, "...", text[max(0, m.start()-90): m.end()+60])
    if "L01" in f or "L02" in f or "index" in f:
        pass
    wim = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, re.S)
    if wim:
        t = html.unescape(re.sub(r"<[^>]+>", " ", wim.group(1)))
        print("WHY-IT-MATTERS words", len(t.split()))
    for p in SCOPE:
        hits = [m.start() for m in re.finditer(p, text, re.I)]
        if hits:
            print("SCOPE", p, len(hits))
