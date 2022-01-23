import csv
import pandas as pd
import xlwt  # 导入模块
import os

# with open(path, 'r', encoding='utf-8') as f:
#     reader = csv.reader(f, delimiter=';')
#     for row in reader:
#         # PM25 = f[0]
#         print(row[0])

path = 'D:/Project/chinaVis2021/数据集/aday/'
# path = 'D:/Project/chinaVis2021/数据集/aday/' + '201301/CN-Reanalysis-daily-2013010100.csv'

# dt = pd.read_csv(path)
# print(dt.head())

#
# def cal(path):
#     pass


path = 'D:/Project/chinaVis2021/数据集/aday/'
startYear = 2013
startMonth = '01'
startDay = '0100'

# IAQIS = {'SO2': {[0, 50, 150, 475, 800, 1600, 2100, 2620], [0, 150, 500, 650, 800, 1600, 2100, 2620]},
#          'NO2': {[0, 40, 80, 180, 280, 565, 750, 940], [0, 100, 200, 700, 1200, 2340, 3090, 3840]},
#          'PM10': {[0, 50, 150, 250, 350, 420, 500, 600]},
#          'CO': {[0, 2, 4, 14, 24, 36, 48, 60], [0, 5, 10, 35, 60, 90, 120, 150]},
#          'O3': {[0, 100, 160, 215, 265, 800, 1000, 1200], [0, 160, 200, 300, 400, 800, 1000, 1200]},
#          'PM25': {[0, 35, 75, 115, 150, 250, 350, 500]},
#          'IAQI': {[0, 50, 100, 150, 200, 300, 400, 500]}}

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
            # print(i, pm_val)
            iaqi = cal_linear(refer[i], refer[i + 1], p[i], p[i + 1], float(pm_val))
            # print(iaqi)
            return iaqi
    return -99


# calIAQI(IAQIS, 185, 'PM10')

