import argparse
import numpy as np
import matplotlib.pyplot as plt
from euphonic import StructureFactor
from euphonic.util import _bose_factor, is_gamma
from util import (calc_abs_error, calc_rel_error,
                  plot_at_qpt, get_scaling, get_max_rel_error_idx)

def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    sf1, freqs1, qpts1 = get_sf(args.sf1, use_bose=not args.nobose)
    sf2, freqs2, qpts2 = get_sf(args.sf2, use_bose=not args.nobose)
    dg_modes = get_degenerate_modes(freqs1)

    if args.mask_bragg:
        mask = np.ones(sf1.shape, dtype=np.int32)
        for gamma_idx in np.where(is_gamma(qpts1))[0]:
            mask[gamma_idx, :3] = 0
        sf1 *= mask
        sf2 *= mask
    sf_sum1 = calc_sf_sum(dg_modes, sf1)
    sf_sum2 = calc_sf_sum(dg_modes, sf2)

    # Don't scale if they're both from euphonic
    if not (args.sqw1.endswith('.json') and args.sqw2.endswith('.json')):
        scale = get_scaling(sf_sum1, sf_sum2)
        sf_sum2 *=scale
    abs_error = calc_abs_error(sf_sum1, sf_sum2)
    rel_error = calc_rel_error(sf_sum1, sf_sum2)
    print(f'\nResults for {args.sf1} {args.sf2}')
    print((f'Absolute Error - mean: {np.mean(abs_error)} '
           f'max: {np.max(abs_error)} min: {np.min(abs_error)}'))
    print((f'Relative Error - mean: {np.mean(rel_error) } '
           f'max: {np.max(rel_error)} min: {np.min(rel_error)}'))

    if args.n:
        idx = get_max_rel_error_idx(sf_sum1, sf_sum2, n=int(args.n))
        print(f'Points with largest mean relative error: {idx}')

    if args.qpts:
        qpts = [int(x) for x in args.qpts.split(',')]
        for qpt in qpts:
            plot_at_qpt(qpts1[qpt], sf_sum1[qpt], sf_sum2[qpt],
                        [args.sf1, args.sf2])


def get_sf(filename, **kwargs):
    if filename.endswith('.json'):
        return get_euphonic_sf(filename, **kwargs)
    else:
        return get_ab2tds_sf(filename)


def get_euphonic_sf(filename, use_bose=True):
     sf = StructureFactor.from_json_file(filename)
     sf_val = sf.structure_factors.magnitude
     if sf.temperature is not None and use_bose:
         bose = _bose_factor(sf._frequencies,
                             sf._temperature)
         sf_val *= bose
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
    for i, freqs in enumerate(frequencies):
        diff = np.append(2*TOL, np.diff(freqs))
        unique_index = np.where(diff > TOL)[0]
        x = np.zeros((freqs.shape), dtype=np.int32)
        x[unique_index] = 1
        idx[i] = np.cumsum(x) - 1
    return idx


def calc_sf_sum(bin_idx, sf):
    sf_sum = np.zeros(sf.shape)
    for i in range(len(sf)):
        summed = np.bincount(bin_idx[i], sf[i])
        sf_sum[i, :len(summed)] = summed
    return sf_sum
 

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
        '-n',
        help='Output the n points with the largest errors')
    return parser
    

if __name__ == '__main__':
    main()
