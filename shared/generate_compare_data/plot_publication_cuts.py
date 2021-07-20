import matplotlib
matplotlib.rcParams['font.family'] = 'serif'
#matplotlib.rcParams['font.size'] = 20
matplotlib.rcParams['font.size'] = 18

#matplotlib.rcParams['font.serif'] = 'CMU Serif'

import os
import glob

import numpy as np

from euphonic import ureg, DebyeWaller
from euphonic.plot import plot_2d
from util import get_fc, get_qpts, get_euphonic_fpath, get_material_info


def get_fine_sf(qpts, material, fine_qpts_mult):
    """
    Get structure factor on a finer set of q-points
    for nicer plotting
    """
    if fine_qpts_mult > 1:
        new_qpts = np.zeros((len(qpts)*fine_qpts_mult - 1, 3))
    else:
        new_qpts = qpts
    qpts_idx = np.arange(len(new_qpts))
    for i in range(3):
        new_qpts[:, i] = np.interp(qpts_idx,
                                   qpts_idx[::fine_qpts_mult],
                                   qpts[:, i])
    fc = get_fc(material)
    print(f'Calculating {len(new_qpts)} q-points for {material}')
    phon = fc.calculate_qpoint_phonon_modes(
            new_qpts, asr='reciprocal')
    dw = get_dw(material)
    # Avoid divide by zero frequencies
    phon._frequencies[phon._frequencies == 0] = np.amin(np.absolute(
        phon._frequencies[phon._frequencies != 0]))
    sf = phon.calculate_structure_factor(dw=dw)
    return sf


def get_dw(material, temp='300'):
    _, grid, _, _ = get_material_info(material)
    fname = get_euphonic_fpath(material, 'euphonic', 'dw', '300',
                               from_fc=True, grid=grid)
    return DebyeWaller.from_json_file(fname)


def get_ebins(material, bin_width=0.005):
    if material == 'quartz':
        return np.arange(0, 165, bin_width)*ureg('meV')
    elif material == 'lzo':
        return np.arange(0, 105, bin_width)*ureg('meV')
    elif material == 'nb':
        return np.arange(0, 31, bin_width)*ureg('meV')
    elif material == 'al':
        return np.arange(0, 46, bin_width)*ureg('meV')


def get_fig(material, cut, x_data_idx=None, negative_idx=False,
            fine_qpts_mult=1, e_max=None, lim=None, **plot_kwargs):
    qpts = get_qpts(material, cut)
    sf = get_fine_sf(qpts, material, fine_qpts_mult)
    ebins = get_ebins(material)
    if e_max is not None:
        e_max = e_max*ebins.units
        ebins = ebins[ebins < e_max]
    sqw = sf.calculate_sqw_map(ebins)
    if lim is not None:
        sqw._z_data[sqw._z_data > lim] = lim
    sqw = sqw.broaden(x_width=0.005*ureg('1/angstrom'),
                      y_width=1.5*ureg('meV'), shape='gauss')
    if x_data_idx != None:
        sqw.x_tick_labels = None
        sqw._x_data = sf.qpts[:, x_data_idx]
        if negative_idx:
            sqw._x_data = np.negative(sqw._x_data)
    fig = plot_2d(sqw, y_label='Energy (meV)', **plot_kwargs)
    return fig



save_kwargs = {'bbox_inches': 'tight'}
fig1 = get_fig('quartz', '30L_qe_fine', 2, negative_idx=True, fine_qpts_mult=10,
               vmax=3.5, x_label='[-3,0,-L]')
matplotlib.pyplot.savefig('figures/cuts/quartz_30L_cut.pdf', **save_kwargs)
fig2 = get_fig('quartz', '2ph_m4_0_qe', 0, vmax=3.5,
               x_label='[H,-4,0]', fine_qpts_mult=10)
matplotlib.pyplot.savefig('figures/cuts/quartz_2ph_cut.pdf', **save_kwargs)

fig3 = get_fig('lzo', 'kagome_qe', 2, negative_idx=True, vmax=7.5,
               x_label='[-5,7,-L]', fine_qpts_mult=10, lim=1e5)
matplotlib.pyplot.savefig('figures/cuts/lzo_kagome_cut.pdf', **save_kwargs)
fig4 = get_fig('lzo', 'hh2_qe_fine', 0, vmax=7.5,
               x_label='[H,-H,-2]', fine_qpts_mult=10, lim=1e5)
matplotlib.pyplot.savefig('figures/cuts/lzo_hh2_cut.pdf', **save_kwargs)

fig5 = get_fig('nb', '110_qe', 0, vmax=100,
               x_label='[H,H,0]', fine_qpts_mult=50)
matplotlib.pyplot.savefig('figures/cuts/nb_110_cut.pdf', **save_kwargs)
fig6 = get_fig('nb', 'm110_qe', 1, vmax=150,
               x_label='[2-K,K,0]', fine_qpts_mult=50, e_max=12)
matplotlib.pyplot.savefig('figures/cuts/nb_m110_cut.pdf', **save_kwargs)

fig7 = get_fig('al', 'h00_qe', 0, vmax=75,
               x_label='[H,2,2]', fine_qpts_mult=50)
matplotlib.pyplot.savefig('figures/cuts/al_h00_cut.pdf', **save_kwargs)
fig8 = get_fig('al', 'h_0.5kl_qe', 0, vmax=75,
               x_label='[H, 2+0.5H, 2+0.5H]', fine_qpts_mult=50)
matplotlib.pyplot.savefig('figures/cuts/al_h_05kl_cut.pdf', **save_kwargs)

matplotlib.pyplot.show()
