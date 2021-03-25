import matplotlib
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.size'] = 18

import os

import numpy as np
import matplotlib as mpl

from compare_sf import get_summed_and_scaled_sfs
from compare_sqw import get_scaled_sqws
from util import plot_at_qpt, plot_at_qpt_bar
from euphonic import StructureFactor


def plot_sqw(material, cut, sqw_files, qpts_idx, labels=None):
    sqw_files = fnames_to_paths(material, cut, sqw_files)
    sqws, ebins = get_scaled_sqws(
        sqw_files, mask_bragg=True)
    figs = []
    if labels == None:
        labels = sqw_files
    qpts = get_qpts(material, cut)
    for ebins_i in ebins:
        if len(ebins_i) == sqws[0].shape[1]:
            plot_ebins = ebins_i
    for qpt in qpts_idx:
        print(f'Plotting sqw for {cut} at qpt:{qpt} {qpts[qpt]}')
        fig = plot_at_qpt(
                [x[qpt] for x in sqws],
                labels, x=plot_ebins,
                x_title='Energy (meV)', y_title='Intensity',
                noshow=True,
                **{'loc': 2})
        ax = fig.get_axes()[0]
        ax.set_xlim(ebins[0][0], ebins[0][-1])
        ax.set_ylim(0)
        figs.append(fig)
    return figs


def plot_sf(material, cut, sf_files, qpts_idx, labels=None):
    sf_files = fnames_to_paths(material, cut, sf_files)
    sf_sums, qpts, dg_freqs = get_summed_and_scaled_sfs(
        sf_files, use_bose=True, mask_bragg=True)
    figs = []
    if labels == None:
        labels = sf_files
    for qpt in qpts_idx:
        print(f'Plotting sf for {cut} at qpt:{qpt} {qpts[0][qpt]}')
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


def fnames_to_paths(material, cut, fnames):
    paths = []
    for fname in fnames:
        if fname.endswith('.dat'):
            model = 'ab2tds'
        elif fname.endswith('.csv') or fname.startswith('sqw'):
            model = 'oclimax'
        else:
            model = 'euphonic'
        paths.append(get_path(material, cut, model, fname))
    return paths


def get_path(material, cut, model, fname):
    return os.path.join('..', '..', material, cut, model, fname)

# High error q-points
ab2tds_filenames = ['alongthelineF_300K.dat',
                    'sf_phonons_300K.json',
                    'sf_fc_300K.json']
ab2tds_labels = ['CASTEP phonons, Ab2tds structure factors',
                 'CASTEP phonons, Euphonic structure factors',
                 'Euphonic phonons, Euphonic structure factors']
figs = plot_sf('quartz', '2ph_m4_0_qe', ab2tds_filenames, [50],
               labels=ab2tds_labels)

oclimax_lzo_filenames = ['La2Zr2O7_2Dmesh_scqw_300K.csv',
                         'sqw_euphonic_ph_300K.json',
                         'sqw_euphonic_300K.json']
oclimax_quartz_filenames = ['quartz_2Dmesh_scqw_300K.csv',
                            'sqw_euphonic_ph_300K.json',
                            'sqw_euphonic_300K.json']
oclimax_nb_filenames = ['nb_2Dmesh_scqw_300K.csv',
                        'sqw_euphonic_ph_300K.json',
                        'sqw_euphonic_300K.json']
oclimax_labels=['CASTEP phonons, Oclimax intensities',
                'CASTEP phonons, Euphonic intensities',
                'Euphonic phonons, Euphonic intensities']
figs = plot_sqw('lzo', 'hh2_qe_fine', oclimax_lzo_filenames, [66],
                labels=oclimax_labels)

# Selection of other q-points
figs = plot_sqw('lzo', 'kagome_qe', oclimax_lzo_filenames, [6],
               labels=oclimax_labels)
figs = plot_sqw('lzo', 'hh2_qe_fine', oclimax_lzo_filenames, [36],
               labels=oclimax_labels)
figs = plot_sqw('quartz', '2ph_m4_0_qe', oclimax_quartz_filenames, [67],
               labels=oclimax_labels)
figs = plot_sqw('quartz', '30L_qe_fine', oclimax_quartz_filenames, [185],
               labels=oclimax_labels)
figs = plot_sqw('nb', '110_qe', oclimax_nb_filenames, [40],
               labels=oclimax_labels)
figs = plot_sqw('nb', 'm110_qe', oclimax_nb_filenames, [40],
               labels=oclimax_labels)

mpl.pyplot.show()

