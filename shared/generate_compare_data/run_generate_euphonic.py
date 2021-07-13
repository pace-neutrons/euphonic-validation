import os

from generate_euphonic_dw import main as dw_main
from generate_euphonic_sf import main as sf_main
from generate_euphonic_sqw import main as sqw_main
from util import get_material_info, get_dir, get_euphonic_fname, get_euphonic_fpath

materials = ['quartz', 'lzo', 'nb']
for mat in materials:
    cuts, grid, temps = get_material_info(mat)

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
            sqw_main([mat, cut, '--temp', temp,
                      '--ofig', os.path.join(get_dir(mat, cut=cut, code='euphonic'),
                                             'euphonic_sqw_'+ temp + 'K.pdf')])
            sqw_main([mat, cut, '--temp', temp, '--freqs'])
