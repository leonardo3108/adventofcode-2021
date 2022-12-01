lines = ['#############','#...........#','###D#B#A#C###','  #D#C#B#A#  ','  #D#B#A#C#  ','  #B#D#A#C#  ','  #########  ']
destination = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

def show(prefix, lines):
    for line in lines:
        print(prefix + line)

def show_history(prefix, sep, locations_history):
    lines_history = [locations2lines(locations) for locations in locations_history[:2]]
    for line_number in range(7):
        line = prefix
        for element in lines_history:
            line += element[line_number] + sep
        print(line)


def line2locations(lines):
    locations = {'A': [], 'B': [], 'C': [], 'D': []}
    ocupation = {}
    #print('--------------')
    for position, line in enumerate(lines[2:-1]):
        locations[line[3]].append((0, position))
        locations[line[5]].append((1, position))
        locations[line[7]].append((2, position))
        locations[line[9]].append((3, position))
        ocupation[(0, position)] = line[3]
        ocupation[(1, position)] = line[5]
        ocupation[(2, position)] = line[7]
        ocupation[(3, position)] = line[9]
        #print (position, line[3], line[5], line[7], line[9])
    #print('--------------')
    return locations, ocupation

def change_line(line, position, value):
    return line[:position] + value + line[position+1:]
    
def change_lines(lines, room, position, value):
    if room in [0,1,2,3]:
        lines[position+2] = change_line(lines[position+2], room*2+3, value)
    elif position in [0,1]:
        lines[1] = change_line(lines[1], position+1, value)
    elif position in [2,3]:
        lines[1] = change_line(lines[1], position+8, value)
    elif position in [4,5,6]:
        lines[1] = change_line(lines[1], position*2-4, value)
    return lines
    
def locations2lines(locations):
    lines = ['#############','#...........#','###.#.#.#.###','  #.#.#.#.#  ','  #.#.#.#.#  ','  #.#.#.#.#  ','  #########  ']
    for amphipod_type in locations.keys():
        for room, position in locations[amphipod_type]:
            lines = change_lines(lines, room, position, amphipod_type)
    return lines

def check_path(ocupation, start_room, start_position, end_room, end_position):
    if start_room == end_room:
        print('ERRO!!!!!!!   (check_path)  ')
        return None
    if start_room > end_room:
        start_room, start_position, end_room, end_position = end_room, end_position, start_room, start_position
    if end_room == 4:
        if end_position in [0,1]:
            for mid_position in range(4, start_room + 4):
                block = ocupation.get((4, mid_position), '.')
                if block != '.':
                    return 4, mid_position, block
            if end_position == 0:
                block = ocupation.get((4, 1), '.')
                if block != '.':
                    return 4, 1, block
        elif end_position in [2,3]:
            for mid_position in range(start_room + 4, 7):
                block = ocupation.get((4, mid_position), '.')
                if block != '.':
                    return 4, mid_position, block
            if end_position == 3:
                block = ocupation.get((4, 2), '.')
                if block != '.':
                    return 4, 2, block
        else:
            if start_room + 3.5 < end_position:
                step = 1
            else:
                step = -1
            for mid_position in range(start_room + 4, end_position, step):
                block = ocupation.get((4, mid_position), '.')
                if block != '.':
                    return 4, mid_position, block
    else:
        for mid_position in range(start_room + 4, end_room + 4):
            block = ocupation.get((4, mid_position), '.')
            if block != '.':
                return 4, mid_position, block
    return None

def move(lines, locations, ocupation, specimen, start_room, start_position, end_room, end_position):
    start_value = ocupation.get((start_room, start_position), '.')
    end_value = ocupation.get((end_room, end_position), '.')
    if start_value != '.' and end_value == '.' or start_value == '.' and end_value != '.':
        path = check_path(ocupation, start_room, start_position, end_room, end_position)
        if not path:
            ocupation[(end_room, end_position)] = start_value
            ocupation[(start_room, start_position)] = end_value
            lines = change_lines(lines, end_room, end_position, start_value)
            lines = change_lines(lines, start_room, start_position, end_value)
            if start_value != '.':
                locations[start_value][specimen] = (end_room, end_position)
            else:
                locations[end_value][specimen] = (start_room, start_position)
            return lines, locations, ocupation
        #else:
        #    print('\tblocked path:', (start_room, start_position), '>', path[0:2], '=' + path[2] + '=', '>', (end_room, end_position))
    else:
        print('ERRO!!!!!!!!!!!!!!!!')
        exit(1)

