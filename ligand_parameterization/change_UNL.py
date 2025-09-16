# Ask user to write MOL2 file and the desired name for the ligand
fichero_mol = input("Write the MOL2 file name: ")
nombre_ligando = input("Write the desired name for your ligand: ")

# Store modified lines
lineas_modificadas = []
in_atoms = False

try:
    with open(fichero_mol, mode="r") as fichero:
        for linea in fichero:
            if "@<TRIPOS>ATOM" in linea:
                in_atoms = True
                lineas_modificadas.append(linea)
                continue
            elif "@<TRIPOS>BOND" in linea:
                in_atoms = False
                lineas_modificadas.append(linea)
                continue

            if in_atoms:
                partes = linea.strip().split()
                if len(partes) >= 9:
                    # Reemplazar nombre del residuo (columna 8)
                    partes[7] = nombre_ligando
                    # Reconstruir línea con formato fijo
                    linea = (
                        f"{int(partes[0]):>7d} "   # atom_id
                        f"{partes[1]:<8s}"         # atom_name
                        f"{float(partes[2]):>10.4f} "
                        f"{float(partes[3]):>10.4f} "
                        f"{float(partes[4]):>10.4f} "
                        f"{partes[5]:<6s}"
                        f"{int(partes[6]):>5d} "
                        f"{partes[7]:<6s}"
                        f"{float(partes[8]):>11.4f}\n"
                    )
            lineas_modificadas.append(linea)

except Exception as e:
    print(f"❌ Error reading mol2 file: {e}")

# Write a new MOL2 file
try:
    nuevo_fichero = f"new_{fichero_mol}"
    with open(nuevo_fichero, mode="w") as fichero:
        fichero.writelines(lineas_modificadas)
    print(f"✅ Ligand name successfully updated in {nuevo_fichero}")
except Exception as e:
    print(f"❌ Error processing mol2 file: {e}")