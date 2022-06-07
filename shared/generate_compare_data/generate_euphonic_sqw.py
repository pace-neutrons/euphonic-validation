"""
Generate a Euphonic Spectrum2D object containing S(Q, w) from
a StructureFractor .json file generated with
generate_euphonic_sf.py Energy bins are read from an OClimax
.params input file
"""
import argparse
import os
import numpy as np
import re
from euphonic import ureg, StructureFactor
from euphonic.plot import plot_2d
from util import find_file, get_dir, get_euphonic_fpath


def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)
    from_fc = bool(not args.freqs)
    reduced = bool(args.reduced)

    sf_file = get_euphonic_fpath(args.material, 'euphonic', 'sf', args.temp,
                                 cut=args.cut, from_fc=from_fc, reduced=reduced)
    sf = StructureFactor.from_json_file(sf_file)
    ebin_edges = read_oclimax_ebins(
        find_file(get_dir(args.material, cut=args.cut, code='oclimax'),
                  '*.params.copy'))
    sqw = sf.calculate_sqw_map(ebin_edges*ureg('meV'))

    if args.ofig:
        fig = plot_2d(sqw, vmax=10)
        fig_file = os.path.abspath(args.ofig)
        fig.savefig(fig_file)
        print(f'Written to {fig_file}')

    if args.osqw:
        out_file = args.osqw
    else:
        out_file = get_euphonic_fpath(
            args.material, 'euphonic', 'sqw', args.temp,
            cut=args.cut, from_fc=from_fc, reduced=reduced)
    sqw.to_json_file(out_file)

def read_oclimax_ebins(filename):
    print(f'Reading oclimax bins from {filename}')
    with open(filename, 'r') as f:
        data = ''.join(f.readlines())
    min_e = float(re.search('MINE\s*=\s*(-?\d+\.?\d*)\s*', data).group(1))
    max_e = float(re.search('MAXE\s*=\s*(-?\d+\.?\d*)\s*', data).group(1))
    bin_size = float(re.search('dE\s*=\s*(\d+\.\d+)\s*', data).group(1))
    ebin_edges = np.arange(min_e, max_e + 1.01*bin_size, bin_size)
    return ebin_edges

def read_oclimax_ebins_csv(filename):
    n_e_bins = 0
    with open(filename, 'r') as f:
        while True:
            n_e_bins += 1
            if f.readline().strip() == '':
                break
    n_e_bins -= 5  # Subtract header lines
    data = np.genfromtxt(filename, delimiter=',', invalid_raise=False)
    ebins = data[:n_e_bins, 1] # left ebins
    ebin_width = np.mean(np.diff(ebins))
    return np.append(ebins, ebins[-1] + ebin_width)

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('material')
    parser.add_argument('cut')
    parser.add_argument(
        '--temp', required=True,
        help='Temperature in K')
    parser.add_argument(
        '--freqs', action='store_true',
        help='Use SF generated from precalculated phonon frequencies')
    parser.add_argument(
        '--reduced', action='store_true',
        help='Use SF generated with a debye-waller factor from a reduced'
             '(rather than full) grid')
    parser.add_argument(
        '--osqw',
        help='Output sqw .json file')
    parser.add_argument(
        '--ofig',
        help='Output figure file')

    return parser


if __name__ == '__main__':
    main()
