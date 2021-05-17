import matplotlib
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.size'] = 20
#matplotlib.rcParams['font.serif'] = 'CMU Serif'

import os
import glob

import numpy as np
import matplotlib as mpl

from euphonic import (ureg, StructureFactor, QpointPhononModes,
                      ForceConstants, DebyeWaller)
from euphonic.plot import plot_2d


def get_sf(material, cut):
    path = os.path.join(
            '..', '..', material, cut, 'euphonic', 'sf_fc_300K.json')
    sf =  StructureFactor.from_json_file(path)
    return sf


def get_fine_sf(sf, material, cut, fine_qpts_mult):
    """
    Get structure factor on a finer set of q-points
    for nicer plotting
    """
    new_qpts = np.zeros((len(sf.qpts)*fine_qpts_mult - 1, 3))
    qpts_idx = np.arange(len(new_qpts))
    for i in range(3):
        new_qpts[:, i] = np.interp(qpts_idx,
                                   qpts_idx[::fine_qpts_mult],
                                   sf.qpts[:, i])
    fc = get_fc(material)
    print(f'Calculating {len(new_qpts)} q-points for {material}')
    phon = fc.calculate_qpoint_phonon_modes(
            new_qpts, asr='reciprocal', use_c=True, n_threads=2)
    dw = get_dw(material)
    sf = phon.calculate_structure_factor(dw=dw)
    return sf


def get_fc(material):
    glob_path = os.path.join(
            '..', '..', material, 'shared', 'castep', '*.castep_bin')
    return ForceConstants.from_castep(glob.glob(glob_path)[0])


def get_dw(material, temp='300'):
    path = os.path.join('..', '..', material, 'shared', 'euphonic',
                        'dw_fc_666_' + temp + 'K.json')
    return DebyeWaller.from_json_file(path)


def get_ebins(material, bin_width=0.01):
    if material == 'quartz':
        return np.arange(0, 165, bin_width)*ureg('meV')
    elif material == 'lzo':
        return np.arange(0, 105, bin_width)*ureg('meV')
    elif material == 'nb':
        return np.arange(0, 30, bin_width)*ureg('meV')


def get_fig(material, cut, x_data_idx=None, negative_idx=False,
            fine_qpts_mult=0, **plot_kwargs):
    sf = get_sf(material, cut)
    if fine_qpts_mult > 0:
        sf = get_fine_sf(sf, material, cut, fine_qpts_mult)
    sqw = sf.calculate_sqw_map(get_ebins(material))
    sqw = sqw.broaden(y_width=1.5*ureg('meV'), shape='gauss')
    if x_data_idx != None:
        sqw.x_tick_labels = None
        sqw._x_data = sf.qpts[:, x_data_idx]
        if negative_idx:
            sqw._x_data = np.negative(sqw._x_data)
    fig = plot_2d(sqw, y_label='Energy (meV)', **plot_kwargs)
    return fig


fig1 = get_fig('quartz', '30L_qe_fine', 2, negative_idx=True, fine_qpts_mult=5,
               vmax=4e-12, x_label='[-3,0,-L]')
fig2 = get_fig('quartz', '2ph_m4_0_qe', 0, vmax=4e-12,
               x_label='[H,-4,0]', fine_qpts_mult=5)
fig3 = get_fig('lzo', 'kagome_qe', 2, negative_idx=True, vmax=3e-11,
               x_label='[-5,7,-L]', fine_qpts_mult=5)
fig4 = get_fig('lzo', 'hh2_qe_fine', 0, vmax=3e-11,
               x_label='[H,-H,-2]', fine_qpts_mult=5)
fig5 = get_fig('nb', '110_qe', 0, vmax=1e-11,
               x_label='[H,H,0]', fine_qpts_mult=5)
fig6 = get_fig('nb', 'm110_qe', 1, vmax=1e-11,
               x_label='[2-K,K,0]', fine_qpts_mult=5)

matplotlib.pyplot.show()
