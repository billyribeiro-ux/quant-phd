#!/bin/sh
# Round 8 M5-b extra checks, run from checkout at pin ce7b382
cd /Users/billyribeiro/.fanout/wt/verifyB8-M5-b
echo "== pytest M5-scoped lab tests"; .venv/bin/pytest -q tests/test_labs.py -k M5 2>&1 | tail -1
echo "== pytest runner and page tests"; .venv/bin/pytest -q tests/test_run_labs.py tests/test_page_checks.py 2>&1 | tail -1
echo "== pytest full test_labs (out-of-slice E3 twins absent in checkout)"; .venv/bin/pytest -q tests/test_labs.py 2>&1 | tail -1
echo "== verify_refs offline"; .venv/bin/python tools/verify_refs.py --offline 2>&1 | tail -1
echo "== build_site --check"; .venv/bin/python tools/build_site.py --check 2>&1 | tail -1
echo "== render_curriculum then git diff (generated files)"; .venv/bin/python tools/render_curriculum.py >/dev/null 2>&1; git diff --stat -- CURRICULUM.md curriculum/curriculum.json | tail -1; echo "diff_rc=$?"
echo "== twin vs page code (ignoring final newline)"
for t in L05 L06 L07; do .venv/bin/python -I -c "
import html,re
src=open('course/modules/M/M5/$t.html',encoding='utf-8').read()
m=re.search(r'<pre><code class=\"language-python\" data-run>(.*?)</code></pre>', src, re.S)
tw=open('tests/labs/M5/lab-M5-$t-1.py',encoding='utf-8').read()
print('$t equal', html.unescape(m.group(1)).rstrip('\n')==tw.rstrip('\n'))"; done
echo "== notation macro usage"; grep -c 'mathbb{R}\|mathbb{N}' course/modules/M/M5/L06.html course/modules/M/M5/L07.html
echo "== B(S) / B(N) citations"; grep -n 'which is \\(B(S)\\)\|B(S)\\) of L04' course/modules/M/M5/L06.html | cut -c1-80
echo "== L07 references claim and Corollary 3.2 proof block"; grep -n 'Each theorem, lemma, proposition and corollary is proved' course/modules/M/M5/L07.html | cut -c1-60; awk 'NR>=175 && NR<=177' course/modules/M/M5/L07.html | grep -c 'Proof'
