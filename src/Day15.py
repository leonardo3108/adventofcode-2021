def find_points(distance):
    return [(DIM_X - 1 - dx, DIM_Y - 1 + dx - distance) for dx in range(0, distance + 1)]

def get_value(x, y):
    value = [9999, 9999, 9999, 9999] #down, right, up, left
    xs = [x, x+1, x, x-1]
    ys = [y+1, x, y-1, x]
    if y < DIM_Y - 1:
        value[0] = cost[(x, y+1)] + rows[y+1][x]
    if x == DIM_X - 1:
        if value[0] == 9999:
            value[1] = 0
        else:
            value[1] = 9999
    else:
        value[1] = cost[(x+1, y)] + rows[y][x+1]
    if y > 0 and (x, y-1) in cost:
        value[2] = cost[(x, y-1)] + rows[y-1][x]
    if x > 0 and (x-1, y) in cost:
        value[3] = cost[(x-1, y)] + rows[y][x-1]
    minvalue = 9999
    arg = -1
    for i in range(4):
        if value[i] < minvalue:
            minvalue = value[i]
            arg = i
    return value[arg], xs[arg], ys[arg]
    
def add_kid(xo, yo, x, y, check):
    if check:
        if (x > 0 and xo != x-1 or yo != y) and (x-1, y) in kids and (x,y) in kids[(x-1, y)]:
            kids[(x-1, y)].remove((x,y))
        elif (x < DIM_X-1 and xo != x+1 or yo != y) and (x+1, y) in kids and (x,y) in kids[(x+1, y)]:
            kids[(x+1, y)].remove((x,y))
        elif (xo != x or yo != y-1 and y > 0) and (x, y-1) in kids and (x,y) in kids[(x, y-1)]:
            kids[(x, y-1)].remove((x,y))
        elif (xo != x or yo != y+1 and y < DIM_Y - 1) and (x, y+1) in kids and (x,y) in kids[(x, y+1)]:
            kids[(x, y+1)].remove((x,y))
    if (xo, yo) not in kids:
        kids[(xo, yo)] = []
    kids[(xo, yo)].append((x,y))

def verify(x, y):
    value, xo, yo = get_value(x, y)
    if value > cost[(x,y)]:
        print('ERROR (increased cost):', (x,y), value, '>', cost[(x,y)])
        exit(1)
    elif value < cost[(x,y)]:
        cost[(x,y)] = value
        add_kid(xo, yo, x, y, True)
        if (x,y) in kids:
            for xi, yi in kids[(x,y)]:
                if xi != xo or yi != yo:
                    verify(xi, yi)
        return True
    return False

def add_value(v, r):
    while v > 9:
        v -= 9
    r.append(v)    

######################################################################################  
#####################################  PART ONE  #####################################  
######################################################################################  

#################################  MONTAGEM DO GRID  #################################  
DIM_X = DIM_Y = 100
rows = [[int(value) for value in row.rstrip()] for row in open('../resource/input15.txt') if len(row.rstrip()) == DIM_X]
assert len(rows) == DIM_Y

#################################  CALCULO INICIAL DO GRID  #################################  
cost = {}
kids = {}

for y in range(DIM_Y - 1, -1, -1):
    for x in range(DIM_Y - 1, -1, -1):
        cost[(x,y)], xo, yo = get_value(x, y)
        add_kid(xo, yo, x, y, False)

#################################  CALCULO DEFINITIVO DO GRID  #################################  
instable = True
while instable:
    instable = False
    x = y = 0
    while y < DIM_Y and not instable:
        while x < DIM_X and not instable:
            instable = verify(x, y)
            x += 1
        y += 1
        
#for y in range(DIM_Y - 1, -1, -1):
#    print(','.join([str(cost[(x,y)]) for x in range(DIM_Y - 1, -1, -1)]))
print('Part one:', cost[(0,0)])

######################################################################################  
#####################################  PART TWO  #####################################  
######################################################################################  

#################################  MONTAGEM DO GRID  #################################  
DIM_X = DIM_Y = 500
new_rows = []
for row in rows:
    new_row = row.copy()
    for part in range(1, 5):
        for value in row:
            add_value(value + part, new_row)
    new_rows.append(new_row)
rows = new_rows.copy()
for part in range(1, 5):
    for row in new_rows:
        new_row = []
        for value in row:
            add_value(value + part, new_row)
        rows.append(new_row)

#################################  CALCULO INICIAL DO GRID  #################################  
cost = {}
kids = {}

for y in range(DIM_Y - 1, -1, -1):
    for x in range(DIM_Y - 1, -1, -1):
        cost[(x,y)], xo, yo = get_value(x, y)
        add_kid(xo, yo, x, y, False)

#################################  CALCULO DEFINITIVO DO GRID  #################################  
instable = True
while instable:
    instable = False
    x = y = 0
    while y < DIM_Y and not instable:
        while x < DIM_X and not instable:
            instable = verify(x, y)
            x += 1
        y += 1
    if instable:
        print('instable!', x, y)
        
#for y in range(DIM_Y - 1, -1, -1):
#    print(','.join([str(cost[(x,y)]) for x in range(DIM_Y - 1, -1, -1)]))
print('Part two:', cost[(0,0)])
