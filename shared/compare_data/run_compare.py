from compare_sf import main as compare_sf_main
from compare_sqw import main as compare_sqw_main


quartz_cuts = ['2ph_m4_0_qe', '30L_qe']
for cut in quartz_cuts:
    compare_sf_main(['--sf1', '../../quartz/' + cut + '/euphonic/sf_phonons_100K.json',
                     '--sf2', '../../quartz/' + cut + '/ab2tds/alongthelineF_100K.dat'])

    compare_sf_main(['--sf1', '../../quartz/' + cut + '/euphonic/sf_fc_100K.json',
                     '--sf2', '../../quartz/' + cut + '/ab2tds/alongthelineF_100K.dat',
                     '--mask-bragg', '--qpts', '0,10,20,30'])

    compare_sqw_main(['--sqw1', '../../quartz/' + cut + '/oclimax/sqw_euphonic_5K.json',
                      '--sqw2', '../../quartz/' + cut + '/oclimax/quartz_2Dmesh_scqw_5K.csv',
                      '--qpts', '0,10,30,50', '--mask-bragg'])

lzo_cuts = ['kagome_300K_qe', 'hh2_qe']
for cut in lzo_cuts:
    compare_sf_main(['--sf1', '../../lzo/' + cut + '/euphonic/sf_fc_300K.json',
                     '--sf2', '../../lzo/' + cut + '/ab2tds/alongthelineF_300K.dat',
                     '--mask-bragg'])

    compare_sqw_main(['--sqw1', '../../lzo/kagome_300K_qe/oclimax/sqw_euphonic_300K.json',
                      '--sqw2', '../../lzo/kagome_300K_qe/oclimax/La2Zr2O7_2Dmesh_scqw_300K.csv',
                      '--qpts', '0,10,30,50', '--mask-bragg'])


