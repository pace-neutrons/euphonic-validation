import argparse
import numpy as np
import matplotlib.pyplot as plt
from euphonic import StructureFactor
from euphonic.util import _bose_factor

def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    if args.ab2tds:
        qpts, frequencies, sf_ab, _ = get_ab2tds_data(args.ab2tds)
    
    if args.euphonic:
        sf = StructureFactor.from_json_file(args.euphonic)
        sf_eu = sf.structure_factors.magnitude

    dg_modes = get_degenerate_modes(sf.frequencies.magnitude)
    sf_ab_sum = get_sf_sum(dg_modes, sf_ab)
    bose = _bose_factor(sf._frequencies, 100.)
    sf_eu_sum = get_sf_sum(dg_modes, sf_eu*bose)
    scale = get_scaling(sf_eu_sum, sf_ab_sum)
    sf_ab_sum *=scale

    if args.qpts:
        qpts = [int(x) for x in args.qpts.split(',')]
        for qpt in qpts:
            plot_sf(sf.qpts[qpt], sf_eu_sum[qpt], sf_ab_sum[qpt])


def plot_sf(qpt, sf_eu_sum, sf_ab_sum):
    fig, ax = plt.subplots()
    x = np.arange(len(sf_eu_sum))
    ax.plot(x, sf_eu_sum, label='Euphonic')
    ax.plot(x, sf_ab_sum, label='Ab2tds')
    ax.legend()
    fig.suptitle(f'SF at {qpt}')
    fig.show()


def get_ab2tds_data(data_file):
    data = np.loadtxt(data_file)
    qpts = data[:, :3]
    freqs = data[:, range(3, data.shape[1], 3)]
    sf = data[:, range(4, data.shape[1], 3)]
    anti_sf = data[:, range(5, data.shape[1], 3)]
    return qpts, freqs, sf, anti_sf


def get_scaling(sf1, sf2):
    scale = sf1/sf2
    scale = scale[np.logical_and(~np.isnan(scale), ~np.isinf(scale))]
    m = 2.0
    scale_reduced = scale[abs(scale - np.mean(scale)) < m * np.std(scale)]
    scale = np.mean(scale_reduced)
    return scale


def get_degenerate_modes(frequencies, TOL=0.1):
    idx = np.zeros(frequencies.shape, dtype=np.int32)
    # Loop over q-points
    for i, freqs in enumerate(frequencies):
        diff = np.append(2*TOL, np.diff(freqs))
        unique_index = np.where(diff > TOL)[0]
        x = np.zeros((freqs.shape), dtype=np.int32)
        x[unique_index] = 1
        idx[i] = np.cumsum(x) - 1
    return idx


def get_sf_sum(bin_idx, sf):
    sf_sum = np.zeros(sf.shape)
    for i in range(len(sf)):
        summed = np.bincount(bin_idx[i], sf[i])
        sf_sum[i, :len(summed)] = summed
    return sf_sum
 

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o',
        help='Output file')
    parser.add_argument(
        '--euphonic',
        help='Euphonic sf file')
    parser.add_argument(
        '--ab2tds',
        help='Ab2tds alongthelineF.dat file')
    parser.add_argument(
        '--qpts',
        help='Q-points idx to plot')
    return parser
    

if __name__ == '__main__':
    main()
