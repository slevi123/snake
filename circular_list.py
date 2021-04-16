class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


u = Node('U') # ri = r, le = l
r = Node('R', left=u) # ri = d
d = Node('D', left=r) # ri = 
l = Node('L', right=u, left=d)

u.right = r
u.left = l
r.right= d
d.right = l

cur = u
print(cur.data)
while True:
    c = input(':>')
    if c == 'd':
        cur = cur.right
        print(cur.data)
    elif c == 'a':
        cur = cur.left
        print(cur.data)
    else:
        break
