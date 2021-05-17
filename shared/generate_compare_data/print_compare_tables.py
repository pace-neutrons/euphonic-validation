import os

import numpy as np

from compare_sf import main as compare_sf_main
from compare_sqw import main as compare_sqw_main
from util import get_euphonic_fpath, get_material_info

materials = ['nb', 'quartz', 'lzo']
materials_castep = ['nb', 'quartz', 'La2Zr2O7']
temperatures = ['300', '5']
cuts = []
for mat in materials:
    cuts_mat, _, _ = get_material_info(mat)
    cuts.append(cuts_mat)

sf_rel_err = np.empty((len(materials), len(cuts[0])), dtype=object)
sf_castep_rel_err = np.empty((len(materials), len(cuts[0])), dtype=object)
sqw_rel_err = np.empty((len(materials), len(cuts[0]), 2), dtype=object)
sqw_castep_rel_err = np.empty((len(materials), len(cuts[0]), 2), dtype=object)

for i, mat in enumerate(materials):
    for j, cut in enumerate(cuts[i]):
        _, _, rel_err, rel_idx, _ = compare_sf_main(
            ['--sf2', get_euphonic_fpath(mat, 'euphonic', 'sf', '300', cut=cut, from_fc=True),
             '--sf1', os.path.join('..', '..', mat, cut, 'ab2tds', 'alongthelineF_300K.dat'),
             '--mask-bragg', '-n', '3'])
        sf_rel_err[i, j] = rel_err[rel_idx]

        _, _, rel_err, rel_idx, _ = compare_sf_main(
            ['--sf2', get_euphonic_fpath(mat, 'euphonic', 'sf', '300', cut=cut, from_fc=False),
             '--sf1', os.path.join('..', '..', mat, cut, 'ab2tds', 'alongthelineF_300K.dat'),
             '--mask-bragg', '-n', '3'])
        sf_castep_rel_err[i, j] = rel_err[rel_idx]

        for k, temp in enumerate(temperatures):
            _, _, rel_err, rel_idx, _ = compare_sqw_main(
                ['--sqw2', get_euphonic_fpath(mat, 'euphonic', 'sqw', temp, cut=cut, from_fc=True),
                 '--sqw1', os.path.join('..', '..', mat, cut, 'oclimax', materials_castep[i] + '_2Dmesh_scqw_' + temp + 'K.csv'),
                 '--mask-bragg', '-n', '3'])
            sqw_rel_err[i, j, k] = rel_err[rel_idx]

            _, _, rel_err, rel_idx, _ = compare_sqw_main(
                ['--sqw2', get_euphonic_fpath(mat, 'euphonic', 'sqw', temp, cut=cut, from_fc=False),
                 '--sqw1', os.path.join('..', '..', mat, cut, 'oclimax', materials_castep[i] + '_2Dmesh_scqw_' + temp + 'K.csv'),
                 '--mask-bragg', '-n', '3'])
            sqw_castep_rel_err[i, j, k] = rel_err[rel_idx]

# Print Ab2tds table
print('\n    ', end='')
for i, mat in enumerate(materials):
    print(f'|{mat:27}', end='')
print('|')
print('    ', end='')
for i, mat in enumerate(materials):
    for j, cut in enumerate(cuts[i]):
        print(f'|{cut:13}', end='')
print('|')
print('CSTP', end='')
for i, mat in enumerate(materials):
    for j, cut in enumerate(cuts[i]):
        print(f'|{np.mean(sf_castep_rel_err[i,j])*100:13.4f}', end='')
print('|')
print('Euph', end='')
for i, mat in enumerate(materials):
    for j, cut in enumerate(cuts[i]):
        print(f'|{np.mean(sf_rel_err[i,j])*100:13.4f}', end='')

# Print corresponding rows in Latex format
def format_latex(num):
    if num < 0.01:
        return '\\textless 0.01'
    else:
        return f'{num:.2f}'
print_latex_rows = True
if print_latex_rows:
    print('\nCASTEP phonons', end='')
    for i, mat in enumerate(materials):
        for j, cut in enumerate(cuts[i]):
            print(f' & {format_latex(np.mean(sf_castep_rel_err[i,j])*100)}', end='')
    print('\nEuphonic phonons', end='')
    for i, mat in enumerate(materials):
        for j, cut in enumerate(cuts[i]):
            print(f' & {format_latex(np.mean(sf_rel_err[i,j])*100)}', end='')

# Print OClimax table
print('\n\n    ', end='')
for i, mat in enumerate(materials):
    print(f'|{mat:27}', end='')
print('|')
print('    ', end='')
for i, mat in enumerate(materials):
    for j, cut in enumerate(cuts[i]):
        print(f'|{cut:13}', end='')
print('|')
print('Temp', end='')
for i, mat in enumerate(materials):
    for j, cut in enumerate(cuts[i]):
        for k, temp in enumerate(temperatures):
            print(f'|{temp:6}', end='')
print('|')
print('CSTP', end='')
for i, mat in enumerate(materials):
    for j, cut in enumerate(cuts[i]):
        for k, temp in enumerate(temperatures):
            print(f'|{np.mean(sqw_castep_rel_err[i,j,k])*100:6.4f}', end='')
print('|')
print('Euph', end='')
for i, mat in enumerate(materials):
    for j, cut in enumerate(cuts[i]):
        for k, temp in enumerate(temperatures):
            print(f'|{np.mean(sqw_rel_err[i,j,k])*100:6.4f}', end='')
print('')

# Print corresponding rows in Latex format
if print_latex_rows:
    print('\nCASTEP phonons', end='')
    for i, mat in enumerate(materials):
        for j, cut in enumerate(cuts[i]):
            for k, temp in enumerate(temperatures):
                print(f' & {format_latex(np.mean(sqw_castep_rel_err[i,j,k])*100)}', end='')
    print('\nEuphonic phonons', end='')
    for i, mat in enumerate(materials):
        for j, cut in enumerate(cuts[i]):
            for k, temp in enumerate(temperatures):
                print(f' & {format_latex(np.mean(sqw_rel_err[i,j,k])*100)}', end='')

