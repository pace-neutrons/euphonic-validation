from oclimax_to_sqw import main as oclimax_to_sqw_main
from util import get_material_info

materials = ['quartz', 'lzo', 'nb', 'al', 'mapbcl3']

for mat in materials:
    cuts, _, temps, _ = get_material_info(mat)
    # Only used temp for Ab2tds is 300K

    for cut in cuts:
        for temp in temps:
            oclimax_to_sqw_main([mat, cut, '--temp', temp])
