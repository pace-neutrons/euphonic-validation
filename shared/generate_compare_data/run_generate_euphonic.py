import os

from generate_euphonic_dw import main as dw_main
from generate_euphonic_sf import main as sf_main
from generate_euphonic_sqw import main as sqw_main
from util import get_material_info, get_dir, get_euphonic_fname, get_euphonic_fpath

materials = ['quartz', 'lzo', 'nb', 'al']

for mat in materials:
    cuts, grid, temps, _ = get_material_info(mat)

    # Generate Debye-Waller for different temperatures
    for temp in temps:
        dw_fc = dw_main([mat, '--grid', grid, '--temp', temp])
        dw_phonons = dw_main([mat, '--grid', grid, '--temp', temp, '--freqs'])

    # Generate structure factors for different temperatures
    for temp in temps:
        for cut in cuts:
            sf_main([mat, cut,
                     '--dw', get_euphonic_fpath(mat, 'euphonic', 'dw', temp, from_fc=True, grid=grid)])
            sf_main([mat, cut,
                     '--dw', get_euphonic_fpath(mat, 'euphonic', 'dw', temp, from_fc=False, grid=grid),
                     '--freqs'])

    # Generate S(Q,w) map
    for temp in temps:
        for cut in cuts:
            sqw_main([mat, cut, '--temp', temp,])
            sqw_main([mat, cut, '--temp', temp, '--freqs'])

# Generate Euphonic data with reduced grid
# Only using Ab2tds for comparison so only use quartz, lzo and nb
generate_reduced = True
ab2tds_materials = materials[:3]
if generate_reduced:
    for mat in ab2tds_materials:
        cuts, grid, temps, _ = get_material_info(mat)

        # Generate Debye-Waller for 300K - only need for Ab2tds comparison
        dw_fc = dw_main([mat, '--grid', grid, '--temp', '300', '--reduced'])
        dw_phonons = dw_main([mat, '--grid', grid, '--temp', '300', '--freqs', '--reduced'])

        # Generate structure factors
        for cut in cuts:
            sf_main([mat, cut,
                     '--dw', get_euphonic_fpath(mat, 'euphonic', 'dw', '300', from_fc=True, grid=grid, reduced=True),
                     '-o',  get_euphonic_fpath(mat, 'euphonic', 'sf', '300', cut=cut, from_fc=True, reduced=True)])
            sf_main([mat, cut,
                     '--dw', get_euphonic_fpath(mat, 'euphonic', 'dw', '300', from_fc=False, grid=grid, reduced=True),
                     '--freqs', '-o',  get_euphonic_fpath(mat, 'euphonic', 'sf', '300', cut=cut, from_fc=False, reduced=True)])

        # Generate S(Q,w) map
        for cut in cuts:
            sqw_main([mat, cut, '--temp', '300', '--reduced'])
            sqw_main([mat, cut, '--temp', '300', '--freqs', '--reduced'])

