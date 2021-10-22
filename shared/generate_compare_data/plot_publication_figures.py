import matplotlib
#matplotlib.rcParams['font.family'] = 'serif'
#matplotlib.rcParams['font.size'] = 18
#matplotlib.rcParams['font.size'] = 11

import os

import numpy as np
import matplotlib as mpl

from euphonic.spectra import Spectrum2D
from compare_sqw import main as compare_sqw_main
from compare_sqw import get_scaled_sqws
from util import plot_at_qpt, get_lim, get_qpts, get_euphonic_fpath


def plot_sqw(material, cut, temp, code, qpts_idx, labels=None, ptype=None,
             yscale=None, loc=2, min_e=None):
    sqw_files = get_sqw_fnames(material, cut, temp, code)

    mask_negative = (code == 'ab2tds')
    sqws, ebins = get_scaled_sqws(
        sqw_files, mask_bragg=True, mask_negative=mask_negative)
    plot_ebins = Spectrum2D._bin_edges_to_centres(ebins[0])
    qpts = get_qpts(material, cut)

    figs = []
    if labels == None:
        labels = sqw_files
    if ptype == 'scatter':
        plot_zeros = False
    else:
        plot_zeros = True
    xlim = [plot_ebins[0], plot_ebins[-1]]
    if min_e:
        xlim[0] = min_e
    for qpt in qpts_idx:
        print(f'Plotting sqw for {cut} at qpt:{qpt} {qpts[qpt]}')
        fig = plot_at_qpt(
                [x[qpt] for x in sqws],
                labels, x=plot_ebins,
                x_title='Energy (meV)', y_title='Intensity',
                noshow=True,
                ptype=ptype,
                plot_zeros=plot_zeros,
                xlim=xlim,
                **{'loc': loc})
        ax = fig.get_axes()[0]
        # Remove tick labels - they have been multiplied by an arbitrary scaling factor
        ax.set_yticklabels([])
#        rel_err_lim = get_lim(sqws[0])
#        ax.plot(ax.get_xlim(), [rel_err_lim, rel_err_lim], color='k', ls='--', label='Limit')
#        ax.legend()
        if yscale is not None:
            ax.set_ylim(0, ax.get_ylim()[1]*yscale)
        else:
            ax.set_ylim(0)
        figs.append(fig)
    return figs


def plot_sqw_residual(material, cut, temp, code, qpts_idx, labels=None,
                      loc=2, ptype=None, min_e=None):
    sqw_files = get_sqw_fnames(material, cut, temp, code)
    mask_negative = (code == 'ab2tds')
    sqws, ebins = get_scaled_sqws(
        sqw_files, mask_bragg=True, mask_negative=mask_negative)
    plot_ebins = Spectrum2D._bin_edges_to_centres(ebins[0])
    figs = []
    if labels == None:
        labels = sqw_files
    qpts = get_qpts(material, cut)
    xlim = [plot_ebins[0], plot_ebins[-1]]
    if min_e:
        xlim[0] = min_e
    from util import markers, line_colours, marker_sizes
    for qpt in qpts_idx:
        print(f'Plotting sqw residual for {cut} at qpt:{qpt} {qpts[qpt]}')
        fig = plot_at_qpt(
                [x[qpt] - sqws[0][qpt] for x in sqws[1:]],
                labels[1:], x=plot_ebins,
                x_title='Energy (meV)', y_title='Intensity Residual',
                noshow=True,
                ptype=ptype, lc=line_colours[1:], marks=markers[1:],
                msizes=marker_sizes[1:], plot_zeros=False, xlim=xlim,
                **{'loc': loc})
        figs.append(fig)
    return figs


def plot_sqw_rel_err(material, cut, temp, code, qpts_idx, labels=None, ptype=None,
                     yscale=None, loc=2, min_e=None):
    sqw_files = get_sqw_fnames(material, cut, temp, code)
    rel_errs = []
    rel_idxs = []
    for sqw in sqw_files[1:]:
        _, _, rel_err, rel_idx, _ = compare_sqw_main(
        ['--sqw1', sqw_files[0], '--sqw2', sqw, '--mask-bragg'])
        rel_errs.append(rel_err*100)
        rel_idxs.append(rel_idx)

    sqw = Spectrum2D.from_json_file(sqw_files[0])
    plot_ebins = Spectrum2D._bin_edges_to_centres(sqw.y_data.magnitude)
    figs = []
    if labels == None:
        labels = sqw_files
    qpts = get_qpts(material, cut)
    if ptype == 'scatter':
        plot_zeros = False
    else:
        plot_zeros = True
    xlim = [plot_ebins[0], plot_ebins[-1]]
    if min_e:
        xlim[0] = min_e
    from util import markers, line_colours, marker_sizes
    for qpt in qpts_idx:
        print(f'Plotting sqw err for {cut} at qpt:{qpt} {qpts[qpt]}')
        # Only plot relative diffs that come from values above a certain
        # tolerance (i.e. the ones that were used to calculate the mean)
        # - otherwise there are unrepresantative high values
        y_idx = rel_idxs[0][1][np.where(rel_idxs[0][0] == qpt)[0]]
        fig = plot_at_qpt(
                [x[qpt][y_idx] for x in rel_errs],
                labels[1:], x=plot_ebins[y_idx],
                x_title='Energy (meV)', y_title='Relative Percentage Difference',
                noshow=True,
                ptype=ptype, lc=line_colours[1:], marks=markers[1:],
                msizes=marker_sizes[1:], plot_zeros=True, xlim=xlim,
                **{'loc': loc})
        ax = fig.get_axes()[0]
        if yscale is not None:
            ax.set_ylim(0, ax.get_ylim()[1]*yscale)
        else:
            ax.set_ylim(0)
        figs.append(fig)
    return figs


