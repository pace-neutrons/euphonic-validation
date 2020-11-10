from euphonic.plot import plot_2d
from euphonic import ureg, StructureFactor
import numpy as np

sf = StructureFactor.from_json_file('../euphonic/sf_phonons_5K.json')
ebins = np.arange(0,180,0.5)*ureg('meV')

sqw = sf.calculate_sqw_map(ebins)
fig, ims = plot_2d(sqw, ratio=1.0, vmax=1e-8)
fig.show()
