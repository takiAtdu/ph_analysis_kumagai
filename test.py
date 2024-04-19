import os
from pymatgen.core.structure import Structure
from pymatgen.core.periodic_table import Element
from pymatgen.io.vasp.outputs import Outcar, Vasprun
from pymatgen.io.vasp.inputs import Poscar
from mp_api.client import MPRester
import numpy as np
from dotenv import load_dotenv
import homcloud.interface as hc
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
import matplotlib.pyplot as plt
import ase.io

import common

x_range = common.x_range
x_bins = common.x_bins

load_dotenv()

proxy = "http://proxy.imr.tohoku.ac.jp:8080"

with MPRester(os.environ['MP_API_KEY']) as mpr:
    results = mpr.materials.summary.search(material_ids=["mp-1204829"])

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
for result in results:
    # print(structure.as_dict()["species"][0]["element"])
    # print(structure.coords)
    # elem = Element(structure.as_dict()["species"][0]["element"])
    # print(elem.atomic_radius_calculated)

    # pointcloud.append(structure.coords)
    # x = structure.coords[0]
    # y = structure.coords[1]
    # z = structure.coords[2]
    # for i in range(3):
    #     for j in range(3):
    #         for k in range(3):
    #             dx = x + a * i
    #             dy = y + b * j
    #             zd = z + c * k
    #             coords = [dx, dy, zd]
    #             pointcloud.append(coords)

    result.structure.to("test.cif", fmt="cif")
    atoms = ase.io.read("test.cif")
    for i in range(1, 20):
        atoms_rep = atoms.repeat(i)
        if len(atoms_rep) >= 10000:
            break
    print(atoms_rep)
    print(type(atoms_rep))
    atoms_positions = atoms_rep.get_positions()
    print(atoms_positions)
    print(type(atoms_positions))

    weights = []
    try:
        for atom in atoms_rep:
            elem = Element(atom.symbol)
            atomic_radius = float(elem.atomic_radius)
            weights.append(atomic_radius ** 2)
    except:
        print("skip")
        break

hc.PDList.from_alpha_filtration(atoms_positions, save_to="test.pdgm", save_boundary_map=True)
# hc.PDList.from_alpha_filtration(pointcloud, save_to="test.pdgm", periodicity=[(0, a*3), (0, b*3), (0, c*3)], save_boundary_map=True)

pdlist = hc.PDList("test.pdgm")
pd1 = pdlist.dth_diagram(1)
pd1.histogram(x_range=x_range, x_bins=x_bins).plot(colorbar={"type": "log"})
plt.savefig("test.png")