# -*- coding: utf-8 -*-

#Ask user which files must be used
mol_nomenclatura = input("MOL2 with correct nomenclature: ")
mol_Gaussian = input("MOL2 from Gaussian: ")

#Get correct nomenclature from correct MOL2
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
    print(f"❌ Error reading nomenclature file: {e}")
            
        
#change atom names and id from mol2 from Gaussian
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
    print(f"❌ Error processing Gaussian mol2: {e}")
                
                
        
#save new mol2 with appropiate geometry and nomenclature

nombre_salida = f"nomenclatura_{mol_Gaussian}"
try:
    with open(nombre_salida, "w", encoding="utf-8") as out:
        out.writelines(lineas_modificadas)
except Exception as e:
    print(f"❌ Error saving output mol2: {e}")

print(f"✅ File created: {nombre_salida}")

if len(numeros) != len(nomenclatura):
    print("⚠️ Warning: atom IDs and names list have inconsistent lengths!")
    
if contador < len(nomenclatura):
    print(f"⚠️ Warning: not all nomenclature atoms used ({contador}/{len(nomenclatura)})")
elif contador > len(nomenclatura):
    print(f"⚠️ Warning: more atoms in Gaussian mol2 than in nomenclature mol2 ({contador}/{len(nomenclatura)})")

