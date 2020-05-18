from compare_sf import main as compare_main

compare_main(['--sf1', '../../quartz/2ph_m4_0_ECut/euphonic/sf_phonons_100K.json',
              '--sf2', '../../quartz/2ph_m4_0_ECut/ab2tds/alongthelineF_100K.dat'])

compare_main(['--sf1', '../../quartz/2ph_m4_0_ECut/euphonic/sf_fc_100K.json',
              '--sf2', '../../quartz/2ph_m4_0_ECut/ab2tds/alongthelineF_100K.dat',
              '--qpts', '0,19,50,100,190', '--mask-bragg'])
