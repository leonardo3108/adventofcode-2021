from math import ceil

DEBUG = 0

if DEBUG >= 3:
    arq = 'resource/input15-mini.txt'    
    DIM_X = DIM_Y = 10
else:
    arq = 'resource/input15.txt'
    DIM_X = DIM_Y = 100

def show_map(map, sep = ''):
    height = len(map)
    width = len(map[0])
    if height > 100 or width > 100:
        tiles_x = ceil(width / 100)
        tiles_y = ceil(height / 100)
        for tile_y in range(0, tiles_y):
            slice_y0 = tile_y * 100
            slice_yf = slice_y0 + 100
            for tile_x in range(0, tiles_x):
                slice_x0 = tile_x * 100
                slice_xf = slice_x0 + 100
                print('Tile ', tile_y+1, 'x', tile_x+1, ' / ', tiles_y, 'x', str(tiles_x), '  -  positions ', slice_y0,':', slice_yf, ' x ', slice_x0, ':', slice_xf, '(Y x X):')
                show_map([row[slice_x0:slice_xf] for row in map[slice_y0:slice_yf]], sep)
    else:
        for row in map:
            result = [str(value) for value in row]
            print(sep.join(result))
def get_map(width, height, arq):
    rows = []
    for line in open(arq):
        row = line.rstrip()
        assert(len(row) == width)
        rows.append([int(value) for value in row]) 
    assert len(rows) == height
    return rows
def get_grid(width, height):
    return [[0]*width for _ in range(height)]
counter = 0
def get_path(start, target, map, costs, paths, depth = 0):
    if start in costs:
        pass#print('get_path', str(start), 'recorded.')
    elif start == target:
        costs[start] = 0
        paths[start] = [start]
    else:
        x, y = start
        right_cost = down_cost = 99999
        if x < target[0]:  ##look right
            right_cost, right_path = get_path((x + 1, y), target, map, costs, paths, depth + 1)
            right_cost += map[y][x + 1]   #enter cost
        if y < target[1]:  ##look down
            down_cost, down_path = get_path((x, y + 1), target, map, costs, paths, depth + 1)
            down_cost += map[y + 1][x]   #enter cost
        if right_cost < down_cost:
            costs[start] = right_cost
            paths[start] = right_path.copy()
        else:
            costs[start] = down_cost
            paths[start] = down_path.copy()
        paths[start].insert(0, start)
    #print('get_path', str(start) + '.' * depth, '->', costs[start], paths[start])
    return costs[start], paths[start]
    
start = (0,0)
target = (DIM_X - 1, DIM_Y - 1)

map = get_map(DIM_X, DIM_Y, arq)
if DEBUG:
    print('Risk Levels:')
    show_map(map)
assert target[0] > start[0]  #*
assert target[1] > start[1]  #**
costs = {}
paths = {}

for diagonal in range(target[1], -1, -1):
    cost, path = get_path((diagonal, diagonal), target, map, costs, paths)
    if DEBUG:
        print(path, '--->', cost)
print('Part one:', cost)

def get_full_map(original_map, times):
    width = len(original_map[0])
    height = len(original_map)
    full_map = get_grid(width * times, height * times)
    for relative_y in range(height):
        for relative_x in range(width):
            base_value = original_map[relative_y][relative_x]
            for tile_y in range(times):
                value = base_value
                for tile_x in range(times):
                    full_map[tile_y * height + relative_y][tile_x * width + relative_x] = value
                    #print(tile_y * height + relative_y, tile_x * width + relative_x, value)
                    value = value + 1 if value < 9 else 1
                base_value = base_value + 1 if base_value < 9 else 1
    return full_map

TIMES = 5
assert TIMES > 0 and TIMES == int(TIMES), 'TIMES (' + str(TIMES) + ') should be a positive integer'
full_map = get_full_map(map, TIMES)
if DEBUG:
    print('\nRisk Levels - full cave:')
    show_map(full_map)
width = DIM_X * TIMES
height = DIM_Y * TIMES
target = (width - 1, height - 1)
costs = {}
paths = {}

for diagonal in range(target[1], -1, -1):
    cost, path = get_path((diagonal, diagonal), target, full_map, costs, paths)
    if DEBUG:
        print(path, '--->', cost)
print('Part two:')
print('\tInitial cost:', cost)

def adjust(x, y, decrease, new_path, costs, paths, height, width):
    costs[(x,y)] -= decrease
    paths[(x,y)] = new_path.copy()
    paths[(x,y)].insert(0, [x,y])
    #print('ops:', x, y, decrease, paths[(x, y)])
    if y > 0 and (x,y) in paths[(x, y - 1)]:
        adjust(x, y - 1, decrease, paths[(x,y)], costs, paths, height, width)
    if y < height-1 and (x,y) in paths[(x, y + 1)]:
        adjust(x, y + 1, decrease, paths[(x,y)], costs, paths, height, width)
    if x > 0 and (x,y) in paths[(x - 1, y)]:
        adjust(x - 1, y, decrease, paths[(x,y)], costs, paths, height, width)
    if x < width-1 and (x,y) in paths[(x + 1, y)]:
        adjust(x + 1, y, decrease, paths[(x,y)], costs, paths, height, width)
def fix(x, y, new_x, new_y, decrease, costs, paths, height, width):
    costs[(x,y)] -= decrease
    paths[(x,y)] = paths[(new_x, new_y)].copy()
    paths[(x,y)].insert(0, [x,y])
    #print('fixed:', paths[(x,y)])
    if x != new_x and y > 0 and (x,y) in paths[(x, y - 1)]:
        adjust(x, y - 1, decrease, paths[(x,y)], costs, paths, height, width)
    if y != new_y and x > 0 and (x,y) in paths[(x - 1, y)]:
        adjust(x - 1, y, decrease, paths[(x,y)], costs, paths, height, width)
    return costs[(x,y)] 

print('\tFixing paths:')
while(True):
    fixes = 0
    old_cost = cost
    for y in range(height - 1, -1, -1):
        for x in range(width - 1, -1, -1):
            my_cost = costs[(x,y)]
            up_decrease = left_decrease = down_decrease = right_decrease = -1
            if y > 0:
                up_decrease  =  my_cost - costs[(x, y - 1)] - full_map[y - 1][x]
            if up_decrease > 0:
                my_cost = fix(x, y, x, y - 1, up_decrease, costs, paths, 500, 500)
                fixes += 1
            if y < height - 2:
                down_decrease  =  my_cost - costs[(x, y + 1)] - full_map[y + 1][x]
            if down_decrease > 0:
                my_cost = fix(x, y, x, y + 1, down_decrease, costs, paths, 500, 500)
                fixes += 1
            if x > 0:
                left_decrease = my_cost - costs[(x - 1, y)] - full_map[y][x - 1]
            if left_decrease > 0:
                my_cost = fix(x, y, x - 1, y, left_decrease, costs, paths, height, width)
                fixes += 1
            if x < width - 2:
                right_decrease = my_cost - costs[(x + 1, y)] - full_map[y][x + 1]
            if right_decrease > 0:
                my_cost = fix(x, y, x + 1, y, right_decrease, costs, paths, height, width)
                fixes += 1
    cost = costs[(0,0)]
    if cost < old_cost:
        print('\tNew cost:', cost, '- fixes:', fixes)
    else:
        print('\t\tfixes:', fixes)
    if fixes == 0:
        break
print('Part two:', cost)
