from collections import Counter

section = 'template'
polimer = ''
rule = {}
kids = {}
for line in [line.rstrip() for line in open('../resource/input14.txt')]:
    if section == 'template':
        polimer = line
        section = 'pairs'
    elif section == 'pairs' and line:
        pair, insertion = line.split(' -> ')
        rule[pair] = pair[0] + insertion + pair[1]
        kids[pair] = (pair[0] + insertion, insertion + pair[1])


def get_pairs(polimer):
    return [polimer[position:position+2] for position in range(len(polimer)-1)]

def do_insertions(counter):
    new = Counter()
    for pair in counter.keys():
        first, second = kids[pair]
        new[first] = new.get(first, 0) + counter[pair]
        new[second] = new.get(second, 0) + counter[pair]
    return new

def grow_polimer(counter, steps, verbose):
    for step in range(steps):
        counter = do_insertions(counter)
        if verbose:
            print((step+1), counter)
    return counter

def get_elements(pairs, first, last):
    elements = Counter()
    for pair in pairs.keys():
        start, end = pair
        elements[start] = elements.get(start, 0) + pairs[pair]
        elements[end] = elements.get(end, 0) + pairs[pair]
    for element in elements:
        elements[element] = (elements.get(element, 0) + (element == first) + (element == last)) // 2
    return elements

def get_diff(counter):
    quantities = sorted(list(counter.values()))
    return quantities[-1] - quantities[0]

counter = Counter(get_pairs(polimer))
counter = grow_polimer(counter, 10, False)

first, last = polimer[0], polimer[-1]
elements = get_elements(counter, first, last)

print('Part one:', get_diff(elements))

counter = grow_polimer(counter, 30, False)
elements = get_elements(counter, first, last)
print('Part two:', get_diff(elements))


