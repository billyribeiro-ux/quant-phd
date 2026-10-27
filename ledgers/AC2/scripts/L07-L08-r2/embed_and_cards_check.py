"""Round-2 checks: (a) embedded lab code and expected blocks equal the twins and twin stdout;
(b) internal links on L07/L08 resolve; (c) near-duplicate scan over cards.json.
Run: python3 -I embed_and_cards_check.py <checkout>"""
import difflib, html, itertools, json, os, re, subprocess, sys
root = sys.argv[1]
py = os.path.join(root, ".venv", "bin", "python")
for name, twin in [("L07", "tests/labs/AC2/lab-AC2-L07-1.py"), ("L08", "tests/labs/AC2/lab-AC2-L08-1.py")]:
    page = os.path.join(root, "course/modules/AC/AC2", f"{name}.html")
    t = open(page, encoding="utf-8").read()
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', t, re.S).group(1))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', t, re.S).group(1)).strip()
    tw_path = os.path.join(root, twin)
    out = subprocess.run([py, "-I", "-W", "error", tw_path], capture_output=True, text=True, cwd=root).stdout.strip()
    print(f"{name}: embedded code == twin: {code.strip() == open(tw_path, encoding='utf-8').read().strip()}; expected == twin stdout: {exp == out}")
    base = os.path.dirname(page)
    for href in sorted(set(re.findall(r'href="([^"]+)"', t))):
        if href.startswith(("http", "#", "mailto")):
            continue
        path, _, frag = href.partition("#")
        target = os.path.normpath(os.path.join(base, path)) if path else page
        ok = os.path.exists(target)
        fok = (f'id="{frag}"' in open(target, encoding="utf-8").read()) if (ok and frag) else True
        if not (ok and fok):
            print(f"  BROKEN {name} {href}")
    print(f"  {name}: all internal hrefs checked")
cards = json.load(open(os.path.join(root, "course/modules/AC/AC2/cards.json"), encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique:", len(set(ids)), "sequential:", ids == [f"AC2-c{i:03d}" for i in range(1, len(ids) + 1)])
pairs = []
for a, b in itertools.combinations(cards, 2):
    r = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
    rb = difflib.SequenceMatcher(None, a["back"].lower(), b["back"].lower()).ratio()
    if r > 0.6 or rb > 0.6:
        pairs.append((round(r, 2), round(rb, 2), a["id"], b["id"]))
print("pairs with front or back similarity > 0.6:", len(pairs))
for p in sorted(pairs, reverse=True):
    print("  ", p)
