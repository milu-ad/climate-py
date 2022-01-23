import os,json,time,datetime
import numpy as np
from numpy import array, zeros, argmin, inf, equal, ndim

# from scipy.spatial.distance import cdist
from sklearn.metrics.pairwise import manhattan_distances
#在这里我用到的是曼哈顿距离(求绝对值距离)
#如果比较的是二维数组，则用欧几里得距离

def distance(s,t):
    vec_s = np.array(s)
    vec_t = np.array(t)
    if type(s)== type([]) or type(t)== type([]) :
        return np.sqrt(np.sum(np.square(vec_s-vec_t)))
    else:
        return abs(int(s)-int(t))



def DTW(s1,s2):
    s_len, t_len = len(s1), len(s2)
    ini_m = zeros((s_len + 1, t_len + 1))

    ini_m[0, 1:] = inf
    ini_m[1:, 0] = inf
    use_matrics = ini_m[1:, 1:]

    # 浅复制
    # print D1

    # 生成原始距离矩阵--dtwd
    for i in range(s_len):
        for j in range(t_len):
            use_matrics[i, j] = distance(s1[i],s2[j])  # 距离计算方式






    # 当前路径长度 = 前一步的路径长度 + 当前元素的大小
    # a) 左边的相邻元素 (i, j-1)
    # b) 上面的相邻元素 (i-1, j)
    # c) 左上方的相邻元素 (i-1, j-1)

    M = use_matrics.copy()
    # 代码核心，动态计算最短距离
    for i in range(0, s_len):  # (0,8)
        for j in range(0, t_len):  # (0,6)
            # 获得累计距离矩阵
            use_matrics[i, j] += min(ini_m[i, j], ini_m[i, j + 1], ini_m[i + 1, j])

    # 获取最短路径
    i, j = array(ini_m.shape) - 2  # i=7  j =5
    p, q = [i], [j]
    # 回溯寻找最短路径
    while (i > 0 or j > 0):
        tb = argmin((ini_m[i, j], ini_m[i, j + 1], ini_m[i + 1, j]))  # 最小值的索引
        if tb == 0:
            i -= 1
            j -= 1
        elif tb == 1:
            i -= 1
        else:
            j -= 1
        p.insert(0, i)
        q.insert(0, j)

    # print('M = ', M)  # 原始距离矩阵
    # print('sequence = ', list(zip(p, q)))  # 匹配路径过程
    # print('use_matrics = ', use_matrics)  # Cost Matrix或者叫累积距离矩阵
    # print(use_matrics[-1, -1])  # 序列距离
    return use_matrics[-1, -1]

# 讲天数换算为日期
def get_date(year,day):
    fir_day = datetime.datetime(year,1,1)
    zone = datetime.timedelta(days=day-1)
    return datetime.datetime.strftime(fir_day + zone, "%Y-%m-%d")

# 获取单维污染等级匹配结果
# 滑动窗口匹配，与目标序列等长
def query_level(target):
    dir = os.getcwd() + '\data\level_combine_ini'
    lists = os.listdir(dir)  # 列出文件夹下所有的目录与文件
    len_t = len(target)
    result = {}
    now_time = datetime.datetime.now()
    print(now_time)
    for i in range(0, len(lists)):
        path = os.path.join(dir, lists[i])
        for root, dirs, files in os.walk(path):
            # 数据分别是 D:\PycharmProjects\climate\data\AQI_city\上海市 [] ['上海市.csv']
            dic_key = root.split('\\')[-1]  # 省会/市名称  上海市
            for file in files:
                dir_file = root + '\\' + file
                count = 0
                start_count = 0
                with open(dir_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    end_index = len(data)-len_t+1
                    source = []
                    for index in range(0,end_index):
                        peroid_obj = []

                        start_count += list(data[index].values())[0]
                        for t in range(len_t):
                            for k, v in data[index+t].items():
                                source.append(k)
                                count += v
                        sec_distance = DTW(source, target)  # 2,3,4,5
                        # result[sec_distance] = {}
                        date = get_date(2013, count)
                        start_date = get_date(2013,start_count)
                        peroid_obj.append(start_count)
                        peroid_obj.append(count)
                        # peroid_obj.append(count-start_count)

                        if sec_distance not in result:
                            result[sec_distance] = {}
                            result[sec_distance][dic_key] = []
                        else:
                            if dic_key not in result[sec_distance]:
                                result[sec_distance][dic_key] = []
                        result[sec_distance][dic_key].append(peroid_obj)
                        # print(index, sec_distance, source,start_count,count,start_date, date,list(data[index].values())[0])
                        source = []
                        count = start_count
    print(datetime.datetime.now())
    print(result[1])
    print(result[2])
    print(result[3])
        #         break
        #     break
        # break
    pass

# 根据时间段和地区获取等级相似的序列数据
def get_secquence(province,start_count,end_count):
    # start_date = get_date(2013, start_count)
    # start_time,end_time,
    dir = os.getcwd()+'\data\AQI_value'
    lists = os.listdir(dir)
    res = [[],[],[],[],[],[]]
    for i in range(0,len(lists)):
        path = os.path.join(dir, lists[i])
        for root, dirs, files in os.walk(path):
            # 数据分别是 D:\PycharmProjects\climate\data\AQI_city\上海市 [] ['上海市.csv']
            dic_key = root.split('\\')[-1]  # 省会/市名称  上海市
            if dic_key == province:
                for file in files:
                    dir_file = root + '\\' + file
                    with open(dir_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        for i in range(start_count,end_count+1):
                            one_day =  get_date(2013, i)
                            res[0].append(data[one_day]['level_PM25'])
                            res[1].append(data[one_day]['level_PM10'])
                            res[2].append(data[one_day]['level_SO2'])
                            res[3].append(data[one_day]['level_NO2'])
                            res[4].append(data[one_day]['level_CO'])
                            res[5].append(data[one_day]['level_O3'])
                            # res.append(data[one_day])
    print(res)
    pass

# 对等级相似的数据进行数值匹配，多维指标
def similarity(source,target,limit):
    len_t = len(target)
    len_s = len(source)
    # len_part = int(len_s/len_t)
    for i in range(0,len_s-len_t+1):
        sec_distance = DTW(source[0:len_t + i], target)
    pass



if __name__ == "__main__":
    # print(get_date(2016, 1))

    s1 = [2,5,2,4,3]
    query_level(s1)
    # get_secquence('上海市',9,17)


    pass



