"""
Prints max difference in frequencies between Euphonic
and CASTEP for each cut
"""
import os

import numpy as np
from euphonic.util import is_gamma

from compare_sqw import main as compare_sqw_main
from util import get_material_info, get_dir, get_fc, get_phonon_modes

# Get material/cut metadata
castep_materials = ['nb', 'quartz', 'lzo']
root_patterns = ['Nb-181818-s0.5-NCP19-vib-disp', 'quartz', 'La2Zr2O7']
castep_cuts = []
for mat in castep_materials:
    cuts_mat, _, _, _ = get_material_info(mat)
    castep_cuts.append(cuts_mat)

# Read CASTEP .phonon for each cut
cmodes = []
for cuts_per_mat, mat, root_pat in zip(
        castep_cuts, castep_materials, root_patterns):
    modes_per_mat = []
    for cut in cuts_per_mat:
        modes_per_mat.append(get_phonon_modes(mat, cut, root_pat))
    cmodes.append(modes_per_mat)

# Calculate equivalent Euphonic QpointPhononModes for each cut
eumodes = []
for cmodes_per_mat, mat in zip(cmodes, castep_materials):
    modes_per_mat = []
    fc = get_fc(mat)
    for cmode in cmodes_per_mat:
        qpts = cmode.qpts
        modes_per_mat.append(
            fc.calculate_qpoint_phonon_modes(qpts, asr='reciprocal'))
    eumodes.append(modes_per_mat)

# Calcuate absolute different in frequencies for each cut
freq_diffs = []
for cmodes_per_mat, eumodes_per_mat in zip(cmodes, eumodes):
    diff_per_mat = []
    for cmode, eumode in zip(cmodes_per_mat, eumodes_per_mat):
        gamma_idx = is_gamma(cmode.qpts)
        diff_per_mat.append(np.abs(
            cmode.frequencies - eumode.frequencies).magnitude[~gamma_idx])
        import pdb; pdb.set_trace()
    freq_diffs.append(diff_per_mat)

# Calcuate absolute difference in frequencies for each cut
for mat, cut_per_mat, diff_per_mat in zip(castep_materials, castep_cuts, freq_diffs):
    print(f'Material {mat}')
    for cut, diff in zip(cut_per_mat, diff_per_mat):
        print(f'Cut {cut} {np.amax(diff)} meV')

#def get_phonon_modes(material: str, direc: str, root_pattern: str):

#def get_dir(material: str, code: Optional[str] = None,
#            cut: Optional[str] = None) -> str:
#def get_fc(material: str):
#    cuts, grid, temps, code = get_material_info(material)
#    if code == 'castep':
#        pattern = '*.castep_bin'
#    elif code == 'phonopy':
#        pattern = '*[!m][!e][!s][!h].yaml'  # Do not match *mesh.yaml file
#    else:
#        raise ValueError('Unrecognised code {code}')
#    fc_file = find_file(get_dir(material, code=code), pattern)
##    print(f'Reading force constants from {fc_file}')
#    if code == 'castep':
#        fc = ForceConstants.from_castep(fc_file)
#    else:
#        fc = ForceConstants.from_phonopy(summary_name=fc_file)
#    return fc

#def get_phonon_modes(material: str, direc: str, root_pattern: str):
#    _, _, _, code = get_material_info(material)
#    if code == 'castep':
#        pattern = f'{root_pattern}.phonon'
#    elif code == 'phonopy':
#        pattern = f'{root_pattern}.yaml'
#    else:
#        raise ValueError('Unrecognised code {code}')
#    phon_file = find_file(get_dir(material, cut=direc, code=code), pattern)
#    print(f'Reading phonon modes from {phon_file}')
#    if code == 'castep':
#        phon = QpointPhononModes.from_castep(phon_file)
#    else:
#        phon = QpointPhononModes.from_phonopy(phonon_name=phon_file)
#    return phon

#def get_dir(material: str, code: Optional[str] = None,
#            cut: Optional[str] = None) -> str:
#    """
#    Get directory containing files for that material, cut and code
#    """
#    path = os.path.join('..', '..', material)
#    if cut is None:
#        cut = 'shared'
#    path = os.path.join(path, cut)
#    if code is not None:
#        path = os.path.join(path, code)
#    return path

