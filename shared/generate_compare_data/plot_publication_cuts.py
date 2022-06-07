"""
Plots pretty versions of the validation cuts (fine
q and E bins, gaussian broadening)
"""
import matplotlib
#matplotlib.rcParams['font.family'] = 'serif'
#matplotlib.rcParams['font.size'] = 20
#matplotlib.rcParams['font.size'] = 18

#matplotlib.rcParams['font.serif'] = 'CMU Serif'

import os
import glob

import numpy as np

from euphonic import ureg, DebyeWaller
from euphonic.plot import plot_2d
from util import (get_fc, get_qpts, get_euphonic_fpath, get_material_info,
                  latex_cut_names)


def get_fine_sf(qpts, material, fine_qpts_mult, append_qpts=None,
                prepend_qpts=None):
    """
    Get structure factor on a finer set of q-points
    for nicer plotting
    """
    if append_qpts is not None:
        qpts = np.append(qpts, append_qpts, axis=0)
    if prepend_qpts is not None:
        qpts = np.insert(qpts, 0, prepend_qpts, axis=0)
    if fine_qpts_mult > 1:
        new_qpts = np.zeros((len(qpts) + (len(qpts) - 1)*(fine_qpts_mult - 1), 3))
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


def get_ticks(ax_lim, spacing):
    prec = 2
    tick_min = round(spacing*round(float(ax_lim[0])/spacing),prec)
    tick_max = round(spacing*round(float(ax_lim[1])/spacing),prec) + 0.1*spacing
    if spacing%1 < 10**(-prec):
        dtype = np.int32
    else:
        dtype = None
    ticks = np.arange(tick_min, tick_max, spacing, dtype=dtype)
    return ticks


def get_fig(material, cut, x_data_idx=None, negative_idx=False,
            fine_qpts_mult=1, e_max=None, lim=None, append_qpts=None,
            prepend_qpts=None, x_tick_spacing=None, y_tick_spacing=None,
            **plot_kwargs):
    qpts = get_qpts(material, cut)
    sf = get_fine_sf(qpts, material, fine_qpts_mult, append_qpts=append_qpts,
                     prepend_qpts=prepend_qpts)
    ebins = get_ebins(material)
    if e_max is not None:
        e_max = e_max*ebins.units
        ebins = ebins[ebins < e_max]
    sqw = sf.calculate_sqw_map(ebins)
    if lim is not None:
        sqw._z_data[sqw._z_data > lim] = lim
    sqw = sqw.broaden(x_width=0.005*ureg('1/angstrom'),
                      y_width=1.5*ureg('meV'), shape='gauss')
    if x_data_idx is not None:
        sqw.x_tick_labels = None
        sqw._x_data = sf.qpts[:, x_data_idx]
        if negative_idx:
            sqw._x_data = np.negative(sqw._x_data)
    with matplotlib.pyplot.style.context('pub.mplstyle'):
        fig = plot_2d(sqw, y_label='Energy (meV)', **plot_kwargs)
    ax = fig.axes[0]
    if x_tick_spacing is not None:
        ax.set_xticks(get_ticks(ax.get_xlim(), x_tick_spacing))
    if y_tick_spacing is not None:
        ax.set_yticks(get_ticks(ax.get_ylim(), y_tick_spacing))
    return fig



save_kwargs = {'bbox_inches': 'tight'}
fig1 = get_fig('quartz', '30L_qe_fine', 2, negative_idx=True, fine_qpts_mult=10,
               vmax=3.5, x_label=latex_cut_names['30L_qe_fine'],
               x_tick_spacing=1, y_tick_spacing=50)
matplotlib.pyplot.savefig('figures/cuts/quartz_30L_cut.png', **save_kwargs)
fig2 = get_fig('quartz', '2ph_m4_0_qe', 0, vmax=3.5, prepend_qpts=np.array([[-4., -4., 0.]]),
               x_label=latex_cut_names['2ph_m4_0_qe'], fine_qpts_mult=2,
               x_tick_spacing=2, y_tick_spacing=50)
matplotlib.pyplot.savefig('figures/cuts/quartz_2ph_cut.png', **save_kwargs)

fig3 = get_fig('lzo', 'kagome_qe', 2, negative_idx=True, vmax=7.5,
               x_label=latex_cut_names['kagome_qe'], fine_qpts_mult=10, lim=1e5,
               x_tick_spacing=2, y_tick_spacing=25)
matplotlib.pyplot.savefig('figures/cuts/lzo_kagome_cut.png', **save_kwargs)
fig4 = get_fig('lzo', 'hh2_qe_fine', 0, vmax=7.5, append_qpts=np.array([[-4., 4., -2.]]),
               x_label=latex_cut_names['hh2_qe_fine'], fine_qpts_mult=10, lim=1e5,
               x_tick_spacing=1, y_tick_spacing=25)
matplotlib.pyplot.savefig('figures/cuts/lzo_hh2_cut.png', **save_kwargs)

fig5 = get_fig('nb', '110_qe', 0, vmax=100,
               x_label=latex_cut_names['110_qe'], fine_qpts_mult=50,
               x_tick_spacing=0.1, y_tick_spacing=10)
matplotlib.pyplot.savefig('figures/cuts/nb_110_cut.png', **save_kwargs)
fig6 = get_fig('nb', 'm110_qe', 1, vmax=150,
               x_label=latex_cut_names['m110_qe'], fine_qpts_mult=50, e_max=12,
               x_tick_spacing=0.1, y_tick_spacing=5)
matplotlib.pyplot.savefig('figures/cuts/nb_m110_cut.png', **save_kwargs)

fig7 = get_fig('al', 'h00_qe', 0, vmax=75,
               x_label=latex_cut_names['h00_qe'], fine_qpts_mult=50,
               x_tick_spacing=0.1, y_tick_spacing=10)
matplotlib.pyplot.savefig('figures/cuts/al_h00_cut.png', **save_kwargs)
fig8 = get_fig('al', 'h_0.5kl_qe', 0, vmax=75,
               x_label=latex_cut_names['h_0.5kl_qe'], fine_qpts_mult=50,
               x_tick_spacing=0.2, y_tick_spacing=10)
matplotlib.pyplot.savefig('figures/cuts/al_h_05kl_cut.png', **save_kwargs)

matplotlib.pyplot.show()
