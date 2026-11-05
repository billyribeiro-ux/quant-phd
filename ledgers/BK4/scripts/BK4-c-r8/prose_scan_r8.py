"""Round 8: visible-text scan of project.html (tags, scripts and code blocks removed) for process words and scope words."""
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1])
src = (ROOT / "course/modules/BK/BK4/project.html").read_text(encoding="utf-8")
src = re.sub(r"<pre.*?</pre>", " ", src, flags=re.S)
src = re.sub(r"<script.*?</script>", " ", src, flags=re.S)
src = re.sub(r"<aside class=\"annotation\".*?</aside>", " ", src, flags=re.S)
text = html.unescape(re.sub(r"<[^>]+>", " ", src))
text = re.sub(r"\s+", " ", text)
process = r"\b(verifier|verify|builder|build|batch|agent|round|ledger|TODO|FIXME|placeholder|pending|draft|planner|architect|plan|Haiku|Claude|rubric-builder|fixer|slice)\b"
scope = r"\b(only|all|always|every|any|same|drives|exactly|never)\b"
print("PROCESS-WORD HITS:")
for m in re.finditer(process, text, re.I):
    print("  ", repr(text[max(0, m.start()-70):m.end()+50]))
print("SCOPE-WORD HITS:", len(re.findall(scope, text, re.I)))
for m in re.finditer(scope, text, re.I):
    print("  ", repr(text[max(0, m.start()-80):m.end()+40]))
