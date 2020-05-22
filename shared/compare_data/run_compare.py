from compare_sf import main as compare_sf_main
from compare_sqw import main as compare_sqw_main

compare_sf_main(['--sf1', '../../quartz/2ph_m4_0_ECut/euphonic/sf_phonons_100K.json',
                 '--sf2', '../../quartz/2ph_m4_0_ECut/ab2tds/alongthelineF_100K.dat'])

compare_sf_main(['--sf1', '../../quartz/2ph_m4_0_ECut/euphonic/sf_fc_100K.json',
                 '--sf2', '../../quartz/2ph_m4_0_ECut/ab2tds/alongthelineF_100K.dat'])
                 '--mask-bragg'])

compare_sqw_main(['--sqw1', '../../quartz/2ph_m4_0_ECut/oclimax/sqw_euphonic_5K.json',
                  '--sqw2', '../../quartz/2ph_m4_0_ECut/oclimax/quartz_2Dmesh_scqw_5K.csv',
                  '--qpts', '0,19,50,100,190', '--mask-bragg'])
