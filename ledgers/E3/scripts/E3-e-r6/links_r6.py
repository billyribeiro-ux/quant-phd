# Checks every href and src of the E3 project and hub pages: file exists; fragment exists as an id in the target file.
import os, re
root = "/Users/billyribeiro/.fanout/wt/verifyD6-E3-e/course/modules/E/E3"
ids_cache = {}
def ids(path):
    if path not in ids_cache:
        txt = open(path, encoding="utf-8").read()
        ids_cache[path] = set(re.findall(r'\bid="([^"]+)"', txt)) | set(re.findall(r'<dfn[^>]*\bid="([^"]+)"', txt))
    return ids_cache[path]
bad = 0
for page in ("project.html", "index.html"):
    src = os.path.join(root, page)
    txt = open(src, encoding="utf-8").read()
    links = re.findall(r'(?:href|src)="([^"]+)"', txt)
    n = 0
    for link in links:
        if link.startswith(("http://", "https://", "mailto:", "data:")):
            continue
        n += 1
        file_part, _, frag = link.partition("#")
        target = src if file_part == "" else os.path.normpath(os.path.join(os.path.dirname(src), file_part))
        if not os.path.exists(target):
            print("MISSING FILE", page, link); bad += 1; continue
        if frag:
            if target.endswith(".html") and frag not in ids(target):
                print("MISSING FRAGMENT", page, link); bad += 1
    print(page, "local links", n)
print("bad", bad)
