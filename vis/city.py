import csv
import json
import os
import os.path
from pathlib import Path

import numpy as np


# 获取数据
def getData(path):
    with open(path, 'r', encoding='utf-8') as fp:
        dt = csv.reader(fp)
        rows = [row for row in dt]
        length = 0
        start = 2
        newStart = 2
        lunshu = 0

        # 一次循环一个城市的所有月份
        for i in range(2013, 2019):
            for j in range(1, 11):
                PM25Tmp = []
                PM10Tmp = []
                SO2Tmp = []
                NO2Tmp = []
                COTmp = []
                O3Tmp = []
                ym = []
                for k in range(0, 3):
                    t = j + k  # 月份顺序 1 2 3
                    if t >= 10:
                        t = str(t)
                    else:
                        t = '0' + str(t)
                    ym.append(str(i) + '-' + str(t))  # 将连续的三个月加入候选数组中 2013-01 2013-12 2013-03

                start = newStart
                first = True
                # len(rows)-1是因为最后有两个空行
                for d in range(start, len(rows), 2):
                    year = rows[d][0].split('-')[0]  # 数据行中的年月
                    month = rows[d][0].split('-')[1]
                    if str(year) + '-' + str(month) in ym:
                        PM25Tmp.append(eval(rows[d][1]))  # 一个市的三个月内的指标的值
                        PM10Tmp.append(eval(rows[d][2]))  # 一个市的三个月内的指标的值
                        SO2Tmp.append(eval(rows[d][3]))  # 一个市的三个月内的指标的值
                        NO2Tmp.append(eval(rows[d][4]))  # 一个市的三个月内的指标的值
                        COTmp.append(eval(rows[d][5]))  # 一个市的三个月内的指标的值
                        O3Tmp.append(eval(rows[d][6]))  # 一个市的三个月内的指标的值
                        if str(year) + '-' + str(month) == ym[1] and first and ym[2].split('-')[1] != '12':  # 当这一轮不是这个今年的最后一轮时，将当前时间内的第二个月的开始值作为下一个轮的开始值
                            newStart = d + 2  # 保存下一轮的开始位置
                            first = False  # 标识是否为第二个月的开始
                        elif ym[2].split('-')[1] == '12':  # 是每年的最后一轮
                            newStart = d + 4
                    else:
                        break
                # print(len(PM25Tmp))
                res['PM25'][lunshu].append(PM25Tmp)
                res['PM10'][lunshu].append(PM10Tmp)
                res['SO2'][lunshu].append(SO2Tmp)
                res['NO2'][lunshu].append(NO2Tmp)
                res['CO'][lunshu].append(COTmp)
                res['O3'][lunshu].append(O3Tmp)
                lunshu += 1


