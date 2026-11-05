"""Count the sentences of the spec Context dd on project.html (round 12). Usage: python3 -I context_sentences.py <checkout>"""

import re
import sys
from pathlib import Path

html = (Path(sys.argv[1]) / "course/modules/BK/BK4/project.html").read_text(encoding="utf-8")
m = re.search(r"<dt>Context</dt>\s*<dd>(.*?)</dd>", html, re.S)
text = re.sub(r"<[^>]+>", "", m.group(1)).strip()
sentences = [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", text) if s]
print("Context sentences:", len(sentences))
for i, s in enumerate(sentences, 1):
    print(i, s[:100])
