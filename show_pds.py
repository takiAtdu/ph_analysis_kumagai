import os
import shutil
import homcloud.interface as hc
import matplotlib.pyplot as plt
import glob

save_dir = "retrieve_cifs/output/"

try:
    shutil.rmtree(save_dir + "pd0")
    shutil.rmtree(save_dir + "pd1")
    shutil.rmtree(save_dir + "pd2")
except OSError as e:
    pass
os.makedirs(save_dir, exist_ok=True)

pdgm_list = glob.glob(save_dir + "pdgm/*.pdgm")
skip = []
progress = 0
for pdgm_path in pdgm_list:
    filename = os.path.splitext(os.path.basename(pdgm_path))[0]
    print(filename)

    for i in range(3):
        pd = hc.PDList(pdgm_path).dth_diagram(i)
        try:
            if i == 0:
                pd.histogram().plot(colorbar={"type": "log"})
            elif i == 1:
                pd.histogram().plot(colorbar={"type": "log"})
            elif i == 2:
                pd.histogram().plot(colorbar={"type": "log"})
            os.makedirs(save_dir + "pd" + str(i), exist_ok=True)
            png_path = save_dir + "pd" + str(i) + "/" + filename + "_pd" + str(i) + ".png"
            plt.savefig(png_path)
        except OSError as e:
            skip.append(filename)
            pass

    progress += 1
    print(str(progress/len(pdgm_list)*100) + " %")

print(skip)