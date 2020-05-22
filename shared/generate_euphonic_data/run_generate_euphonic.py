from generate_euphonic_dw import main as dw_main
from generate_euphonic_sf import main as sf_main
from generate_euphonic_sqw import main as sqw_main

grids = ['6,6,6']

# Generate Debye-Waller and structure factors for different temperatures
# for Quartz
quartz_temps = ['5', '100']
for grid in grids:
    for temp in quartz_temps:
        dw_fc = dw_main(['../../quartz', '--grid', grid, '--temp', temp])
        dw_phonons = dw_main(['../../quartz', '--grid', grid, '--temp', temp, '--freqs'])

        sf_main(['../../quartz/2ph_m4_0_ECut/', '--dw', dw_fc])
        sf_main(['../../quartz/2ph_m4_0_ECut/', '--dw', dw_phonons, '--freqs'])

# Generate Ab2tds S(Q,w) map for Quartz
sqw_main(['../../quartz/2ph_m4_0_ECut/euphonic/sf_fc_100K.json', '--ab2tds',
          '--ofig', '../../quartz/2ph_m4_0_ECut/ab2tds/euphonic_100K.pdf',
          '--osqw', '../../quartz/2ph_m4_0_ECut/ab2tds/sqw_euphonic_100K.json'])

# Generate OClimax S(Q,w) map for Quartz
sqw_main(['../../quartz/2ph_m4_0_ECut/euphonic/sf_fc_5K.json', '--oclimax',
          '--ofig', '../../quartz/2ph_m4_0_ECut/oclimax/euphonic_5K.pdf',
          '--osqw', '../../quartz/2ph_m4_0_ECut/oclimax/sqw_euphonic_5K.json'])
sqw_main(['../../quartz/2ph_m4_0_ECut/euphonic/sf_phonons_5K.json', '--oclimax',
          '--ofig', '../../quartz/2ph_m4_0_ECut/oclimax/euphonic_ph_5K.pdf',
          '--osqw', '../../quartz/2ph_m4_0_ECut/oclimax/sqw_euphonic_ph_5K.json'])

# Generate Debye-Waller and structure factors for LZO
lzo_temps = ['300']
for grid in grids:
    for temp in lzo_temps:
        dw_fc = dw_main(['../../lzo', '--grid', grid, '--temp', temp])
        dw_phonons = dw_main(['../../lzo', '--grid', grid, '--temp', temp, '--freqs'])

        sf_main(['../../lzo/LZO_kagome_300K/', '--dw', dw_fc])
        sf_main(['../../lzo/LZO_kagome_300K/', '--dw', dw_phonons, '--freqs'])

# Generate Ab2tds S(Q,w) map for Quartz
sqw_main(['../../lzo/LZO_kagome_300K/euphonic/sf_fc_300K.json', '--ab2tds',
          '--ofig', '../../lzo/LZO_kagome_300K/ab2tds/euphonic_300K.pdf',
          '--osqw', '../../lzo/LZO_kagome_300K/ab2tds/sqw_euphonic_300K.json'])

# Generate OClimax S(Q,w) map for LZO
sqw_main(['../../lzo/LZO_kagome_300K/euphonic/sf_fc_300K.json', '--oclimax',
          '--ofig', '../../lzo/LZO_kagome_300K/oclimax/euphonic_300K.pdf',
          '--osqw', '../../lzo/LZO_kagome_300K/oclimax/sqw_euphonic_300K.json'])
sqw_main(['../../lzo/LZO_kagome_300K/euphonic/sf_phonons_300K.json', '--oclimax',
          '--ofig', '../../lzo/LZO_kagome_300K/oclimax/euphonic_ph_300K.pdf',
          '--osqw', '../../lzo/LZO_kagome_300K/oclimax/sqw_euphonic_ph_300K.json'])

