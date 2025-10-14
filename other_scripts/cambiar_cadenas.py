# -*- coding: utf-8 -*-

# Script to make chain B residue numbering consistent with chain A in a PDB file.
# Suitable only for homodimeric proteins.



###############################################################################
#                           Functions
###############################################################################

def leer_pdb(fichero):
    info_cadena_A = []
    try:
        with open(fichero, "r", encoding="utf-8") as f:
            for linea in f:
                if linea.startswith(("ATOM", "HETATM")) and linea[21] == "A":
                    resnum = linea[22:26].strip()
                    info_cadena_A.append(resnum)
    except Exception as e:
        print(f"Error reading file {fichero}: {e}")
    return info_cadena_A


def cambiar_cadenas(fichero, info_cadena_A):
    info_actualizada = []
    try:
        with open(fichero, "r", encoding="utf-8") as f:
            lineas = [l for l in f if l.startswith(("ATOM", "HETATM"))]
            
        #Get info only from chain B
        lineas_B = [l for l in lineas if l[21] == "B"]

        # --- Validation of chain length (A and B) ---
        len_A = len(info_cadena_A)
        len_B = len(lineas_B)

        if len_A != len_B:
            print(f"⚠️ Warning: Chain A has {len_A} residues and B has {len_B}.")
            if len_B > len_A:
                print("   → Only first residues from B will be modified.")
            else:
                print("   → Some numbers from A will not be used.")

        # --- Rewrite file ---
        info_actualizada = []
        contador = 0

        with open(fichero, "r", encoding="utf-8") as f:
            for linea in f:
                if linea.startswith(("ATOM", "HETATM")) and linea[21] == "B":
                    if contador < len(info_cadena_A):
                        nueva_linea = (
                            linea[:22]
                            + f"{int(info_cadena_A[contador]):4d}"
                            + linea[26:]
                        )
                        info_actualizada.append(nueva_linea)
                        contador += 1
                    else:
                        #No more numbers in chain A > rest will not be modified
                        info_actualizada.append(linea)
                else:
                    info_actualizada.append(linea)

    except Exception as e:
        print(f"Error updating chains in {fichero}: {e}")

    return info_actualizada



def escribir_nuevo_pdb(fichero, info_actualizada):
    try:
        with open(f"nuevo_{fichero}", "w", encoding="utf-8") as f:
            f.writelines(info_actualizada)
    except Exception as e:
        print(f"Error writing new file {fichero}: {e}")


        


###############################################################################
#                           Menu
###############################################################################

while True:
    print("What do you want to do?\n")
    print("(1) >> Change chain B numbering from a PDB")
    print("(2) >> Exit\n")
    n = input("Write an option (1 or 2): ")
    
    if n == "1":
        fichero = input("Enter PDB file name to modify: ")
        info_cadena_A = leer_pdb(fichero)
        info_actualizada = cambiar_cadenas(fichero, info_cadena_A)
        escribir_nuevo_pdb(fichero, info_actualizada)
        print(f"File {fichero} updated successfully")
    
    
    elif n == "2":
        
        print("Exiting...")
        
        break 
    
    else:
        print("Error in input. Write 1 or 2. ")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        