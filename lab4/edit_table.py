from enum import Enum


class Dir(Enum):
    LEFT = 0
    CORNER = 1
    UP = 2

    def __repr__(self):
        if self == Dir.LEFT:
            return '⭠'
        elif self == Dir.CORNER:
            return '⭦'
        else:
            return '⭡'

class Op(Enum):
    INSERT = 0
    REPLACE = 1
    DELETE = 2


class EditTable:
    
    def __init__(self, x, y, delta):
        self.x = x
        self.y = y
        self.delta = delta

        self.table = [[None for _ in range(len(y) + 1)] for _ in range(len(x) + 1)]

        for i in range(len(y) + 1):
            self.table[0][i] = (i, Dir.LEFT)
        for i in range(1, len(x) + 1):
            self.table[i][0] = (i, Dir.UP)

        for i in range(1, len(x) + 1):
            for j in range(1, len(y) + 1):
                self.table[i][j] = min([(self.table[i - 1][j][0] + 1, Dir.UP), 
                                            (self.table[i][j - 1][0] + 1, Dir.LEFT), 
                                            (self.table[i - 1][j - 1][0] + delta(x[i - 1], y[j - 1]), Dir.CORNER)], 
                                            key=lambda x: x[0])

    def __str__(self):
        result = f"⭣ {self.x}\n⭢ {self.y}\n"
        for row in self.table:
            result += str(row) + '\n'
        return result

    def __repr__(self):
        return "<EditTable>\n" + self.__str__()

    def get_dist(self):
        return self.table[-1][-1][0]

    def get_seq(self):
        i = len(self.x)
        j = len(self.y)

        seq = []
        while i != 0 or j != 0:
            if self.table[i][j][1] == Dir.LEFT:
                j -= 1
                seq = [(Op.INSERT, j)] + seq
            elif self.table[i][j][1] == Dir.UP:
                i -= 1
                seq = [(Op.DELETE, j)] + seq
            else:
                i -= 1
                j -= 1
                if self.table[i + 1][j + 1][0] != self.table[i][j][0]:
                    seq = [(Op.REPLACE, j)] + seq

        while j != 0:
            j -= 1
            seq = [(Op.INSERT, j)] + seq

        while i != 0:
            i -=1
            seq = [(Op.DELETE, 0)] + seq

        return seq

    def print_seq(self):
        print(self.y)
        x = self.x
        print(x)
        print("edit distance:", self.get_dist())
        
        for i, (op, idx) in enumerate(self.get_seq()):
            print(i + 1, ". ", sep='', end='')
            if op == Op.INSERT:
                if type(x) == str:
                    x = x[:idx] + self.y[idx] + x[idx:]
                else:
                    x = x[:idx] + [self.y[idx]] + x[idx:]
                print(x[:idx], x[idx], x[idx + 1:], sep='*', end='')
                print(f" <----- inserted {x[idx]} on idx {idx}")
            elif op == Op.DELETE:
                deleted = x[idx]
                x = x[:idx] + x[idx + 1:]
                print(x[:idx], x[idx:], sep='*', end='')
                print(f" <----- deleted {deleted} on idx {idx}")
            else:
                replaced = x[idx]
                if type(x) == str:
                    x = x[:idx] + self.y[idx] + x[idx + 1:]
                else:
                    x = x[:idx] + [self.y[idx]] + x[idx + 1:]
                print(x[:idx], x[idx], x[idx + 1:], sep='*', end='')
                print(f" <----- replaced {replaced} with {x[idx]} on idx {idx}")


def _delta2(x, y):
    if x == y:
        return 0
    else:
        return 2

def lcs(x, y):
    return (len(x) + len(y) - EditTable(x, y, _delta2).get_dist()) // 2

def diff(dir_x, dir_y):
    with open(dir_x, 'r') as file_x:
        x = file_x.read()
    with open(dir_y, 'r') as file_y:
        y = file_y.read()

    x = x.split('\n')
    y = y.split('\n')

    edit_table = EditTable(x, y, _delta2)
    seq = edit_table.get_seq()
    bal = 0
    for op, idx in seq:
        if op == Op.DELETE:
            print(f"<{idx + bal} {x[idx + bal]}")
            bal += 1
        else:
            print(f">{idx} {y[idx]}")
            bal -= 1