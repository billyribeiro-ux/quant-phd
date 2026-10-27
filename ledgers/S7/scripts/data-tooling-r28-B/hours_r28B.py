"""Round 28: S7 hours split. Lesson study hours from each lesson's <html data-hours>, the hub's data-hours-lessons and
data-hours-project, and the curriculum module hours in curriculum/curriculum.json (no rendering)."""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
total = 0.0
for n in range(1, 9):
    html = (root / f"course/modules/S/S7/L{n:02d}.html").read_text(encoding="utf-8")
    m = re.search(r'<html[^>]*\bdata-hours="([^"]+)"', html)
    h = float(m.group(1))
    total += h
    print(f"L{n:02d} data-hours {h:g}")
hub = (root / "course/modules/S/S7/index.html").read_text(encoding="utf-8")
hm = re.search(r'<main[^>]*data-hours-lessons="([^"]+)"[^>]*data-hours-project="([^"]+)"', hub)
lessons_h, project_h = float(hm.group(1)), float(hm.group(2))
cur = json.loads((root / "curriculum/curriculum.json").read_text(encoding="utf-8"))
mod = [m for p in cur["parts"] for m in p["modules"] if m["id"] == "S7"][0]
print(f"sum of lesson data-hours {total:g}; hub lessons {lessons_h:g}, hub project {project_h:g}, hub sum {lessons_h+project_h:g}; curriculum module hours {mod['hours']}")
print("project share of module hours:", f"{project_h / mod['hours']:.0%}", "(check_pages allows 10-40%)")
print("hub sums to curriculum:", abs(lessons_h + project_h - mod["hours"]) < 1e-9, "; lessons equal the lesson sum:", abs(total - lessons_h) < 1e-9)
