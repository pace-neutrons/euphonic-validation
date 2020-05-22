from compare_sf import main as compare_sf_main
from compare_sqw import main as compare_sqw_main


compare_sf_main(['--sf1', '../../quartz/2ph_m4_0_ECut/euphonic/sf_phonons_100K.json',
                 '--sf2', '../../quartz/2ph_m4_0_ECut/ab2tds/alongthelineF_100K.dat'])

compare_sf_main(['--sf1', '../../quartz/2ph_m4_0_ECut/euphonic/sf_fc_100K.json',
                 '--sf2', '../../quartz/2ph_m4_0_ECut/ab2tds/alongthelineF_100K.dat',
                 '--mask-bragg'])

compare_sf_main(['--sf1', '../../lzo/LZO_kagome_300K/euphonic/sf_fc_300K.json',
                 '--sf2', '../../lzo/LZO_kagome_300K/ab2tds/alongthelineF_300K.dat',
                 '--mask-bragg'])

compare_sqw_main(['--sqw1', '../../quartz/2ph_m4_0_ECut/oclimax/sqw_euphonic_5K.json',
                  '--sqw2', '../../quartz/2ph_m4_0_ECut/oclimax/quartz_2Dmesh_scqw_5K.csv',
                  '--qpts', '0,19,50,100,190', '--mask-bragg'])

compare_sqw_main(['--sqw1', '../../lzo/LZO_kagome_300K/oclimax/sqw_euphonic_300K.json',
                  '--sqw2', '../../lzo/LZO_kagome_300K/oclimax/La2Zr2O7_2Dmesh_scqw_300K.csv',
                  '--qpts', '0,10,50,70', '--mask-bragg'])

