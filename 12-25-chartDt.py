import os,json,time,datetime,heapq
import numpy as np
from numpy import array, zeros, argmin, inf, equal, ndim

chartDtPathDir = os.getcwd() + '\data\chart_levelSeqDt'
path_city = os.getcwd()+'\data\level_combine_ini\云南省\丽江市.json'
# 讲天数换算为日期
def get_date(year,day):
    fir_day = datetime.datetime(year,1,1)
    zone = datetime.timedelta(days=day-1)
    return datetime.datetime.strftime(fir_day + zone, "%Y-%m-%d")


def get_chart_data():
    # start_date = get_date(2013, start_count)
    # start_time,end_time,
    dir = os.getcwd()+'\data\level_combine_ini'
    lists = os.listdir(dir)
    for i in range(0,len(lists)):
        path = os.path.join(dir, lists[i])
        for root, dirs, files in os.walk(path):
            # 数据分别是 D:\PycharmProjects\climate\data\AQI_city\上海市 [] ['上海市.csv']
            province = root.split('\\')[-1]  # 省会/市名称  上海市
            dir_province = chartDtPathDir + '/' + province
            isExists = os.path.exists(dir_province)
            if not isExists:
                os.makedirs(dir_province)

            for file in files:
                city = file.split('.')[0]
                dir_file = root + '\\' + file
                with open(dir_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    res = []
                    StartDate = 1
                    for dict in data:
                        tmp = {}
                        for k,v in dict.items():
                            EndDate = StartDate + v -1

                            tmp['Level']= k
                            tmp['LastingDays']= v
                            tmp['Type']= 'city'
                            tmp['Start']= get_date(2013,StartDate)
                            tmp['End']= get_date(2013,EndDate)
                            tmp['Description']= dict
                            res.append(tmp)
                            StartDate = EndDate + 1
                    f = open(chartDtPathDir + '/' + province + '/' + city + '.json', 'w', encoding='utf-8')
                    f.write(json.dumps(res))
                    f.close()

    pass


def sss(dir_file):
    with open(dir_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        res = []
        StartDate = 1
        for dict in data:
            tmp = {}
            for k, v in dict.items():
                EndDate = StartDate + v - 1

                tmp['Level'] = k
                tmp['LastingDays'] = v
                tmp['Type'] = 'city'
                tmp['Start'] = get_date(2013, StartDate)
                tmp['End'] = get_date(2013, EndDate)
                tmp['Description'] = dict
                res.append(tmp)
                StartDate = EndDate + 1
        print(res)
    pass



if __name__ == '__main__':
    # sss(path_city)

    get_chart_data()