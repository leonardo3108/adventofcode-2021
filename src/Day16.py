import numpy as np

transmission  = ''
for line in open('../resource/input16.txt'):
    assert not transmission 
    transmission  = ''.join([str(bin(int(hex_value, base=16)))[2:].rjust(4, '0') for hex_value in line.rstrip()])

def process_values(sub_values, packet_type_id):
    if packet_type_id == 0:
        result = sum(sub_values)
    elif packet_type_id == 1:
        result = np.prod(sub_values)
    elif packet_type_id == 2:
        result = min(sub_values)
    elif packet_type_id == 3:
        result = max(sub_values)
    elif packet_type_id == 5:
        result = 0+(sub_values[0] > sub_values[1])
    elif packet_type_id == 6:
        result = 0+(sub_values[0] < sub_values[1])
    elif packet_type_id == 7:
        result = 0+(sub_values[0] == sub_values[1])
    else:
        result = -50
    #print('process', sub_values, '=' + str(packet_type_id) + '=>', result)
    return result

def decode_package(transmission, level, start, end):
    packet_version = int(transmission[start:start+3], base=2)
    packet_type_id = int(transmission[start+3:start+6], base=2)
    body = start + 6
    #print('packet level', level, ' start:', start, ' end:', end, ' body (' + transmission[body:body+10] + '...' + transmission[end-10:end] + ')', '\tversion', packet_version, '\ttype ID', packet_type_id)
    if packet_type_id == 4:
        literal = ''
        position = body
        group_prefix = '1'
        while group_prefix == '1':
            group_prefix = transmission[position]
            literal += transmission[position + 1 : position + 5]
            position += 5
        literal = int(literal, base=2)
        #print('\tliteral value', literal)
        return position, literal, packet_version
    else:
        length_type_id = transmission[body]
        body += 1
        version_add = packet_version
        if length_type_id == '0':
            sub_position = body + 15
            subs_length = int(transmission[body : sub_position], base=2)
            final_position = sub_position + subs_length
            #print('\t(operator)\tlength type ID', length_type_id, '\tfinal position', final_position)
            sub = 0
            sub_values = []
            has_rest = transmission[sub_position : final_position].replace('0','').strip()
            while has_rest:
                sub_position, sub_value, packet_version = decode_package(transmission, level + 1, start = sub_position, end = final_position)
                sub += 1
                sub_values.append(sub_value)
                version_add += packet_version
                has_rest = transmission[sub_position : final_position].replace('0','').strip()
            rest = transmission[final_position : end]
            has_rest = rest.replace('0','').strip()
            if not has_rest:
                final_position = end
        elif length_type_id == '1':
            sub_position = body + 11
            subs_number = int(transmission[body : sub_position], base=2)
            #print('\t(operator)\tlength type ID', length_type_id, '\tnumber of sub-packets', subs_number)
            sub_values = []
            for sub in range(subs_number):
                sub_position, sub_value, packet_version = decode_package(transmission, level + 1, start=sub_position, end=end)
                sub_values.append(sub_value)
                version_add += packet_version
            sub += 1
            final_position = sub_position
        #print('up! level', level, ' from ', sub, 'subs, version_add=', version_add)
        final_value = process_values(sub_values, packet_type_id)
        
        return sub_position, final_value, version_add

#print(transmission)
#print()
sub_position, final_value, version_add = decode_package(transmission, level=0, start = 0, end=len(transmission))
print('Part one:', version_add)
print('Part two:', final_value)


