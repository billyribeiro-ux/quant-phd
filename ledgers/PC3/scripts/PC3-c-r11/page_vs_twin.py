import html, re, sys
root = sys.argv[1]
page = open(f"{root}/course/modules/PC/PC3/project.html", encoding="utf-8").read()
for n in (1, 2, 3):
    m = re.search(rf'<section[^>]*id="lab-PC3-project-{n}".*?</section>', page, re.S)
    sec = m.group(0)
    pres = re.findall(r"<pre[^>]*>(.*?)</pre>", sec, re.S)
    code = html.unescape(re.sub(r"<[^>]+>", "", pres[0]))
    twin = open(f"{root}/tests/labs/PC3/lab-PC3-project-{n}.py", encoding="utf-8").read()
    cl = [l.rstrip() for l in code.strip().splitlines()]
    tl = [l.rstrip() for l in twin.strip().splitlines()]
    same = cl == tl
    blanks = [i for i, l in enumerate(cl) if "___" in l]
    diff_lines = [(i, a, b) for i, (a, b) in enumerate(zip(cl, tl)) if a != b and "___" not in a]
    print(f"lab {n}: page code lines {len(cl)} twin lines {len(tl)} identical={same} blank-lines={len(blanks)} non-blank mismatches={len(diff_lines)} {diff_lines[:3]}")
    outs = re.findall(r'<pre[^>]*class="[^"]*(?:output|expected)[^"]*"[^>]*>(.*?)</pre>', sec, re.S)
    print(f"  expected blocks found: {len(outs)}")
