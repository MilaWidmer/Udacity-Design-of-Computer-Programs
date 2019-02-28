def search(pattern, text):
    "Match pattern anywhere in the text; return longest earliest match or None."
    for i in range(len(text)):
        m = match(pattern, text[i:])
        if m is not None:
            return m

def match(pattern, text):
    "Match pattern against start of text; return longest match found of None."
    remainders = matchset(pattern, text)
    if remainders:
        shortest = min(remainders, key=len)
        return text[:len(text)-len(shortest)]

def components(pattern):
    "Return the op, x and y arguments, x and y are Nonne if missing"
    x = pattern[1] if len(pattern) > 1 else None
    y = pattern[2] if len(pattern) > 2 else None
    return pattern[0], x, y

def matchset(pattern, text):
    "Match patter at start of text; return a set of remainders of text"
    op, x, y = components(pattern)
    if op == 'lit':
        return set([text[len(x):]]) if text.startswith(x) else null
    elif op == 'seq':
        return set(t2 for t1 in matchset(x, text) for t2 in matchset(y, t1))
    elif op == 'alt':
        return (matchset(x, text) | matchset(y, text))
    elif op == 'dot':
        return (set([text[1:]]) if text else null)
    elif op == 'oneof':
        return (set([text[1:]])) if text.startswith(x) else null # or: any(text.startswith(c) for c in x)
    elif op == 'eol':
        return set(['']) if text == '' else null
    elif op == 'star':
        return (set([text]) | set(t2 for t1 in matchset(x, text)
                                   for t2 in matchset(pattern, t1) if t1 != text))
    else:
        raise ValueError('unknown pattern: %s' % pattern)

null = frozenset()

def lit(string):    return ('lit', string)
def seq(x, y):      return ('seq', x, y)
def alt(x, y):      return ('alt', x, y)
def star(x):        return ('star', x)
def plus(x):        return seq(x, star(x))
def opt(x):         return alt(lit(''), x)
def oneof(chars):   return ('oneof', chars)
dot = ('dot')
eol = ('eol')



# T E S T I N G

def test():
    assert matchset(('lit', 'abc'), 'abcdef') == set(['def'])
    assert matchset(('seq', ('lit', 'hi '),
                     ('lit', 'there ')),
                    'hi there nice to meet you') == set(['nice to meet you'])
    assert matchset(('alt', ('lit', 'dog'),
                     ('lit', 'cat')), 'dog and cat') == set([' and cat'])
    assert matchset(('dot',), 'am i missing something?') == set(['m i missing something?'])
    assert matchset(('oneof', 'a'), 'aabc123') == set(['abc123'])
    assert matchset(('eol',), '') == set([''])
    assert matchset(('eol',), 'not end of line') == frozenset([])
    assert matchset(('star', ('lit', 'hey')), 'heyhey!') == set(['!', 'heyhey!', 'hey!'])
    assert match(('star', ('lit', 'a')), 'aaabcd') == 'aaa'
    assert match(('alt', ('lit', 'b'), ('lit', 'c')), 'ab') == None
    assert match(('alt', ('lit', 'b'), ('lit', 'a')), 'ab') == 'a'
    assert search(('alt', ('lit', 'b'), ('lit', 'c')), 'ab') == 'b'
    return 'tests pass'

print (test())
