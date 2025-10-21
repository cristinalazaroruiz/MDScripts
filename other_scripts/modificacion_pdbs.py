
# For some programs, you may need your hodimer protein to have two chains (A and B)
# with different nomenclature (chain B starting from chain A last residue)

###############################################################################
#                           Functions
###############################################################################

#read PDB and save information of all chains
def leer_pdb(fichero):
    cadena_A = []
    cadena_B = []
    FAD_A = []
    FAD_B = []
    NAD = []
    try:
        with open(fichero, "r", encoding="utf-8") as f:
            for linea in f:
                if len(linea) < 22:
                    continue  # línea demasiado corta, la ignoramos
                if not (linea.startswith("ATOM") or linea.startswith("HETATM")):
                    continue  # solo queremos coordenadas atómicas
                if linea[21] == "A":
                    cadena_A.append(linea)
                elif linea[21] == "B":
                    cadena_B.append(linea)
                elif linea[21] == "C":
                    FAD_A.append(linea)
                elif linea[21] == "D":
                    FAD_B.append(linea)
                elif linea[21] == "E":
                    NAD.append(linea)
                
        return cadena_A, cadena_B, FAD_A, FAD_B, NAD
            
    except Exception as e:
        print(f"Error in loading file {fichero}")
        print(f"Error details: {e}")
        return cadena_A, cadena_B, FAD_A, FAD_B, NAD


#change chain B nomenclature
def cambiar_cadenaB(cadena_A, cadena_B):
    nueva_cadena_B = []
    try:
        if not cadena_A:
            raise ValueError("Chain A not found in PDB file.")
        if not cadena_B:
            raise ValueError("Chain B not found in PDB file.")

        # Firstly, we get last chain A residue number 
        # Generate our counter for chain B
        
        ultima_linea_A = cadena_A[-1]
        ultimo_residuo_cadena_A = int(ultima_linea_A[22:26])
        contador_cadena_B = ultimo_residuo_cadena_A +1
        
        # Get current residue (with resName and resSeq) to know when it changes
        residuo_actual = cadena_B[0][17:26] #include resName y resSeq
        
        for elemento in cadena_B:
            residuo = elemento[17:26]

            # If residue changes, we increase the counter
            if residuo != residuo_actual:
                contador_cadena_B += 1
                residuo_actual = residuo

        
            # Replace residue number with the counter
            nuevo_num = str(contador_cadena_B).rjust(4)
            nueva_linea = elemento[:22] + nuevo_num + elemento[26:]
            nueva_cadena_B.append(nueva_linea)
            
        return nueva_cadena_B
        
    
    except Exception as e:
        
        print("Error in renumbering chain B")
        print(f"Error details: {e}")
        
    return nueva_cadena_B


#Write new file (no overwrite)
def escribir_nuevo_pdb(fichero, cadena_A, nueva_cadena_B, FAD_A, FAD_B, NAD):
    try:
        with open(f"nuevo_{fichero}", "w", encoding="utf-8") as f:
            f.writelines(cadena_A + nueva_cadena_B + FAD_A +FAD_B + NAD)
    except Exception as e:
        print(f"Error when updating file: {fichero}")
        print(f"Error details: {e}")
        
        
        
###############################################################################
#                           MENU
###############################################################################

while True:
    print("What do you want to do?\n")
    print("(1) >> Renumber chain B")
    print("(2) >> Exit\n")
    n = input("Write an option (1 or 2): ")
    
    if n == "1":
        
        print("\n⚠️ This script assumes: ")
        print("Homodimer protein with chains A and B")
        print("Two FADs in chains C y D")
        print("May have NAD in chain E")
        print("Revise PDB and check all requirements are fulfiled\n")
              
        
        fichero = input("Enter PDB name: ")
        
        cadena_A, cadena_B, FAD_A, FAD_B, NAD = leer_pdb(fichero)
        nueva_cadena_B = cambiar_cadenaB(cadena_A, cadena_B)
        escribir_nuevo_pdb(fichero, cadena_A, nueva_cadena_B, FAD_A, FAD_B, NAD)
        
        print(f"File {fichero} successfully")
    
    
    elif n == "2":
        
        print("Exiting...")
        
        break 
    
    else:
        print("Error in input. Write 1 or 2. ")
        
        
        



















        
        
        
        
        
        
        
        
        
        
