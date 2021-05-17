import argparse
import numpy as np
import matplotlib.pyplot as plt
from euphonic import Spectrum2D
from euphonic.util import is_gamma
from util import (get_abs_error_and_idx, get_rel_error_and_idx,
                  get_scaling, plot_at_qpt, get_max_rel_error_idx)

def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    sqws, ebins = get_scaled_sqws([args.sqw1, args.sqw2],
                                  mask_bragg=args.mask_bragg)

    all_abs_error, abs_idx = get_abs_error_and_idx(sqws[0], sqws[1])
    all_rel_error, rel_idx, lim = get_rel_error_and_idx(sqws[0], sqws[1])
    abs_error = all_abs_error[abs_idx]
    rel_error = all_rel_error[rel_idx]
    print(f'\nResults for {args.sqw1} {args.sqw2}')
    print((f'Absolute Error - mean: {np.mean(abs_error)} '
           f'max: {np.max(abs_error)} min: {np.min(abs_error)}'))
    print((f'Relative Error - mean: {np.mean(rel_error) } '
           f'max: {np.max(rel_error)} min: {np.min(rel_error)}'))


    if args.n:
        idx = get_max_rel_error_idx(sqws[0], sqws[1], n=int(args.n))
        print(f'Points with largest mean relative error: {idx}')

    if args.qpts:
        figs = []
        qpts = [int(x) for x in args.qpts.split(',')]
        for qpt in qpts:
            fig = plot_at_qpt(
                [sqws[0][qpt], sqws[1][qpt]],
                [args.sqw1, args.sqw2],
                x=ebins[0][:len(sqws[0][qpt])],
                noshow=args.noshow,
                title=f'Q-point: {qpt}',
                **{'loc': 1, 'prop': {'size': 8}})
            if fig is not None:
                figs.append(fig)
        return figs
    else:
        return all_abs_error, abs_idx, all_rel_error, rel_idx, lim


def get_sqw(filename):
    if filename.endswith('.json'):
        return get_euphonic_sqw(filename)
    else:
        return get_oclimax_sqw(filename)


def get_euphonic_sqw(filename):
     sqw = Spectrum2D.from_json_file(filename)
     sqw_val = sqw.z_data.magnitude
     return sqw.z_data.magnitude, sqw.y_data.magnitude


def get_oclimax_sqw(filename):
    n_e_bins = 0
    with open(filename, 'r') as f:
        while True:
            n_e_bins += 1
            if f.readline().strip() == '':
                break
    n_e_bins -= 5  # Subtract header lines
    data = np.genfromtxt(filename, delimiter=',', invalid_raise=False)
    ebins = data[:n_e_bins, 1]
    qpts = data[::n_e_bins, 0]
    sqw = np.reshape(data[:, 2], (len(qpts), len(ebins)))
    return sqw, ebins

def get_scaled_sqws(sqw_files, mask_bragg=True):
    sqw_arr = []
    ebins_arr = []

    for sqw_file in sqw_files:
        sqw, ebins = get_sqw(sqw_file)
        sqw_arr.append(sqw)
        ebins_arr.append(ebins)

    if mask_bragg:
        low_e_bins = np.where(np.absolute(ebins_arr[0]) < 1)
        for sqw in sqw_arr:
            sqw[:, low_e_bins] = 0

    # Don't scale if they're both from euphonic
    for i, sqw_file in enumerate(sqw_files[1:]):
            if not (sqw_files[0].endswith('.json') and sqw_file.endswith('.json')):
                scale = get_scaling(sqw_arr[0], sqw_arr[i + 1])
                sqw_arr[i + 1] *= scale

    return sqw_arr, ebins_arr


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o',
        help='Output file')
    parser.add_argument(
        '--sqw1', required=True,
        help='First file containing sqw results')
    parser.add_argument(
        '--sqw2', required=True,
        help='Second file containing sqw results')
    parser.add_argument(
        '--qpts',
        help='Q-points idx to plot')
    parser.add_argument(
        '--noshow', action='store_true',
        help='Don\'t show the figure(s), just return them')
    parser.add_argument(
        '--mask-bragg', action='store_true',
        help=('Mask out Bragg peaks (sets intensities in lowest energy '
              'bin to zero)'))
    parser.add_argument(
        '-n',
        help='Output the n points with the largest errors')
    return parser
    

if __name__ == '__main__':
    main()
