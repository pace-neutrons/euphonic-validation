cp ../castep/Nb-181818-s0.5-NCP19-vib-disp-666-grid.phonon .
make_TDS_Simmetrization Nb-181818-s0.5-NCP19-vib-disp-666-grid.phonon symmetry_input
make_TDS_DW Nb-181818-s0.5-NCP19-vib-disp-666-grid.phonon.md5_code=0ba8d6e79abe5a2e06d879c26e51c190 dw_input
rm Nb-181818-s0.5-NCP19-vib-disp-666-grid.phonon
