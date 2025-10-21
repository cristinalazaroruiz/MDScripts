#Para algunos programas, necesitamos que nuestra proteina dimerica tenga dos 
#cadenas con numeracion distinta (la B de forma consecutiva a la A).


###############################################################################
#                           Functions
###############################################################################

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
        print(f"Error al cargar el fichero {fichero}")
        print(f"Detalles del error: {e}")
        return cadena_A, cadena_B, FAD_A, FAD_B, NAD



def cambiar_cadenaB(cadena_A, cadena_B):
    nueva_cadena_B = []
    try:
        if not cadena_A:
            raise ValueError("No se encontró la cadena A en el fichero PDB.")
        if not cadena_B:
            raise ValueError("No se encontró la cadena B en el fichero PDB.")

        #prmero recuperamos la info de cual es el ultimo residuo cadena A
        #y generamos nuestro contador
        
        ultima_linea_A = cadena_A[-1]
        ultimo_residuo_cadena_A = int(ultima_linea_A[22:26])
        contador_cadena_B = ultimo_residuo_cadena_A +1
        
        # Seguimiento del residuo anterior para saber cuándo cambia
        residuo_actual = cadena_B[0][17:26] #incluimos resName y resSeq
        
        for elemento in cadena_B:
            residuo = elemento[17:26]

            # Si el residuo cambia, aumentamos el contador
            if residuo != residuo_actual:
                contador_cadena_B += 1
                residuo_actual = residuo

            # Sustituimos el número del residuo en la línea
            nuevo_num = str(contador_cadena_B).rjust(4)
            nueva_linea = elemento[:22] + nuevo_num + elemento[26:]
            nueva_cadena_B.append(nueva_linea)
            
        return nueva_cadena_B
        
    
    except Exception as e:
        
        print("Error al renumerar la cadena B")
        print(f"Detalles del error: {e}")
        
    return nueva_cadena_B



def escribir_nuevo_pdb(fichero, cadena_A, nueva_cadena_B, FAD_A, FAD_B, NAD):
    try:
        with open(f"nuevo_{fichero}", "w", encoding="utf-8") as f:
            f.writelines(cadena_A + nueva_cadena_B + FAD_A +FAD_B + NAD)
    except Exception as e:
        print(f"Error al escribir la nueva version de {fichero}")
        print(f"Detalles del error: {e}")
        
        
        
###############################################################################
#                           MENU
###############################################################################

while True:
    print("¿Qué quieres hacer?\n")
    print("(1) >> Renumerar cadena B")
    print("(2) >> Salir\n")
    n = input("Write an option (1 or 2): ")
    
    if n == "1":
        
        print("\n⚠️ Este script asume: ")
        print("Proteina dimerica con cadenas A y B")
        print("Dos FADs en cadenas C y D")
        print("Puede tener un NAD en una cadena E")
        print("Revisa el PDB y comprueba que se cumplen estos requisitos\n")
              
        
        fichero = input("Nombre del fichero PDB: ")
        
        cadena_A, cadena_B, FAD_A, FAD_B, NAD = leer_pdb(fichero)
        nueva_cadena_B = cambiar_cadenaB(cadena_A, cadena_B)
        escribir_nuevo_pdb(fichero, cadena_A, nueva_cadena_B, FAD_A, FAD_B, NAD)
        
        print(f"Fichero {fichero} actualizado con éxito")
    
    
    elif n == "2":
        
        print("Saliendo...")
        
        break 
    
    else:
        print("Error en el input. Escribe 1 ó 2. ")
        
        
        



















        
        
        
        
        
        
        
        
        
        
