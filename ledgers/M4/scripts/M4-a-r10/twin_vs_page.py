# Round 10: compare each slice lab page's code block and expected block with its twin and with twin stdout.
import html, re, sys
from pathlib import Path
ROOT = Path(sys.argv[1])
out_dir = Path(sys.argv[2])
for n in (1, 2, 3, 4):
    page = (ROOT / f"course/modules/M/M4/L0{n}.html").read_text(encoding="utf-8")
    twin = (ROOT / f"tests/labs/M4/lab-M4-L0{n}-1.py").read_text(encoding="utf-8")
    m_code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    m_exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(m_code.group(1)) if m_code else None
    exp = html.unescape(m_exp.group(1)) if m_exp else None
    stdout = (out_dir / f"out_L0{n}.txt").read_text(encoding="utf-8")
    print(f"L0{n}: page_code_blocks={len(re.findall(r'data-run', page))} expected_blocks={len(re.findall('class=\"expected\"', page))}")
    print(f"  page code.rstrip(chr(10)) == twin.rstrip(chr(10)): {code.rstrip(chr(10)) == twin.rstrip(chr(10))} (len page {len(code or '')}, twin {len(twin)})")
    print(f"  expected == stdout: {exp.rstrip(chr(10)) == stdout.rstrip(chr(10))} (len exp {len(exp or '')}, stdout {len(stdout)})")
    if code != twin:
        import difflib
        for line in list(difflib.unified_diff(twin.splitlines(), (code or '').splitlines(), 'twin', 'page', lineterm=''))[:20]:
            print('   ', line)
    if exp != stdout:
        import difflib
        for line in list(difflib.unified_diff(stdout.splitlines(), (exp or '').splitlines(), 'stdout', 'expected', lineterm=''))[:20]:
            print('   ', line)
