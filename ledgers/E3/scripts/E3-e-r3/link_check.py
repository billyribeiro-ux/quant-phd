import re, os, html
base = "course/modules/E/E3"
src = open(os.path.join(base, "project.html"), encoding="utf-8").read()
ids_here = set(re.findall(r'\sid="([^"]+)"', src))
hrefs = re.findall(r'(?:href|src)="([^"]+)"', src)
probs = []
for h in hrefs:
    h2 = html.unescape(h)
    if h2.startswith(("http://", "https://", "mailto:")):
        probs.append(("EXTERNAL", h2)); continue
    if h2.startswith("#"):
        if h2[1:] not in ids_here: probs.append(("MISSING ANCHOR", h2))
        continue
    path, _, frag = h2.partition("#")
    full = os.path.normpath(os.path.join(base, path))
    if not os.path.exists(full):
        probs.append(("MISSING FILE", h2)); continue
    if frag and full.endswith(".html"):
        other = open(full, encoding="utf-8").read()
        if frag not in set(re.findall(r'\sid="([^"]+)"', other)):
            probs.append(("MISSING TARGET ID", h2))
print("project.html href/src:", len(hrefs), "problems:", probs)
# concept links: data-concept on <a class="concept"> must point to an existing def in the named lesson
for m in re.finditer(r'<a class="concept" data-concept="([^"]+)" href="([^"]+)"', src):
    concept, href = m.group(1), m.group(2)
    path, _, frag = href.partition("#")
    full = os.path.normpath(os.path.join(base, path))
    other = open(full, encoding="utf-8").read()
    ok = ('id="%s"' % frag) in other and ('data-concept="%s"' % concept) in other
    print("concept", concept, href, "OK" if ok else "BROKEN")
