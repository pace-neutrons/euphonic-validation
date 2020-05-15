from generate_euphonic_dw import main as dw_main
from generate_euphonic_sf import main as sf_main

grids = ['6,6,6']
temps = ['5', '100']

for grid in grids:
    for temp in temps:
        dw_fc = dw_main(['../../quartz', '--grid', grid, '--temp', temp])
        dw_phonons = dw_main(['../../quartz', '--grid', grid, '--temp', temp, '--freqs'])

        sf_main(['../../quartz/2ph_m4_0_ECut/', '--dw', dw_fc])
        sf_main(['../../quartz/2ph_m4_0_ECut/', '--dw', dw_phonons, '--freqs'])

