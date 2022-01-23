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
        for i in range(1,len(rows)):
            cur = rows[i][8]
            if i==1:
                old = cur
            if old == cur:
                count += 1
                level_obj[cur] = count
            else:
                # level_obj = partition(level_obj)  # 分区
                # print(level_obj)
                levelLists.append(level_obj)
                count = 1
                old = cur
                level_obj = {}
                level_obj[cur] = count
                # if i == len(rows)-1:
                #     # level_obj = partition(level_obj)   # 分区
                #     levelLists.append(level_obj)
            if i == len(rows) - 1:
                # level_obj = partition(level_obj)   # 分区
                levelLists.append(level_obj)
        #         print('2222',i, fileDir, levelLists)
        # print(fileDir,levelLists)
        f = open('./data/level_combine_ini/' +province+'/'+ city + '.json', 'w', encoding='utf-8')
        f.write(json.dumps(levelLists))
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
    dir = os.getcwd() + '\data\level_combine_ini'
    pathSec = './data/repeatSec_ini'
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




if __name__ == "__main__":
    # 获取数据并分别写入文件
    dir = os.getcwd() + '\data\AQI_city'
    getDir(dir,'level_combine_ini')
    # getLevelData()
    # getSubSequence()
    # partition()


