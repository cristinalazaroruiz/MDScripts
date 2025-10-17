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
covariance = xpm2dat(covariance_XPM)

if covariance is not None:
    cor_matrix = cov2cor(covariance)
    if cor_matrix is not None:
        print("✅ Process completed successfully")
    else:
        print("Something went wrong while generating the correlation matrix.")
else:
    print("Something went wrong while generating the covariance matrix")





