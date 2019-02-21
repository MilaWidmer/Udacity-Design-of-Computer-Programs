import itertools, re, time
import cProfile


def faster_solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None.
    This version precompiles the formula; only one eval per formula."""
    f, letters = compile_formula(formula)
    for digits in itertools.permutations((1,2,3,4,5,6,7,8,9,0), len(letters)):
        try:
            if f(*digits) is True:
                table = str.maketrans(letters, ''.join(map(str, digits)))
                return formula.translate(table)
        except ArithmeticError:
            pass

def compile_formula(formula, verbose=False):
    """Compile formula into a function. Also return letters found, as a str,
    in same order as parms of function. For example, 'YOU == ME**2' returns
    (lambda Y, M, E, U, O: (U+10*O+100*Y) == (E+10*M)**2), 'YMEUO'"""
    letters = ''.join(set(re.findall('[A-Z]', formula)))
    print(letters)
    parms = ', '.join(letters)
    print(parms)
    tokens = map(compile_word, re.split('([A-Z]+)', formula))
    print(tokens)
    body = ''.join(tokens)
    print(body)
    f = 'lambda %s: %s' % (parms, body)
    print(f)
    if verbose: print(f)
    return eval(f), letters


def compile_word(word):
    """Compile a word of uppercase letters as numeric digits.
    E.g., eompile_word('YOU') => '(1*U+10*0+100*Y)'
    Non-uppercase words unchanged: compile_word('+') => '+'"""
    if word.isupper():
        terms = [('%s*%s' % (10**i, d))
                 for (i, d) in enumerate(word[::-1])]
        return '(' + '+'.join(terms) + ')'
    else:
        return word


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
        print('%6.4f sec:   %s \n' % timedcall(faster_solve, example))
    print(time.perf_counter()-t0)

def timedcall(fn, *args):
    "Call function and return elapsed time."
    t0 = time.perf_counter()
    result = fn(*args)
    t1 = time.perf_counter()
    return t1-t0, result

cProfile.run('test()')