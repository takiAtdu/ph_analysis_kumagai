import os
from PIL import Image
import glob
import cv2


basedir = input("パスを指定(ex. /Users/takigawaatsushi/Documents/研究室/研究/data/EPMA/240205/1800c24h) : ")
condition = input("熱処理条件_倍率(data内から選択) : ")
filepaths = glob.glob(basedir + "/*.bmp")
filepaths.sort()
savedir = "data/" + condition + "/"
os.makedirs(savedir, exist_ok=True)

for bmppath in filepaths:
	print("-------------------------")
	print(bmppath)

	image = Image.open(bmppath)

	pngname = os.path.splitext(os.path.basename(bmppath))[0] + ".png"
	pngpath = savedir + pngname
	print(pngpath)
	image.save(pngpath)

	# 画像読み込み
	img = cv2.imread(pngpath)

	# トリミング
	# img[top : bottom, left : right]
	cut_img = img[0:960, 0:1280]

	# 保存
	cv2.imwrite(pngpath, cut_img)
