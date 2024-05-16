import os
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.preprocessing import LabelEncoder

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


is_weights = input("weights?: ")
is_periodic = input("periodic?: ")

df = pd.read_csv('retrieve_cifs.csv')
data = df[df["formula_pretty"] == "SiO2"]
filename_list = data["filename"].values.tolist()
# data = df[df["crystal_system"].isin(['Cubic', 'Tetragonal'])]
# filename_list = data["filename"].values.tolist()
# filename_list = df["filename"].values.tolist()

is_metal = np.array(df["is_metal"].values)
crystal_system = np.array(df["crystal_system"].values)


if is_weights == "1" and is_periodic != "1":
    base_dir = "retrieve_cifs/output/weights/"
elif is_weights != "1" and is_periodic == "1":
    base_dir = "retrieve_cifs/output/periodic/"
elif is_weights == "1" and is_periodic == "1":
    base_dir = "retrieve_cifs/output/weights_periodic/"
else:
    base_dir = "retrieve_cifs/output/none/"


for dimension in range(3):
    print(f"start {dimension}th dimension")
    vect_list = []
    labels = []
    for i, filename in enumerate(filename_list):
        try:
            vect_path = base_dir + "pd" + str(dimension) + "_vect/" + filename + ".npy"
            if not os.path.exists(vect_path):
                continue
            vect = np.load(base_dir + "pd" + str(dimension) + "_vect/" + filename + ".npy")
            vect_list.append(vect)
            labels.append(crystal_system[i])
        except:
            pass
    print("vect_list[0]: ", vect_list[0])
    print("type(vect_list[0]): ", type(vect_list[0]))
    print("len(labels): ", len(labels))
    print("labels[0]: ", labels[0])

    vects = np.array(vect_list)
    print("vects.shape: ", vects.shape)

    # data = vects / vects.max()
    data = vects

    # ラベルを数値に変換
    print("ラベルを数値に変換")
    le = LabelEncoder()
    numeric_labels = le.fit_transform(labels)

    # 階層的クラスタリングを実行
    print("階層的クラスタリングを実行")
    linked = linkage(data, method='ward')

    # クラスタリングの結果を3つのクラスターに分ける
    print("クラスタリングの結果をnつのクラスターに分ける")
    clusters_num = 7
    clusters = fcluster(linked, t=clusters_num, criterion='maxclust')

    # クラスタリングに基づくデンドログラム
    plt.figure(figsize=(20, 10))

    plt.subplot(1, 2, 1)
    dendrogram(linked,
               orientation='top',
               distance_sort='descending',
               show_leaf_counts=True,
               labels=labels,  # ラベルを指定
               color_threshold=linked[-(clusters_num - 1), 2])  # クラスタの数を3に指定するための閾値
    plt.title("Hierarchical Clustering Dendrogram with Clusters")
    plt.xlabel("Sample index")
    plt.ylabel("Distance")

    # ラベルに基づくデンドログラム
    plt.subplot(1, 2, 2)
    dendrogram(linked,
               orientation='top',
               distance_sort='descending',
               show_leaf_counts=True,
               labels=labels,  # ラベルを指定
               leaf_rotation=90,  # ラベルを横に表示
               leaf_font_size=10)  # フォントサイズ
    plt.title("Hierarchical Clustering Dendrogram with Labels Colored")
    plt.xlabel("Sample index")
    plt.ylabel("Distance")

    # ラベルに基づく色分けを追加
    # 各ラベルに対応する色を定義
    print("各ラベルに対応する色を定義")
    label_colors = {le.classes_[i]: plt.cm.viridis(i / len(le.classes_)) for i in range(len(le.classes_))}

    ax = plt.gca()
    x_labels = ax.get_xmajorticklabels()
    for lbl in x_labels:
        lbl.set_color(label_colors[lbl.get_text()])

    plt.tight_layout()
    plt.savefig(base_dir + f"hierarchical_clustering_{dimension}th.png")

