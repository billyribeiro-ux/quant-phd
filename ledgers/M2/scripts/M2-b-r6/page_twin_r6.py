# Round-6: for each M2 lab L07-L12, compare the page's data-run code block with the twin file (trailing newline ignored),
# and the page's expected block with the twin's stdout from the isolated run.
import html, re, sys, pathlib
root = pathlib.Path(sys.argv[1])
for n in ["L07", "L08", "L09", "L10", "L11", "L12"]:
    page = (root / f"course/modules/M/M2/{n}.html").read_text(encoding="utf-8")
    twin = (root / f"tests/labs/M2/lab-M2-{n}-1.py").read_text(encoding="utf-8")
    out = (root / f"ledgers/M2/scripts/M2-b-r6/twin_{n}.stdout").read_text(encoding="utf-8")
    codes = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    exps = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code_ok = [html.unescape(c).rstrip("\n") == twin.rstrip("\n") for c in codes]
    exp_ok = [html.unescape(e).rstrip("\n") == out.rstrip("\n") for e in exps]
    print(n, "code blocks", len(codes), "equal to twin", code_ok, "| expected blocks", len(exps), "equal to fresh stdout", exp_ok)
