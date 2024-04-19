import numpy as np
import pyvista as pv  # モジュールの読み込み
import homcloud.pyvistahelper as pvhelper  # HomCloud側のヘルパー関数を導入
import os
import glob


file_list = glob.glob("binary3d/*.txt")
image = np.stack([np.loadtxt("binary3d/binary3d_{:d}.txt".format(n)) > 0.5 for n in range(len(file_list))], axis=0)
print(image.shape)
print(image.dtype)

pl = pv.Plotter()
pl.add_mesh(pvhelper.Bitmap3D(image).threshold(0.5), show_scalar_bar=False, opacity=0.7)
pl.show()