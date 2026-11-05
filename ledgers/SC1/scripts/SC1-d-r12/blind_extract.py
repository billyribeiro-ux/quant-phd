import re, sys, html
src = open(sys.argv[1], encoding="utf-8").read()
start = src.index('<article class="exemplar" id="exemplar-a"')
end = src.index('<section class="rubric-self"')
body = src[start:end]
body = re.sub(r'<aside class="annotation".*?</aside>', '', body, flags=re.S)
body = re.sub(r'<p class="exemplar-verdict".*?</p>', '', body, flags=re.S)
body = re.sub(r'<article class="exemplar" id="(exemplar-[ab])"[^>]*>', r'\n=== \1 ===', body)
body = re.sub(r'<(/?)(p|h[45]|h5|li|ol|ul|div|article)[^>]*>', lambda m: '\n' if m.group(2) in ('p','h5','h4','li') else '', body)
body = re.sub(r'<[^>]+>', '', body)
print(html.unescape(re.sub(r'\n\s*\n+', '\n', body)))
