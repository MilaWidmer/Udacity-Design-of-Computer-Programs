from functools import update_wrapper

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args.
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return ('From cache:', cache[args])
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)
    return _f

@decorator
def n_ary(f):
    """Given binary function f(x,y), return an n_ary function such that
    f(x, y, z) = f(x, f(y, z)), etc. Also allow f(x) = x."""
    def n_ary_f(x, *args):
        return x if not args else f(x, n_ary_f(*args))
    update_wrapper(n_ary_f, f)
    return n_ary_f

@memo
@n_ary # is the same as: seq = n_ary(seq)
def seq(x, y): return ('seq', x, y)

print(seq(1,2,3,4))
print(seq(1,2,3,4))

print(help(seq))
print(help(n_ary))
print(help(memo))
