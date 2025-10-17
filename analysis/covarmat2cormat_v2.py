import numpy as np
from gromacs.fileformats.xpm import XPM

print("⚠ WARNING: GROMACS, GROMACS WRAPPER and numpy must be installed in your system\n")

###############################################################################
#                           Functions
##############################################################################

#Convert covariance matrix in XPM from GROMACS to DAT format
def xpm2dat(covariance_XPM):
    mat = None
    try:
        #get matrix as numpy array
        x = XPM(covariance_XPM)
        mat = x.array
        
        #conversion to float
        mat = np.array(mat, dtype=float)
        
        # Save as .dat with numpy
        np.savetxt("covar_matrix.dat", mat, fmt="%.5f")
        print(f"✅ Matrix saved as covar_matrix.dat with shape {mat.shape}")
        print(f"Matrix preview (top-left 5x5):\n{mat[:5, :5]}")
        return mat
        
    except Exception as e:
        print("****************************************************************")
        print("Error. Impossible to make covariance conversion from XPM to DAT")
        print(f"Error details: {e}")
        print("****************************************************************")
        return mat


#Adapt matrix to AMBER format (compatible with SPMweb server)
#GROMACS calculates the covariance matrix for X,Y,Z coordenates for each atom
#AMBER calculates the covariance matrix per atom
def collapse_3D_covariance(cov3D):
    """
    Collapse 3N x 3N covariance to N x N by averaging over x,y,z coordinates
    """
    try:
        N = cov3D.shape[0] // 3 #number of atoms (each atom 3 coordinates)
        collapsed = np.zeros((N, N)) #new matrix Natoms x Natoms
        for i in range(N):
            for j in range(N):
                sub = cov3D[3*i:3*i+3, 3*j:3*j+3] #data per atom (3 files and 3 columns)
                collapsed[i, j] = np.trace(sub) / 3.0 #average per atom
        print("Shape of loaded covariance matrix:", cov3D.shape)
        print(f"✅ Collapsed covariance matrix to shape {collapsed.shape} (Amber style)")
        np.savetxt("covar_amber.dat", collapsed, fmt="%.5f")
        return collapsed
    except Exception as e:
        print("Error in collapsing to AMBER format")
        print(f"Error details: {e}")



#Transform covariance matrix (in numpy format) to correlation matrix and
#writes the correlation matrix in DAT file
def cov2cor(mat):
    """
    Convert covariance matrix in correlation matrix
    : mat = covariance matrix (np.ndarray)
    """
    #Get the inverse of the standar deviation of each variable
    try:
        D = 1 / np.sqrt(np.diag(mat))
        D[np.isinf(D)] = 0  # prevents division by 0
        D[np.isnan(D)] = 0 #prevents NaNs
        
        # Normalize
        correlation = D[:, None] * mat * D[None, :]  
        
        # Force diagonal to be 1
        np.fill_diagonal(correlation, 1.0)
        
        #save results
        np.savetxt("cor_matrix.dat", correlation, fmt="%.5f")
        
        print("Diagonal of collapsed covariance matrix:", np.diag(collapsed))
        print("✅ correlation matrix generated successfully")
        print("✅ Matrix saved as cor_matrix.dat")
        
        return correlation
        
        

    except Exception as e:
        print("❌ Error: Failed to generate correlation matrix.")
        print(f"Error details: {e}")
        return None
        
        
    
###############################################################################
#                               MENU
##############################################################################

#Get covar matrix and generate DAT file
covariance_XPM = input("Write your covar matrix XPM format: ")
mat =xpm2dat(covariance_XPM)

if mat is not None:
     collapsed = collapse_3D_covariance(mat)
     if collapsed is not None:
         correlation = cov2cor(collapsed)
         print("🎉 Process completed successfully!")
     else:
        print("❌ Failed to generate correlation matrix.")
        
else:
    print("❌ Failed to load covariance matrix.")






