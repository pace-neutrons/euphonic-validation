import argparse
import os
import fnmatch

import numpy as np

from euphonic import ureg, ForceConstants, QpointPhononModes
from euphonic.util import mp_grid
from util import get_euphonic_fpath, get_dir, get_fc, get_phonon_modes


def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    if args.freqs or args.reduced:
        grid_str = args.grid.replace(',', '')
        if args.reduced:
            pattern = f'*{grid_str}-grid*'
        else:
            pattern = f'*{grid_str}*full*'
        phonons = get_phonon_modes(args.material, 'shared',
                                   pattern)

    if not args.freqs:
        fc = get_fc(args.material)
        if args.reduced:
            qpts = phonons.qpts
            weights = phonons.weights
        else:
            qpts = mp_grid([int(x) for x in args.grid.split(',')])
            weights = None
        print('Calculating frequencies...')
        phonons = fc.calculate_qpoint_phonon_modes(qpts, asr='reciprocal',
                                                   splitting=False,
                                                   weights=weights)

    dw = phonons.calculate_debye_waller(float(args.temp)*ureg('K'),
                                        symmetrise=False)

    if args.o:
        out_file = args.o 
    else:
        out_file = get_euphonic_fpath(
                args.material, 'euphonic', 'dw', args.temp,
                from_fc=bool(not args.freqs), grid=args.grid,
                reduced=args.reduced)
    dw.to_json_file(out_file)
    return out_file


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('material')
    parser.add_argument(
        '--grid', required=True,
        help='MP Grid for Debye-Waller factor e.g. --grid 5,5,5')
    parser.add_argument(
        '--temp', required=True,
        help='Temperature for Debye-Waller factor in K')
    parser.add_argument(
        '-o',
        help='Output file')
    parser.add_argument(
        '--reduced', action='store_true',
        help='Use symmetry-reduced MP grid')
    parser.add_argument(
        '--freqs', action='store_true',
        help='Use precalculated frequencies from .phonon')
    return parser

if __name__ == '__main__':
    main()
