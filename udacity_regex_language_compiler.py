def search(pattern, text):
    "Match pattern anywhere in the text; return longest earliest match or None."
    for i in range(len(text)):
        m = match(pattern, text[i:])
        if m is not None and m is not '':
            return m

def match(pattern, text):
    "Match pattern against start of text; return longest match found of None."
    remainders = pattern(text)
    if remainders:
        shortest = min(remainders, key=len)
        return text[:len(text)-len(shortest)]

def lit(s): return lambda text: set([text[len(s):]]) if text.startswith(s) else null
def seq(x, y): return lambda text: set().union(*map(y, x(text)))
def alt(x, y): return lambda text: x(text) | y(text)
def star(x): return lambda t: (set([t]) |
                               set(t2 for t1 in x(t) if t1 != t
                                   for t2 in star(x)(t1)))
def plus(x): return seq(x, star(x))
def opt(x): return alt(lit(''), x)
def oneof(chars): return lambda text: set([text[1:]]) if (text and text[0] in chars) else null
dot = lambda text: set([text[1:]]) if text else null
eol = lambda text: set(['']) if text == '' else null

null = frozenset()

# T E S T I N G

def test():
    assert match(star(lit('a')), 'aaabcd') == 'aaa'
    assert match(alt(lit('b'), lit('c')), 'ab') == None
    assert match(alt(lit('b'), lit('a')), 'ab') == 'a'
    assert search(alt(lit('b'), lit('c')), 'ab') == 'b'
    return 'tests pass'

print (test())

print (search(star(alt(lit('a'), lit('b'))),'sdfsdfabbbcd'))