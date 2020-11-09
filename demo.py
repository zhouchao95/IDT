import pandas as pd
from IDT import IDT_VR
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
            print(init_ix, i, sum(data["class_disp"][init_ix: i]))
            results.append(data.iloc[init_ix:i,:])
            init_ix = i
    return results


def plot_circle(data):

    fig = plt.figure(figsize=(6,6))
    axe = fig.gca()

    centX, centY = [], []
    for d in data:
        if sum(d["class_disp"]) == 0: ## 当处于注视状态时，才画图
            centerX = ((d.iloc[0]['et_x']+d.iloc[-1]['et_x'])/2)
            centerY = ((d.iloc[0]['et_y']+d.iloc[-1]['et_y'])/2)
            centX.append(centerX)
            centY.append(centerY)
            plt.plot(centerX, centerY)
            radius = d.shape[0] ## 以持续间隔作为圆的半径
            circle = Circle(xy=(centerX, centerY), radius=radius/500, alpha=0.5, color='g')
            if radius > 50:
                continue
            axe.add_patch(circle)
    plt.plot(centX, centY)
    plt.show()

    
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
    plot_circle(splits)