tudo = []
record = [0]
recordist = [None]

def check(prefix, locations):
    points = 0
    for amphipod_type in locations.keys():
        for room, position in locations[amphipod_type]:
            if room == destination[amphipod_type]:
                points += 1
    print(prefix + '  ' + str(points), 'points.')
    if points > record[0]:
        record[0] = points
        print('legal', points, 'points')
        recordist[0] = locations.copy()
        if points == 16:
            print('ACABOU')
            exit(1)
    tudo.append(points)
    

def locations2moves(locations_history, ocupation, level):
    if level > 66:
        #print(locations)
        #print(ocupation)
        exit(1)
        return
    locations = dict(locations_history[0])
    for amphipod_type in locations.keys():
        for specimen, (room, position) in enumerate(locations[amphipod_type]):
            lines = locations2lines(locations)
            moves = []
            #print('Looking for destinations for', amphipod_type, (room, position))
            if room == 4:
                if position == 0:
                    block = ocupation.get((4, 1), '.')
                    if block != '.':
                        #print('\tblocked room: (4, 1) (' + block + ')')
                        continue
                elif position == 3:
                    block = ocupation.get((4, 2), '.')
                    if block != '.':
                        #print('\tblocked room: (4, 2) (' + block + ')')
                        continue
            else:
                if position > 0:
                    other_position = position - 1
                    other_block = ocupation.get((room, other_position), '.')
                    while other_block == '.' and other_position > 0:
                        other_position -= 1
                        other_block = ocupation.get((room, other_position), '.')
                    if other_block != '.':
                        #print('\tblocked room:', (room, other_position), '(' + other_block + ')')
                        continue
            task_room = destination[amphipod_type]
            if task_room != room:
                task_position = 0
                block = ocupation.get((task_room, task_position), '.')
                if block == '.':
                    while block == '.' and task_position < 3:
                        task_position += 1
                        block = ocupation.get((task_room, task_position), '.')
                    if block == amphipod_type:
                        task_position -= 1
                    if block in ['.', amphipod_type]:
                        moves.append((task_room, task_position))
                    #else:
                    #    print('\tproibited room:', (task_room, task_position), '(' + block + ')')
                #else:
                #    print('\tdestination (room,position):', (task_room, task_position), 'already ocupied:', block)
            if room != 4:
                if task_room == room:
                    #print('ops...', amphipod_type, (room, position))
                    not_again = True
                    for other_position in range(position+1, 4):
                        if ocupation.get((room, other_position), '.') != amphipod_type:
                            not_again = False
                            break
                    if not_again:
                    #    print('\tDead end for:', amphipod_type, 'in', (task_room, task_position))
                        continue
                task_room = 4
                for task_position in [0,1,2,3,4,5,6]:
                    block = ocupation.get((task_room, task_position), '.')
                    if block == '.':
                        if task_position in [0,3]:
                            if task_position == 0:
                                other_block = ocupation.get((task_room, 1), '.')
                            else:
                                other_block = ocupation.get((task_room, 2), '.')
                            if other_block != '.':
                                #print('\tdestination (room,position):', (task_room, task_position), 'blocked')
                                continue
                        moves.append((task_room, task_position))
                    #else:
                    #    print('\tdestination (room,position):', (task_room, task_position), 'already ocupied:', block)
            if moves:
                print('Level', level, '--------------------------- Possible moves for', amphipod_type, str((room, position)) + ':', moves)
                for move_room, move_position in moves:
                    moved = move(lines, locations, ocupation, specimen, room, position, move_room, move_position)
                    if moved:
                        lines, locations, ocupation = moved
                        #show('\t', lines)
                        show_history('\t', '  ', locations_history)
                        check('\t',locations)
                        locations_history.insert(0, locations)
                        locations2moves(locations_history, ocupation, level + 1)
                        lines, locations, ocupation = move(lines, locations, ocupation, specimen, move_room, move_position, room, position)
            else:
                #print('\tStuck here!', amphipod_type, (room, position))
                continue
    return

locations, ocupation = line2locations(lines)
print(locations)
print(ocupation)
print('--------------')
lines = locations2lines(locations)
show('', lines)
print('--------------')
locations2moves([locations], ocupation, 0)
#room0, room1, room2, room3
#position0, position1, position2, position3

#room4
#left corner: position0, position1
#right corner: position2, position3
#halfway: position4, position5, position6

print('Max:', record[0], 'points', recordist[0])

