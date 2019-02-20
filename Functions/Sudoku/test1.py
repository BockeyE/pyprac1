import time

t0 = time.time()


class point:
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
    # 列数统计
    col = []
    lenth = len(sudoku)
    for i in range(p.x, lenth, 9):
        col.append(sudoku[i])
    col = set(col)
    col.remove(0)
    return col


def blockNum(p, sudoku):
    # 方格块统计
    block_x = p.x // 3
    block_y = p.x // 3
    block = []
    start = block_y * 3 * 9 + block_x * 3
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
                # 这一步是核心判断点，在循环遍历过程中，判断当前数是否在3尺度上重复
                if j not in rowNum(p, sudoku) and j not in colNum(p, sudoku) and j not in blockNum(p, sudoku):
                    # 将未重复的数字添加到可用的数字列表中
                    p.available.append(j)
            pointList.append(p)
    return pointList


def check(p, sudoku):
    if p.value == 0:
        # 如果value0，则其为不可用值
        print('not assign p')
        return False
    if p.value not in rowNum(p, sudoku) and p.value not in colNum(p, sudoku) and p.value not in blockNum(p, sudoku):
        return True
    else:
        return False


def tryInsert(p, sudoku):
    availableNum = p.available
    for v in availableNum:
        p.value = v
        if check(p, sudoku):
            sudoku[p.y * 9 + p.x] = p.value
            if len(pointList)<=0
