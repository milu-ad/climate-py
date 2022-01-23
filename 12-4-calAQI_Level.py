import csv,json
import os
from pathlib import Path

IAQIS = {'SO2': [[0, 50, 150, 475, 800, 1600, 2100, 2620], [0, 150, 500, 650, 800, 1600, 2100, 2620]],
         'NO2': [[0, 40, 80, 180, 280, 565, 750, 940], [0, 100, 200, 700, 1200, 2340, 3090, 3840]],
         'PM10': [[0, 50, 150, 250, 350, 420, 500, 600]],
         'CO': [[0, 2, 4, 14, 24, 36, 48, 60], [0, 5, 10, 35, 60, 90, 120, 150]],
         'O3': [[0, 100, 160, 215, 265, 800, 1000, 1200], [0, 160, 200, 300, 400, 800, 1000, 1200]],
         'PM25': [[0, 35, 75, 115, 150, 250, 350, 500]],
         'IAQI': [[0, 50, 100, 150, 200, 300, 400, 500]]}


def cal_linear(iaqi_lo, iaqi_hi, bp_lo, bp_hi, cp):
    # 线性缩放
    iaqi = (iaqi_hi - iaqi_lo) * (cp - bp_lo) / (bp_hi - bp_lo) + iaqi_lo
    return iaqi


def calIAQI(lists, pm_val, zhibiao):
    refer = lists['IAQI'][0]
    p = lists[zhibiao][0]
    for i in range(0, len(p) - 1):
        if p[i] <= float(pm_val) < p[i + 1]:
            iaqi = cal_linear(refer[i], refer[i + 1], p[i], p[i + 1], float(pm_val))
            return iaqi
    return -99


def calLevel(aqi):
    level = []
    if 0 <= aqi < 51:
        level = 1
    if 51 <= aqi < 101:
        level = 2
    if 101 <= aqi < 151:
        level = 3
    if 151 <= aqi < 201:
        level = 4
    if 201 <= aqi < 300:
        level = 5
    if aqi > 300:
        level = 6
    return level


# 存储所有数据--level
def cal(fileDir):
    with open(fileDir, 'r', encoding='utf-8') as csvfile:
        dt = csv.reader(csvfile)
        row = [rows for rows in dt]
    parentCity = fileDir.split('\\')[5]  # 省级名称
    currCity = fileDir.split('\\')[-1].split('.csv')[0]  # 城市名称
    try:
        os.mkdir(os.getcwd() + '\data\\AQI_level\\' + parentCity)
    except:
        pass
    # homedir = (os.getcwd() + '/data/AQI_level/' + parentCity + '/' + currCity).replace('\\', '/')

    f = open(os.getcwd() + '/data/AQI_level/' + parentCity + '/' + currCity + '.json', 'w', encoding='utf-8')
    res = []
    ress = {}
    for i in range(1, len(row)):
        # date = row[i][0]
        # level_PM25 = calLevel(row[i][1])
        # level_PM10 = calLevel(row[i][2])
        # level_SO2 = calLevel(row[i][3])
        # level_NO2 = calLevel(row[i][4])
        # level_CO = calLevel(row[i][5])
        # level_O3 = calLevel(row[i][6])
        day_info = {}
        dt = [float(row[i][j]) for j in range(1,7)]
        # label = dt.index(max(dt))
        # level = row[i][7]


        # day_info['date'] = row[i][0]
        day_info['level_PM25'] = calLevel(float(row[i][1]))
        day_info['level_PM10'] = calLevel(float(row[i][2]))
        day_info['level_SO2'] = calLevel(float(row[i][3]))
        day_info['level_NO2'] = calLevel(float(row[i][4]))
        day_info['level_CO'] = calLevel(float(row[i][5]))
        day_info['level_O3'] = calLevel(float(row[i][6]))
        day_info['label'] = row[0][dt.index(max(dt))+1]
        day_info['level'] = int(row[i][8])
        ress[row[i][0]] = day_info
        # print(ress)
        # print(row[i][0],max(dt),dt.index(max(dt)),row[0])

        # res.append(day_info)
    f.write(json.dumps(ress))
    f.close()


# 存储所有数据--value
def AQIJson(fileDir):
    with open(fileDir, 'r', encoding='utf-8') as csvfile:
        dt = csv.reader(csvfile)
        row = [rows for rows in dt]
    parentCity = fileDir.split('\\')[5]  # 省级名称
    currCity = fileDir.split('\\')[-1].split('.csv')[0]  # 城市名称
    try:
        os.mkdir(os.getcwd() + '\data\\AQI_value\\' + parentCity)
    except:
        pass

    f = open(os.getcwd() + '/data/AQI_value/' + parentCity + '/' + currCity + '.json', 'w', encoding='utf-8')
    ress = {}
    for i in range(1, len(row)):
        day_info = {}
        dt = [float(row[i][j]) for j in range(1,7)]
        # day_info['date'] = row[i][0]
        day_info['level_PM25'] = float(row[i][1])
        day_info['level_PM10'] = float(row[i][2])
        day_info['level_SO2'] = float(row[i][3])
        day_info['level_NO2'] = float(row[i][4])
        day_info['level_CO'] = float(row[i][5])
        day_info['level_O3'] = float(row[i][6])
        day_info['label'] = row[0][dt.index(max(dt))+1]
        day_info['level'] = int(row[i][8])
        ress[row[i][0]] = day_info
        # print(ress)

    f.write(json.dumps(ress))
    f.close()




def getDir(dir):
    p = Path(dir)
    for p in list(p.glob('*')):
        if p.is_file():  # p: D:\Project\chinaVis2021\数据集\China_new\海南省\屯昌县.csv   如果是一个文件
            fileDir = str(p)
            print(fileDir)
            # cal(fileDir)
            AQIJson(fileDir)
        else:
            subdir = []
            subdir = getDir(os.path.join(dir, p.name))


# 循环每一个城市的每一个
if __name__ == "__main__":
    # 获取数据并分别写入文件
    dir = os.getcwd() + '\data\\AQI_city\\'
    # dir = 'D:/Project/chinaVis2021/数据集/China_new'
    getDir(dir)
