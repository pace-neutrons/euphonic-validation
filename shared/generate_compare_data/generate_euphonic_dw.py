import argparse
import os
import fnmatch

import numpy as np

from euphonic import ureg, ForceConstants, QpointPhononModes
from euphonic.util import mp_grid
from util import get_euphonic_fpath, get_dir, get_fc


def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    castep_dir = get_dir(args.material, 'castep')

    if args.freqs:
        grid_str = args.grid.replace(',', '')
        fname = '*-' + grid_str + '-full-grid.phonon'
        castep_phonon_file = find_file(castep_dir, fname)
        print(f'Reading frequencies from {castep_phonon_file}')
        phonons = QpointPhononModes.from_castep(castep_phonon_file)
    else:
        fc = get_fc(args.material)
        qpts = mp_grid([int(x) for x in args.grid.split(',')])
        print('Calculating frequencies...')
        phonons = fc.calculate_qpoint_phonon_modes(qpts, asr='reciprocal',
                                                   splitting=False)

    dw = phonons.calculate_debye_waller(float(args.temp)*ureg('K'),
                                        symmetrise=False)

    if args.o:
        out_file = args.o 
    else:
        out_file = get_euphonic_fpath(
                args.material, 'euphonic', 'dw', args.temp,
                from_fc=bool(not args.freqs), grid=args.grid)
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
        '--freqs', action='store_true',
        help='Use precalculated frequencies from .phonon')
    return parser

if __name__ == '__main__':
    main()
