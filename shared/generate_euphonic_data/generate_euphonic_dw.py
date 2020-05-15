import argparse
import os
import fnmatch
import numpy as np
from euphonic import ureg, ForceConstants, QpointPhononModes
from euphonic.util import mp_grid


def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    material_dir = os.path.abspath(args.material_dir)

    grid_str = args.grid.replace(',', '')
    if args.freqs:
        fname = '*-' + grid_str + '-grid.phonon'
        castep_phonon_file = find_file(
            os.path.join(material_dir, 'shared', 'castep'), fname)
        print(f'Reading frequencies from {castep_phonon_file}')
        phonons = QpointPhononModes.from_castep(castep_phonon_file)
    else:
        castep_fc_file = find_file(
            os.path.join(material_dir, 'shared', 'castep'),
            '*.castep_bin')
        print(f'Reading force constants from {castep_fc_file}')
        fc = ForceConstants.from_castep(castep_fc_file)

        qpts = mp_grid([int(x) for x in args.grid.split(',')])
        print('Calculating frequencies...')
        phonons = fc.calculate_qpoint_phonon_modes(qpts, asr='reciprocal',
                                                   splitting=False)

    dw = phonons.calculate_debye_waller(float(args.temp)*ureg('K'))

    if args.o:
        out_file = args.o 
    else:
        freq_str = 'phonons' if args.freqs else 'fc'
        out_file = os.path.abspath(
            os.path.join(
                material_dir, 'shared', 'euphonic',
                f'dw_{freq_str}_{grid_str}_{str(args.temp)}K.json'))
    dw.to_json_file(out_file)
    return out_file


def find_file(fdir, pattern):
    for f in os.listdir(fdir):
        if fnmatch.fnmatch(f, pattern):
            return os.path.join(fdir, f)
    raise Exception(f'{pattern} not found in {fdir}')


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('material_dir')
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
