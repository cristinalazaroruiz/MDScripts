import numpy as np
from gromacs.fileformats.xpm import XPM

# Cargar el archivo .xpm
x = XPM(input("Escribe el nombre de la matriz en XPM: "), reverse=True)

try:
    # Obtener la matriz como numpy array
    mat = x.array  # según documentación
    
    # Guardar como .dat
    np.savetxt("dist_matrix.dat", mat, fmt="%.5f")
    print(f"✅ Matriz guardada en dist_matrix.dat con forma {mat.shape}")
    print(mat)
except Exception as e:
    print("****************************************************************")
    print("Error. No se ha podido hacer la conversión")
    print(f"Error: {e}")
    print("****************************************************************")
