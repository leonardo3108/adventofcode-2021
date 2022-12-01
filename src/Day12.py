edges = [line.rstrip().split('-') for line in open('../resource/input12.txt')]

connections = {}
for cave1, cave2 in edges:
    if cave1 in connections:
        connections[cave1].append(cave2)
    else:
        connections[cave1] = [cave2]
    if cave2 in connections:
        connections[cave2].append(cave1)
    else:
        connections[cave2] = [cave1]

caves_lower = sorted([cave.lower() for cave in connections.keys()])
caves = []
for cave in caves_lower:
    if cave in connections.keys():
        caves.append(cave)
    else:
        caves.append(cave.upper())
        
sorted_connections = {}

for cave1 in caves:
    conn = connections[cave1]
    sorted_connections[cave1] = [cave for cave in caves if cave in conn]
connections = sorted_connections

def redundant(path):
    size = len(path)
    for former in paths:
        if path == former[:size]:
            return True
    return False

def find_paths(start, end, path, limit, actual_limit):
    path.append(start)
    #if redundant(path):
    #    return
    if start == end:
        paths.append(path)
        actual_limit = limit
        print(path)
        return
    for middle in connections[start]:
        if middle in path:
            if middle.lower() == middle:
                if middle not in ['start', 'end'] and path.count(middle) < actual_limit:
                        find_paths(middle, end, path.copy(), limit, 1)
            else:
                find_paths(middle, end, path.copy(), limit, actual_limit)
                
        else:
            find_paths(middle, end, path.copy(), limit, actual_limit)

#print(connections)
paths = []
find_paths('start', 'end', [], 1, 1)
#print(sorted(paths))
print('Part one:', len(paths))
paths = []
find_paths('start', 'end', [], 2, 2)
#print(sorted(paths))
print('Part two:', len(paths))

    
