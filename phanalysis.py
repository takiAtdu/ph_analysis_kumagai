import os
import homcloud.interface as hc
import glob
import numpy as np

import common

condition = input("熱処理条件_倍率(data内から選択) : ")
filenames = glob.glob("data/" + condition + "/*.png")
filenames.sort()


for png_path in filenames:
    # 画像の読み込み
    print("画像を読み込み中です。")
    image_name = os.path.splitext(os.path.basename(png_path))[0]
    print(png_path)

    # mode="L" とするとグレースケールで読み込まれる
    pict = common.read_image(png_path)

    # 閾値の設定
    print("閾値を設定中です。")
    thresholds = common.get_thresholds(pict)

    # PH解析
    print("PH解析中です。")

    # 2値化
    pict_tic, pict_t2, pict_moss = common.binarize(pict, thresholds)

    tic_count = np.count_nonzero(pict_tic)
    t2_count = np.count_nonzero(pict_t2)
    moss_count = np.count_nonzero(pict_moss)

    sum = tic_count + t2_count + moss_count

    print("-----相分率-----")
    print("TiC : ", tic_count / sum * 100)
    print("T2 : ", t2_count / sum * 100)
    print("Moss : ", moss_count / sum * 100)

    # PH解析
    pd_result_path = "output/"

    tic_result_path = pd_result_path + "pdgm_tic/" + condition + "/"
    os.makedirs(tic_result_path, exist_ok=True)
    hc.PDList.from_bitmap_levelset(hc.distance_transform(pict_tic, signed=True),
                                   save_to=tic_result_path + image_name + "-pd_tic.pdgm")

    t2_result_path = pd_result_path + "pdgm_t2/" + condition + "/"
    os.makedirs(t2_result_path, exist_ok=True)
    hc.PDList.from_bitmap_levelset(hc.distance_transform(pict_t2, signed=True),
                                   save_to=t2_result_path + image_name + "-pd_t2.pdgm")

    moss_result_path = pd_result_path + "pdgm_moss/" + condition + "/"
    os.makedirs(moss_result_path, exist_ok=True)
    hc.PDList.from_bitmap_levelset(hc.distance_transform(pict_moss, signed=True),
                                   save_to=moss_result_path + image_name + "-pd_moss.pdgm")

    print(tic_result_path + image_name + "-pd_tic.pdgm")
    print(t2_result_path + image_name + "-pd_t2.pdgm")
    print(moss_result_path + image_name + "-pd_moss.pdgm")
