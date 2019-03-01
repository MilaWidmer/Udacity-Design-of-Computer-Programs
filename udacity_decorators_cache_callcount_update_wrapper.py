from functools import update_wrapper

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

callcounts = {}

@decorator
def countcalls(f):
    "Decorator that makes the function count calls to it, in callcounts[f]"
    def _f(*args):
        callcounts[_f] += 1
        return f(*args)
    callcounts[_f] = 0
    return _f

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args.
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return (cache[args])
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)
    return _f

@countcalls
@memo
def fib(n): return 1 if n <= 1 else fib(n-1) + fib(n-2)

print(fib(10))
print(callcounts)