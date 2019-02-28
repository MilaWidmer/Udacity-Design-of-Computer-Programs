def lit(s):
    set_s = set([s])
    return lambda Ns: set_s if len(s) in Ns else null

def oneof(chars):
    set_c = set(chars)
    #print(set_c)
    return lambda Ns: set_c if 1 in Ns else null

def alt(x, y):      return lambda Ns: x(Ns) | y(Ns)
def star(x):        return lambda Ns: opt(plus(x))(Ns)
def plus(x):        return lambda Ns: genseq(x, star(x), Ns, startx=1)
def seq(x, y):      return lambda Ns: genseq(x, y, Ns)
def opt(x):         return alt(epsilon, x)
dot = oneof('abc')
epsilon = lit('')

def genseq(x, y, Ns, startx=0):
    "Set of matches to xy whose total len is in Ns, with x-match's len in Ns_..."
    # Tricky part: x+ is defined as x+ = x x*
    # To stop the recursion, the first x must generate at least 1 char,
    # and then the recursive x* has that many fewer characters. We use
    # startx=1 to say that x must match at least 1 character
    if not Ns:
        return null
    xmatches = x(set(range(startx, max(Ns)+1)))
    Ns_x = set(len(m) for m in xmatches)
    Ns_y = set(n-m for n in Ns for m in Ns_x if n-m >=0)
    ymatches = y(Ns_y)
    return set(m1 + m2
               for m1 in xmatches for m2 in ymatches
               if len(m1+m2) in Ns)

null = frozenset()



# T E S T I N G

def test_gen():
    def N(hi): return set(range(hi+1))
    a, b, c = map(lit, 'abc')
    assert star(oneof('ab'))(N(2)) == set(['', 'a', 'aa', 'ab', 'ba', 'bb', 'b'])
    assert (seq(star(a), seq(star(b), star(c)))(set([4])) ==
            set(['aaaa', 'aaab', 'aaac', 'aabb', 'aabc', 'aacc', 'abbb',
                 'abbc', 'abcc', 'accc', 'bbbb', 'bbbc', 'bbcc', 'bccc', 'cccc']))
    assert (seq(plus(a), seq(plus(b), plus(c)))(set([5])) ==
            set(['aaabc', 'aabbc', 'aabcc', 'abbbc', 'abbcc', 'abccc']))
    assert (seq(oneof('bcfhrsm'), lit('at'))(N(3)) ==
            set(['bat', 'cat', 'fat', 'hat', 'mat', 'rat', 'sat']))
    assert (seq(star(alt(a,b)), opt(c))(set([3])) ==
            set(['aaa', 'aab', 'aac', 'aba', 'abb', 'abc', 'baa',
                 'bab', 'bac', 'bba', 'bbb', 'bbc']))
    assert lit('hello')(set([5])) == set(['hello'])
    assert lit('hello')(set([4])) == set ()
    assert lit('hello')(set([6])) == set()
    return 'test_gen passes!'

print (test_gen())

