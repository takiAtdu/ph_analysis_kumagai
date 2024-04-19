import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

import common

labels = np.array([1]*100 + [2]*100 + [3]*100 + [4]*100 + [5]*100 + [6]*100)

phase = input("phase(moss, t2, tic) : ")
dimension = int(input("dimension(0, 1) : "))
sigma = common.sigma
weight = common.weight
bins = common.bins
pd_range = common.pd_range
diagonal = common.diagonal

pdvects = common.get_pdvects(phase, dimension)
print("pdvects.shape: ", pdvects.shape)


# 正規化
print('pdvects (min, max): (', pdvects.min(), ', ', pdvects.max(), ')')
pdvects = pdvects / pdvects.max()

print("pdvects[0].shape: ", pdvects[0].shape)

# 主成分解析
pca = PCA(n_components=10)
pca.fit(pdvects)

reduced = pca.transform(pdvects)



# # 寄与率を表示
# plt.bar([n for n in range(1, len(pca.explained_variance_ratio_)+1)], pca.explained_variance_ratio_)

# print([n for n in range(1, len(pca.explained_variance_ratio_)+1)])
# print(pca.explained_variance_ratio_)

# 主成分をプロット
x = []
y = []
z = []
for vec in reduced:
    x.append(vec[0])
    y.append(vec[1])
    z.append(vec[2])
x = x/max(x)
y = y/max(y)
z = z/max(z)


fig = plt.figure()
pc_dim = input("表示する次元 : ")
if pc_dim == "3":
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel("PC1", size = 10, color = "k")
    ax.set_ylabel("PC2", size = 10, color = "k")
    ax.set_zlabel("PC3", size = 10, color = "k")
elif pc_dim == "2":
    ax = fig.add_subplot(111)
    xlabel = input("x軸（1, 2, 3）：")
    ylabel = input("y軸（1, 2, 3）：")
    ax.set_xlabel("PC"+xlabel, size = 10, color = "k")
    ax.set_ylabel("PC"+ylabel, size = 10, color = "k")

ax.set_xticks([-1.0, -0.5, 0, 0.5, 1.0])
ax.set_yticks([-1.0, -0.5, 0, 0.5, 1.0])
if pc_dim == "3":
    ax.set_zticks([-1.0, -0.5, 0, 0.5, 1.0])

if pc_dim == "3":
    ax.scatter(x[labels == 1], y[labels == 1], z[labels == 1], s = 20, c = "r")
    ax.scatter(x[labels == 2], y[labels == 2], z[labels == 2], s = 20, c = "b")
    ax.scatter(x[labels == 3], y[labels == 3], z[labels == 3], s = 20, c = "y")
    ax.scatter(x[labels == 4], y[labels == 4], z[labels == 4], s = 20, c = "g")
    ax.scatter(x[labels == 5], y[labels == 5], z[labels == 5], s = 20, c = "c")
    ax.scatter(x[labels == 6], y[labels == 6], z[labels == 6], s = 20, c = "k")
elif pc_dim == "2":
    if xlabel == "1" and ylabel == "2":
        ax.scatter(x[labels == 1], y[labels == 1], s = 20, c = "r")
        ax.scatter(x[labels == 2], y[labels == 2], s = 20, c = "b")
        ax.scatter(x[labels == 3], y[labels == 3], s = 20, c = "y")
        ax.scatter(x[labels == 4], y[labels == 4], s = 20, c = "g")
        ax.scatter(x[labels == 5], y[labels == 5], s = 20, c = "c")
        ax.scatter(x[labels == 6], y[labels == 6], s = 20, c = "k")
    elif xlabel == "1" and ylabel == "3":
        ax.scatter(x[labels == 1], z[labels == 1], s = 20, c = "r")
        ax.scatter(x[labels == 2], z[labels == 2], s = 20, c = "b")
        ax.scatter(x[labels == 3], z[labels == 3], s = 20, c = "y")
        ax.scatter(x[labels == 4], z[labels == 4], s = 20, c = "g")
        ax.scatter(x[labels == 5], z[labels == 5], s = 20, c = "c")
        ax.scatter(x[labels == 6], z[labels == 6], s = 20, c = "k")
    elif xlabel == "2" and ylabel == "3":
        ax.scatter(y[labels == 1], z[labels == 1], s = 20, c = "r")
        ax.scatter(y[labels == 2], z[labels == 2], s = 20, c = "b")
        ax.scatter(y[labels == 3], z[labels == 3], s = 20, c = "y")
        ax.scatter(y[labels == 4], z[labels == 4], s = 20, c = "g")
        ax.scatter(y[labels == 5], z[labels == 5], s = 20, c = "c")
        ax.scatter(y[labels == 6], z[labels == 6], s = 20, c = "k")

legend_flag = input("凡例を表示するか[y/n] : ")
if legend_flag == "y":
    ax.legend(["1600c24h", "1600c3h", "1700c3h", "1800c24h", "1800c3h", "As Cast"])

# 出力
save_flag = input("保存するか[y/n] : ")
if save_flag == "y":
    save_dir = "output/classification/"
    os.makedirs(save_dir, exist_ok=True)
    if pc_dim == "3":
        plt.savefig(save_dir + pc_dim+"D_" + phase + str(dimension) + ".png")
    elif pc_dim == "2":
        plt.savefig(save_dir + pc_dim+"D_" + phase + str(dimension) + "_PC"+xlabel + "_" + "PC"+ylabel + ".png")
else:
    plt.show()