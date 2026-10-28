import html, re, sys
pages = {"L04": "course/modules/M/M3/L04.html", "L05": "course/modules/M/M3/L05.html", "L06": "course/modules/M/M3/L06.html"}
root = sys.argv[1]
for k, p in pages.items():
    src = open(f"{root}/{p}", encoding="utf-8").read()
    blocks = re.findall(r"<pre>(.*?)</pre>", src, re.S)
    out = open(f"/tmp/M3-v/b5/twin-{k}.out", encoding="utf-8").read()
    lines = out.rstrip("\n").split("\n")
    hits = [b for b in blocks if html.unescape(re.sub(r"<[^>]+>", "", b)).rstrip("\n") == "\n".join(lines)]
    print(k, "pre blocks:", len(blocks), "lines:", len(lines), "exact match blocks:", len(hits))