def get_sqw_fnames(material, cut, temp, code):
    sqw_files = []
    sqw_files.append(get_euphonic_fpath(material, code, 'sqw', temp, cut))
    sqw_files.append(get_euphonic_fpath(material, 'euphonic', 'sqw',
                                        temp, cut, from_fc=False))
    sqw_files.append(get_euphonic_fpath(material, 'euphonic', 'sqw',
                                        temp, cut, from_fc=True))
    return sqw_files


with mpl.style.context('pub.mplstyle'):
    # High  q-points
    ab2tds_labels = ['Ab2tds',  'Euphonic & CASTEP Interpolation',
                     'Euphonic & Euphonic Interpolation']
    fig = plot_sqw('quartz', '30L_qe_fine', '300', 'ab2tds', [153],
                   labels=ab2tds_labels, ptype='scatter', min_e=-0.1,
                   loc=1)
    mpl.pyplot.savefig('figures/quartz_ab2tds_30L_qe_fine_q153_m1.5.png')


    oclimax_labels = ['Oclimax',  'Euphonic & CASTEP Interpolation',
                      'Euphonic & Euphonic Interpolation']
    figs = plot_sqw('lzo', 'kagome_qe', '300', 'oclimax', [41],
                    labels=oclimax_labels, ptype='scatter', yscale=0.425,
                    min_e=-100)
    mpl.pyplot.savefig('figures/lzo_oclimax_kagome_qe_q41_m4.1.png')
    figs = plot_sqw_rel_err('lzo', 'kagome_qe', '300', 'oclimax', [41],
                            labels=oclimax_labels, ptype='scatter', yscale=1.3,
                            min_e=-100)
    mpl.pyplot.savefig('figures/lzo_oclimax_relerr_kagome_qe_q41_m4.1.png')
#figs = plot_sqw_residual('lzo', 'kagome_qe', '300', 'oclimax', [41],
#                         labels=oclimax_labels, ptype='scatter')

# Selection of other q-points
#figs = plot_sqw('lzo', 'hh2_qe_fine', oclimax_lzo_filenames, [36],
#               labels=oclimax_labels, ptype='scatter', yscale=1.25)
#mpl.pyplot.savefig('figures/appendix/lzo_oclimax_hh2_qe_fine_q36_7.1.pdf')
#figs = plot_sqw_rel_err('lzo', 'hh2_qe_fine', oclimax_lzo_filenames, [36],
#                        labels=oclimax_labels, ptype='scatter', yscale=1.2)
#mpl.pyplot.savefig('figures/appendix/lzo_oclimax_relerr_hh2_qe_fine_q36_7.1.pdf')
#figs = plot_sqw('quartz', '2ph_m4_0_qe', oclimax_quartz_filenames, [67],
#               labels=oclimax_labels, ptype='scatter')
#mpl.pyplot.savefig('figures/appendix/quartz_oclimax_2ph_m4_0_qe_q67_m0.6.pdf')
#figs = plot_sqw_rel_err('quartz', '2ph_m4_0_qe', oclimax_quartz_filenames, [67],
#                        labels=oclimax_labels, ptype='scatter', yscale=1.2)
#mpl.pyplot.savefig('figures/appendix/quartz_oclimax_relerr_2ph_m4_0_qe_q67_m0.6.pdf')
#figs = plot_sqw('quartz', '30L_qe_fine', oclimax_quartz_filenames, [185],
#               labels=oclimax_labels, ptype='scatter', yscale=1.25)
#mpl.pyplot.savefig('figures/appendix/quartz_oclimax_30L_qe_fine_q185_m2.3.pdf')
#figs = plot_sqw_rel_err('quartz', '30L_qe_fine', oclimax_quartz_filenames, [185],
#               labels=oclimax_labels, ptype='scatter', yscale=1.2)
#mpl.pyplot.savefig('figures/appendix/quartz_oclimax_relerr_30L_qe_fine_q185_m2.3.pdf')
#figs = plot_sqw('nb', '110_qe', oclimax_nb_filenames, [40],
#               labels=oclimax_labels, ptype='scatter')
#mpl.pyplot.savefig('figures/appendix/nb_oclimax_110_qe_q40_1.2.pdf')
#figs = plot_sqw_rel_err('nb', '110_qe', oclimax_nb_filenames, [40],
#                        labels=oclimax_labels, ptype='scatter', loc=1)
#mpl.pyplot.savefig('figures/appendix/nb_oclimax_relerr_110_qe_q40_1.2.pdf')
#figs = plot_sqw('nb', 'm110_qe', oclimax_nb_filenames, [40],
#               labels=oclimax_labels, ptype='scatter')
#mpl.pyplot.savefig('figures/appendix/nb_oclimax_m110_qe_q40_0.8_1.2.pdf')
#figs = plot_sqw_rel_err('nb', 'm110_qe', oclimax_nb_filenames, [40],
#                        labels=oclimax_labels, ptype='scatter', loc=3)
#mpl.pyplot.savefig('figures/appendix/nb_oclimax_relerr_m110_qe_q40_0.8_1.2.pdf')

#mpl.pyplot.show()

