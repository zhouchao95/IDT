# -*- coding: utf-8 -*- 

'''
Author: ByronVon
Email: wangy@craiditx.com
Version: 
Date: 2020-11-09 10:23:23
LastEditTime: 2020-11-15 22:52:09
'''
import random
import numpy as np
import pandas as pd
from IDT import IDT_VR
import matplotlib.image as img
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def split_zones(data):
    """输入为一个dataframe，且包含"class_disp"这个状态列，根据注视的状态分区间
    """
    results, init_ix = [], 0

    for i in range(1, data.shape[0]):
        if data["class_disp"][i] == data["class_disp"][i-1]:
            continue
        else:
            # print(init_ix, i, sum(data["class_disp"][init_ix: i]))
            results.append(data.iloc[init_ix:i,:])
            init_ix = i
    return results


def plot_circle(data,picture):

    bg = img.imread(picture) ## bg为一个numpy数组
    bg = np.flipud(bg) ## 翻转图像
    fig = plt.figure() 
    axe = fig.gca()
    plt.imshow(bg) ## 将图片铺满背景
    plt.xlim(0, bg.shape[1]) ## 将坐标轴与图片shape同比拉伸
    plt.ylim(0, bg.shape[0])

    centX, centY = [], []
    for d in data:
        if sum(d["class_disp"]) == 0: ## 当处于注视状态时，才画图
            centerX = np.abs(((d.iloc[0]['et_x']+d.iloc[-1]['et_x'])/2*1000))
            centerY = np.abs(((d.iloc[0]['et_y']+d.iloc[-1]['et_y'])/2*1000))
            centX.append(centerX)
            centY.append(centerY)
            plt.plot(centerX, centerY)
            radius = d.shape[0] ## 以持续间隔作为圆的半径
            circle = Circle(xy=(centerX, centerY), radius=random.randint(10,50), alpha=0.5, color='g')
            # if radius > 50:
            #     continue
            axe.add_patch(circle)
    plt.plot(centX, centY)
    plt.show()


def qnum2eule(qx, qy, qz, qw):
    '''
    按照Z-Y-X顺序的顺序将四元数转成欧拉角
    '''    
    vector = np.zeros((3,1))
    vector[0] = np.arctan2(2*(qx*qy+qz*qw),1-2*(qy**2+qz**2))
    vector[1] = np.arcsin(2*(qx*qz-qw*qy))
    vector[2] = np.arctan2(2*(qx*qw+qy*qz),1-2*(qz**2+qw**2))
    return vector

def qum2matrix(qx, qy, qz, qw):
    '''四元数转旋转矩阵
    '''
    matrix = np.zeros((3,3))
    matrix[0][0] = 1-2*qy**2-2*qz**2 ## 1-2y^2-2z^2
    matrix[0][1] = 2*(qx*qy-qz*qw) ## 2(xy-zw)
    matrix[0][2] = 2*(qx*qz+qy*qw) ## 2(xz+yw)
    matrix[1][0] = 2*(qx*qy+qz*qw) ## 2(xy+zw)
    matrix[1][1] = 1-2*qx**2-2*qz**2 ## 1-2x^2-2z^2
    matrix[1][2] = 2*(qy*qz-qx*qw) ## 2(yz-xw)
    matrix[2][0] = 2*(qx*qz-qy*qw) ## 2(xz-yw)
    matrix[2][1] = 2*(qy*qz+qx*qw) ## 2(yz+xw)
    matrix[2][2] = 1-2*qx**2-2*qy**2 ## 1-2x^2-2y^2
    return matrix

if __name__ == "__main__":
    
    # ## 检测 注视/扫视 的状态，将结果保存到 './dataset/std_data.csv' 中
    # data = pd.read_csv('./dataset/std_eye_moving.csv')
    # ## 参数说明
    # ## time_th(窗口间隔): 25000ns,即25ms；
    # ## disp_th(转动角度): 1度,角度
    # ## frec_th(咋样频率): 20,越大那么检测到的注视点越少
    # new_data = IDT_VR(data=data,time_th=25000,disp_th=1,frec_th=20,debug=True)

    # print(sum(new_data['class_disp']))

    # new_data.to_csv('./dataset/std_data.csv.bak')

    ## 分割 注视和扫视 时间窗口
    splits = split_zones(pd.read_csv('./dataset/std_data.csv'))

    ## 使用 注视状态 的点绘图
    plot_circle(splits,'./dataset/image1.png')
