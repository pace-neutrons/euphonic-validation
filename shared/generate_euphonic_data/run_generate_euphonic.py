from generate_euphonic_dw import main as dw_main
from generate_euphonic_sf import main as sf_main
from generate_euphonic_sqw import main as sqw_main


# Generate Debye-Waller for different temperatures for Quartz
quartz_temps = ['5', '100']
grids = ['6,6,6']
for grid in grids:
    for temp in quartz_temps:
        dw_fc = dw_main(['../../quartz', '--grid', grid, '--temp', temp])
        dw_phonons = dw_main(['../../quartz', '--grid', grid, '--temp', temp, '--freqs'])

# Generate structure factors for different temperatures for Quartz
quartz_cuts = ['2ph_m4_0_qe']
for temp in quartz_temps:
    for cut in quartz_cuts:
        sf_main(['../../quartz/' + cut + '/', '--dw', '../../quartz/shared/euphonic/dw_fc_666_' + temp + 'K.json'])
        sf_main(['../../quartz/' + cut + '/', '--dw', '../../quartz/shared/euphonic/dw_phonons_666_' + temp + 'K.json', '--freqs'])

# Generate Ab2tds S(Q,w) map for Quartz
for cut in quartz_cuts:
    sqw_main(['../../quartz/' + cut + '/euphonic/sf_fc_100K.json', '--ab2tds',
              '--ofig', '../../quartz/' + cut + '/ab2tds/euphonic_100K.pdf',
              '--osqw', '../../quartz/' + cut + '/ab2tds/sqw_euphonic_100K.json'])

# Generate OClimax S(Q,w) map for Quartz
for cut in quartz_cuts:
    sqw_main(['../../quartz/' + cut + '/euphonic/sf_fc_5K.json', '--oclimax',
              '--ofig', '../../quartz/' + cut + '/oclimax/euphonic_5K.pdf',
              '--osqw', '../../quartz/' + cut + '/oclimax/sqw_euphonic_5K.json'])
    sqw_main(['../../quartz/' + cut + '/euphonic/sf_phonons_5K.json', '--oclimax',
              '--ofig', '../../quartz/' + cut + '/oclimax/euphonic_ph_5K.pdf',
              '--osqw', '../../quartz/' + cut + '/oclimax/sqw_euphonic_ph_5K.json'])

# Generate Debye-Waller for LZO
lzo_temps = ['300']
for grid in grids:
    for temp in lzo_temps:
        dw_fc = dw_main(['../../lzo', '--grid', grid, '--temp', temp])
        dw_phonons = dw_main(['../../lzo', '--grid', grid, '--temp', temp, '--freqs'])

# Generate structure factors for LZO
lzo_cuts = ['kagome_300K_qe']
for cut in lzo_cuts:
    sf_main(['../../lzo/' + cut + '/', '--dw', '../../lzo/shared/euphonic/dw_fc_666_' + temp + 'K.json'])
    sf_main(['../../lzo/' + cut + '/', '--dw', '../../lzo/shared/euphonic/dw_phonons_666_' + temp + 'K.json', '--freqs'])

# Generate Ab2tds S(Q,w) map for LZO
for cut in lzo_cuts:
    sqw_main(['../../lzo/' + cut + '/euphonic/sf_fc_300K.json', '--ab2tds',
              '--ofig', '../../lzo/' + cut + '/ab2tds/euphonic_300K.pdf',
              '--osqw', '../../lzo/' + cut + '/ab2tds/sqw_euphonic_300K.json'])

# Generate OClimax S(Q,w) map for LZO
for cut in lzo_cuts:
    sqw_main(['../../lzo/' + cut + '/euphonic/sf_fc_300K.json', '--oclimax',
              '--ofig', '../../lzo/' + cut + '/oclimax/euphonic_300K.pdf',
              '--osqw', '../../lzo/' + cut + '/oclimax/sqw_euphonic_300K.json'])
    sqw_main(['../../lzo/' + cut + '/euphonic/sf_phonons_300K.json', '--oclimax',
              '--ofig', '../../lzo/' + cut + '/oclimax/euphonic_ph_300K.pdf',
              '--osqw', '../../lzo/' + cut + '/oclimax/sqw_euphonic_ph_300K.json'])
