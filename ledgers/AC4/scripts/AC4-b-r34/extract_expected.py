"""Extract the data-run and expected blocks of a lab from a course page, for comparison with a live run."""
import html
import re
import sys

page, out_expected = sys.argv[1], sys.argv[2]
text = open(page, encoding="utf-8").read()
m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
exp = html.unescape(m.group(1))
open(out_expected, "w", encoding="utf-8").write(exp)
code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
open(out_expected + ".code.py", "w", encoding="utf-8").write(html.unescape(code.group(1)))
print("expected lines:", exp.count("\n"), "code lines:", html.unescape(code.group(1)).count("\n"))
