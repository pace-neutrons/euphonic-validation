import numpy as np
APPLYTIMEREVERSAL=0
Temperature=300
resolutionfile='resolution.txt'
Saturation=0.2
lowerLimit=0
bottom_meV=0
NEUTRONCALC=1
CohB={'La': 8.24, 'Zr': 7.16, 'O': 5.803}
NeutronE=1e10
branchWeight=np.ones(66).tolist()
EigScal=0
UniqueIon=-1

redStarts = [[-5., 7., 0.]]
redEnds = [[-5., 7., -8.]]
Nqlines = [81]
