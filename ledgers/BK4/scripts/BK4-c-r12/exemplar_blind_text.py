"""Blind extraction: exemplar memo prose with annotation asides and the official-scoring paragraphs removed."""
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
lines = src.splitlines()
start = next(i for i, l in enumerate(lines) if 'id="exemplar-a"' in l)
end = next(i for i, l in enumerate(lines) if 'id="self-assessment"' in l)
chunk = "\n".join(lines[start:end])
chunk = re.sub(r'<aside class="annotation".*?</aside>', "", chunk, flags=re.S)
chunk = re.sub(r'<p class="exemplar-verdict".*?</p>', "", chunk, flags=re.S)
text = re.sub(r"<[^>]+>", "\n", chunk)
text = re.sub(r"\n\s*\n+", "\n", text)
print(text.strip())
