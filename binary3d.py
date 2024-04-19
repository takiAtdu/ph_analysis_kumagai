import os
import shutil

from pymatgen.core.periodic_table import Element
from mp_api.client import MPRester
import numpy as np
from dotenv import load_dotenv

mag = 10
lot = 1

load_dotenv()

try:
    shutil.rmtree("binary3d")
except OSError as e:
    pass

with MPRester(os.environ['MP_API_KEY']) as mpr:
    # results = mpr.materials.summary.search(formula=["SiO2"])
    # results = mpr.materials.summary.search(material_ids=["mp-5229"])
    results = mpr.materials.summary.search(material_ids=["mp-559928"])


a = int(results[0].structure.lattice.a * mag)
b = int(results[0].structure.lattice.b * mag)
c = int(results[0].structure.lattice.c * mag)

def in_box(x, y, z):
    return 0 <= x <= a*lot-1 and 0 <= y <= b*lot-1 and 0 <= z <= c*lot-1

print(a, b, c)

image = np.ones((a*lot, b*lot, c*lot))
for structure in results[0].structure:
    print(structure.as_dict()["species"][0]["element"])
    print(structure.coords)
    elem = Element(structure.as_dict()["species"][0]["element"])
    print(elem.ionic_radii)

    x = int(structure.coords[0] * mag)
    y = int(structure.coords[1] * mag)
    z = int(structure.coords[2] * mag)
    coords1 = np.array([x, y, z])

    # radii is given in angstrom
    if str(elem) == "Si":
        ionic_radii = elem.ionic_radii[4]
    elif str(elem) == "O":
        ionic_radii = elem.ionic_radii[-2]
    elif str(elem) == "Sr":
        ionic_radii = elem.ionic_radii[2]
    elif str(elem) == "Ti":
        ionic_radii = elem.ionic_radii[4]
    else:
        ionic_radii = 0.1

    radii = int(ionic_radii * mag)

    for i in range(-radii, radii+1):
        for j in range(-radii, radii+1):
            for k in range(-radii, radii+1):
                x_dx = x + i
                y_dy = y + j
                z_dz = z + k
                coords2 = np.array([x_dx, y_dy, z_dz])
                distance = int(np.linalg.norm(coords2 - coords1))

                if distance <= radii:
                    for s in range(lot+1):
                        for t in range(lot+1):
                            for u in range(lot+1):
                                x_dx_a = x_dx + s * a
                                y_dy_b = y_dy + t * b
                                z_dz_c = z_dz + u * c
                                if in_box(x_dx_a, y_dy_b, z_dz_c):
                                    image[x_dx_a][y_dy_b][z_dz_c] = 0

print(image.shape)

os.makedirs("binary3d", exist_ok=True)
for i, layer in enumerate(image):
    np.savetxt("binary3d/binary3d_"+str(i)+".txt", layer)
