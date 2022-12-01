program = [cmd_line.rstrip().split() for cmd_line in open('../resource/input24.txt')]

def execute(command_line, model_str, variables, index):
    command, variable = command_line[:2]
    if command == 'inp':
        variables[variable] = int(model_str[index])
        index += 1
    elif command in ['mul', 'add', 'mod', 'div', 'eql']:
        if command_line[2] in variables.keys():
            value = variables[command_line[2]]
        else:
            value = int(command_line[2])
        if command == 'mul':
            variables[variable] *= value
        elif command == 'add':
            variables[variable] += value
        elif command == 'mod':
            variables[variable] %= value
        elif command == 'div':
            variables[variable] //= value
        elif command == 'eql':
            if variables[variable] == value:
                variables[variable] = 1
            else:
                variables[variable] = 0
    return variables, index

verbose = False

def build_str(model_str, position):
    digit = model_str[position]
    if digit == '1':
        new_digit = '9'
    else:
        new_digit = str(int(digit)-1)
    if position == 13:
        return model_str[:position] + new_digit
    else:
        return model_str[:position] + new_digit + model_str[position+1:]

def decrease(model_str):
    position = 13
    while True:
        model_str = build_str(model_str, position)
        if model_str[position] == '1':
            if position == 0:
                return None
            position -= 1
        else:
            return model_str
        
model_str = '99999999999999'
while model_str:
    index = 0
    variables = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
#    if verbose:
#        print(model_str + ':', variables, 'index:', index)
    for command_line in program:
        variables, index = execute(command_line, model_str, variables, index)
#        if verbose:
#            print(command_line, 'variables:', variables, 'index:', index)
#    if verbose:
#        print(model_str + ':', 'variables:', variables, 'index:', index)
    if variables['z'] == 0:
        break
    model_str = decrease(model_str)
    if model_str[-5:] == '11111':
        print(model_str)