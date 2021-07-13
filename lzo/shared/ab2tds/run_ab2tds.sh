cp ../castep/La2Zr2O7-444-full-grid.phonon .
make_TDS_Simmetrization La2Zr2O7-444-full-grid.phonon symmetry_input
rm La2Zr2O7-444-full-grid.phonon
make_TDS_DW La2Zr2O7-444-full-grid.phonon.md5_code=c20191af30f9ef722fe109b0d7d0c0be dw_input
