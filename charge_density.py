import os
from mp_api.client import MPRester
from dotenv import load_dotenv

load_dotenv()

with MPRester(os.environ['MP_API_KEY']) as mpr:
    # this will return a pymatgen Chgcar object
    charge_density = mpr.get_charge_density_from_material_id("mp-149")

print(charge_density)
print(type(charge_density))

print(charge_density.net_magnetization)
print(type(charge_density.net_magnetization))

charge_density.write_file("charge_density.txt")