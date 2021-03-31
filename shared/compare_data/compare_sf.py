import argparse
import numpy as np
import matplotlib.pyplot as plt
from euphonic import StructureFactor
from euphonic.util import is_gamma
from util import (get_abs_error_and_idx, get_rel_error_and_idx,
                  plot_at_qpt, get_scaling, get_max_rel_error_idx)

def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    sf_sum, qpts, dg_freqs = get_summed_and_scaled_sfs(
        [args.sf1, args.sf2], use_bose=not args.nobose,
        mask_bragg=args.mask_bragg)

    all_abs_error, abs_idx = get_abs_error_and_idx(sf_sum[0], sf_sum[1])
    all_rel_error, rel_idx, lim = get_rel_error_and_idx(sf_sum[0], sf_sum[1])
    abs_error = all_abs_error[abs_idx]
    rel_error = all_rel_error[rel_idx]
    print(f'\nResults for {args.sf1} {args.sf2}')
    print((f'Absolute Error - mean: {np.mean(abs_error)} '
           f'max: {np.max(abs_error)} min: {np.min(abs_error)}'))
    print((f'Relative Error - mean: {np.mean(rel_error) } '
           f'max: {np.max(rel_error)} min: {np.min(rel_error)}'))

    if args.n:
        idx = get_max_rel_error_idx(sf_sum[0], sf_sum[1], n=int(args.n))
        print(f'Points with largest mean relative error: {idx}')

    if args.qpts:
        figs = []
        qpts_idx = [int(x) for x in args.qpts.split(',')]
        for qpt in qpts_idx:
            # As the structure factors have been summed, the last
            # n entries are zero (where n is the number of
            # degenerate modes)
            zero_idx = np.where(dg_freqs[qpt] == 0)[0]
            if len(zero_idx) > 0:
                idx = zero_idx[0]
            else:
                idx = dg_freqs.shape[1]
            fig = plot_at_qpt(
                [sf_sum[0][qpt, :idx], sf_sum[1][qpt, :idx]],
                [args.sf1, args.sf2], x=dg_freqs[qpt, :idx],
                x_title='Mode Frequency (meV)', y_title='Intensity',
                noshow=args.noshow, title=f'Q-point: {qpts[0][qpt]}',
                **{'loc': 1, 'prop': {'size': 8}})
            if fig is not None:
                figs.append(fig)
        return figs
    else:
        return all_abs_error, abs_idx, all_rel_error, rel_idx, lim


def get_sf(filename, **kwargs):
    if filename.endswith('.json'):
        return get_euphonic_sf(filename, **kwargs)
    else:
        return get_ab2tds_sf(filename)


def get_euphonic_sf(filename, use_bose=True):
     sf = StructureFactor.from_json_file(filename)
     sf_val = sf.structure_factors.magnitude
     if sf.temperature is not None and use_bose:
         bose = sf._bose_factor(sf.temperature)
         sf_val *= (1 + bose)
     return sf_val, sf.frequencies.magnitude, sf.qpts


def get_ab2tds_sf(filename):
    data = np.loadtxt(filename)
    qpts = data[:, :3]
    freqs = data[:, range(3, data.shape[1], 3)]
    sf = data[:, range(4, data.shape[1], 3)]
    anti_sf = data[:, range(5, data.shape[1], 3)]
    return sf, freqs, qpts


def get_degenerate_modes(frequencies, TOL=0.5):
    idx = np.zeros(frequencies.shape, dtype=np.int32)
    dg_freqs = np.zeros(frequencies.shape)
    for i, freqs in enumerate(frequencies):
        diff = np.append(2*TOL, np.diff(freqs))
        unique_index = np.where(diff > TOL)[0]
        x = np.zeros((freqs.shape), dtype=np.int32)
        x[unique_index] = 1
        idx[i] = np.cumsum(x) - 1
        dg_freqs[i, :len(unique_index)] = frequencies[i, unique_index]
    return idx, dg_freqs


def calc_sf_sum(bin_idx, sf):
    sf_sum = np.zeros(sf.shape)
    for i in range(len(sf)):
        summed = np.bincount(bin_idx[i], sf[i])
        sf_sum[i, :len(summed)] = summed
    return sf_sum
 
def get_summed_and_scaled_sfs(sf_files, use_bose=True, mask_bragg=True):
    sf_arr = []
    sf_sum_arr = []
    freq_arr = []
    qpt_arr = []

    for sf_file in sf_files:
        sf, freqs, qpts = get_sf(sf_file, use_bose=use_bose)
        sf_arr.append(sf)
        freq_arr.append(freqs)
        qpt_arr.append(qpts)
    dg_modes, dg_freqs = get_degenerate_modes(freq_arr[0])

    if mask_bragg:
        mask = np.ones(sf_arr[0].shape, dtype=np.int32)
        for gamma_idx in np.where(is_gamma(qpt_arr[0]))[0]:
            mask[gamma_idx, :3] = 0
        for sf in sf_arr:
            sf *= mask

    for sf in sf_arr:
        sf_sum_arr.append(calc_sf_sum(dg_modes, sf))

    # Don't scale if they're both from euphonic
    for i, sf_file in enumerate(sf_files[1:]):
            if not (sf_files[0].endswith('.json') and sf_file.endswith('.json')):
                scale = get_scaling(sf_sum_arr[0], sf_sum_arr[i + 1])
                sf_sum_arr[i + 1] *= scale

    return sf_sum_arr, qpt_arr, dg_freqs

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o',
        help='Output file')
    parser.add_argument(
        '--sf1', required=True,
        help='First file containing sf results')
    parser.add_argument(
        '--sf2', required=True,
        help='Second file containing sf results')
    parser.add_argument(
        '--qpts',
        help='Q-points idx to plot')
    parser.add_argument(
        '--mask-bragg', action='store_true',
        help=('Mask out Bragg peaks (acoustic mode structure factors '
              'at gamma points'))
    parser.add_argument(
        '--nobose', action='store_true',
        help='Don\'t add the Bose factor to the Euphonic calculation')
    parser.add_argument(
        '--noshow', action='store_true',
        help='Don\'t show the figure(s), just return them')
    parser.add_argument(
        '-n',
        help='Output the n points with the largest errors')
    return parser
    

if __name__ == '__main__':
    main()
