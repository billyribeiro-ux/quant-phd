import re, sys
src_path, dst_path = sys.argv[1], sys.argv[2]
src = open(src_path, encoding="utf-8").read()
def fix(m):
    return m.group(0).replace("<", "&lt;")
out = re.sub(r"\\\((?:.*?)\\\)|\\\[(?:.*?)\\\]", fix, src, flags=re.S)
open(dst_path, "w", encoding="utf-8").write(out)
