closure = {'{': '}', '[': ']', '<': '>', '(': ')'}
openning = {closure[v]: v for v in closure.keys()}
points_illegal = {')': 3, ']': 57, '}': 1197, '>': 25137}
points_completion = {')': 1, ']': 2, '}': 3, '>': 4}

def parse(rest, expect, chunck):
    #print('chunck: "' + chunck + '" - rest: "' + rest + '" - expect: "' + expect + '"')
    next_char = rest[0]
    if expect:
        next_expect = expect[0]
        more_expect = expect[1:]
    else:
        next_expect = ''
        more_expect = ''
    rest = rest[1:]
    if next_char in closure.keys():
        if rest:
            return parse(rest, closure[next_char] + expect, chunck)
        else:
            #print('\tincomplete:', expect)
            return closure[next_char] + expect
    elif next_char == next_expect:
        if rest:
            return parse(rest, more_expect, openning[next_char] + chunck + next_expect)
        else:
            #print('\tincomplete:', more_expect)
            return more_expect
    else:
        #print('\tsintax error', next_char, 'expect', next_expect)
        return points_illegal[next_char]
   
def complete(rest):
    points = 0
    completion = ''
    for next_char in rest:
        completion = openning[next_char] + completion
        points = points * 5 + points_completion[next_char]
    return completion, points
    
lines = [line.rstrip() for line in open('../resource/input10.txt')]
#lines = ['[({(<(())[]>[[{[]{<()<>>', '[(()[<>])]({[<{<<[]>>(', '{([(<{}[<>[]}>{[]{[(<()>', '(((({<>}<{<{<>}{[]{[]{}', '[[<[([]))<([[{}[[()]]]', '[{[{({}]{}}([{[{{{}}([]', '{<[[]]>}<{[{[{[]{()[[[]', '[<(<(<(<{}))><([]([]()', '<{([([[(<>()){}]>(<<{{', '<{([{{}}[<[[[<>{}]]]>[]]']
  
total_illegal = 0
total_completions = []
for line in lines:
    result = parse(line, '', '')
    if type(result) == type(0):
        total_illegal += result
    else:
        completion, points = complete(result)
        #print(result, points)
        total_completions.append(points)

print('Part one:', total_illegal)

total_completions = sorted(total_completions)
middle = (len(total_completions)-1)//2
median = total_completions[middle]
print('Part two:', median)

