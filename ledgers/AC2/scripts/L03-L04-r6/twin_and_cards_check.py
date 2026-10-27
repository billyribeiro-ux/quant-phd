# Round-6 checks for AC2 L03/L04: embedded data-run code equals the twin; expected block equals twin stdout;
# cards: 140 contiguous ids, changed-card list vs 11b3477, and the L03/L04 card subjects unchanged.
import html, json, re, subprocess, sys
root = sys.argv[1]
for l in ("L03", "L04"):
    src = open(f"{root}/course/modules/AC/AC2/{l}.html", encoding="utf-8").read()
    twin = open(f"{root}/tests/labs/AC2/lab-AC2-{l}-1.py", encoding="utf-8").read()
    code = [html.unescape(b) for b in re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)]
    exp = [html.unescape(b) for b in re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)]
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/AC2/lab-AC2-{l}-1.py"],
                         capture_output=True, text=True, check=True).stdout
    print(l, "code_blocks", len(code), "code_equals_twin", all(c.rstrip() == twin.rstrip() for c in code),
          "expected_equals_twin_stdout", exp[0].rstrip() == out.rstrip(), "expected_lines", len(out.splitlines()))
new = json.load(open(f"{root}/course/modules/AC/AC2/cards.json"))
old = json.load(open("/tmp/ac2-v/L03-L04/r6/cards_11b.json"))
ids = [c["id"] for c in new]
print("cards", len(new), "contiguous", ids == [f"AC2-c{i:03d}" for i in range(1, 141)], "unique_fronts",
      len({c["front"] for c in new}) == len(new), "unique_backs", len({c["back"] for c in new}) == len(new))
ob = {c["id"]: c for c in old}
print("changed_vs_11b3477", [c["id"] for c in new if ob[c["id"]] != c])
mine = [c["id"] for c in new if c["lesson"] in ("L03", "L04")]
print("L03_L04_cards", len(mine), "none_changed", not set(mine) & {c["id"] for c in new if ob[c["id"]] != c})
