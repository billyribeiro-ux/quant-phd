"""Compare the code and expected block of each project lab on project.html with its twin (round 6, slice e).

Usage: python -I page_code_vs_twin_r6.py <project.html> <twin dir>
"""
import html, re, subprocess, sys
src = open(sys.argv[1], encoding='utf-8').read()
twin_dir = sys.argv[2]
for n in (1, 2, 3):
    start = src.index(f'id="lab-M2-project-{n}"')
    end = src.index('</section>', start)
    block = src[start:end]
    code = re.search(r'<pre><code[^>]*>(.*?)</code></pre>', block, re.S).group(1)
    code = html.unescape(code)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', block, re.S).group(1)
    exp = html.unescape(exp)
    twin = open(f'{twin_dir}/lab-M2-project-{n}.py', encoding='utf-8').read()
    print(f'project lab {n}: page code == twin: {code.strip() == twin.strip()} (page {len(code)} chars, twin {len(twin)} chars)')
    run = subprocess.run([sys.executable, '-I', '-W', 'error', f'{twin_dir}/lab-M2-project-{n}.py'], capture_output=True, text=True)
    print(f'  twin rc={run.returncode} stderr={run.stderr.strip()!r}')
    print(f'  expected block == twin output: {exp.strip() == run.stdout.strip()}')
    if exp.strip() != run.stdout.strip():
        import difflib
        print('\n'.join(difflib.unified_diff(exp.strip().splitlines(), run.stdout.strip().splitlines(), 'expected', 'output', lineterm='')))
