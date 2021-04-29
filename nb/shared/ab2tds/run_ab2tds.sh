cp ../castep/Nb-181818-s0.5-NCP19-vib-disp-101010-full-grid.phonon .
make_TDS_Simmetrization Nb-181818-s0.5-NCP19-vib-disp-101010-full-grid.phonon symmetry_input
rm Nb-181818-s0.5-NCP19-vib-disp-101010-full-grid.phonon
make_TDS_DW Nb-181818-s0.5-NCP19-vib-disp-101010-full-grid.phonon.md5_code=7fb08943874c47b899e49215a732ae84 dw_input
