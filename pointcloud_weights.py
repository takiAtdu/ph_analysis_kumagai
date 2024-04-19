import os
from pymatgen.core.periodic_table import Element
from mp_api.client import MPRester
import numpy as np
from dotenv import load_dotenv
import homcloud.interface as hc
import matplotlib.pyplot as plt
import pyvista as pv

import common

x_range = common.x_range
x_bins = common.x_bins

load_dotenv()

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
# a = Decimal(str(a)).quantize(Decimal('0.0000001'), ROUND_HALF_UP)
b = results[0].structure.lattice.b
# b = Decimal(str(b)).quantize(Decimal('0.0000001'), ROUND_HALF_UP)
c = results[0].structure.lattice.c
# c = Decimal(str(c)).quantize(Decimal('0.0000001'), ROUND_HALF_UP)

# print(results[0].structure.lattice.a)
# print(results[0].structure.lattice.b)
# print(results[0].structure.lattice.c)

pointcloud = []
weights = []
for structure in results[0].structure:
    elem = Element(structure.as_dict()["species"][0]["element"])

    x = structure.coords[0]
    y = structure.coords[1]
    z = structure.coords[2]
    for i in range(3):
        for j in range(3):
            for k in range(3):
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
                weights.append(ionic_radii**2)


pointcloud = np.array(pointcloud)
print(pointcloud.shape)
# np.savetxt('pointcloud_weights.txt', pointcloud)

weights = np.array(weights)
print(weights.shape)

# hc.PDList.from_alpha_filtration(pointcloud, save_to="test.pdgm", save_boundary_map=True)
hc.PDList.from_alpha_filtration(pointcloud, weight=weights, save_to="pointcloud_weights.pdgm", periodicity=[(0, a*3), (0, b*3), (0, c*3)], save_boundary_map=True)

for i in range(3):
    pd = hc.PDList("pointcloud_weights.pdgm").dth_diagram(i)
    pd.histogram(x_bins=x_bins).plot(colorbar={"type": "log"})
    plt.savefig("pointcloud_weights_pd"+str(i)+".png")

# pd = hc.PDList("pointcloud_weights.pdgm").dth_diagram(2)
# pair = pd.nearest_pair_to(1, 1.3)
# stable_volume = pair.stable_volume(0.05)
# optimal_volume = pair.optimal_volume()
#
# pl = pv.Plotter()
# pl.add_mesh(pv.PointSet(pointcloud))
# pl.add_mesh(stable_volume.to_pyvista_boundary_mesh(), color="green")
# # pl.add_mesh(optimal_volume.to_pyvista_boundary_mesh(), color="green")
# pl.show()