# 将每个市的区县求平均值，每个市每天只保留一条数据
def getAverge(path):
    with open(path, 'r', encoding='utf-8') as fp:
        dt = csv.reader(fp)
        rows = [row for row in dt]
        tmp = '2013-01-01'  # 初始日期
        sum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        number = 0
        mkDir = '\\'.join(path.replace('China_new', 'preCluster').split('\\')[0:-1])
        try:
            os.mkdir(mkDir)
        except:
            print('文件已创建')

        newPath = mkDir + '\\' + path.split('\\')[-1]
        f = open(newPath, 'w', encoding='utf-8')
        writer = csv.writer(f)
        writer.writerow(
            ('date', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'U', 'V', 'TEMP', 'RH', 'PSFC', 'lat', 'lon',
             '国家', '省份', '城市'))

        endIndex = len(rows)
        if rows[len(rows) - 1] == '':
            endIndex = len(rows) - 1

        for i in range(1, endIndex):
            date = rows[i][0]  # 当前日期

            if date == tmp:
                tmpArr = [eval(rows[i][1]), eval(rows[i][2]), eval(rows[i][3]), eval(rows[i][4]), eval(rows[i][5]),
                          eval(rows[i][6]), eval(rows[i][7]), eval(rows[i][8]), eval(rows[i][9]), eval(rows[i][10]),
                          eval(rows[i][11])]
                sum = list(map(lambda x: x[0] + x[1], zip(sum, tmpArr)))  # 所有区县数据求和
                number += 1
                if i == endIndex - 1:  # 如果是最后一条数据
                    sum = np.array(sum)
                    sum /= number
                    resTurple = (tmp,) + tuple(sum) + ('中国', path.split('\\')[5], path.split('\\')[6].split('.')[0])
                    writer.writerow(resTurple)
                    break
            else:
                sum = np.array(sum)
                sum /= number
                resTuple = (tmp,) + tuple(sum) + ('中国', path.split('\\')[5], path.split('\\')[6].split('.')[0])
                writer.writerow(resTuple)

                number = 0
                sum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                tmp = date
                tmpArr = [eval(rows[i][1]), eval(rows[i][2]), eval(rows[i][3]), eval(rows[i][4]), eval(rows[i][5]),
                          eval(rows[i][6]), eval(rows[i][7]), eval(rows[i][8]), eval(rows[i][9]), eval(rows[i][10]),
                          eval(rows[i][11])]
                sum = list(map(lambda x: x[0] + x[1], zip(sum, tmpArr)))

                number += 1

                if i == endIndex - 1:  # 如果是最后一条数据
                    sum = np.array(sum)
                    sum /= number
                    resTurple = (tmp,) + tuple(sum) + ('中国', path.split('\\')[5], path.split('\\')[6].split('.')[0])
                    writer.writerow(resTurple)
                    break
        f.close()


def getDir(dir):
    p = Path(dir)
    for p in list(p.glob('*')):
        if p.is_file():  # p: D:\Project\chinaVis2021\数据集\China_new\海南省\屯昌县.csv
            fileDir = str(p)
            # print('\\'.join(fileDir.split('\\')[5:]))
            # getAverge(fileDir)  # 取数据均值   使用China_new路径
            getData(fileDir)  # 统计用于聚类
        else:
            subdir = []
            subdir = getDir(os.path.join(dir, p.name))
    # return res


# 获取目标数据
def getDesData():
    f = open('./data/CO-cluster.json', 'r', encoding='utf-8')
    dt = json.load(f)
    return dt['CO'][0]
    # print(len(dt['CO'][0]))


if __name__ == "__main__":
    # 存储所有数据的字典
    metrics = ['PM25', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    res = {
        'PM25': [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                 [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                 [], [], [], [], [], [], [], []],
        'PM10': [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                 [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                 [], [], [], [], [], [], [], []],
        'SO2': [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                [], [], [], [], [], [], [], []],
        'NO2': [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                [], [], [], [], [], [], [], [], [], []],
        'CO': [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
               [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
               [], [], [], [], [], [], [], []],
        'O3': [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
               [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
               [], [], [], [], [], [], [], []]}

    # 获取数据并分别写入文件
    # dir = 'D:/Project/chinaVis2021/数据集/China_new'
    dir = 'D:/Project/chinaVis2021/数据集/preCluster'
    getDir(dir)

    for i in metrics:
        f = open('./cluster/data/' + i + '-cluster.json', 'w', encoding='utf8')
        f.write(json.dumps({i: res[i]}))
        f.close()


    metricsRes = ['PM25', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    # 循环所有指标的文件
    for i in range(len(metricsRes)):
        with open('./cluster/data/' + metricsRes[i] + '-cluster.json', 'r', encoding='utf-8') as f:  # 读取用于聚类的指标文件
            dt = json.load(f)

            # 循环60组时间段
            for j in range(0, len(dt[metricsRes[i]])):
                for k in range(0, len(dt[metricsRes[i]][j])):
                    print(metricsRes[i],j,len(dt[metricsRes[i]][j]), len(dt[metricsRes[i]][j][k]))
