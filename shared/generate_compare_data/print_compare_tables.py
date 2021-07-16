import os

import numpy as np

from compare_sqw import main as compare_sqw_main
from util import get_euphonic_fpath, get_material_info

oclimax_materials = ['nb', 'quartz', 'lzo', 'al']
ab2tds_materials = ['nb', 'quartz', 'lzo']
temperatures = ['300', '5']
ab2tds_cuts = []
oclimax_cuts = []
for mat in ab2tds_materials:
    cuts_mat, _, _, _ = get_material_info(mat)
    ab2tds_cuts.append(cuts_mat)
for mat in oclimax_materials:
    cuts_mat, _, _, _ = get_material_info(mat)
    oclimax_cuts.append(cuts_mat)

ab2tds_fc_rel_err = np.empty((len(ab2tds_materials), len(ab2tds_cuts[0])), dtype=object)
ab2tds_freqs_rel_err = np.empty((len(ab2tds_materials), len(ab2tds_cuts[0])), dtype=object)
oclimax_fc_rel_err = np.empty((len(oclimax_materials), len(oclimax_cuts[0]), 2), dtype=object)
oclimax_freqs_rel_err = np.empty((len(oclimax_materials), len(oclimax_cuts[0]), 2), dtype=object)

for i, mat in enumerate(ab2tds_materials):
    for j, cut in enumerate(ab2tds_cuts[i]):
        _, _, rel_err, rel_idx, _ = compare_sqw_main(
            ['--sqw1', get_euphonic_fpath(mat, 'euphonic', 'sqw', '300', cut=cut, from_fc=True),
             '--sqw2', get_euphonic_fpath(mat, 'ab2tds', 'sqw', '300', cut=cut),
             '--mask-bragg', '--mask-negative', '-n', '3'])
        ab2tds_fc_rel_err[i, j] = rel_err[rel_idx]

        _, _, rel_err, rel_idx, _ = compare_sqw_main(
            ['--sqw1', get_euphonic_fpath(mat, 'euphonic', 'sqw', '300', cut=cut, from_fc=False),
             '--sqw2', get_euphonic_fpath(mat, 'ab2tds', 'sqw', '300', cut=cut),
             '--mask-bragg', '--mask-negative', '-n', '3'])
        ab2tds_freqs_rel_err[i, j] = rel_err[rel_idx]

for i, mat in enumerate(oclimax_materials):
    for j, cut in enumerate(oclimax_cuts[i]):
        for k, temp in enumerate(temperatures):
            _, _, rel_err, rel_idx, _ = compare_sqw_main(
                ['--sqw1', get_euphonic_fpath(mat, 'euphonic', 'sqw', temp, cut=cut, from_fc=True),
                 '--sqw2', get_euphonic_fpath(mat, 'oclimax', 'sqw', temp, cut=cut),

                 '--mask-bragg', '-n', '3'])
            oclimax_fc_rel_err[i, j, k] = rel_err[rel_idx]

            _, _, rel_err, rel_idx, _ = compare_sqw_main(
                ['--sqw1', get_euphonic_fpath(mat, 'euphonic', 'sqw', temp, cut=cut, from_fc=False),
                 '--sqw2', get_euphonic_fpath(mat, 'oclimax', 'sqw', temp, cut=cut),
                 '--mask-bragg', '-n', '3'])
            oclimax_freqs_rel_err[i, j, k] = rel_err[rel_idx]

# Print Ab2tds table
print('\n    ', end='')
for i, mat in enumerate(ab2tds_materials):
    print(f'|{mat:27}', end='')
print('|')
print('    ', end='')
for i, mat in enumerate(ab2tds_materials):
    for j, cut in enumerate(ab2tds_cuts[i]):
        print(f'|{cut:13}', end='')
print('|')
print('Code', end='')
for i, mat in enumerate(ab2tds_materials):
    for j, cut in enumerate(ab2tds_cuts[i]):
        print(f'|{np.mean(ab2tds_freqs_rel_err[i,j])*100:13.4f}', end='')
print('|')
print('Euph', end='')
for i, mat in enumerate(ab2tds_materials):
    for j, cut in enumerate(ab2tds_cuts[i]):
        print(f'|{np.mean(ab2tds_fc_rel_err[i,j])*100:13.4f}', end='')

# Print corresponding rows in Latex format
def format_latex(num):
    if num < 0.01:
        return '\\textless 0.01'
    else:
        return f'{num:.2f}'
print_latex_rows = True
if print_latex_rows:
    print('\nCode phonons', end='')
    for i, mat in enumerate(ab2tds_materials):
        for j, cut in enumerate(ab2tds_cuts[i]):
            print(f' & {format_latex(np.mean(ab2tds_freqs_rel_err[i,j])*100)}', end='')
    print('\nEuphonic phonons', end='')
    for i, mat in enumerate(ab2tds_materials):
        for j, cut in enumerate(ab2tds_cuts[i]):
            print(f' & {format_latex(np.mean(ab2tds_fc_rel_err[i,j])*100)}', end='')

# Print OClimax table
print('\n\n    ', end='')
for i, mat in enumerate(oclimax_materials):
    print(f'|{mat:27}', end='')
print('|')
print('    ', end='')
for i, mat in enumerate(oclimax_materials):
    for j, cut in enumerate(oclimax_cuts[i]):
        print(f'|{cut:13}', end='')
print('|')
print('Temp', end='')
for i, mat in enumerate(oclimax_materials):
    for j, cut in enumerate(oclimax_cuts[i]):
        for k, temp in enumerate(temperatures):
            print(f'|{temp:6}', end='')
print('|')
print('Code', end='')
for i, mat in enumerate(oclimax_materials):
    for j, cut in enumerate(oclimax_cuts[i]):
        for k, temp in enumerate(temperatures):
            print(f'|{np.mean(oclimax_freqs_rel_err[i,j,k])*100:6.4f}', end='')
print('|')
print('Euph', end='')
for i, mat in enumerate(oclimax_materials):
    for j, cut in enumerate(oclimax_cuts[i]):
        for k, temp in enumerate(temperatures):
            print(f'|{np.mean(oclimax_fc_rel_err[i,j,k])*100:6.4f}', end='')
print('')

# Print corresponding rows in Latex format
if print_latex_rows:
    print('\nCode phonons', end='')
    for i, mat in enumerate(oclimax_materials):
        for j, cut in enumerate(oclimax_cuts[i]):
            for k, temp in enumerate(temperatures):
                print(f' & {format_latex(np.mean(oclimax_freqs_rel_err[i,j,k])*100)}', end='')
    print('\nEuphonic phonons', end='')
    for i, mat in enumerate(oclimax_materials):
        for j, cut in enumerate(oclimax_cuts[i]):
            for k, temp in enumerate(temperatures):
                print(f' & {format_latex(np.mean(oclimax_fc_rel_err[i,j,k])*100)}', end='')

