from skimage.filters import threshold_multiotsu
import numpy as np
import cv2
import glob

pd_range = (-25, 25)
pd0_range = (-25, 15)
pd1_range = (-10, 25)
bins = 16
sigma = 1
weight = ("atan", 0.01, 10)

x_range = (-1, 40)
x_bins = 32


diagonal = []
for i in range(bins):
    if i == 0:
        diagonal.append(i)
    else:
        x = diagonal[i-1] + i + 1
        diagonal.append(x)


def get_thresholds(pict):
    # 大津の方法
    thresholds = threshold_multiotsu(pict)
    thresholds[1] += 20
    return thresholds

def read_image(png_path):
  pict = cv2.imread(png_path, cv2.IMREAD_GRAYSCALE)
  return pict

def binarize(pict, thresholds):
  pict_tic = pict < thresholds[0]
  pict_t2 = (thresholds[0] <= pict) & (pict <= thresholds[1])
  pict_moss = (thresholds[1]) < pict

  return pict_tic, pict_t2, pict_moss

def get_hv():
  hv = [952.4, 925.2, 955.9, 850.2, 948.1, 983.4]
  return hv

def get_pdvects(phase, dimension):
  pdvects_list = glob.glob("output/vectorize/*"+phase+str(dimension)+".npy")
  pdvects_list.sort()
  for i in range(len(pdvects_list)):
    print(pdvects_list[i])
    if i == 0:
      pdvects = np.load(pdvects_list[i])
    else:
      temp_vects = np.load(pdvects_list[i])
      pdvects = np.concatenate([pdvects, temp_vects])

  return pdvects
