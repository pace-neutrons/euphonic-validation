import argparse
import os
import numpy as np
from euphonic import ureg, StructureFactor
from euphonic.plot import plot_2d


def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    sf = StructureFactor.from_json_file(args.sf_file)
    cut_dir = os.path.abspath(os.path.dirname(os.path.dirname(args.sf_file)))

    if args.ab2tds:
        ebin_edges = get_ebin_edges(
            np.loadtxt(os.path.join(cut_dir, 'ab2tds', 'ebins.dat')))
        sqw = sf.calculate_sqw_map(ebin_edges*ureg('meV'))
        fig, ims = plot_2d(sqw, ratio=1.0, vmax=7e-10)

    fig_file = os.path.abspath(args.ofig)
    fig.savefig(fig_file)
    print(f'Written to {fig_file}') 
    sqw.to_json_file(os.path.abspath(args.osqw))


def get_ebin_edges(ebin_centres):
    ebin_edges = np.zeros(len(ebin_centres) + 1)
    ebin_width = np.mean(np.diff(ebin_centres))
    ebin_edges[:-1] = ebin_centres - ebin_width/2
    ebin_edges[-1] = ebin_centres[-1] + ebin_width/2
    return ebin_edges


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'sf_file',
        help='The euphonic StructureFactor .json file to read')
    parser.add_argument(
        '--osqw', default='sqw.json',
        help='Output sqw .json file')
    parser.add_argument(
        '--ofig', default='fig.png',
        help='Output figure file')
    parser.add_argument(
        '--ab2tds', action='store_true',
        help='Replicate Ab2tds output')
    
    return parser


if __name__ == '__main__':
    main()
