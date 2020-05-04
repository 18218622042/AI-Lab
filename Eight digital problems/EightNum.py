import numpy as np


class Node:
    '''
    startState example:
    [['1','2','3'],
     ['4','5','6'],
     ['7',' ','8']]
    '''
    def __init__(self, startState, tag=None, parent=None):
        self.state = startState
        self.tag = tag
        self.parent = parent

    def getPos(self, pos):
        return np.where(self.state == pos)

    # getWn,getPn,getSn可扩展至n数码
    def getWn(self, endState):
        res = 0
        for i in range(3):
            for j in range(3):
                if self.state[i, j] != endState[i, j] and self.state[i, j] != ' ':
                    res += 1
        return res

    def getPn(self, endState):
        res = 0
        for i in range(3):
            for j in range(3):
                tmp = self.state[i, j]
                row, col = np.where(endState == tmp)
                res += abs(i - row) + abs(j - col)
        return res

    def getSn(self, endState):
        res = 0
        tmp = [(0,0),(0,1),(0,2),(1,2),(2,2),(2,1),(2,0),(1,0)]
        for i in range(8):
            t = self.state[tmp[i][0],tmp[i][1]]
            tn = self.state[tmp[(i+1)%8][0],tmp[(i+1)%8][1]]
            if t == ' ':
                continue
            else:
                # x = endState[tmp[(i+1)%8][0],tmp[(i+1)%8][1]]
                x,y = np.where(endState == t)
                n = tmp.index((x[0],y[0])) + 1
                n %= 8
                dn = endState[tmp[n][0],tmp[n][1]]
                if tn != dn:
                    res += 2
        if self.state[1,1] != ' ':
            res += 1
        return res

            

class EightDigital:
    def __init__(self, startState, endState):
        self.node = Node(startState)
        self.endState = endState

    def getDeepth(self):
        tmp = self.node
        res = 0
        while tmp.parent:
            res += 1
            tmp = tmp.parent
        return res

    def getPath(self):
        path = []
        path.append(self.node.state.tolist())
        while self.node.parent:
            self.node = self.node.parent
            path.append(self.node.state.tolist())
        return reversed(path)

    def expand(self):
        row, col = self.node.getPos(' ')
        childNode = []

        if 'Up' != self.node.tag and row > 0:
            childNode.append(self.moveUp(row, col))

        if 'Down' != self.node.tag and row < 2:
            childNode.append(self.moveDown(row, col))

        if 'Left' != self.node.tag and col > 0:
            childNode.append(self.moveLeft(row, col))

        if 'Right' != self.node.tag and col < 2:
            childNode.append(self.moveRight(row, col))

        return childNode

    def moveUp(self, row, col):
        tmp = self.node.state.copy()
        tmp[row, col], tmp[row - 1, col] = tmp[row - 1, col], tmp[row, col]
        child = Node(tmp, 'Down', self.node)
        return child

    def moveDown(self, row, col):
        tmp = self.node.state.copy()
        tmp[row, col], tmp[row + 1, col] = tmp[row + 1, col], tmp[row, col]
        child = Node(tmp, 'Up', self.node)
        return child

    def moveLeft(self, row, col):
        tmp = self.node.state.copy()
        tmp[row, col], tmp[row, col - 1] = tmp[row, col - 1], tmp[row, col]
        child = Node(tmp, 'Right', self.node)
        return child

    def moveRight(self, row, col):
        tmp = self.node.state.copy()
        tmp[row, col], tmp[row, col + 1] = tmp[row, col + 1], tmp[row, col]
        child = Node(tmp, 'Left', self.node)
        return child