import numpy as np

import matplotlib.pyplot as plt

#计算点到直线的距离
def calculate_error(st, seq_range):
    x = np.arange(seq_range[0], seq_range[1] + 1)
    y = np.array(st[seq_range[0]:seq_range[1] + 1])
    A = np.ones((len(x), 2), float)
    A[:, 0] = x
    # 返回回归系数、残差平方和、自变量X的秩、X的奇异值
    (p, residuals, ranks, s) = np.linalg.lstsq(A, y, rcond=None)#最小二乘法回归
    try:
        error = residuals[0]
    except IndexError:
        error = 0.0
    return error
def improvement_splitting_here(T, i, seq_range):
    return calculate_error(T, (seq_range[0], i)) + calculate_error(T, (i + 1, seq_range[1]))
def Top_Down(T, max_error, seq_range=None):
    if not seq_range:
        seq_range = (0, len(T) - 1)
    best_so_far = float('inf')
    break_point = float('inf')
    for i in range(seq_range[0] + 1, seq_range[1]):
        improvement_in_approximation = improvement_splitting_here(T, i, seq_range)
        if improvement_in_approximation < best_so_far:
            break_point = i
            best_so_far = improvement_in_approximation
    left_error = calculate_error(T, (seq_range[0], break_point))
    left_seg = T[seq_range[0]:break_point + 1]
    right_error = calculate_error(T, (break_point+1, seq_range[1]))
    right_seg = T[break_point+1:seq_range[1]+1]
    if left_error > max_error:
        segleft = Top_Down(T, max_error, (seq_range[0], break_point))
    else:
        segleft = [left_seg]
    if right_error > max_error:
        segright = Top_Down(T, max_error, (break_point, seq_range[1]))
    else:
        segright = [right_seg]
    return segleft + segright
df_2001_split=Top_Down(df_2001['arousal'],0.02)
#df_2001为DataFrame，df_2001['arousal']为其中一列572点的series，想要对这一series进行分段；
#返回得到的df_2001_split是list,每一行为分成的一段；
#0.02为多次尝试后设置的阈值；
x=[]#x存储分界点的index
y=[]#根据index
for i in range(0,len(df_2001_split)):
    x.append(df_2001_split[i].index.start)
x.append(len(df_2001)-1)#记得再加上最后一个点的index
for i in x:
    y.append(df_2001['arousal'][(df_2001['arousal'].index==i)])
y=np.array(y)


#图形表示
plt.figure(figsize=(10,5))
plt.plot(df_2001['arousal'].index,df_2001['arousal'])
plt.scatter(x,y,color="r")
plt.show()


