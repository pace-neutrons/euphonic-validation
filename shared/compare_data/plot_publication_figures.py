import matplotlib
matplotlib.rcParams['font.family'] = 'serif'
#matplotlib.rcParams['font.serif'] = 'CMU Serif'

import os

import numpy as np
import matplotlib as mpl

from compare_sf import get_summed_and_scaled_sfs
from util import plot_at_qpt


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
                noshow=True)
            figs.append(fig)
    return figs


def get_path(material, cut, model, fname):
    return os.path.join('..', '..', material, cut, model, fname)


figs = plot_sf([get_path('lzo', 'kagome_qe', 'ab2tds', 'alongthelineF_300K.dat'),
                get_path('lzo', 'kagome_qe', 'euphonic', 'sf_phonons_300K.json'),
                get_path('lzo', 'kagome_qe', 'euphonic', 'sf_fc_300K.json')],
               [39, 79],
               labels=['CASTEP phonons, Ab2tds structure factors',
                       'CASTEP phonons, Euphonic structure factors',
                       'Euphonic phonons, Euphonic structure factors'])

for fig in figs:
    mpl.pyplot.show()

