import html, re, sys
# Usage: extract_check.py <lesson.html> <twin.py> <out_prefix>
# Writes <out_prefix>.code.py (page code, unescaped) and <out_prefix>.expected.txt (expected block, unescaped).
lesson, twin, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
src = open(lesson, encoding="utf-8").read()
m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
code = html.unescape(m.group(1))
e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
expected = html.unescape(re.sub(r"<[^>]+>", "", e.group(1)))
open(prefix + ".code.py", "w", encoding="utf-8").write(code)
open(prefix + ".expected.txt", "w", encoding="utf-8").write(expected)
tw = open(twin, encoding="utf-8").read()
print("page_code_equals_twin:", code.strip() == tw.strip(), "page_code_lines:", len(code.splitlines()), "twin_lines:", len(tw.splitlines()))
