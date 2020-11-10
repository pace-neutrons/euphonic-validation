cp ../castep/quartz.phonon .
sudo oclimax convert -c quartz.phonon -o quartz
rm quartz.phonon
cp ../../shared/oclimax/quartz-666-grid.oclimax .
cp quartz.params.copy quartz.params
sudo oclimax run quartz-666-grid.oclimax quartz.params quartz.oclimax
rm quartz-666-grid.oclimax
