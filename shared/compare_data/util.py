import numpy as np
import matplotlib.pyplot as plt
import warnings


# Define here so they can be imported from elsewhere too,
# to allow consistent plot styles
line_colours = ['m', 'orange', 'tab:cyan']
line_styles = ['-', '-', '--']
markers = ['o', '+', 'x']
marker_sizes = [5**2, 7**2, 6**2]


def plot_at_qpt(arrs, labels, x=None, x_title='', y_title='',
                title='', noshow=False, ptype=None, lc=line_colours,
                ls=line_styles, marks=markers, msizes=marker_sizes,
                plot_zeros=True, **legend_kwargs):
    fig, ax = plt.subplots()
    if x is None:
        x = np.arange(len(arr1))
    if ptype is None:
        ptype = 'line'
    if not plot_zeros:
        arrs_np = np.array(arrs)
        nonzero_idx = np.where(np.any(arrs_np > 0, axis=0))[0]
        arrs = arrs_np[:, nonzero_idx]
        x = x[nonzero_idx]
    for i, arr in enumerate(arrs):
        if ptype == 'line':
            ax.plot(x, arr, label=labels[i], color=lc[i%len(lc)], ls=ls[i%len(ls)])
        elif ptype == 'bar':
            ax.bar(x, arr, width=np.mean(np.diff(x)), align='edge',
                   label=labels[i], color=lc[i%len(lc)], alpha=0.5)
        elif ptype == 'scatter':
            ax.scatter(x, arr, label=labels[i], color=lc[i%len(lc)],
                       marker=marks[i%len(marks)], s=msizes[i%len(msizes)])
        else:
            raise ValueError(f'Unexpected plot type {pytype}')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 3))
    ax.legend(**legend_kwargs)
    if x_title:
        ax.set_xlabel(x_title)
    if y_title:
        ax.set_ylabel(y_title)
    if title:
        fig.suptitle(title)
    if not noshow:
        fig.show()
    else:
        return fig


def get_scaling(arr1, arr2, rel_tol=None):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        scale = arr1/arr2
    idx, lim = get_idx_more_than_rel_tol(arr2, rel_tol)
    return np.mean(scale[idx])


def get_abs_error_and_idx(arr1, arr2):
    # Ignore zero entries - these will artificially reduce the abs error
    idx = np.where(np.logical_and(np.abs(arr1) > 0, np.abs(arr2) > 0))
    return np.abs(arr1 - arr2), idx


def get_idx_more_than_rel_tol(arr, rel_tol=None):
    lim = get_lim(arr, rel_tol)
    idx = np.where(arr > lim)
    print(f'arr_shape: {arr.shape} max: {np.max(arr)} lim: {lim} '
          f'n_nonzero: {len(np.where(arr > 0)[0])} n_used_entries: {len(idx[0])}')
    return idx, lim


def get_lim(arr, rel_tol=None):
    if rel_tol is None:
        rel_tol = 1e-4
    lim = rel_tol*np.max(arr)
    return lim


def get_rel_error_and_idx(arr1, arr2, rel_tol=None):
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
        rel_err = np.abs(arr1 - arr2)/arr1
    idx, lim = get_idx_more_than_rel_tol(arr1, rel_tol)
    return rel_err, idx, lim

def get_max_rel_error_idx(arr1, arr2, n=10, **kwargs):
    rel_err, idx, lim = get_rel_error_and_idx(arr1, arr2, **kwargs)
    rel_err_reduced = rel_err[idx]
    max_err_reduced_idx = np.argsort(-rel_err_reduced)
    # Now we can find which q-points/branches have the largest relative
    # errors in the original arrays (while disregarding almost-zero entries)
    max_err_idx = (idx[0][max_err_reduced_idx[:n]],
                   idx[1][max_err_reduced_idx[:n]])
    return max_err_idx
