rows = []
for row in open('../resource/input09.txt'):
    assert len(row.rstrip()) == 100
    rows.append([int(value) for value in row.rstrip()])
assert len(rows) == 100

def get_neighbors(rows, x, y):
    result = []
    if x > 0:
        result.append((x-1, y, rows[y][x-1]))
    if x < 99:
        result.append((x+1, y, rows[y][x+1]))
    if y > 0:
        result.append((x, y-1, rows[y-1][x]))
    if y < 99:
        result.append((x, y+1, rows[y+1][x]))
    return result

def is_low_point(rows, x, y):
    point = rows[y][x]
    for _, _, value in get_neighbors(rows, x, y):
        if value <= point:
            return False
    return True

def get_basin(rows, x, y, original):
    basin = []
    for x, y, value in get_neighbors(rows, x, y):
        if value < 9 and (x,y) not in original:
            basin.append((x,y))
    return basin
    
risk = 0
low_points = []
for y, row in enumerate(rows):
    for x, value in enumerate(row):
        if is_low_point(rows, x, y):
            risk += value + 1
            low_points.append((x,y))
print('Part one:', risk)
assert risk == 439

basins = []
for x, y in low_points:
    basin = []
    uncovered = []
    new = get_basin(rows, x, y, basin)
    while new or uncovered:
        basin += new
        uncovered += new
        x, y = uncovered.pop(0)
        new = get_basin(rows, x, y, basin)
    basins.append(len(basin))

top3 = sorted(basins, reverse=True)[:3]
print('Part two:', top3[0] * top3[1] * top3[2])

