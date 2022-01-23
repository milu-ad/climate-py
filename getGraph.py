class Vertext():  # 包含了顶点信息,以及顶点连接边

    def __init__(self, key):  # key表示是添加的顶点的索引
        self.id = key
        self.connectedTo = {}  # 初始化临接列表

    def addNeighbor(self, nbr, weight=0):  # 这个是赋值权重的函数
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):  # 得到这个顶点所连接的其他的所有的顶点 (keys类型是class)
        return self.connectedTo.keys()

    def getId(self):  # 返回自己的key
        return self.id

    def getWeight(self, nbr):  # 返回所连接ner顶点的权重是多少
        return self.connectedTo[nbr]


'''
Graph包含了所有的顶点
包含了一个主表(临接列表)
'''


class Graph():  # 图 => 由顶点所构成的图

    '''
    存储图的方式是用邻接表实现的.
    数据结构: {
                key:Vertext(){
                    self.id = key
                    self.connectedTo{
                        相邻节点类实例 : 权重
                        ..
                        ..
                    }
                }
                ..
                ..
        }
    '''

    def __init__(self):
        self.vertList = {}  # 临接列表
        self.numVertices = 0  # 顶点个数初始化
        self.nodeLists = []  # 所有节点值

    def addVertex(self, key):  # 添加顶点
        self.numVertices = self.numVertices + 1  # 顶点个数累加
        self.nodeLists.append(key)
        keyId = self.nodeLists.index(key)

        newVertex = Vertext(keyId)  # 创建一个顶点的临接矩阵

        self.vertList[keyId] = newVertex
        # print('neibor',key,self.vertList[key],'2123131',newVertex)  # neibor 0 0 connectedTo: [] 2123131 0 connectedTo: []
        print('vertList', self.vertList)
        return newVertex

    def getVertex(self, n):  # 通过key查找定点
        if n in self.nodeLists:
            return self.vertList[self.nodeLists.index(n)]
        else:
            return None

    def __contains__(self, n):  # transition:包含 => 返回所查询顶点是否存在于图中
        # print( 6 in g)
        return n in self.nodeLists

    def addEdge(self, f, t, cost=1):  # 添加一条边.
        print('f', f, 't', t)

        if f not in self.nodeLists:  # 如果没有边,就创建一条边
            nv = self.addVertex(f)
        if t not in self.nodeLists:  # 如果没有边,就创建一条边
            nv = self.addVertex(t)
        else:
            f_id = self.nodeLists.index(f)
            t_id = self.nodeLists.index(t)
            for w in self.vertList[f_id].getConnections():
                # if self.nodeLists[w.getId()] == t:
                if w.getId() == t_id:
                    cost += self.vertList[f_id].getWeight(w)
                    # print('w',w,self.vertList[f].getWeight(w),cost)
        f_id = self.nodeLists.index(f)
        t_id = self.nodeLists.index(t)

        self.vertList[f_id].addNeighbor(self.vertList[t_id], cost)  # cost是权重

    def getVertices(self):  # 返回图中所有的定点
        # return self.vertList.keys()
        return self.nodeLists

    def getVerticeIndex(self):  # 返回图中所有的定点索引
        return self.vertList.keys()

    def __iter__(self):  # return => 把顶点一个一个的迭代取出.
        return iter(self.vertList.values())


#
# -------------------------------------------------
# 以下是测试数据.可删除
# -------------------------------------------------
#
g = Graph()

# for i in range(6):
#     g.addVertex(i)
# print(g.vertList)

'''
# a = g.vertList[0]
# print(a.connectedTo)
'''

g.addEdge({'a': 1}, {'b': 3})
g.addEdge({'a': 1}, {'b': 3})
g.addEdge({'a': 1}, {'b': 3})
g.addEdge(4, 5)
g.addEdge(4, 5)
g.addEdge(0, 5, 1)
g.addEdge(1, 2, 1)
g.addEdge(2, 3, 1)
g.addEdge(3, 4, 1)
# g.addEdge(2,3,9)
# g.addEdge(3,4,7)
# g.addEdge(3,5,3)
# g.addEdge(4,0,1)
# g.addEdge(5,4,8)
# g.addEdge(5,2,1)

print('g', g.getVertices())
# vertList = { key :VertextObject}
# VertextObject =  ||key = key, connectedTo = {到达节点:权重}||   => |||| 表示的是权重的意思

# print(g.nodeLists)
for v in g:  # 循环类实例 => return ->  g = VertextObject的集合  v = VertextObject
    for w in v.getConnections():  # 获得类实例的connectedTO
        # print(w)
        print("({},{}:{})".format(g.nodeLists[v.getId()], g.nodeLists[w.getId()],
                                  v.getWeight(w)))  ## 为什么会是这样 => 因为这个时候v就是class啊



