import copy

import numpy as np
import random


class Game(object):
    def __init__(self, dimension=4):
        self.dimension = dimension  
        self.matrix = np.zeros((dimension, dimension))  
        self.matrixSimu = np.zeros((dimension, dimension))

    def judge_gameover(self):  
     
        for a in range(0, self.dimension):
            for b in range(0, self.dimension - 1):
                if self.matrix[a][b] == self.matrix[a][b + 1] or self.matrix[a][b] == 0 or self.matrix[a][b + 1] == 0:
                    return False
        
        self.matrix = np.transpose(self.matrix) 
        for a in range(0, self.dimension):
            for b in range(0, self.dimension - 1):
                if self.matrix[a][b] == self.matrix[a][b + 1] or self.matrix[a][b] == 0 or self.matrix[a][b + 1] == 0:
                    return False
        return True

    def generate_num(self):  

     
        list_0 = []
        for a in range(0, self.dimension):
            for b in range(0, self.dimension):
                if self.matrix[a, b] == 0:
                    list_0.append([a, b])

     
        if len(list_0) != 0:
            x = random.sample(list_0, 1)[0]  
            self.matrix[x[0]][x[1]] = random.randrange(2, 5, 2)

    def left_(self, matrix):  
       
        for i in range(0, self.dimension):
            list_i = list(matrix[i])
            while 0 in list_i:
                list_i.remove(0)
            while len(list_i) != self.dimension:
                list_i.append(0)
            matrix[i] = list_i

      
        for a in range(0, self.dimension):
            for b in range(0, self.dimension - 1):
                if matrix[a][b] != 0 and matrix[a][b] == matrix[a][b + 1]:
                    matrix[a][b] = 2 * matrix[a][b]
                    matrix[a][b + 1] = 0
                else:
                    pass

       
        for i in range(0, self.dimension):
            list_i = list(matrix[i])
            while 0 in list_i:
                list_i.remove(0)
            while len(list_i) != self.dimension:
                list_i.append(0)
            matrix[i] = list_i

    def right_(self, matrix):  
        for i in range(0, self.dimension): 
            matrix[i] = matrix[i][::-1]
        self.left_(matrix)  
        for i in range(0, self.dimension):  
            matrix[i] = matrix[i][::-1]

    def down_(self, matrix):  
        matrix = matrix[::-1] 
        self.up_(matrix)
        matrix = matrix[::-1] 

    def up_(self, matrix):  
        matrix = np.transpose(matrix) 
        self.left_(matrix)
        matrix = np.transpose(matrix)  

    def move(self, matrix, dir):
        if dir == 3:
            self.left_(matrix)
        elif dir == 1:
            self.right_(matrix)

        elif dir == 0:
            self.up_(matrix)

        elif dir == 2:
            self.down_(matrix)

    def print_(self, matrix): 
        for i in matrix:
            print(i)

    def simulation(self, dir):
    

        self.matrixSimu = copy.deepcopy(self.matrix)
     
        if dir == 'UP':
            self.move(self.matrixSimu, 0)

      
        elif dir == 'RIGHT':
            self.move(self.matrixSimu, 1)

   
        elif dir == 'DOWN':
            self.move(self.matrixSimu, 2)
      
        elif dir == 'LEFT':
            self.move(self.matrixSimu, 3)

    def monotonicity(self):
        score = 100  
        subtract = score / (2 * 4 * 4) 
      
        average = 0
        for i in range(4):
            for j in range(4):
                average = self.matrixSimu[i][j] + average
        average /= 16

 
        maxNum = {'num': 0, 'i': 0, 'j': 0}
        for i in range(4):
            for j in range(4):
                if self.matrixSimu[i][j] > maxNum['num']:
                    maxNum['num'] = self.matrixSimu[i][j]
                    maxNum['i'] = i
                    maxNum['j'] = j

  
        if maxNum['j'] < 2:
            for i in range(4):
                for j in range(1, 4):
                    if self.matrixSimu[i][j] > self.matrixSimu[i][j - 1]:
                        score -= subtract * ((self.matrixSimu[i][j] - self.matrixSimu[i][j - 1]) / average)
     
        else:
            for i in range(4):
                for j in range(1, 4):
                    if self.matrixSimu[i][j] < self.matrixSimu[i][j - 1]:
                        score -= subtract * ((self.matrixSimu[i][j - 1] - self.matrixSimu[i][j]) / average)
     
        if maxNum['i'] < 2:
            for j in range(4):
                for i in range(1, 4):
                    if self.matrixSimu[i][j] > self.matrixSimu[i - 1][j]:
                        score -= subtract * ((self.matrixSimu[i][j] - self.matrixSimu[i - 1][j]) / average)
       
        else:
            for j in range(4):
                for i in range(1, 4):
                    if self.matrixSimu[i][j] < self.matrixSimu[i - 1][j]:
                        score -= subtract * ((self.matrixSimu[i - 1][j] - self.matrixSimu[i][j]) / average)
        return score

 
    def smoothness(self):
        score = 0  
        plus = 20 
        
        average = 0
        for i in range(4):
            for j in range(4):
                average += self.matrixSimu[i][j]
        average /= 16

    
        for i in range(4):
            for j in range(1, 4):
                if self.matrixSimu[i][j] == self.matrixSimu[i][j - 1]:
                    score += plus * (self.matrixSimu[i][j] / average)
      
        for j in range(4):
            for i in range(1, 4):
                if self.matrixSimu[i][j] == self.matrixSimu[i - 1][j]:
                    score += plus * (self.matrixSimu[i][j] / average)
        return score


    def freeTiles(self):
        score = 0  
        plus = 10  
        
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


if __name__ == '__main__':  
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
