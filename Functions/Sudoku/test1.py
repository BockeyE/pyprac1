import time

t0 = time.time()


class point:
    def __init__(self, x, y):
        #初始化一个点对象，拥有坐标属性和周围可填入的点列表，以及本身的值属性
        self.x = x
        self.y = y
        self.available = []
        self.value = 0


def rowNum(p, sudoku):
    # 行数统计，统计该行的数字set集合，不可重复，直接横向选取list为set
    row = set(sudoku[p.y * 9:(p.y + 1) * 9])
    row.remove(0)
    return row


def colNum(p, sudoku):
    # 列数统计，同上
    # 方法不同，每9个数取一个，即按列取数
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
    block_y = p.y // 3
    # 除以3 取整
    block = []
    start = block_y * 3 * 9 + block_x * 3
    for i in range(start, start + 3):
        block.append(sudoku[i])

    for i in range(start + 9, start + 9 + 3):
        block.append(sudoku[i])

    for i in range(start + 18, start + 18 + 3):
        block.append(sudoku[i])

    # 3个循环也是取到一个9宫格中对应的所有数字
    block = set(block)
    block.remove(0)
    return block


def initPoints(sudoku):
    # 初始化points,将数独列表中所有的点转为ponit对象，并返回point对象的列表
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
        # 判断方法同前
        return True
    else:
        return False


def showSudoku(sudoku):
    # 打印出数独列表的方法
    for i in range(9):
        for j in range(9):
            print('%d ' % (sudoku[i * 9 + j]), end='')
        print('')


def tryInsert(p, sudoku, pointList):
    # 递归插入到数独列表中，
    availableNum = p.available
    for v in availableNum:
        p.value = v
        if check(p, sudoku):
            sudoku[p.y * 9 + p.x] = p.value
            if len(pointList) <= 0:
                # 当p点列表中没有元素时，插入方法执行完毕
                t1 = time.time()
                userTime = t1 - t0
                showSudoku(sudoku)
                print('\n use time : %f s' % userTime)
                exit()
            p2 = pointList.pop()
            tryInsert(p2, sudoku, pointList)
            # 递归插入
            sudoku[p2.y * 9 + p2.x] = 0
            sudoku[p.y * 9 + p.x] = 0
            p2.value = 0
            pointList.append(p2)
        else:
            pass


if __name__ == '__main__':
    sudoku = [
        8, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 3, 6, 0, 0, 0, 0, 0,
        0, 7, 0, 0, 9, 0, 2, 0, 0,
        0, 5, 0, 0, 0, 7, 0, 0, 0,
        0, 0, 0, 0, 4, 5, 7, 0, 0,
        0, 0, 0, 1, 0, 0, 0, 3, 0,
        0, 0, 1, 0, 0, 0, 0, 6, 8,
        0, 0, 8, 5, 0, 0, 0, 1, 0,
        0, 9, 0, 0, 0, 0, 4, 0, 0,
    ]
    pointList = initPoints(sudoku)
    showSudoku(sudoku)
    print('\n')
    p = pointList.pop()
    tryInsert(p, sudoku, pointList)
