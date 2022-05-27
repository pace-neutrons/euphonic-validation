cp ../castep/Nb-181818-s0.5-NCP19-vib-disp.phonon .
sudo oclimax convert -c Nb-181818-s0.5-NCP19-vib-disp.phonon -o nb
rm Nb-181818-s0.5-NCP19-vib-disp.phonon

# Get 10-10-10 grid
cp ../../shared/oclimax/Nb-181818-s0.5-NCP19-vib-disp-101010-full-grid.oclimax .
# Get grid with zero eigenvectors
#cp ../castep/Nb-181818-s0.5-NCP19-vib-disp-zero-grid.phonon .
#sudo oclimax convert -c Nb-181818-s0.5-NCP19-vib-disp-zero-grid.phonon -o Nb-181818-s0.5-NCP19-vib-disp-zero-grid
#rm Nb-181818-s0.5-NCP19-vib-disp-zero-grid.phonon .

cp nb.params.copy nb.params
sudo oclimax run Nb-181818-s0.5-NCP19-vib-disp-101010-full-grid.oclimax nb.params nb.oclimax
#sudo oclimax run Nb-181818-s0.5-NCP19-vib-disp-zero-grid.oclimax nb.params nb.oclimax


rm Nb-181818-s0.5-NCP19-vib-disp-101010-full-grid.oclimax
#rm Nb-181818-s0.5-NCP19-vib-disp-zero-grid.oclimax
