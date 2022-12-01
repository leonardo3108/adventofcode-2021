program = [cmd_line.rstrip().split() for cmd_line in open('../resource/input24.txt')]

blocks = []

for command_line in program:
    if command_line[0] == 'inp':
        blocks.append([])
    blocks[-1].append(command_line)

first_block = True
base = []

params = ['alpha', 'beta', 'gama', 'delta']
values = {'alpha':list(range(1,10))}
param_command_line = {}
command_line_param = {}

param_number = 0
for block_number, block in enumerate(blocks):
    for index, command in enumerate(block):
        if block_number == 0:
            base.append(command.copy())
        else:
            base_command = base[index]
            if command[0] == 'inp':
                if base_command[-1] not in params:
                    param = params[param_number]
                    base_command.append(param)
                    param_command_line[index] = base_command
                    command_line_param[param] = index
                    param_number += 1
            elif command != base_command or index == 4:
                if base_command[-1] not in params:
                    param = params[param_number]
                    values[param] = [int(base_command[-1])]
                    base_command[-1] = param
                    param_command_line[index] = base_command
                    command_line_param[param] = index
                    param_number += 1
                values[base_command[-1]].append(int(block[index][-1]))

for command in base:
    print(' '.join(command))

print()

for param in params:
    print(param + ',' + str(values[param]).replace(' ','').replace('[','').replace(']',''))
