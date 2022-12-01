def absolute(position):
    return [abs(position[0]), abs(position[1]), abs(position[2])]

def distance(position):
    return sum(absolute(position))

def nearest(scanner, quantity):
    past = 0
    values = sorted(distances_scanner[scanner])[:quantity]
    result = [distances_scanner[scanner].index(value) for value in values]
    return result[:quantity]
    
def compare(scanner1, scanner2):
    for value in distances_beacons_bags[scanner1].keys():
        if value in distances_beacons_bags[scanner2]:
            print('ACHEI!!!!!!!!!!!!!!!', scanner1, scanner2, value, distances_beacons_bags[scanner1][value], distances_beacons_bags[scanner2][value])
            

LIMIT = 25
    
scans = {}
distances_scanner = {}
nearests = {}
selections = {}
vectors_beacons = {}
distances_beacons = {}
distances_beacons_bags = {}


#for line in open('../resource/input19.txt'):
for line in open('../resource/input19-mini.txt'):
    if '---' in line:
        scanner = int(line.split()[2])
        scans[scanner] = []
        distances_scanner[scanner] = []
    elif ',' in line:
        scan = [int(x) for x in line.rstrip().split(',')]
        scans[scanner].append(scan)
        distances_scanner[scanner].append(distance(scan))

for scanner in distances_scanner.keys():
    nearests[scanner] = nearest(scanner, LIMIT)
    distances_beacons_bags[scanner] = {}
    for position in nearests[scanner]:
        selections[(scanner, position)] = scans[scanner][position]
        for other in nearests[scanner]:
            if other < position:
                delta = [scans[scanner][position][dim] - scans[scanner][other][dim] for dim in [0,1,2]]
                module = distance(delta)
                vectors_beacons[(scanner, position, other)] = delta
                distances_beacons[(scanner, position, other)] = module
                if module not in distances_beacons_bags[scanner]:
                    distances_beacons_bags[scanner][module] = []
                distances_beacons_bags[scanner][module].append((position, other))

compare(0,1)


exit()
print()
print(selections)
print()
print(vectors_beacons)
print()
print(distances_beacons_bags)

