"""Exact comparison of each slice page's run code block and expected output block against its twin and a real run.

Usage: python -I exact_blocks.py <page.html> <twin.py> <run_output.txt>
"""

from __future__ import annotations

import html
import re
import sys

page = open(sys.argv[1], encoding="utf-8").read()
code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
code_text = html.unescape(code.group(1)).rstrip("\n")
exp_text = html.unescape(expected.group(1)).rstrip("\n")
twin = open(sys.argv[2], encoding="utf-8").read().rstrip("\n")
run = open(sys.argv[3], encoding="utf-8").read().rstrip("\n")
print(sys.argv[1].split("/")[-1], "code==twin:", code_text == twin, "expected==run:", exp_text == run)
