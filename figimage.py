# -*- coding: utf-8 -*- 

'''
Author: ByronVon
Email: wangy@craiditx.com
Version: 
Date: 2020-11-12 10:17:17
LastEditTime: 2020-11-15 22:46:33
'''
import random
import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

bg = img.imread('image2.png') ## bg为一个numpy数组
bg = np.flipud(bg) ## 翻转图像
fig = plt.figure() 
axe = fig.gca()
plt.imshow(bg) ## 将图片铺满背景
plt.xlim(0, bg.shape[1]) ## 将坐标轴与图片shape同比拉伸
plt.ylim(0, bg.shape[0])

data = [i for i in range(150)]

centX, centY = [],[]
for d in data:
    centerX = (d+5*random.random())
    centerY = (4*(d+random.random()))
    centX.append(centerX)
    centY.append(centerY)
    plt.plot(centerX, centerY)
    radius = random.randint(1,10) ## 以持续间隔作为圆的半径
    circle = Circle(xy=(centerX, centerY), radius=radius, alpha=0.5, color='g')
    axe.add_patch(circle)
plt.plot(centX, centY)
plt.show()