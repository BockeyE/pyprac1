import time

t0 = time.time()


class point:
    # 数独中的一个点对象，包含x，y坐标，avail是周围可以填写的位置数组
    # value是值
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.available = []
        self.value = 0


def rowNum(p, sudoku):
    # 行数
    row = set(sudoku[p.y * 9:(p.y + 1) * 9])
    row.remove(0)
    return row


def colNum(p, sudoku):
    col = []
    lenth = len(sudoku)
    for i in range(p.x, lenth, 9):
        col.append(sudoku[i])
    col = set(col)
    col.remove(0)
    return col


def blockNum(p, sudoku):
    block_x = p.x // 3
    block_y = p.y // 3
    block = []
    start = block_y * 3 + 9 + block_x * 3
    for i in range(start, start + 3):
        block.append(sudoku[i])
    for i in range(start + 9, start + 9 + 3):
        block.append(sudoku[i])
    for i in range(start + 18, start + 18 + 3):
        block.append(sudoku[i])
    block = set(block)
    block.remove(0)
    return block


def initPoint(sudoku):
    pointList = []
    lenth = len(sudoku)
    for i in range(lenth):
        if sudoku[i] == 0:
            p = point(i % 9, i // 9)
            for j in range(1, 10):
                if j not in rowNum(p, sudoku) and j not in colNum(p, sudoku) and j not in blockNum(p, sudoku):
                    p.available.append(j)
