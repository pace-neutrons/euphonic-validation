import os
from euphonic import ForceConstants, ureg
from euphonic.util import get_reference_data, mp_grid
import numpy as np
from util import get_ab2tds_fpath, get_oclimax_fpath
from ab2tds_to_sqw import get_ab2tds_sf
from oclimax_to_sqw import get_oclimax_sqw

#fc = ForceConstants.from_castep('..\..\quartz\shared\castep\quartz.castep_bin')
#fc = ForceConstants.from_castep('..\..\lzo\shared\castep\La2Zr2O7.castep_bin')
fc = ForceConstants.from_castep('..\..\\nb\shared\castep\\Nb-181818-s0.5-NCP19-vib-disp.castep_bin')


#qh = np.linspace(0., 2., 1001)
#qpts = np.zeros((len(qh), 3))
#qpts[:, 0] = qh
qpts = np.array([[0.01, 0.0, 0.0],
                 [0.02, 0.0, 0.0],
                 [0.03, 0.0, 0.0]])

# Euphonic
asr = 'realspace'
modes = fc.calculate_qpoint_phonon_modes(qpts, asr=asr)
dw_modes = fc.calculate_qpoint_phonon_modes(mp_grid([10, 10, 10]), asr=asr)
dw_0 = dw_modes.calculate_debye_waller(0*ureg('K'))
dw_5 = dw_modes.calculate_debye_waller(5*ureg('K'))
dw_300 = dw_modes.calculate_debye_waller(300*ureg('K'))
import pdb; pdb.set_trace()
sf = modes.calculate_structure_factor()
sf_5 = modes.calculate_structure_factor(dw=dw_5)
sf_5_bose = sf_5.structure_factors*(1 + sf_5._bose_factor())
sf_300 = modes.calculate_structure_factor(dw=dw_300)
sf_300_bose = sf_300.structure_factors*(1 + sf_300._bose_factor())
ebins = np.arange(0, 30, 0.05)*ureg('meV')
sqw = sf.calculate_sqw_map(ebins)
sqw_300 = sf_300.calculate_sqw_map(ebins)
sqw_300_bose_only = sf.calculate_sqw_map(ebins, temperature=300*ureg('K'))
sf_0 = modes.calculate_structure_factor(dw=dw_0)
sqw_0 = sf_0.calculate_sqw_map(ebins)
sqw_0_bose_only = sf.calculate_sqw_map(ebins, temperature=0*ureg('K'))

# Ab2tds
ab2tds_sf_300, freqs, qpts = get_ab2tds_sf(get_ab2tds_fpath('nb', 'acoustic_test', '300'))
ab2tds_sf_5, freqs, qpts = get_ab2tds_sf(get_ab2tds_fpath('nb', 'acoustic_test', '5'))

# OClimax
fname_300 = get_oclimax_fpath('nb', 'acoustic_test', temp='300', in_file=False)
fname_300_zeroevec = os.path.splitext(fname_300)[0] + '_zero_evecs.csv'
fname_0 = get_oclimax_fpath('nb', 'acoustic_test', temp='0', in_file=False)
fname_0_zeroevec = os.path.splitext(fname_0)[0] + '_zero_evecs.csv'
oclimax_sqw_300, oclimax_ebins = get_oclimax_sqw(fname_300)
oclimax_sqw_300_zeroevec, oclimax_ebins = get_oclimax_sqw(fname_300_zeroevec)
oclimax_sqw_0, oclimax_ebins = get_oclimax_sqw(fname_0)
oclimax_sqw_0_zeroevec, oclimax_ebins = get_oclimax_sqw(fname_0_zeroevec)

ffmt = '%.4f'
efmt = '%.4e'
#with open('nb_no_asr.txt', 'a') as f:
with open('nb_realspace_ab2tds_oclimax.txt', 'a') as f:
    f.write('*'*10)
    f.write('\nCell vectors (angstrom)\n')
    for cv in fc.crystal.cell_vectors:
        np.savetxt(f, cv.magnitude,fmt='%.5f', newline=' ')
    f.write('\n\nCell parameters (a, b, c, angle(b, c), angle(a, c), angle(a, b))\n')
    from ase.geometry import Cell
    cell = Cell(fc.crystal.cell_vectors.magnitude)
    np.savetxt(f, cell.cellpar(),fmt='%.5f', newline=' ')
    f.write('\n')
    for i, qpt in enumerate(qpts):
        f.write('\n')
        f.write('*'*10)
        f.write('\nQ = ')
        np.savetxt(f, qpt,fmt='%.2f', newline=' ')
        f.write(f'\n\nfrequencies ({modes.frequencies.units})\n')
        np.savetxt(f, modes.frequencies[i].magnitude,fmt=ffmt)
        f.write(f'\neigenvectors\n')
        for j, mode_evec in enumerate(modes.eigenvectors[i]):
