# -*- coding: utf-8 -*-

# Pedir nombres de los ficheros
fichero_mol2 = input("Escribe el nombre del fichero mol2: ")
fichero_chg = input("Escribe el nombre del fichero chg: ")

# Guardar las cargas del fichero .chg
cargas_def = []
with open(fichero_chg, "r", encoding="utf-8") as f:
    for linea in f:
        linea = linea.strip()
        if linea:
            partes = linea.split()
            try:
                carga = float(partes[-1])  # último valor
                cargas_def.append(carga)
            except ValueError:
                raise ValueError(f"No se pudo convertir en número la línea del .chg: {linea}")

# Accedemos a las cargas del fichero .mol2 y las cambiamos
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

                # Reconstruir con formato fijo (ajustado a lo habitual en mol2)
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
                    f"No hay suficientes cargas en {fichero_chg}. "
                    f"El .mol2 requiere al menos {i_carga+1}, pero solo hay {len(cargas_def)}."
                )
        else:
            salida.append(linea)

# Guardar el resultado en un nuevo archivo
nombre_salida = f"ready_{fichero_mol2}"
with open(nombre_salida, "w", encoding="utf-8") as out:
    out.writelines(salida)

print(f"✅ Archivo generado: {nombre_salida}")
print(f"   Se reemplazaron {i_carga} cargas de {len(cargas_def)} disponibles.")
