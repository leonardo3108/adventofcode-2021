dimension = {'x': 0, 'y': 1}
section = 'dots'
dots = []
folds = []
for line in [line.rstrip() for line in open('../resource/input13.txt')]:
    if section == 'dots':
        if line:
            dots.append([int(value) for value in line.rstrip().split(',')])
        else:
            section = 'instructions'
    elif section == 'instructions':
        variable, value = line.rstrip().split()[-1].split('=')
        folds.append((dimension[variable], int(value)))
        
print('Dots:', len(dots))
print('Folds:', folds)

def make_fold(fold, dots):
    new_dots = []
    dim, value = fold
    for dot in dots:
        if dot[dim] > value:
            dot[dim] = 2 * value - dot[dim]
        if dot not in new_dots:
            new_dots.append(dot)
    return new_dots

print('Part one:', len(make_fold(folds[0], dots)))

for fold in folds:
    dots = make_fold(fold, dots)

print('\nPart two:\n')

message = ['.'*40, '.'*40, '.'*40, '.'*40, '.'*40, '.'*40]

for x, y in dots:
    assert y < 6
    assert x < 40
    message[y] = message[y][:x] + '#' + message[y][x+1:]

for line in message:
    print(line)
    