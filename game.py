import copy

import numpy as np
import random


class Game(object):
    def __init__(self, dimension=4):
        self.dimension = dimension  # 维数，决定要构建几维的矩阵
        self.matrix = np.zeros((dimension, dimension))  # 创建一个全是0的n(n = dimension)维矩阵
        self.matrixSimu = np.zeros((dimension, dimension))

    def judge_gameover(self):  # 判断是否游戏结束，如果游戏结束返回True，未结束则返回False
        '''如果水平方向上任意两个相邻的数字有相等的或者有为0的那么游戏未结束'''
        for a in range(0, self.dimension):
            for b in range(0, self.dimension - 1):
                if self.matrix[a][b] == self.matrix[a][b + 1] or self.matrix[a][b] == 0 or self.matrix[a][b + 1] == 0:
                    return False
        '''如果垂直方向上任意两个相邻的数字有相等的或者有为0的那么游戏未结束'''
        self.matrix = np.transpose(self.matrix)  # 先转置垂直方向变作水平方向 eg:[[1,2],[3,4]]>>[[1,3],[2,4]]
        for a in range(0, self.dimension):
            for b in range(0, self.dimension - 1):
                if self.matrix[a][b] == self.matrix[a][b + 1] or self.matrix[a][b] == 0 or self.matrix[a][b + 1] == 0:
                    return False
        return True

    def generate_num(self):  # 在随机的空白(为0)的位置替换为1个随机的2或者4

        # 判断矩阵内为零的数的位置,并将索引放入到list_0中
        list_0 = []
        for a in range(0, self.dimension):
            for b in range(0, self.dimension):
                if self.matrix[a, b] == 0:
                    list_0.append([a, b])

        # 判断矩阵内为0的数的个数，如果为0,那么就不再生成新的数字
        if len(list_0) != 0:
            x = random.sample(list_0, 1)[0]  # 注意random.sample()函数返回值类型为列表
            self.matrix[x[0]][x[1]] = random.randrange(2, 5, 2)

    def left_(self, matrix):  # 向左平移合并
        '''数字向左平移'''
        for i in range(0, self.dimension):
            list_i = list(matrix[i])
            while 0 in list_i:
                list_i.remove(0)
            while len(list_i) != self.dimension:
                list_i.append(0)
            matrix[i] = list_i

        '''水平向左合并'''
        for a in range(0, self.dimension):
            for b in range(0, self.dimension - 1):
                if matrix[a][b] != 0 and matrix[a][b] == matrix[a][b + 1]:
                    matrix[a][b] = 2 * matrix[a][b]
                    matrix[a][b + 1] = 0
                else:
                    pass

        '''数字向左平移'''
        for i in range(0, self.dimension):
            list_i = list(matrix[i])
            while 0 in list_i:
                list_i.remove(0)
            while len(list_i) != self.dimension:
                list_i.append(0)
            matrix[i] = list_i

    def right_(self, matrix):  # 向右平移合并
        for i in range(0, self.dimension):  # 将矩阵水平方向反转 eg：[[1,2],[3,4]]>>[[2,1],[4,3]]
            matrix[i] = matrix[i][::-1]
        self.left_(matrix)  # 注意在类中内置函数互相调用前面要加self.，也注意不要循环调用
        for i in range(0, self.dimension):  # 再将矩阵水平方向反转回来
            matrix[i] = matrix[i][::-1]

    def down_(self, matrix):  # 向下平移合并
        matrix = matrix[::-1]  # 先上下反转 eg:[[1,2],[3,4]]>>[[3,4],[1,2]]
        self.up_(matrix)
        matrix = matrix[::-1]  # 再上下反转回来eg:[[3,4],[1,2]]>>[[1,2],[3,4]]

    def up_(self, matrix):  # 向上平移合并
        matrix = np.transpose(matrix)  # 先转置 eg:[[1,2],[3,4]]>>[[1,3],[2,4]]
        self.left_(matrix)
        matrix = np.transpose(matrix)  # 再转置回来 eg:[[1,3],[2,4]]>>[[1,2],[3,4]]

    def move(self, matrix, dir):
        if dir == 3:
            self.left_(matrix)
        elif dir == 1:
            self.right_(matrix)

        elif dir == 0:
            self.up_(matrix)

        elif dir == 2:
            self.down_(matrix)

    def print_(self, matrix):  # 显示
        for i in matrix:
            print(i)

    def simulation(self, dir):
        # 初始化预测模型

        self.matrixSimu = copy.deepcopy(self.matrix)
        # 上移
        if dir == 'UP':
            self.move(self.matrixSimu, 0)

        # 右移
        elif dir == 'RIGHT':
            self.move(self.matrixSimu, 1)

        # 下移
        elif dir == 'DOWN':
            self.move(self.matrixSimu, 2)
        # 左移
        elif dir == 'LEFT':
            self.move(self.matrixSimu, 3)

    def monotonicity(self):
        score = 100  # 初始化分数
        subtract = score / (2 * 4 * 4)  # 每次减去的基数
        # 求当前所有数字的平均数
        average = 0
        for i in range(4):
            for j in range(4):
                average = self.matrixSimu[i][j] + average
        average /= 16

        # 检测最高数字所在区域
        maxNum = {'num': 0, 'i': 0, 'j': 0}
        for i in range(4):
            for j in range(4):
                if self.matrixSimu[i][j] > maxNum['num']:
                    maxNum['num'] = self.matrixSimu[i][j]
                    maxNum['i'] = i
                    maxNum['j'] = j

        # 左-右：递减
        if maxNum['j'] < 2:
            for i in range(4):
                for j in range(1, 4):
                    if self.matrixSimu[i][j] > self.matrixSimu[i][j - 1]:
                        score -= subtract * ((self.matrixSimu[i][j] - self.matrixSimu[i][j - 1]) / average)
        # 左-右：递增
        else:
            for i in range(4):
                for j in range(1, 4):
                    if self.matrixSimu[i][j] < self.matrixSimu[i][j - 1]:
                        score -= subtract * ((self.matrixSimu[i][j - 1] - self.matrixSimu[i][j]) / average)
        # 上-下：递减
        if maxNum['i'] < 2:
            for j in range(4):
                for i in range(1, 4):
                    if self.matrixSimu[i][j] > self.matrixSimu[i - 1][j]:
                        score -= subtract * ((self.matrixSimu[i][j] - self.matrixSimu[i - 1][j]) / average)
        # 上-下：递增
        else:
            for j in range(4):
                for i in range(1, 4):
                    if self.matrixSimu[i][j] < self.matrixSimu[i - 1][j]:
                        score -= subtract * ((self.matrixSimu[i - 1][j] - self.matrixSimu[i][j]) / average)
        return score

    # 平滑性得分
    def smoothness(self):
        score = 0  # 初始化分数
        plus = 20  # 每次加上的基数
        # 求当前所有数字的平均数
        average = 0
        for i in range(4):
            for j in range(4):
                average += self.matrixSimu[i][j]
        average /= 16

        # 横向扫描
        for i in range(4):
            for j in range(1, 4):
                if self.matrixSimu[i][j] == self.matrixSimu[i][j - 1]:
                    score += plus * (self.matrixSimu[i][j] / average)
        # 纵向扫描
        for j in range(4):
            for i in range(1, 4):
                if self.matrixSimu[i][j] == self.matrixSimu[i - 1][j]:
                    score += plus * (self.matrixSimu[i][j] / average)
        return score

    # 空闲方块加分
    def freeTiles(self):
        score = 0  # 初始化分数
        plus = 10  # 每次加上的基数
        # 遍历数组
        for j in range(4):
            for i in range(4):
                if self.matrixSimu[i][j] == 0:
                    score += plus
        return score

    dirKey = ['UP', 'RIGHT', 'DOWN', 'LEFT']
    weightProp = [15, 4, 4]

    def compare_matrix(self, matrix1, matrix2):
        isEqual = True
        for i in range(4):
            for j in range(4):
                if matrix1[i][j] != matrix2[i][j]:
                    isEqual = False
        return isEqual

    scores = [0] * 4
    MAX_DEPTH = 4

    def helper(self, score, depth):
        if depth >= self.MAX_DEPTH:
            return 0

        tree_score = 0
        for i in range(4):
            tree_score += self.helper(score, depth + 1) * ((self.MAX_DEPTH + 1 - depth) / self.MAX_DEPTH)

        return tree_score + score

    def best_move(self):
        self.scores = [0] * 4
        for i in range(4):
            self.simulation(self.dirKey[i])
            # 该方向无法移动
            if self.compare_matrix(self.matrix, self.matrixSimu):
                self.scores[i] = 0

            else:
                self.scores[i] = self.monotonicity() * self.weightProp[0] + self.smoothness() * self.weightProp[
                    1] + self.freeTiles() * self.weightProp[2] + self.helper(self.scores[i], self.MAX_DEPTH)
        self.move(self.matrix, self.scores.index(max(self.scores)))

    def run(self):
        self.__init__()
        self.generate_num()
        self.generate_num()
        count = 0
        for i in range(10000):
            count += 1
            self.best_move()
            self.generate_num()
            if self.judge_gameover():
                return self.matrix, np.amax(self.matrix), count


if __name__ == '__main__':  # 主程序
    g1 = Game()
    g1.generate_num()
    g1.generate_num()

    for i in range(10000):
        g1.best_move()
        g1.generate_num()
        g1.print_(g1.matrix)
        if g1.judge_gameover():
            print("moves: " and i)
            break
