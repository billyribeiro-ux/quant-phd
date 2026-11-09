"""Verifier round 5: compare each CS2 L05-L08 page's lab code block with its twin, byte for byte.
Usage: python3 -I page_code_eq_twin_r5.py <checkout>"""
import html
import re
import sys

root = sys.argv[1]
for n in (5, 6, 7, 8):
    page = open(f"{root}/course/modules/CS/CS2/L0{n}.html", encoding="utf-8").read()
    i = page.index('data-run')
    m = re.search(r"<code[^>]*>(.*?)</code>", page[i:], re.S)
    code = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
    twin = open(f"{root}/tests/labs/CS2/lab-CS2-L0{n}-1.py", encoding="utf-8").read()
    print(f"L0{n}: code chars {len(code)} twin chars {len(twin)} identical_after_strip={code.strip() == twin.strip()}")
    if code.strip() != twin.strip():
        a, b = code.strip().splitlines(), twin.strip().splitlines()
        for k, (x, y) in enumerate(zip(a, b), 1):
            if x != y:
                print("  first diff line", k, "page:", x, "| twin:", y)
                break
        else:
            print("  length differs", len(a), len(b))
