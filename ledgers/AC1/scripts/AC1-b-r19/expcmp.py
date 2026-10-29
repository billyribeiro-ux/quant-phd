import re, subprocess, sys, html
for t in ('L04','L05','L06'):
    page = open(f'course/modules/AC/AC1/{t}.html').read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    exp = html.unescape(m.group(1)).strip().splitlines()
    out = subprocess.run([sys.executable, '-I', '-W', 'error', f'tests/labs/AC1/lab-AC1-{t}-1.py'], capture_output=True, text=True).stdout.strip().splitlines()
    print(t, 'expected lines', len(exp), 'twin lines', len(out), 'IDENTICAL' if exp == out else 'DIFF')
