def n_ary(f):
    """Given binary function f(x,y), return an n_ary function such that
    f(x, y, z) = f(x, f(y, z)), etc. Also allow f(x) = x."""
    def n_ary_f(x, *args):
        return x if not args else f(x, n_ary_f(*args))
    return n_ary_f

@n_ary # is the same as: seq = n_ary(seq)
def seq(x, y): return ('seq', x, y)

print (seq(1,2,3,4))
print (seq(1))
