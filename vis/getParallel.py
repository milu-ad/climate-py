import csv
import json
import os
import os.path
from pathlib import Path

import numpy as np


def parallelLevelDt(filePath):
    provinceName = str(filePath.split('\\')[-1].split('.csv')[0])
    with open(filePath, 'r', encoding='utf-8') as fp:
        dt = csv.reader(fp)
        rows = [row for row in dt]
        # 循环处理每一个文件
        for i in range(1, len(rows)):
            t = {'name': cityNum, 'PM2.5': rows[i][1], 'PM10': rows[i][2], 'SO2': rows[i][3], 'NO2': rows[i][4],
                 'CO': rows[i][5], 'O3': rows[i][6]}
            try:
                res[rows[i][0]].append(t)
            except:
                res[rows[i][0]] = []
                res[rows[i][0]].append(t)
            # res[rows[i][0]].append(t)


# 转换平行坐标的数据
def parallelDt(filePath):
    provinceName = str(filePath.split('\\')[-1].split('.csv')[0])
    with open(filePath, 'r', encoding='utf-8') as fp:
        dt = csv.reader(fp)
        rows = [row for row in dt]
        # 循环处理每一个文件
        for i in range(1, len(rows)):
            t = {'name': provinceName, 'PM2.5': rows[i][1], 'PM10': rows[i][2], 'SO2': rows[i][3], 'NO2': rows[i][4],
                 'CO': rows[i][5], 'O3': rows[i][6]}
            try:
                res[rows[i][0]].append(t)
            except:
                res[rows[i][0]] = []
                res[rows[i][0]].append(t)
            # res[rows[i][0]].append(t)


# 循环数据获取每个省的总数据
def getDir(dir, cityNum):
    p = Path(dir)
    for p in list(p.glob('*')):
        if p.is_file():  # p: D:\Project\chinaVis2021\数据集\China_new\海南省\屯昌县.csv
            fileDir = str(p)

            parallelDt(fileDir)  # 统计用于聚类
            # cityNum += 1
        else:
            subdir = []
            subdir = getDir(os.path.join(dir, p.name), cityNum)


# 计算每个省的各个指标数据的求和
def getProvSum():
    for root, dirs, files in os.walk("D:\\Project\\chinaVis2021\\数据集\\preCluster\\"):
        # 遍历文件
        for d in dirs:
            fdpath = os.path.join(root, d)
            provName = fdpath.split('\\')[-1]  # 省份名称

            lstmp = []
            count = 0
            for root1, dirs1, files1 in os.walk(fdpath):
                # 遍历一个省份下的所有文件
                # print(provName, 111)
                for f1 in files1:
                    count = count + 1
                    fpath = os.path.join(root1, f1)
                    # print(f1)
                    fr = open(fpath, 'r', encoding='utf-8')
                    ls = []  # 其中存放的始终为当前读取的文件的数据
                    for line in fr:  # 将CSV文件当中的二维数据读到列表当中去
                        line = line.replace("\n", "")
                        ls.append(line.split(","))
                    if lstmp:
                        for i in range(1, len(ls)):  # 遍历列表变量
                            if len(ls[i]) != 1:
                                for j in range(1, 7):
                                    lstmp[i][j] = float(lstmp[i][j]) + float(ls[i][j])
                    else:
                        lstmp = list(ls)

            for i in range(1, len(lstmp)):  # 遍历所有行
                if len(lstmp[i]) != 1:
                    for j in range(1, 7):  # 遍历一行的所有数值
                        lstmp[i][j] = float(lstmp[i][j]) / count

            with open('./provSum/' + provName + '.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for index, row in enumerate(lstmp):
                    if index % 2 == 0:
                        writer.writerow(row[0:7])

            fr.close()
            csvfile.close()


# 将一个省的指标数据求和取平均
def getProvMSum():
    for root, dirs, files in os.walk("D:\\Project\\chinaVis2021\\数据集\\preCluster\\"):
        # 遍历文件
        for d in dirs:
            fdpath = os.path.join(root, d)
            provName = fdpath.split('\\')[-1]  # 省份名称

            lstmp = []
            count = 0
            for root1, dirs1, files1 in os.walk(fdpath):
                # 遍历一个省份下的所有文件
                # print(provName, 111)
                for f1 in files1:
                    count = count + 1
                    fpath = os.path.join(root1, f1)
                    # print(f1)
                    fr = open(fpath, 'r', encoding='utf-8')
                    ls = []  # 其中存放的始终为当前读取的文件的数据
                    for line in fr:  # 将CSV文件当中的二维数据读到列表当中去
                        line = line.replace("\n", "")
                        ls.append(line.split(","))
                    if lstmp:
                        for i in range(1, len(ls)):  # 遍历列表变量
                            if len(ls[i]) != 1:
                                for j in range(1, 12):
                                    lstmp[i][j] = float(lstmp[i][j]) + float(ls[i][j])
                    else:
                        lstmp = list(ls)

            for i in range(1, len(lstmp)):  # 遍历所有行
                if len(lstmp[i]) != 1:
                    for j in range(1, 12):  # 遍历一行的所有数值
                        lstmp[i][j] = float(lstmp[i][j]) / count

            with open('./provMSum/' + provName + '.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for index, row in enumerate(lstmp):
                    if index % 2 == 0:
                        writer.writerow(row[0:12])

            fr.close()
            csvfile.close()


# 按照城市顺序转换平行坐标的数据
def parallelSortDt(filePath, prov):
    with open(filePath, 'r', encoding='utf-8') as fp:
        dt = csv.reader(fp)
        rows = [row for row in dt]
        # 循环处理每一个文件
        for i in range(1, len(rows)):
            t = {'name': prov, 'PM2.5': rows[i][1], 'PM10': rows[i][2], 'SO2': rows[i][3], 'NO2': rows[i][4],
                 'CO': rows[i][5], 'O3': rows[i][6]}
            try:
                res[rows[i][0]].append(t)
            except:
                res[rows[i][0]] = []
                res[rows[i][0]].append(t)
            # res[rows[i][0]].append(t)


if __name__ == "__main__":
    res = {}
    cityNum = 0
    # getProvSum()
    # getProvMSum()

    # path = './provSum'
    # getDir(path, cityNum)
    # f = open('provSum/provinceParallel.json', 'w', encoding='utf8')
    # f.write(str(res))
    # f.close()

    # 按照顺序处理城市
    alist = ["北京市", "天津市", "河北省", "山东省", "上海市", "江苏省", "浙江省", "辽宁省", "吉林省", "黑龙江省", "福建省", "广东省", "海南省", "香港特别行政区",
             "台湾省", "山西省", "内蒙古自治区", "河南省", "陕西省", "安徽省", "江西省", "湖北省", "湖南省", "广西壮族自治区", "重庆市", "四川省", "贵州省", "云南省", "西藏自治区", "甘肃省",

             "青海省", "宁夏回族自治区", "新疆维吾尔自治区"]
    for prov in alist:
        path = './provSum/' + prov + '.csv'
        parallelSortDt(path, prov)
        f = open('provSum/provinceParallel.json', 'w', encoding='utf8')
        f.write(str(res))
        f.close()
