import os

import numpy as np

from compare_sqw import main as compare_sqw_main
from util import (get_euphonic_fpath, get_material_info, latex_mat_names,
                  latex_cut_names)

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

# Print in Latex format
if print_latex_rows:
    print('\n\\begin{tabular}{|c|c|c|c|}\n'
          '\hline\n'
          '\multirow{3}{*}{Material} &\n'
          '\multirow{3}{*}{Cut} &\n'
          '\multicolumn{2}{|c|}{Mean Relative Percentage Difference} \\\\\n'
          '\cline{3-4}\n'
          '  && \multicolumn{1}{|p{3cm}|}{\centering Euphonic \\\\ Interpolation} &\n'
          '     \multicolumn{1}{|p{3cm}|}{\centering CASTEP \\\\ Interpolation} \\\\\n'
          '\hline')
    for i, mat in enumerate(ab2tds_materials):
        print(f'\multirow{{2}}{{*}}{{{latex_mat_names[mat]}}} &')
        for j, cut in enumerate(ab2tds_cuts[i]):
            # amps indent so that data is placed in the correct column
            amps = '' if j == 0 else '& '
            print(f'  {amps}{{{latex_cut_names[cut]}}} & '
                  f'{format_latex(np.mean(ab2tds_fc_rel_err[i,j])*100)} & '
                  f'{format_latex(np.mean(ab2tds_freqs_rel_err[i,j])*100)} \\\\')
            print('  \cline{2-4}')
        print('\hline')
    print('\end{tabular}')

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

# Print in Latex format
if print_latex_rows:
    print('\\begin{tabular}{|c|c|c|c|c|}\n'
          '\hline\n'
          '\multirow{3}{*}{Material} &\n'
          '\multirow{3}{*}{Cut} &\n'
          '\multirow{3}{*}{Temperature (K)} &\n'
          '\multicolumn{2}{|c|}{Mean Relative Percentage Difference} \\\\\n'
          '\cline{4-5}\n'
          '  &&& \multicolumn{1}{|p{3cm}|}{\centering Euphonic \\\\ Interpolation} &\n'
          '      \multicolumn{1}{|p{3cm}|}{\centering CASTEP/Phonopy \\\\ Interpolation} \\\\\n'
          '\hline')
    for i, mat in enumerate(oclimax_materials):
        print(f'\multirow{{4}}{{*}}{{{latex_mat_names[mat]}}} &')
        for j, cut in enumerate(oclimax_cuts[i]):
            # amps indent so that data is placed in the correct column
            amps = '' if j == 0 else '& '
            print(f'  {amps}\multirow{{2}}{{*}}{{{latex_cut_names[cut]}}} &')
            for k, temp in enumerate(temperatures):
                # amps indent so that data is placed in the correct column
                amps = '' if k == 0 else '&& '
                print(f'    {amps}{temp} & {format_latex(np.mean(oclimax_fc_rel_err[i,j,k])*100)} '
                      f'& {format_latex(np.mean(oclimax_freqs_rel_err[i,j,k])*100)} \\\\')
                print('    \cline{3-5}')
            print('  \cline{2-5}')
        print('\hline')
    print('\end{tabular}')

print_reduced = True
if print_reduced:
    ab2tds_reduced_fc_rel_err = np.empty((len(ab2tds_materials), len(ab2tds_cuts[0])), dtype=object)
    ab2tds_reduced_freqs_rel_err = np.empty((len(ab2tds_materials), len(ab2tds_cuts[0])), dtype=object)
    for i, mat in enumerate(ab2tds_materials):
        for j, cut in enumerate(ab2tds_cuts[i]):
            _, _, rel_err, rel_idx, _ = compare_sqw_main(
                ['--sqw1', get_euphonic_fpath(mat, 'euphonic', 'sqw', '300', cut=cut, from_fc=True, reduced=True),
                 '--sqw2', get_euphonic_fpath(mat, 'ab2tds', 'sqw', '300', cut=cut),
                 '--mask-bragg', '--mask-negative', '-n', '3'])
            ab2tds_reduced_fc_rel_err[i, j] = rel_err[rel_idx]

            _, _, rel_err, rel_idx, _ = compare_sqw_main(
                ['--sqw1', get_euphonic_fpath(mat, 'euphonic', 'sqw', '300', cut=cut, from_fc=False, reduced=True),
                 '--sqw2', get_euphonic_fpath(mat, 'ab2tds', 'sqw', '300', cut=cut),
                 '--mask-bragg', '--mask-negative', '-n', '3'])
            ab2tds_reduced_freqs_rel_err[i, j] = rel_err[rel_idx]

    if print_latex_rows:
        print('\n\\begin{tabular}{|c|c|c|c|}\n'
              '\hline\n'
              '\multirow{3}{*}{Material} &\n'
              '\multirow{3}{*}{Cut} &\n'
              '\multicolumn{2}{|c|}{Mean Relative Percentage Difference} \\\\\n'
              '\cline{3-4}\n'
              '  && \multicolumn{1}{|p{3cm}|}{\centering Euphonic \\\\ Interpolation} &\n'
              '     \multicolumn{1}{|p{3cm}|}{\centering CASTEP \\\\ Interpolation} \\\\\n'
              '\hline')
        for i, mat in enumerate(ab2tds_materials):
            print(f'\multirow{{2}}{{*}}{{{latex_mat_names[mat]}}} &')
            for j, cut in enumerate(ab2tds_cuts[i]):
                # amps indent so that data is placed in the correct column
                amps = '' if j == 0 else '& '
                print(f'  {amps}{{{latex_cut_names[cut]}}} & '
                      f'{format_latex(np.mean(ab2tds_reduced_fc_rel_err[i,j])*100)} & '
                      f'{format_latex(np.mean(ab2tds_reduced_freqs_rel_err[i,j])*100)} \\\\')
                print('  \cline{2-4}')
            print('\hline')
        print('\end{tabular}')

