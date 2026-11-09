"""Round-12 blind scoring aid: prints the exemplar memo text and the rubric table with the official-scoring verdict
paragraphs and the annotation asides removed, so the exemplars can be scored from the descriptors before reading the
official scores. usage: blind_exemplars.py <project.html>"""
import re
import sys
src = open(sys.argv[1], encoding="utf-8").read()
src = re.sub(r'<p class="exemplar-verdict"[^>]*>.*?</p>', "[verdict removed]", src, flags=re.S)
src = re.sub(r'<aside class="annotation".*?</aside>', "[annotation removed]", src, flags=re.S)
start = src.index('<h3 id="rubric"') if '<h3 id="rubric"' in src else src.index('id="rubric"')
end = src.index('<h3 id="exemplars"') if '<h3 id="exemplars"' in src else src.index('id="exemplars"')
print(re.sub(r"<[^>]+>", " ", src[start:end])[:6000])
ex = src.index('id="exemplar-a"')
print("=====EXEMPLAR A + B MEMO TEXT=====")
body = src[ex:src.index('<section class="rubric-self"')]
print(re.sub(r"[ \t]+", " ", re.sub(r"<[^>]+>", " ", body)))
