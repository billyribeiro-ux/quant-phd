"""Resolve every internal href with a fragment in the slice pages against the target file's ids.

usage: python3 -I links_r10.py <course-root> <page> [<page> ...]   (pages relative to course-root's module dir)
"""
import os
import re
import sys

root = sys.argv[1]
for page in sys.argv[2:]:
    src_path = os.path.join(root, page)
    html = open(src_path, encoding="utf-8").read()
    ids_cache: dict[str, set[str]] = {}
    bad = 0
    total = 0
    for href in re.findall(r'href="([^"]+)"', html):
        if "#" not in href or href.startswith("http"):
            continue
        target, frag = href.split("#", 1)
        tpath = os.path.normpath(os.path.join(os.path.dirname(src_path), target)) if target else src_path
        if not os.path.exists(tpath):
            print(f"MISSING FILE {page}: {href}")
            bad += 1
            total += 1
            continue
        if tpath not in ids_cache:
            t = open(tpath, encoding="utf-8").read()
            ids_cache[tpath] = set(re.findall(r'\bid="([^"]+)"', t))
        total += 1
        if frag not in ids_cache[tpath]:
            print(f"UNRESOLVED {page}: {href}")
            bad += 1
    print(f"{page}: {total} fragment links, {bad} unresolved")
