# euphonic-validation
A repository to store output from Ab2tds/OClimax/Euphonic, to validate
Euphonic's phonon frequency and inelastic neutron scattering intensity
calculations

## Directory layout

### Cuts
The cut directories are organised by `material` -> `cut` -> `software`
e.g. the `quartz` -> `2ph_m4_0_qe` -> `oclimax` directory contains
OClimax input/output files for the quartz cut named 2ph_m4_0_qe.

**`cut` -> `CASTEP` directory**

This only applies for the quartz, Nb and LZO materials. Contains a
`material.cell` CASTEP input file and `material.phonon` CASTEP output
file for the q-points contained in the cut.

**`cut` -> `Phonopy` directory**

Only applies for the Al material. Contains an `cut_band.yaml` Phonopy
output file containing the q-points, frequencies and eigenvectors for
the cut.

**`cut` -> `ab2tds` directory**

This contains the input files for Abt2ds for a particular cut
(`intensity_map_input.py`, `resolution.txt`), the output intensities
at 300K (`res_300K.dat`), the output mode-resolved structure factors
with Bose factor applied at the mode frequencies (`alongthelineF_300K.dat`)
and a short script to run ab2tds with the input files (`run_ab2tds.sh`). The
`ab2tds_sqw_300K.json` file is the data in `alongthelineF_300K.dat` which has
been transformed to a Euphonic `Spectrum2D` object via binning with the
`shared/generate_compare_data/ab2tds_to_sqw.py` script.

**`cut` -> `Oclimax` directory**

This contains the input files for OClimax for a particular cut, both
`quartz.params.copy` and `quartz.params` to prevent `quartz.params`
from being overwritten by OClimax. `material.oclimax` contains the
q-points, frequencies and eigenvectors for the q-points in that cut
in Oclimax format, created by running `oclimax convert` on the corresponding
`material\cut\castep\material.phonon` file. `material_2Dmesh_scqw_TK.csv`
are the OClimax output intensities at T K. `oclimax_sqw_TK.json` is the
data in `material_2Dmesh_scqw_TK.csv` which has been transformed to a
Euphonic `Spectrum2D` object via binning with the
`shared/generate_compare_data/oclimax_to_sqw.py` script. The `run_oclimax.sh`
script will run OClimax with the relevant input files.

**`cut` -> `Euphonic` directory**

This contains output Euphonic files. `euphonic_sf_fc_TK.json` contains the
Euphonic structure factors calculated for the q-points in that cut at T K,
produced by the `shared/generate_compare_data/generate_euphonic_sf.py` script,
calculated from Euphonic frequencies calculated from the force constants. The
`euphonic_sf_phonons_TK.json` is the same as `euphonic_sf_fc_TK.json` but the
structure factors have been calculated from phonon frequencies read from the
`material.phonon` file (using the `--freqs` argument to `generate_euphonic_sf.py`).
The `euphonic_sqw_fc/phonons_TK.json` file contains the Euphonic intensities,
calculated by binning the contents of the corresponding
`euphonic_sf_fc/phonons_TK.json` with the
`shared/generate_compare_data/generate_euphonic_sqw.py` script. There are
also some files with `reduced` in the name e.g.
`euphonic_sf_fc_reduced_300K.json`, these have been created with a
symmetry-reduced (rather than full unfolded) Debye-Waller grid.

### Debye-Waller Data
The grid q-point data and Debye-Waller files (for each software as
applicable) are in the `material` -> `shared` -> `software` directory.
e.g. the `quartz` -> `shared` -> `castep` directory contains CASTEP
input/output files for gridded data for quartz.

**`shared` -> `CASTEP` directory**

This only applies for the quartz, Nb and LZO materials.
Contains a `material.castep_bin`, `material.param` and
`material.cell` CASTEP input files and `material.phonon`
CASTEP output file for a q-point grid for that material

**`shared` -> `Phonopy` directory**

Only applies for the Al material. Contains a Phonopy
`material.yaml` input file (containing the structure
and force constants) and a `material_mesh.yaml` output
file containing the q-points, frequencies and
eigenvectors for the Debye-Waller grid.

**`shared` -> `ab2tds` directory**

Contains the input files for the Ab2tds Debye-Waller calculation (`dw_input`
and `symmetry_input`), a script to run the Ab2tds DW calculation
(`run_ab2tds.sh`) and the output HDF5 file (`material.md5_code`) storing the
Debye-Waller data.

**`shared` -> `Oclimax` directory**
`material.oclimax` contains the q-points, frequencies and eigenvectors for
the q-point grid in Oclimax format, created by running `oclimax convert`
on the corresponding `material\shared\castep\material.phonon` file.

**`shared` -> `Euphonic` directory**
Contains output Euphonic files. The `euphonic_dw_fc/phonons_NNN_TK.json`
file contains a Euphonic `DebyeWaller` object calculated at T K on a
NxNxN grid, using frequencies calculated from force constants (`fc`) or
read from a CASTEP `.phonon` file (`phonon`), produced with the
`shared/generate_compare_data/generate_euphonic_dw.py` script.

### Analysis Scripts
These are contained in  the `shared` -> `generate_compare_data` directory.
What each script does is described in the docstring in the script.
