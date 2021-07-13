cp ../castep/quartz-554-full-grid.phonon .
make_TDS_Simmetrization quartz-554-full-grid.phonon symmetry_input
rm quartz-554-full-grid.phonon
make_TDS_DW quartz-554-full-grid.phonon.md5_code=0e08e97757df0c4ba9f648daf3c31078 dw_input
