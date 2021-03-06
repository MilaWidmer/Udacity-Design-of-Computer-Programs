import random

def deal(numhands, n=5, deck=[r+s for r in '23456789TJQKA' for s in 'SHDC']):
    "Shuffle the deck and deal out numhands n-card hands."
    random.shuffle(deck)
    return [deck[n*i:n*(i+1)] for i in range(numhands)]

def poker(hands):
    "Return a list of winning hands: poker([hand1, hand2, hand3,...]) -> [hand1, ...]"
    return allmax(hands, key = hand_rank_refactored_2)

def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."
    result, maxval = [], None
    key = key or (lambda x: x)
    print ('hands and ranks:')
    for x in iterable:
        print (x)
        xval = key(x)
        print (xval)
        if not result or xval > maxval:
            result, maxval = [x], xval
        elif xval == maxval:
            result.append(x)
    print('maxval:\n'+str(maxval))
    print('winner:')
    return result

def hand_rank_refactored_2(hand):
    "Return a value indicating how high the hand ranks."
    # counts is the count of each rank; ranks lists corresponding ranks
    # E.g. '7 T 7 9 7' => counts = (3, 1, 1); ranks = (7, 10, 9)
    groups = group(['--23456789TJQKA'.index(r) for r, s in hand])
    counts, ranks = zip(*groups)
    if ranks == (14, 5, 4, 3, 2):
        ranks = (5, 4, 3, 2, 1)
    straight = len(ranks) == 5 and max(ranks)-min(ranks) == 4
    flush = len(set([s for r,s in hand])) == 1
    return max(count_rankings[counts], 4*straight + 5*flush), ranks

count_rankings = {(5, ):10, (4, 1):7, (3, 2):6, (3, 1, 1):3, (2, 2, 1):2,
                  (2, 1, 1, 1):1, (1, 1, 1, 1, 1):0}

def group(items):
    "Return a list of [(count, x)...], highest count first, then highest x first."
    groups = [(items.count(x), x) for x in set(items)]
    return sorted(groups, reverse=True)

print(poker(deal(3)))