# 一次计算一个文件的所有数据
def cal(filename):
    with open(path + filename, 'r', encoding='utf-8') as csvfile:
        dt = csv.reader(csvfile)
        row = [rows for rows in dt]
    # print(dt.head())
    # PM25 = dt['PM2.5(微克每立方米)']
    # PM10 = dt['PM10(微克每立方米)']
    # SO2 = dt['SO2(微克每立方米)']
    # NO2 = dt['NO2(微克每立方米)']
    # CO = dt['CO(豪克每立方米)']
    # O3 = dt['O3(微克每立方米)']
    # lat = dt['lat']
    # lon = dt['lon']
    # 创建新的表格
    # newb = xlwt.Workbook(encoding='utf-8')  # 创建新的工作簿
    # nws = newb.add_sheet('1')  # 添加工作表
    # nws.write('PM2.5(微克每立方米)', 'PM10(微克每立方米)', 'SO2(微克每立方米)', 'NO2(微克每立方米)', 'CO(豪克每立方米)', 'O3(微克每立方米)', 'lat', 'lon')  # 向表中写入title

    # csv_path = 'D:/Project/chinaVis2021/dataset/IAQI/aday/' + filename
    try:
        os.mkdir(os.getcwd() + '/dataset/IAQI/aday/' + filename.split('/')[0])
    except:
        pass
    homedir = (os.getcwd() + '/dataset/IAQI/aday/' + filename).replace('/', '\\')
    csvfile = open(homedir, 'w', newline='', encoding='utf-8')
    writer = csv.writer(csvfile)
    writer.writerow(('PM2.5(微克每立方米)', 'PM10(微克每立方米)', 'SO2(微克每立方米)', 'NO2(微克每立方米)', 'CO(豪克每立方米)', 'O3(微克每立方米)', 'IAQI', 'lat', 'lon'))  # 向表中写入title

    for i in range(1, len(row)):
        # print(row, row[i])
        tPM25 = calIAQI(IAQIS, row[i][0], 'PM25')
        tPM10 = calIAQI(IAQIS, row[i][1], 'PM10')
        tSO2 = calIAQI(IAQIS, row[i][2], 'SO2')
        tNO2 = calIAQI(IAQIS, row[i][3], 'NO2')
        tCO = calIAQI(IAQIS, row[i][4], 'CO')
        tO3 = calIAQI(IAQIS, row[i][5], 'O3')
        tIAQI = max(tPM25, tPM10, tCO, tNO2, tO3, tSO2)  # 选择最大的值
        content = (tPM25, tPM10, tSO2, tNO2, tCO, tO3, tIAQI, row[i][6], row[i][7])
        writer.writerow((content))


    # for row in dt:
    #     # print(dt, row[0])
    #     tPM25 = calIAQI(IAQIS, row[0], 'PM25')
    #     tPM10 = calIAQI(IAQIS, row[1], 'PM10')
    #     tSO2 = calIAQI(IAQIS, row[2], 'SO2')
    #     tNO2 = calIAQI(IAQIS, row[3], 'NO2')
    #     tCO = calIAQI(IAQIS, row[4], 'CO')
    #     tO3 = calIAQI(IAQIS, row[5], 'O3')
    #     tIAQI = max(tPM25, tPM10, tCO, tNO2, tO3, tSO2)  # 选择最大的值
    #     content = (tPM25, tPM10, tSO2, tNO2, tCO, tO3, tIAQI, row[6], row[7])
    #     writer.writerow((content))

    # for i in range(0, len(CO)):
    #     tPM25 = calIAQI(IAQIS, PM25[i], 'PM25')
    #     tPM10 = calIAQI(IAQIS, PM10[i], 'PM10')
    #     tSO2 = calIAQI(IAQIS, SO2[i], 'SO2')
    #     tNO2 = calIAQI(IAQIS, NO2[i], 'NO2')
    #     tCO = calIAQI(IAQIS, CO[i], 'CO')
    #     tO3 = calIAQI(IAQIS, O3[i], 'O3')
    #     tIAQI = max(tPM25, tPM10, tCO, tNO2, tO3, tSO2)  # 选择最大的值
    #     # nPM25 = calIAQI(IAQIS, PM25[i], 'PM25')
    #     # nPM10 = calIAQI(IAQIS, PM10[i], 'PM10')
    #     # nSO2 = calIAQI(IAQIS, SO2[i], 'SO2')
    #     # nNO2 = calIAQI(IAQIS, NO2[i], 'NO2')
    #     # nCO = calIAQI(IAQIS, CO[i], 'CO')
    #     # nO3 = calIAQI(IAQIS, O3[i], 'O3')
    #     # nws.write(tPM25, tPM10, tSO2, tNO2, tCO, tO3, tIAQI, lat[i], lon[i])
    #     content = (tPM25, tPM10, tSO2, tNO2, tCO, tO3, tIAQI, lat[i], lon[i])
    #     writer.writerow((content))
    # newb.save('D:/Project/chinaVis2021/dataset/IAQI/aday/' + filename.split('.')[0] + '.xlsx')  # 保存工作簿
    csvfile.close()
    print(filename)


def rang(end, y, m):
    for d in range(1, end):
        if d < 10:
            dd = '0' + str(d)
        else:
            dd = d
        filename = str(y) + m + '/CN-Reanalysis-daily-' + str(y) + m + str(dd) + '00.csv'
        cal(filename)
        # print(filename)


def bigMonth(y, m):
    rang(32, y, m)


def smallMonth(y, m):
    if m in ['04', '06', '09', '11']:
        rang(31, y, m)
    elif y == 2016:
        rang(30, y, m)
    else:
        rang(29, y, m)

for y in range(2013, 2019):
    for m in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
        if m in ['01', '03', '05', '07', '08', '10', '12']:
            bigMonth(y, m)
        else:
            smallMonth(y, m)
