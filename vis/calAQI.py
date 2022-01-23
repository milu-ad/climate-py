import csv
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


# 一次计算一个文件的所有数据
def cal(fileDir):
    with open(fileDir, 'r', encoding='utf-8') as csvfile:
        dt = csv.reader(csvfile)
        row = [rows for rows in dt]
    parentCity = fileDir.split('\\')[5]  # 省级名称
    currCity = fileDir.split('\\')[-1]  # 城市名称

    try:
        os.mkdir(os.getcwd() + '\data\\AQI_level\\' + parentCity)
    except:
        pass
    homedir = (os.getcwd() + '/data/AQI_level/' + parentCity + '/' + currCity).replace('\\', '/')
    csvfile = open(homedir, 'w', newline='', encoding='utf-8')
    writer = csv.writer(csvfile)
    writer.writerow(('date', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'label', 'IAQI_level'))  # 向表中写入title
    # writer.writerow(('date', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'IAQI', 'level','TEMP','RH','PSFC','U','V'))  # 向表中写入title

    for i in range(2, len(row), 2):
        date = row[i][0]
        tPM25 = calIAQI(IAQIS, row[i][1], 'PM25')
        tPM10 = calIAQI(IAQIS, row[i][2], 'PM10')
        tSO2 = calIAQI(IAQIS, row[i][3], 'SO2')
        tNO2 = calIAQI(IAQIS, row[i][4], 'NO2')
        tCO = calIAQI(IAQIS, row[i][5], 'CO')
        tO3 = calIAQI(IAQIS, row[i][6], 'O3')
        tIAQI = max(tPM25, tPM10, tCO, tNO2, tO3, tSO2)  # 选择最大的值
        level = calLevel(tIAQI)

        # content = (date, tPM25, tPM10, tSO2, tNO2, tCO, tO3, tIAQI, level,row[i][9],row[i][10],row[i][11],row[i][7],row[i][8])
        content = (date, tPM25, tPM10, tSO2, tNO2, tCO, tO3, tIAQI, level)
        writer.writerow((content))
    csvfile.close()


def getDir(dir):
    p = Path(dir)
    for p in list(p.glob('*')):
        if p.is_file():  # p: D:\Project\chinaVis2021\数据集\China_new\海南省\屯昌县.csv   如果是一个文件
            fileDir = str(p)
            print(fileDir)
            cal(fileDir)
        else:
            subdir = []
            subdir = getDir(os.path.join(dir, p.name))


# 循环每一个城市的每一个
if __name__ == "__main__":
    # 获取数据并分别写入文件
    dir = os.getcwd() + '\data\\avIAQI_city\\'
    # dir = 'D:/Project/chinaVis2021/数据集/China_new'
    getDir(dir)
