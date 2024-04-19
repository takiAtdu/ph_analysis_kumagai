import os
import shutil
from pymatgen.core.periodic_table import Element
from mp_api.client import MPRester
import numpy as np
from dotenv import load_dotenv
import homcloud.interface as hc
import matplotlib.pyplot as plt
import pyvista as pv
import ase
import ase.io

import common

x_range = common.x_range
x_bins = common.x_bins

load_dotenv()

try:
    shutil.rmtree("ph_sio2")
except OSError as e:
    pass

os.makedirs("ph_sio2", exist_ok=True)
save_dir = "ph_sio2/"

with MPRester(os.environ['MP_API_KEY']) as mpr:
    results = mpr.materials.summary.search(formula=["SiO2"])

# print(results[0])
# print(type(results[0]))
# print(results[0].structure)
# print(type(results[0].structure))

# print(results[0].structure.lattice)
# print(type(results[0].structure.lattice))
#
# print(results[0].structure.species)
# print(type(results[0].structure.species))

a = results[0].structure.lattice.a
# b = results[0].structure.lattice.b
# c = results[0].structure.lattice.c
b = a
c = a

# print(results[0].structure.lattice.a)
# print(results[0].structure.lattice.b)
# print(results[0].structure.lattice.c)

for index, result in enumerate(results):
    pointcloud = []
    weights = []
    for structure in result.structure:
        elem = Element(structure.as_dict()["species"][0]["element"])

        x = structure.coords[0]
        y = structure.coords[1]
        z = structure.coords[2]

        for i in range(1):
            for j in range(1):
                for k in range(1):
                    dx = x + a * i
                    dy = y + b * j
                    zd = z + c * k
                    coords = [dx, dy, zd]
                    pointcloud.append(coords)

                    # radii is given in angstrom
                    if str(elem) == "Si":
                        ionic_radii = elem.ionic_radii[4]
                    elif str(elem) == "O":
                        ionic_radii = elem.ionic_radii[-2]
                    weights.append(ionic_radii ** 2)

    pointcloud = np.array(pointcloud)
    print(pointcloud.shape)
    # np.savetxt(save_dir+'pointcloud_weights_'+str(index)+'.txt', pointcloud)

    weights = np.array(weights)
    print(weights.shape)

    hc.PDList.from_alpha_filtration(pointcloud, save_to=save_dir+"pointcloud_weights_"+str(index)+".pdgm", save_boundary_map=True)
    # hc.PDList.from_alpha_filtration(pointcloud, weight=weights, save_to=save_dir+"pointcloud_weights_"+str(index)+".pdgm", periodicity=[(0, a * 3), (0, b * 3), (0, c * 3)], save_boundary_map=True)

    for i in range(3):
        pd = hc.PDList(save_dir+"pointcloud_weights_"+str(index)+".pdgm").dth_diagram(i)
        try:
            pd.histogram(x_range=x_range, x_bins=x_bins).plot(colorbar={"type": "log"})
            plt.savefig(save_dir + "pointcloud_weights_" + str(index) + "_pd" + str(i) + ".png")
        except OSError as e:
            pass
