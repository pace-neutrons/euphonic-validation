import argparse
import numpy as np
import matplotlib.pyplot as plt
from euphonic import Spectrum2D
from euphonic.util import _bose_factor, is_gamma
from util import (calc_mean_abs_error, calc_mean_rel_error,
                  get_scaling, plot_at_qpt)

def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    sqw1, ebins1 = get_sqw(args.sqw1)
    sqw2, ebins2 = get_sqw(args.sqw2)

    if args.mask_bragg:
        sqw1[:, 0] = 0
        sqw2[:, 0] = 0

    scale = get_scaling(sqw1, sqw2)
    sqw2 *=scale
    print(f'Results for {args.sqw1} {args.sqw2}')
    print(f'Mean abs error: {calc_mean_abs_error(sqw1, sqw2)}')
    print(f'Mean rel error: {calc_mean_rel_error(sqw1, sqw2)}')

    if args.qpts:
        qpts = [int(x) for x in args.qpts.split(',')]
        for qpt in qpts:
            plot_at_qpt(qpt, sqw1[qpt], sqw2[qpt],
                    [args.sqw1, args.sqw2], x=ebins1[:len(sqw1[qpt])])


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
    return parser
    

if __name__ == '__main__':
    main()
