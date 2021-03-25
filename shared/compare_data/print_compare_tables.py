import os

import numpy as np

from compare_sf import main as compare_sf_main
from compare_sqw import main as compare_sqw_main

temperatures = ['300', '5']

materials = ['lzo', 'quartz', 'nb']
materials_castep = ['La2Zr2O7', 'quartz', 'nb']
cuts = [['kagome_qe', 'hh2_qe_fine'],
        ['2ph_m4_0_qe', '30L_qe_fine'],
        ['110_qe', 'm110_qe']]

sf_rel_err = np.empty((len(materials), len(cuts[0])), dtype=object)
sf_castep_rel_err = np.empty((len(materials), len(cuts[0])), dtype=object)
sqw_rel_err = np.empty((len(materials), len(cuts[0]), 2), dtype=object)
sqw_castep_rel_err = np.empty((len(materials), len(cuts[0]), 2), dtype=object)

for i, mat in enumerate(materials):
    for j, cut in enumerate(cuts[i]):
        _, sf_rel_err[i, j] = compare_sf_main(
            ['--sf2', os.path.join('..', '..', mat, cut, 'euphonic', 'sf_fc_300K.json'),
             '--sf1', os.path.join('..', '..', mat, cut, 'ab2tds', 'alongthelineF_300K.dat'),
             '--mask-bragg'])

        _, sf_castep_rel_err[i, j] = compare_sf_main(
            ['--sf2', os.path.join('..', '..', mat, cut, 'euphonic', 'sf_phonons_300K.json'),
             '--sf1', os.path.join('..', '..', mat, cut, 'ab2tds', 'alongthelineF_300K.dat'),
             '--mask-bragg'])
        for k, temp in enumerate(temperatures):
            _, sqw_rel_err[i, j, k] = compare_sqw_main(
                ['--sqw2', os.path.join('..', '..', mat, cut, 'oclimax', 'sqw_euphonic_' + temp + 'K.json'),
                 '--sqw1', os.path.join('..', '..', mat, cut, 'oclimax', materials_castep[i] + '_2Dmesh_scqw_' + temp + 'K.csv'),
                 '--mask-bragg'])
            _, sqw_castep_rel_err[i, j, k] = compare_sqw_main(
                ['--sqw2', os.path.join('..', '..', mat, cut, 'oclimax', 'sqw_euphonic_ph_' + temp + 'K.json'),
                 '--sqw1', os.path.join('..', '..', mat, cut, 'oclimax', materials_castep[i] + '_2Dmesh_scqw_' + temp + 'K.csv'),
                 '--mask-bragg'])

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

