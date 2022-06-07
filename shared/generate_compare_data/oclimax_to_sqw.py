"""
Convert an Oclimax .csv output file to a Euphonic Spectrum2D .json
"""
import os
import re
import argparse

import numpy as np
import matplotlib.pyplot as plt
from euphonic import Spectrum2D
from euphonic.util import is_gamma

from util import get_oclimax_fpath, get_euphonic_fpath

def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    oclimax_fname = get_oclimax_fpath(
        args.material, args.cut, in_file=False, temp=args.temp)

    sqw_vals, ebins = get_oclimax_sqw(oclimax_fname)

    euphonic_fname = get_euphonic_fpath(
        args.material, code='euphonic', obj='sqw', temperature=args.temp,
        cut=args.cut, from_fc=False)
    euphonic_sqw = Spectrum2D.from_json_file(euphonic_fname)
    # Use ebins from the Euphonic S(Q,w). These are taken from the OClimax
    # .params input file, which seems to result in more accurate binning of
    # data compared with using the energy bins from the .csv output file
    sqw_obj = Spectrum2D(euphonic_sqw.x_data,
                         euphonic_sqw.y_data,
                         sqw_vals*euphonic_sqw.z_data.units)

    sqw_obj.to_json_file(get_euphonic_fpath(args.material, 'oclimax', 'sqw',
                                            args.temp, cut=args.cut))

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
    parser.add_argument('material')
    parser.add_argument('cut')
    parser.add_argument(
        '--temp', required=True,
        help='Temperature in K')
    return parser
    

if __name__ == '__main__':
    main()
