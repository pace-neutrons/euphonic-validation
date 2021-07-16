from ab2tds_to_sqw import main as ab2tds_to_sqw_main
from util import get_material_info

materials = ['quartz', 'lzo', 'nb']
for mat in materials:
    cuts, _, _, _ = get_material_info(mat)
    # Only used temp for Ab2tds is 300K
    temp = '300'

    for cut in cuts:
        ab2tds_to_sqw_main([mat, cut, '--temp', temp])
