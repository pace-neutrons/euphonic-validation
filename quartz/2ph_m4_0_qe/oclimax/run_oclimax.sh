#cp ../castep/quartz.phonon .
#sudo oclimax convert -c quartz.phonon -o quartz
#rm quartz.phonon
cp ../../shared/oclimax/quartz-554-full-grid.oclimax .
cp quartz.params.copy quartz.params
sudo oclimax run quartz-554-full-grid.oclimax quartz.params quartz.oclimax
rm quartz-554-full-grid.oclimax
