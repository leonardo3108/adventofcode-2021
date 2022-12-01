from collections import Counter

for line in open('../resource/input06.txt'):
    counts = dict(Counter([int(d) for d in line.rstrip().split(',')]))

past = 256
new_age = 6
first_age = 8
groups = list(range(first_age + 1))

total = 0
for day in groups:
    if day in counts:
        total += counts[day]
    else:
        counts[day] = 0

def show(day, groups, counts, total):
    print('Day', day, '-', ',  '.join([str(group) + ': ' + str(counts[group]) for group in groups]), ' - total:', total)

show(0, groups, counts, total)
for day in range(1, past+1):
    renew = 0
    for group in sorted(groups):
        quantity = counts[group]
        if group == 0:
            renew = quantity
        else:
            counts[group - 1] = quantity
    counts[new_age] = counts[new_age] + renew
    counts[first_age] = renew
    total += renew
    show(day, groups, counts, total)
    


