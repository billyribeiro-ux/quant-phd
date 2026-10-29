# Does the page's R2 solution's unexhibited subtree exist, and does an explicit 7-node height-4 AVL tree exist?
# tree as nested tuples (key, left, right); height/balance computed independently
def h(t): return 0 if t is None else 1+max(h(t[1]),h(t[2]))
def ok(t):
    if t is None: return True
    return abs(h(t[1])-h(t[2]))<=1 and ok(t[1]) and ok(t[2])
def size(t): return 0 if t is None else 1+size(t[1])+size(t[2])
def keys(t): return [] if t is None else keys(t[1])+[t[0]]+keys(t[2])
leaf=lambda k:(k,None,None)
t3_4=(2,(1,None,None),(3,None,None))  # placeholder, fixed below
t4=(3,(1,None,(2,None,None)),None)    # 2-node height-2 tree
sub_h3_4=(3,(2,(1,None,None),None),(4,None,None))  # height 3, 4 nodes
print("sub h3 4 nodes: height",h(sub_h3_4),"size",size(sub_h3_4),"AVL",ok(sub_h3_4))
sub_h2_2=(1,None,(2,None,None))
print("sub h2 2 nodes: height",h(sub_h2_2),"size",size(sub_h2_2),"AVL",ok(sub_h2_2))
root=(5,sub_h3_4,sub_h2_2)
# keys must be BST: shift
def shift(t,d): return None if t is None else (t[0]+d,shift(t[1],d),shift(t[2],d))
root=(10,shift(sub_h3_4,0),shift(sub_h2_2,0))
print("root keys", keys(root))
print("7-node tree height",h(root),"size",size(root),"AVL",ok(root))
