import os,json
import numpy as np
from numpy import array, zeros, argmin, inf, equal, ndim
# from scipy.spatial.distance import cdist
from sklearn.metrics.pairwise import manhattan_distances
#在这里我用到的是曼哈顿距离(求绝对值距离)
#如果比较的是二维数组，则用欧几里得距离

def distance(s,t):
    vec_s = np.array(s)
    vec_t = np.array(t)
    # print(vec_s,vec_t)
    if type(s)== type([]) or type(t)== type([]) :
        return np.sqrt(np.sum(np.square(vec_s-vec_t)))
    else:
        return abs(s-t)

def dtwd(s1,s2):
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
    return use_matrics


def DTW(s1,s2,dis_type):

    if dis_type == 'dtwd':
        dtwd(s1,s2)

    elif dis_type == 'dtwi':
        s_len, t_len = len(s1[0]), len(s2[0])
        dimention = len(s2)
        res_matrics = []

        # matrics =[[] for i in range(dimention)]
        for s in range(0, s_len - t_len + 1):  # 查找序列起始点
            for e in range(s, s_len - t_len + 1): # 查找终点

                ini_matrics = zeros((len(s1[0][s:t_len + e]), len(s2[0])))
                ini_matrics = np.array(ini_matrics)

                for z in range(dimention):  # 当前选择的污染指标
                    # print(s,e,z,s1[z][s:t_len + e])
                    sec = s1[z][s:t_len + e]
                    # ini_matrics[z] = zeros((len(sec), len(s2[z])))

                    mt_tmp = dtwd(sec, s2[z])  # 距离计算方式

                    # print('sec',sec)
                    # print('t[z]',s2[z])
                    # print('mt_tmp',mt_tmp)
                    ini_matrics += mt_tmp/dimention
                res_matrics.append(ini_matrics)
                print(s,e,ini_matrics)

def similarity(source,target,limit):
    len_t = len(target)
    len_s = len(source)
    len_part = int(len_s/len_t)
    for i in range(0,len_s,len_part):
        DTW(source[0:len_t + i], target)
        if len_t+i<len_s:
            DTW(source[0:len_t+i], target)
    pass

if __name__ == "__main__":
    s1 = [1, 2, 3, 4, 1, 5, 5, 5, 4]
    s2 = [6, 4, 5, 5, 5, 4]
    s3 = [2, 3, 4, 5, 5, 5]

    s4 = [[1,1],[1,2],[3,4],[3,3],[3,3],[3,3]]
    s5 = [[2,2],[3,2],[3,2]]
    s6 = [[1,2],[3,2],[3,3]]
    s7 = [[1,1],[1,2],[3,4],[3,3]]
    # a = DTW(s1, s2)
    # b = DTW(s1, s3)

    sS = [[127.15406250000001, 80.01104166666666, 66.23208333333332, 209.79375, 98.55958333333331, 162.95833333333337, 144.72916666666666, 232.27083333333331, 77.02031250000002], [77.50425, 61.37504166666667, 53.316625, 118.44070833333333, 55.848875, 89.36945833333333, 84.65158333333333, 120.1385, 58.03870833333333], [53.067166666666665, 34.26825000000001, 21.328833333333332, 62.335249999999995, 17.737916666666667, 33.8435, 25.12741666666667, 47.874833333333335, 25.95575000000001], [65.01406250000001, 72.0621875, 80.9675, 111.99229166666666, 79.32489583333331, 85.4034375, 85.49020833333333, 81.90104166666666, 45.78291666666666], [37.293749999999996, 38.145833333333336, 34.4625, 48.179166666666674, 37.43124999999999, 44.52916666666666, 44.4875, 47.99166666666665, 36.24166666666667], [15.639166666666668, 16.239125, 14.285791666666665, 9.062916666666668, 15.166041666666667, 17.017249999999997, 17.117625000000004, 13.052416666666668, 24.348000000000003]]
    st = [[66.23208333333332, 209.79375, 98.55958333333331, 162.95833333333337, 144.72916666666666], [53.316625, 118.44070833333333, 55.848875, 89.36945833333333, 84.65158333333333], [21.328833333333332, 62.335249999999995, 17.737916666666667, 33.8435, 25.12741666666667], [80.9675, 111.99229166666666, 79.32489583333331, 85.4034375, 85.49020833333333], [34.4625, 48.179166666666674, 37.43124999999999, 44.52916666666666, 44.4875], [14.285791666666665, 9.062916666666668, 15.166041666666667, 17.017249999999997, 17.117625000000004]]


    # c = DTW(s4, s5)
    # d = DTW(s4, s6)
    # e = dtwd(s4, s7)

    f = DTW(sS, st,'dtwi')





