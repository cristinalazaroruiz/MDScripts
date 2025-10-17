import numpy as np
from gromacs.fileformats.xpm import XPM

#Note that GROMACS, GROMACS WRAPPER and numpy must be install in your system. 
print("WARNING: Note that GROMACS, GROMACS WRAPPER and numpy must be install in your system")
# Upload XPM file
x = XPM(input("Insert XPM file name: "), reverse=True)

try:
    #get matrix as numpy array
    mat = x.array
    
    # Save as .dat with numpy
    np.savetxt("dist_matrix.dat", mat, fmt="%.5f")
    print(f"✅ Matrix saved as dist_matrix.dat with shape {mat.shape}")
    print(mat)
except Exception as e:
    print("****************************************************************")
    print("Error. Impossible to make conversion of XPM to DAT")
    print(f"Error: {e}")
    print("****************************************************************")
