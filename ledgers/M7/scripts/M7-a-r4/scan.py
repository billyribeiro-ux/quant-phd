import re,html,sys
base='/tmp/verifyB4-M7-a/course/modules/M/M7/'
files=['index.html','L01.html','L02.html','L03.html']
banned=['roughly','about ','historically','typically','usually','generally','often','mostly','...','…','TODO','TBD','lorem','for brevity','details omitted','beyond the scope','left as an exercise','you can add more','it is important to note','studies show','experts agree','it is well known','obviously','clearly','half']
process=['builder','verifier','verif','round','REQUEST','unit report','fanout','audit','build ']
scope=[r'\bonly\b',r'\ball\b',r'\balways\b',r'\bevery\b',r'\bany\b',r'\bsame\b',r'\bdrives\b',r'\boffsets\b',r'\braises\b',r'\bas much as\b']
closure=['covariance','efficient frontier','dynamic programming','contraction','newton','convexity','correlation','multivariate','value function','expected return','variance','Bellman','envelope']
for f in files:
    raw=open(base+f,encoding='utf-8').read()
    # drop script/style, keep text
    t=re.sub(r'<script.*?</script>|<style.*?</style>','',raw,flags=re.S)
    t=re.sub(r'<pre.*?</pre>','',t,flags=re.S)  # code/expected blocks handled separately
    t=html.unescape(re.sub(r'<[^>]+>',' ',t))
    t=re.sub(r'\s+',' ',t)
    print('==',f,len(t))
    for group,name in ((banned,'BANNED'),(process,'PROCESS')):
        for w in group:
            for m in re.finditer(re.escape(w),t,flags=re.I):
                print(name,repr(w),'::',t[max(0,m.start()-70):m.end()+40])
    for w in scope:
        for m in re.finditer(w,t,flags=re.I):
            print('SCOPE',w,'::',t[max(0,m.start()-60):m.end()+40])
    for w in closure:
        for m in re.finditer(re.escape(w),t,flags=re.I):
            print('CLOSURE',w,'::',t[max(0,m.start()-50):m.end()+30])
