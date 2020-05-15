from compare_sf import main as compare_main

compare_main(['--euphonic', '../../quartz/2ph_m4_0_ECut/euphonic/sf_phonons_100K.json',
              '--ab2tds', '../../quartz/2ph_m4_0_ECut/ab2tds/alongthelineF_100K.dat',
              '--qpts', '0,10,50,150'])

