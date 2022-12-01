for line in open('../resource/input07.txt'):
    positions = [int(d) for d in line.rstrip().split(',')]
#positions = [16,1,2,0,4,2,7,1,2,14]

fuels = []
#center = round(sum(positions)/len(positions))
for center in range(max(positions)+1):
    fuel = sum([abs(position - center) for position in positions])
    fuels.append(fuel)
    #print(center, fuel)
print('Part one:', min(fuels))

diffs = []
fuels = []
#center = round(sum(positions)/len(positions))
for center in range(max(positions)+1):
    diffs = [abs(position - center) for position in positions]
    fuel = sum([(1+diff)*diff//2 for diff in diffs])
    fuels.append(fuel)
    #print(center, fuel)
print('Part two:', min(fuels))


