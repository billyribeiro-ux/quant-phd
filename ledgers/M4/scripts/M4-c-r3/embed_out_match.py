import sys, html
# usage: embed_out_match.py <page.txt (page_text3 output)> <twin_output.txt>
page = open(sys.argv[1], encoding="utf-8").read()
out = open(sys.argv[2], encoding="utf-8").read().splitlines()
missing = [l for l in out if l.strip() and l not in page]
print(f"lines={len([l for l in out if l.strip()])} missing_from_page={len(missing)}")
for l in missing:
    print("MISSING:", l)
