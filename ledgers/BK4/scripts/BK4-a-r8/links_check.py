"""Check every href and data-concept link in the BK4 slice pages resolves to an existing file and id."""
import os
import re
import sys

PAGES = ["course/modules/BK/BK4/index.html", "course/modules/BK/BK4/L01.html",
         "course/modules/BK/BK4/L02.html", "course/modules/BK/BK4/L03.html"]
problems = 0
count = 0
ids_cache = {}


def ids_of(path):
    if path not in ids_cache:
        text = open(path, encoding="utf-8").read()
        ids_cache[path] = set(re.findall(r'\bid="([^"]+)"', text))
    return ids_cache[path]


for page in PAGES:
    text = open(page, encoding="utf-8").read()
    base = os.path.dirname(page)
    for href in re.findall(r'href="([^"]+)"', text):
        if href.startswith(("http://", "https://", "mailto:")):
            print("EXTERNAL", page, href)
            problems += 1
            continue
        count += 1
        target, _, frag = href.partition("#")
        path = os.path.normpath(os.path.join(base, target)) if target else page
        if not os.path.exists(path):
            print("MISSING FILE", page, href)
            problems += 1
            continue
        if frag and frag not in ids_of(path):
            print("MISSING ID", page, href)
            problems += 1
print("hrefs checked", count, "problems", problems)
