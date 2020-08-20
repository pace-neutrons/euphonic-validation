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
quartz_cuts = ['2ph_m4_0_qe','30L_qe', '30L_qe_fine']
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
    for temp in quartz_temps:
        sqw_main(['../../quartz/' + cut + '/euphonic/sf_fc_' + temp + 'K.json', '--oclimax',
                  '--ofig', '../../quartz/' + cut + '/oclimax/euphonic_' + temp + 'K.pdf',
                  '--osqw', '../../quartz/' + cut + '/oclimax/sqw_euphonic_' + temp + 'K.json'])
        sqw_main(['../../quartz/' + cut + '/euphonic/sf_phonons_' + temp + 'K.json', '--oclimax',
                  '--ofig', '../../quartz/' + cut + '/oclimax/euphonic_ph_' + temp + 'K.pdf',
                  '--osqw', '../../quartz/' + cut + '/oclimax/sqw_euphonic_ph_' + temp + 'K.json'])

# Generate Debye-Waller for LZO
lzo_temps = ['300']
for grid in grids:
    for temp in lzo_temps:
        dw_fc = dw_main(['../../lzo', '--grid', grid, '--temp', temp])
        dw_phonons = dw_main(['../../lzo', '--grid', grid, '--temp', temp, '--freqs'])

# Generate structure factors for LZO
lzo_cuts = ['kagome_qe', 'hh2_qe', 'hh2_qe_fine']
for temp in lzo_temps:
    for cut in lzo_cuts:
        sf_main(['../../lzo/' + cut + '/', '--dw', '../../lzo/shared/euphonic/dw_fc_666_' + temp + 'K.json'])
        sf_main(['../../lzo/' + cut + '/', '--dw', '../../lzo/shared/euphonic/dw_phonons_666_' + temp + 'K.json', '--freqs'])

# Generate Ab2tds S(Q,w) map for LZO
for cut in lzo_cuts:
    for temp in lzo_temps:
        sqw_main(['../../lzo/' + cut + '/euphonic/sf_fc_' + temp + 'K.json', '--ab2tds',
                  '--ofig', '../../lzo/' + cut + '/ab2tds/euphonic_' + temp + 'K.pdf',
                  '--osqw', '../../lzo/' + cut + '/ab2tds/sqw_euphonic_' + temp + 'K.json'])

# Generate OClimax S(Q,w) map for LZO
for cut in lzo_cuts:
    for temp in lzo_temps:
        sqw_main(['../../lzo/' + cut + '/euphonic/sf_fc_' + temp + 'K.json', '--oclimax',
                  '--ofig', '../../lzo/' + cut + '/oclimax/euphonic_' + temp + 'K.pdf',
                  '--osqw', '../../lzo/' + cut + '/oclimax/sqw_euphonic_' + temp + 'K.json'])
        sqw_main(['../../lzo/' + cut + '/euphonic/sf_phonons_' + temp + 'K.json', '--oclimax',
                  '--ofig', '../../lzo/' + cut + '/oclimax_new/euphonic_ph_' + temp + 'K.pdf',
                  '--osqw', '../../lzo/' + cut + '/oclimax_new/sqw_euphonic_ph_' + temp + 'K.json'])

# Generate Debye-Waller for Nb
nb_temps = ['5', '100']
for grid in grids:
    for temp in nb_temps:
        dw_fc = dw_main(['../../nb', '--grid', grid, '--temp', temp])
        dw_phonons = dw_main(['../../nb', '--grid', grid, '--temp', temp, '--freqs'])

