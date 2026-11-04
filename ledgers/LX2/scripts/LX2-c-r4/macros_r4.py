"""LX2-c round 4: count TeX control sequences on project.html (for the notation row)."""

import collections
import re
from pathlib import Path

text = Path("course/modules/LX/LX2/project.html").read_text(encoding="utf-8")
print(sorted(collections.Counter(re.findall(r"\\[A-Za-z]+", text)).items()))
