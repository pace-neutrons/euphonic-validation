import argparse
import os

import numpy as np

from euphonic import ureg, ForceConstants, QpointPhononModes, DebyeWaller
from euphonic.util import is_gamma
from util import (get_euphonic_fpath, get_dir, get_fc, get_phonon_modes,
                  find_file)

def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)
    if args.freqs:
        phonons = get_phonon_modes(args.material, args.cut, '*')
        # Remove duplicated gamma points in the case of splitting - Ab2tds
        # and OClimax squash these into one point whereas Euphonic doesn't
        # so force this behaviour to avoid index errors
        gamma_i = np.where(is_gamma(phonons.qpts))[0]
        split_qpts = gamma_i[:-1][np.diff(gamma_i) == 1]
        phonons = QpointPhononModes(
            phonons.crystal,
            np.delete(phonons.qpts, split_qpts, axis=0),
            np.delete(phonons.frequencies.magnitude, split_qpts,
                      axis=0)*phonons.frequencies.units,
            np.delete(phonons.eigenvectors, split_qpts, axis=0))
    else:
        fc = get_fc(args.material)
        qpts_file = find_file(
            get_dir(args.material, cut=args.cut), '*_qpts.txt')
        print(f'Reading qpts from {qpts_file}')
        qpts = np.loadtxt(qpts_file, delimiter=',')
        print('Calculating frequencies...')
        phonons = fc.calculate_qpoint_phonon_modes(qpts, asr='reciprocal',
                                                   splitting=False,
                                                   insert_gamma=False)

    print(f'Reading DebyeWaller from {args.dw}')
    dw = DebyeWaller.from_json_file(args.dw)

    sf = phonons.calculate_structure_factor(dw=dw)
    if args.o:
        out_file = args.o 
    else:
        temp_str = str(int(dw.temperature.magnitude))
        out_file = get_euphonic_fpath(
            args.material, 'euphonic', 'sf', temp_str,
            cut=args.cut, from_fc=bool(not args.freqs))
    sf.to_json_file(out_file)
    return out_file


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('material')
    parser.add_argument('cut')
    parser.add_argument(
        '--dw', required=True,
        help='The .json file containing the Debye-Waller factor')
    parser.add_argument(
        '-o',
        help='Output file')
    parser.add_argument(
        '--freqs', action='store_true',
        help='Use precalculated frequencies from .phonon')
    return parser


if __name__ == '__main__':
    main()
