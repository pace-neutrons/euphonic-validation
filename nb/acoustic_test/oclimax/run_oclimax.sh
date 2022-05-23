#cp ../castep/Nb-181818-s0.5-NCP19-vib-disp.phonon .
#sudo oclimax convert -c Nb-181818-s0.5-NCP19-vib-disp.phonon -o nb
#rm Nb-181818-s0.5-NCP19-vib-disp.phonon
cp ../../shared/oclimax/Nb-181818-s0.5-NCP19-vib-disp-101010-full-grid.oclimax .
cp nb.params.copy nb.params
sudo oclimax run Nb-181818-s0.5-NCP19-vib-disp-101010-full-grid.oclimax nb.params nb.oclimax
rm Nb-181818-s0.5-NCP19-vib-disp-101010-full-grid.oclimax
