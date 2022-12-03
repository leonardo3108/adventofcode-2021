class Board:
    def __init__(self) -> None:
        self.lines = []
    def complete(self) -> None:
        self.size = len(self.lines[0])
        self.columns = [[line[i] for line in self.lines] for i in range(self.size)]
        self.position = {self.lines[y][x]: (x, y) for x in range(self.size) for y in range(self.size)}
        self.line_hits = [0 for _ in self.lines]
        self.column_hits = [0 for _ in self.columns]
        self.marked = []
        self.all = self.lines[0].copy()
        for line in self.lines[1:]:
            self.all.extend(line)
        #[n for n in line for line in self.lines]
        self.unmarked = self.all.copy()
        self.openned = True
    def check_hit(self, number) -> int:
        if self.openned and number in self.position:
            self.marked.append(number)
            self.unmarked.remove(number)
            x, y = self.position[number]
            self.line_hits[y] += 1
            self.column_hits[x] += 1
            if self.size in [self.line_hits[y], self.column_hits[x]]:
                self.openned = False
                return 2
            return 1
        return 0

    def __repr__(self) -> str:
        result = ''
        for line in self.lines:
            result += '\n' + str(line)
        #result += '\n---'
        #for column in self.columns:
        #    result += '\n' + str(column)
        return result
        #return str(self.position)

numbers = []
boards = []
for line in open('resource/input04.txt'):
    line = line.rstrip()
    if not numbers:
        numbers = [int(n) for n in line.split(',')]
    elif not line:
        if boards:
            board.complete()
        board = Board()
        boards.append(board)
    else:
        board.lines.append([int(n) for n in line.split(' ') if n])
board.complete()
#print(len(boards), 'boards loaded.')
#print('Numbers:', numbers)
#print(boards)

first = True
for i, number in enumerate(numbers):
    #print('New number:', number)
    for board in boards:
        hit = board.check_hit(number)
        if hit == 2:
            #print(board)
            #print(board.unmarked)
            #print(board.marked)
            score = sum(board.unmarked) * number
            if first:
                print('Part one:', score)
                first = False
print('Part two:', score)
