from generate_euphonic_dw import main as dw_main
from generate_euphonic_sf import main as sf_main
from generate_euphonic_sqw import main as sqw_main


# Generate Debye-Waller for different temperatures for Quartz
quartz_temps = ['5', '300']
quartz_grid = '5,5,4'
quartz_gridstr = quartz_grid.replace(',', '')
for temp in quartz_temps:
    dw_fc = dw_main(['../../quartz', '--grid', quartz_grid, '--temp', temp])
    dw_phonons = dw_main(['../../quartz', '--grid', quartz_grid, '--temp', temp, '--freqs'])

# Generate structure factors for different temperatures for Quartz
quartz_cuts = ['2ph_m4_0_qe', '30L_qe_fine']
for temp in quartz_temps:
    for cut in quartz_cuts:
        sf_main(['../../quartz/' + cut + '/', '--dw', '../../quartz/shared/euphonic/dw_fc_' + quartz_gridstr + '_' + temp + 'K.json'])
        sf_main(['../../quartz/' + cut + '/', '--dw', '../../quartz/shared/euphonic/dw_phonons_' + quartz_gridstr + '_' + temp + 'K.json', '--freqs'])

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
lzo_temps = ['5', '300']
lzo_grid = '4,4,4'
lzo_gridstr = lzo_grid.replace(',', '')
for temp in lzo_temps:
    dw_fc = dw_main(['../../lzo', '--grid', lzo_grid, '--temp', temp])
    dw_phonons = dw_main(['../../lzo', '--grid', lzo_grid, '--temp', temp, '--freqs'])

# Generate structure factors for LZO
lzo_cuts = ['kagome_qe', 'hh2_qe_fine']
for temp in lzo_temps:
    for cut in lzo_cuts:
        sf_main(['../../lzo/' + cut + '/', '--dw', '../../lzo/shared/euphonic/dw_fc_' + lzo_gridstr + '_' + temp + 'K.json'])
        sf_main(['../../lzo/' + cut + '/', '--dw', '../../lzo/shared/euphonic/dw_phonons_' + lzo_gridstr + '_' + temp + 'K.json', '--freqs'])

# Generate OClimax S(Q,w) map for LZO
for cut in lzo_cuts:
    for temp in lzo_temps:
        sqw_main(['../../lzo/' + cut + '/euphonic/sf_fc_' + temp + 'K.json', '--oclimax',
                  '--ofig', '../../lzo/' + cut + '/oclimax/euphonic_' + temp + 'K.pdf',
                  '--osqw', '../../lzo/' + cut + '/oclimax/sqw_euphonic_' + temp + 'K.json'])
        sqw_main(['../../lzo/' + cut + '/euphonic/sf_phonons_' + temp + 'K.json', '--oclimax',
                  '--ofig', '../../lzo/' + cut + '/oclimax/euphonic_ph_' + temp + 'K.pdf',
                  '--osqw', '../../lzo/' + cut + '/oclimax/sqw_euphonic_ph_' + temp + 'K.json'])

# Generate Debye-Waller for Nb
nb_temps = ['5', '300']
nb_grid = '10,10,10'
nb_gridstr = nb_grid.replace(',', '')
for temp in nb_temps:
    dw_fc = dw_main(['../../nb', '--grid', nb_grid, '--temp', temp])
    dw_phonons = dw_main(['../../nb', '--grid', nb_grid, '--temp', temp, '--freqs'])

# Generate structure factors for Nb
nb_cuts = ['110_qe', 'm110_qe']
for temp in nb_temps:
    for cut in nb_cuts:
        sf_main(['../../nb/' + cut + '/', '--dw', '../../nb/shared/euphonic/dw_fc_' + nb_gridstr + '_' + temp + 'K.json'])
        sf_main(['../../nb/' + cut + '/', '--dw', '../../nb/shared/euphonic/dw_phonons_' + nb_gridstr + '_' + temp + 'K.json', '--freqs'])

# Generate OClimax S(Q,w) map for Nb
for cut in nb_cuts:
    for temp in nb_temps:
        sqw_main(['../../nb/' + cut + '/euphonic/sf_fc_' + temp + 'K.json', '--oclimax',
                  '--ofig', '../../nb/' + cut + '/oclimax/euphonic_' + temp + 'K.pdf',
                  '--osqw', '../../nb/' + cut + '/oclimax/sqw_euphonic_' + temp + 'K.json'])
        sqw_main(['../../nb/' + cut + '/euphonic/sf_phonons_' + temp + 'K.json', '--oclimax',
                  '--ofig', '../../nb/' + cut + '/oclimax/euphonic_ph_' + temp + 'K.pdf',
                  '--osqw', '../../nb/' + cut + '/oclimax/sqw_euphonic_ph_' + temp + 'K.json'])

