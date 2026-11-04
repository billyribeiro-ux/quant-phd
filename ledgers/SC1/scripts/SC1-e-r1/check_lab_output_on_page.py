"""Every stdout line of each SC1 lab twin must appear in its lesson page's embedded output (visible text).
Read-only. Usage: check_lab_output_on_page.py <labs dir> <stdout dir> <module dir>
Pairs: lab-SC1-Lnn-1 -> Lnn, lab-SC1-project-k -> project (project text extracted separately).
"""
import os
import re
import sys

import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_text import page_text

labs_dir, out_dir, module_dir = sys.argv[1], sys.argv[2], sys.argv[3]
page_for = {}
for f in sorted(os.listdir(labs_dir)):
    if not f.endswith(".py"):
        continue
    stem = f[:-3]
    m = re.match(r"lab-SC1-(L\d\d)-1$", stem)
    page = m.group(1) if m else None
    if page is None and stem.startswith("lab-SC1-project"):
        page = "project"
    page_for[stem] = page
bad = 0
for stem, page in page_for.items():
    if page == "project":
        continue
    text = page_text(f"{module_dir}/{page}.html")
    text = re.sub(r"\s+", " ", text)
    lines = [ln.strip() for ln in open(f"{out_dir}/{stem}.stdout", encoding="utf-8") if ln.strip()]
    missing = [ln for ln in lines if re.sub(r"\s+", " ", ln) not in text]
    print(f"{stem} ({page}): {len(lines)} output lines, {len(missing)} not found on the page text")
    for ln in missing[:5]:
        print("   NOT ON PAGE:", ln[:140])
    bad += len(missing)
print("total output lines not on page:", bad)
