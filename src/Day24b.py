program = [cmd_line.rstrip().split() for cmd_line in open('../resource/input24.txt')]

#for command_line in program:
#    print(command_line)
print('\n\n\n')
print(len(program), 'commands.')

def execute(command_line, variables, index):
    command, variable = command_line[:2]
    if command == 'inp':
        variables[variable] = 'model_str!' + str(index)
        index += 1
    elif command in ['mul', 'add', 'mod', 'div', 'eql']:
        if command_line[2] in variables.keys():
            value = variables[command_line[2]]
        else:
            value = int(command_line[2])
        if command in ['mul', 'mod', 'div'] and variables[variable] == '0':
            return variables, index, command_line
        if command in ['add'] and variables[variable] == '0':
            variables[variable] = str(value)
            if str(value).isdigit():
                return variables, index, ['set', variable, str(value)]
            return variables, index, ['set', variable, command_line[2]]
        if command in ['mul', 'div']:
            if str(value) == '1':
                return variables, index, command_line
            if value == 0:
                variables[variable] = '0'
                return variables, index, ['set', variable, variables[variable]]
            if str(value).isdigit():
                if variables[variable].isdigit():
                    if command == 'mul':
                        variables[variable] = str(int(variables[variable]) * int(value))
                    elif command == 'div':
                        variables[variable] = str(int(variables[variable]) // int(value))
                    return variables, index, ['set', variable, variables[variable]]
                else:
                    if command == 'mul':
                        variables[variable] += '*' + str(value)
                    elif command == 'div':
                        variables[variable] += '/' + str(value)
            else:
                if command == 'mul':
                    variables[variable] += '*(' + str(value) + ')'
                elif command == 'div':
                    variables[variable] += '/(' + str(value) + ')'
            #print('passou-' + command, variable, variables[variable], value)
        elif command == 'add':
            if value == '0':
                return variables, index, command_line
            if variables[variable].isdigit():
                variables[variable] = str(int(variables[variable]) + value)
                return variables, index, ['set', variable, variables[variable]]
            if variables[variable][-2] == '+' and variables[variable][-1].isdigit() and str(value).isdigit():
                variables[variable] = variables[variable][:-1] + str(int(variables[variable][-1]) + int(value))
            elif str(value)[0] == '-':
                #print('passou-sub', variable, variables[variable], value)
                variables[variable] += '-' + str(value)[1:]
            else:
                #print('passou-add', variable, variables[variable], value)
                variables[variable] += '+' + str(value)
        elif command == 'mod':
            if variables[variable][:-3] == 'model_str!' and value > 9 + int(variables[variable][-1]):
                return variables, index, command_line
            if str(value).isdigit() and not variables[variable].isdigit():
                variables[variable] += '%' + str(value)
                return variables, index, command_line
            print('passou-mod', variable, variables[variable], value)
            variables[variable] %= value
        elif command == 'eql':
            if variables[variable].isdigit():
                if len(variables[variable]) > 1 and value[:-1] == 'model_str!':
                    variables[variable] = '0'
                    return variables, index, ['set', variable, '0']
                if variables[variable] == str(value):
                    variables[variable] = '1'
                    return variables, index, ['set', variable, '1']
            elif variables[variable][:10] == 'model_str!' and '+' in variables[variable]:
                calc = variables[variable].split('+')
                if len(calc) > 1 and calc[-1].isdigit():
                    if int(calc[-1]) >= 9 and value[:-1] == 'model_str!':
                        variables[variable] = '0'
                        return variables, index, ['set', variable, '0']
            print('passou-eql', variable, variables[variable], value)
            variables[variable] += '=' + str(value)
    return variables, index, command_line

index = 0
variables = {'w': '0', 'x': '0', 'y': '0', 'z': '0'}
new_program = []

LIMIT = 105

def show(prefix, variables):
    print(prefix + 'variables:')
    for variable in variables.keys():
        print(prefix + '\t\'' + variable + '\':', variables[variable])

quiet = LIMIT - 5
super_quiet = quiet - 5
for line_number, command_line in enumerate(program[:LIMIT]):
    if line_number >= quiet:
        print(command_line)
        show('', variables)
        print(index)
    str_before = str(variables) + ' ' + str(index)
    variables, index, new_command = execute(command_line, variables, index)
    str_after = str(variables) + ' ' + str(index)
    if str_before == str_after:
        prefix = '\tnot changed:'
    else:
        prefix = '\tchanged:    '
        new_program.append(new_command)
    if line_number >= super_quiet:
        print(prefix + str(command_line))
        show(prefix, variables)
        print(prefix + 'index:', index)
        print('----------------------------------------')
print(len(new_program), '/', LIMIT, 'commands. Last five:')
for command_line in new_program[-5:]:
    print('\t' + str(command_line))
