SIZE = 10
MIN_STEPS = 100

rows = []
for row in open('../resource/input11.txt'):
    assert len(row.rstrip()) == SIZE
    rows.append([int(value) for value in row.rstrip()])
assert len(rows) == SIZE


def increase_octopus(rows, ready, x, y):
    if x >= 0 and x < SIZE and y >= 0 and y < SIZE and (x,y) not in ready:
        rows[y][x] += 1
        if rows[y][x] > 9:
            ready.append((x, y))

def increase_grid(rows):
    ready = []
    for x in range(SIZE):
        for y in range(SIZE):
            increase_octopus(rows, ready, x, y)
    return rows, ready

def flash(rows, ready):
    index = 0
    while index < len(ready):
        x, y = ready[index]
        increase_octopus(rows, ready, x-1, y-1)
        increase_octopus(rows, ready, x-1, y)
        increase_octopus(rows, ready, x-1, y+1)
        increase_octopus(rows, ready, x, y-1)
        increase_octopus(rows, ready, x, y+1)
        increase_octopus(rows, ready, x+1, y-1)
        increase_octopus(rows, ready, x+1, y)
        increase_octopus(rows, ready, x+1, y+1)
        rows[y][x] = 0
        index += 1
    return index

def make_step(rows):
    rows, ready = increase_grid(rows)
    return flash(rows, ready)
    
flashes = all = step = 0
size_grid = SIZE * SIZE
while not all or step < MIN_STEPS:
    flashes_step = make_step(rows)
    if step < MIN_STEPS:
        flashes += flashes_step
    if flashes_step == size_grid and not all:
        all = step+1
    step += 1
    #print('step', step, 'flashes_step', flashes_step, 'flashes', flashes, 'all', all, str(rows).replace(' ', '').replace(',', '').replace('][', ' ').replace('[[', '[').replace(']]', ']'))
print('Part one:', flashes)
print('Part two:', all)

