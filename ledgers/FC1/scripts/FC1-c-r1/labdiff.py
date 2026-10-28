import re, html, pathlib, subprocess, sys
root = pathlib.Path('/tmp/verifyC1-FC1-c')
page = (root/'course/modules/FC/FC1/project.html').read_text()
sections = re.findall(r'<section class="lab[^"]*" id="(lab-FC1-project-\d)".*?<pre><code[^>]*>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
for lab_id, code, expected in sections:
    code = html.unescape(code); expected = html.unescape(expected)
    twin = (root/f'tests/labs/FC1/{lab_id}.py').read_text()
    same = code.rstrip() == twin.rstrip()
    out = subprocess.run([str(root/'.venv/bin/python'), '-I', '-W', 'error', str(root/f'tests/labs/FC1/{lab_id}.py')], capture_output=True, text=True).stdout
    print(lab_id, 'page code == twin:', same, '| expected == run output:', expected.strip() == out.strip(), '| lines', len(out.splitlines()))
    if not same:
        import difflib
        print(''.join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), 'twin', 'page'))[:40]))
