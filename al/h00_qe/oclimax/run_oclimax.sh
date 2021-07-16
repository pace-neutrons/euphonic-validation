#cp ../phonopy/al_h00_band.yaml .
#sudo oclimax convert -yamld al_h00_band.yaml -o al_h00
#rm al_h00_band.yaml

cp ../../shared/oclimax/al_101010_full_grid.oclimax .
cp al.params.copy al.params
sudo oclimax run  al_101010_full_grid.oclimax al.params al_h00.oclimax
rm al_101010_full_grid.oclimax al.params
