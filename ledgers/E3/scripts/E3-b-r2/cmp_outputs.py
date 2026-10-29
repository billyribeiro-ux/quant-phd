import sys, re, html
page, run = sys.argv[1], sys.argv[2]
src = open(page, encoding='utf-8').read()
m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
exp = html.unescape(re.sub(r'<[^>]+>', '', m.group(1)))
got = open(run, encoding='utf-8').read()
print("embedded lines:", len(exp.strip().splitlines()), "run lines:", len(got.strip().splitlines()))
print("identical after strip:", exp.strip() == got.strip())
if exp.strip() != got.strip():
    import difflib
    for l in difflib.unified_diff(exp.strip().splitlines(), got.strip().splitlines(), lineterm=''):
        print(l[:300])
