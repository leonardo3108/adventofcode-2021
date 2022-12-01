#input = 'target area: x=81..129, y=-150..-108'
xmin, xmax = 81, 129
ymin, ymax = -150, -108

print ('xmin:', xmin, '  xmax:', xmax, '  ymin:', ymin, '  ymax:', ymax)
print('==========================================')

def probex(vx0):
    x = sx = step = 0
    vx = vx0
    result = []
    if vx > 0:
        sx = -1
    elif vx < 0:
        sx = 1
    while vx != 0:
        step += 1
        x += vx
        vx += sx
        if x >= xmin and x <= xmax:
            result.append((vx0, vx, x, step))
        if vx0 > 0 and x > xmax or vx0 < 0 and x < xmin:
            break
    return result

def probey(vy0):
    y = step = 0
    vy = vy0
    result = []
    highest = 0
    while y > ymin or vy >= 0:
        step += 1
        y += vy
        if y > highest:
            highest = y
        vy -= 1
        if y >= ymin and y <= ymax:
            result.append((vy0, vy, y, step, highest))
        if vy0 < 0 and y < ymin:
            break
    return result

resultsX = []
resultsY = []
for vx0 in range(0, xmax+1):
    resultsX.extend(probex(vx0))
for vy0 in range(ymin, 500):
    resultsY.extend(probey(vy0))

findingsX = {}
findingsY = {}
for vx0, vx, x, step in resultsX:
    if step not in findingsX:
        findingsX[step] = []
    findingsX[step].append((vx0, vx, x))
for vy0, vy, y, step, highest in resultsY:
    if step not in findingsY:
        findingsY[step] = []
    findingsY[step].append((vy0, vy, y, highest))

results = []
all_highest = 0
for step in range(23):
    if step in findingsX and step in findingsY:
        for vx0, vx, x in findingsX[step]:
            for vy0, vy, y, highest in findingsY[step]:
                results.append(((vx0, vy0), (vx, vy), (x, y), highest, step))
                if highest > all_highest:
                    all_highest = highest

print(results)
print(all_highest)

#    print('vx0:', vx0, '- vx:', vx, '- x:', x, '- step:', step)
#    print('vy0:', vy0, '- vy:', vy, '- y:', y, '- step:', step)
