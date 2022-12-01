import re

def count_nesting(expression):
    return expression.count('[')-expression.count(']')
    
def find_pair(expression, start_position):
    find_expr = expression
    if start_position > 0:
        find_expr = find_expr[start_position:]
    mt_list = re.split('(\[\d+,\d+\])', find_expr, 1)
    if len(mt_list) > 1:
        if start_position > 0:
            mt_list[0] = expression[:start_position] + mt_list[0]
        return mt_list
    return None

def add_number(expression, reverse, number):
    if reverse:
        expression = expression[::-1]
    mt_list = re.split('(\d+)', expression, 1)
    if len(mt_list) > 1:
        other = mt_list[1]
        if reverse:
            other = other[::-1]
        number += int(other)
        if reverse:
            number = str(number)[::-1]
        expression = mt_list[0] + str(number) + mt_list[2]
    if reverse:
        expression = expression[::-1]
    return expression

def parse_pair(pair):
    return [int(x) for x in pair.lstrip('[').rstrip(']').split(',')]
    
def explode(left_expr, pair, right_expr, config):
    if config['verboseExplosion']:
        print('Exploding:')
        sufix = ''
    else:
        sufix = ' (explosion)'
    to_left, to_right = parse_pair(pair)
    if config['verboseExplosion']:
        print('\t' + left_expr, '<<<', to_left, '*', to_right, '>>>', right_expr)
        print('Result:')
    result = add_number(left_expr, True, to_left) + '0' + add_number(right_expr, False, to_right)
    if config['verboseExplosion'] or config['verboseResultExplosion']:
        print('\t' + result + sufix)
    return result

def find_explosion(expression, config):
    if config['verboseFindExplosion']:
        print('Finding pair:')
    start_position = 0
    while (True):
        finding = find_pair(expression, start_position)
        if finding:
            nesting = count_nesting(finding[0])
            if nesting >= 4:
                if config['verboseFindExplosion']:
                    print('\t' + finding[0] + '****' + finding[1] + '****' + finding[2])
                return explode(finding[0], finding[1], finding[2], config), True
            else:
                start_position = len(finding[0]) + len(finding[1])
                if config['verboseTryExplosion']:
                    print('\t' + finding[0] + '*'*nesting + finding[1] + '*'*nesting + finding[2])
        else:
            if config['verboseFindExplosion']:
                print('\tnot found!')
            return expression, False

def find_split(expression, config):
    if config['verboseFindSplitting']:
        print('Finding number to split:')
        sufix = ''
    else:
        sufix = ' (splitting)'
    mt_list = re.split('(\d\d+)', expression, 1)
    if len(mt_list) > 1:
        number = int(mt_list[1])
        if config['verboseFindSplitting']:
            print('\t' + mt_list[0] + '<<<', number, '>>>' + mt_list[2])
            print('Result:')
        to_left = number // 2
        to_right = number - to_left
        expression = mt_list[0] + '[' + str(to_left) + ',' + str(to_right) + ']' + mt_list[2]
        if config['verboseResultSplitting']:
            print('\t' + expression + sufix)
        return expression, True
    return expression, False

def pre_addition(sn1, sn2):
    if sn1:
        return '[' + sn1 + ',' + sn2 + ']'
    return sn2

def addition(sn1, sn2, config):
    expression = pre_addition(sn1, sn2)
    if config['verboseAddition']:
        print('\nAdd:')
        print('\t' + expression)

    splitted = True
    while (splitted):
        exploded = True
        while (exploded):
            expression, exploded = find_explosion(expression, config)
        expression, splitted = find_split(expression, config)

    if config['verboseAddition']:
        print('\nSum:')
    if config['verbosePartialSum']:
        print('\t' + expression)
    if config['verboseAddition']:
        print()
    return expression

def magnitude_pair(pair):
    left, right = parse_pair(pair)
    return str(3 * left + 2 * right)

def magnitude_expression(expression):
    if config['verboseMagnitudeCalc']:
        print('\nMagnitude calculation:')
    result = find_pair(expression, 0)
    while (result):
        expression = result[0] + magnitude_pair(result[1]) + result[2]
        if config['verboseMagnitudeCalc']:
            print('\t' + expression)
        result = find_pair(expression, 0)
    return expression

##### preprocessing input #####

snailfish_numbers = []
for line in [line.strip() for line in open('../resource/input18.txt')]:
    snailfish_numbers.append(line)

#snailfish_numbers = ['[1,1]','[2,2]','[3,3]','[4,4]']
#snailfish_numbers = ['[1,1]','[2,2]','[3,3]','[4,4]','[5,5]']
#snailfish_numbers = ['[1,1]','[2,2]','[3,3]','[4,4]','[5,5]','[6,6]']
#snailfish_numbers = ['[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]','[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]','[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]','[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]','[7,[5,[[3,8],[1,4]]]]','[[2,[2,2]],[8,[8,1]]]','[2,9]','[1,[[[9,3],9],[[9,0],[0,7]]]]','[[[5,[7,4]],7],1]','[[[[4,2],2],6],[8,7]]']
#snailfish_numbers = ['[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]','[[[5,[2,8]],4],[5,[[9,9],0]]]','[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]','[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]','[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]','[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]','[[[[5,4],[7,7]],8],[[8,3],8]]','[[9,3],[[9,9],[6,[4,9]]]]','[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]','[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]']

config = {'verboseInput': False, 'verboseFindExplosion': False, 'verboseTryExplosion': False, 'verboseExplosion': False, 'verboseResultExplosion': False, 
          'verboseFindSplitting': False, 'verboseResultSplitting': False, 'verboseAddition': False, 'verbosePartialSum': False, 'verboseMagnitudeCalc': False}

print('-------Part One-------')

if config['verboseInput']:
    print('Input lines:')
    for snailfish_number in snailfish_numbers:
        print('\t' + snailfish_number)

##### preprocessing additions #####

expression = ''

if config['verbosePartialSum']:
    print('\nProcessing additions:')

for snailfish_number in snailfish_numbers:
    expression = addition(expression, snailfish_number, config)

print('\nFinal sum:')
print('\t' + expression)

print('Magnitude:', magnitude_expression(expression))
    
print('\n-------Part Two-------')
magnitudes = []
for i, snailfish_number1 in enumerate(snailfish_numbers):
    for j, snailfish_number2 in enumerate(snailfish_numbers):
        if i != j:
            expression = addition(snailfish_number1, snailfish_number2, config)
            magnitudes.append(int(magnitude_expression(expression)))
print('Max Magnitude:', max(magnitudes))
        
        