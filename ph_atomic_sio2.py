import os
import shutil
from mp_api.client import MPRester
import numpy as np
from dotenv import load_dotenv
import homcloud.interface as hc
import matplotlib.pyplot as plt
import ase.io
from pymatgen.core.periodic_table import Element

import common

x_range = common.x_range
x_bins = common.x_bins

load_dotenv()

try:
    shutil.rmtree("ph_atomic_sio2")
except OSError as e:
    pass

save_dir = "ph_atomic_sio2/"
os.makedirs(save_dir, exist_ok=True)
os.makedirs(save_dir + "cif", exist_ok=True)
os.makedirs(save_dir + "pdgm", exist_ok=True)
os.makedirs(save_dir + "pd0", exist_ok=True)
os.makedirs(save_dir + "pd1", exist_ok=True)
os.makedirs(save_dir + "pd2", exist_ok=True)

with MPRester(os.environ['MP_API_KEY']) as mpr:
    results = mpr.materials.summary.search(formula=["SiO2"])

for result in results:
    filename = result.material_id
    print(filename)

    cif_path = save_dir + "cif/" + filename + ".cif"
    result.structure.to(cif_path, fmt="cif")

    atoms = ase.io.read(cif_path)
    filename = os.path.splitext(os.path.basename(cif_path))[0]
    print(filename)

    print(atoms)
    print("原子数: ", str(len(atoms)))
    print(type(atoms))
    print(atoms[0])
    print(type(atoms[0]))
    print(atoms[0].charge)
    print(type(atoms[0].charge))
    print(atoms[0].symbol)
    print(type(atoms[0].symbol))

    for i in range(1, 20):
        atoms_rep = atoms.repeat(i)
        if len(atoms_rep) >= 10000:
            break
    print(atoms_rep)
    print(type(atoms_rep))
    atoms_positions = atoms_rep.get_positions()
    print(atoms_positions)
    print(type(atoms_positions))

    elem = Element(atoms_rep[10].symbol)
    print(elem.ionic_radii)
    print(type(elem.ionic_radii))
    print(elem.atomic_radius)
    print(type(elem.atomic_radius))
    print(float(elem.atomic_radius))

    weights = []
    for atom in atoms_rep:
        elem = Element(atom.symbol)

        # radii is given in angstrom
        if str(elem) == "Si":
            ionic_radii = elem.ionic_radii[4]
        elif str(elem) == "O":
            ionic_radii = elem.ionic_radii[-2]
        else:
            ionic_radii = 0
        weights.append(ionic_radii ** 2)
    weights = np.array(weights)
    print(weights.shape)
    print(atoms_positions.shape)

    atoms_positions += np.random.uniform(-1e-4, 1e-4, size=atoms_positions.shape)
    pdgm_path = save_dir + "pdgm/" + filename + ".pdgm"
    hc.PDList.from_alpha_filtration(atoms_positions, weight=weights, save_boundary_map=True, save_to=pdgm_path)

    for i in range(3):
        pd = hc.PDList(pdgm_path).dth_diagram(i)
        try:
            if i == 0:
                pd.histogram((0, 1), 16).plot(colorbar={"type": "log"})
            elif i == 1:
                pd.histogram((0, 20), 32).plot(colorbar={"type": "log"})
            elif i == 2:
                pd.histogram((0, 20), 32).plot(colorbar={"type": "log"})
            png_path = save_dir + "pd" + str(i) + "/" + filename + "_pd" + str(i) + ".png"
            plt.savefig(png_path)
        except OSError as e:
            pass
