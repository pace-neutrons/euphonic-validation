import numpy as np

from compare_sf import main as compare_sf_main
from compare_sqw import main as compare_sqw_main

temperatures = ['300', '5']

quartz_cuts = ['2ph_m4_0_qe', '30L_qe_fine']

sf_abs_err = np.empty((3, 2), dtype=object)
sf_rel_err = np.empty((3, 2), dtype=object)
sqw_abs_err = np.empty((3, 2), dtype=object)
sqw_rel_err = np.empty((3, 2), dtype=object)

for i, cut in enumerate(quartz_cuts):
    sf_abs_err[0, i], sf_rel_err[0, i] = compare_sf_main(
        ['--sf1', '../../quartz/' + cut + '/euphonic/sf_fc_300K.json',
         '--sf2', '../../quartz/' + cut + '/ab2tds/alongthelineF_300K.dat',
         '--mask-bragg'])
    for temp in temperatures:
        sqw_abs_err[0, i], sqw_rel_err[0, i] = compare_sqw_main(
            ['--sqw1', '../../quartz/' + cut + '/oclimax/sqw_euphonic_' + temp + 'K.json',
             '--sqw2', '../../quartz/' + cut + '/oclimax/quartz_2Dmesh_scqw_' + temp + 'K.csv',
             '--mask-bragg'])

lzo_cuts = ['kagome_qe', 'hh2_qe_fine']
for cut in lzo_cuts:
    sf_abs_err[1, i], sf_rel_err[1, i] = compare_sf_main(
        ['--sf1', '../../lzo/' + cut + '/euphonic/sf_fc_300K.json',
         '--sf2', '../../lzo/' + cut + '/ab2tds/alongthelineF_300K.dat',
         '--mask-bragg'])
    for temp in temperatures:
        sqw_abs_err[1, i], sqw_rel_err[1, i] = compare_sqw_main(
            ['--sqw1', '../../lzo/' + cut + '/oclimax/sqw_euphonic_' + temp + 'K.json',
             '--sqw2', '../../lzo/' + cut + '/oclimax/La2Zr2O7_2Dmesh_scqw_' + temp + 'K.csv',
             '--mask-bragg'])

nb_cuts = ['110_qe', 'm110_qe']
for cut in nb_cuts:
    sf_abs_err[2, i], sf_rel_err[2, i] = compare_sf_main(
        ['--sf1', '../../nb/' + cut + '/euphonic/sf_fc_300K.json',
         '--sf2', '../../nb/' + cut + '/ab2tds/alongthelineF_300K.dat',
         '--mask-bragg'])
    for temp in temperatures:
        sqw_abs_err[2, i], sqw_rel_err[2, i] = compare_sqw_main(
            ['--sqw1', '../../nb/' + cut + '/oclimax/sqw_euphonic_' + temp + 'K.json',
             '--sqw2', '../../nb/' + cut + '/oclimax/nb_2Dmesh_scqw_' + temp + 'K.csv',
             '--mask-bragg'])

