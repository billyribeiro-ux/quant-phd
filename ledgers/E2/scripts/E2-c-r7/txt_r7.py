import re, sys, html
src = open(sys.argv[1], encoding="utf-8").read()
src = re.sub(r"<script.*?</script>|<style.*?</style>", "", src, flags=re.S)
src = re.sub(r"<pre><code class=\"language-python\" data-run>.*?</code></pre>", "[LAB CODE]", src, flags=re.S)
src = re.sub(r"<pre class=\"expected\".*?</pre>", "[EXPECTED]", src, flags=re.S)
src = re.sub(r"</(p|li|h[1-6]|tr|div|section|pre)>", "\n", src)
src = re.sub(r"<[^>]+>", "", src)
src = html.unescape(src)
lines = [l.strip() for l in src.splitlines()]
print("\n".join(l for l in lines if l))
