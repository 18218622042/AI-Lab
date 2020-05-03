import numpy as np


class Node:
    '''
    startState example:
    [['1','2','3'],
     ['4','5','6'],
     ['7',' ','8']]
    '''
    def __init__(self, startState, tag = None, parent = None):
        self.state = startState
        self.tag = tag
        self.parent = parent

    def getPos(self):
        return np.where(self.state == ' ')
        
    def getWn(self, endState):
        res = 0
        for i in range(3):
            for j in range(3):
                if self.state[i, j] != endState[i, j] and self.state[i,j] != ' ':
                    res += 1
        return res


class EightDigital:
    def __init__(self, startState, endState):
        self.node = Node(startState)
        self.endState = endState

    def run(self):
        open = []
        close = []
        open.append(self.node)
        nodeSum = 0
        steps = 1

        while open:
            self.node = open.pop(0)
            if (self.node.state == self.endState).all():
                return self.getPath(), steps, nodeSum
            else:
                close.append(self.node)
                childNode = self.expand()
                nodeSum += len(childNode)
                steps += 1
                for s in childNode:
                    s.fn = self.getDeepth() + 1 + s.getWn(self.endState)
                open.extend(childNode)
                open.sort(key=lambda s: s.fn)
        return None, steps, nodeSum

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
        return path

    def expand(self):
        row, col = self.node.getPos()
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


if __name__ == "__main__":
    startState = np.array([[2, 8, 3], [1, 6, 4], [7, ' ', 5]])
    endState = np.array([[1, 2, 3], [8, ' ', 4], [7, 6, 5]])
    test = EightDigital(startState, endState)
    path,steps,nodeSum = test.run()
    for i in path:
        for j in i:
            print(j)
        print('---------------')
    print(steps,nodeSum)