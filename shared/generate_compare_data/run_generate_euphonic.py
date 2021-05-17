from generate_euphonic_dw import main as dw_main
from generate_euphonic_sf import main as sf_main
from generate_euphonic_sqw import main as sqw_main
from util import get_material_info, get_dir, get_euphonic_fname, get_euphonic_fpath


# Generate Debye-Waller for different temperatures for Quartz
quartz_cuts, quartz_grid, quartz_temps = get_material_info('quartz')
for temp in quartz_temps:
    dw_fc = dw_main(['quartz', '--grid', quartz_grid, '--temp', temp])
    dw_phonons = dw_main(['quartz', '--grid', quartz_grid, '--temp', temp, '--freqs'])
# Generate structure factors for different temperatures for Quartz
for temp in quartz_temps:
    for cut in quartz_cuts:
        sf_main(['../../quartz/' + cut + '/',
                 '--dw', get_euphonic_fpath('quartz', 'euphonic', 'dw', temp, from_fc=True, grid=quartz_grid)])
        sf_main(['../../quartz/' + cut + '/',
                 '--dw', get_euphonic_fpath('quartz', 'euphonic', 'dw', temp, from_fc=False, grid=quartz_grid),
                 '--freqs'])
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
lzo_cuts, lzo_grid, lzo_temps = get_material_info('lzo')
for temp in lzo_temps:
    dw_fc = dw_main(['lzo', '--grid', lzo_grid, '--temp', temp])
    dw_phonons = dw_main(['lzo', '--grid', lzo_grid, '--temp', temp, '--freqs'])
# Generate structure factors for LZO
for temp in lzo_temps:
    for cut in lzo_cuts:
        sf_main(['../../lzo/' + cut + '/',
                 '--dw', get_euphonic_fpath('lzo', 'euphonic', 'dw', temp, from_fc=True, grid=lzo_grid)])
        sf_main(['../../lzo/' + cut + '/',
                 '--dw', get_euphonic_fpath('lzo', 'euphonic', 'dw', temp, from_fc=True, grid=lzo_grid),
                 '--freqs'])
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
nb_cuts, nb_grid, nb_temps = get_material_info('nb')
for temp in nb_temps:
    dw_fc = dw_main(['nb', '--grid', nb_grid, '--temp', temp])
    dw_phonons = dw_main(['nb', '--grid', nb_grid, '--temp', temp, '--freqs'])
# Generate structure factors for Nb
for temp in nb_temps:
    for cut in nb_cuts:
        sf_main(['../../nb/' + cut + '/',
                 '--dw', get_euphonic_fpath('nb', 'euphonic', 'dw', temp, from_fc=True, grid=nb_grid)])
        sf_main(['../../nb/' + cut + '/',
                 '--dw', get_euphonic_fpath('nb', 'euphonic', 'dw', temp, from_fc=False, grid=nb_grid),
                 '--freqs'])
# Generate OClimax S(Q,w) map for Nb
for cut in nb_cuts:
    for temp in nb_temps:
        sqw_main(['../../nb/' + cut + '/euphonic/sf_fc_' + temp + 'K.json', '--oclimax',
                  '--ofig', '../../nb/' + cut + '/oclimax/euphonic_' + temp + 'K.pdf',
                  '--osqw', '../../nb/' + cut + '/oclimax/sqw_euphonic_' + temp + 'K.json'])
        sqw_main(['../../nb/' + cut + '/euphonic/sf_phonons_' + temp + 'K.json', '--oclimax',
                  '--ofig', '../../nb/' + cut + '/oclimax/euphonic_ph_' + temp + 'K.pdf',
                  '--osqw', '../../nb/' + cut + '/oclimax/sqw_euphonic_ph_' + temp + 'K.json'])

