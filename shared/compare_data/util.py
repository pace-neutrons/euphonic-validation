import numpy as np
import matplotlib.pyplot as plt
import warnings


def plot_at_qpt(qpt, arr1, arr2, labels, x=None):
    fig, ax = plt.subplots()
    if x is None:
        x = np.arange(len(arr1))
    ax.plot(x, arr1, label=labels[0])
    ax.plot(x, arr2, label=labels[1])
    ax.legend(loc=1, prop={'size': 8})
    fig.suptitle(f'Q-point: {qpt}')
    fig.show()


def get_scaling(arr1, arr2, rel_tol=1e-3):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        scale = arr1/arr2
    lim = rel_tol*np.median(arr2[np.nonzero(arr2)])
    idx = get_idx_more_than_x(arr1, arr2, lim=lim)
    return np.mean(scale[idx])


def get_idx_more_than_x(arr1, arr2, lim=0):
    idx = np.where(np.logical_and(np.abs(arr1) > lim, np.abs(arr2) > lim))
    return idx


def calc_abs_error(arr1, arr2):
    # Ignore zero entries - these will artificially reduce the abs error
    idx = get_idx_more_than_x(arr1, arr2)
    return np.abs(arr1[idx] - arr2[idx])


def calc_rel_error(arr1, arr2, **kwargs):
    rel_err, idx = get_rel_error_and_idx(arr1, arr2, **kwargs)
    return rel_err[idx]

def get_rel_error_and_idx(arr1, arr2, rel_tol=1e-3):
    """
    Gets relative error of all array entries, and indices of entries
    that are below a certain relative tolerance so that these can be
    ignored - near-zero entries artificially cause a large relative
    error. We allow a divide by zero and therefore nan entries in
    rel_err as it is important to retain information on the original
    indexes, using np.where to only calculate the relative error on array
    entries above the threshold would reduce it to a 1d array and lose
    information on where the errors originally came from
    """
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        rel_err = np.abs(arr1 - arr2)/arr2
    lim = rel_tol*np.median(arr2[np.nonzero(arr2)])
    idx = get_idx_more_than_x(arr1, arr2, lim=lim)
    return rel_err, idx

def get_max_rel_error_idx(arr1, arr2, n=10, **kwargs):
    rel_err, idx = get_rel_error_and_idx(arr1, arr2, **kwargs)
    rel_err_reduced = rel_err[idx]
    max_err_reduced_idx = np.argsort(-rel_err_reduced)
    # Now we can find which q-points/branches have the largest relative
    # errors in the original arrays (while disregarding almost-zero entries)
    max_err_idx = (idx[0][max_err_reduced_idx[:n]],
                   idx[1][max_err_reduced_idx[:n]])
    return max_err_idx
