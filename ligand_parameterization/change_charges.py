# -*- coding: utf-8 -*-

#Script to replace charges from mol2 file from the ones generated in the chg file 

# Ask users for file names (mol2 and chg)
fichero_mol2 = input("Enter file name with extension MOL2: ")
fichero_chg = input("Enter file name with extension CHG: ")

# Save charges from file .chg
cargas_def = []
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

# Get charges from .mol2 and change them
salida = []
i_carga = 0
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

# Save the result to a new file
nombre_salida = f"ready_{fichero_mol2}"
with open(nombre_salida, "w", encoding="utf-8") as out:
    out.writelines(salida)

print(f"✅ File created: {nombre_salida}")
print(f"    {i_carga} charges were replaced from  {len(cargas_def)} available.")
