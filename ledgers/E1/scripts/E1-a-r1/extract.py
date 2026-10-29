import html, re, sys
src = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
exp = html.unescape(m.group(1))
act = open(sys.argv[2], encoding="utf-8").read()
print("MATCH" if exp.strip() == act.strip() else "DIFF")
if exp.strip() != act.strip():
    import difflib
    print("\n".join(difflib.unified_diff(exp.splitlines(), act.splitlines(), lineterm="")))
