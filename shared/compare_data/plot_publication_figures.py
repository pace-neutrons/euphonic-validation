import matplotlib
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.size'] = 18

#matplotlib.rcParams['font.serif'] = 'CMU Serif'

import os

import numpy as np
import matplotlib as mpl

from compare_sf import get_summed_and_scaled_sfs
from compare_sqw import get_scaled_sqws
from util import plot_at_qpt
from euphonic import StructureFactor


def plot_sqw(sqw_files, qpts_idx, labels=None):
    sqws, ebins = get_scaled_sqws(
        sqw_files, mask_bragg=True)
    figs = []
    if labels == None:
        labels = sqw_files
    for qpt in qpts_idx:
        fig = plot_at_qpt(
                [x[qpt] for x in sqws],
                labels, x=ebins[0],
                x_title='Energy (meV)', y_title='Intensity',
                noshow=True,
                **{'loc': 2})
        ax = fig.get_axes()[0]
        ax.set_xlim(ebins[0][0], ebins[0][-1])
        ax.set_ylim(0)
        figs.append(fig)
    return figs

def plot_sf(sf_files, qpts_idx, labels=None):
    sf_sums, qpts, dg_freqs = get_summed_and_scaled_sfs(
        sf_files, use_bose=True, mask_bragg=True)
    figs = []
    if labels == None:
        labels = sf_files
    for qpt in qpts_idx:
        # As the structure factors have been summed, the last n entries
        # are zero (where n is the number of degenerate modes)
            zero_idx = np.where(dg_freqs[qpt] == 0)[0]
            if len(zero_idx) > 0:
                idx = zero_idx[0]
            else:
                idx = dg_freqs.shape[1]
            fig = plot_at_qpt(
                [x[qpt, :idx] for x in sf_sums],
                labels, x=dg_freqs[qpt, :idx],
                x_title='Mode Frequency (meV)', y_title='Intensity',
                noshow=True, **{'loc': 1})
            ax = fig.get_axes()[0]
            ax.set_xlim(0, dg_freqs[qpt, idx - 1])
            ax.set_ylim(0)
            figs.append(fig)
    return figs


def get_qpts(material, cut):
    sf = StructureFactor.from_json_file(
            get_path(material, cut, 'euphonic', 'sf_fc_300K.json'))
    return sf.qpts


def get_path(material, cut, model, fname):
    return os.path.join('..', '..', material, cut, model, fname)


figs = plot_sf([get_path('lzo', 'kagome_qe', 'ab2tds', 'alongthelineF_300K.dat'),
                get_path('lzo', 'kagome_qe', 'euphonic', 'sf_phonons_300K.json'),
                get_path('lzo', 'kagome_qe', 'euphonic', 'sf_fc_300K.json')],
               [79],
               labels=['CASTEP phonons, Ab2tds structure factors',
                       'CASTEP phonons, Euphonic structure factors',
                       'Euphonic phonons, Euphonic structure factors'])

figs = plot_sqw([get_path('lzo', 'hh2_qe_fine', 'oclimax', 'La2Zr2O7_2Dmesh_scqw_300K.csv'),
                 get_path('lzo', 'hh2_qe_fine', 'oclimax', 'sqw_euphonic_ph_300K.json'),
                 get_path('lzo', 'hh2_qe_fine', 'oclimax', 'sqw_euphonic_300K.json')],
                [66],
                labels=['CASTEP phonons, Oclimax intensities',
                        'CASTEP phonons, Euphonic intensities',
                        'Euphonic phonons, Euphonic intensities'])

for fig in figs:
    mpl.pyplot.show()

