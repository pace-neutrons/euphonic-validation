import argparse
import os
import numpy as np
from util import find_file
from euphonic import ureg, ForceConstants, QpointPhononModes, DebyeWaller
from euphonic.util import is_gamma

def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    cut_dir = os.path.abspath(args.cut_dir)
    if args.freqs:
        castep_phonon_file = find_file(os.path.join(cut_dir, 'castep'),
                                       '*.phonon')
        print(f'Reading frequencies from {castep_phonon_file}')
        phonons = QpointPhononModes.from_castep(castep_phonon_file)
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
        castep_fc_file = find_file(
            os.path.join(cut_dir, '..', 'shared', 'castep'),
            '*.castep_bin')
        print(f'Reading force constants from {castep_fc_file}')
        fc = ForceConstants.from_castep(castep_fc_file)

        qpts_file = find_file(os.path.join(cut_dir), '*_qpts.txt')
        print(f'Reading qpts from {qpts_file}')
        qpts = np.loadtxt(qpts_file, delimiter=',')
        print('Calculating frequencies...')
        phonons = fc.calculate_qpoint_phonon_modes(qpts, asr='reciprocal',
                                                   splitting=True,
                                                   insert_gamma=False)

    fm = ureg.fm
    sl = {'Si': 4.1491*fm, 'O': 5.803*fm, 'La': 8.24*fm, 'Zr': 7.16*fm,
          'Nb': 7.054*fm}
    if args.dw:
        print(f'Reading DebyeWaller from {args.dw}')
        dw = DebyeWaller.from_json_file(args.dw)
    else:
        dw = None
    sf = phonons.calculate_structure_factor(
        sl, dw=dw)
    if args.o:
        out_file = args.o 
    else:
        freq_str = 'phonons' if args.freqs else 'fc'
        temp_str = f'_{str(int(dw.temperature.magnitude))}K' if dw else ''
        out_file = os.path.abspath(os.path.join(
            cut_dir, 'euphonic', f'sf_{freq_str}{temp_str}.json'))
    sf.to_json_file(out_file)
    return out_file


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('cut_dir')
    parser.add_argument(
        '--dw',
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
