# Blind extraction: exemplar essay text only. Strips data-scores, data-level, verdict paragraphs, annotations.
import re, sys
src = open(sys.argv[1], encoding='utf-8').read().split('\n')
# keep only lines 489..617 (1-indexed) = exemplar section
seg = '\n'.join(src[488:617])
seg = re.sub(r'<aside.*?</aside>', '', seg, flags=re.S)
seg = re.sub(r'<p class="exemplar-verdict".*?</p>', '', seg, flags=re.S)
seg = re.sub(r'\s*data-(scores|level|label)="[^"]*"', '', seg)
seg = re.sub(r'<[^>]+>', ' ', seg)
seg = re.sub(r'[ \t]+', ' ', seg)
seg = re.sub(r'\n\s*\n+', '\n', seg)
print(seg)
