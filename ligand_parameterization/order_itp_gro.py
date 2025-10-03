
##############################################################################
#                       Functions
##############################################################################

#read gro file and classify into parts (header, atom number, atoms and box)
def leer_gro(fichero_gro):
    try:
        with open(fichero_gro, mode = "r", encoding="utf-8") as fichero:
            lineas_gro = fichero.readlines()
            header = lineas_gro[0]
            numero_atomos = lineas_gro[1]
            atomos = lineas_gro[2:-1]
            box = lineas_gro[-1]
    except Exception as e:
        print(f"Could not open GRO file, error: {e}")
        return None
    
    return header, numero_atomos, atomos, box

#Read ITP file and extract atom names
def leer_itp(fichero_itp):
    try:
        with open(fichero_itp, mode = "r", encoding="utf-8") as fichero:
            contenido_itp = fichero.readlines()
            nombres = []
            en_atomos = False
            for linea in contenido_itp:
                if linea.strip().startswith("[ atoms ]"): #section with atom names
                    en_atomos = True
                    continue
                if en_atomos:
                    if linea.strip().startswith("["):
                        break #end of atom section
                    if linea.strip().startswith(";") or not linea.strip(): #comments or empty lines
                        continue
                    partes = linea.split()
                    nombres.append(partes[4]) #add names in correct order    
        return nombres
    except Exception as e:
        print(f"Could not open ITP file, error: {e}")
        return None

# Change atom order in GRO file based on ITP names
def cambiar_orden(header, numero_atomos, atomos, box, nombres):
    contenido_ordenado = [header, numero_atomos]
    try:
        for nombre in nombres: # go through atom names from ITP
            encontrado = False #check if all atoms from itp are in gro
            for linea in atomos: #go through gro lines with atom information
                partes = linea.split()
                if partes[1] == nombre: #match between gro atom name and itp atom name
                    contenido_ordenado.append(linea) #add atoms in order in new gro file
                    encontrado = True
            if not encontrado:
                print(f"⚠️ Atom {nombre} from ITP not found in GRO file")
                    
        contenido_ordenado.append(box)
        return contenido_ordenado       
    except Exception as e:    
        print(f"Could not reorder GRO file, error: {e}")         
                


##############################################################################
#                       MENU
##############################################################################

while True:
    print("¿What do you want to do?")
    print("(1) >> Reorder GRO file to match ITP file order")
    print("(2) >> Exit")
    n = input("Choose (enter 1 o 2): ")
    
    if n == "1":
        fichero_gro = input("Enter disordered GRO file name: ")
        fichero_itp = input("Enter ITP file name with correct order: ")
        
        #Apply functions
        header, numero_atomos, atomos, box = leer_gro(fichero_gro)
        nombres = leer_itp(fichero_itp)
        contenido_ordenado = cambiar_orden(header, numero_atomos, atomos, box, nombres)
        
        
        #write new gro file with correct atom order
        try:
            with open(f"ordered_{fichero_gro}", mode = "w", encoding="utf-8") as fichero:
                fichero.writelines(contenido_ordenado)
        except Exception as e:
            print(f"Could not write ordered GRO file, error: {e}")
        
        if int(numero_atomos.strip()) != len(nombres):
            print("⚠️ Atom count in GRO file does not match actual number of atoms")
            print(f"Atom count indicated in GRO file: {numero_atomos}")
            print(f"Actual atom count in GRO file: {len(nombres)}")
        
        
        #Renumber atoms in new GRO file 
        try:
            with open(f"ordered_{fichero_gro}", mode = "r+", encoding="utf-8"  ) as fichero:
                lineas_fichero = fichero.readlines()
                header = lineas_fichero[0]
                numero_atomos = lineas_fichero[1]
                atomos = lineas_fichero[2:-1]
                box = lineas_fichero[-1]
                nuevas_lineas = [header, numero_atomos]
                contador = 1
                for linea in atomos:
                    nuevas_lineas.append(linea[:15] + f"{contador:5d}" + linea[20:])
                    contador += 1            
                 
                nuevas_lineas.append(box)
                #overwrite file
                fichero.seek(0)
                fichero.writelines(nuevas_lineas)
                fichero.truncate()  
                print("-----------------------------------------------------------------------------")
                print(f"Process successfully completed, new file created: ordered_{fichero_gro} ") 
                print("-----------------------------------------------------------------------------")

                    
        except Exception as e:
            print(f"Could not renumber GRO file, please check manually. Error: {e}")
    
       
    elif n == "2":
        print("Exiting the program...")
        print("-----------------------------------------------------------------------------")
        print("-----------------------------------------------------------------------------")
        break 
    else:
        print("Invalid input, please enter 1 or 2")

