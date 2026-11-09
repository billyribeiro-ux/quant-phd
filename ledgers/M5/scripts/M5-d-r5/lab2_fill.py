import re,sys
src=open(sys.argv[1]).read()
src=src.replace("ratio = ___","ratio = sup_distance(bellman(v), bellman(w)) / sup_distance(v, w)").replace("certified = ___","certified = BETA / (1 - BETA) * change")
open(sys.argv[2],"w").write(src)
