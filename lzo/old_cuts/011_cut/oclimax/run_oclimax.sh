cp ../castep/La2Zr2O7.phonon .
sudo oclimax convert -c La2Zr2O7.phonon -o La2Zr2O7
rm La2Zr2O7.phonon
cp ../../shared/oclimax/La2Zr2O7-666-grid.oclimax .
cp La2Zr2O7.params.copy La2Zr2O7.params
sudo oclimax run La2Zr2O7-666-grid.oclimax La2Zr2O7.params La2Zr2O7.oclimax
rm La2Zr2O7-666-grid.oclimax
