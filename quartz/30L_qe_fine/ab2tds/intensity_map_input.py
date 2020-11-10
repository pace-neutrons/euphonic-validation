import numpy as np
APPLYTIMEREVERSAL=0
Temperature=300
resolutionfile='resolution.txt'
Saturation=0.2
lowerLimit=0
bottom_meV=0
NEUTRONCALC=1
CohB={'Si': 4.1491, 'O': 5.803}
NeutronE=1e10
branchWeight=np.ones(27).tolist()
EigScal=0
UniqueIon=-1

redStarts = [[-3, 0.0, 2.325]]
redEnds = [[-3, 0.0, -2.325]]
Nqlines = [187]
