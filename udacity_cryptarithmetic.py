import itertools, re, time
import cProfile


def solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None."""
    for f in fill_in(formula):
        if valid(f):
            return(f)

def fill_in(formula):
    "Generate all possible fillings-in of letters in formula with digits."
    letters = ''.join(set(re.findall('[A-Z]', formula)))
    for digits in itertools.permutations('1234567890', len(letters)):
        table = str.maketrans(letters, ''.join(digits))
        yield formula.translate(table)

def valid(f):
    "Formula f is valid of it has no numbers with leading zero, and evals true"
    try:
        return not re.search(r'\b0[0-9]', f) and eval(f) is True
    except ArithmeticError:
        return False


# T E S T I N G

examples = """TWO + TWO == FOUR
A**2 + B**2 == C**2
A**2 + BE**2 == BY**2
X / X == X
A**N + B**N == C**N and N > 1
ATOM**0.5 == A + TO + M
GLITTERS is not GOLD
ONE < TWO and FOUR < FIVE
ONE < TWO < THREE 
sum(range(AA)) == BB
sum(range(POP)) == BOBO
ODD + ODD == EVEN
PLUTO not in set([PLANETS])""".splitlines()

def test():
    t0 = time.perf_counter()
    for example in examples:
        print(13*' ', example)
        print('%6.4f sec:   %s \n' % timedcall(solve, example))
    print(time.perf_counter()-t0)

def timedcall(fn, *args):
    "Call function and return elapsed time."
    t0 = time.perf_counter()
    result = fn(*args)
    t1 = time.perf_counter()
    return t1-t0, result

cProfile.run('test()')