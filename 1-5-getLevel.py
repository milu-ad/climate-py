import csv
import os,json
from pathlib import Path

# ['date', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'IAQI', 'level']

# 1 从csv中获取数据
# csv中获取包含level的数据
def getDir(dir,subDir):
    list = os.listdir(dir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(dir, list[i])
        for root, dirs, files in os.walk(path):
            # 数据分别是 D:\PycharmProjects\climate\data\AQI_city\上海市 [] ['上海市.csv']
            province = root.split('\\')[-1]
            dir_province = './data/'+subDir+'/'+province  # 文件夹路径--省份
            isExists = os.path.exists(dir_province)
            if not isExists:
                os.makedirs(dir_province)
            for file in files:
                dir_file = root+'\\'+file
                getJson(dir_file,province)
        #         break
        #     break
        # break

# 2、合并相邻天数出现同等级的数据 存储为 level_combine_ini
# 按照划分，将同一区间的数值调整为区间最大值  存储为 level_combine
# 合并相同等级数据，csv-json存储
def getJson(fileDir,province):
    with open(fileDir, 'r', encoding='utf-8') as csvfile:
        city = fileDir.split('\\')[-1].split('.')[0]
        dt = csv.reader(csvfile)
        rows = [row for row in dt]
        levelLists =[]
        count = 0
        level_obj = {}
        level_sec = []
        for i in range(1,len(rows)):
            cur = rows[i][8]
            if i==1:
                old = cur
                level_sec.append(cur)

            if old == cur:
                count += 1
                level_obj[cur] = count
            else:
                level_obj = partition(level_obj)  # 分区
                # print(level_obj)
                levelLists.append(level_obj)
                count = 1
                old = cur
                level_sec.append(cur)
                level_obj = {}
                level_obj[cur] = count
                if i == len(rows)-1:
                    level_obj = partition(level_obj)   # 分区
                    levelLists.append(level_obj)

        # f = open('./data/level_combine/' +province+'/'+ city + '.json', 'w', encoding='utf-8')
        # f.write(json.dumps(levelLists))
        # f.close()
        f = open('./data/level_record/' +province+'/'+ city + '.json', 'w', encoding='utf-8')
        f.write(json.dumps(level_sec))
        f.close()
    pass

# 3、按照划分，将同一区间的数值调整为区间最大值  存储为 level_combine
# 区间划分,将连续2天与仅有1天的数据合并为出现1-2天的情况，数值为2
def parts():
    dir = os.getcwd() + '\data\level_combine_ini'
    pathMerge = './data/level_combine'
    lists = os.listdir(dir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(lists)):
        path = os.path.join(dir, lists[i])
        for root, dirs, files in os.walk(path):
            province = root.split('\\')[-1]
            dir_province = pathMerge + '/' + province  # 文件夹路径--省份
            isExists = os.path.exists(dir_province)
            if not isExists:
                os.makedirs(dir_province)
            for file in files:
                city = file.split('.')[0]
                dir_file = root + '\\' + file
                with open(dir_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    res = []
                    for item in data:
                        obj = {}
                        for k,v in item.items():
                            if v < 3:
                                obj[k] = 2
                            elif v < 5:
                                obj[k] = 4
                            elif v < 7:
                                obj[k] = 6
                            elif v < 10:
                                obj[k] = 9
                            elif v < 16:
                                obj[k] = 15
                            elif v < 21:
                                obj[k] = 20
                            elif v < 31:
                                obj[k] = 30
                            elif v < 41:
                                obj[k] = 40
                            elif v < 61:
                                obj[k] = 60
                            elif v < 81:
                                obj[k] = 80
                            elif v < 101:
                                obj[k] = 100
                            elif v < 201:
                                obj[k] = 200
                            elif v < 301:
                                obj[k] = 300
                            elif v < 401:
                                obj[k] = 400
                            else:
                                obj[k] = 500
                        res.append(obj)
                    # f = open(pathMerge + '/' + province + '/' + city + '.json', 'w', encoding='utf-8')
                    # f.write(json.dumps(res))
                    # f.close()

                    # merge_obj = {}
                    # res_list = []
                    # count = 0
                    # for i in range(0,len(res)):
                    #     for k,v in res[i].items():
                    #         cur = v
                    #         if i==1:
                    #             old = cur
                    #         if old == cur:
                    #             count+=1
                    #             merge_obj[cur] = count
    pass


def partition(level_obj):
    key = list(level_obj.keys())[0]
    cur = list(level_obj.values())[0]
    obj = {}
    if cur < 3:
        obj[key] = 2
    elif cur < 5:
        obj[key] = 4
    elif cur < 7:
        obj[key] = 6
    elif cur < 10:
        obj[key] = 9
    elif cur < 16:
        obj[key] = 15
    elif cur < 21:
        obj[key] = 20
    elif cur < 31:
        obj[key] = 30
    elif cur < 41:
        obj[key] = 40
    elif cur < 61:
        obj[key] = 60
    elif cur < 81:
        obj[key] = 80
    elif cur < 101:
        obj[key] = 100
    elif cur < 201:
        obj[key] = 200
    elif cur < 301:
        obj[key] = 300
    elif cur < 401:
        obj[key] = 400
    else:
        obj[key] = 500
    return obj
    pass

# 此步为获取连续N天出现同一等级的频次，据此进行区间划分  all.json
# 获取连续同等级天数分别出现的次数
def getLevelData():
    dir = os.getcwd() + '\data\level_combine_ini'
    lists = os.listdir(dir)  # 列出文件夹下所有的目录与文件
    # ress={}
    # count_list=[]
    res = {}

    for i in range(0, len(lists)):
        path = os.path.join(dir, lists[i])
        for root, dirs, files in os.walk(path):
            for file in files:
                ress = {}
                count_list = []
                dir_file = root + '\\' + file
                with open(dir_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for obj in data:
                        values = list(obj.values())[0]  # [[1],[2],[3]]
                        print(values)
                        if values not in count_list:
                            count_list.append(values)
                            ress[values] = 1
                        else:
                            ress[values] = ress[values] + 1
                            # if ress[values]<20:
                            #     ress[values] = ress[values] + 1
                            # else:
                            #     ress[values] =20
                res[file] = ress
    # f = open('./data/level_combine/all.json', 'w', encoding='utf-8')
    # f.write(json.dumps(res))
    # f.close()
    print(res) # 连续同等级天数分别出现的次数

# 4、获取重复子序列
# 获取重复子序列的序列值、出现索引以及出现次数
def getRepeatSec(arr):
    subStr = []
    lens = len(arr)
    len_store = {}
    frequences = []
    for j in range(2, lens):
        for i in range(0, lens - j + 1):
            keySeq = [arr[i] for i in range(i, i + j)]
            count = 1
            if keySeq not in subStr:
                subStr.append(keySeq)
                len_store[j] = []
                len_store[j].append(keySeq)
                content = []
                indexs = []
                content.append(keySeq)
                indexs.append(i)
                # 剩余的子序列中查找key序列出现频次
                for k in range(i + j, len(arr[i + j:]) + 1):
                    if arr[k:k + j] == keySeq:
                        indexs.append(k)
                        count = count + 1
                content.append(indexs)
                content.append(count)
                # frequences.append(content)
                if count < 2:
                    continue
                else:
                    frequences.append(content)
        print(j)
    return frequences

# 4、获取重复子序列    存储为 repeatSec
def getSubSequence():
    dir = os.getcwd() + '\data\level_combine'
    pathSec = './data/repeatSec'
    lists = os.listdir(dir)  # 列出文件夹下所有的目录与文件

    for i in range(0, len(lists)):
        path = os.path.join(dir, lists[i])
        for root, dirs, files in os.walk(path):
            province = root.split('\\')[-1]

            dir_province = pathSec + '/' + province  # 文件夹路径--省份
            isExists = os.path.exists(dir_province)
            if not isExists:
                os.makedirs(dir_province)
            for file in files:
                city = file.split('.')[0]

                dir_file = root + '\\' + file
                with open(dir_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    secList = getRepeatSec(data)
                    f = open(pathSec +  '/' + province + '/' + city + '.json', 'w', encoding='utf-8')
                    f.write(json.dumps(secList))
                    # f.write('23')
                    f.close()
                # break
            # break
        # break
    pass

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

    def getId(self):  # 返回自己的key, 此处为节点在nodelist中的索引
        return self.id

    def getWeight(self, nbr):  # 返回所连接ner顶点的权重是多少
        return self.connectedTo[nbr]


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
        self.nodeLists = []  # 所有节点值set() 【{}，{}】

        self.nodeSet = []  # 缺少最后一个节点信息，新增一条边进写入一个source节点
        self.groupName = []
        self.totalNodes = {}  #{"2_5": ["2_5_1"]}
        self.links = []

    def addVertex(self, key):  # 添加顶点
        self.numVertices = self.numVertices + 1  # 顶点个数累加
        self.nodeLists.append(key)
        keyId = self.nodeLists.index(key)
        newVertex = Vertext(keyId)  # 创建一个顶点的临接矩阵

        self.vertList[keyId] = newVertex
        # print('neibor',key,self.vertList[key],'2123131',newVertex)  # neibor 0 0 connectedTo: [] 2123131 0 connectedTo: []
        return newVertex

    def getVertex(self, n):  # 通过key查找定点
        if n in self.nodeLists:
            # get {'3': 1} 1 connectedTo: [2, 3, 4, 6, 5, 0, 9, 11, 18, 20, 19, 13, 8, 12, 28, 22, 31, 10, 14, 17]
            # print('get',n,self.vertList[self.nodeLists.index(n)])
            return self.vertList[self.nodeLists.index(n)]
        else:
            return None

    def __contains__(self, n):  # transition:包含 => 返回所查询顶点是否存在于图中
        # print( 6 in g)
        return n in self.nodeLists


    def addEdge(self, f, t, flag, cost=1):  # 添加一条边.
        s_key = str(list(f.keys())[0])
        s_value = str(list(f.values())[0])
        s_groupname = s_key + '_' + s_value  # 节点的分组名
        t_groupname = str(list(t.keys())[0]) + '_' + str(list(t.values())[0])
        if f not in self.nodeLists:  # 如果没有边,就创建一条边
            nv = self.addVertex(f)
        if t not in self.nodeLists:  # 如果没有边,就创建一条边
            nv = self.addVertex(t)
        if f not in self.nodeSet:
            self.nodeSet.append(f)
            self.groupName.append(s_groupname)
            self.totalNodes[s_groupname] = [s_groupname + '_' + str(1)]
        else:
            preIndex = len(self.totalNodes[s_groupname])  # 当前group中包含的节点个数
            self.groupName.append(s_groupname)
            self.totalNodes[s_groupname].append(s_groupname + '_' + str(preIndex+1))

            f_id = self.nodeLists.index(f)
            t_id = self.nodeLists.index(t)

            for w in self.vertList[f_id].getConnections():
                # if self.nodeLists[w.getId()] == t:
                if w.getId() == t_id:
                    cost += self.vertList[f_id].getWeight(w)

        f_id = self.nodeLists.index(f)
        t_id = self.nodeLists.index(t)

        if flag:
            if t not in self.nodeSet:
                self.nodeSet.append(t)
                self.groupName.append(t_groupname)
                self.totalNodes[t_groupname] = [t_groupname + '_' + str(1)]

            else:
                pre_index_t = len(self.totalNodes[t_groupname])  # 当前group中包含的节点个数
                self.groupName.append(t_groupname)
                self.totalNodes[t_groupname].append(t_groupname + '_' + str(pre_index_t+1))


        self.vertList[f_id].addNeighbor(self.vertList[t_id], cost)  # cost是权重


    def getVertices(self):  # 返回图中所有的定点
        # return self.vertList.keys()
        return self.nodeLists

    def getVerticeIndex(self):  # 返回图中所有的定点索引
        return self.vertList.keys()

    def __iter__(self):  # return => 把顶点一个一个的迭代取出.
        return iter(self.vertList.values())

def getLink(f,t,cost):
    link_tmp, source_tmp, target_tmp = {}, {"name": "", "group": "", "value": 1}, {"name": "", "group": "", "value": 1}
    s_key = str(list(f.keys())[0])
    t_key = str(list(t.keys())[0])
    s_value = str(list(f.values())[0])
    t_value = str(list(t.values())[0])
    s_groupName = s_key + '_' + s_value  # 节点的分组名
    t_groupName = t_key + '_' + t_value  # 节点的分组名

    source_tmp['group'] = s_groupName
    source_tmp['name'] = s_groupName + '_' + str(cost)
    source_tmp['value'] = 1

    target_tmp['group'] = t_groupName
    target_tmp['name'] = t_groupName + '_' + str(cost)
    target_tmp['value'] = 1

    link_tmp['source'] = source_tmp
    link_tmp['target'] = target_tmp
    pass

def getGrapg():
    dir = os.getcwd() + '\data\level_combine_ini'
    lists = os.listdir(dir)  # 列出文件夹下所有的目录与文件
    chartDtPath_ini = os.getcwd() + '\data\chartData_before_merge'
    chartDtPath_m = os.getcwd() + '\data\chartData_merge'
    chartDtPath = os.getcwd() + '\data\chartDataIni'
    chartDtPathDir = os.getcwd() + '\data\chartDataDir'

    for i in range(0, len(lists)):
        path = os.path.join(dir, lists[i])
        for root, dirs, files in os.walk(path):
            province = root.split('\\')[-1]
            dir_province = chartDtPathDir + '/' + province
            isExists = os.path.exists(dir_province)
            if not isExists:
                os.makedirs(dir_province)

            # p =0
            for file in files:
                g = Graph()
                city = file.split('.')[0]
                res = []
                sequenceRecord = {}
                nodes = []
                links = []
                graph_date = {'nodes':[],'links':[]}
                fg = False  # 标识最后一条数据

                dir_file = root + '\\' + file
                with open(dir_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for j in range(0, len(data) - 1):
                        if j == len(data) - 2:
                            fg = True
                        g.addEdge(data[j], data[j + 1],fg)
                        # if j == len(data)-2:
                        #     print("out",j)
                        #     t_groupname = str(list(data[j + 1].keys())[0]) + '_' + str(list(data[j + 1].values())[0])
                        #     if data[j+1] not in g.nodeSet:
                        #         g.nodeSet.append(data[j + 1])
                        #         g.groupName.append(t_groupname)
                        #         g.totalNodes[t_groupname] = [t_groupname + '_' + str(1)]


                # print(g.getVertices() ) # 原始序列
                # print(g.getVertex(g.getVertices()[0])) #  0 connectedTo: [2, 17]
                # print('t',file,g.nodeLists)
                print('ini',file,g.totalNodes)

                for group,nodeList in g.totalNodes.items():
                    for item in nodeList:
                        obj = {'group': group, 'name': item}
                        nodes.append(obj)
                # print(nodes)
                count = 0
                for v in g:  # 循环类实例 => return ->  g = VertextObject的集合  v = VertextObject
                    count+=1
                    # print(count,v.getId(),g.nodeLists[v.getId()])  # {'2': 5}
                    nodeCount = 0
                    curNode = g.getVertices()[v.getId()]  # v {'2': 5}
                    nodeLength = len(g.nodeLists)
                    nextNode = (v.getId() < nodeLength - 1) and (g.getVertices()[v.getId() + 1])

                    for w in v.getConnections():  # 获得类实例的connectedTO
                        s_key = str(list(g.nodeLists[v.getId()].keys())[0])
                        t_key = str(list(g.nodeLists[w.getId()].keys())[0])
                        s_value = str(list(g.nodeLists[v.getId()].values())[0])
                        t_value = str(list(g.nodeLists[w.getId()].values())[0])
                        s_groupName = s_key + '_' + s_value  # 节点的分组名
                        t_groupName = t_key + '_' + t_value  # 节点的分组名
                        r_key = s_groupName + '*' + t_groupName
                        pre_count = nodeCount
                        nodeCount += v.getWeight(w)  # 合并获取当前group共多少节点
                        # print(pre_count,nodeCount,r_key,groupName,v.getWeight(w))
                        # print('r_key',r_key,g.totalNodes[s_groupName],g.totalNodes[t_groupName],v.getWeight(w))
                        if r_key not in sequenceRecord.keys():
                            reverse_key = t_key + '_' + t_value + '*' + s_key + '_' + s_value
                            if reverse_key in sequenceRecord.keys():
                                sequenceRecord[reverse_key].append(v.getWeight(w))
                                for index_t in range(0, v.getWeight(w)):
                                    link_tmp = {}
                                    source_tmp = {'group': s_groupName,
                                                  'name': g.totalNodes[s_groupName][index_t + pre_count], 'value': 1}
                                    target_tmp = {'group': t_groupName, 'name': g.totalNodes[t_groupName][index_t],
                                                  'value': 1}
                                    link_tmp['source'] = target_tmp
                                    link_tmp['target'] = source_tmp
                                    link_tmp['value'] = 1
                                    link_tmp['direction'] = 't_s'
                                    links.append(link_tmp)
                            else:
                                sequenceRecord[r_key] = [v.getWeight(w)]
                                # print(sequenceRecord[r_key])
                                for index_t in range(0, v.getWeight(w)):
                                    # print(t_groupName, v.getWeight(w),index_t,g.totalNodes[t_groupName])

                                    link_tmp = {}
                                    source_tmp = {'group': s_groupName,
                                                  'name': g.totalNodes[s_groupName][index_t + pre_count], 'value': 1}
                                    target_tmp = {'group': t_groupName, 'name': g.totalNodes[t_groupName][index_t],
                                                  'value': 1}
                                    link_tmp['source'] = source_tmp
                                    link_tmp['target'] = target_tmp
                                    link_tmp['value'] = 1
                                    link_tmp['direction'] = 's_t'
                                    links.append(link_tmp)
                    # print(links)

                        # tmp = []
                        # tmp.append([curNode, nextNode])
                        # tmp.append(v.getWeight(w))
                        # res.append(tmp)  # 相邻序列权重
                        # # print("({},{},weight:{})".format(g.nodeLists[v.getId()], g.nodeLists[w.getId()], v.getWeight(w)))
                        #

                graph_date['nodes'] = nodes
                graph_date['links'] = links
                #

                # print(graph_date)
                # 方向数据写入link
                f4 = open(chartDtPathDir + '/' + province + '/' + city + '.json', 'w', encoding='utf-8')
                f4.write(json.dumps(graph_date))
                f4.close()


                # f3 = open(chartDtPath + '/' + province + '/' + city + '.json', 'w', encoding='utf-8')
                # f3.write(json.dumps(graph_date))
                # f3.close()

                # f1 = open(chartDtPath_ini + '/' + province + '/' + city + '.json', 'w', encoding='utf-8')
                # f1.write(json.dumps(res))
                # f1.close()
                #
                # f2 = open(chartDtPath_ + '/' + province + '/' + city + '.json', 'w', encoding='utf-8')
                # f2.write(json.dumps(sequenceRecord))
                # f2.close()
                # print(sequenceRecord)
        #         break
        #     break
        # break


if __name__ == "__main__":
    # 获取数据并分别写入文件
    dir = os.getcwd() + '\data\AQI_city'
    # getDir(dir,'level_record')
    # getLevelData()
    getGrapg()
    # partition()


