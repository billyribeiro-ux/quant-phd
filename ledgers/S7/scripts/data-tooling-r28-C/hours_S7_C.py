"""Round-28 part C: hours of S7 re-summed from the repository (r25-hours-S7).
Reads curriculum/curriculum.json (unit S7), the hub's data-hours attributes and each lesson's and the project's data-hours.
Run: python -I hours_S7_C.py <checkout>"""
import json
import re
import sys
from html.parser import HTMLParser

ROOT = sys.argv[1]


class Attrs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found = []

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k.startswith("data-hours"):
                self.found.append((tag, k, v))


def hours_of(path):
    p = Attrs()
    p.feed(open(path, encoding="utf-8").read())
    return p.found


cur = json.load(open(f"{ROOT}/curriculum/curriculum.json", encoding="utf-8"))
units = [m for part in cur["parts"] for m in part["modules"]]
s7 = [{"id": u["id"], "hours": u["hours"]} for u in units if u.get("id") == "S7"]
print("curriculum S7:", s7[0] if s7 else "MISSING")
hub = hours_of(f"{ROOT}/course/modules/S/S7/index.html")
print("hub data-hours:", hub)
lessons = {}
for n in range(1, 9):
    f = f"{ROOT}/course/modules/S/S7/L{n:02d}.html"
    lessons[f"L{n:02d}"] = [v for _, k, v in hours_of(f) if k == "data-hours"]
print("lesson data-hours:", lessons)
proj = hours_of(f"{ROOT}/course/modules/S/S7/project.html")
print("project data-hours-project:", proj)
lesson_sum = sum(float(v[0]) for v in lessons.values())
hub_l = next(float(v) for _, k, v in hub if k == "data-hours-lessons")
hub_p = next(float(v) for _, k, v in hub if k == "data-hours-project")
cur_h = s7[0]["hours"]
print(f"sum lessons {lesson_sum} | hub lessons {hub_l} + hub project {hub_p} = {hub_l + hub_p} | curriculum {cur_h}")
print("hub lessons == sum of lesson data-hours:", hub_l == lesson_sum)
print("hub project == project data-hours-project:", hub_p == float(proj[0][2]))
print("hub total == curriculum hours:", hub_l + hub_p == cur_h)
print("project share %:", round(100 * hub_p / cur_h, 1))
