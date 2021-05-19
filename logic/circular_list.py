from random import choice


class Node:
    """Node with two pointers and a data variable"""
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


class DirectionCircle:
    """Circular list containing for directions: U, R, D, L.
    Get a random direction with random_direction() method.
    Move across directions using .right and .left properties."""
    u = Node('U')  # ri = r, le = l
    r = Node('R', left=u)  # ri = d
    d = Node('D', left=r)  # ri =
    l = Node('L', right=u, left=d)

    u.right = r
    u.left = l
    r.right = d
    d.right = l

    @classmethod
    def random_direction(cls):
        return choice((cls.l, cls.r, cls.u, cls.d))

# cur = u
# print(cur.data)
# while True:
#     c = input(':>')
#     if c == 'd':
#         cur = cur.right
#         print(cur.data)
#     elif c == 'a':
#         cur = cur.left
#         print(cur.data)
#     else:
#         break
