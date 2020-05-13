from generate_euphonic_dw import main as dw_main
from generate_euphonic_sf import main as sf_main

dw_fc = dw_main(['../quartz', '--grid', '6,6,6', '--temp', '5'])
dw_phonons = dw_main(['../quartz', '--grid', '6,6,6', '--temp', '5', '--freqs'])

sf_main(['../quartz/2ph_m4_0_ECut/', '--dw', dw_fc])
sf_main(['../quartz/2ph_m4_0_ECut/', '--dw', dw_phonons, '--freqs'])

