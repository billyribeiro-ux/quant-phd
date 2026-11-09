"""Print exemplar memo prose only (no annotations, no verdict/reveal blocks), for blind scoring.

Input: course/modules/LX/LX1/project.html. Output: stdout. Removes <aside class="annotation"> blocks and
any element with data-reveal or class exemplar-verdict. Rubric table is printed separately by the verifier.
"""
import html
import re
import sys

path = sys.argv[1]
text = open(path, encoding="utf-8").read().splitlines()
start = next(i for i, line in enumerate(text) if 'id="exemplar-a"' in line)
end = next(i for i, line in enumerate(text) if 'id="self-assessment"' in line)
block = "\n".join(text[start:end])
block = re.sub(r'<aside class="annotation".*?</aside>', "", block, flags=re.S)
block = re.sub(r'<p class="exemplar-verdict"[^>]*>.*?</p>', "", block, flags=re.S)
block = re.sub(r"<article[^>]*>", "\n=== EXEMPLAR ===\n", block)
block = re.sub(r"<h4[^>]*>(.*?)</h4>", r"\n## \1\n", block, flags=re.S)
block = re.sub(r"<h5[^>]*>(.*?)</h5>", r"\n### \1\n", block, flags=re.S)
block = re.sub(r"</p>", "\n", block)
block = re.sub(r"<[^>]+>", "", block)
print(html.unescape(block))
