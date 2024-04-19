import os
import numpy as np
import homcloud.interface as hc
import glob

import common

labels = np.array([1]*100 + [2]*100 + [3]*100 + [4]*100 + [5]*100 + [6]*100)

condition = input("熱処理条件_倍率 : ")
# phase = input("phase(moss, t2, tic) : ")
phases = ["moss", "t2", "tic"]
# dimension = int(input("dimension(0, 1) : "))
dimensions = [0, 1]
sigma = common.sigma
weight = common.weight
bins = common.bins
pd_range = common.pd_range
diagonal = common.diagonal

for phase in phases:
    pdnames = glob.glob("output/pdgm_"+phase+"/"+condition+"/*.pdgm", recursive=True)
    pdnames.sort()
    for dimension in dimensions:
        for pdname in pdnames:
            print(pdname)

        # PH解析の結果を取得
        pds = [hc.PDList(pdname).dth_diagram(dimension) for pdname in pdnames]

        # ベクトル化
        spec = hc.PIVectorizeSpec(pd_range, bins, sigma=sigma, weight=weight)
        pdvects = np.vstack([spec.vectorize(pd) for pd in pds])

        os.makedirs("output/vectorize/", exist_ok=True)
        np.save("output/vectorize/"+condition+"_"+phase+str(dimension)+".npy", pdvects)
        print("output/vectorize/"+condition+"_"+phase+str(dimension)+".npy")
