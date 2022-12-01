hits = {}
hits2 = {}
for line in open('../resource/input05.txt'):
    for i, point in enumerate(line.rstrip().split()[0::2]):
        position_x, position_y = [int(position) for position in point.split(',')]
        if i == 0:
            start_x, start_y = position_x, position_y
        else:
            end_x, end_y = position_x, position_y
    if start_x == end_x:
        if start_y <= end_y:
            #print(start_x, start_y, '>>>', end_x, end_y, ' - up')
            step = 1
        else:
            #print(start_x, start_y, '>>>', end_x, end_y, ' - down')
            step = -1
        for y in range(start_y, end_y + step, step):
            hits[(start_x, y)] = hits.get((start_x, y), 0) + 1
            hits2[(start_x, y)] = hits2.get((start_x, y), 0) + 1
    elif start_y == end_y:
        if start_x <= end_x:
            #print(start_x, start_y, '>>>', end_x, end_y, ' - right')
            step = 1
        else:
            #print(start_x, start_y, '>>>', end_x, end_y, ' - left')
            step = -1
        for x in range(start_x, end_x + step, step):
            hits[(x, start_y)] = hits.get((x, start_y), 0) + 1
            hits2[(x, start_y)] = hits2.get((x, start_y), 0) + 1
    else:
        #print(start_x, start_y, '>>>', end_x, end_y, ' - diagonal')
        if start_x <= end_x:
            step_x = 1
        else:
            step_x = -1
        if start_y <= end_y:
            step_y = 1
        else:
            step_y = -1
        y = start_y
        for x in range(start_x, end_x + step_x, step_x):
            hits2[(x, y)] = hits2.get((x, y), 0) + 1
            y += step_y
count = 0
for x, y in hits.keys():
    if hits[(x,y)] > 1:
        #print((x,y), hits[(x,y)]) 
        count += 1
print('Part one:', count)
count = 0
for x, y in hits2.keys():
    if hits2[(x,y)] > 1:
        #print((x,y), hits[(x,y)]) 
        count += 1
print('Part two:', count)
