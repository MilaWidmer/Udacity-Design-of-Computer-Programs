from functools import update_wrapper

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator # is the same as: n_ary = update_wrap(n_ary)
def n_ary(f):
    """Given binary function f(x,y), return an n_ary function such that
    f(x, y, z) = f(x, f(y, z)), etc. Also allow f(x) = x."""
    def n_ary_f(x, *args):
        return x if not args else f(x, n_ary_f(*args))
    return n_ary_f

@n_ary # is the same as: seq = n_ary(seq)
def seq(x, y): return ('seq', x, y)

print (help(seq))
print (help(n_ary))
