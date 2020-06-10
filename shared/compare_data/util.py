import numpy as np
import matplotlib.pyplot as plt


def plot_at_qpt(qpt, arr1, arr2, labels, x=None):
    fig, ax = plt.subplots()
    if x is None:
        x = np.arange(len(arr1))
    ax.plot(x, arr1, label=labels[0])
    ax.plot(x, arr2, label=labels[1])
    ax.legend(loc=1, prop={'size': 8})
    fig.suptitle(f'Q-point: {qpt}')
    fig.show()


def get_scaling(arr1, arr2):
    idx = np.nonzero(arr2)
    scale = arr1[idx]/arr2[idx]
    m = 2.0
    scale_reduced = scale[abs(scale - np.mean(scale)) < m*np.std(scale)]
    scale = np.mean(scale_reduced)
    return scale


def get_idx_more_than_x(arr1, arr2, lim=0):
    idx = np.where(np.logical_and(np.abs(arr1) > lim, np.abs(arr2) > lim))
    return idx


def calc_abs_error(arr1, arr2):
    # Ignore zero entries - these will artificially reduce the abs error
    idx = get_idx_more_than_x(arr1, arr2)
    return np.abs(arr1[idx] - arr2[idx])


def calc_rel_error(arr1, arr2, rel_tol=1e-5):
    # Ignore almost-zero entries - these will artificially cause a large
    # relative error
    lim = rel_tol*np.mean(arr2)
    idx = get_idx_more_than_x(arr1, arr2, lim=lim)
    return np.abs(arr1[idx] - arr2[idx])/arr2[idx]
