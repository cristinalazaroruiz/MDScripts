# -*- coding: utf-8 -*-

##############################################################################
#                               Libraries
##############################################################################

import os
from Bio import PDB
from Bio.PDB import PDBParser, is_aa
from Bio.SeqUtils import seq1
import requests


##############################################################################
#                       Working directory
##############################################################################

path = r"C:\Users\usuario\Desktop\clazaro_files\PNPOx\estructuras" #change 
os.chdir(path)


##############################################################################
#                           Functions
##############################################################################

#Download PDB file from PDB

def descargar_PDB (lista, path):
    for elemento in lista:
        url =  f"https://files.rcsb.org/download/{elemento}.pdb"
        response = requests.get(url)
        
        if response.status_code == 200:
            path_elemento = f"{path}\\{elemento}.pdb"
            with open(path_elemento, "w") as file:
                file.write(response.text)
                print(f"Archivo PDB descargado y guardado en {path}")
        else:
            print(f"Ha habido un error con {elemento}. El codigo HTTP de la llamada es: {response.status_code}")



#¡¡¡Be careful with modified residues like CME!!!!!

#get sequence from PDB file
def recuperar_secuencia(fichero):
    secuencia = []
    try:
        parser = PDB.PDBParser(QUIET=True)
        structure = parser.get_structure("protein", fichero)
    except Exception as e:
        print(f"No se ha podido recuperar la secuencia. Error: {e}")
        return secuencia 
    for model in structure:
        for chain in model:
            for residue in chain:
                if is_aa(residue):
                    secuencia.append(residue.get_resname())
    
    return secuencia

#get sequence from PDB file when there are several chains:
def recuperar_secuencia_cadenas(fichero):
    secuencias = {}
    try:
        parser = PDB.PDBParser(QUIET=True)
        structure = parser.get_structure("protein", fichero)
    except Exception as e:
        print(f"No se ha podido recuperar la secuencia. Error: {e}")
        return secuencias
    
    for model in structure:
        for chain in model:
            secuencia_chain = []
            for residue in chain:
                if is_aa(residue, standard=False): #if true, only 20 standard aa will be consider. I
                    secuencia_chain.append(residue.get_resname())
            if secuencia_chain:
                secuencias[chain.id] = secuencia_chain
    
    return secuencias
    

#get sequence from CIF file when there are several chains:

def recuperar_secuencia_cadenas_CIF(fichero):
    secuencias = {}
    try:
        parser = PDB.MMCIFParser(QUIET=True)
        structure = parser.get_structure("protein", fichero)
    except Exception as e:
        print(f"No se ha podido recuperar la secuencia. Error: {e}")
        return secuencias
    
    for model in structure:
        for chain in model:
            secuencia_chain = []
            for residue in chain:
                if is_aa(residue, standard=True):
                    secuencia_chain.append(residue.get_resname())
            if secuencia_chain:
                secuencias[chain.id] = secuencia_chain
    
    return secuencias
    

#Obtain SEQRES from PDB file
def recuperar_seqres(fichero):
    secuencia = []
    try:
        with open(fichero, mode="r") as f:
            for elemento in f:
                if elemento.startswith("SEQRES"):
                    partes = elemento.strip().split()
                    secuencia.extend(partes[4:])
        return secuencia
    except Exception as e:
        print(f"No se ha recuperado la secuencia correctamente, error: {e}")
        return secuencia



#change 3-code sequence to 1-code sequence
def pasar_codigo_1letra(secuencia_tres_letras):
    try:
        secuencia = "".join(secuencia_tres_letras)
        return seq1(secuencia)
    except Exception as e:
        print(f"Error. {e} ")
        print("Se devuelve un string de la secuencia de 3 letras")
        return "".join(secuencia_tres_letras) #unusual residues will be named as X


#convert 1-code sequence to text file (txt)
def escribir_secuencia(nombre, secuencia):
    try:
        with open(f"{nombre}.txt", mode = "w") as fichero:
            fichero.write(secuencia)
    except Exception as e:
        print(f"No se ha podido crear el archivo, error: {e}")
        
        
##############################################################################
#                           Examples
##############################################################################
FPR_plegada_3_letras = recuperar_secuencia("FPR_plegado.pdb")
FPR_plegada_1_letra = pasar_codigo_1letra(FPR_plegada_3_letras)
escribir_secuencia("FPR_plegada_secuencia", FPR_plegada_1_letra)


FPR_extendida_3_letras = recuperar_secuencia("FPR_extendida.pdb")
FPR_extendida_1_letra = pasar_codigo_1letra(FPR_extendida_3_letras)
escribir_secuencia("FPR_extendida_secuencia", FPR_extendida_1_letra)        
        


##############################################################################
#                           Examples 2
##############################################################################

objetos_pymol = [] #add PDB codes. 


#download pdbs 
descargar_PDB(objetos_pymol, path)


#get sequence from each pdb from the list
#first add pdb extension
lista_pdbs = []
for objeto in objetos_pymol:
    objeto = "{}.pdb".format(objeto) 
    lista_pdbs.append(objeto)



secuencias = []
for elemento in lista_pdbs:
    secuencia = recuperar_secuencia(elemento)
    secuencias.append(secuencia)


secuencias_1_letra = []
for i in secuencias:
    secuencia = pasar_codigo_1letra(i)
    secuencias_1_letra.append(secuencia)


#dictionary pdb name - sequence
diccionario = dict(zip(objetos_pymol, secuencias_1_letra))

#write dictionary with FASTA format
with open("secuencia.txt", mode = "w") as fichero:
    for key,valor in diccionario.items():
        cabecera = "> {}".format(key)
        fichero.write(cabecera + "\n")
        fichero.write(valor+"\n")














