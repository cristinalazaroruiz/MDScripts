# -*- coding: utf-8 -*-

###############################################################################
#                           Functions
###############################################################################


#get correct nomenclature from correct MOL2
def get_correct_nomenclature(mol_nomenclatura):
    numeros = []
    nomenclatura = []
    en_atom_section = False
    try:
        with open(mol_nomenclatura, "r", encoding="utf-8") as f:
            for linea in f:
                if "@<TRIPOS>ATOM" in linea:
                    en_atom_section = True
                    continue
                if "@<TRIPOS>BOND" in linea:
                    break
                if en_atom_section:
                    partes = linea.strip().split()
                    if len(partes) >= 2:
                        numeros.append(partes[0])
                        nomenclatura.append(partes[1])
    except Exception as e:
        print(f"❌ Error reading nomenclature file {mol_nomenclatura}: {e}")
    
    return numeros, nomenclatura 


#change atom names and id from mol2 from Gaussian
def change_nomenclature(mol_Gaussian, numeros, nomenclatura):
    contador = 0
    en_atom_section = False
    lineas_modificadas = []
    try:
        with open(mol_Gaussian, "r", encoding="utf-8") as f:
            for linea in f:
                if "@<TRIPOS>ATOM" in linea:
                    en_atom_section = True
                    lineas_modificadas.append(linea)
                    continue
                elif "@<TRIPOS>BOND" in linea:
                    en_atom_section = False
                    lineas_modificadas.append(linea)
                    continue
                if en_atom_section:
                    partes = linea.strip().split()
                    if len(partes) >= 2 and contador < len(nomenclatura):
                        partes[0] = numeros[contador]
                        partes[1] = nomenclatura[contador]
                        contador += 1
                        # reconstruir la línea con formato tabular
                        linea = (f"{partes[0]:>7} {partes[1]:<8} {partes[2]:>10} {partes[3]:>10} "
                                 f"{partes[4]:>10} {partes[5]:<7} {partes[6]:>5} {partes[7]:<8} "
                                 f"{partes[8]:>10}\n")
                        
                lineas_modificadas.append(linea)
    except Exception as e:
        print(f"❌ Error processing Gaussian mol2 {mol_Gaussian}: {e}")
                    
    return lineas_modificadas, contador



###############################################################################
#                           Menu
###############################################################################

while True:
    
    print("¿What do you want to do?")
    print("(1) >> Apply correct nomenclature to Gaussian MOL2")
    print("(2) >> Exit")
    n = input("Choose (enter 1 o 2): ")
    
    if n == "1":
        
        #Ask user which files must be used
        mol_nomenclatura = input("MOL2 with correct nomenclature: ")
        mol_Gaussian = input("MOL2 from Gaussian: ")
        
        #Apply functions
        numeros, nomenclatura = get_correct_nomenclature(mol_nomenclatura)
        lineas_modificadas, contador = change_nomenclature(mol_Gaussian, numeros, nomenclatura)
        
        #save new mol2 with appropiate geometry and nomenclature
        nombre_salida = f"nomenclatura_{mol_Gaussian}"
        try:
            with open(nombre_salida, "w", encoding="utf-8") as out:
                out.writelines(lineas_modificadas)
        except Exception as e:
            print(f"❌ Error saving output mol2 {nombre_salida}: {e}")

        print(f"✅ File created: {nombre_salida}")

        if len(numeros) != len(nomenclatura):
            print(f"⚠️ Warning: atom IDs and names list have inconsistent lengths! in {nombre_salida}")
            
        if contador < len(nomenclatura):
            print(f"⚠️ Warning: not all nomenclature atoms used in {nombre_salida}: ({contador}/{len(nomenclatura)})")
        elif contador > len(nomenclatura):
            print(f"⚠️ Warning: more atoms in Gaussian mol2 than in nomenclature mol2 in {nombre_salida}: ({contador}/{len(nomenclatura)})")
        
    elif n == "2":
        print("Exiting the program...")
        print("-----------------------------------------------------------------------------")
        print("-----------------------------------------------------------------------------")
        break 
    
    else:
        print("Invalid input, please enter 1 or 2")

    
    



