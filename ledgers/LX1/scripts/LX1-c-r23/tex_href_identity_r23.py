"""Round 23 (LX1-c): compares the TeX spans and the href/id attributes of project.html at the current checkout with
the pin 6d22ff56 (git show). Usage: python -I tex_href_identity_r23.py <repo_root>"""
import re
import subprocess
import sys

root = sys.argv[1]
cur = open(f"{root}/course/modules/LX/LX1/project.html", encoding="utf-8").read()
old = subprocess.run(["git", "-C", root, "show", "6d22ff56:course/modules/LX/LX1/project.html"], capture_output=True, text=True, check=True).stdout
tex = lambda t: re.findall(r"\\\((.*?)\\\)", t, re.S)
attr = lambda t: re.findall(r'(?:href|id)="[^"]*"', t)
print("TeX spans: current", len(tex(cur)), "pin", len(tex(old)), "identical" if tex(cur) == tex(old) else "DIFFERENT")
print("href/id attributes: current", len(attr(cur)), "pin", len(attr(old)), "identical" if attr(cur) == attr(old) else "DIFFERENT")
print("line 473 contains TeX or href/id:", bool(re.search(r"\\\(|href=|id=", cur.splitlines()[472].split("<td>")[0])))
