import sys, html, re
src = open(sys.argv[1], encoding='utf-8').read()
src = re.sub(r'(?is)<(script|style)\b.*?</\1>', '', src)
src = re.sub(r'(?i)<br\s*/?>', '\n', src)
src = re.sub(r'(?i)</(p|li|h[1-6]|pre|div|tr|section|summary)>', '\n', src)
src = re.sub(r'<[^>]+>', '', src)
out = html.unescape(src)
out = re.sub(r'\n\s*\n+', '\n', out)
print(out)
