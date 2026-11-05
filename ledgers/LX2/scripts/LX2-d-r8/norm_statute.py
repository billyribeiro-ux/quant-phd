import re, sys
src = sys.argv[1]
text = open(src, encoding='utf-8', errors='replace').read()
# strip page-layout hyphenation at line ends: "re-\n   fusing" -> "refusing"
text = re.sub(r'-\n\s+', '', text)
text = re.sub(r'\s+', ' ', text)
text = text.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
text = text.replace("''", '"')
sys.stdout.write(text)
