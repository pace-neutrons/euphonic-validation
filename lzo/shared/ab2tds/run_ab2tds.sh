cp ../castep/La2Zr2O7-666-grid.phonon .
make_TDS_Simmetrization La2Zr2O7-666-grid.phonon symmetry_input
rm La2Zr2O7-666-grid.phonon
make_TDS_DW La2Zr2O7-666-grid.phonon.md5_code=801b2c549e4ec5a50059b1eb2a5a3778 dw_input
