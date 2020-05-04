import types
from random import randint
from EightNum import *

# h1(n) =W(n) “不在位”的将牌数
def AStarWn(self):
    open = []
    close = []
    open.append(self.node)
    nodeSum = 0
    steps = 0

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

# h2(n) = P(n)将牌“不在位”的距离和
def AStarPn(self):
    open = []
    close = []
    open.append(self.node)
    nodeSum = 0
    steps = 0

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
                s.pn = s.getPn(self.endState)
            open.extend(childNode)
            open.sort(key=lambda s: s.pn)
    return None, steps, nodeSum

# h3(n) = h(n)＝P(n)+3S(n)
def AStarSn(self):
    open = []
    close = []
    open.append(self.node)
    nodeSum = 0
    steps = 0

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
                s.hn = s.getPn(self.endState) + 3 * s.getSn(self.endState)
            open.extend(childNode)
            open.sort(key=lambda s: s.hn)
    return None, steps, nodeSum


def getRandomState():
    t = ''
    while len(t) != 9:
        x = str(randint(0,8))
        if t.find(x) == -1:
            t+=x       
    t = t.replace('0',' ')
    t = list(t)
    state = np.array([t[0:3],t[3:6],t[6:9]])
    return state

# 测试数据
def testData():
    test = [
    [['8','2','6'],[' ','4','7'],['5','1','3']],
    [['2',' ','6'],['7','4','1'],['5','8','3']],
    [['8','1','4'],['7','5',' '],['2','3','6']],
    [['2','8','3'],['1','6','4'],['7',' ','5']],
    [['6',' ','4'],['8','5','1'],['7','3','2']]]
    return np.array(test[randint(0,4)])


if __name__ == "__main__":

    startState = testData()
    # startState = getRandomState()
    print(startState)
    print('-----------------')
    endState = np.array([[1, 2, 3], [8, ' ', 4], [7, 6, 5]])

    # h1(n) =W(n) “不在位”的将牌数
    test = EightDigital(startState, endState)
    test.AStarWn = types.MethodType(AStarWn,test)
    path,steps,nodeSum = test.AStarWn()
    print('扩展节点数%d,生成节点数%d' % (steps,nodeSum))
    # for i in path:
    #     for j in i:
    #         print(j)
    #     print('---------------')
    

    # h2(n) = P(n)将牌“不在位”的距离和
    test = EightDigital(startState, endState)
    test.AStarPn = types.MethodType(AStarPn,test)
    path,steps,nodeSum = test.AStarPn()
    print('扩展节点数%d,生成节点数%d' % (steps,nodeSum))
    # for i in path:
    #     for j in i:
    #         print(j)s
    #     print('---------------')
    

    # h3(n) = h(n)＝P(n)+3S(n)
    test = EightDigital(startState, endState)
    test.AStarSn = types.MethodType(AStarSn,test)
    path,steps,nodeSum = test.AStarSn()
    print('扩展节点数%d,生成节点数%d' % (steps,nodeSum))
    # for i in path:
    #     for j in i:
    #         print(j)
    #     print('---------------')
    

