#cp ../phonopy/mapbcl3_hkl_band.yaml .
#sudo oclimax convert -yamld mapbcl3_hkl_band.yaml -o mapbcl3_hkl
#rm mapbcl3_hkl_band.yaml

cp ../../shared/oclimax/mapbcl3_666_full_grid.oclimax .
cp mapbcl3.params.copy mapbcl3.params
sudo oclimax run  mapbcl3_666_full_grid.oclimax mapbcl3.params mapbcl3_hkl.oclimax
rm mapbcl3_666_full_grid.oclimax mapbcl3.params mapbcl3_hkl.params
