def hilo(a, b, c):
    if c < b: b, c = c, b
    if b < a: a, b = b, a
    if c < b: b, c = c, b
    return a + c

def complementary_color(r, g, b):
    k = hilo(r, g, b)
    return tuple(k - u for u in (r, g, b))

def rgb2hex(r, g, b):
    return "#{0:02x}{1:02x}{2:02x}".format(r, g, b)