import numpy as np
import seekpath
import matplotlib.pyplot as plt
from euphonic import ForceConstants, ureg, DebyeWaller
from euphonic.util import mp_grid
from euphonic.plot import plot_2d

fc = ForceConstants.from_phonopy()

#cell = fc.crystal.to_spglib_cell()
#qpts = seekpath.get_explicit_k_path(cell)["explicit_kpoints_rel"]

# 2. 2. 2. to 6. 2. 2.
#centre = np.array([2.,2.,2.])
#step = np.array([0.005, 0, 0])
#nsteps = 801

# Cut #1
# 2. 2. 2. to 6. 6. 6.
#centre = np.array([2., 2., 2.])
#step = np.array([0.02, 0.02, 0.02])
#nsteps = 201
#emax = 35
#n_ebins = 101

# 2. 2. 2. to 6. 4. 4.
#centre = np.array([2., 2., 2.])
#step = np.array([0.005, 0.0025, 0.0025])
#nsteps = 801

# Cut #2
centre = np.array([0., 1., 0.])
step = np.array([0., 0.016, 0.]) # Shows another mode at 50meV
nsteps = 251
emax = 50
n_ebins = 141

qpts = np.zeros((nsteps, 3))
qpts += centre
qpts += np.array(range(nsteps))[:, np.newaxis]*step[np.newaxis, :]

modes = fc.calculate_qpoint_phonon_modes(qpts)

dw = DebyeWaller.from_json_file('dw300K.json')
sf = modes.calculate_structure_factor(dw=dw)

if not 'emax' in locals():
    emax = np.amax(modes.frequencies.magnitude)
if not 'n_ebins' in locals():
    n_ebins = 1001
eunit = modes.frequencies.units
ebins = np.linspace(0, emax, n_ebins)*eunit
sqw = sf.calculate_sqw_map(ebins, calc_bose=True)
sqw = sqw.broaden(y_width=1.5*eunit)
sqw.x_tick_labels = [(0, str(qpts[0])), (len(qpts) - 1, str(qpts[-1]))]

fig, textboxes = plot_2d(sqw, intensity_widget=True, vmax=5)

#fig.show()
plt.show()
