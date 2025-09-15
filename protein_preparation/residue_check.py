# -*- coding: utf-8 -*-

##############################################################################
#                               Libraries
##############################################################################

import os
from Bio import PDB
from Bio.PDB import PDBParser, is_aa
from Bio.SeqUtils import seq1


##############################################################################
#                       Working directory
##############################################################################

path = r"C:\Users\crist\Desktop\trabajo_unizar\FPR" #change 
os.chdir(path)


##############################################################################
#                           Functions
##############################################################################

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


#change 3-code sequence to 1-code sequence
def pasar_codigo_1letra(secuencia_tres_letras):
    try:
        secuencia = "".join(secuencia_tres_letras)
        return seq1(secuencia)
    except Exception as e:
        print(f"Error. {e} ")
        print("Se devuelve un string de la secuencia de 3 letras")
        return "".join(secuencia_tres_letras)


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
        

