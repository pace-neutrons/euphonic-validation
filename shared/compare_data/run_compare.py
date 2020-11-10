from compare_sf import main as compare_sf_main
from compare_sqw import main as compare_sqw_main

temperatures = ['300', '5']

quartz_cuts = ['2ph_m4_0_qe', '30L_qe_fine']
for cut in quartz_cuts:
    compare_sf_main(['--sf1', '../../quartz/' + cut + '/euphonic/sf_fc_300K.json',
                     '--sf2', '../../quartz/' + cut + '/ab2tds/alongthelineF_300K.dat',
                     '--mask-bragg', '--qpts', '20'])
    for temp in temperatures:
        compare_sqw_main(['--sqw1', '../../quartz/' + cut + '/oclimax/sqw_euphonic_' + temp + 'K.json',
                          '--sqw2', '../../quartz/' + cut + '/oclimax/quartz_2Dmesh_scqw_' + temp + 'K.csv',
                          '--qpts', '20', '--mask-bragg'])

lzo_cuts = ['kagome_qe', 'hh2_qe_fine']
for cut in lzo_cuts:
    compare_sf_main(['--sf1', '../../lzo/' + cut + '/euphonic/sf_fc_300K.json',
                     '--sf2', '../../lzo/' + cut + '/ab2tds/alongthelineF_300K.dat',
                     '--mask-bragg', '--qpts', '20'])
    for temp in temperatures:
        compare_sqw_main(['--sqw1', '../../lzo/' + cut + '/oclimax/sqw_euphonic_' + temp + 'K.json',
                          '--sqw2', '../../lzo/' + cut + '/oclimax/La2Zr2O7_2Dmesh_scqw_' + temp + 'K.csv',
                          '--qpts', '20', '--mask-bragg'])

nb_cuts = ['110_qe', 'm110_qe']
for cut in nb_cuts:
    compare_sf_main(['--sf1', '../../nb/' + cut + '/euphonic/sf_fc_300K.json',
                     '--sf2', '../../nb/' + cut + '/ab2tds/alongthelineF_300K.dat',
                     '--mask-bragg', '--qpts', '40'])
    for temp in temperatures:
        compare_sqw_main(['--sqw1', '../../nb/' + cut + '/oclimax/sqw_euphonic_' + temp + 'K.json',
                          '--sqw2', '../../nb/' + cut + '/oclimax/nb_2Dmesh_scqw_' + temp + 'K.csv',
                          '--qpts', '40', '--mask-bragg'])
