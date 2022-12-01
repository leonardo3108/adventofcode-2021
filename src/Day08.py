def minus(patt1, patt2):
    return [seg for seg in patt1 if seg not in patt2]

def last(patt1, patt2):
    m = minus(patt1, patt2)
    if len(m) == 1:
        return m[0]
    return None
    
def missing(pattern):
    if len(pattern) != 6:
        return None
    return last('abcdefg', pattern)
    
count = 0
total = 0
for line in open('../resource/input08.txt'):
    patterns, outputs = [elem.rstrip().split() for elem in line.split('|')]
    fast_decode = {}
    decode_235 = []
    decode_690 = {}
    decode = {}
    code = {}
    segment = {}
    for pattern in patterns:
        sorted_pattern = ''.join(sorted(pattern))
        if len(sorted_pattern) == 2:
            decode[sorted_pattern] = fast_decode[sorted_pattern] = 1
            code[1] = sorted_pattern
        elif len(sorted_pattern) == 3:
            decode[sorted_pattern] = fast_decode[sorted_pattern] = 7
            code[7] = sorted_pattern
        elif len(sorted_pattern) == 4:
            decode[sorted_pattern] = fast_decode[sorted_pattern] = 4
            code[4] = sorted_pattern
        elif len(sorted_pattern) == 5:
            decode_235.append(sorted_pattern)
        elif len(sorted_pattern) == 6:
            decode_690[missing(sorted_pattern)] = sorted_pattern
        elif len(sorted_pattern) == 7:
            decode[sorted_pattern] = fast_decode[sorted_pattern] = 8
    sorted_outputs = []
    for output in outputs:
        sorted_output = ''.join(sorted(output))
        count += sorted_output in fast_decode
        sorted_outputs.append(sorted_output)
    code_4_1 = minus(code[4], code[1])
    for seg in decode_690.keys():
        if seg in code[1]:
            segment['c']  = seg
            decode[decode_690[seg]] = 6
            code[6] = decode_690[seg]
            segment['f'] = last(code[1], seg)
        elif seg in code_4_1:
            decode[decode_690[seg]] = 0
            code[0] = decode_690[seg]
            segment['d'] = seg
            segment['b'] = last(code_4_1, seg)
        else:
            decode[decode_690[seg]] = 9
            code[9] = decode_690[seg]
            segment['e'] = seg
    segment['a'] = last(code[7], code[1])
    segment['g'] = last(minus(minus(code[0], code[7]), code_4_1), segment['e'])
    for pattern in decode_235:
        if segment['e'] in pattern:
            decode[pattern] = 2
        elif segment['c'] in pattern:
            decode[pattern] = 3
        else:
            decode[pattern] = 5
    number = 0
    for output in sorted_outputs:
        number = number * 10 + decode[output]
    total += number
print('Part one:', count)
print('Part two:', total)
