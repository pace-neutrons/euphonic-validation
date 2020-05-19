from generate_euphonic_dw import main as dw_main
from generate_euphonic_sf import main as sf_main
from generate_euphonic_sqw import main as sqw_main

grids = ['6,6,6']
temps = ['5', '100']

# Generate Debye-Waller and structure factors for different temperatures
for grid in grids:
    for temp in temps:
        dw_fc = dw_main(['../../quartz', '--grid', grid, '--temp', temp])
        dw_phonons = dw_main(['../../quartz', '--grid', grid, '--temp', temp, '--freqs'])

        sf_main(['../../quartz/2ph_m4_0_ECut/', '--dw', dw_fc])
        sf_main(['../../quartz/2ph_m4_0_ECut/', '--dw', dw_phonons, '--freqs'])

# Generate Ab2tds S(Q,w) map
sqw_main(['../../quartz/2ph_m4_0_ECut/euphonic/sf_fc_100K.json', '--ab2tds',
          '--ofig', '../../quartz/2ph_m4_0_ECut/ab2tds/euphonic_100K.pdf',
          '--osqw', '../../quartz/2ph_m4_0_ECut/ab2tds/sqw_euphonic_100K.json'])
