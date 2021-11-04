import numpy as np
import seekpath
import matplotlib.pyplot as plt
from euphonic import ForceConstants, ureg, DebyeWaller
from euphonic.util import mp_grid
from euphonic.plot import plot_2d

fc = ForceConstants.from_phonopy()

#cell = fc.crystal.to_spglib_cell()
#qpts = seekpath.get_explicit_k_path(cell)["explicit_kpoints_rel"]

#centre = np.array([0., 0., 0.])
centre = np.array([3., 3., 3.])
step = np.array([0.005, 0, 0])
nsteps = 801

qpts = np.zeros((nsteps, 3))
qpts += centre
qpts += np.array(range(nsteps))[:, np.newaxis]*step[np.newaxis, :]

modes = fc.calculate_qpoint_phonon_modes(qpts)

dw = DebyeWaller.from_json_file('dw300K.json')
sf = modes.calculate_structure_factor(dw=dw)

eunit = modes.frequencies.units
n_ebins = 1001
ebins = np.linspace(
    0, np.amax(modes.frequencies.magnitude), n_ebins)*eunit
sqw = sf.calculate_sqw_map(ebins, calc_bose=True)
sqw = sqw.broaden(y_width=1.5*eunit)
sqw.x_tick_labels = [(0, str(qpts[0])), (len(qpts) - 1, str(qpts[-1]))]

fig, textboxes = plot_2d(sqw, intensity_widget=True)

fig.show()
#plt.show()
