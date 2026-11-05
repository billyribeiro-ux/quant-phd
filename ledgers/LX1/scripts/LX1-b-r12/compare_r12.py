"""LX1-b round 12: page data-run code equals the twin source; expected block equals the twin's stdout (line for line)."""
import html
import re
import sys

root = sys.argv[1]
out = f"{root}/ledgers/LX1/scripts/LX1-b-r12/out"
ok = True
for page, twin in (("L03", "lab-LX1-L03-1"), ("L04", "lab-LX1-L04-1")):
    text = open(f"{root}/course/modules/LX/LX1/{page}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    src = open(f"{root}/tests/labs/LX1/{twin}.py", encoding="utf-8").read()
    same = code.rstrip(chr(10)) == src.rstrip(chr(10))
    print(page, "data-run code equals twin source:", same, "| page lines", code.count("\n"), "twin lines", src.count("\n"),
          "| page block at line", text[: m.start()].count("\n") + 1, "to", text[: m.end()].count("\n") + 1)
    ok &= same
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1))
    stdout = open(f"{out}/twin_{page}.out", encoding="utf-8").read()
    eq = expected.rstrip("\n") == stdout.rstrip("\n")
    print(page, "expected block equals twin stdout:", eq, "| expected lines", len(expected.splitlines()),
          "| block at line", text[: e.start()].count("\n") + 1, "to", text[: e.end()].count("\n") + 1)
    if not eq:
        import difflib
        print("\n".join(difflib.unified_diff(stdout.splitlines(), expected.splitlines(), lineterm="")))
    ok &= eq
print("ALL EQUAL:", ok)
