"""Scan L07 and L08 learner prose for banned phrases, process words and data-files attributes; print every hit with its line."""
import re
import sys

root = sys.argv[1]
banned = re.compile(r"(roughly|about |historically|typically|usually|most |many |often|generally|half|several|\.\.\.|…|some |few |majority|substantial|significant|widely|studies|research shows|in general|approximately|estimate|typical)", re.I)
process = re.compile(r"\b(build|builder|built|round|verifier|verified|REQUESTS|unit report|agent|draft|TODO|placeholder)\b", re.I)
scope = re.compile(r"(\ball\b|\bevery\b|\bonly\b|\balways\b|\bnever\b|\bsame\b|\bdrives\b|\boffsets\b|\braises\b|as much as)", re.I)
for lab in ("L07", "L08"):
    text = open(f"{root}/course/modules/AC/AC4/{lab}.html", encoding="utf-8").read()
    print(lab, "data-files present:", "data-files" in text)
    in_code = False
    for i, line in enumerate(text.splitlines(), 1):
        if "<pre" in line:
            in_code = True
        if not in_code:
            for kind, pat in (("banned", banned), ("process", process), ("scope", scope)):
                for m in pat.finditer(line):
                    print(lab, i, kind, repr(m.group(0)))
        if "</pre>" in line:
            in_code = False
