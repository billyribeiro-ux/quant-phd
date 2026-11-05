"""Print the data-run code block of a BK4 lesson page, HTML-unescaped: page_code.py PAGE.html"""
import html
import re
import sys

text = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
sys.stdout.write(html.unescape(m.group(1)))
