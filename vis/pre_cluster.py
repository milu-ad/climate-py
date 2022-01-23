import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist  # 计算距离
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

path_Location  =os.getcwd()+'./data/location-ini.txt'

# path  =os.getcwd()+'/CN-Reanalysis-daily-2013010100.csv'
# # path = 'D:/Project/chinaVis2021/数据集/aday/' + '201301/CN-Reanalysis-daily-2013010100.csv'
#
# dt = pd.read_csv(path)
# data = dt['列标题']
# print(data)
#


# 获取目标数据
def getDesData(param, j):
    f = open('./data/'+param+'-cluster.json', 'r', encoding='utf-8')
    dt = json.load(f)
    return np.array(dt[param][j])


class pre_cluster:
    def __init__(self):
        self.title_dict = {}
        self.cluster_dict = {}
        self.y_kmeans = {}
        self.weight = []
        pass
    def kmeans_cluster(self):
        resNameWeight = os.getcwd() + "/5_9-weight.txt"
        resultWeight = open(resNameWeight, 'a', encoding='utf-8')
        # print(1,len(self.weight))
        for i in range(0, len(self.weight)):  # 遍历每一个城市，共384个城市
            for k in range(0,len(self.weight[0])):  # 第一个三个月的数据（第一个城市）
                resultWeight.write(str(self.weight[i][k]) + ' ')
            resultWeight.write('\r\n')
        resultWeight.write('\r\n')


        self.cluster = KMeans( init='k-means++', n_clusters=5)
        self.y_kmeans = self.cluster.fit(self.weight)  # 加载数据集合
        # print(self.y_kmeans)
        r1 = pd.Series(self.cluster.labels_) # Series是一个一维的数据结构,labels是分的类别
        # print(r1)
        center_points = self.cluster.cluster_centers_
        # print(center_points)
        r2 = pd.DataFrame(self.cluster.cluster_centers_)
        # print("聚类中心点", r2)
        # print(self.cluster.cluster_centers_)
        r = pd.concat([r2,r1],axis = 1)
        # r = pd.concat([pd.DataFrame(self.weight), pd.Series(self.cluster.labels_)], axis=1)
        # print(r)

        # print('各类别数目', pd.Series(self.cluster.labels_).value_counts())
        # print(self.cluster.labels_)
        # print()
        # 1-30 存储标签
        resNameLabel = os.getcwd() + "/5_9-label.txt"
        resultLabel = open(resNameLabel, 'a', encoding='utf-8')

        resLocation = os.getcwd() + "/5_9-location_label.txt"
        resultLocation = open(resLocation, 'a', encoding='utf-8')
        with open(path_Location,'r',encoding='utf-8') as fl:
            locations = fl.readlines()
            # print('len(self.weight)',len(self.weight))
            for i in range(len(self.weight)):
                resultLabel.write(str(r1[i]) + ' ')
                resultLocation.write(str(r1[i]) + ' '+locations[2*i-1])
                resultLabel.write('\n')
                # resultLocation.write('\n')
            resultLabel.write('\n')
            resultLocation.write('\n')

    def kmeans_evaluate(self):
        K = range(4, 18)
        meandistortions = []
        score = []
        for k in K:
            kmeans = KMeans(init='k-means++', n_clusters=k)
            kmeans.fit(self.weight)
            print('center', kmeans.cluster_centers_)
            print('各类别数目', pd.Series(kmeans.labels_).value_counts())
            for index, value in enumerate(kmeans.labels_):
                if value not in self.cluster_dict:
                    self.cluster_dict[value] = [index]
                else:
                    self.cluster_dict[value].append(index)
            # print(self.cluster_dict)
            print(sorted(self.cluster_dict.items(), key=lambda x: x[0]))

            score.append(metrics.silhouette_score(self.weight, kmeans.labels_, metric='euclidean'))

            meandistortions.append(sum(np.min(cdist(self.weight, kmeans.cluster_centers_, 'euclidean'), axis=1)) / self.weight.shape[0])
        print('meandistortions',meandistortions)
        print('score',score)
        plt.plot(K, meandistortions, 'bx-')
        plt.xlabel('k')
        plt.ylabel(u'DEGREE')
        plt.show()
        pass


    def drawh(self):  # delimiter是数据分隔符
        outputfile = os.getcwd() + "/ingre_result_5-9.xlsx"
        # # resName = os.getcwd() + "/0_mainclass_weight.txt"
        # # resNames = os.getcwd() + "/0_maintype_label.txt"
        # # resName = os.getcwd() + "/0_subclass_weight.txt"
        # # resNames = os.getcwd() + "/0_subtype_label.txt"
        #
        resName = os.getcwd() + "/ingre_weight_5-9.txt"
        resNames = os.getcwd() + "/ingre_label_5-9.txt"
        #
        # # 1-28 读取文件并写入矩阵  权重
        fp = open(resName, 'r', encoding='utf-8')
        row_list = fp.readlines()  # splitlines默认参数是‘\n’
        fp.close()
        data_list = [[float(i) for i in row.strip().split(' ')] for row in row_list if
                     len(row[:-1].split('\r\n')[0]) > 0]
        res = np.mat(data_list)
        print(res)

        # 标签数据
        fpl = open(resNames, 'r', encoding='utf-8')
        row_list_label = fpl.readlines()  # splitlines默认参数是‘\n’
        # print(row_list_label)
        fpl.close()
        list_label = [float(row) for row in row_list_label]
        print("分类标签", list_label)

        colors_list = ['red', 'blue', 'green', 'yellow', 'pink', 'gray', 'purple', 'orange']
        tsne = TSNE(n_components=2)
        Y = tsne.fit_transform(res)  # 进行数据降维，fit_transform将X投影到一个嵌入空间并返回转换结果
        print("降维结果 ",Y)         #  Y 与 tsne.embedding_结果相同
        # C_Y = tsne.fit_transform(center_points)
        # print('center:', C_Y)
        r = pd.concat([pd.DataFrame(Y, columns=['x', 'y']), pd.Series(list_label)], axis=1)
        print("拼接降维结果与分类标签", r)
        r.to_excel(outputfile)

        # d = r[r[0] == 0]
        # plt.plot(d['x'], d['y'], 'r.')
        # d = r[r[0] == 1]
        # plt.plot(d['x'], d['y'], 'go')
        # d = r[r[0] == 2]
        # plt.plot(d['x'], d['y'], 'b*')
        # d = r[r[0] == 3]
        # plt.plot(d['x'], d['y'],color='gray')
        # d = r[r[0] == 4]
        # plt.plot(d['x'], d['y'], color='orange')
        # d = r[r[0] == 5]
        # plt.plot(d['x'], d['y'],color='green')
        # d = r[r[0] == 6]
        # plt.plot(d['x'], d['y'], color='yellow')
        # d = r[r[0] == 7]
        # plt.plot(d['x'], d['y'],color='pink')

        d = r[r[0] == 1]
        plt.plot(d['x'], d['y'], 'r.')
        d = r[r[0] == 7]
        plt.plot(d['x'], d['y'],'o', color = 'purple')
        d = r[r[0] == 5]
        plt.plot(d['x'], d['y'], 'b*')
        d = r[r[0] == 3]
        plt.plot(d['x'], d['y'],'o', color='gray')
        d = r[r[0] == 4]
        plt.plot(d['x'], d['y'],'o', color='orange')
        d = r[r[0] == 6]
        plt.plot(d['x'], d['y'],'o', color='green')
        d = r[r[0] == 2]
        plt.plot(d['x'], d['y'],'o', color='yellow')
        d = r[r[0] == 0]
        plt.plot(d['x'], d['y'],'o', color='pink')

        plt.show()
        print('完成')





if __name__ == '__main__':
    metrics = ['PM25', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    for i in range(len(metrics)):
        with open('./data/' + metrics[i] + '-cluster.json', 'r', encoding='utf-8') as f:
            dt = json.load(f)

            for j in range(len(dt[metrics[i]])-1, len(dt[metrics[i]])):
                print(metrics[i],j)
                p = pre_cluster()
                # if j==59:
                #     print(dt[metrics[i]][j])
                p.weight = np.array(dt[metrics[i]][j])
                p.kmeans_cluster()



    # p = pre_cluster()
    # p.kmeans_cluster()
    # p.kmeans_evaluate()
    # p.drawh()



