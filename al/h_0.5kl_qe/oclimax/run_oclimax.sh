#cp ../phonopy/al_h_0.5kl_band.yaml .
#sudo oclimax convert -yamld al_h_0.5kl_band.yaml -o al_h_0.5kl
#rm al_h_0.5kl_band.yaml

cp ../../shared/oclimax/al_101010_full_grid.oclimax .
cp al.params.copy al.params
sudo oclimax run  al_101010_full_grid.oclimax al.params al_h_0.5kl.oclimax
rm al_101010_full_grid.oclimax al.params
