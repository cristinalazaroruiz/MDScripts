# -*- coding: utf-8 -*-

# Script to replace charges from mol2 file from the ones generated in the chg file 

###############################################################################
#                           Functions
###############################################################################

# Save charges from file .chg
def save_charges_chg(fichero_chg):
    cargas_def = []
    try:
        with open(fichero_chg, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    partes = linea.split()
                    try:
                        carga = float(partes[-1]) 
                        cargas_def.append(carga)
                    except ValueError:
                        raise ValueError(f"Could not convert the following line from .chg to a number: {linea}")
            return cargas_def

    except Exception as e:
        print(f"Cannot open {fichero_chg}, error: {e}")
        return cargas_def 


# Get charges from .mol2 and change them
def change_charges_mol2(fichero_mol2, cargas_def, fichero_chg):
    salida = []
    i_carga = 0
    try:
        with open(fichero_mol2, "r", encoding="utf-8") as m:
            en_atomos = False
            for linea in m:
                if linea.startswith("@<TRIPOS>ATOM"):
                    en_atomos = True
                    salida.append(linea)
                    continue
                elif linea.startswith("@<TRIPOS>") and en_atomos:
                    en_atomos = False
                    salida.append(linea)
                    continue
    
                if en_atomos:
                    partes = linea.strip().split()
                    if i_carga < len(cargas_def):
                        nueva_carga = cargas_def[i_carga]
    
                        # Rebuild mol2 format
                        nueva_linea = "{:>7} {:<4} {:>10.4f} {:>10.4f} {:>10.4f} {:<5} {:>3} {:<6} {:>12.6f}\n".format(
                            int(partes[0]),      # atom_id
                            partes[1],           # atom_name
                            float(partes[2]),    # x
                            float(partes[3]),    # y
                            float(partes[4]),    # z
                            partes[5],           # atom_type
                            int(partes[6]),      # subst_id
                            partes[7],           # subst_name
                            nueva_carga          # charge
                        )
                        salida.append(nueva_linea)
                        i_carga += 1
                    else:
                        raise ValueError(
                            f"Not enough charges in {fichero_chg}. "
                            f"The .mol2 file requires at least {i_carga+1}, but only {len(cargas_def)} are available."
                        )
                else:
                    salida.append(linea)
                    
        return salida, i_carga
    
    except Exception as e:
        print(f"Cannot open {fichero_mol2}, error: {e}")
        return salida, i_carga


###############################################################################
#                           Menu
###############################################################################

while True:
    print("\nWhat do you want to do?")
    print("(1) >> Change MOL2 charges with CHG charges")
    print("(2) >> Exit")
    n = input("Choose (enter 1 or 2): ")
    
    if n == "1":
        fichero_mol2 = input("Enter file name with extension MOL2: ")
        fichero_chg = input("Enter file name with extension CHG: ")
        
        cargas_def = save_charges_chg(fichero_chg)
        if not cargas_def:
            print("No charges loaded — check your CHG file.")
            continue

        salida, i_carga = change_charges_mol2(fichero_mol2, cargas_def, fichero_chg)
        
        nombre_salida = f"ready_{fichero_mol2}"
        try:
            with open(nombre_salida, "w", encoding="utf-8") as out:
                out.writelines(salida)
            
            print(f"✅ File created: {nombre_salida}")
            print(f"   {i_carga} charges were replaced from {len(cargas_def)} available.")
        except Exception as e:
            print(f"Cannot write new MOL2 {nombre_salida} with correct charges.")
            print(f"Error: {e}")
        
    elif n == "2":
        print("\nExiting program... 👋")
        print("-------------------------------------------------------------------------------")
        break 
    else:
        print("Invalid input, please enter 1 or 2.")


