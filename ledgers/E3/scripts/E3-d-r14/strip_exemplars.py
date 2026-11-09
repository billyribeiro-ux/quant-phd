"""Strip the rubric exemplar annotations, verdict lines and score attributes from project.html (ruling 15).

Writes the rubric table and exemplar memo prose only. Drops every <aside class="annotation">, every
<p class="exemplar-verdict">, and the data-scores, data-level and data-label attributes of the exemplar
articles and the annotation list items. Usage: strip_exemplars.py <project.html> <out.html>
"""

import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
out = re.sub(r'<aside class="annotation".*?</aside>', "", src, flags=re.S)
out = re.sub(r'<p class="exemplar-verdict".*?</p>', "", out, flags=re.S)
out = re.sub(r'\s(data-scores|data-level|data-label)="[^"]*"', "", out)
out = re.sub(r"<li class=\"(meets|misses)\"[^>]*>.*?</li>", "", out, flags=re.S)
start = out.index('<h3 id="rubric-heading">')
end = out.index('<section class="rubric-self"')
open(sys.argv[2], "w", encoding="utf-8").write(out[start:end])
print("stripped bytes", len(out[start:end]))
