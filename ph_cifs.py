import os
import shutil
import numpy as np
import homcloud.interface as hc
import ase.io
from pymatgen.core.periodic_table import Element
import glob

save_dir = "retrieve_cifs/output/"

try:
    shutil.rmtree(save_dir)
except OSError as e:
    pass
os.makedirs(save_dir, exist_ok=True)

cif_list = glob.glob("retrieve_cifs/cifs/*.cif")
skip = []
for index, cif in enumerate(cif_list):
    filename = os.path.splitext(os.path.basename(cif))[0]
    print(filename)

    atoms = ase.io.read(cif)
    print(atoms)
    print(type(atoms))
    print(atoms[0])
    print(type(atoms[0]))
    print(atoms[0].symbol)
    print(type(atoms[0].symbol))

    atoms_rep = atoms.repeat(1)
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
        print("skip ", filename)
        skip.append(filename)
        break
    weights = np.array(weights)
    print(weights.shape)
    print(atoms_positions.shape)

    atoms_positions += np.random.uniform(-1e-4, 1e-4, size=atoms_positions.shape)
    os.makedirs(save_dir + "pdgm/", exist_ok=True)
    pdgm_path = save_dir + "pdgm/" + filename + ".pdgm"
    hc.PDList.from_alpha_filtration(atoms_positions, weight=weights, save_boundary_map=True, save_to=pdgm_path)

    print(str(index/len(cif_list)*100) + " %")

print(skip)