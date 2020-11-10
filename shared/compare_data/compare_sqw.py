import argparse
import numpy as np
import matplotlib.pyplot as plt
from euphonic import Spectrum2D
from euphonic.util import is_gamma
from util import (calc_abs_error, calc_rel_error, get_scaling,
                  plot_at_qpt, get_max_rel_error_idx)

def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    sqw1, ebins1 = get_sqw(args.sqw1)
    sqw2, ebins2 = get_sqw(args.sqw2)

    if args.mask_bragg:
        low_e_bins = np.where(np.absolute(ebins1) < 1)
        sqw1[:, low_e_bins] = 0
        sqw2[:, low_e_bins] = 0

    # Don't scale if they're both from euphonic
    if not (args.sqw1.endswith('.json') and args.sqw2.endswith('.json')):
        scale = get_scaling(sqw1, sqw2)
        sqw2 *=scale
    abs_error = calc_abs_error(sqw1, sqw2)
    rel_error = calc_rel_error(sqw1, sqw2)
    print(f'\nResults for {args.sqw1} {args.sqw2}')
    print((f'Absolute Error - mean: {np.mean(abs_error)} '
           f'max: {np.max(abs_error)} min: {np.min(abs_error)}'))
    print((f'Relative Error - mean: {np.mean(rel_error) } '
           f'max: {np.max(rel_error)} min: {np.min(rel_error)}'))

    if args.qpts:
        qpts = [int(x) for x in args.qpts.split(',')]
        for qpt in qpts:
            plot_at_qpt(qpt, sqw1[qpt], sqw2[qpt],
                    [args.sqw1, args.sqw2], x=ebins1[:len(sqw1[qpt])])

    if args.n:
        idx = get_max_rel_error_idx(sqw1, sqw2, n=int(args.n))
        print(f'Points with largest mean relative error: {idx}')


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
        '--mask-bragg', action='store_true',
        help=('Mask out Bragg peaks (sets intensities in lowest energy '
              'bin to zero)'))
    parser.add_argument(
        '-n',
        help='Output the n points with the largest errors')
    return parser
    

if __name__ == '__main__':
    main()
