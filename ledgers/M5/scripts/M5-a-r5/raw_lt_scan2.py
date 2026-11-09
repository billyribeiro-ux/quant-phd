import re, sys
# A '<letter' is a real tag only if it matches a complete start/end tag with no '<' or '>' inside its attribute part.
TAG = re.compile(r"</?[A-Za-z][A-Za-z0-9-]*(\s[^<>]*)?/?>")
for f in sys.argv[1:]:
    src = open(f, encoding="utf-8").read()
    body = re.sub(r"<!--.*?-->", "", src, flags=re.S)
    bad = []
    for m in re.finditer(r"<(?=[A-Za-z/])", body):
        if not TAG.match(body, m.start()):
            bad.append((body[:m.start()].count("\n") + 1, body[m.start():m.start()+40].replace("\n", " ")))
    print(f, "lt_letter_not_a_complete_tag:", len(bad))
    for ln, ctx in bad:
        print("   line", ln, repr(ctx))
