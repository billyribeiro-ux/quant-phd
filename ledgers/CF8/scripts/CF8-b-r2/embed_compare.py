import re, html, subprocess, sys
root = sys.argv[1]
for L, f in [('L03', 'lab-CF8-L03-1'), ('L04', 'lab-CF8-L04-1'), ('L05', 'lab-CF8-L05-1')]:
    page = open(f'{root}/course/modules/CF/CF8/{L}.html', encoding='utf-8').read()
    blocks = re.findall(r'<pre[^>]*>(.*?)</pre>', page, re.S)
    out = subprocess.run([f'{root}/.venv/bin/python', '-I', '-W', 'error', f'{root}/tests/labs/CF8/{f}.py'],
                         capture_output=True, text=True).stdout
    cands = [html.unescape(re.sub(r'<[^>]+>', '', x)).strip() for x in blocks]
    print(L, 'exact match of live run output in a <pre> block:', any(c == out.strip() for c in cands))
