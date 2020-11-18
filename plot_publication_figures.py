import matplotlib
matplotlib.rcParams['font.family'] = 'serif'
#matplotlib.rcParams['font.serif'] = 'CMU Serif'

import os

import numpy as np
import matplotlib as mpl

from euphonic import ureg, StructureFactor, QpointPhononModes
from euphonic.plot import plot_2d

def get_sf(material, cut):
    path = os.path.join(material, cut, 'euphonic', 'sf_fc_300K.json')
    sf =  StructureFactor.from_json_file(path)
    return sf

def get_ebins(material, bin_width=0.01):
    if material == 'quartz':
        return np.arange(0, 165, bin_width)*ureg('meV')
    elif material == 'lzo':
        return np.arange(0, 105, bin_width)*ureg('meV')
    elif material == 'nb':
        return np.arange(0, 30, bin_width)*ureg('meV')

def get_fig(material, cut, x_data_idx=None, negative_idx=False,
            **plot_kwargs):
    sf = get_sf(material, cut)
    sqw = sf.calculate_sqw_map(get_ebins(material))
    sqw = sqw.broaden(y_width=1.5*ureg('meV'))
    if x_data_idx != None:
        sqw.x_tick_labels = None
        sqw._x_data = sf.qpts[:, np.absolute(x_data_idx)]
        if negative_idx:
            sqw._x_data = np.negative(sqw._x_data)

    fig = plot_2d(sqw, y_label='Energy (meV)', **plot_kwargs)
    return fig

fig1 = get_fig('quartz', '30L_qe_fine', 2, negative_idx=True,
               vmax=1e-11, x_label='[-3,0,-L]')
fig2 = get_fig('quartz', '2ph_m4_0_qe', 0, vmax=1e-11,
               x_label='[H,-4,0]')
fig3 = get_fig('lzo', 'kagome_qe', -2, negative_idx=True, vmax=1e-11,
               x_label='[-5,7,-L]')
fig4 = get_fig('lzo', 'hh2_qe_fine', 0, vmax=1e-11,
               x_label='[H,-H,-2]')
fig5 = get_fig('nb', '110_qe', 0, vmax=1e-11,
               x_label='[H,H,0]')
fig6 = get_fig('nb', 'm110_qe', 1, vmax=1e-11,
               x_label='[2-K,K,0]')

matplotlib.pyplot.show()
