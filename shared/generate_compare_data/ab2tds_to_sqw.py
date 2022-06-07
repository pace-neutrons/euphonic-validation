"""
Converts Ab2tds data from a alongthelineF.dat file
containing mode-resolved structure factors (with Bose
factor) to a Euphonic Spectrum2D object by binning in
energy
"""
import os
import re
import argparse

import numpy as np
import matplotlib.pyplot as plt
from euphonic import StructureFactor, ureg
from euphonic.util import is_gamma

from util import (get_ab2tds_fpath, get_oclimax_fpath,
                  get_euphonic_fpath)
from generate_euphonic_sqw import read_oclimax_ebins

def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    ab2tds_fname = get_ab2tds_fpath(args.material, args.cut, args.temp)
    sf_vals, freqs, qpts = get_ab2tds_sf(ab2tds_fname)

    euphonic_fname = get_euphonic_fpath(args.material, code='euphonic', obj='sf',
                                        temperature=args.temp, cut=args.cut,
                                        from_fc=False)
    euphonic_sf = StructureFactor.from_json_file(euphonic_fname)


    # Use Euphonic frequencies for binning, frequencies in the Ab2tds
    # file have undergone unit conversions so may be slightly different
    # and result in different S(Q, w) binning
    sf_obj = StructureFactor(euphonic_sf.crystal, euphonic_sf.qpts,
                             euphonic_sf.frequencies,
                             sf_vals*ureg('mbarn'),
                             temperature=euphonic_sf.temperature)

    # Use ebins from the OClimax .params input file, which seems to
    # result in more accurate binning of data compared with using the
    # energy bins from the .csv output file. Now Euphonic, Ab2tds and
    # OClimax-generated intensities will have the same binning for
    # better comparison
    oclimax_fname = get_oclimax_fpath(args.material, args.cut,
                                      temp=args.temp,
                                      in_file=True)
    ebin_edges = read_oclimax_ebins(oclimax_fname)

    # Use calc_bose=False because the bose factor has already been applied
    # to Ab2tds data
    sqw = sf_obj.calculate_sqw_map(ebin_edges*ureg('meV'), calc_bose=False)
    sqw.to_json_file(get_euphonic_fpath(args.material, 'ab2tds', 'sqw',
                                        args.temp, cut=args.cut))

def get_ab2tds_sf(filename):
    data = np.loadtxt(filename)
    qpts = data[:, :3]
    freqs = data[:, range(3, data.shape[1], 3)]
    sf = data[:, range(4, data.shape[1], 3)]
    anti_sf = data[:, range(5, data.shape[1], 3)]
    return sf, freqs, qpts

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
