import os
import shutil
from mp_api.client import MPRester
from dotenv import load_dotenv

import common

x_range = common.x_range
x_bins = common.x_bins

load_dotenv()

try:
    shutil.rmtree("retrieve_cifs")
except OSError as e:
    pass

save_dir = "retrieve_cifs/cifs/"
os.makedirs(save_dir, exist_ok=True)

with MPRester(os.environ['MP_API_KEY']) as mpr:
    results = mpr.materials.summary.search(crystal_system=["Cubic", "Tetrahedral", "Orthorhombic"])
    # results = mpr.materials.summary.search(formula=["SiO2"])

for result in results:
    filename = result.material_id
    print(filename)

    cif_path = save_dir + filename + ".cif"
    result.structure.to(cif_path, fmt="cif")

print(len(results))