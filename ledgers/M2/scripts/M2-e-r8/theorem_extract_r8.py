import re, html, sys
L = sys.argv[1]
t = open(f"course/modules/M/M2/{L}.html", encoding="utf-8").read()
i = t.find("Theorem 1.2 (")
j = t.find("Remark 1.3", i)
seg = html.unescape(t[i:j])
seg = re.sub(r"\s+", " ", seg)
print(L, seg[:900])
