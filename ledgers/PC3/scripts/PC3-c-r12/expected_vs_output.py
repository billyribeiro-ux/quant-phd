import html, re, sys
root, d = sys.argv[1], sys.argv[2]
page = open(f"{root}/course/modules/PC/PC3/project.html", encoding="utf-8").read()
for n in (1, 2, 3):
    sec = re.search(rf'<section[^>]*id="lab-PC3-project-{n}".*?</section>', page, re.S).group(0)
    pres = re.findall(r"<pre([^>]*)>(.*?)</pre>", sec, re.S)
    for attrs, body in pres[1:]:
        text = html.unescape(re.sub(r"<[^>]+>", "", body)).strip()
        out = open(f"{d}/twin_project_{n}.stdout", encoding="utf-8").read().strip()
        print(f"lab {n} pre attrs={attrs.strip()[:60]!r} equals twin stdout: {text == out}")
        if text != out:
            tl, ol = text.splitlines(), out.splitlines()
            for i, (a, b) in enumerate(zip(tl, ol)):
                if a != b:
                    print("  first diff line", i, "page:", a[:120], "| twin:", b[:120]); break
            print("  page lines", len(tl), "twin lines", len(ol))