#            f.write(f'\nmode {j}')
            np.savetxt(f, mode_evec, fmt=ffmt)
        f.write(f'\nEuphonic one-phonon structure factors eq.7, no DW/Bose ({sf.structure_factors.units})\n')
        np.savetxt(f, sf.structure_factors[i].magnitude, fmt=efmt)
        f.write(f'\nEuphonic one-phonon structure factors eq.7 with DW and bose at 300K ({sf.structure_factors.units})\n')
        np.savetxt(f, sf_300_bose[i].magnitude, fmt=efmt)
        f.write(f'\nEuphonic one-phonon structure factors eq.7 with DW and bose at 5K ({sf.structure_factors.units})\n')
        np.savetxt(f, sf_5_bose[i].magnitude, fmt=efmt)
        f.write(f'\nAb2tds one-phonon structure factors (eq. 7 WITH DW and Bose factor at 300K)\n')
        np.savetxt(f, ab2tds_sf_300[i], fmt=efmt)
        f.write(f'\nAb2tds one-phonon structure factors (eq. 7 WITH DW and Bose factor at 5K)\n')
        np.savetxt(f, ab2tds_sf_5[i], fmt=efmt)
        f.write(f'\nenergy bins ({ebins.units})\n')
        np.savetxt(f, ebins.magnitude, fmt='%.2f', newline=' ')
        f.write(f'\n\nEuphonic dynamical structure factors eq.9, nonzero bins, no DW/Bose ({sqw.z_data.units})\n')
        eu_idx = np.where(sqw.z_data[i].magnitude > 0)
        np.savetxt(f, sqw.z_data[i, eu_idx].magnitude, fmt=ffmt)
        f.write(f'\n\nEuphonic dynamical structure factors eq.9, nonzero bins with DW and Bose at 300K ({sqw.z_data.units})\n')
        np.savetxt(f, sqw_300.z_data[i, eu_idx].magnitude, fmt=ffmt)
#        f.write(f'\n\nEuphonic dynamical structure factors eq.9, nonzero bins with Bose only at 300K ({sqw.z_data.units})\n')
#        np.savetxt(f, sqw_300_bose_only.z_data[i, eu_idx].magnitude, fmt=ffmt)
        f.write(f'\n\nEuphonic dynamical structure factors eq.9, nonzero bins with DW and Bose at 0K ({sqw.z_data.units})\n')
        np.savetxt(f, sqw_0.z_data[i, eu_idx].magnitude, fmt=ffmt)
#        f.write(f'\n\nEuphonic dynamical structure factors eq.9, nonzero bins with Bose only at 0K ({sqw.z_data.units})\n')
#        np.savetxt(f, sqw_0_bose_only.z_data[i, eu_idx].magnitude, fmt=efmt)
        f.write('\nOClimax dynamical structure factors (eq. 9) at 300K with bose and DW, nonzero bins\n')
        oclimax_idx = np.where(oclimax_sqw_300[i+1] > 0)[0]
        oclimax_idx = oclimax_idx[int(len(oclimax_idx)/2):]
        np.savetxt(f, [*[0]*(3-len(oclimax_idx)), *oclimax_sqw_300[i+1, oclimax_idx]], fmt=ffmt, newline=' ')
#        f.write('\nOClimax dynamical structure factors (eq. 9) at 300K with bose only, nonzero bins\n')
#        np.savetxt(f, oclimax_sqw_300_zeroevec[i+1, oclimax_idx], fmt=ffmt)
        f.write('\n\nOClimax dynamical structure factors (eq. 9) at 0K with bose and DW, nonzero bins\n')
        np.savetxt(f, [*[0]*(3-len(oclimax_idx)), *oclimax_sqw_0[i+1, oclimax_idx]], fmt=ffmt, newline=' ')
#        f.write('\nOClimax dynamical structure factors (eq. 9) at 0K with bose only, nonzero bins\n')
#        np.savetxt(f, oclimax_sqw_0_zeroevec[i+1, oclimax_idx], fmt=ffmt)
        f.write('\n')
        
        

#cohb = get_reference_data(
#    collection='Sears1992',
#    physical_property='coherent_scattering_length')
#recip = fc.crystal.reciprocal_cell().magnitude # inverse ang
#import pdb; pdb.set_trace()
#q_cart = np.einsum('ij,jk->ik', qpts, recip) # inverse ang
#r_cart = np.einsum('ij,jk->ik', fc.crystal.atom_r, fc.crystal.cell_vectors.magnitude) # ang
#qdote = np.einsum('ijkl,il->ijk', modes.eigenvectors, q_cart) #inverse ang
#magq = np.linalg.norm(q_cart, axis=-1)
#mage = np.linalg.norm(modes.eigenvectors, axis=-1)
#psi = np.arccos(qdote/np.einsum('ijk,i->ijk', mage, magq)) # radians

#mass = np.sum(fc.crystal.atom_mass) # in amu
#cohbs = np.array([cohb[atom_type].magnitude for atom_type in fc.crystal.atom_type]) # in fm
#exp_gr = np.exp(1j*np.einsum('ij,kj->ik', q_cart, r_cart))
#fn = np.einsum('ij,j->i', exp_gr, cohbs) # in fm, leaving out DW

#intensity = (0.5/mass)*np.einsum('ijk,i,i->ijk', np.cos(psi)**2, magq**2, np.abs(fn)**2) # in (fm*ang)/amu